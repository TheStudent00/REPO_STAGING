#!/bin/bash
# L2 lane 9 — the sweep with the float-symbol and float-literal rules added
# and the printed-text cross-check made advisory, the build, and the census
# the report's translation table is made of.
set -u

TOTAL=3
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the sweep"
python3 -c "
import resource, sys, time
sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline/lean')
import model_translate as M
start = time.time()
M.model_command(M.HERE, M.os.path.join(M.HERE, 'archproof', 'Archproof'))
print('sweep wall %.1f s' % (time.time() - start))
print('sweep peak RSS %d kB'
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"

echo "[2/$TOTAL] lake build Archproof.Model"
cd archproof || exit 1
cat > Archproof.lean <<'LEAN'
import Archproof.Basic
import Archproof.Model
import Archproof.Render
LEAN
time lake build Archproof.Model
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[3/$TOTAL] the census"
python3 - <<'PY'
import json
d = json.load(open('PseudoCoupHQ/Research/op_pipeline/lean/'
                   'model_L2.json'))
per = d["per_mnemonic"]
translated = sorted(m for m in per if per[m]["translated"])
no_builder = sorted(m for m in per if per[m]["no_builder"])
left = sorted(m for m in per
              if not per[m]["translated"] and not per[m]["no_builder"])
print("| what | mnemonics |")
print("|---|---|")
print("| in the reference's opcode table | %d |" % len(per))
print("| a census row (an entry with NO builder) | %d |" % len(no_builder))
print("| at least one operand shape TRANSLATED into a Lean definition | %d |"
      % len(translated))
print("| a builder, but no operand shape this sweep spells | %d |" % len(left))
print("")
print("the census rows, by name: %s" % " ".join(no_builder))
print("")
print("--- the %d with a builder and nothing translated" % len(left))
for m in left:
    causes = per[m]["causes"]
    top = sorted(causes.items(), key=lambda kv: -kv[1])[:1]
    print("  %-10s attempts %3d  not modelled %3d  nothing written %3d  "
          "refused %3d  %s"
          % (m, per[m]["attempts"], per[m]["not_modelled"],
             per[m]["nothing"], per[m]["refused"],
             "; ".join("%s x%d" % (c, n) for c, n in top)))
print("")
print("--- every refusal cause over the whole sweep, counted")
tally = {}
for row in d["rows"]:
    if row["outcome"] != "REFUSED":
        continue
    for piece in (row.get("cause") or "?").split("; "):
        tally[piece.split(": ")[-1]] = \
            tally.get(piece.split(": ")[-1], 0) + 1
for cause, n in sorted(tally.items(), key=lambda kv: -kv[1]):
    print("  %-46s %d" % (cause[:46], n))
print("")
print("--- the printed-text cross-check, over every definition written")
cross = {}
for row in d["rows"]:
    for one in row.get("defs", []):
        state = one.get("cross_check")
        if state is None:
            state = "not run (a float definition: the printed-text route " \
                    "refuses every float node)"
        head = state.split(" ")[0]
        cross[head] = cross.get(head, 0) + 1
for head, n in sorted(cross.items(), key=lambda kv: -kv[1]):
    print("  %-16s %d" % (head, n))
print("")
print("--- the mnemonics whose definitions carry an uninterpreted float "
      "primitive")
floats = set()
for row in d["rows"]:
    for one in row.get("defs", []):
        if one.get("float"):
            floats.add(row["mnem"])
print("  %d distinct: %s" % (len(floats), " ".join(sorted(floats))))
print("")
print("definitions: %d" % d["definitions"])
print("opaque float primitives: %d -- %s"
      % (len(d["opaque_float_primitives"]),
         " ".join(d["opaque_float_primitives"])))
PY
echo "--- exit $?"
