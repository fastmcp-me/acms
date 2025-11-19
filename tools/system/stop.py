"""
System stop tool - Stop the container services.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_stop",
    "category": "system",
    "description": "Stop the container services",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["stop", "system", "services", "shutdown"],
}


async def acms_system_stop(prefix: Optional[str] = None) -> str:
    """Stop the container services."""
    cmd_args = ["system", "stop"]
    if prefix:
        cmd_args.extend(["--prefix", prefix])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_stop)
