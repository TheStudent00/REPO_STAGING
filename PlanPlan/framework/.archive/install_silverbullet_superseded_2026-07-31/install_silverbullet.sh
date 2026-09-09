#!/usr/bin/env bash
# Install SilverBullet (open-source, MIT — silverbullet.md) and
# serve a vault. UNVERIFIED by execution (written while the
# session sandbox was down); if the install URL has moved, check
# https://silverbullet.md for the current one-liner.
#
# Usage:
#   bash ~/Programming/PlanningPlan/framework/install_silverbullet.sh
#   # then serve a vault, e.g.:
#   silverbullet ~/Programming/PseudoCoup_v6/Planning
#   # opens a local web UI (default http://localhost:3000)

set -e

# 1. Deno runtime (SilverBullet runs on Deno)
if ! command -v deno >/dev/null 2>&1; then
    echo "installing deno..."
    curl -fsSL https://deno.land/install.sh | sh
    export PATH="$HOME/.deno/bin:$PATH"
    echo 'export PATH="$HOME/.deno/bin:$PATH"' >> ~/.bashrc
fi

# 2. SilverBullet
# `--global` is REQUIRED on Deno 2.x. Without it Deno 2 refuses with
# "the following required arguments were not provided: --global",
# and it fails while PARSING ARGUMENTS, so the URL is never fetched.
# Deno 1.x did not need the flag; this machine runs 2.9.4.
deno install --global -f --name silverbullet -A \
    --unstable-kv --unstable-worker-options \
    https://get.silverbullet.md

echo
echo "done. serve a folder with:"
echo "  silverbullet <path-to-folder>"
echo "e.g.:"
echo "  silverbullet ~/Programming/PseudoCoup_v6/Planning"
