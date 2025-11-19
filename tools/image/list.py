"""
Image list tool - List all images.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_image_list",
    "category": "image",
    "description": "List all images with formatting options",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["list", "images", "ls", "available"],
}


async def acms_image_list(
    quiet: bool = False, verbose: bool = False, format: str = "table"
) -> str:
    """List all images with formatting options."""
    cmd_args = ["image", "ls"]
    if quiet:
        cmd_args.append("--quiet")
    if verbose:
        cmd_args.append("--verbose")
    if format != "table":
        cmd_args.extend(["--format", format])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_list)
