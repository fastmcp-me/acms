"""
System status tool - Show container system status.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_status",
    "category": "system",
    "description": "Show container system status",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["status", "system", "info", "health"],
}


async def acms_system_status() -> str:
    """Show container system status."""
    result = await run_container_command("system", "status")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_status)
