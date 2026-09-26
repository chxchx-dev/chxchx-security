from __future__ import annotations

import argparse
import json
import sys

from rich.prompt import Prompt

from chxchx_security import __version__
from chxchx_security.config import ConfigurationError, Settings
from chxchx_security.services.audit import doctor
from chxchx_security.services.network import (
    ALLOWED_MAC_MODES,
    active_connections,
    apply_mac_mode,
    connection_label,
)
from chxchx_security.services.tor import (
    protected_shell,
    run_protected,
    service_state,
    socks_reachable,
    start_service,
    verify,
)
from chxchx_security.ui import checks_table, console, header


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chxsec", description="ChxChx Security privacy CLI")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command")

    doctor_p = sub.add_parser("doctor", help="Check local privacy prerequisites")
    doctor_p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    audit_p = sub.add_parser("audit", help="Alias of doctor")
    audit_p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    tor = sub.add_parser("tor", help="Tor service and route checks")
    tor_sub = tor.add_subparsers(dest="tor_command", required=True)
    tor_sub.add_parser("status")
    tor_sub.add_parser("start")
    verify_p = tor_sub.add_parser("verify")
    verify_p.add_argument("--reveal-ip", action="store_true")
    verify_p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    run_p = sub.add_parser("run", help="Run a compatible command through torsocks")
    run_p.add_argument("argv", nargs=argparse.REMAINDER)

    sub.add_parser("shell", help="Start an ephemeral torsocks shell")

    mac = sub.add_parser("mac", help="NetworkManager MAC privacy")
    mac_sub = mac.add_subparsers(dest="mac_command", required=True)
    mac_list = mac_sub.add_parser("list")
    mac_list.add_argument(
        "--reveal-identifiers",
        action="store_true",
        help="Show local connection names and types",
    )
    mac_apply = mac_sub.add_parser("apply")
    mac_apply.add_argument("connection")
    mac_apply.add_argument("mode", choices=sorted(ALLOWED_MAC_MODES))
    mac_apply.add_argument("--reconnect", action="store_true")

    sub.add_parser("about")
    return parser


def _checks_json(checks) -> str:
    return json.dumps(
        {
            "ok": all(check.ok for check in checks),
            "checks": [
                {"name": check.name, "ok": check.ok, "detail": check.detail}
                for check in checks
            ],
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def _checks_ok(checks) -> bool:
    return all(check.ok for check in checks)


def _verification_json(result) -> str:
    return json.dumps(
        {
            "ok": result.ok,
            "is_tor": result.is_tor,
            "ip": result.ip,
            "detail": result.detail,
            "error": result.error_code,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def _interactive(settings: Settings) -> int:
    header(__version__)
    console.print("[bold]1[/] Doctor / audit")
    console.print("[bold]2[/] Start Tor")
    console.print("[bold]3[/] Verify Tor route")
    console.print("[bold]4[/] Open protected shell")
    console.print("[bold]5[/] List active NetworkManager profiles")
    console.print("[bold]0[/] Exit")
    choice = Prompt.ask("Select", choices=["0", "1", "2", "3", "4", "5"], default="1")
    if choice == "0":
        return 0
    if choice == "1":
        checks = doctor(settings)
        checks_table(checks)
        return 0 if _checks_ok(checks) else 1
    if choice == "2":
        result = start_service()
        console.print("[green]Tor started[/]" if result.ok else f"[red]{result.stderr or result.stdout}[/]")
        return 0 if result.ok else 1
    if choice == "3":
        result = verify(settings)
        if result.ok:
            console.print(f"[green]{result.detail}[/] exit={result.ip or 'hidden'}")
            return 0
        console.print(f"[red]{result.detail}[/]")
        return 1
    if choice == "4":
        console.print("[yellow]This shell protects compatible TCP apps; it is not a whole-host tunnel.[/]")
        return protected_shell(settings)
    if choice == "5":
        for item in active_connections():
            console.print(f"- {connection_label(item)}")
        return 0
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        parser.error(str(exc))

    if args.command is None:
        return _interactive(settings)

    if args.command in {"doctor", "audit"}:
        checks = doctor(settings)
        if getattr(args, "json", False):
            print(_checks_json(checks))
        else:
            header(__version__)
            checks_table(checks)
        return 0 if _checks_ok(checks) else 1

    if args.command == "tor":
        if args.tor_command == "status":
            console.print(f"service={service_state()} socks={'reachable' if socks_reachable(settings) else 'down'}")
            return 0
        if args.tor_command == "start":
            result = start_service()
            console.print("Tor started" if result.ok else result.stderr or result.stdout)
            return 0 if result.ok else 1
        if args.tor_command == "verify":
            result = verify(settings, reveal_ip=args.reveal_ip)
            if args.json:
                print(_verification_json(result))
            else:
                console.print(f"{result.detail}; exit={result.ip or 'not shown'}")
            return 0 if result.ok else 1

    if args.command == "run":
        command = list(args.argv)
        if command and command[0] == "--":
            command = command[1:]
        if not command:
            parser.error("chxsec run requires a command after --")
        try:
            return run_protected(settings, command)
        except RuntimeError as exc:
            console.print(f"[red]{exc}[/]")
            return 1

    if args.command == "shell":
        try:
            return protected_shell(settings)
        except RuntimeError as exc:
            console.print(f"[red]{exc}[/]")
            return 1

    if args.command == "mac":
        if args.mac_command == "list":
            for item in active_connections():
                console.print(
                    f"- {connection_label(item, reveal_identifiers=args.reveal_identifiers)}"
                )
            return 0
        if args.mac_command == "apply":
            result = apply_mac_mode(args.connection, args.mode, reconnect=args.reconnect)
            if result.ok:
                console.print("[green]NetworkManager profile updated.[/]")
                if not args.reconnect:
                    console.print("Reconnect later for the new MAC policy to take effect.")
                return 0
            console.print(f"[red]{result.stderr or result.stdout}[/]")
            return 1

    if args.command == "about":
        console.print(
            "ChxChx Security reduces accidental network exposure for explicitly protected processes. "
            f"It does not provide invisibility, anti-forensics, or whole-host anonymity in {__version__}."
        )
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
