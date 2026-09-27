```text
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
```

# ChxChx Security v0.1.2

Terminal-first privacy orchestrator for Fedora. It does **not** claim to make a machine invisible or erase forensic evidence. Its purpose is narrower and testable: launch compatible applications through Tor, validate the Tor path, reduce accidental local metadata, and manage NetworkManager MAC privacy settings without putting secrets or machine-specific data in Git.

## What v0.1.2 does

- Rich terminal UI inspired by mobile terminal workflows.
- `doctor` checks required Fedora/Linux components without printing username, hostname, serials or permanent MAC addresses.
- `doctor --json` emits machine-readable readiness results without a terminal banner.
- `tor start/status/verify` orchestrates the system Tor daemon and verifies the route with Tor Project's check API through SOCKS hostname resolution.
- `tor verify --json` emits the verification result while masking the exit IP by default.
- `run -- <command>` executes a compatible program through `torsocks --isolate`.
- `shell` starts an ephemeral protected shell with `torsocks`, restrictive umask, no shell-history file, and a temporary runtime directory. It **does not erase system logs**.
- `mac list/apply` manages NetworkManager's supported cloned-MAC modes (`random`, `stable`, `stable-ssid`, `preserve`, `permanent`); connection identifiers are hidden by default.
- Optional local `.env` configuration; dotenv files and local runtime files are ignored by Git.
- No custom cryptography and no custom proxy implementation.

## Threat boundary

This project can reduce exposure of the public source IP for **compatible TCP applications launched through ChxChx Security**. It does not automatically anonymize every process on the workstation. UDP, statically linked applications, sandboxed apps, browsers with fingerprinting, plugins, account logins, cookies, WebRTC, application telemetry and behavior can still identify a user.

For web anonymity, use Tor Browser rather than assuming a normal browser becomes anonymous because it is proxied.

## Fedora install

```bash
./install-fedora.sh --yes
source .venv/bin/activate
chxsec doctor
chxsec tor verify
chxsec
```

`install-fedora.sh` installs Fedora packages, creates `.venv` and installs the project. Tor itself is provided by Fedora/Tor packages; this project does not vendor Tor. The installer does not start or enable Tor unless explicitly requested:

```bash
./install-fedora.sh --yes --start-tor
./install-fedora.sh --yes --enable-tor
```

Use `./install-fedora.sh --help` to see all options. Use `--dry-run` to inspect the planned actions without changing the system.

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
chxsec mac list --reveal-identifiers
chxsec mac apply "My WiFi" random
chxsec session tools
chxsec session plan demo
chxsec session network-plan demo --subnet 10.203.0.0/30
chxsec session tor-port-plan 10.203.0.1
chxsec session firewall-plan demo --subnet 10.203.0.0/30
chxsec session network-apply demo --subnet 10.203.0.0/30        # dry-run
chxsec session network-apply demo --subnet 10.203.0.0/30 --yes  # privileged
chxsec session destroy demo
```

Applying a MAC policy modifies the selected NetworkManager connection profile. Add `--reconnect` only when you are prepared for the connection to drop and reconnect.

## Security defaults

- No runtime logs by default.
- No username/hostname collection.
- No persistent storage of detected public IPs.
- Tor verification masks IP output unless `--reveal-ip` is explicitly supplied.
- `mac list` hides SSIDs and local interface names unless `--reveal-identifiers` is explicitly supplied.
- Direct-IP checks are disabled by default.
- Commands that modify system networking are explicit and use existing system tools.

JSON commands return exit code `0` only when all requested checks succeed; failed readiness or
verification returns exit code `1`.

## Security guarantees and limits

- Protected execution refuses to run when the Tor SOCKS listener is unavailable; there is no direct-network fallback.
- Tor verification resolves the check hostname through SOCKS and requires the endpoint to confirm `IsTor`.
- The project reduces exposure for explicitly protected compatible TCP processes; it is not a whole-host anonymity system.
- The project does not erase system logs, audit records or third-party history.
- `session plan` is currently dry-run only; it never creates namespaces or changes firewall rules.
- `session network-plan` is planning-only. `session network-apply --yes` is the first privileged command: it creates the namespace and a veth pair with addresses, installs no route and no firewall rules, and rolls everything back on failure. Without `--yes` it only prints the commands. `session destroy` removes the namespace and veth.
- `session tor-port-plan` only renders private `TransPort`/`DNSPort` directives; it never writes Tor configuration or restarts the service.
- `session firewall-plan` renders a fail-closed `nftables` ruleset; it never applies rules to the host.
- Do not publish terminal screenshots or logs containing SSIDs, usernames, hostnames, home paths, IPs or interface names.

## Development

```bash
./install-fedora.sh --yes --with-dev
source .venv/bin/activate
pytest
```

Live Fedora/Tor integration checks are opt-in because they require a running Tor service and
external network access:

```bash
make integration
```

The namespace lifecycle smoke test is separate because it uses privileged `ip netns` commands:

```bash
make namespace-integration
```
