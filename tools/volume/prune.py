"""
Volume prune tool - Remove unreferenced volumes.
"""
import logging

from tools._common.utils import run_container_command, format_command_result

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_volume_prune",
    "category": "volume",
    "description": "Remove unreferenced volumes",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["prune", "volume", "cleanup", "remove", "unused", "unreferenced"],
}


async def acms_volume_prune() -> str:
    """
    Remove unreferenced volumes.

    Removes all volumes that are not currently referenced by any containers.

    Returns:
        Results of the prune operation
    """
    try:
        cmd_args = ["volume", "prune"]

        result = await run_container_command(*cmd_args)
        return format_command_result(result)

    except Exception as e:
        logger.error(f"Failed to prune volumes: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_volume_prune)
