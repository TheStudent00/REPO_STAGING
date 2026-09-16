#!/bin/bash
# sl1 lane 28 -- rv6 again on the GENERATED lifter: every RISC-V cell,
# both routes, ship flags, c cpp go rust, ONE PROCESS, the driver
# rv6_all_langs.py itself (as rd1's lane 2 ran it); the store sl1_all so
# rd1_all stays beside it; then this round's table beside log_268's,
# "of 255" on every row, and every WALK_REFUSED row's cause.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/sl1gocache GOPATH=/work/sl1gopath SL1_WORK=/work/sl1lift
mkdir -p "$GOCACHE" "$GOPATH" /work/sl1b2 /work/sl1run /work/sl1lift
sha256sum $RV/riscv_reference.py
cat > /work/sl1run/run.py <<'PYEOF'
import os, sys
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
RV = "PseudoCoupHQ/Research/oracle/riscv"
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
OP = "PseudoCoupHQ/Research/op_pipeline"
sys.argv = ["rv6_all_langs.py", "run", OP, OP, EMU, RV + "/twins.json", RV + "/model_table_rv.json", G + "/sl1_all", G + "/src_sl1_all", "/work/sl1b2"]
sys.path.insert(0, G)
import rv6_all_langs
import rv_general
rv_general.ABORT_NAME = "ABORT_MEMORY_SL1"
print("the memory bound: %d kB, abort %s" % (rv_general.ABORT_KB, rv_general.ABORT_NAME), flush=True)
sys.exit(rv_general.main())
PYEOF
echo "[1/3] every cell, four languages, both routes, generated lifter: started $(date -u +%FT%TZ)"
timeout 12000 python3 /work/sl1run/run.py 2>&1 | grep -v "^   \[" | tail -40
echo "  exit: ${PIPESTATUS[0]}  finished $(date -u +%FT%TZ)"
echo "[2/3] this round's table beside log_268's rd1, population 255 on every row"
timeout 600 python3 - <<'PYEOF'
import json
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
NAME = {"c": "c", "cpp": "c++", "rust": "rust", "go": "go"}
def rows_of(path):
    return [json.loads(l) for l in open(path) if l.strip()]
def per_cell(rows):
    held = {}
    for row in rows:
        cell = row["cell"]; held[(cell["mnem"], cell["shape"], cell["key_width"], row["target"])] = row
    return held
def table(path, label):
    held = per_cell(rows_of(path)); counts = {}
    for key, row in held.items():
        counts.setdefault(key[3], {}); counts[key[3]][row["kind"]] = counts[key[3]].get(row["kind"], 0) + 1
    print(""); print(label); print("| language | proved | disproved | undecided | refused | of |"); print("|---|---|---|---|---|---|")
    for target in ("c", "cpp", "rust", "go"):
        got = counts.get(target) or {}
        print("| %s | %d | %d | %d | %d | 255 |" % (NAME[target], got.get("proved", 0), got.get("sat", 0), got.get("undecided", 0), got.get("refused", 0)))
    cells = {}
    for key, row in held.items():
        cells.setdefault(key[:3], set())
        if row["kind"] == "proved": cells[key[:3]].add(key[3])
    print("| proved on at least one of the four | %d | | | | 255 |" % sum(1 for v in cells.values() if v))
    print("| proved on all four | %d | | | | 255 |" % sum(1 for v in cells.values() if len(v) == 4))
    return held
before = table(G + "/rd1_all.jsonl", "log_268's rd1, the transcription:")
after = table(G + "/sl1_all.jsonl", "sl1, the generated lifter:")
print(""); print("every (cell, target) whose verdict MOVED, LITERAL"); print("| mnem | shape | width | language | rd1 | sl1 |"); print("|---|---|---|---|---|---|")
moved = 0
for key in sorted(set(before) | set(after)):
    was = before[key]["kind"] if key in before else "(not run)"; now = after[key]["kind"] if key in after else "(not run)"
    if was == now: continue
    moved += 1; print("| `%s` | `%s` | %s | %s | %s | %s |" % (key[0], key[1], key[2], NAME.get(key[3], key[3]), was, now))
print(""); print("%d (cell, target) verdicts moved" % moved)
print(""); print("every refused row of sl1 with its cause (WALK_REFUSED and the rest), LITERAL"); print("| mnem | shape | width | language | outcome | cause |"); print("|---|---|---|---|---|---|")
for key in sorted(after):
    row = after[key]
    if row["kind"] != "refused": continue
    v = row.get("verdict") or {}
    print("| `%s` | `%s` | %s | %s | %s | %s |" % (key[0], key[1], key[2], NAME.get(key[3], key[3]), v.get("outcome"), str(v.get("reason", ""))[:140].replace("|", "/")))
print(""); print("former WALK_REFUSED rows of rd1, their verdict now"); print("| mnem | shape | width | language | rd1 cause | sl1 |"); print("|---|---|---|---|---|---|")
for key in sorted(before):
    row = before[key]; v = row.get("verdict") or {}
    if v.get("outcome") != "WALK_REFUSED": continue
    print("| `%s` | `%s` | %s | %s | %s | %s |" % (key[0], key[1], key[2], NAME.get(key[3], key[3]), str(v.get("reason", ""))[:80], after[key]["kind"] if key in after else "(not run)"))
PYEOF
echo "[3/3] the spelling guard over the store"
python3 $OP/check_no_spelling_keys.py $G/sl1_all.json 2>&1 | tail -3; echo "  guard rc=$?"
echo "done $(date -u +%FT%TZ)"
