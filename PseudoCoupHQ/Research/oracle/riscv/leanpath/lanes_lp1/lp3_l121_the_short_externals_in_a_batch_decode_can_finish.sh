#!/bin/bash
# lp3_l121_the_short_externals_in_a_batch_decode_can_finish.sh
#
# l120 REFUSED ALL 23 AND THE REASON WAS THE BATCH, NOT THE SLICES. Its
# walk.log says it in one line, next to the run that worked:
#
#   rm1, 9 units:   decode: 238 words,  lean rc=0,  74.8s
#   rm0, 23 units:  decode: 3747 words, lean rc=-1, 900.0s
#
# rc=-1 at exactly 900.0s is the decode step timing out. When decode returns
# nothing, every unit refuses for want of a constructor -- which reads as
# 'Sail would not decode it' and is really 'I asked for 3,747 words at once'.
# The word lists themselves are right: rm0 and rm1 for f64_eq are identical,
# 25 words, same first six and same last three.
#
# So this lane takes only the externals whose slices are SHORT -- 105
# instructions or fewer, fifteen of the twenty-three, about 1,000 words, four
# times the batch that decoded in 75 seconds. The eight long ones (283 to 712
# instructions) get their own lane rather than being carried along to time it
# out again.
#
# l119 PARSED NO WORDS AND THE FAULT WAS MINE, AGAIN IN THE SAME PLACE.
# The `.dis` files were produced with `--no-show-raw-insn`, so they carry
# mnemonics and no instruction words at all; the regex was right and the
# input file was wrong. The words live in the `.o`, and
# `llvm-objdump -d <op>.rm0.value.flat.o` prints them as the second field:
#
#        0: 7ff00613     li  a2, 0x7ff
#
# which is the same convention the nine rm1 units were built with. This is
# the second word-extraction bug of this line; the first is recorded in
# log 293 as the walker being right and my input wrong.
#
# STEP 1.2 OF THE TEMPLATE, DRIVEN AT ITS OWN CRITERION. the owner, 2026-09-17:
#
#   "if all of the arch-opcodes have full body Lean expressions, that is
#    S1.2: Complete: 100%. i think proof stuff belongs elsewhere. especially
#    considering we have no other reference of truth since the slice itself
#    is the only definition we have to work with."
#
# So 1.2 is measured as BODY-FULLNESS, not as proof. Counting it that way
# against what the corpus actually calls:
#
#   23  externals the corpus's own float arch-opcodes call
#    9  externals walked into Lean so far -- but AT ROUNDING MODE 1
#    0  at rounding mode 0, which is the mode every arch-unit in the corpus
#       maps to (`emulation:<op>_rm0`)
#
# The rm0 and rm1 flattened objects DIFFER, comparisons included: f64_eq is
# 1528 bytes at both modes and the bytes are not the same. So the nine already
# walked do not serve the arch-opcodes that call rm0, and the honest count
# before this lane is zero of twenty-three.
#
# WHAT IS ALREADY IN HAND, so the scope is clear: every one of the 67 slices
# EXISTS, flattened, and has been verified bit-exact against Berkeley
# SoftFloat. Nothing is being derived here. The only thing missing is the walk
# into Lean, and that mechanism is proven -- nine of nine certified.
#
# WHERE THIS WILL BE HARD, said before the run. The nine that worked were
# SHORT: f64_lt is 34 instructions. The twenty still needed are not --
#
#   i32_to_f64  49     f32_to_f64  97     f64_mul  306
#   i64_to_f64 100     f64_div    345     f32_add  644
#   f64_add    707     f64_sub    712
#
# -- and the `meaning_*` theorem is discharged by one `simp`. Whether that
# scales from 34 instructions to 707 is exactly what is unknown, and the
# converts (49 to 100) are the ones most likely to come back certified. The
# lane is ordered shortest-first so the useful results land even if the long
# ones time out.
#
# Fetches nothing. Writes $A/runs/float_rm0_short only. Budget: four hours.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
SF=PseudoCoupHQ/Research/oracle/riscv/softfloat_slices
P=/work/proof; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
S=$A/strip_perarm/strip.json
G=$A/runs/float_rm0_short; mkdir -p $G
t0=$(date +%s)
export WALK_JOBS=4 WALK_MAX_WORDS=1200
[ -f $S ] || { echo "FLAG: no $S"; exit 3; }

echo "[1/3] the externals the corpus calls, at rm0, shortest first  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os, re, collections
SF = "PseudoCoupHQ/Research/oracle/riscv/softfloat_slices"
G  = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_rm0_short"
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
long_ones = [u["name"] for u in units if len(u["words"]) > LIMIT]
units = [u for u in units if len(u["words"]) <= LIMIT]
print("  held back for their own lane (%d): %s" % (len(long_ones), ", ".join(long_ones)))
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
G  = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/float_rm0_short"
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
