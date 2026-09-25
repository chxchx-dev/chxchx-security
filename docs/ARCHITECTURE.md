# Architecture

```text
+--------------------------+
|   ChxChx Security CLI    |
|  argparse + Rich terminal|
+------------+-------------+
             |
   +---------+----------+------------------+
   |                    |                  |
   v                    v                  v
+--------+          +----------+       +-----------+
| Audit  |          | Tor svc  |       | NM privacy|
| engine |          | adapter  |       | adapter   |
+---+----+          +----+-----+       +-----+-----+
    |                    |                   |
    v                    v                   v
Linux/systemd       tor.service +        NetworkManager
capabilities        torsocks/curl         / nmcli
                         |
                         v
                    Tor network
```

## Modules

- `config.py`: environment configuration; no secret values are printed.
- `services/tor.py`: service status/start, SOCKS reachability, Tor route verification, protected process/shell.
- `services/network.py`: explicit NetworkManager MAC policy changes.
- `services/audit.py`: read-only dependency and readiness checks.
- `utils/redact.py`: prevents accidental display of full IP/MAC values in future logging or reports.
- `ui.py`: terminal presentation only; contains no security logic.

## Why Python only in 0.1.0

A C++ helper is not justified yet. There is no performance-sensitive packet processing, cryptography or kernel-facing component in this release. Adding a privileged native binary would increase memory-safety and privilege-escalation attack surface without improving anonymity.

If a later release adds a minimal privileged network-namespace helper, it should be small, separately audited, capability-scoped and invoked through a narrow protocol. See `native/README.md`.
