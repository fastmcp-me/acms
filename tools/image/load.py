"""
Image load tool - Load images from a tar archive.
"""
from typing import Optional

from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_load",
    "category": "image",
    "description": "Load images from a tar archive",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["load", "import", "archive", "tar", "image", "restore"],
}


async def acms_image_load(input: Optional[str] = None) -> str:
    """Load images from a tar archive."""
    cmd_args = ["image", "load"]
    if input:
        cmd_args.extend(["--input", input])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_load)
