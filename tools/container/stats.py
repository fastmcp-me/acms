"""
Container stats tool - Display real-time resource consumption metrics.
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
    "name": "acms_container_stats",
    "category": "container",
    "description": "Display real-time resource consumption metrics for containers",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["stats", "metrics", "resource", "usage", "cpu", "memory", "monitoring"],
}


async def acms_container_stats(
    containers: Optional[List[str]] = None,
    format: str = "table",
    no_stream: bool = False,
) -> str:
    """
    Display real-time resource consumption metrics.

    Args:
        containers: Optional list of container IDs (all running if omitted)
        format: Output format (json|table; default: table)
        no_stream: Single snapshot instead of continuous update

    Returns:
        Resource usage statistics (CPU, memory, I/O, processes)
    """
    try:
        # Validate containers parameter
        validated_containers = (
            validate_array_parameter(containers, "containers")
            if containers is not None
            else None
        )

        cmd_args = ["stats"]

        if format != "table":
            cmd_args.extend(["--format", format])
        if no_stream:
            cmd_args.append("--no-stream")

        # Add container IDs if specified
        if validated_containers:
            cmd_args.extend(validated_containers)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)

    except Exception as e:
        logger.error(f"Failed to get container stats: {e}", exc_info=True)
        raise


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_stats)
