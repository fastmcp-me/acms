"""
System df tool - Report disk usage by resource type.
"""
import logging

from tools._common.utils import run_container_command, format_command_result

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_system_df",
    "category": "system",
    "description": "Report disk usage by resource type (images, containers, volumes)",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["df", "disk", "usage", "space", "storage", "system"],
}


async def acms_system_df(format: str = "table") -> str:
    """
    Report disk usage by resource type.

    Shows disk space usage broken down by:
    - Images
    - Containers
    - Volumes
    - Build cache

    Args:
        format: Output format (json|table; default: table)

    Returns:
        Disk usage statistics by resource type
    """
    try:
        cmd_args = ["system", "df"]

        if format != "table":
            cmd_args.extend(["--format", format])

        result = await run_container_command(*cmd_args)
        return format_command_result(result)

    except Exception as e:
        logger.error(f"Failed to get disk usage: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_df)
