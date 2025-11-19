"""
System DNS create tool - Create a local DNS domain for containers.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_dns_create",
    "category": "system",
    "description": "Create a local DNS domain for containers",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["dns", "create", "domain", "local"],
}


async def acms_system_dns_create(name: str) -> str:
    """Create a local DNS domain for containers."""
    result = await run_container_command("system", "dns", "create", name)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_dns_create)
