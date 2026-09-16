#!/bin/bash
# lx1_l6_interp_sample.sh -- task lx1, lane 6: THE SAMPLE, first --
# five RISC-V cells x the seven interpreted targets = 35 runs, before
# the whole 255-cell population. No network: this lane and every one
# after it fetches nothing (lx1's one network lane was lane 1-5, the
# swift probe).
#
#   [1/3] the sha256 of every store this run reads
#   [2/3] the sample rule, LITERAL, before anything runs (interp_check's
#         own, unchanged)
#   [3/3] the loop: 5 cells x 7 targets
set -u

HQ=PseudoCoupHQ
RV="$HQ/Research/oracle/riscv"
PREFIX="$RV/lx1_interp_sample"
SRC="$RV/interp_src_lx1_sample"
total=3

i=1
echo "[$i/$total] the sha256 of riscv_reference.py READ this run (task sl1 regenerates it beside this task)"
sha256sum "$RV/riscv_reference.py"
sha256sum "$RV/twins.json"
sha256sum "$RV/model_table_rv.json"

i=2
echo ""
echo "[$i/$total] the sample rule, LITERAL"
python3 -c "
import sys
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation/interp')
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation/handful')
sys.path.insert(0, '$HQ/Research/op_pipeline')
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation')
import interp_check as IC
print(IC.SAMPLE_RULE)
"
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the loop, 5 cells x 7 targets"
rm -f "$PREFIX.jsonl"
python3 "$RV/rv_interp.py" sample "$RV/twins.json" "$RV/model_table_rv.json" \
  "$PREFIX" "$SRC" 5
echo "  exit: $?"

echo ""
echo "the store, one line per run:"
cat "$PREFIX.jsonl" | python3 -c "
import json, sys
for line in sys.stdin:
    row = json.loads(line)
    print('%-10s %-10s %3s  %-10s %-11s %s' % (
        row.get('mnem'), row.get('shape'), row.get('key_width'),
        row.get('lang'), row.get('outcome'),
        row.get('refusal_cause') or ''))
"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
