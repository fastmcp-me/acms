"""
Container logs tool - Fetch logs from a container.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_logs",
    "category": "container",
    "description": "Fetch logs from a container",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["logs", "output", "container", "debug", "stdout", "stderr"],
}


async def acms_container_logs(
    container: str,
    follow: bool = False,
    boot: bool = False,
    n: Optional[int] = None,
) -> str:
    """Fetch logs from a container."""
    cmd_args = ["logs"]
    if follow:
        cmd_args.append("--follow")
    if boot:
        cmd_args.append("--boot")
    if n is not None:
        cmd_args.extend(["-n", str(n)])
    cmd_args.append(container)

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_logs)
