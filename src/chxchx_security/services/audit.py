from __future__ import annotations

import platform
from dataclasses import dataclass

from chxchx_security.config import Settings
from chxchx_security.services.tor import service_state, socks_reachable
from chxchx_security.utils.process import exists, run


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _fedora_release() -> str:
    try:
        data = {}
        with open("/etc/os-release", "r", encoding="utf-8") as handle:
            for line in handle:
                if "=" in line:
                    key, val = line.rstrip().split("=", 1)
                    data[key] = val.strip('"')
        return f"{data.get('NAME', 'Linux')} {data.get('VERSION_ID', '')}".strip()
    except OSError:
        return platform.system()


def doctor(settings: Settings) -> list[Check]:
    checks = [
        Check("OS", exists("dnf"), _fedora_release()),
        Check("Tor binary", exists("tor"), "installed" if exists("tor") else "missing"),
        Check("torsocks", exists("torsocks"), "installed" if exists("torsocks") else "missing"),
        Check("curl", exists("curl"), "installed" if exists("curl") else "missing"),
        Check("NetworkManager CLI", exists("nmcli"), "installed" if exists("nmcli") else "missing"),
        Check("Tor service", service_state() == "active", service_state()),
        Check("Tor SOCKS", socks_reachable(settings), f"{settings.tor_socks_host}:{settings.tor_socks_port}"),
    ]
    if exists("firewall-cmd"):
        state = run(["firewall-cmd", "--state"], timeout=5)
        checks.append(Check("firewalld", state.ok, state.stdout or state.stderr))
    return checks
