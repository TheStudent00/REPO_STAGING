#!/bin/bash
# bank1_l1_preflight_and_sample.sh -- task bank1, lane 1.
#
# WHAT THIS LANE DOES: reads what is on disk before anything is banked.
# The stores the bank will read and their line counts; the outer set;
# the compilers this instance answers with; then THE MEMORY SAMPLE the
# law asks for -- the first 20 runs of every store turned into
# certificates, nothing written, peak resident printed per store.
#
# MEMORY: bound 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_BANK1, checked after every store.  Nothing here
# forks a worker.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
TOTAL=6

echo "[1/$TOTAL] the two new files compile"
python3 -m py_compile "$A/bank.py" && echo "  bank.py compiles"
python3 -m py_compile "$A/autopoly.py" && echo "  autopoly.py compiles"
python3 -m py_compile "$A/autopoly1.py" && echo "  autopoly1.py compiles"
echo

echo "[2/$TOTAL] the stores on disk, line for line"
for f in autopoly_runs.jsonl autopoly2_runs.jsonl autopoly3_runs.jsonl \
         autopoly3_off_runs.jsonl autopoly4_runs.jsonl \
         expand1_runs.jsonl expand1_interp.jsonl autopoly5_runs.jsonl \
         expand2_runs.jsonl ; do
    printf '  %-34s %6s line(s)  %10s byte(s)\n' \
        "$f" "$(wc -l < "$A/$f")" "$(stat -c %s "$A/$f")"
done
echo

echo "[3/$TOTAL] the outer set"
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
doc = json.load(open(here + "/autopoly5_cells.json"))
print("  cells on autopoly5_cells.json: %d" % len(doc["asked"]))
total = 0
for record in doc["asked"]:
    total = total + record["attested_ledger_rows"]
print("  attested ledger rows over the outer set: %d" % total)
census = doc.get("setter_census") or {}
setters = set()
rows = 0
for consumer, held in census.items():
    for row in held:
        setters.add(row["mnem"])
        rows = rows + row.get("ledger_rows", 0)
print("  flag consumers the corpus records: %d" % len(census))
print("  setters the corpus records: %d" % len(setters))
print("  flag-pair ledger rows behind them: %d" % rows)
PY
echo

echo "[4/$TOTAL] task ap1's own driver still answers under its own name"
python3 "$A/autopoly.py" preflight | head -5
echo

echo "[5/$TOTAL] the compilers this instance answers with, LITERAL"
/usr/bin/clang --version 2>&1 | head -1
/usr/bin/clang++ --version 2>&1 | head -1
rustc --version 2>&1 | head -1
go version 2>&1 | head -1
/persist/swift/usr/bin/swiftc --version 2>&1 | head -1
echo

echo "[6/$TOTAL] THE MEMORY SAMPLE: the first 20 runs of every store"
python3 "$A/bank.py" sample 20
echo
echo "lane done"
