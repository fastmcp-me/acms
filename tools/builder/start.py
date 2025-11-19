"""
Builder start tool - Start the BuildKit builder container.
"""
from tools._common.utils import run_container_command, format_command_result

TOOL_METADATA = {
    "name": "acms_builder_start",
    "category": "builder",
    "description": "Start the BuildKit builder container",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "keywords": ["start", "builder", "buildkit", "begin"],
}


async def acms_builder_start(cpus: float = 2.0, memory: str = "2048MB") -> str:
    """Start the BuildKit builder container."""
    cmd_args = ["builder", "start"]
    if cpus != 2.0:
        cmd_args.extend(["--cpus", str(cpus)])
    if memory != "2048MB":
        cmd_args.extend(["--memory", memory])

    result = await run_container_command(*cmd_args)
    return format_command_result(result)


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_builder_start)
