from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

BANNER_MAIN = r"""
   ██████╗██╗  ██╗██╗  ██╗ ██████╗██╗  ██╗██╗  ██╗
  ██╔════╝██║  ██║╚██╗██╔╝██╔════╝██║  ██║╚██╗██╔╝
  ██║     ███████║ ╚███╔╝ ██║     ███████║ ╚███╔╝
  ██║     ██╔══██║ ██╔██╗ ██║     ██╔══██║ ██╔██╗
  ╚██████╗██║  ██║██╔╝ ██╗╚██████╗██║  ██║██╔╝ ██╗
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝

              C H X C H X   S E C U R I T Y

               PRIVACY • SECURITY • CONTROL

                      by @chxchx-dev

                [ SYSTEM STATUS: SECURED ]
"""

SIGNATURE_SHORT = r"""┌─[ CHXCHX SECURITY ]──────────────────────────┐
│                                             │
│   Privacy • Security • Control              │
│                                             │
│   chxsec $ _                                │
│                                             │
│                     by @chxchx-dev          │
└─────────────────────────────────────────────┘"""


def header(version: str) -> None:
    console.print(BANNER_MAIN, markup=False, highlight=False)
    console.print(f"v{version} · privacy orchestrator", style="dim", markup=False, highlight=False)


def print_signature() -> None:
    console.print(SIGNATURE_SHORT, markup=False, highlight=False)


def checks_table(checks) -> None:
    table = Table(title="Privacy readiness")
    table.add_column("Check")
    table.add_column("State")
    table.add_column("Detail")
    for check in checks:
        table.add_row(check.name, "OK" if check.ok else "WARN", check.detail)
    console.print(table)
