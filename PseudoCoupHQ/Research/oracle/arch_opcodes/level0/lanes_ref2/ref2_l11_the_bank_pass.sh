#!/bin/bash
# ref2 lane 11 -- the loop in bank mode, with the reference in its re-attempt
# rule and the audit at 100%.
#
# `ref2_bank.py` patches `autopoly.code_version_of` and `autopoly.version_key`
# IN THIS PROCESS so the loop's own "has the machinery moved?" rule reads the
# reference's two sha256 beside the driver's, the loop's and the renderer's.
# Neither shared file is edited.  Every certified triple is re-derived (the
# audit at `--audit-share 1`), and the pass writes its own store `ref2_runs.jsonl`
# and its own rendered sources `src_ref2/` beside every earlier pass's.
#
# WHAT AN ALARM IS AND IS NOT.  An ALARM is a re-derived verdict that differs
# from its certificate ON IDENTICAL INPUTS -- same term text, same source
# sha256, same compiler and flags -- and the pass stops on one.  A key whose
# TERM TEXT moved is not identical inputs: it is banked beside the old
# certificate as a changed artifact, which is exactly what this task's four
# corrections are expected to produce.
#
# Memory bound: 12 GB for the lane; the loop's own is 6 GB with its own named
# abort, and this task's is ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
A=$HQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work/ref2home
mkdir -p "$HOME"
cd "$L0" || exit 1

echo "[1/4] the pass"
python3 "$L0/ref2_bank.py" audit
echo "--- exit $?"

echo "[2/4] the cost line"
cd "$A" || exit 1
python3 autopoly.py --pass ref2 --audit-share 1 --bank report | \
    grep -v 'peak resident'
echo "--- exit $?"

echo "[3/4] every audited triple whose artifact changed"
python3 autopoly.py --pass ref2 --audit-share 1 --bank changed | \
    grep -v 'peak resident' | head -60
echo "--- exit $?"

echo "[4/4] the audit's own answers"
python3 autopoly.py --pass ref2 --audit-share 1 --bank audit | \
    grep -v 'peak resident' | tail -40
echo "--- exit $?"
