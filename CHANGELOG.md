# Changelog

## Unreleased

- Added `session firewall-apply` (dry-run unless `--yes`): validates and atomically installs the session's nftables tables; `session destroy` now removes them too.
- Fixed the planned firewall ruleset: invalid `tcp redirect` syntax, host-wide `forward policy drop` (now scoped to the session interface), IPv6 not dropped from the session interface, and unreachable TCP-DNS rules.
- Added `session network-apply` (dry-run unless `--yes`) to create a namespace and wire a veth pair with rollback, and `session destroy` to remove it.
- Compact ASCII banner shown on interactive start and `doctor`; short signature shown by `about`.
- Added the validated protected-session lifecycle contract for the upcoming namespace implementation.
- Added namespace prerequisite detection and a non-executing session plan.
- Added a tested namespace create/destroy adapter with loopback setup and rollback.
- Added a validated veth/Tor-port network plan without privileged execution.
- Added a validated, non-executing private Tor `TransPort`/`DNSPort` configuration plan.
- Added a validated, non-executing fail-closed `nftables` ruleset plan.

## 0.1.2 - 2026-09-26

- Protected commands now require a verified Tor route before launching.
- Added opt-in live integration tests for a real Fedora/Tor environment.

## 0.1.1 - 2026-09-26

- Added JSON output for `doctor` and `tor verify`.
- Added validation for numeric environment settings.
- Added coverage for configuration, process execution, diagnostics and CLI output.
- `doctor` now returns a failing exit code when a readiness check fails.
- Removed the committed `.env.example`; all dotenv files are now ignored from the public tree.
- Added system-clock readiness checks, retryable Tor verification and classified verification errors.
- Hid local NetworkManager connection identifiers from `mac list` by default.
- Expanded the Fedora installer to prepare the virtual environment and support explicit Tor service actions.
- Fixed interactive `doctor` exit codes and added JSON support to the `audit` alias.
- Added a standard `make check` validation target and continuous integration configuration.

## 0.1.0 - 2026-09-25

- Initial Fedora-focused privacy CLI.
- Tor service orchestration and Tor-path verification.
- `torsocks --isolate` protected command execution and ephemeral shell.
- NetworkManager MAC privacy profile support.
- Redaction helpers and no-log-by-default policy.
- Architecture, threat model, phases, rules and roadmap documentation.
