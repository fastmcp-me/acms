"""
Image prune tool - Remove unused (dangling) images.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_prune",
    "category": "image",
    "description": "Remove unused (dangling) images",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["prune", "cleanup", "dangling", "unused", "images"],
}


async def acms_image_prune() -> str:
    """Remove unused (dangling) images."""
    result = await run_container_command("image", "prune")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_prune)
