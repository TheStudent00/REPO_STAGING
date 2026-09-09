#!/usr/bin/env bash
# One-time setup: create the PRIVATE GitHub repo for PseudoCoup_v6
# and push the initial state. Run by the owner on the host machine
# (requires the `gh` CLI, authenticated: `gh auth status`).
#
# Idempotent-ish: safe to re-run if a step failed; it skips what
# already exists.
#
# Usage:  ./create_github_repo.sh

set -e
REPO=~/Programming/PseudoCoup_v6
cd "$REPO"

# 1. local git repo
if [ ! -d .git ]; then
    git init -b master
    echo "  initialized local repo (branch: master)"
fi

# 2. first commit if none exists
if ! git rev-parse HEAD >/dev/null 2>&1; then
    git add -A
    git commit -m "PCv6 founding: AgentMemory, commit system, planning carried from PCv5"
    echo "  created initial commit"
fi

# 3. private GitHub repo + remote + push
if git remote get-url origin >/dev/null 2>&1; then
    echo "  remote 'origin' already configured: $(git remote get-url origin)"
    git push -u origin master
else
    gh repo create PseudoCoup_v6 --private --source . --remote origin --push
    echo "  created private repo and pushed"
fi

echo "done."
