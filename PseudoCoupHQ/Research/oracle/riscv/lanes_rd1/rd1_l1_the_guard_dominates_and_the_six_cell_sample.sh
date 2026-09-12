#!/bin/bash
# rd1 lane 1 -- the one rule in render_general.py, measured: a conditional whose
# branch holds a trapping node is written as an `if` that dominates the
# operation. Six cells, the divide family first, on c cpp go rust, both routes,
# with go's `div` source and its compiled body printed whole.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1 /work/rd1s /work/rd1body

echo "[1/5] the file this task changed and the files it reads, sha256"
sha256sum "$G/render_general.py" "$EMU/go/go_render.py" \
  "$EMU/swift/swift_render.py" "$EMU/rust/rust_render.py" \
  "$G/build.py" "$G/rv_general.py" "$RV/twins.json" \
  "$RV/model_table_rv.json" "$RV/riscv_reference.py"

cat > /work/rd1/sample.py <<'PYEOF'
"""rd1's six-cell sample: the population ordered with the divide family
first, on c cpp go rust, both routes, sources saved."""
import json
import os
import sys

G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
RV = "PseudoCoupHQ/Research/oracle/riscv"
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
OP = "PseudoCoupHQ/Research/op_pipeline"
sys.path.insert(0, G)
sys.path.insert(0, RV)

import rv_general as RVG
import render_general as RGEN
import rv_loop as RL
import inherit as INH
import inherit_rv3 as INH3

MODEL = RV + "/model_table_rv.json"
TWINS = RV + "/twins.json"
OUT = G + "/src_rd1_sample"
EXT = {"c": "c", "cpp": "cpp", "go": "go", "rust": "rs"}
HOW_MANY = 6


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def dividing_first(twins_path):
    """the population, the divide family first.  THE FILTER IS MACHINE
    FORM: a cell is in the family when its own TERM holds a node of z3's
    own division or remainder declaration kinds.  No mnemonic and no
    source token is read."""
    rows = json.load(open(twins_path))["rows"]
    cells = []
    for row in rows:
        cells.append({"mnem": row["mnem"], "shape": row["shape"],
                      "key_width": row["key_width"],
                      "places": [p["writes"] for p in row["places"]]})
        continue
    terms, _operands = RL.riscv_terms(MODEL)
    first = []
    rest = []
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        found = False
        for place in cell["places"]:
            term = terms.get((key, place))
            if term is None:
                continue
            for node in RGEN.leaves_first(term):
                if node.decl().kind() in RGEN.DIVIDING_KINDS:
                    found = True
                    break
                continue
            if found:
                break
            continue
        if found:
            first.append(cell)
            continue
        rest.append(cell)
        continue
    say("   the filter: a cell whose term holds a node of z3's own "
        "division or remainder kinds")
    say("   %d of %d cells are in that family; the sample takes the "
        "first %d cells of the family-first order"
        % (len(first), len(cells), HOW_MANY))
    picked = (first + rest)[:HOW_MANY]
    for cell in picked:
        say("     %s %s %d, places %s"
            % (cell["mnem"], cell["shape"], cell["key_width"],
               ",".join(cell["places"])))
        continue
    return picked


_render = RVG.RG.render


def render_and_save(ordered, target, families, home_family, bits, label,
                    word, policy, text):
    made = _render(ordered, target, families, home_family, bits, label,
                   word, policy, text)
    path = os.path.join(OUT, "%s.%s" % (label, EXT.get(target, target)))
    handle = open(path, "w")
    handle.write(made["source"])
    handle.close()
    return made


def main():
    RVG.ABORT_NAME = "ABORT_MEMORY_RD1"
    INH3.install()
    RVG.TARGETS = ["c", "cpp", "go", "rust"]
    RL.untwinned = dividing_first
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    RVG.RG.render = render_and_save
    say("[2/5] the sample: %d cells, the divide family first, on %s, "
        "both routes" % (HOW_MANY, ", ".join(RVG.TARGETS)))
    rc = RVG.run_command(OP, OP, EMU, TWINS, MODEL, G + "/rd1_sample",
                         OUT, "/work/rd1s", None)
    say("   the sample's exit: %d" % rc)

    say("[3/5] the go divide's rendered source, LITERAL")
    path = os.path.join(
        OUT, "div_gpr_gpr_gpr_64__reg_a0__go__native_first.go")
    if not os.path.exists(path):
        say("   FLAG: %s was not written; what the sample wrote:" % path)
        for name in sorted(os.listdir(OUT)):
            say("     %s" % name)
            continue
        return 1
    source = open(path).read()
    for line in source.splitlines():
        say("   %s" % line)
        continue

    say("[4/5] that source compiled for riscv64 at the ship flags, and "
        "its carved body, LITERAL")
    got, command, diagnostic = INH.compile_and_carve(source, "go",
                                                     "/work/rd1body")
    say("   the compile command: %s" % command)
    if got is None:
        say("   FLAG: the compile refused, LITERAL: %s"
            % (diagnostic or "")[:800])
        return 1
    raw, body = got
    say("   %d instructions" % len(body))
    for index, line in enumerate(body):
        say("   %2d  %s" % (index, line))
        continue
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF

timeout 1800 python3 /work/rd1/sample.py
echo "  the python exit: $?"

echo "[5/5] the sample's census"
timeout 120 python3 -c "
import json
d = json.load(open('$G/rd1_sample.json'))
print('   census:      %s' % d['census'])
print('   per target:  %s' % d['per_target'])
print('   seconds:     %s' % d['meta']['seconds'])
print('   peak kB:     %s' % d['meta']['peak_kb'])
"
echo "  exit: $?"
