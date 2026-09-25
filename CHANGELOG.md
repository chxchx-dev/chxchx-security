# Changelog

## Unreleased

- Added JSON output for `doctor` and `tor verify`.
- Added validation for numeric environment settings.
- Added coverage for configuration, process execution, diagnostics and CLI output.
- `doctor` now returns a failing exit code when a readiness check fails.
- Removed the committed `.env.example`; all dotenv files are now ignored from the public tree.

## 0.1.0 - 2026-09-25

- Initial Fedora-focused privacy CLI.
- Tor service orchestration and Tor-path verification.
- `torsocks --isolate` protected command execution and ephemeral shell.
- NetworkManager MAC privacy profile support.
- Redaction helpers and no-log-by-default policy.
- Architecture, threat model, phases, rules and roadmap documentation.
