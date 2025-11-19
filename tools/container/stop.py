"""
Container stop tool - Stop running containers gracefully.
"""
from typing import Optional, List
import logging

from tools._common.utils import (
    run_container_command,
    format_command_result,
    validate_array_parameter,
)

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_container_stop",
    "category": "container",
    "description": "Stop running containers gracefully by sending a signal",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["stop", "container", "terminate", "graceful", "shutdown"],
}


async def acms_container_stop(
    containers: List[str], signal: str = "SIGTERM", time: Optional[float] = None
) -> str:
    """Stop running containers gracefully by sending a signal."""
    try:
        # Validate containers parameter
        validated_containers = validate_array_parameter(containers, "containers")
        if not validated_containers:
            raise ValueError(
                "Parameter 'containers' is required and cannot be empty. "
                "Provide at least one container name to stop."
            )

        cmd_args = ["stop"]
        if signal != "SIGTERM":
            cmd_args.extend(["--signal", signal])
        if time is not None:
            cmd_args.extend(["--time", str(time)])

        cmd_args.extend(validated_containers)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in container_stop: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_stop)
