# Threat model

## In scope

- Accidental direct TCP connection by an application the user intentionally launches through `chxsec run` or `chxsec shell`.
- Local DNS leakage caused by a direct hostname lookup in the Tor verification path.
- Reusing one Tor stream context for unrelated protected launches; torsocks isolation is enabled.
- Wi-Fi/Ethernet link-layer tracking reduced through supported NetworkManager cloned-MAC settings.
- Accidental publication of `.env`, logs, machine dumps and common secret formats to Git.

## Out of scope for v0.1.0

- Global whole-host transparent Tor routing.
- UDP anonymization.
- Browser fingerprint protection.
- Account/cookie/behavioral de-anonymization.
- Malware, root compromise or hostile kernel.
- Hardware identifiers visible to local firmware or privileged software.
- ISP knowledge that a Tor connection exists.
- Guaranteed anonymity against a global passive observer.
- Erasing OS, router, application, provider or remote-service logs.
- Anti-forensics.

## Core assumption

The workstation is trusted enough to execute Fedora packages and the local Python CLI. If the host is compromised, the anonymity guarantees of a user-space orchestrator are not meaningful.
