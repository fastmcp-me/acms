"""
Image delete tool - Remove one or more images.
"""
from typing import List
import logging

from tools._common.utils import (
    run_container_command,
    format_command_result,
    validate_array_parameter,
)

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_image_delete",
    "category": "image",
    "description": "Remove one or more images",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "image", "cleanup"],
}


async def acms_image_delete(images: List[str]) -> str:
    """Remove one or more images."""
    try:
        # Validate images parameter
        validated_images = validate_array_parameter(images, "images")
        if not validated_images:
            raise ValueError(
                "Parameter 'images' is required and cannot be empty. "
                "Provide at least one image name to delete."
            )

        cmd_args = ["image", "rm"]
        cmd_args.extend(validated_images)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in image_delete: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_image_delete)
