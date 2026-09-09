#!/usr/bin/env bash
# The one bash entry point for the planning framework.
#
#   bash PlanPlan/plan.sh <command> [args...]
#
# Every command is a call into PlanPlan/framework/. This
# script holds two things and nothing else: which interpreter to use,
# and which tool a word maps to.
#
# WHY IT EXISTS. the owner, 2026-08-05: "i just dont like calling python
# functions in the terminal because ive found very often issues with
# environment and whatever else. bash call is preferable." The
# framework is standard library only, so ANY python3 runs it — but
# "any" is exactly the problem when a machine has several and PATH
# decides. This picks one, says which, and fails loudly if none works.
#
# COMMANDS
#   check    <root>...            consistency checks; exits 1 on errors
#   dash     <root>...            regenerate every DASHBOARD.md
#   nodes    <root>... [--apply]  realize registered-but-missing nodes
#   project  <root>... [--apply]  rebuild the `## sub_nodes` projections
#   adopt    <root>... [--apply]  fill in place fields + CHECK ids
#   tree     <root> [--with ...]  print the tree as text
#   view     <root> [-o FILE]     write the reading view (html)
#   explore  <root> [-o FILE]     write the card explorer (html)
#   serve    <root> [PORT]        card explorer, re-scanned per request
#   migrate  <name> <repo>...     a framework-wide change; dry run first
#   which                         show the interpreter that would be used
#   help                          this text
#
# Anything not listed is passed straight through, so a flag added to a
# tool later needs no change here.

set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
F="$HERE/framework"

# ---- interpreter -----------------------------------------------------------
# Order matters. PLANPLAN_PYTHON wins so a machine can override without
# editing this file. Otherwise take the first that exists AND runs — a
# name on PATH that fails to execute is worse than one that is absent,
# because the error surfaces later and looks like a tool bug.
usable() {
    command -v "$1" >/dev/null 2>&1 && \
    "$1" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,8) else 1)' 2>/dev/null
}

pick_python() {
    # An override that does not work is an ERROR, not a reason to try
    # something else. Falling through would hide a typo and run a
    # different interpreter than the one asked for — the half-working
    # failure this framework keeps finding elsewhere.
    if [ -n "${PLANPLAN_PYTHON:-}" ]; then
        if usable "$PLANPLAN_PYTHON"; then echo "$PLANPLAN_PYTHON"; return 0; fi
        echo "PLANPLAN_PYTHON is set to '$PLANPLAN_PYTHON', which is not a usable python3 (3.8+)." >&2
        return 2
    fi
    for c in python3 python3.13 python3.12 /usr/bin/python3 \
             "$HOME/anaconda3/bin/python3"; do
        if usable "$c"; then echo "$c"; return 0; fi
    done
    return 1
}

PY="$(pick_python)" || {
    echo "no usable python3 found (need 3.8+)." >&2
    echo "  tried: PLANPLAN_PYTHON, python3, python3.13, python3.12," >&2
    echo "         /usr/bin/python3, ~/anaconda3/bin/python3" >&2
    echo "  set one:  PLANPLAN_PYTHON=/path/to/python3 bash $0 ..." >&2
    exit 2
}

require() {
    [ -f "$F/$1" ] || { echo "missing tool: $F/$1" >&2; exit 2; }
}

usage() { sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'; }

CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
    check)    require check_plans.py;        "$PY" "$F/check_plans.py" "$@" ;;
    dash)     require generate_dashboards.py; "$PY" "$F/generate_dashboards.py" "$@" ;;
    nodes)    require generate_nodes.py;     "$PY" "$F/generate_nodes.py" "$@" ;;
    project)  require generate_nodes.py;     "$PY" "$F/generate_nodes.py" "$@" --projections ;;
    adopt)    require generate_nodes.py;     "$PY" "$F/generate_nodes.py" "$@" --adopt-edges --adopt-checks ;;
    tree)     require render_plan.py;        "$PY" "$F/render_plan.py" "$@" --tree ;;
    view)     require render_plan.py;        "$PY" "$F/render_plan.py" "$@" ;;
    explore)  require explorer.py;           "$PY" "$F/explorer.py" "$@" ;;
    serve)
        require explorer.py
        root="${1:-}"; port="${2:-8800}"
        [ -n "$root" ] || { echo "serve needs a planning root" >&2; exit 2; }
        "$PY" "$F/explorer.py" "$root" --serve "$port"
        ;;
    migrate)  require migrate.py;            "$PY" "$F/migrate.py" "$@" ;;
    which)
        echo "interpreter: $PY"
        "$PY" --version
        echo "framework:   $F"
        ;;
    -h|--help|help) usage ;;
    *)
        echo "unknown command: $CMD" >&2
        echo >&2
        usage >&2
        exit 2
        ;;
esac
