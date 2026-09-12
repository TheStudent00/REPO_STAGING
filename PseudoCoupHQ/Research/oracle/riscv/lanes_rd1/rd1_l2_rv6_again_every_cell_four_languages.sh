#!/bin/bash
# rd1 lane 2 -- rv6 again, under the guarded render: every RISC-V cell, both
# routes, ship flags, c cpp go rust, ONE PROCESS and no pool. The driver is
# rv6_all_langs.py itself, imported so the run is its own, with this task's
# named memory abort set on it; the store is rd1_all so log_265's rv6_all
# stays where it is and the two can be read side by side.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rd1gocache GOPATH=/work/rd1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rd1b /work/rd1run

cat > /work/rd1run/run.py <<'PYEOF'
"""rv6 again: rv6_all_langs.py's own run, one process, with rd1's named
memory abort."""
import os
import sys

G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
RV = "PseudoCoupHQ/Research/oracle/riscv"
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
OP = "PseudoCoupHQ/Research/op_pipeline"

sys.argv = ["rv6_all_langs.py", "run", OP, OP, EMU,
            RV + "/twins.json", RV + "/model_table_rv.json",
            G + "/rd1_all", G + "/src_rd1_all", "/work/rd1b"]
sys.path.insert(0, G)
import rv6_all_langs                                            # noqa: F401
import rv_general

rv_general.ABORT_NAME = "ABORT_MEMORY_RD1"
print("the memory bound: %d kB, abort %s"
      % (rv_general.ABORT_KB, rv_general.ABORT_NAME), flush=True)
sys.exit(rv_general.main())
PYEOF

echo "[1/3] every cell, four languages, both routes: started $(date -u +%FT%TZ)"
timeout 9000 python3 /work/rd1run/run.py
echo "  exit: $?"
echo "  finished $(date -u +%FT%TZ)"

echo "[2/3] the count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rd1_all" "$RV/twins.json" \
  "$RV/certificates_riscv64_rv3.jsonl" "$RV/rv_loop.jsonl"
echo "  exit: $?"

echo "[3/3] this round's table beside log_265's rv6, population 255 on every row"
timeout 300 python3 - <<'PYEOF'
import json
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
NAME = {"c": "c", "cpp": "c++", "rust": "rust", "go": "go"}


def rows_of(path):
    out = []
    for line in open(path):
        text = line.strip()
        if not text:
            continue
        out.append(json.loads(text))
        continue
    return out


def per_cell(rows):
    """one verdict per (cell, target): the cell's own kind, which is the
    best of its two routes -- the driver's own choice."""
    held = {}
    for row in rows:
        cell = row["cell"]
        key = (cell["mnem"], cell["shape"], cell["key_width"],
               row["target"])
        held[key] = row["kind"]
        continue
    return held


def table(path, label):
    held = per_cell(rows_of(path))
    counts = {}
    for (mnem, shape, width, target), kind in held.items():
        counts.setdefault(target, {})
        counts[target][kind] = counts[target].get(kind, 0) + 1
        continue
    print("")
    print("%s" % label)
    print("| language | proved | disproved | undecided | refused | of |")
    print("|---|---|---|---|---|---|")
    for target in ("c", "cpp", "rust", "go"):
        got = counts.get(target) or {}
        print("| %s | %d | %d | %d | %d | 255 |"
              % (NAME[target], got.get("proved", 0), got.get("sat", 0),
                 got.get("undecided", 0), got.get("refused", 0)))
        continue
    cells = {}
    for (mnem, shape, width, target), kind in held.items():
        key = (mnem, shape, width)
        cells.setdefault(key, set())
        if kind == "proved":
            cells[key].add(target)
        continue
    any_one = 0
    all_four = 0
    for key in cells:
        if cells[key]:
            any_one = any_one + 1
        if len(cells[key]) == 4:
            all_four = all_four + 1
        continue
    print("| proved on at least one of the four | %d | | | | 255 |"
          % any_one)
    print("| proved on all four | %d | | | | 255 |" % all_four)
    return held


before = table(G + "/rv6_all.jsonl", "log_265's rv6, the eager render:")
after = table(G + "/rd1_all.jsonl", "rd1, the guarded render:")

print("")
print("the disproved column, before -> after")
print("| language | disproved, rv6 | disproved, rd1 | of |")
print("|---|---|---|---|")
for target in ("c", "cpp", "rust", "go"):
    was = 0
    now = 0
    for key in before:
        if key[3] == target and before[key] == "sat":
            was = was + 1
        continue
    for key in after:
        if key[3] == target and after[key] == "sat":
            now = now + 1
        continue
    print("| %s | %d | %d | 255 |" % (NAME[target], was, now))
    continue

print("")
print("every (cell, target) whose verdict MOVED, LITERAL")
print("| mnem | shape | width | language | rv6 | rd1 |")
print("|---|---|---|---|---|---|")
moved = 0
for key in sorted(set(before) | set(after)):
    was = before.get(key, "(not run)")
    now = after.get(key, "(not run)")
    if was == now:
        continue
    moved = moved + 1
    print("| `%s` | `%s` | %s | %s | %s | %s |"
          % (key[0], key[1], key[2], NAME.get(key[3], key[3]), was, now))
    continue
print("")
print("%d (cell, target) verdicts moved" % moved)
PYEOF
echo "  exit: $?"
