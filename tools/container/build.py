"""
Container build tool - Build an OCI image from a local build context.
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
    "name": "acms_container_build",
    "category": "container",
    "description": "Build an OCI image from a local build context",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["build", "image", "dockerfile", "oci", "create"],
}


async def acms_container_build(
    path: str = ".",
    tag: Optional[List[str]] = None,
    file: Optional[str] = None,
    build_arg: Optional[List[str]] = None,
    label: Optional[List[str]] = None,
    no_cache: bool = False,
    target: Optional[str] = None,
    arch: Optional[str] = None,
    os: Optional[str] = None,
    platform: Optional[str] = None,
    cpus: float = 2.0,
    memory: str = "2048MB",
    output: Optional[str] = None,
    progress: str = "auto",
    vsock_port: int = 8088,
    quiet: bool = False,
) -> str:
    """Build an OCI image from a local build context."""
    try:
        # Validate array parameters
        validated_tag = (
            validate_array_parameter(tag, "tag") if tag is not None else None
        )
        validated_build_arg = (
            validate_array_parameter(build_arg, "build_arg") if build_arg is not None else None
        )
        validated_label = (
            validate_array_parameter(label, "label") if label is not None else None
        )

        cmd_args = ["build"]
        if validated_tag:
            for t in validated_tag:
                cmd_args.extend(["--tag", t])
        if file:
            cmd_args.extend(["--file", file])
        if validated_build_arg:
            for arg in validated_build_arg:
                cmd_args.extend(["--build-arg", arg])
        if validated_label:
            for lbl in validated_label:
                cmd_args.extend(["--label", lbl])
        if no_cache:
            cmd_args.append("--no-cache")
        if target:
            cmd_args.extend(["--target", target])
        if arch:
            cmd_args.extend(["--arch", arch])
        if os:
            cmd_args.extend(["--os", os])
        if platform:
            cmd_args.extend(["--platform", platform])
        if cpus != 2.0:
            cmd_args.extend(["--cpus", str(cpus)])
        if memory != "2048MB":
            cmd_args.extend(["--memory", memory])
        if output:
            cmd_args.extend(["--output", output])
        if progress != "auto":
            cmd_args.extend(["--progress", progress])
        if vsock_port != 8088:
            cmd_args.extend(["--vsock-port", str(vsock_port)])
        if quiet:
            cmd_args.append("--quiet")
        cmd_args.append(path)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except Exception as e:
        logger.error(f"Failed to build container: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_build)
