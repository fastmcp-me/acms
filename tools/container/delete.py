"""
Container delete tool - Remove one or more containers.
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
    "name": "acms_container_delete",
    "category": "container",
    "description": "Remove one or more containers",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "container", "cleanup"],
}


async def acms_container_delete(containers: List[str], force: bool = False) -> str:
    """Remove one or more containers."""
    try:
        # Validate containers parameter
        validated_containers = validate_array_parameter(containers, "containers")
        if not validated_containers:
            raise ValueError(
                "Parameter 'containers' is required and cannot be empty. "
                "Provide at least one container name to delete."
            )

        cmd_args = ["rm"]
        if force:
            cmd_args.append("--force")

        cmd_args.extend(validated_containers)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in container_delete: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_delete)
