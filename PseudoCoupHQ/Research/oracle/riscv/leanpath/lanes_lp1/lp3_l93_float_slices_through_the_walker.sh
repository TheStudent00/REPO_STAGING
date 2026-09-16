#!/bin/bash
# lp3_l93_float_slices_through_the_walker.sh -- THE STEP NEVER DONE:
# take RISC-V float operations that have been sliced out of Berkeley
# SoftFloat and flattened to a single branch-free block, and run them
# through the walker, which composes Sail's own instruction definitions
# to get a Lean expression. Four operations, the ones with no branches
# AND no memory, so nothing the walker refuses is present. Fetches
# nothing. Records: DevComms/log_293.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
R=$A/runs/float
cd $A
echo "[1/2] the four units"
python3 -c "
import json; u=json.load(open('$R/units.json'))
for x in u: print('  %-16s %2d words' % (x['name'], len(x['words'])))
"
echo "[2/2] walk: decode each word with Sail's decoder, compose Sail's definitions, certify in Lean"
export WALK_JOBS=2 WALK_MAX_WORDS=200
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S $R/units.json $R/walk 900 > $R/walk.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - start ))s"
grep -E "CERTIFIED|REFUSED|FAILED|decode:|Traceback" $R/walk.log | cut -c1-200
python3 - <<'PY'
import json
try:
    d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float/walk/walk.json"))
    print("  summary:", json.dumps(d["summary"]))
    for r in d["rows"]:
        print("  %-16s %-10s %s" % (r["unit"], r["verdict"], (r.get("proposal") or r.get("why") or "")[:150]))
except Exception as e:
    print("  no walk.json:", e)
PY
echo done
