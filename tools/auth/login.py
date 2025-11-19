"""
Registry login tool - Authenticate with a registry.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_registry_login",
    "category": "auth",
    "description": "Authenticate with a registry",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "keywords": ["login", "authenticate", "registry", "credentials"],
}


async def acms_registry_login(
    server: str,
    username: Optional[str] = None,
    password_stdin: bool = False,
    scheme: str = "auto",
) -> str:
    """Authenticate with a registry."""
    cmd_args = ["registry", "login"]
    if username:
        cmd_args.extend(["--username", username])
    if password_stdin:
        cmd_args.append("--password-stdin")
    if scheme != "auto":
        cmd_args.extend(["--scheme", scheme])
    cmd_args.append(server)

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_registry_login)
