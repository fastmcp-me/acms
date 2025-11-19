"""
Container stop_all tool - Stop all running containers gracefully.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_stop_all",
    "category": "container",
    "description": "Stop all running containers gracefully by sending a signal",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["stop", "all", "containers", "terminate", "shutdown"],
}


async def acms_container_stop_all(
    signal: str = "SIGTERM", time: Optional[float] = None
) -> str:
    """Stop all running containers gracefully by sending a signal."""
    cmd_args = ["stop", "--all"]
    if signal != "SIGTERM":
        cmd_args.extend(["--signal", signal])
    if time is not None:
        cmd_args.extend(["--time", str(time)])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_stop_all)
