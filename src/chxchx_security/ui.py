from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

BANNER = r"""
   ________      ________      ________            
  / ____/ /_  __/ ____/ /_  __/ ____/ /_  _  __   
 / /   / __ \/ / /   / __ \/ / /   / __ \| |/_/   
/ /___/ / / / / /___/ / / / / /___/ / / />  <     
\____/_/ /_/_/\____/_/ /_/_/\____/_/ /_/_/|_|     
                S E C U R I T Y
"""


def header(version: str) -> None:
    console.print(Panel.fit(BANNER, title=f"v{version}", subtitle="privacy orchestrator"))


def checks_table(checks) -> None:
    table = Table(title="Privacy readiness")
    table.add_column("Check")
    table.add_column("State")
    table.add_column("Detail")
    for check in checks:
        table.add_row(check.name, "OK" if check.ok else "WARN", check.detail)
    console.print(table)
