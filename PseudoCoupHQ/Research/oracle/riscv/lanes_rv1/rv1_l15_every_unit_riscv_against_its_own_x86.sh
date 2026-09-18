#!/bin/bash
# rv1_l15_every_unit_riscv_against_its_own_x86.sh
#
# THE CROSS-ARCHITECTURE MAPPING, WIDE. `claim_check.py` walks a unit's
# x86-64 ship body with `op_pipeline/reference.py`, walks its riscv64 body
# with the RISC-V reference, and asks z3 whether the two agree at the unit's
# own answer width. Task rv1 ran it on ELEVEN units -- one per cell of the
# arch-opcode model table -- and got seven IDENTICAL_AFTER_NORMALIZE, three
# DIFFER and one NO_CORPUS_UNIT.
#
# Nothing about the checker was ever limited to eleven. `attest_rv.json`
# carries a riscv64 body for 507 units and marks `x86_ship_body_in_the_store`
# on EVERY ONE of them, and the term store holds an answer home for all 507.
# So the pairing is complete and has simply never been run.
#
#   pick_units_all.py  ->  units_all.json (507 rows, all PICKED)
#                          carved_all.json (the riscv64 bodies)
#   claim_check.py     ->  claim_all.json
#
# NOTHING IS GUESSED. A unit whose term store record names no answer home is
# written `NO_ANSWER_HOME` and skipped rather than given an invented one --
# the answer home is what the comparison reads out of, so inventing one would
# invent the verdict. On this corpus that case does not arise: all 507 have
# one, and the picker says so in its own output.
#
# WHY IT MUST RUN HERE AND NOT ON THE LAPTOP: `reference.py` shells out to
# `llvm-objdump`, which the laptop does not have. A first attempt there died
# on it forty units in and was stopped; this lane is the re-run in the image
# that carries the toolchain.
#
# Fetches nothing. Writes $RV/xarch only. Budget: one hour.
set -uo pipefail
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
R=PseudoCoupHQ
OP=$R/Research/op_pipeline
RV=$R/Research/oracle/riscv
OUT=$RV/xarch; mkdir -p $OUT
t0=$(date +%s)

echo "[1/4] the toolchain this needs  ($(( $(date +%s) - t0 ))s)"
for t in llvm-objdump clang python3; do
  p=$(command -v $t 2>/dev/null) || { echo "  FLAG: $t missing"; exit 3; }
  printf "  %-14s %s\n" "$t" "$p"
done
python3 -c "import z3; print('  z3            %s' % z3.get_version_string())" || exit 3
for f in $OP/reference.py $OP/term.py $OP/term66_store $RV/attest_rv.json $RV/claim_check.py $RV/pick_units_all.py; do
  [ -e "$f" ] || { echo "  FLAG: missing $f"; exit 3; }
done
echo "  every input present"

echo "[2/4] pair every unit that has both lowerings  ($(( $(date +%s) - t0 ))s)"
python3 $RV/pick_units_all.py $OP $RV/attest_rv.json $OUT 2>&1 | sed 's/^/  /'
[ -f $OUT/units_all.json ] || { echo "  FLAG: the picker wrote nothing"; exit 3; }

echo "[3/4] riscv64 against x86-64, unit by unit  ($(( $(date +%s) - t0 ))s)"
python3 -u $RV/claim_check.py $OP $OUT/units_all.json $OUT/carved_all.json \
        $OUT/claim_all > $OUT/claim_all.log 2>&1
rc=$?
echo "  claim_check rc=$rc, $(grep -c '^\[' $OUT/claim_all.log) units walked"
tail -3 $OUT/claim_all.log | sed 's/^/  /'
[ -f $OUT/claim_all.json ] || { echo "  FLAG: no claim_all.json"; exit 3; }

echo "[4/4] the table  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections
p = "PseudoCoupHQ/Research/oracle/riscv/xarch/claim_all.json"
rows = json.load(open(p))["rows"]
tally = collections.Counter(r["outcome"] for r in rows)
print("  outcomes over %d units:" % len(rows))
for k, n in tally.most_common():
    print("    %-26s %4d" % (k, n))

diff = [r for r in rows if r["outcome"] == "DIFFER"]
print()
print("  THE DIVERGENCES -- where riscv64 and x86-64 compute different bits")
print("  for the SAME compiler-operator: %d" % len(diff))
by = collections.Counter((r.get("lang"), r.get("operator"),
                          str(r.get("lhs_type")), str(r.get("rhs_type")))
                         for r in diff)
for (lg, op, lt, rt), n in by.most_common(25):
    print("    %-4s %-6s %-12s %-12s x%d" % (lg, op, lt, rt, n))
print()
print("  first ten, with the input that breaks them:")
for r in diff[:10]:
    print("    %-12s %-4s %-14s width %-3s  %s"
          % (r.get("unit"), r.get("lang"), (r.get("expression") or "")[:14],
             r.get("answer_width"), str(r.get("counterexample"))[:70]))

ref = [r for r in rows if "REFUSED" in (r["outcome"] or "")]
if ref:
    print()
    print("  walks refused: %d" % len(ref))
    c = collections.Counter((r["outcome"], (r.get("cause") or "")[:60]) for r in ref)
    for (o, why), n in c.most_common(12):
        print("    %-20s %-62s x%d" % (o, why, n))
PY
OPD=PseudoCoupHQ/Research/op_pipeline
[ -f $OUT/claim_all.json ] && python3 $OPD/check_no_spelling_keys.py $OUT/claim_all.json 2>&1 | tail -1
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
