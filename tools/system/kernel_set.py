"""
System kernel set tool - Install or update the Linux kernel.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_kernel_set",
    "category": "system",
    "description": "Install or update the Linux kernel",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["kernel", "install", "update", "linux"],
}


async def acms_system_kernel_set(
    binary: Optional[str] = None,
    tar: Optional[str] = None,
    arch: Optional[str] = None,
    recommended: bool = False,
) -> str:
    """Install or update the Linux kernel."""
    cmd_args = ["system", "kernel", "set"]
    if binary:
        cmd_args.extend(["--binary", binary])
    if tar:
        cmd_args.extend(["--tar", tar])
    if arch:
        cmd_args.extend(["--arch", arch])
    if recommended:
        cmd_args.append("--recommended")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_kernel_set)
