"""
Container list tool - List containers with formatting options.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_list",
    "category": "container",
    "description": "List containers with formatting options",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["list", "containers", "ps", "running", "all"],
}


async def acms_container_list(
    all: bool = False, quiet: bool = False, format: str = "table"
) -> str:
    """
    List containers with formatting options.

    Args:
        all: Show all containers (default shows only running)
        quiet: Only display container IDs
        format: Output format (table, json, or template)

    Returns:
        Formatted container list output
    """
    cmd_args = ["list"]
    if all:
        cmd_args.append("--all")
    if quiet:
        cmd_args.append("--quiet")
    if format != "table":
        cmd_args.extend(["--format", format])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_list)
