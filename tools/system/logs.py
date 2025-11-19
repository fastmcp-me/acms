"""
System logs tool - Display logs from the container services.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_logs",
    "category": "system",
    "description": "Display logs from the container services",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["logs", "system", "output", "debug"],
}


async def acms_system_logs(last: str = "5m", follow: bool = False) -> str:
    """Display logs from the container services."""
    cmd_args = ["system", "logs"]
    if last != "5m":
        cmd_args.extend(["--last", last])
    if follow:
        cmd_args.append("--follow")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_logs)
