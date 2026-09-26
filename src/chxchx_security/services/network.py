from __future__ import annotations

from dataclasses import dataclass

from chxchx_security.utils.process import CmdResult, exists, run

ALLOWED_MAC_MODES = {"random", "stable", "stable-ssid", "preserve", "permanent"}


@dataclass(frozen=True)
class ConnectionInfo:
    name: str
    kind: str


def connection_label(connection: ConnectionInfo, *, reveal_identifiers: bool = False) -> str:
    """Return a safe display label without exposing local connection names by default."""
    if reveal_identifiers:
        return f"{connection.name} ({connection.kind})"
    labels = {
        "802-11-wireless": "Wi-Fi connection",
        "wifi": "Wi-Fi connection",
        "802-3-ethernet": "Ethernet connection",
        "ethernet": "Ethernet connection",
        "tun": "Tunnel interface",
        "bridge": "Bridge interface",
        "loopback": "Loopback interface",
    }
    return labels.get(connection.kind, "Network connection")


def active_connections() -> list[ConnectionInfo]:
    if not exists("nmcli"):
        return []
    result = run(
        ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active"],
        timeout=8,
    )
    if not result.ok:
        return []
    connections: list[ConnectionInfo] = []
    for line in result.stdout.splitlines():
        if not line.strip() or ":" not in line:
            continue
        name, kind = line.rsplit(":", 1)
        connections.append(ConnectionInfo(name=name, kind=kind))
    return connections


def connection_type(name: str) -> str | None:
    result = run(
        ["nmcli", "-g", "connection.type", "connection", "show", name], timeout=8
    )
    return result.stdout.strip() if result.ok else None


def _mac_property(kind: str) -> str | None:
    if kind in {"802-11-wireless", "wifi"}:
        return "802-11-wireless.cloned-mac-address"
    if kind in {"802-3-ethernet", "ethernet"}:
        return "802-3-ethernet.cloned-mac-address"
    return None


def apply_mac_mode(name: str, mode: str, *, reconnect: bool = False) -> CmdResult:
    if mode not in ALLOWED_MAC_MODES:
        return CmdResult(False, 2, "", f"unsupported MAC mode: {mode}")
    if not exists("nmcli"):
        return CmdResult(False, 127, "", "nmcli not found")

    kind = connection_type(name)
    if not kind:
        return CmdResult(False, 1, "", "connection not found")
    prop = _mac_property(kind)
    if not prop:
        return CmdResult(False, 2, "", f"unsupported connection type: {kind}")

    result = run(["sudo", "nmcli", "connection", "modify", name, prop, mode], timeout=20)
    if not result.ok or not reconnect:
        return result

    down = run(["sudo", "nmcli", "connection", "down", name], timeout=30)
    if not down.ok:
        return down
    return run(["sudo", "nmcli", "connection", "up", name], timeout=45)
