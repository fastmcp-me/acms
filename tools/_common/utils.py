"""
Shared utilities for ACMS MCP tools.
"""
from typing import TypeAlias, Optional, List, Dict, Any
import asyncio
import logging
import json

logger = logging.getLogger("ACMS")

CommandResult: TypeAlias = Dict[str, Any]


def _validate_container_arg(arg: str) -> str:
    """
    Validate container command arguments to prevent command injection.

    Args:
        arg: Command argument to validate

    Returns:
        str: Validated argument

    Raises:
        ValueError: If argument contains forbidden characters
    """
    if not isinstance(arg, str):
        raise ValueError(f"Argument must be a string, got {type(arg).__name__}")

    # Disallow dangerous characters that could be used for command injection
    forbidden_chars = [";", "|", "&", "$", "`", "\n", "\r", "\x00"]
    for char in forbidden_chars:
        if char in arg:
            raise ValueError(f"Invalid character '{repr(char)}' in argument.")

    # Additional check for shell metacharacters
    if arg.strip().startswith("-") and any(c in arg for c in ["$(", "${", "`"]):
        raise ValueError(f"Argument appears to contain shell command substitution: {arg}")

    return arg


async def run_container_command(*args: str) -> CommandResult:
    """
    Execute a container command and return the result.

    Args:
        *args: Command arguments to pass to container CLI

    Returns:
        Dict[str, Any]: Command execution result containing stdout, stderr, return_code, and command

    Raises:
        RuntimeError: If command execution fails
        ValueError: If arguments contain forbidden characters
    """
    # Validate all arguments to prevent command injection
    try:
        validated_args = [_validate_container_arg(arg) for arg in args]
    except ValueError as e:
        logger.error(f"Argument validation failed: {e}")
        raise ValueError(f"Invalid command argument: {e}")

    cmd = ["container"] + validated_args
    logger.info(f"Executing: {' '.join(cmd)}")

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        stdout_text = stdout.decode("utf-8", errors="replace") if stdout else ""
        stderr_text = stderr.decode("utf-8", errors="replace") if stderr else ""

        result = {
            "stdout": stdout_text,
            "stderr": stderr_text,
            "return_code": process.returncode,
            "command": " ".join(cmd),
        }

        # Log command completion with detailed results
        if process.returncode == 0:
            logger.info("Completed successfully (exit code: 0)")
        else:
            logger.warning(f"Failed with exit code: {process.returncode}")
            if stderr_text:
                logger.warning(f"Error output: {stderr_text.strip()}")

        return result

    except Exception as e:
        error_msg = f"Exception executing command '{' '.join(cmd)}': {e}"
        logger.error(error_msg)
        logger.error("Stack trace:", exc_info=True)
        raise RuntimeError(f"Failed to execute command: {e}")


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
