#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]] || ! command -v dnf >/dev/null 2>&1; then
  echo "This installer targets Fedora-like systems with dnf." >&2
  exit 1
fi

packages=(python3 python3-pip tor torsocks curl NetworkManager)
printf 'ChxChx Security will install/verify these packages:\n'
printf '  - %s\n' "${packages[@]}"
echo
sudo dnf install -y "${packages[@]}"

echo
echo "Packages ready. The Tor service is NOT enabled at boot by this installer."
echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -e ."
echo "Then: chxsec tor start && chxsec tor verify"
