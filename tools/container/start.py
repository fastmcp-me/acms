"""
Container start tool - Start a stopped container.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_start",
    "category": "container",
    "description": "Start a stopped container with attachment options",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["start", "container", "resume", "begin"],
}


async def acms_container_start(
    container: str, attach: bool = False, interactive: bool = False
) -> str:
    """Start a stopped container with attachment options."""
    cmd_args = ["start"]
    if attach:
        cmd_args.append("--attach")
    if interactive:
        cmd_args.append("--interactive")
    cmd_args.append(container)

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_start)
