#!/bin/bash
# rd1 lane 4 -- where the one rule fires, what is left disproved and why, that
# c, c++ and rust are untouched byte for byte, and the spelling guard.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1g

echo "[1/5] c, c++ and rust are untouched: the sample's sources against the pre-rd1 render"
timeout 300 python3 - <<'PYEOF'
import os
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
NEW = G + "/src_rd1_sample"
OLD = G + "/emulations_riscv64"
same = {}
differ = {}
missing = []
for name in sorted(os.listdir(NEW)):
    old = os.path.join(OLD, name)
    if not os.path.exists(old):
        missing.append(name)
        continue
    target = name.split("__")[2]
    if open(old, "rb").read() == open(os.path.join(NEW, name), "rb").read():
        same[target] = same.get(target, 0) + 1
        continue
    differ[target] = differ.get(target, 0) + 1
    continue
print("| language | sources byte-identical to the pre-rd1 render | sources that differ |")
print("|---|---|---|")
for target in ("c", "cpp", "rust", "go"):
    print("| %s | %d | %d |" % (target, same.get(target, 0),
                                differ.get(target, 0)))
if missing:
    print("not in the pre-rd1 render at all: %s" % ", ".join(missing))
PYEOF
echo "  exit: $?"

echo "[2/5] the go divide, before and after, side by side"
diff -u "$G/emulations_riscv64/div_gpr_gpr_gpr_64__reg_a0__go__native_first.go" \
        "$G/src_rd1_sample/div_gpr_gpr_gpr_64__reg_a0__go__native_first.go" || true

echo "[3/5] where the rule fires: every RISC-V cell rendered for go, render only, guards counted"
cat > /work/rd1g/guards.py <<'PYEOF'
"""render only, no compile: how many of the 255 cells carry a conditional
whose branch holds a trapping node, on go, under each policy."""
import json
import os
import sys

G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
RV = "PseudoCoupHQ/Research/oracle/riscv"
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
OP = "PseudoCoupHQ/Research/op_pipeline"
sys.path.insert(0, G)
sys.path.insert(0, RV)
sys.path.insert(0, os.path.join(EMU, "handful"))
sys.path.insert(0, os.path.join(EMU, "autopoly"))
sys.path.insert(0, EMU)
sys.path.insert(0, os.path.join(EMU, "rust"))
sys.path.insert(0, os.path.join(EMU, "go"))
sys.path.insert(0, os.path.join(EMU, "swift"))

import rv_general as RVG
import render_general as RGEN
import twins as TW
import rv_loop as RL
import handful as H
import construct as CONS
import inherit_rv3 as INH3


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main():
    INH3.install()
    TW.bring_in(OP, OP)
    rows = json.load(open(RV + "/twins.json"))["rows"]
    cells = []
    for row in rows:
        cells.append({"mnem": row["mnem"], "shape": row["shape"],
                      "key_width": row["key_width"],
                      "places": [p["writes"] for p in row["places"]]})
        continue
    terms, _operands = RL.riscv_terms(RV + "/model_table_rv.json")
    say("| language | policy | cells rendered | cells with a guarded "
        "conditional | guarded conditionals |")
    say("|---|---|---|---|---|")
    fired = {}
    for target in ("go", "c"):
        word = CONS.word_of(target)
        for policy in ("native_first", "all_constructed"):
            rendered = 0
            cells_with = 0
            guards = 0
            for cell in cells:
                key = (cell["mnem"], cell["shape"], cell["key_width"])
                carried = 0
                for place in cell["places"]:
                    term = terms.get((key, place))
                    if term is None:
                        continue
                    slotted, _refusal = RL.in_parameter_slots(
                        sys.modules["term"], term)
                    if slotted is None:
                        continue
                    record = H.place_record("reg_rdi", slotted)
                    if record.get("families") is None:
                        continue
                    ordered = H.renderer_input(record["term"])
                    label = "%s_%s_%d__%s__%s__%s" % (
                        cell["mnem"], cell["shape"], cell["key_width"],
                        place, target, policy)
                    label = label.replace(".", "_")
                    try:
                        made = RGEN.render(ordered, target,
                                           record["families"],
                                           record["home"]["family"],
                                           record["bits"], label, word,
                                           policy,
                                           record.get("text") or "")
                    except Exception:                         # noqa: BLE001
                        continue
                    rendered = rendered + 1
                    carried = carried + made["guards"]
                    guards = guards + made["guards"]
                    continue
                if carried > 0:
                    cells_with = cells_with + 1
                    fired.setdefault((target, policy), [])
                    fired[(target, policy)].append(
                        (cell["mnem"], cell["shape"], cell["key_width"],
                         carried))
                continue
            say("| %s | %s | %d | %d | %d |"
                % (target, policy, rendered, cells_with, guards))
            continue
        continue
    say("")
    say("the cells whose go render carries one, LITERAL")
    say("| mnem | shape | width | policy | guarded conditionals |")
    say("|---|---|---|---|---|")
    for target, policy in sorted(fired):
        if target != "go":
            continue
        for mnem, shape, width, count in fired[(target, policy)]:
            say("| `%s` | `%s` | %d | %s | %d |"
                % (mnem, shape, width, policy, count))
            continue
        continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF
timeout 3000 python3 /work/rd1g/guards.py
echo "  exit: $?"

echo "[4/5] what is left disproved, per language, with the counterexample"
timeout 300 python3 - <<'PYEOF'
import json
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
NAME = {"c": "c", "cpp": "c++", "rust": "rust", "go": "go"}
held = {}
for line in open(G + "/rd1_all.jsonl"):
    text = line.strip()
    if not text:
        continue
    row = json.loads(text)
    cell = row["cell"]
    held[(cell["mnem"], cell["shape"], cell["key_width"],
          row["target"])] = row
print("| mnem | shape | width | language | outcome | the counterexample, LITERAL |")
print("|---|---|---|---|---|---|")
for key in sorted(held):
    row = held[key]
    if row.get("kind") != "sat":
        continue
    verdict = row.get("verdict") or {}
    counter = verdict.get("counterexample")
    print("| `%s` | `%s` | %s | %s | %s | %s |"
          % (key[0], key[1], key[2], NAME.get(key[3], key[3]),
             verdict.get("outcome"),
             ("%s" % counter)[:200].replace("\n", " ")))
print("")
print("| mnem | shape | width | language | refused, the cause |")
print("|---|---|---|---|---|")
for key in sorted(held):
    row = held[key]
    if row.get("kind") != "refused":
        continue
    verdict = row.get("verdict") or {}
    reason = verdict.get("reason") or verdict.get("outcome")
    print("| `%s` | `%s` | %s | %s | %s |"
          % (key[0], key[1], key[2], NAME.get(key[3], key[3]),
             ("%s" % reason)[:160].replace("\n", " ")))
PYEOF
echo "  exit: $?"

echo "[5/5] the spelling guard over every json this task wrote, and the exempt count"
timeout 300 python3 "$OP/check_no_spelling_keys.py" \
  "$G/rd1_all.json" "$G/rd1_sample.json"
echo "  the guard's exit: $?"
echo -n "  grep -c exempt over the files this task added: "
grep -c exempt "$RV/lanes_rd1/"*.sh | tr '\n' ' '
echo ""
