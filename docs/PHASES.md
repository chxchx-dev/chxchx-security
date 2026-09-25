# Project phases

## Phase 0 — v0.1.0 (included)

Objective: trustworthy process-level privacy orchestration.

Deliverables:
- Fedora installer bootstrap.
- Readiness doctor.
- Tor service start/status.
- SOCKS reachability.
- Tor route verification.
- Isolated torsocks command runner.
- Ephemeral protected shell.
- NetworkManager cloned-MAC policy manager.
- Git/secrets hygiene.
- Tests and threat model.

Exit criteria:
- Protected execution refuses to run when Tor is unavailable.
- Verification uses SOCKS hostname resolution and confirms `IsTor`.
- No machine identity is gathered for normal output.

## Phase 1 — v0.2.x

Objective: stronger per-session isolation without changing the whole workstation.

Planned work:
- Dedicated Linux network namespace for protected sessions.
- nftables rules scoped only to that namespace.
- Tor `TransPort`/`DNSPort` integration.
- Automatic rollback on process exit.
- IPv4/IPv6 leak tests from inside the namespace.
- Integration tests in a disposable VM.

## Phase 2 — v0.3.x

Objective: operational hardening.

Planned work:
- Signed release artifacts and SBOM.
- Reproducible packaging.
- SELinux policy review.
- Dependency pinning and vulnerability scanning.
- Config schema validation.

## Phase 3 — v1.0

Objective: stable, auditable Fedora privacy workstation helper.

Requirements before 1.0:
- Independent code review.
- VM-based leak-test suite.
- Namespace fail-closed behavior demonstrated under Tor crash, DNS failure and process launch edge cases.
- Documented rollback and recovery procedures.
