"""
Builder delete tool - Remove the BuildKit builder container.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_builder_delete",
    "category": "builder",
    "description": "Remove the BuildKit builder container",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["delete", "remove", "rm", "builder", "buildkit"],
}


async def acms_builder_delete(force: bool = False) -> str:
    """Remove the BuildKit builder container."""
    cmd_args = ["builder", "rm"]
    if force:
        cmd_args.append("--force")

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_builder_delete)
