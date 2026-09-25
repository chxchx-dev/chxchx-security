# Engineering rules

1. Never implement custom encryption, onion routing, SOCKS or VPN protocols when maintained system components exist.
2. Never silently fall back from Tor to a direct connection.
3. Never print usernames, hostnames, permanent MAC addresses, serial numbers or machine IDs in normal output.
4. Never persist public-IP checks by default.
5. Never commit `.env`, keys, tokens, logs or machine dumps.
6. All privileged operations must be narrow, visible and initiated by an explicit user command.
7. Do not modify firewall policy in v0.1.0.
8. A network change must have a documented rollback path.
9. Protected mode must clearly state its limits: compatible TCP applications only.
10. Treat normal browsers as fingerprintable; recommend Tor Browser for web anonymity.
11. Tests must not require external network access.
12. Dependencies must be minimal; security-critical behavior should rely on Fedora/Tor/NetworkManager packages rather than Python reimplementations.
13. No code may attempt to delete system journals, audit records or third-party logs.
14. Security claims must be measurable by a check or explicitly marked as a limitation.
