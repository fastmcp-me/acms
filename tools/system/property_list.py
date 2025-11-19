"""
System property list tool - List all system properties.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_property_list",
    "category": "system",
    "description": "List all system properties",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["property", "list", "config", "settings"],
}


async def acms_system_property_list() -> str:
    """List all system properties."""
    result = await run_container_command("system", "property", "list")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_property_list)
