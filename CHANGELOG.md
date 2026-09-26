# Changelog

## Unreleased

- Added JSON output for `doctor` and `tor verify`.
- Added validation for numeric environment settings.
- Added coverage for configuration, process execution, diagnostics and CLI output.
- `doctor` now returns a failing exit code when a readiness check fails.
- Removed the committed `.env.example`; all dotenv files are now ignored from the public tree.
- Added system-clock readiness checks, retryable Tor verification and classified verification errors.
- Hid local NetworkManager connection identifiers from `mac list` by default.
- Expanded the Fedora installer to prepare the virtual environment and support explicit Tor service actions.

## 0.1.0 - 2026-09-25

- Initial Fedora-focused privacy CLI.
- Tor service orchestration and Tor-path verification.
- `torsocks --isolate` protected command execution and ephemeral shell.
- NetworkManager MAC privacy profile support.
- Redaction helpers and no-log-by-default policy.
- Architecture, threat model, phases, rules and roadmap documentation.
