"""
Registry logout tool - Log out of a registry.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_registry_logout",
    "category": "auth",
    "description": "Log out of a registry",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "keywords": ["logout", "deauthenticate", "registry"],
}


async def acms_registry_logout(server: str) -> str:
    """Log out of a registry."""
    result = await run_container_command("registry", "logout", server)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_registry_logout)
