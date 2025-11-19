"""
Container run tool - Run a command in a new container.
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
    "name": "acms_container_run",
    "category": "container",
    "description": "Run a command in a new container with full parameter support",
    "annotations": {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
    "keywords": ["run", "container", "execute", "start", "create", "launch"],
}


async def acms_container_run(
    image: str,
    command: Optional[List[str]] = None,
    cwd: Optional[str] = None,
    env: Optional[List[str]] = None,
    env_file: Optional[str] = None,
    uid: Optional[int] = None,
    gid: Optional[int] = None,
    interactive: bool = False,
    tty: bool = False,
    user: Optional[str] = None,
    cpus: Optional[float] = None,
    memory: Optional[str] = None,
    detach: bool = False,
    entrypoint: Optional[str] = None,
    mount: Optional[List[str]] = None,
    publish: Optional[List[str]] = None,
    publish_socket: Optional[List[str]] = None,
    tmpfs: Optional[List[str]] = None,
    name: Optional[str] = None,
    remove: bool = False,
    os: str = "linux",
    arch: str = "arm64",
    volume: Optional[List[str]] = None,
    kernel: Optional[str] = None,
    network: Optional[str] = None,
    cidfile: Optional[str] = None,
    no_dns: bool = False,
    dns: Optional[List[str]] = None,
    dns_domain: Optional[str] = None,
    dns_search: Optional[List[str]] = None,
    dns_option: Optional[List[str]] = None,
    label: Optional[List[str]] = None,
    virtualization: bool = False,
    scheme: str = "auto",
    disable_progress_updates: bool = False,
) -> str:
    """Run a command in a new container with full parameter support."""
    try:
        # Validate all array parameters
        validated_command = (
            validate_array_parameter(command, "command") if command is not None else None
        )
        validated_env = validate_array_parameter(env, "env") if env is not None else None
        validated_mount = (
            validate_array_parameter(mount, "mount") if mount is not None else None
        )
        validated_publish = (
            validate_array_parameter(publish, "publish") if publish is not None else None
        )
        validated_publish_socket = (
            validate_array_parameter(publish_socket, "publish_socket")
            if publish_socket is not None
            else None
        )
        validated_tmpfs = (
            validate_array_parameter(tmpfs, "tmpfs") if tmpfs is not None else None
        )
        validated_volume = (
            validate_array_parameter(volume, "volume") if volume is not None else None
        )
        validated_dns = validate_array_parameter(dns, "dns") if dns is not None else None
        validated_dns_search = (
            validate_array_parameter(dns_search, "dns_search")
            if dns_search is not None
            else None
        )
        validated_dns_option = (
            validate_array_parameter(dns_option, "dns_option")
            if dns_option is not None
            else None
        )
        validated_label = (
            validate_array_parameter(label, "label") if label is not None else None
        )

        cmd_args = ["run"]

        if cwd:
            cmd_args.extend(["--cwd", cwd])
        if validated_env:
            for e in validated_env:
                cmd_args.extend(["--env", e])
        if env_file:
            cmd_args.extend(["--env-file", env_file])
        if uid is not None:
            cmd_args.extend(["--uid", str(uid)])
        if gid is not None:
            cmd_args.extend(["--gid", str(gid)])
        if interactive:
            cmd_args.append("--interactive")
        if tty:
            cmd_args.append("--tty")
        if user:
            cmd_args.extend(["--user", user])
        if cpus is not None:
            cmd_args.extend(["--cpus", str(cpus)])
        if memory:
            cmd_args.extend(["--memory", memory])
        if detach:
            cmd_args.append("--detach")
        if entrypoint:
            cmd_args.extend(["--entrypoint", entrypoint])
        if validated_mount:
            for m in validated_mount:
                cmd_args.extend(["--mount", m])
        if validated_publish:
            for p in validated_publish:
                cmd_args.extend(["--publish", p])
        if validated_publish_socket:
            for ps in validated_publish_socket:
                cmd_args.extend(["--publish-socket", ps])
        if validated_tmpfs:
            for t in validated_tmpfs:
                cmd_args.extend(["--tmpfs", t])
        if name:
            cmd_args.extend(["--name", name])
        if remove:
            cmd_args.append("--remove")
        if os != "linux":
            cmd_args.extend(["--os", os])
        if arch != "arm64":
            cmd_args.extend(["--arch", arch])
        if validated_volume:
            for v in validated_volume:
                cmd_args.extend(["--volume", v])
        if kernel:
            cmd_args.extend(["--kernel", kernel])
        if network:
            cmd_args.extend(["--network", network])
        if cidfile:
            cmd_args.extend(["--cidfile", cidfile])
        if no_dns:
            cmd_args.append("--no-dns")
        if validated_dns:
            for d in validated_dns:
                cmd_args.extend(["--dns", d])
        if dns_domain:
            cmd_args.extend(["--dns-domain", dns_domain])
        if validated_dns_search:
            for ds in validated_dns_search:
                cmd_args.extend(["--dns-search", ds])
        if validated_dns_option:
            for do in validated_dns_option:
                cmd_args.extend(["--dns-option", do])
        if validated_label:
            for lbl in validated_label:
                cmd_args.extend(["--label", lbl])
        if virtualization:
            cmd_args.append("--virtualization")
        if scheme != "auto":
            cmd_args.extend(["--scheme", scheme])
        if disable_progress_updates:
            cmd_args.append("--disable-progress-updates")

        cmd_args.append(image)
        if validated_command:
            cmd_args.extend(validated_command)

        result = await run_container_command(*cmd_args)
        return format_command_result(result)
    except ValueError as e:
        logger.error(f"Parameter validation error in container_run: {e}")
        return f"Parameter validation error: {str(e)}"


def register(mcp) -> None:
    """Register this tool with the MCP server."""
    mcp.tool(
        description=TOOL_METADATA["description"],
        annotations=TOOL_METADATA["annotations"],
    )(acms_container_run)
