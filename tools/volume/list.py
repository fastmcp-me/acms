"""
Volume list tool - List volumes.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_volume_list",
    "category": "volume",
    "description": "List volumes",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["list", "volumes", "ls", "storage"],
}


async def acms_volume_list(quiet: bool = False, format: str = "table") -> str:
    """List volumes."""
    cmd_args = ["volume", "ls"]
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
    )(acms_volume_list)
