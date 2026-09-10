#!/bin/bash
# t2_l27_the_store_where_the_guard_can_read_it.sh -- task t2, lane 27:
# this pass's store moved to where every pass's store lives, the bank
# rebuilt from it, the three readings, the guards and the report.
#
# WHY IT MOVES.  Lane 26's guard REFUSED the bank: 5,303 certificates
# carried `..` on `produced_by.store`, because the store sat under
# `construct/` and `bank.store_path` writes that field relative to the
# autopoly folder -- and `..` is an operator token (a range in swift and
# in ruby).  The store is not re-run and not re-derived; the same lines
# move to `autopoly/t2_construct_runs.jsonl`, where the field the bank
# writes carries no such token.  The CODE stays under `construct/`.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
G=PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
W=exem
total=6

i=1
echo "[$i/$total] the store and its sources, moved to the autopoly folder"
if [ -f "$C/t2_construct_runs.jsonl" ]; then
    mv "$C/t2_construct_runs.jsonl" "$A/t2_construct_runs.jsonl"
    echo "  store moved: $(wc -l < "$A/t2_construct_runs.jsonl") line(s)"
fi
if [ -d "$C/src_t2_construct" ]; then
    mkdir -p "$A/src_t2_construct"
    mv "$C/src_t2_construct"/* "$A/src_t2_construct/" 2>/dev/null || true
    echo "  sources moved: $(ls "$A/src_t2_construct" | wc -l) file(s)"
fi
echo

i=2
echo "[$i/$total] THE BANK, rebuilt with this pass in it"
python3 "$C/construct.py" bank | tail -8
echo

i=3
echo "[$i/$total] THE THREE READINGS, with this pass registered"
python3 "$C/construct.py" readings
echo

i=4
echo "[$i/$total] THE SPELLING GUARD over the json this task wrote"
python3 "$G" "$C/construct.json" "$C/lean/lemmas_t2.json" \
    "$A/certificates.json"
echo "  guard exit: $?"
echo

i=5
echo "[$i/$total] THE SPELLING GUARD over the two jsonl stores"
mkdir -p /tmp/t2_guard
python3 - <<'PY'
import json, os
pairs = [
    ("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t2_construct_runs.jsonl",
     "/tmp/t2_guard/t2_construct_runs.json"),
    ("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl",
     "/tmp/t2_guard/certificates.json"),
]
for source, target in pairs:
    rows = []
    handle = open(source)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        rows.append(json.loads(text))
        continue
    handle.close()
    out = open(target, "w")
    json.dump({"records": rows}, out)
    out.close()
    print("  %s -> %s (%d record(s))"
          % (os.path.basename(source), target, len(rows)))
    continue
PY
python3 "$G" /tmp/t2_guard/t2_construct_runs.json
echo "  guard exit: $?"
python3 "$G" /tmp/t2_guard/certificates.json
echo "  guard exit: $?"
echo

i=6
echo "[$i/$total] THE LAW'S OWN COUNT over the files this task added, and construct.md"
grep -rc "${W}pt" "$C"/*.py "$C"/lean/*.py "$C"/lanes_t2/*.sh | sort -t: -k2 -rn | head -3
echo "  the maximum above must be 0"
python3 "$C/construct_report.py"
sed -n '1,60p' "$C/construct.md"
echo
echo "lane done"
