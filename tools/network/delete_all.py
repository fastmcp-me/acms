"""
Network delete_all tool - Delete all networks.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_network_delete_all",
    "category": "network",
    "description": "Delete all networks",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "all", "networks"],
}


async def acms_network_delete_all() -> str:
    """Delete all networks."""
    result = await run_container_command("network", "rm", "--all")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_network_delete_all)
