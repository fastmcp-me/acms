"""
Image inspect tool - Show detailed information for images.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_inspect",
    "category": "image",
    "description": "Show detailed information for one or more images in JSON",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["inspect", "details", "info", "image", "json", "metadata"],
}


async def acms_image_inspect(image: str) -> str:
    """Show detailed information for one or more images in JSON."""
    result = await run_container_command("image", "inspect", image)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_inspect)
