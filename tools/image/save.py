"""
Image save tool - Save an image to a tar archive.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_save",
    "category": "image",
    "description": "Save an image to a tar archive",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["save", "export", "archive", "tar", "image", "backup"],
}


async def acms_image_save(
    reference: str, output: Optional[str] = None, platform: Optional[str] = None
) -> str:
    """Save an image to a tar archive."""
    cmd_args = ["image", "save"]
    if platform:
        cmd_args.extend(["--platform", platform])
    if output:
        cmd_args.extend(["--output", output])
    cmd_args.append(reference)

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_save)
