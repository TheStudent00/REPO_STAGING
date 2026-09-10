#!/usr/bin/env bash
# The one place bash logic lives for the PseudoCoup line.
#
#   bash PRIVATE/PseudoCoupHQ/hq.sh
#
# That is the whole normal usage. With no arguments it does everything
# that needs doing: regenerates the dashboards, checks every planning
# tree for consistency, and commits and pushes every repo.
#
# If the checks find an error it stops and pushes NOTHING. Re-run with
# --force to push anyway.
#
# The narrower commands exist for when you want one part on its own:
#   hq.sh check       consistency checks only, changes nothing
#   hq.sh dashboard   regenerate the dashboards only
#   hq.sh sources     fetch every upstream language source (host only)
#   hq.sh tree        print the planning trees as text
#   hq.sh explore     write the card explorer for the whole line, then
#                     open PRIVATE/PseudoCoupHQ/plan_explorer.html
#   hq.sh unlock      clear stale .git/index.lock files only
#   hq.sh list        show what is configured and what is missing
#   hq.sh help        this text
#
# `tree` takes a repo NAME, not a path, and defaults to all of them:
#   hq.sh tree                 every root
#   hq.sh tree PseudoCoup_v5   just that one
#
# `sources` is deliberately NOT part of the no-argument run: it pulls
# hundreds of MB from the network and needs cargo, which is not
# something a routine commit should ever start.
#
# This script holds sequencing and nothing else — every step is a call
# into PRIVATE/PlanPlan/framework/ or into a repo's own
# git_commit_push.sh, so each piece still works on its own.
#
# Run it as `bash <path>`: the sandbox cannot set the executable bit.

set -uo pipefail

FRAMEWORK=PRIVATE/PlanPlan/framework

# Planning roots the checks and dashboards run over.
ROOTS=(
    PRIVATE/PseudoCoupHQ/Planning
    PRIVATE/PseudoCoup_v5/Planning
    PRIVATE/PseudoCoup_v6/Planning
    PRIVATE/PseudoIR/Planning
)
# NOT here: PRIVATE/PlanPlan/Planning. It has a planning
# tree of its own as of 2026-08-01, but this script WRITES (it
# regenerates projections and dashboards), and HQ does not write into
# PlanPlan — same reason PlanPlan is absent from
# git_commit_push_all.sh. Check that tree with its own invocation:
#   python3 PRIVATE/PlanPlan/framework/generate_nodes.py \
#       PRIVATE/PlanPlan/Planning --projections --apply
#   python3 PRIVATE/PlanPlan/framework/generate_dashboards.py \
#       PRIVATE/PlanPlan/Planning
#   python3 PRIVATE/PlanPlan/framework/check_plans.py \
#       PRIVATE/PlanPlan/Planning

usage() {
    sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'
}

# The one fetcher of upstream language sources for the line. HQ does
# not fetch anything itself — it calls the script in the repo that owns
# that research, the same way `commit` calls each repo's own
# git_commit_push.sh.
SOURCES_SCRIPT=PRIVATE/PseudoCoup_v5/Research/fetch_all_sources.sh

# The framework's own bash entry point. HQ calls it rather than calling
# python directly, so which interpreter runs the tools is decided in ONE
# place — PlanPlan's — and not repeated here (the owner, 2026-08-05: a bash
# call is preferable to a python call, because the environment is where
# these go wrong).
PLAN_SH=PRIVATE/PlanPlan/plan.sh

# Resolve a repo NAME to its planning root, so the caller types
# `PseudoCoup_v5`, not a path.
root_of() {
    for r in "${ROOTS[@]}"; do
        [ "$(basename "$(dirname "$r")")" = "$1" ] && { echo "$r"; return 0; }
    done
    echo "unknown repo: $1" >&2
    echo "  known:" >&2
    for r in "${ROOTS[@]}"; do echo "    $(basename "$(dirname "$r")")" >&2; done
    return 2
}

do_sources() {
    if [ ! -f "$SOURCES_SCRIPT" ]; then
        echo "missing: $SOURCES_SCRIPT" >&2
        echo "  is PRIVATE/PseudoCoup_v5 checked out?" >&2
        return 2
    fi
    bash "$SOURCES_SCRIPT" "$@"
    return $?
}

require_tool() {
    if [ ! -f "$1" ]; then
        echo "missing tool: $1" >&2
        echo "  the framework lives in PRIVATE/PlanPlan/ — is it checked out?" >&2
        exit 2
    fi
}

do_dashboard() {
    require_tool "$FRAMEWORK/generate_dashboards.py"
    require_tool "$FRAMEWORK/generate_nodes.py"
    # Both of a node's GENERATED files are regenerated here, together:
    # its DASHBOARD.md, and the `## nodes` projection inside its CORE.
    # check_plans reports neither as stale — it checks that a
    # projection agrees with its register, not that it is current with
    # the sub-node definitions behind it. Regenerating both before the
    # check is what makes a clean check mean the tree agrees with
    # itself. Added 2026-08-01.
    echo "=== rebuilding node projections ==="
    python3 "$FRAMEWORK/generate_nodes.py" "${ROOTS[@]}" \
        --projections --apply
    echo "=== regenerating dashboards ==="
    python3 "$FRAMEWORK/generate_dashboards.py" "${ROOTS[@]}"
}

do_check() {
    require_tool "$FRAMEWORK/check_plans.py"
    echo "=== consistency checks ==="
    python3 "$FRAMEWORK/check_plans.py" "${ROOTS[@]}"
    return $?
}

# Repos that can be left holding a stale .git/index.lock. Added
# 2026-08-02: a session running `git status` inside the sandbox leaves
# the lock file behind, because the sandbox can create it and then
# cannot unlink it. The next commit on the host then fails with
# "Unable to create '.git/index.lock': File exists" — and the person
# hitting that error did not cause it.
#
# PlanPlan is in this list even though HQ does not commit it and does
# not write into it. Clearing sandbox debris is not development of that
# repo; leaving it would just break the next commit made there.
LOCK_REPOS=(
    PRIVATE/PseudoCoupHQ
    PRIVATE/PseudoCoup_v5
    PRIVATE/PseudoCoup_v6
    PRIVATE/PseudoIR
    PRIVATE/PlanPlan
    PRIVATE/DevComms
)

do_unlock() {
    # Only locks older than a minute are cleared. A git operation that
    # is genuinely running holds its lock for far less than that, so
    # the age test is what stops this from shooting a live process.
    # Every removal is printed: this must never be silent, because a
    # lock that keeps coming back is a real problem wearing a
    # harmless-looking mask.
    local found=0
    for repo in "${LOCK_REPOS[@]}"; do
        local lock="$repo/.git/index.lock"
        if [ -e "$lock" ]; then
            if [ -n "$(find "$lock" -mmin +1 2>/dev/null)" ]; then
                rm -f "$lock" && echo "  cleared stale lock: $lock"
                found=1
            else
                echo "  lock present but FRESH, left alone: $lock" >&2
                echo "    another git process may be running right now." >&2
                found=1
            fi
        fi
    done
    if [ $found -eq 0 ]; then
        echo "  none"
    fi
}

# No subcommand means do everything. `hq.sh --force` means the same
# thing with the refusal overridden, so --force works whether or not
# the word `commit` was typed.
CMD="${1:-commit}"
FORCE=""
if [ "$CMD" = "--force" ]; then
    CMD="commit"
    FORCE="--force"
fi
if [ "${2:-}" = "--force" ]; then
    FORCE="--force"
fi

case "$CMD" in
    commit)
        echo "=== clearing stale git index locks ==="
        do_unlock
        echo

        # Dashboards first: they are generated from the plans, so
        # regenerating before the check means the check sees the
        # dashboards that are about to be committed, not the last
        # ones. Any change they produce rides along in this commit.
        do_dashboard || { echo "dashboard generation failed — nothing committed" >&2; exit 1; }
        echo

        do_check
        rc=$?
        echo

        if [ $rc -ne 0 ]; then
            if [ "$FORCE" = "--force" ]; then
                echo "!!! checks FAILED (exit $rc) — committing anyway on --force"
                echo
            else
                echo "=== NOTHING WAS COMMITTED ===" >&2
                echo "  the consistency checks above failed (exit $rc)." >&2
                echo "  fix them, or push anyway with:" >&2
                echo "    bash PRIVATE/PseudoCoupHQ/hq.sh --force" >&2
                exit 1
            fi
        fi

        bash PRIVATE/PseudoCoupHQ/git_commit_push_all.sh
        exit $?
        ;;

    check)
        do_check
        exit $?
        ;;

    dashboard)
        do_dashboard
        exit $?
        ;;

    sources)
        # `hq.sh sources --list` passes straight through.
        do_sources "${@:2}"
        exit $?
        ;;

    tree)
        if [ -n "${2:-}" ]; then
            r=$(root_of "$2") || exit 2
            bash "$PLAN_SH" tree "$r" "${@:3}"
        else
            for r in "${ROOTS[@]}"; do
                echo "=== $(basename "$(dirname "$r")")"
                bash "$PLAN_SH" tree "$r"
                echo
            done
        fi
        exit $?
        ;;

    explore)
        # Every tree in the line, one page, one fixed place. No flags to
        # remember and no path to type: the whole point is that it is
        # one word and then you open the file.
        out=PRIVATE/PseudoCoupHQ/plan_explorer.html
        bash "$PLAN_SH" explore "${ROOTS[@]}" --title "PseudoCoup line" -o "$out"
        exit $?
        ;;

    unlock)
        echo "=== clearing stale git index locks ==="
        do_unlock
        exit 0
        ;;

    list)
        echo "planning roots checked and dashboarded:"
        for r in "${ROOTS[@]}"; do
            if [ -d "$r" ]; then echo "  $r"; else echo "  $r   (MISSING)"; fi
        done
        echo
        echo "framework tools:"
        for t in check_plans.py generate_dashboards.py render_plan.py; do
            if [ -f "$FRAMEWORK/$t" ]; then echo "  $FRAMEWORK/$t"; else echo "  $FRAMEWORK/$t   (MISSING)"; fi
        done
        echo
        echo "repos committed (from git_commit_push_all.sh):"
        bash PRIVATE/PseudoCoupHQ/git_commit_push_all.sh --list | tail -n +2
        echo
        echo "upstream sources fetcher:"
        if [ -f "$SOURCES_SCRIPT" ]; then
            echo "  $SOURCES_SCRIPT"
        else
            echo "  $SOURCES_SCRIPT   (MISSING)"
        fi
        exit 0
        ;;

    -h|--help|help)
        usage
        exit 0
        ;;

    *)
        echo "unknown subcommand: $1" >&2
        echo >&2
        usage >&2
        exit 2
        ;;
esac
