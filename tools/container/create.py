"""
Container create tool - Create a new container from an image without starting it.
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
    "name": "acms_container_create",
    "category": "container",
    "description": "Create a new container from an image without starting it",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["create", "container", "new", "image"],
}


async def acms_container_create(
    image: str,
    command: Optional[List[str]] = None,
    name: Optional[str] = None,
    env: Optional[List[str]] = None,
    publish: Optional[List[str]] = None,
    volume: Optional[List[str]] = None,
    mount: Optional[List[str]] = None,
    network: Optional[str] = None,
    label: Optional[List[str]] = None,
    user: Optional[str] = None,
    entrypoint: Optional[str] = None,
) -> str:
    """Create a new container from an image without starting it."""
    try:
        # Validate all array parameters
        validated_command = (
            validate_array_parameter(command, "command") if command is not None else None
        )
        validated_env = validate_array_parameter(env, "env") if env is not None else None
        validated_publish = (
            validate_array_parameter(publish, "publish") if publish is not None else None
        )
        validated_volume = (
            validate_array_parameter(volume, "volume") if volume is not None else None
        )
        validated_mount = (
            validate_array_parameter(mount, "mount") if mount is not None else None
        )
        validated_label = (
            validate_array_parameter(label, "label") if label is not None else None
        )

        cmd_args = ["create"]

        if name:
            cmd_args.extend(["--name", name])
        if validated_env:
            for e in validated_env:
                cmd_args.extend(["--env", e])
        if validated_publish:
            for p in validated_publish:
                cmd_args.extend(["--publish", p])
        if validated_volume:
            for v in validated_volume:
                cmd_args.extend(["--volume", v])
        if validated_mount:
            for m in validated_mount:
                cmd_args.extend(["--mount", m])
        if network:
            cmd_args.extend(["--network", network])
        if validated_label:
            for lbl in validated_label:
                cmd_args.extend(["--label", lbl])
        if user:
            cmd_args.extend(["--user", user])
        if entrypoint:
            cmd_args.extend(["--entrypoint", entrypoint])

        cmd_args.append(image)
        if validated_command:
            cmd_args.extend(validated_command)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in container_create: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_create)
