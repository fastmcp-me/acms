"""
Container kill tool - Immediately kill running containers.
"""
from typing import List
import logging

from tools._common.utils import (
    run_container_command,
    format_command_result,
    validate_array_parameter,
)

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_container_kill",
    "category": "container",
    "description": "Immediately kill running containers by sending a signal",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["kill", "container", "force", "terminate", "immediate"],
}


async def acms_container_kill(containers: List[str], signal: str = "KILL") -> str:
    """Immediately kill running containers by sending a signal."""
    try:
        # Validate containers parameter
        validated_containers = validate_array_parameter(containers, "containers")
        if not validated_containers:
            raise ValueError(
                "Parameter 'containers' is required and cannot be empty. "
                "Provide at least one container name to kill."
            )

        cmd_args = ["kill"]
        if signal != "KILL":
            cmd_args.extend(["--signal", signal])

        cmd_args.extend(validated_containers)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except Exception as e:
        logger.error(f"Failed to kill container: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_kill)
