"""
Network delete tool - Delete one or more networks.
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
    "name": "acms_network_delete",
    "category": "network",
    "description": "Delete one or more networks",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "network"],
}


async def acms_network_delete(networks: List[str]) -> str:
    """Delete one or more networks."""
    try:
        # Validate networks parameter
        validated_networks = validate_array_parameter(networks, "networks")
        if not validated_networks:
            raise ValueError(
                "Parameter 'networks' is required and cannot be empty. "
                "Provide at least one network name to delete."
            )

        cmd_args = ["network", "rm"]
        cmd_args.extend(validated_networks)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in network_delete: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_network_delete)
