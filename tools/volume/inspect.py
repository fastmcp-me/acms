"""
Volume inspect tool - Display detailed information for volumes.
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
    "name": "acms_volume_inspect",
    "category": "volume",
    "description": "Display detailed information for volumes",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["inspect", "details", "info", "volume", "json"],
}


async def acms_volume_inspect(names: List[str]) -> str:
    """Display detailed information for volumes."""
    try:
        # Validate names parameter
        validated_names = validate_array_parameter(names, "names")
        if not validated_names:
            raise ValueError(
                "Parameter 'names' is required and cannot be empty. "
                "Provide at least one volume name to inspect."
            )

        cmd_args = ["volume", "inspect"]
        cmd_args.extend(validated_names)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except Exception as e:
        logger.error(f"Failed to inspect volume: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_volume_inspect)
