"""
Shared utilities for ACMS MCP tools.
"""
from typing import TypeAlias, Optional, List, Dict, Any, Set
import asyncio
import logging
import json
import os
import time

logger = logging.getLogger("ACMS")

CommandResult: TypeAlias = Dict[str, Any]

# Configuration from environment variables
COMMAND_TIMEOUT = int(os.getenv("ACMS_COMMAND_TIMEOUT", "300"))  # 5 minutes default
MAX_CONCURRENT_COMMANDS = int(os.getenv("ACMS_MAX_CONCURRENT", "10"))
MAX_ARG_LENGTH = int(os.getenv("ACMS_MAX_ARG_LENGTH", "65536"))  # 64KB per argument

# Concurrency control
_command_semaphore = asyncio.Semaphore(MAX_CONCURRENT_COMMANDS)
_active_processes: Set[asyncio.subprocess.Process] = set()


def _validate_container_arg(arg: str) -> str:
    """
    Validate container command arguments to prevent command injection.

    Args:
        arg: Command argument to validate

    Returns:
        str: Validated argument

    Raises:
        ValueError: If argument contains forbidden characters or exceeds length limit
    """
    if not isinstance(arg, str):
        raise ValueError(f"Argument must be a string, got {type(arg).__name__}")

    # Check argument length to prevent DoS via huge arguments
    if len(arg) > MAX_ARG_LENGTH:
        raise ValueError(
            f"Argument exceeds maximum length of {MAX_ARG_LENGTH} characters "
            f"(got {len(arg)} characters)"
        )

    # Disallow dangerous characters that could be used for command injection
    forbidden_chars = [";", "|", "&", "$", "`", "\n", "\r", "\x00"]
    for char in forbidden_chars:
        if char in arg:
            raise ValueError(f"Invalid character '{repr(char)}' in argument.")

    # Additional check for shell metacharacters
    if arg.strip().startswith("-") and any(c in arg for c in ["$(", "${", "`"]):
        raise ValueError(f"Argument appears to contain shell command substitution: {arg}")

    return arg


async def run_container_command(*args: str, timeout: Optional[int] = None) -> CommandResult:
    """
    Execute a container command and return the result with timeout and concurrency control.

    Args:
        *args: Command arguments to pass to container CLI
        timeout: Optional timeout in seconds (defaults to COMMAND_TIMEOUT env var)

    Returns:
        Dict[str, Any]: Command execution result containing stdout, stderr, return_code, command, and duration

    Raises:
        RuntimeError: If command execution fails or times out
        ValueError: If arguments contain forbidden characters
    """
    # Validate all arguments to prevent command injection
    try:
        validated_args = [_validate_container_arg(arg) for arg in args]
    except ValueError as e:
        logger.error(f"Argument validation failed: {e}")
        raise ValueError(f"Invalid command argument: {e}")

    cmd = ["container"] + validated_args
    timeout_value = timeout if timeout is not None else COMMAND_TIMEOUT

    # Use semaphore to limit concurrent commands
    async with _command_semaphore:
        active_count = MAX_CONCURRENT_COMMANDS - _command_semaphore._value
        logger.info(
            f"Executing: {' '.join(cmd)} "
            f"(active: {active_count}/{MAX_CONCURRENT_COMMANDS}, timeout: {timeout_value}s)"
        )

        start_time = time.time()
        process = None

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            # Track active process for graceful shutdown
            _active_processes.add(process)

            try:
                # Execute with timeout
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout_value
                )
            except asyncio.TimeoutError:
                # Kill the process on timeout
                logger.error(f"Command timed out after {timeout_value}s, killing process")
                try:
                    process.kill()
                    await process.wait()
                except Exception as kill_error:
                    logger.error(f"Error killing timed out process: {kill_error}")
                raise RuntimeError(
                    f"Command timed out after {timeout_value}s: {' '.join(cmd)}"
                )

            duration = time.time() - start_time
            stdout_text = stdout.decode("utf-8", errors="replace") if stdout else ""
            stderr_text = stderr.decode("utf-8", errors="replace") if stderr else ""

            result = {
                "stdout": stdout_text,
                "stderr": stderr_text,
                "return_code": process.returncode,
                "command": " ".join(cmd),
                "duration": duration,
            }

            # Log command completion with detailed results
            if process.returncode == 0:
                logger.info(f"Completed successfully in {duration:.2f}s (exit code: 0)")
            else:
                logger.warning(f"Failed with exit code: {process.returncode} after {duration:.2f}s")
                if stderr_text:
                    logger.warning(f"Error output: {stderr_text.strip()}")

            return result

        except asyncio.TimeoutError:
            # Re-raise timeout errors
            raise
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Exception executing command '{' '.join(cmd)}' after {duration:.2f}s: {e}"
            logger.error(error_msg)
            logger.error("Stack trace:", exc_info=True)
            raise RuntimeError(f"Failed to execute command: {e}")
        finally:
            # Always remove from active processes set
            if process is not None:
                _active_processes.discard(process)


def validate_array_parameter(param: Any, param_name: str) -> Optional[List[str]]:
    """
    Validate and normalize array parameters that may come as JSON strings or actual lists.

    Args:
        param: The parameter to validate (could be None, str, or List[str])
        param_name: Name of the parameter for error messages

    Returns:
        Optional[List[str]]: Validated list or None

    Raises:
        ValueError: If parameter is invalid
    """
    if param is None:
        return None

    if isinstance(param, list):
        # Already a list, validate all elements are strings
        if all(isinstance(item, str) for item in param):
            if len(param) == 0:
                raise ValueError(
                    f"Parameter '{param_name}' cannot be an empty array. "
                    "Either omit the parameter or provide at least one item."
                )
            return param
        else:
            raise ValueError(
                f"Parameter '{param_name}' must be a list of strings, "
                f"but contains non-string elements: "
                f"{[type(item).__name__ for item in param if not isinstance(item, str)]}"
            )

    if isinstance(param, str):
        # Try to parse as JSON array
        try:
            parsed = json.loads(param)
            if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
                if len(parsed) == 0:
                    raise ValueError(
                        f"Parameter '{param_name}' cannot be an empty array. "
                        "Either omit the parameter or provide at least one item."
                    )
                return parsed
            else:
                raise ValueError(
                    f"Parameter '{param_name}' JSON must be an array of strings, "
                    f"but got: {type(parsed).__name__}"
                )
        except json.JSONDecodeError:
            # Not JSON, treat as single string and convert to list
            return [param]

    raise ValueError(
        f"Parameter '{param_name}' must be a string, array of strings, or null, "
        f"but got: {type(param).__name__}"
    )


def format_command_result(result: CommandResult) -> str:
    """
    Format the result from a container command execution.

    Args:
        result: Dictionary containing command execution results

    Returns:
        str: Formatted result string for client response
    """
    try:
        duration = result.get("duration", 0)

        # Format response based on return code
        if result["return_code"] == 0:
            response = f"Command executed successfully:\n{result['command']}\n"
            if duration > 0:
                response += f"Duration: {duration:.3f}s\n\n"
            else:
                response += "\n"

            if result["stdout"]:
                response += f"Output:\n{result['stdout']}"
            if result["stderr"]:
                response += f"\nWarnings/Info:\n{result['stderr']}"
        else:
            response = (
                f"Command failed with exit code {result['return_code']}:\n"
                f"{result['command']}\n"
            )
            if duration > 0:
                response += f"Duration: {duration:.3f}s\n\n"
            else:
                response += "\n"

            if result["stderr"]:
                response += f"Error:\n{result['stderr']}"
            if result["stdout"]:
                response += f"\nOutput:\n{result['stdout']}"

        return response

    except Exception as e:
        logger.error(f"Error formatting command result: {e}")
        return f"Error formatting command result: {str(e)}"


async def shutdown_gracefully(timeout: int = 30) -> None:
    """
    Wait for active commands to complete before shutdown.

    Args:
        timeout: Maximum seconds to wait for commands to complete

    This function should be called during server shutdown to ensure
    all in-flight container commands complete cleanly.
    """
    if _active_processes:
        logger.info(
            f"Graceful shutdown: waiting for {len(_active_processes)} active commands "
            f"(timeout: {timeout}s)"
        )
        try:
            # Wait for all active processes to complete
            await asyncio.wait_for(
                asyncio.gather(
                    *[p.wait() for p in _active_processes],
                    return_exceptions=True
                ),
                timeout=timeout
            )
            logger.info("All active commands completed successfully")
        except asyncio.TimeoutError:
            logger.warning(
                f"Graceful shutdown timeout: {len(_active_processes)} commands still running. "
                "Forcing termination..."
            )
            # Kill remaining processes
            for process in _active_processes:
                try:
                    process.kill()
                except Exception as e:
                    logger.error(f"Error killing process during shutdown: {e}")
        except Exception as e:
            logger.error(f"Error during graceful shutdown: {e}")
    else:
        logger.info("Graceful shutdown: no active commands")


def get_command_stats() -> Dict[str, Any]:
    """
    Get statistics about command execution.

    Returns:
        Dictionary with command execution statistics
    """
    return {
        "active_processes": len(_active_processes),
        "max_concurrent": MAX_CONCURRENT_COMMANDS,
        "available_slots": _command_semaphore._value,
        "command_timeout": COMMAND_TIMEOUT,
        "max_arg_length": MAX_ARG_LENGTH,
    }
