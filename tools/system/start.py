"""
System start tool - Start the container services.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_system_start",
    "category": "system",
    "description": "Start the container services",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["start", "system", "services", "begin"],
}


async def acms_system_start(
    app_root: Optional[str] = None,
    install_root: Optional[str] = None,
    enable_kernel_install: bool = False,
    disable_kernel_install: bool = False,
) -> str:
    """Start the container services."""
    cmd_args = ["system", "start"]
    if app_root:
        cmd_args.extend(["--app-root", app_root])
    if install_root:
        cmd_args.extend(["--install-root", install_root])
    if enable_kernel_install:
        cmd_args.append("--enable-kernel-install")
    if disable_kernel_install:
        cmd_args.append("--disable-kernel-install")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_system_start)
