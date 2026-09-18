#!/bin/bash
# lp3_l107_the_bridge_again_with_the_gates_own_header.sh
#
# THE 35 UNDECIDED CLASSES OF l105, AND THE ONE THING BETWEEN THEM AND A
# VERDICT.
#
# Sail's Lean backend defines every comparison over Int:
#
#     def zopz0zI_u (x y : BitVec k_n) : Bool :=
#       ((BitVec.toNatInt x) <b (BitVec.toNatInt y))
#
# `<b` is Int.blt. `bv_decide` cannot bitblast it -- it abstracts the whole
# comparison and answers with a spurious counterexample. `BitVec.ult` is the
# same predicate and IS in its fragment. Sail ships no lemma between them:
# `@[simp_sail]` marks the definitions so they UNFOLD, which is what produces
# the Int spelling, and a grep for `ult` or `blt` across the Sail Lean library
# returns nothing. l104 measured that no library lemma closes it; l105 sized
# the cost -- 35 of 186 classes UNDECIDED, 86 arch-units, concentrated on
# narrow integer comparisons.
#
# WHY THIS IS GENERATED AND NOT TYPED. `Bridges.lean` was hand-written and
# broke on a Lean minor version within hours. `leanpath/sail_bridge.py` READS
# each `def zopz0z...` out of the Prelude, takes the family from the
# conversion it uses (`toInt` signed, `toNatInt` unsigned) and the relation
# from the comparison token, and writes the matching BitVec spelling. A
# definition whose shape it does not recognise is SKIPPED AND NAMED, so a
# rename in Sail shows up as a missing lemma and never as a wrong one.
#
# THE PROOF IS NOT GUESSED EITHER. The generator's `matrix` mode emits one
# theorem per (lemma, candidate tactic), so this lane reports WHICH tactic
# carried rather than only that something did. Nothing is added to the simp
# set on the strength of a tactic that was never run.
#
# Nothing downstream changes here. This lane only establishes whether the
# bridge exists and is provable; using it is the next lane.
#
# Fetches nothing. Writes $A/runs/bridge only. Budget: twenty minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof; PLIB=LeanIM
B=$A/runs/bridge; mkdir -p $B
t0=$(date +%s)
PRELUDE=$P/$PLIB/Prelude.lean
[ -f "$PRELUDE" ] || { echo "FLAG: no $PRELUDE"; exit 3; }
[ -f $A/leanpath/sail_bridge.py ] || { echo "FLAG: no sail_bridge.py"; exit 3; }

echo "[1/4] generate, reading the Prelude  ($(( $(date +%s) - t0 ))s)"
cd $A
python3 -m leanpath.sail_bridge $P $PLIB $B/SailBridge.lean 2>&1 | sed 's/^/  /'
python3 -m leanpath.sail_bridge $P $PLIB $B/SailBridgeMatrix.lean matrix 2>&1 | tail -2 | sed 's/^/  /'
echo "  lemmas: $(grep -c '^theorem sail_bridge' $B/SailBridge.lean)   matrix theorems: $(grep -c '^theorem sail_bridge' $B/SailBridgeMatrix.lean)"
python3 - <<'PY'
import json
d = json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/bridge/SailBridge.json"))
if d.get("skipped"):
    print("  SKIPPED definitions -- a rename would show up here:")
    for s in d["skipped"]:
        print("    %-18s %s" % (s["definition"], s["why"][:90]))
else:
    print("  every two-BitVec Bool definition in the Prelude was recognised")
PY

echo "[2/4] put the matrix to Lean  ($(( $(date +%s) - t0 ))s)"
cd $P
cp $B/SailBridgeMatrix.lean $P/SailBridgeMatrix.lean
timeout 900 lake env lean $P/SailBridgeMatrix.lean > $B/matrix.txt 2>&1
echo "  rc=$?  bytes=$(wc -c < $B/matrix.txt)"

echo "[3/4] which (lemma, tactic) carried  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, re, collections
B = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/bridge"
src = open(B + "/SailBridgeMatrix.lean").read()
out = open(B + "/matrix.txt").read()
meta = json.load(open(B + "/SailBridge.json"))
tactics = meta["meta"]["tactics_offered"]

# a theorem is PROVED unless Lean reported an error inside it.  Errors carry
# a line number, so each is attributed to the theorem whose span holds it.
spans = []
for m in re.finditer(r"^theorem (sail_bridge_\w+)", src, re.M):
    spans.append((src[:m.start()].count("\n") + 1, m.group(1)))
spans.append((10 ** 9, None))
failed = collections.defaultdict(list)
for m in re.finditer(r"^.*?:(\d+):\d+: error: (.*)$", out, re.M):
    line = int(m.group(1))
    owner = None
    for i in range(len(spans) - 1):
        if spans[i][0] <= line < spans[i + 1][0]:
            owner = spans[i][1]
            break
    if owner:
        failed[owner].append(m.group(2)[:70])

names = sorted(set(n.rsplit("_t", 1)[0] for _, n in spans if n))
print("  %-20s %s" % ("lemma", "  ".join("t%d" % i for i in range(len(tactics)))))
rows = []
for name in names:
    marks, first_ok = [], None
    for i in range(len(tactics)):
        key = "%s_t%d" % (name, i)
        ok = key not in failed
        marks.append(" ok" if ok else "  .")
        if ok and first_ok is None:
            first_ok = i
    rows.append({"lemma": name, "first_tactic_that_carried": first_ok,
                 "tactic_text": tactics[first_ok] if first_ok is not None else None})
    print("  %-20s %s   %s" % (name.replace("sail_bridge_", ""),
                               "  ".join(marks),
                               "" if first_ok is not None else "<-- NO TACTIC CARRIED"))
print()
carried = [r for r in rows if r["first_tactic_that_carried"] is not None]
print("  lemmas with a proof: %d of %d" % (len(carried), len(rows)))
for i, t in enumerate(tactics):
    n = sum(1 for r in carried if r["first_tactic_that_carried"] == i)
    if n:
        print("    t%d  x%-3d %s" % (i, n, t))
json.dump({"rows": rows, "tactics": tactics,
           "what": "which candidate tactic proved each generated bridge lemma"},
          open(B + "/bridge_verdicts.json", "w"), indent=1, sort_keys=True)
PY

echo "[4/4] the usable file, with only the lemmas that carried  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json
B = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/bridge"
v = json.load(open(B + "/bridge_verdicts.json"))
good = [r for r in v["rows"] if r["first_tactic_that_carried"] is not None]
meta = json.load(open(B + "/SailBridge.json"))
by_def = {"sail_bridge_" + l["definition"]: l for l in meta["lemmas"]}
lines = ["-- GENERATED, and every lemma below was PUT TO LEAN and carried.",
         "-- The tactic beside each is the one that actually proved it.",
         "import LeanIM", ""]
for r in good:
    l = by_def.get(r["lemma"])
    if l is None:
        continue
    left, right = ("y", "x") if l["operands_swapped"] else ("x", "y")
    lines += ["-- proved by: %s" % r["tactic_text"],
              "theorem %s {n : Nat} (x y : BitVec n) :" % r["lemma"],
              "    %s x y = %s %s %s := by" % (l["definition"],
                                               l["bitvec_predicate"], left, right),
              "  %s" % r["tactic_text"].replace("%(def)s", l["definition"])
                       .replace("%(target)s", l["bitvec_predicate"])
                       .replace("%(conv)s", "BitVec.toInt"
                                if l["family"] == "signed" else "BitVec.toNatInt"),
              ""]
open(B + "/SailBridgeProved.lean", "w").write("\n".join(lines))
print("  wrote SailBridgeProved.lean with %d lemma(s)" % len(good))
PY
cd $P
if [ -s $B/SailBridgeProved.lean ] && grep -q "^theorem" $B/SailBridgeProved.lean; then
  cp $B/SailBridgeProved.lean $P/SailBridgeProved.lean
  timeout 600 lake env lean $P/SailBridgeProved.lean > $B/proved.txt 2>&1
  rc=$?
  echo "  the proved file elaborates on its own: rc=$rc, $(grep -c error $B/proved.txt) error line(s)"
  head -4 $B/proved.txt | sed 's/^/    /'
else
  echo "  FLAG: no lemma carried; there is nothing to use"
fi
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
