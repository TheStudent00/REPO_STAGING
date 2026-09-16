#!/bin/bash
# lp3_l96_let_sharing_on_the_deep_float_slices.sh
#
# l95 showed the per-arm fix works: of the 43 clean flattened float operations,
# 0 are now REFUSED (lui no longer blocks), 21 CERTIFIED, and every failure is
# the SAME one: Lean's kernel reporting "deep recursion detected".
#
# The cause is named in log 278 section 7.3: compose substitutes each register's
# value into every later use, so a value read twice is copied twice and the
# term's nesting depth grows with the body length.
#
# walk.py now has let-sharing: bind each instruction's result to a name and
# refer to the name. The term becomes linear in the instruction count. It is
# OFF by default (WALK_LET_SHARING unset) so every existing run is unchanged;
# this lane turns it on.
#
# Fetches nothing. Records: DevComms/log_293.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
R=$A/runs/float
cd $A
echo "[1/1] the same 43 units, let-sharing ON"
export WALK_JOBS=2 WALK_MAX_WORDS=300 WALK_LET_SHARING=1
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_perarm/strip.json $R/units_all.json $R/walk_lets 1800 > $R/walk_lets.log 2>&1
echo "  rc=$? wall=$(( $(date +%s) - start ))s"
python3 - <<'PY'
import json, collections
try:
    d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float/walk_lets/walk.json"))
    print("  summary:", json.dumps(d["summary"]))
    c=collections.Counter(r["verdict"] for r in d["rows"]); print("  ", dict(c))
    for r in d["rows"]:
        if r["verdict"] != "CERTIFIED":
            print("   %-24s %-9s %s" % (r["unit"], r["verdict"], (r.get("why") or (r.get("errors") or [""])[0])[:110]))
except Exception as e:
    print("  no walk.json:", e)
PY
echo "  --- against l95 (let-sharing off): certified 21, failed 15, refused 0 ---"
echo done
