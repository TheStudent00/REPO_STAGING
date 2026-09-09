#!/usr/bin/env bash
# One-time setup: create the PRIVATE GitHub repo for PseudoCoupHQ
# and push the initial state. Run by the owner on the host machine
# (requires the `gh` CLI, authenticated: `gh auth status`).
#
# Idempotent-ish: safe to re-run if a step failed; it skips what
# already exists.
#
# Usage:  bash ~/Programming/PseudoCoupHQ/create_github_repo.sh
#
# Invoke with `bash <path>` rather than `./create_github_repo.sh` so
# the executable bit is never needed — the Cowork sandbox cannot set
# it, which cost a step during the PCv6 founding.

set -e
REPO=~/Programming/PseudoCoupHQ
cd "$REPO"

# 1. local git repo
if [ ! -d .git ]; then
    git init -b master
    echo "  initialized local repo (branch: master)"
fi

# 2. first commit if none exists
if ! git rev-parse HEAD >/dev/null 2>&1; then
    git add -A
    git commit -m "PseudoCoupHQ founding: meta-planning root over the PseudoCoup line; cross-repo commit driver"
    echo "  created initial commit"
fi

# 3. private GitHub repo + remote + push
if git remote get-url origin >/dev/null 2>&1; then
    echo "  remote 'origin' already configured: $(git remote get-url origin)"
    git push -u origin master
else
    gh repo create PseudoCoupHQ --private --source . --remote origin --push
    echo "  created private repo and pushed"
fi

echo "done."
