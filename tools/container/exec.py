"""
Container exec tool - Execute a command inside a running container.
"""
from typing import Optional, List
import shlex
import logging

from tools._common.utils import (
    run_container_command,
    format_command_result,
    validate_array_parameter,
)

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_container_exec",
    "category": "container",
    "description": "Execute a command inside a running container",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["exec", "execute", "run", "command", "container", "shell"],
}


async def acms_container_exec(
    container: str,
    command: str,
    interactive: bool = False,
    tty: bool = False,
    user: Optional[str] = None,
    env: Optional[List[str]] = None,
) -> str:
    """Execute a command inside a running container."""
    try:
        # Validate array parameters
        validated_env = validate_array_parameter(env, "env") if env is not None else None

        cmd_args = ["exec"]
        if interactive:
            cmd_args.append("--interactive")
        if tty:
            cmd_args.append("--tty")
        if user:
            cmd_args.extend(["--user", user])
        if validated_env:
            for e in validated_env:
                cmd_args.extend(["--env", e])

        # Add container name
        cmd_args.append(container)

        # Split command string into arguments for proper execution
        try:
            command_args = shlex.split(command)
            cmd_args.extend(command_args)
        except ValueError as shlex_error:
            logger.warning(
                f"Failed to parse command with shlex, using as single argument: {shlex_error}"
            )
            cmd_args.append(command)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in container_exec: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_exec)
