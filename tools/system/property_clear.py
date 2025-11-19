"""
System property clear tool - Clear a system property.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_property_clear",
    "category": "system",
    "description": "Clear a system property",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["property", "clear", "delete", "reset", "config"],
}


async def acms_system_property_clear(key: str) -> str:
    """Clear a system property."""
    result = await run_container_command("system", "property", "clear", key)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_property_clear)
