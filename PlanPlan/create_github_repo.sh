#!/usr/bin/env bash
# One-time setup: create the PRIVATE GitHub repo for PlanPlan
# and push the initial state. Run by the owner on the host machine
# (requires the `gh` CLI, authenticated: `gh auth status`).
#
# Usage:  bash ~/Programming/PlanPlan/create_github_repo.sh

set -e
REPO=~/Programming/PlanPlan
cd "$REPO"

if [ ! -d .git ]; then
    git init -b master
    echo "  initialized local repo (branch: master)"
fi

if ! git rev-parse HEAD >/dev/null 2>&1; then
    git add -A
    git commit -m "PlanPlan founding: ontology-evolution research thesis + planning framework draft"
    echo "  created initial commit"
fi

if git remote get-url origin >/dev/null 2>&1; then
    echo "  remote 'origin' already configured: $(git remote get-url origin)"
    git push -u origin master
else
    gh repo create PlanPlan --private --source . --remote origin --push
    echo "  created private repo and pushed"
fi

echo "done."
