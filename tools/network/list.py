"""
Network list tool - List user-defined networks.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_network_list",
    "category": "network",
    "description": "List user-defined networks",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["list", "networks", "ls"],
}


async def acms_network_list(quiet: bool = False, format: str = "table") -> str:
    """List user-defined networks."""
    cmd_args = ["network", "ls"]
    if quiet:
        cmd_args.append("--quiet")
    if format != "table":
        cmd_args.extend(["--format", format])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_network_list)
