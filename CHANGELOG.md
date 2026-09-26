# Changelog

## Unreleased

- Added the validated protected-session lifecycle contract for the upcoming namespace implementation.
- Added namespace prerequisite detection and a non-executing session plan.
- Added a tested namespace create/destroy adapter with loopback setup and rollback.

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
