#!/usr/bin/env bash
# add-commit-push for PseudoCoupHQ itself. Run by the owner on the host
# machine; the Cowork sandbox cannot push (and can leave stale .git
# locks the sandbox itself is denied deleting — cleared here).
#
# This commits HQ ALONE. To commit the whole line in one go, use
# <WORKSPACE_DIR>/PseudoCoupHQ/git_commit_push_all.sh, which calls this
# script and each project repo's own copy.
#
# Message priority: explicit arg > DevComms/next_commit_message.txt
# (written by the sandbox session) > "update". The file is emptied
# after use so a stale message never labels a later commit.
#
# Usage:  bash <WORKSPACE_DIR>/PseudoCoupHQ/git_commit_push.sh ["commit message"]

set +e
REPO=<WORKSPACE_DIR>/PseudoCoupHQ
MSGFILE="$REPO/DevComms/next_commit_message.txt"
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
    # temp objects left by interrupted sandbox git
    find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null
fi

git add -A
if git diff --cached --quiet; then
    echo "  nothing to commit"
else
    git commit -m "$MSG"
fi
git push
