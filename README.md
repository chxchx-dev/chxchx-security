# ChxChx Security v0.1.0

Terminal-first privacy orchestrator for Fedora. It does **not** claim to make a machine invisible or erase forensic evidence. Its purpose is narrower and testable: launch compatible applications through Tor, validate the Tor path, reduce accidental local metadata, and manage NetworkManager MAC privacy settings without putting secrets or machine-specific data in Git.

## What v0.1.0 does

- Rich terminal UI inspired by mobile terminal workflows.
- `doctor` checks required Fedora/Linux components without printing username, hostname, serials or permanent MAC addresses.
- `doctor --json` emits machine-readable readiness results without a terminal banner.
- `tor start/status/verify` orchestrates the system Tor daemon and verifies the route with Tor Project's check API through SOCKS hostname resolution.
- `tor verify --json` emits the verification result while masking the exit IP by default.
- `run -- <command>` executes a compatible program through `torsocks --isolate`.
- `shell` starts an ephemeral protected shell with `torsocks`, restrictive umask, no shell-history file, and a temporary runtime directory. It **does not erase system logs**.
- `mac list/apply` manages NetworkManager's supported cloned-MAC modes (`random`, `stable`, `stable-ssid`, `preserve`, `permanent`).
- Optional local `.env` configuration; dotenv files and local runtime files are ignored by Git.
- No custom cryptography and no custom proxy implementation.

## Threat boundary

This project can reduce exposure of the public source IP for **compatible TCP applications launched through ChxChx Security**. It does not automatically anonymize every process on the workstation. UDP, statically linked applications, sandboxed apps, browsers with fingerprinting, plugins, account logins, cookies, WebRTC, application telemetry and behavior can still identify a user.

For web anonymity, use Tor Browser rather than assuming a normal browser becomes anonymous because it is proxied.

## Fedora install

```bash
./install-fedora.sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
chxsec doctor
chxsec tor start
chxsec tor verify
chxsec
```

`install-fedora.sh` installs Fedora packages only after showing what it will install. Tor itself is provided by Fedora/Tor packages; this project does not vendor Tor.

Configuration is optional. The built-in defaults work without a config file; local overrides may be
placed in `.env` or exported as `CHXSEC_*` environment variables. Never commit dotenv files.

## Examples

```bash
chxsec doctor
chxsec doctor --json
chxsec tor status
chxsec tor verify
chxsec tor verify --json
chxsec run -- curl https://example.com
chxsec shell
chxsec mac list
chxsec mac apply "My WiFi" random
```

Applying a MAC policy modifies the selected NetworkManager connection profile. Add `--reconnect` only when you are prepared for the connection to drop and reconnect.

## Security defaults

- No runtime logs by default.
- No username/hostname collection.
- No persistent storage of detected public IPs.
- Tor verification masks IP output unless `--reveal-ip` is explicitly supplied.
- Direct-IP checks are disabled by default.
- Commands that modify system networking are explicit and use existing system tools.

JSON commands return exit code `0` only when all requested checks succeed; failed readiness or
verification returns exit code `1`.

## Project docs

Read `docs/ORCHESTRATION.md`, `docs/ARCHITECTURE.md`, `docs/THREAT_MODEL.md`, `docs/RULES.md`, `docs/PHASES.md`, `docs/SECURITY.md` and `docs/ROADMAP.md` before extending the project.
