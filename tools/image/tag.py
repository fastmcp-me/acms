"""
Image tag tool - Apply a new tag to an existing image.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_tag",
    "category": "image",
    "description": "Apply a new tag to an existing image",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["tag", "rename", "alias", "image", "label"],
}


async def acms_image_tag(source_image: str, target_image: str) -> str:
    """Apply a new tag to an existing image."""
    result = await run_container_command("image", "tag", source_image, target_image)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_tag)
