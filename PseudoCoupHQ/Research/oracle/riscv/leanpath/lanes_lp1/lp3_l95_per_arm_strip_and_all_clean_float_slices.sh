#!/bin/bash
# lp3_l95_per_arm_strip_and_all_clean_float_slices.sh
#
# THE PER-ARM FIX, and what it unblocks.
#
# Sail puts several instructions in ONE clause and selects with a match:
#   UTYPE: LUI => off                      (pure: a sign-extended immediate)
#          AUIPC => get_arch_pc() + off    (an effect: reads the program counter)
# The strip refused the WHOLE clause over the AUIPC arm, so every body holding
# a `lui` -- "put this constant in a register" -- was refused over a sibling it
# never executes. 82 units of the corpus run of log 278 died this way.
#
# strip.py now certifies such a clause PER ARM: one definition and one theorem
# per pure arm, each stated with the CONCRETE constructor, and NO definition for
# an arm it cannot express, so nothing false can be said about it. walk.py takes
# the arm the decode actually produced and refuses one with no form.
#
# [1] re-strip the whole model: UTYPE must come out CERTIFIED, shape "arms".
# [2] walk all 43 flattened float operations that have no branch and no memory.
#     9 certified before (they had no lui); the other 34 were blocked by lui alone.
# Fetches nothing. Records: DevComms/log_293.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
R=$A/runs/float
cd $A
echo "[1/2] strip the model again: does UTYPE certify per arm?"
start=$(date +%s)
python3 -u -m leanpath strip $P $PLIB $A/strip_perarm 1200 > $R/strip.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - start ))s"
python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/strip_perarm/strip.json"))
s=d["summary"]
print("  certified %s, failed %s, refused %s, of %s" % (s["certified"], s["failed"], s["refused"], s["of"]))
print("  certified per arm: %s" % s.get("certified_per_arm"))
print("  arms with no pure form: %s" % s.get("arms_not_expressible"))
for r in d["rows"]:
    if r.get("shape") == "arms":
        print("  %-14s %-10s pure=%s  none=%s" % (r["clause"], r["verdict"], r.get("pure_arms"), r.get("impure_arms")))
PY
echo "[2/2] walk all 43 clean flattened float operations"
export WALK_JOBS=2 WALK_MAX_WORDS=300
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_perarm/strip.json $R/units_all.json $R/walk_all 1200 > $R/walk_all.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - start ))s"
python3 - <<'PY'
import json, collections
try:
    d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float/walk_all/walk.json"))
    print("  summary:", json.dumps(d["summary"]))
    c=collections.Counter(r["verdict"] for r in d["rows"])
    print("  ", dict(c))
    for r in d["rows"]:
        if r["verdict"] != "CERTIFIED":
            print("   %-24s %-10s %s" % (r["unit"], r["verdict"], (r.get("why") or "")[:110]))
except Exception as e:
    print("  no walk.json:", e)
PY
echo done
