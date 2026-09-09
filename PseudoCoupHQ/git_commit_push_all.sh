#!/usr/bin/env bash
# Commit and push every repo in the PseudoCoup line, from one place.
# Run by the owner on the host machine.
#
# HOW IT WORKS: this script does no git work of its own. It calls
# each repo's OWN git_commit_push.sh, so every repo stays able to
# commit itself standalone and the lock-clearing and message-file
# logic keeps living beside the repo it serves.
#
# Each repo therefore uses ITS OWN staged message from that repo's
# DevComms/next_commit_message.txt. There is deliberately no global
# message option: one message labelling four unrelated commits is
# what the staged-message convention exists to avoid. For a one-off
# message in a single repo, call that repo's script directly —
#     bash ~/Programming/PseudoIR/git_commit_push.sh "quick fix"
# which is exactly why the per-repo scripts were kept.
#
# Usage:
#   bash ~/Programming/PseudoCoupHQ/git_commit_push_all.sh
#   bash ~/Programming/PseudoCoupHQ/git_commit_push_all.sh --only PseudoIR
#   bash ~/Programming/PseudoCoupHQ/git_commit_push_all.sh --list

set +e

# The repos driven from HQ. the owner, 2026-07-31: "for new work:
# PseudoCoup (version 5, version 6) and PseudoIR." PseudoCoupHQ is
# included so the meta-planning commits alongside the work it
# describes — delete that line if HQ should be committed separately.
#
# NOT in this list: ~/Programming/PlanPlan. It is the framework
# research repo rather than part of the PseudoCoup line; commit it
# with its own script. Add it here if that changes.
REPOS=(
    ~/Programming/PseudoCoupHQ
    ~/Programming/PseudoCoup_v5
    ~/Programming/PseudoCoup_v6
    ~/Programming/PseudoIR
)

if [ "$1" = "--list" ]; then
    echo "repos driven from HQ:"
    for r in "${REPOS[@]}"; do echo "  $r"; done
    exit 0
fi

ONLY=""
if [ "$1" = "--only" ]; then
    if [ -z "$2" ]; then
        echo "--only needs a repo name, e.g. --only PseudoIR" >&2
        exit 2
    fi
    ONLY="$2"
fi

FAILED=()
SKIPPED=()
RAN=()

for repo in "${REPOS[@]}"; do
    name="$(basename "$repo")"

    if [ -n "$ONLY" ] && [ "$name" != "$ONLY" ]; then
        continue
    fi

    if [ ! -d "$repo" ]; then
        echo "!!! $name: no such directory ($repo) — skipped"
        SKIPPED+=("$name (missing directory)")
        continue
    fi

    script="$repo/git_commit_push.sh"
    if [ ! -f "$script" ]; then
        echo "!!! $name: no git_commit_push.sh in $repo — skipped"
        SKIPPED+=("$name (no commit script)")
        continue
    fi

    # Called via `bash` deliberately: the Cowork sandbox cannot set
    # the executable bit, so a script it wrote or restored may not
    # be +x. Running it through bash makes that irrelevant.
    bash "$script"
    rc=$?
    RAN+=("$name")
    if [ $rc -ne 0 ]; then
        echo "!!! $name: git_commit_push.sh exited $rc"
        FAILED+=("$name (exit $rc)")
    fi
    echo
done

if [ -n "$ONLY" ] && [ ${#RAN[@]} -eq 0 ] && [ ${#SKIPPED[@]} -eq 0 ]; then
    echo "no repo named '$ONLY' in the list. Try --list." >&2
    exit 2
fi

echo "=== summary ==="
echo "  ran:     ${#RAN[@]} ${RAN[*]}"
if [ ${#SKIPPED[@]} -gt 0 ]; then
    echo "  skipped: ${#SKIPPED[@]}"
    for s in "${SKIPPED[@]}"; do echo "             $s"; done
fi
if [ ${#FAILED[@]} -gt 0 ]; then
    echo "  FAILED:  ${#FAILED[@]}"
    for f in "${FAILED[@]}"; do echo "             $f"; done
    echo
    echo "A failure above is per-repo — the others still committed."
    exit 1
fi
echo "  failed:  0"
echo "done."
