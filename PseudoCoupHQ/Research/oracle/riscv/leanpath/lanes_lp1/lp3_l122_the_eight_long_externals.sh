#!/bin/bash
# lp3_l122_the_eight_long_externals.sh
#
# the owner, 2026-09-17: 1.2 is measured as BODY-FULLNESS, not proof.
#
# l121 walked 15 and ALL 15 produced a Lean body. Five also certified; the
# other ten failed the certification theorem on `(kernel) deep recursion` --
# which is the proof, not the body. `i64_to_f32`'s body is 1,915,374
# characters and exists.
#
# So the remaining gap on the slice side is the 8 never attempted:
#
#   f32_mul 283   f32_div 290   f64_mul 306   f64_div 345
#   f32_add 644   f32_sub 675   f64_add 707   f64_sub 712
#
# Decode is the step that timed out in l120 at 3,747 words; these eight are
# ~3,960 words together, so they go in two batches of four rather than one.
#
# Fetches nothing. Writes $A/runs/float_rm0_long only. Budget: four hours.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
SF=PseudoCoupHQ/Research/oracle/riscv/softfloat_slices
P=/work/proof; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
S=$A/strip_perarm/strip.json
G=$A/runs/float_rm0_long; mkdir -p $G
t0=$(date +%s)
export WALK_JOBS=4 WALK_MAX_WORDS=1200
[ -f $S ] || { echo "FLAG: no $S"; exit 3; }

echo "[1/3] the externals the corpus calls, at rm0, shortest first  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os, re, collections
SF = "PseudoCoupHQ/Research/oracle/riscv/softfloat_slices"
G  = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_rm0_long"
# which externals does the corpus actually call?  read off the arch-units,
# never from a hand-written list
need = set()
for r in json.load(open(SF + "/arch_units/arch_units.json"))["units"]:
    for o in r.get("arch_opcodes") or []:
        m = o.get("mapped_to") or ""
        if m.startswith("emulation:"):
            need.add(re.sub(r"_rm\d+$", "", m.split(":", 1)[1]))
print("  externals the corpus calls: %d" % len(need))

import subprocess
# 4 or 8 hex digits: a compressed instruction is two bytes
WORD = re.compile(r"^\s+[0-9a-f]+:\s+([0-9a-f]{4}(?:[0-9a-f]{4})?)\s")
units = []
for op in sorted(need):
    obj = os.path.join(SF, "flattened", "%s.rm0.value.flat.o" % op)
    if not os.path.exists(obj):
        print("  MISSING slice object: %s" % op); continue
    out = subprocess.run(["llvm-objdump", "-d", obj], capture_output=True,
                         text=True).stdout
    words = [m.group(1) for m in (WORD.match(l) for l in out.split("\n")) if m]
    if not words:
        print("  no words parsed: %s" % op); continue
    units.append({"name": "float_" + op, "lang": "c", "words": words,
                  "symbol": "%s_rm0_value_flat" % op,
                  "cell_display": "SoftFloat %s flattened, rounding mode 0" % op,
                  "source": obj})
units.sort(key=lambda u: len(u["words"]))
# only what a decode batch can finish; the long ones get their own lane
LIMIT = 120
BATCH = int(__import__('os').environ.get('SLICE_BATCH', '0'))
long_ones = [u for u in units if len(u["words"]) > LIMIT]
long_ones.sort(key=lambda u: len(u["words"]))
units = long_ones[:4] if BATCH == 0 else long_ones[4:]
print("  this batch (%d of %d long): %s" % (len(units), len(long_ones), ", ".join(u["name"] for u in units)))
fh = open(G + "/units.json", "w")
json.dump(units, fh, indent=1, sort_keys=True); fh.write("\n"); fh.close()
print("  units written: %d, shortest first" % len(units))
for u in units:
    print("    %-14s %4d instructions" % (u["name"], len(u["words"])))
PY
[ -f $G/units.json ] || { echo "  FLAG: no units.json"; exit 3; }

echo "[2/3] walk them  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 -u -m leanpath walk $P $X $PLIB $S $G/units.json $G/walk 1800 > $G/walk.log 2>&1
echo "  rc=$?  $(tail -1 $G/walk.log)"

echo "[3/3] what is body-full now  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections, os, re
SF = "PseudoCoupHQ/Research/oracle/riscv/softfloat_slices"
G  = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_rm0_long"
rows = json.load(open(G + "/walk/walk.json"))["rows"]
units = {u["name"]: len(u["words"]) for u in json.load(open(G + "/units.json"))}
by = collections.Counter(r.get("verdict") for r in rows)
print("  walk verdicts: %s" % dict(by))
print()
print("  %-16s %6s  %s" % ("external", "insts", "verdict"))
for r in sorted(rows, key=lambda x: units.get(x["unit"], 0)):
    print("  %-16s %6d  %s" % (r["unit"], units.get(r["unit"], 0), r.get("verdict")))
good = {r["unit"].replace("float_", "") for r in rows if r.get("verdict") == "CERTIFIED"}
# which float arch-opcodes are body-full now?
op_of = collections.defaultdict(set)
for r in json.load(open(SF + "/arch_units/arch_units.json"))["units"]:
    for o in r.get("arch_opcodes") or []:
        m = o.get("mapped_to") or ""
        if m.startswith("emulation:"):
            op_of[o["mnemonic"]].add(re.sub(r"_rm\d+$", "", m.split(":", 1)[1]))
full = sorted(m for m, e in op_of.items() if e <= good)
print()
print("  STEP 1.2, at its own criterion -- float arch-opcodes with a body-full")
print("  Lean expression: %d of %d" % (len(full), len(op_of)))
print("    %s" % ", ".join(full))
missing = sorted(set(op_of) - set(full))
if missing:
    print("  still opaque: %s" % ", ".join(missing))
PY
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
