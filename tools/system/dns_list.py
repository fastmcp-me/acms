"""
System DNS list tool - List configured local DNS domains.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_dns_list",
    "category": "system",
    "description": "List configured local DNS domains",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["dns", "list", "domains", "local"],
}


async def acms_system_dns_list() -> str:
    """List configured local DNS domains."""
    result = await run_container_command("system", "dns", "ls")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_dns_list)
