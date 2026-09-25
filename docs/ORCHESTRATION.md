# Orchestration — v0.1.0

## Goal

Coordinate existing Linux privacy primitives without implementing a new anonymity network. ChxChx Security is the control plane; Tor, torsocks, NetworkManager and systemd remain the data-plane/security components.

## Startup flow

1. Load configuration from environment / `.env`.
2. Run `doctor` and verify required commands.
3. Check `tor.service` and local SOCKS port.
4. Refuse protected execution if SOCKS is unavailable. There is no direct-network fallback.
5. For `run`, execute the target under `torsocks --isolate`.
6. For `shell`, create an ephemeral runtime directory, set restrictive permissions, disable shell-history persistence for that child shell, and start `torsocks --shell` with stream isolation.
7. For Tor verification, call the Tor Project check endpoint through `curl --socks5-hostname`, so the hostname is resolved via the SOCKS proxy path.
8. For MAC privacy, modify only an explicitly named NetworkManager connection profile.

## Fail-closed rules

- No Tor SOCKS listener -> protected command does not run.
- Missing torsocks -> protected command does not run.
- Tor verification failure -> report failure; never retry directly.
- Network changes require an explicit command; reconnection requires `--reconnect`.
- Direct public-IP testing is disabled by default.

## v0.1.0 execution modes

### Audit mode
Read-only checks. Does not alter networking.

### Protected process mode
One explicit process is wrapped through torsocks with stream isolation.

### Protected shell mode
Child shell inherits torsocks interception. It is intentionally ephemeral, but the OS and applications may still produce logs or state.

### Network privacy mode
NetworkManager connection profile receives a supported cloned-MAC policy.
