from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CmdResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str


def exists(command: str) -> bool:
    return shutil.which(command) is not None


def run(
    argv: Sequence[str],
    *,
    timeout: int = 20,
    env: dict[str, str] | None = None,
    check: bool = False,
) -> CmdResult:
    try:
        completed = subprocess.run(
            list(argv),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return CmdResult(False, 124, "", str(exc))
    result = CmdResult(
        completed.returncode == 0,
        completed.returncode,
        completed.stdout.strip(),
        completed.stderr.strip(),
    )
    if check and not result.ok:
        raise RuntimeError(result.stderr or result.stdout or "command failed")
    return result
