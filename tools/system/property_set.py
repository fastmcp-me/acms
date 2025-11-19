"""
System property set tool - Set a system property value.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_property_set",
    "category": "system",
    "description": "Set a system property value",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["property", "set", "config", "value", "update"],
}


async def acms_system_property_set(key: str, value: str) -> str:
    """Set a system property value."""
    result = await run_container_command("system", "property", "set", key, value)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_property_set)
