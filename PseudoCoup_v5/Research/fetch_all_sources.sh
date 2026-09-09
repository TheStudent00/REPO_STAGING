#!/usr/bin/env bash
# Fetches every upstream language source this repo's research reads,
# in one run.
#
#   bash ~/Programming/PseudoCoup_v5/Research/fetch_all_sources.sh
#
# Everything lands in ONE shared root outside the repo:
#
#   ~/Programming/Sources        (override with PC_SOURCES=<dir>)
#
# outside because these checkouts are hundreds of MB of upstream code
# that is not ours, and because that folder is filtered out of
# Timeshift (the owner, 2026-08-02), so snapshots do not carry it.
#
#   bash ~/Programming/PseudoCoup_v5/Research/fetch_all_sources.sh --list
#       show what would run and what is already present; fetches
#       nothing, needs no network.
#
#   ... --list --sizes    the same, plus `du` per checkout. Separate
#       because these trees run to gigabytes: `du` over llvm-project
#       walks every file in it, which is slow on the host and, in the
#       sandbox, exhausted the system file table outright.
#
# Run on the HOST: both steps need the network, which the sandbox
# does not have.
#
# This script holds SEQUENCING ONLY. Every step is a call into the
# fetcher that owns that source, so each still works on its own —
# the same rule ~/Programming/PseudoCoupHQ/hq.sh follows.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${PC_SOURCES:-$HOME/Programming/Sources}"

# The two fetchers, in dependency order. The order is not cosmetic:
# fetch_llvm.sh adds sparse directories to the rust/ checkout that
# fetch_sources.sh clones, so it must run second.
#
# 2026-08-02: a third step was REMOVED by a standing prohibition — see
# ~/Programming/PseudoCoupHQ/CRANELIFT_IS_BANNED.md. It fetched, built
# and vendored a banned backend. No step here may fetch it again.
STEPS=(
    "$HERE/rust_routing/fetch_sources.sh|rustc sparse checkout"
    "$HERE/llvm_trace/fetch_llvm.sh|llvm-project, + rustc codegen dirs"
)

# `du` only when asked — see the header for why it is not the default.
SIZES=""
for a in "$@"; do [ "$a" = "--sizes" ] && SIZES="yes"; done

report_present() {
    local found=0
    for d in rust llvm-project; do
        if [ -e "$SRC/$d" ]; then
            if [ -n "$SIZES" ]; then
                printf '  %-14s %s\n' "$d" \
                    "$(du -sh "$SRC/$d" 2>/dev/null | cut -f1)"
            else
                printf '  %-14s present\n' "$d"
            fi
            found=1
        else
            [ -z "${1:-}" ] || printf '  %-14s ABSENT\n' "$d"
        fi
    done
    return $found
}

if [ "${1:-}" = "--list" ]; then
    echo "sources root: $SRC"
    [ -d "$SRC" ] && echo "   (exists)" || echo "   (does not exist yet)"
    echo
    echo "steps, in order:"
    for step in "${STEPS[@]}"; do
        script="${step%%|*}"; what="${step##*|}"
        if [ -f "$script" ]; then
            printf '  %s\n      %s\n' "$script" "$what"
        else
            printf '  %s   (MISSING)\n      %s\n' "$script" "$what"
        fi
    done
    echo
    echo "already present under the sources root:"
    if report_present; then echo "  none"; fi
    exit 0
fi

for a in "$@"; do
    case "$a" in
        --sizes) ;;   # handled above
        *) echo "unknown argument: $a" >&2
           echo "usage: bash $HERE/fetch_all_sources.sh [--list] [--sizes]" >&2
           exit 2 ;;
    esac
done

mkdir -p "$SRC"
echo "=== sources root: $SRC"
echo

failed=()
for step in "${STEPS[@]}"; do
    script="${step%%|*}"; what="${step##*|}"
    echo "=================================================="
    echo "== $(basename "$script") — $what"
    echo "=================================================="
    if [ ! -f "$script" ]; then
        echo "   MISSING: $script" >&2
        failed+=("$(basename "$script") (missing)")
        continue
    fi
    # Each fetcher is run from its own folder: they resolve their
    # siblings relative to $0, so a wrong cwd is a silent no-op rather
    # than an error.
    ( cd "$(dirname "$script")" && bash "$script" )
    rc=$?
    # A failed step does NOT stop the run: a network failure on one
    # checkout should not cost you the other. Every failure is
    # collected and reported at the end instead.
    if [ $rc -ne 0 ]; then
        echo "   !!! FAILED (exit $rc): $script" >&2
        failed+=("$(basename "$script") (exit $rc)")
    fi
    echo
done

echo "=================================================="
echo "== summary"
echo "=================================================="
echo "sources root: $SRC"
report_present show_absent

if [ ${#failed[@]} -ne 0 ]; then
    echo
    echo "steps that failed:" >&2
    for f in "${failed[@]}"; do echo "  $f" >&2; done
    exit 1
fi
echo
echo "all steps completed."
