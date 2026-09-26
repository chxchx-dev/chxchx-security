# Security notes

## Public Git hygiene

The repository is designed so a clean clone contains no user-specific state. All dotenv files are ignored and no environment template is committed. Runtime logs are disabled by default. Do not add screenshots containing SSIDs, usernames, home paths, IPs or terminal prompts to issues or commits.

Before publishing:

```bash
git status --short
git grep -nE '(BEGIN .*PRIVATE KEY|token=|api[_-]?key=|password=)' -- . ':!docs/SECURITY.md'
```

Review commit author identity separately if you do not want a personal email exposed in public Git history; Git metadata is not controlled by this program.

## Local trace expectations

Protected shell history is not written to a shell history file by this tool, and its temp directory is ephemeral. That is not the same as "leaving no trace". systemd, NetworkManager, Tor, the kernel, applications, DNS infrastructure, routers, providers and remote services may create their own records.

The project intentionally does not delete journals, audit records or system logs.

`mac list` uses generic connection labels by default so SSIDs and local interface names are not
printed accidentally. Use `--reveal-identifiers` only when operating on a local terminal and do not
copy that output into public issues or documentation.

## Update policy

Do not vendor Tor. Keep Fedora and Tor packages patched. Security fixes in Tor or NetworkManager matter more than clever wrapper code.
