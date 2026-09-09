#!/usr/bin/env bash
# R3: run each harvest source's own tests where it lives.
# Usage:  bash PseudoCoup_v6/Research/r3_harvest_verification/run_checks.sh
# Continues on failure; writes per-suite logs + runs/status.md.
# UNVERIFIED by execution (staged while the session sandbox was
# down); if an invocation is wrong, its log says exactly how.

set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/runs"
mkdir -p "$OUT"
STATUS="$OUT/status.md"
P=~/Programming

echo "| suite | result | log |" > "$STATUS"
echo "|---|---|---|" >> "$STATUS"

run_suite () {
    # run_suite <name> <workdir> <cmd...>
    local name="$1"; shift
    local dir="$1"; shift
    local log="$OUT/${name}.log"
    echo "== $name =="
    if [ ! -d "$dir" ]; then
        echo "| $name | MISSING-DIR | $dir |" >> "$STATUS"
        echo "  missing dir: $dir"; return
    fi
    ( cd "$dir" && "$@" ) > "$log" 2>&1
    local rc=$?
    if [ $rc -eq 0 ]; then
        echo "| $name | PASS | runs/${name}.log |" >> "$STATUS"
        echo "  PASS"
    elif grep -qiE "command not found|No such file or directory: '?(cargo|kotlinc|node|dart|gradle)|not found" "$log"; then
        echo "| $name | needs-host-toolchain | runs/${name}.log |" >> "$STATUS"
        echo "  needs-host-toolchain (rc=$rc)"
    else
        echo "| $name | FAIL (rc=$rc) | runs/${name}.log |" >> "$STATUS"
        echo "  FAIL rc=$rc (see runs/${name}.log)"
    fi
}

# --- T2 identity + record-shape sources (v0 pseudokotlin) ---
V0="$P/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin"
run_suite v0_idgen_check          "$V0" python3 idgen.py --check
run_suite v0_ledger_unified_check "$V0" python3 ledger_unified.py --check

# --- T2 semantic payload + T3 snapshot-net source (v4/PseudoCoup) ---
# needs pseudoir importable: the CLI's gate/hoisting units import it
run_suite pseudocoup_pytest "$P/PseudoCoup" \
    env PYTHONPATH="$P/PseudoIR" python3 -m pytest tests/ -q

# --- registry + gate + three-way oracle (pseudoir) ---
# tests/ ONLY: repo-wide collection trips on research scratch files
# that sys.exit at import (v2/prober/u_namespace/test_U.py).
# PYTHONPATH: emitted programs are run as subprocesses and import
# pseudoir.U — the package must be importable in the subprocess env
# (historically satisfied by pip install -e; egg-info is the fossil)
run_suite pseudoir_pytest "$P/PseudoIR" \
    env PYTHONPATH="$P/PseudoIR" python3 -m pytest tests/ -q

# --- PCv5 gates (T3/T4 sources; rustc-verified artifacts) ---
run_suite pcv5_test_vocab "$P/PseudoCoup_v5/Research/vocab_transpiler" \
    python3 test_vocab.py
run_suite pcv5_differential_python_side \
    "$P/PseudoCoup_v5/Research/vocab_transpiler/differential" \
    python3 run_python_side.py
run_suite pcv5_cpp_agreement "$P/PseudoCoup_v5/Research/cpp_ingress" \
    python3 test_agreement.py

echo
echo "== status =="
cat "$STATUS"
echo
echo "table written to $STATUS — REPORT.md gets written from these logs."
