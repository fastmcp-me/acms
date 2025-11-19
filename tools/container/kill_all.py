"""
Container kill_all tool - Immediately kill all running containers.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_kill_all",
    "category": "container",
    "description": "Immediately kill all running containers by sending a signal",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["kill", "all", "containers", "force", "terminate"],
}


async def acms_container_kill_all(signal: str = "KILL") -> str:
    """Immediately kill all running containers by sending a signal."""
    cmd_args = ["kill", "--all"]
    if signal != "KILL":
        cmd_args.extend(["--signal", signal])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_kill_all)
