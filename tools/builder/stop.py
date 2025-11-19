"""
Builder stop tool - Stop the BuildKit builder.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_builder_stop",
    "category": "builder",
    "description": "Stop the BuildKit builder",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["stop", "builder", "buildkit", "terminate"],
}


async def acms_builder_stop() -> str:
    """Stop the BuildKit builder."""
    result = await run_container_command("builder", "stop")
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_builder_stop)
