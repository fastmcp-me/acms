"""
Image push tool - Push an image to a registry.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_push",
    "category": "image",
    "description": "Push an image to a registry",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "keywords": ["push", "upload", "image", "registry", "publish"],
}


async def acms_image_push(
    reference: str,
    platform: Optional[str] = None,
    scheme: str = "auto",
    disable_progress_updates: bool = False,
) -> str:
    """Push an image to a registry."""
    cmd_args = ["image", "push"]
    if platform:
        cmd_args.extend(["--platform", platform])
    if scheme != "auto":
        cmd_args.extend(["--scheme", scheme])
    if disable_progress_updates:
        cmd_args.append("--disable-progress-updates")
    cmd_args.append(reference)

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_push)
