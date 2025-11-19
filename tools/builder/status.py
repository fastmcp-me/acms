"""
Builder status tool - Show the current status of the BuildKit builder.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_builder_status",
    "category": "builder",
    "description": "Show the current status of the BuildKit builder",
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["status", "builder", "buildkit", "info"],
}


async def acms_builder_status(json: bool = False) -> str:
    """Show the current status of the BuildKit builder."""
    cmd_args = ["builder", "status"]
    if json:
        cmd_args.append("--json")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_builder_status)
