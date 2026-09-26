from __future__ import annotations

import json
from dataclasses import dataclass

from chxchx_security.services.session import namespace_name, validate_session_id
from chxchx_security.utils.process import exists


REQUIRED_TOOLS = ("ip", "nsenter", "nft")


@dataclass(frozen=True)
class NamespaceTools:
    ip: bool
    nsenter: bool
    nft: bool
    sudo: bool

    @property
    def ready(self) -> bool:
        return self.ip and self.nsenter and self.nft

    def as_dict(self) -> dict[str, bool | str]:
        return {
            "ip": self.ip,
            "nsenter": self.nsenter,
            "nft": self.nft,
            "sudo": self.sudo,
            "ready": self.ready,
        }


def detect_namespace_tools() -> NamespaceTools:
    return NamespaceTools(
        ip=exists("ip"),
        nsenter=exists("nsenter"),
        nft=exists("nft"),
        sudo=exists("sudo"),
    )


@dataclass(frozen=True)
class NamespaceStep:
    name: str
    command: tuple[str, ...] | None
    status: str

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "command": list(self.command) if self.command else None,
            "status": self.status,
        }


@dataclass(frozen=True)
class NamespacePlan:
    session_id: str
    namespace: str
    executable: bool
    reason: str
    steps: tuple[NamespaceStep, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "namespace": self.namespace,
            "executable": self.executable,
            "reason": self.reason,
            "steps": [step.as_dict() for step in self.steps],
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, sort_keys=True)


def build_namespace_plan(session_id: str) -> NamespacePlan:
    validate_session_id(session_id)
    namespace = namespace_name(session_id)
    return NamespacePlan(
        session_id=session_id,
        namespace=namespace,
        executable=False,
        reason="network wiring, Tor ports and scoped nftables are not implemented",
        steps=(
            NamespaceStep(
                "create namespace",
                ("sudo", "ip", "netns", "add", namespace),
                "planned",
            ),
            NamespaceStep("attach isolated network", None, "not_implemented"),
            NamespaceStep("route DNS and TCP through Tor", None, "not_implemented"),
            NamespaceStep("install namespace-scoped nftables", None, "not_implemented"),
            NamespaceStep("launch protected process", None, "blocked"),
            NamespaceStep(
                "destroy namespace",
                ("sudo", "ip", "netns", "delete", namespace),
                "rollback",
            ),
        ),
    )
