"""
Volume create tool - Create a new volume.
"""
from typing import Optional, List
import logging

from tools._common.utils import (
    run_container_command,
    format_command_result,
    validate_array_parameter,
)

logger = logging.getLogger("ACMS")

TOOL_METADATA = {
    "name": "acms_volume_create",
    "category": "volume",
    "description": "Create a new volume",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["create", "volume", "new", "storage"],
}


async def acms_volume_create(
    name: str,
    size: Optional[str] = None,
    opt: Optional[List[str]] = None,
    label: Optional[List[str]] = None,
) -> str:
    """Create a new volume."""
    try:
        # Validate array parameters
        validated_opt = validate_array_parameter(opt, "opt") if opt is not None else None
        validated_label = (
            validate_array_parameter(label, "label") if label is not None else None
        )

        cmd_args = ["volume", "create"]
        if size:
            cmd_args.extend(["-s", size])
        if validated_opt:
            for option in validated_opt:
                cmd_args.extend(["--opt", option])
        if validated_label:
            for lbl in validated_label:
                cmd_args.extend(["--label", lbl])
        cmd_args.append(name)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except Exception as e:
        logger.error(f"Failed to create volume: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_volume_create)
