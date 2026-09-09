#!/bin/bash
# L2 lane 8 — the sweep with its second pass (the flags, machine stack and x87
# stack pre-seeded for the opcodes that READ them), the build, and the census.
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

echo "[3/$TOTAL] the census: mnemonics modelled / translated / refused by cause"
python3 - <<'PY'
import json
d = json.load(open('PseudoCoupHQ/Research/op_pipeline/lean/'
                   'model_L2.json'))
per = d["per_mnemonic"]
translated = sorted(m for m in per if per[m]["translated"])
no_builder = sorted(m for m in per if per[m]["no_builder"])
refused_only = sorted(m for m in per
                      if not per[m]["translated"] and not per[m]["no_builder"])
print("mnemonics in the opcode table            : %d" % len(per))
print("  a census row (an entry with no builder): %d -- %s"
      % (len(no_builder), " ".join(no_builder)))
print("  at least one operand shape TRANSLATED  : %d" % len(translated))
print("  a builder, but no shape translated     : %d" % len(refused_only))
print("")
print("--- the %d with a builder but nothing translated, by cause"
      % len(refused_only))
for m in refused_only:
    causes = per[m]["causes"]
    top = sorted(causes.items(), key=lambda kv: -kv[1])[:2]
    print("  %-12s attempts %3d  not modelled %3d  nothing written %3d  "
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
        cause = piece.split(": ")[-1]
        tally[cause] = tally.get(cause, 0) + 1
for cause, n in sorted(tally.items(), key=lambda kv: -kv[1]):
    print("  %-28s %d" % (cause, n))
print("")
print("--- the float mnemonics: translated with uninterpreted primitives")
floats = []
for row in d["rows"]:
    for one in row.get("defs", []):
        if one.get("float"):
            floats.append(row["mnem"])
print("  %d distinct: %s" % (len(set(floats)), " ".join(sorted(set(floats)))))
print("")
print("definitions: %d" % d["definitions"])
print("opaque float primitives: %d" % len(d["opaque_float_primitives"]))
PY
echo "--- exit $?"
