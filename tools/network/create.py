"""
Network create tool - Create a new network.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_network_create",
    "category": "network",
    "description": "Create a new network",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["create", "network", "new"],
}


async def acms_network_create(name: str) -> str:
    """Create a new network."""
    result = await run_container_command("network", "create", name)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_network_create)
