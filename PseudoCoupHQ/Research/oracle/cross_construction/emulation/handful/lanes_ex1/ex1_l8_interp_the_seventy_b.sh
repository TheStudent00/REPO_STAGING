#!/usr/bin/env bash
# ex1_l8_interp_the_seventy_b.sh -- task ex1, step 6 again, after the
# first pass of lane ex1_l7 found four defects of this task's own and
# each was fixed in the LAYER THAT OWNS IT, never worked around:
#
#   1. php's mask was `(1 << $w) - 1`, and php's `1 << 63` is
#      PHP_INT_MIN, so at 63 and 64 bits the mask left the integers for
#      a double.  `ex_maskbits` now spells it, and the run that caught
#      it is on the record: `shr` cl_gpr 64 answered 0 where the
#      reference answered 1 at the point [2, 1].
#   2. php's multiply was in 32-bit halves and a 32-by-32 product is up
#      to 2^64, which php also leaves the integers for.  It is in
#      16-bit limbs now; the run that caught it answered 2147483648
#      where the reference answered 2147483647 at the point
#      [2147483649, 4294967295].
#   3. `out` is a reserved word in c#, so every c# build refused with
#      `error CS1002: ; expected`.  The variable is `answers` now.
#   4. the GLOSS column read the first `return` in the FILE, which is
#      one of the prelude's.  It reads the emulation's own body now.
#
# and one thing that was not a defect but a wrong OBJECT: the ten cells
# were being read out of the 253-cell outer set, which does not hold
# `sub` imm_gpr 64.  They are read out of the handful's own cells file.
#
# THE FIRST PASS'S STORE IS KEPT, NOT OVERWRITTEN, under
# `expand1_interp_pass1.jsonl`.  Nothing is deleted.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/5] the first pass's store, kept under its own name"
if [ -f expand1_interp.jsonl ] && [ ! -f expand1_interp_pass1.jsonl ]; then
    mv expand1_interp.jsonl expand1_interp_pass1.jsonl
    echo "   expand1_interp.jsonl -> expand1_interp_pass1.jsonl"
    wc -l expand1_interp_pass1.jsonl
else
    echo "   nothing to move"
fi

echo ""
echo "[2/5] the seventy"
python3 expand1.py interp_run

echo ""
echo "[3/5] the aggregate"
python3 expand1.py interp_aggregate

echo ""
echo "[4/5] the table"
python3 expand1.py interp_table

echo ""
echo "[5/5] the two float cells on the COMPILED route, so the two "
echo "      routes' causes can be read side by side"
python3 - <<'PYEOF'
import json
path = "expand1_runs.jsonl"
wanted = {("addss", "xmm_xmm", 32), ("cvtsi2sd", "gpr_xmm", 64),
          ("cvtsi2ss", "gpr_xmm", 32)}
for line in open(path):
    run = json.loads(line)
    key = (run["mnem"], run["shape"], run["key_width"])
    if key not in wanted:
        continue
    print("== `%s` %s %s on cpp   route %s"
          % (key[0], key[1], key[2], run.get("route")))
    for place in run["places"]:
        print("   place %-14s rendered %s  %s"
              % (place["writes"], place.get("rendered"),
                 place.get("refusal_cause") or
                 ((place.get("check") or {}).get("outcome"))))
        if place.get("refusal_detail"):
            print("      detail: %s" % place["refusal_detail"])
PYEOF
echo "done"
