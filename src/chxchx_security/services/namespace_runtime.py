from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, Sequence

from chxchx_security.services.namespace import detect_namespace_tools
from chxchx_security.services.session import (
    SessionLifecycle,
    SessionState,
    namespace_name,
)
from chxchx_security.utils.process import CmdResult, run


CommandRunner = Callable[[Sequence[str]], CmdResult]


@dataclass(frozen=True)
class NamespaceResult:
    ok: bool
    action: str
    session_id: str
    namespace: str
    state: SessionState
    network_ready: bool
    detail: str
    commands: tuple[tuple[str, ...], ...] = ()


class NamespaceRuntime:
    """Lifecycle-only namespace adapter; it does not configure network access."""

    def __init__(
        self,
        *,
        runner: CommandRunner | None = None,
        privileged_prefix: tuple[str, ...] | None = None,
    ) -> None:
        self._runner = runner or (lambda argv: run(argv, timeout=30))
        self._privileged_prefix = (
            ()
            if privileged_prefix is None and os.geteuid() == 0
            else privileged_prefix or ("sudo",)
        )

    def _create_commands(self, namespace: str) -> tuple[tuple[str, ...], ...]:
        prefix = self._privileged_prefix
        return (
            (*prefix, "ip", "netns", "add", namespace),
            (*prefix, "ip", "netns", "exec", namespace, "ip", "link", "set", "lo", "up"),
        )

    def _destroy_command(self, namespace: str) -> tuple[str, ...]:
        return (*self._privileged_prefix, "ip", "netns", "delete", namespace)

    def create(self, session_id: str, *, dry_run: bool = False) -> NamespaceResult:
        lifecycle = SessionLifecycle(session_id)
        namespace = lifecycle.namespace
        commands = self._create_commands(namespace)
        if dry_run:
            return NamespaceResult(
                True,
                "create",
                session_id,
                namespace,
                SessionState.STARTING,
                False,
                "dry-run; no namespace was created",
                commands,
            )

        tools = detect_namespace_tools()
        if not tools.ip:
            return NamespaceResult(
                False,
                "create",
                session_id,
                namespace,
                SessionState.FAILED,
                False,
                "ip command is not installed",
                commands,
            )
        if self._privileged_prefix == ("sudo",) and not tools.sudo:
            return NamespaceResult(
                False,
                "create",
                session_id,
                namespace,
                SessionState.FAILED,
                False,
                "sudo is not installed",
                commands,
            )

        created = self._runner(commands[0])
        if not created.ok:
            return NamespaceResult(
                False,
                "create",
                session_id,
                namespace,
                SessionState.FAILED,
                False,
                "namespace creation failed",
                commands,
            )

        loopback = self._runner(commands[1])
        if not loopback.ok:
            rollback = self._runner(self._destroy_command(namespace))
            rollback_detail = "rollback completed" if rollback.ok else "rollback failed"
            return NamespaceResult(
                False,
                "create",
                session_id,
                namespace,
                SessionState.FAILED,
                False,
                f"loopback setup failed; {rollback_detail}",
                commands + (self._destroy_command(namespace),),
            )

        return NamespaceResult(
            True,
            "create",
            session_id,
            namespace,
            SessionState.ACTIVE,
            False,
            "namespace created; network wiring is not configured",
            commands,
        )

    def destroy(self, session_id: str, *, dry_run: bool = False) -> NamespaceResult:
        namespace = namespace_name(session_id)
        command = self._destroy_command(namespace)
        if dry_run:
            return NamespaceResult(
                True,
                "destroy",
                session_id,
                namespace,
                SessionState.DESTROYED,
                False,
                "dry-run; no namespace was destroyed",
                (command,),
            )

        result = self._runner(command)
        return NamespaceResult(
            result.ok,
            "destroy",
            session_id,
            namespace,
            SessionState.DESTROYED if result.ok else SessionState.FAILED,
            False,
            "namespace destroyed" if result.ok else "namespace destruction failed",
            (command,),
        )
