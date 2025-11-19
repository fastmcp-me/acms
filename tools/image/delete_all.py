"""
Image delete_all tool - Remove all images.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_delete_all",
    "category": "image",
    "description": "Remove all images",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "all", "images", "cleanup"],
}


async def acms_image_delete_all() -> str:
    """Remove all images."""
    result = await run_container_command("image", "rm", "--all")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_delete_all)
