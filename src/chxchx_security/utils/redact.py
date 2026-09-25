from __future__ import annotations

import ipaddress
import re

MAC_RE = re.compile(r"(?i)\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b")


def mask_ip(value: str) -> str:
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return "[redacted-ip]"
    if ip.version == 4:
        parts = value.split(".")
        return f"{parts[0]}.{parts[1]}.x.x"
    exploded = ip.exploded.split(":")
    return ":".join(exploded[:2] + ["x"] * 6)


def redact_text(value: str) -> str:
    value = MAC_RE.sub("[redacted-mac]", value)
    tokens = value.split()
    out: list[str] = []
    for token in tokens:
        stripped = token.strip("[](){}<>,;'")
        try:
            ipaddress.ip_address(stripped)
            out.append(token.replace(stripped, mask_ip(stripped)))
        except ValueError:
            out.append(token)
    return " ".join(out)
