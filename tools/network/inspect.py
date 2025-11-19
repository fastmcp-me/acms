"""
Network inspect tool - Show detailed information about networks.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_network_inspect",
    "category": "network",
    "description": "Show detailed information about networks",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["inspect", "details", "info", "network", "json"],
}


async def acms_network_inspect(name: str) -> str:
    """Show detailed information about networks."""
    result = await run_container_command("network", "inspect", name)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_network_inspect)
