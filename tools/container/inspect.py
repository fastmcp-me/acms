"""
Container inspect tool - Display detailed container information.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_container_inspect",
    "category": "container",
    "description": "Display detailed container information in JSON",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["inspect", "details", "info", "container", "json", "metadata"],
}


async def acms_container_inspect(container: str) -> str:
    """Display detailed container information in JSON."""
    result = await run_container_command("inspect", container)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_inspect)
