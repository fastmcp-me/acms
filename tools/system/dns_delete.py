"""
System DNS delete tool - Delete a local DNS domain.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_dns_delete",
    "category": "system",
    "description": "Delete a local DNS domain",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["dns", "delete", "remove", "domain"],
}


async def acms_system_dns_delete(name: str) -> str:
    """Delete a local DNS domain."""
    result = await run_container_command("system", "dns", "rm", name)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_dns_delete)
