"""
System property get tool - Get the value of a system property.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_property_get",
    "category": "system",
    "description": "Get the value of a system property",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["property", "get", "config", "value"],
}


async def acms_system_property_get(key: str) -> str:
    """Get the value of a system property."""
    result = await run_container_command("system", "property", "get", key)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_property_get)
