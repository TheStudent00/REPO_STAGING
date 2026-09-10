#!/usr/bin/env bash
# One-time setup: create the PRIVATE GitHub repo for PRIVATE/DevComms
# and push the initial state. Run by the owner on the host machine
# (requires the `gh` CLI, authenticated: `gh auth status`).
#
# WHAT THIS REPO IS. `PRIVATE/DevComms` is its own thing (the owner,
# 2026-07-31) — NOT under PseudoCoupHQ's authority and not part of the
# PseudoCoup line. It holds the communication protocol, plan_and_code,
# and the vocabulary analysis: documents that govern how work is done
# rather than any one project's work.
#
# WHY IT NEEDS ONE. Every project repo's
# DevComms/LLM_communication_protocol.md is a SYMLINK pointing here.
# So the documents that govern everything are currently the only ones
# under no version control at all, while four repos version control
# pointers at them. This fixes that without changing who owns what.
#
# NOTE ON THE SYMLINKS. They keep working exactly as they do now —
# they resolve through the filesystem, not through git. This repo does
# not change the layout, it only starts tracking the content.
#
# Idempotent-ish: safe to re-run if a step failed; it skips what
# already exists.
#
# Usage:  bash PRIVATE/DevComms/create_github_repo.sh
#
# Invoked as `bash <path>` so the executable bit is never needed — the
# sandbox cannot set it.

set -e
REPO=PRIVATE/DevComms
cd "$REPO"

# 1. local git repo
if [ ! -d .git ]; then
    git init -b master
    echo "  initialized local repo (branch: master)"
fi

# 2. first commit if none exists
if ! git rev-parse HEAD >/dev/null 2>&1; then
    git add -A
    git commit -m "DevComms founding: communication protocol, plan_and_code, vocabulary analysis"
    echo "  created initial commit"
fi

# 3. private GitHub repo + remote + push
if git remote get-url origin >/dev/null 2>&1; then
    echo "  remote 'origin' already configured: $(git remote get-url origin)"
    git push -u origin master
else
    # Named DevComms_root rather than DevComms: every project repo already
    # contains a folder called DevComms, and a bare repo name of DevComms
    # would be ambiguous when read back in a list of repos. Change it here
    # if you would rather it were plain DevComms.
    gh repo create DevComms_root --private --source . --remote origin --push
    echo "  created private repo and pushed"
fi

echo "done."
