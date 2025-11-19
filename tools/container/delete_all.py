"""
Container delete_all tool - Remove all containers.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_delete_all",
    "category": "container",
    "description": "Remove all containers",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "all", "containers", "cleanup"],
}


async def acms_container_delete_all(force: bool = False) -> str:
    """Remove all containers."""
    cmd_args = ["rm", "--all"]
    if force:
        cmd_args.append("--force")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_delete_all)
