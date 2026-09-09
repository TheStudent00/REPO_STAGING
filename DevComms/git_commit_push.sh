#!/usr/bin/env bash
# add-commit-push for ~/Programming/DevComms. Run by the owner on the host
# machine; the Cowork sandbox cannot push (and can leave stale .git
# locks the sandbox itself is denied deleting — cleared here).
#
# This repo is deliberately NOT driven by
# ~/Programming/PseudoCoupHQ/git_commit_push_all.sh. `~/Programming/DevComms`
# is its own thing and not under PseudoCoupHQ's authority (the owner,
# 2026-07-31), so it is committed on its own. Say the word if you want
# HQ to call it for convenience — that would be a convenience, not a
# change of authority.
#
# Message priority: explicit arg > DevComms/next_commit_message.txt
# > "update". The file is emptied after use so a stale message never
# labels a later commit.
#
# Usage:  bash ~/Programming/DevComms/git_commit_push.sh ["commit message"]

set +e
REPO=~/Programming/DevComms
MSGFILE="$REPO/next_commit_message.txt"
if [ -n "$1" ]; then
    MSG="$1"
elif [ -s "$MSGFILE" ]; then
    MSG="$(cat "$MSGFILE")"
    : > "$MSGFILE"
else
    MSG="update"
fi

echo "=== $REPO ==="
cd "$REPO" || { echo "  cannot cd into $REPO"; exit 1; }

if ! pgrep -x git >/dev/null 2>&1; then
    for lock in .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock; do
        if [ -f "$lock" ]; then
            echo "  clearing stale $lock (no git process running)"
            rm -f "$lock"
        fi
    done
    find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null
fi

git add -A
if git diff --cached --quiet; then
    echo "  nothing to commit"
else
    git commit -m "$MSG"
fi
git push
