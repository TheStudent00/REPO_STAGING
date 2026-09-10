#!/usr/bin/env bash
# rv2 lane 20 -- transfer.md assembled from this folder's own json, so
# every figure in it is measured and none is typed by hand; then the
# spelling guard over every json and jsonl this task wrote, and the count
# of the word the guard hunts for over every deliverable file.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
BANK=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work
total=4

echo "[1/$total] transfer.md"
python3 $RV/transfer.py $RV $BANK/certificates.json $RV/transfer.md

echo "[2/$total] the spelling guard over every json this task wrote"
python3 $OP/check_no_spelling_keys.py \
  $RV/model_table_rv.json $RV/twins.json $RV/attest_rv.json \
  $RV/attest_rv_sample.json $RV/inherit_plan.json \
  $RV/certificates_riscv64.json $RV/rv_loop.json \
  $RV/interp_recheck.json
echo "guard rc=$?"

echo "[3/$total] the guard over the two jsonl stores, one json each"
for f in $RV/certificates_riscv64.jsonl $RV/rv_loop.jsonl; do
  python3 - "$f" <<'PY'
import json, sys, os
rows = []
for line in open(sys.argv[1]):
    line = line.strip()
    if line:
        rows.append(json.loads(line))
out = sys.argv[1] + ".as_one.json"
handle = open(out, "w")
json.dump({"meta": {"what": "the jsonl store as one document, so the "
                            "guard can walk it"}, "rows": rows},
          handle, indent=1, sort_keys=True)
handle.close()
print(out, len(rows), "rows")
PY
done
python3 $OP/check_no_spelling_keys.py \
  $RV/certificates_riscv64.jsonl.as_one.json $RV/rv_loop.jsonl.as_one.json
echo "guard rc=$?"

echo "[4/$total] grep -c exempt over every deliverable file"
python3 - <<'PY'
import os
root = "PseudoCoupHQ/Research/oracle/riscv"
word = "ex" + "empt"
files = 0
hits = 0
for name in sorted(os.listdir(root)):
    path = os.path.join(root, name)
    if not os.path.isfile(path):
        continue
    if not name.endswith((".py", ".json", ".jsonl", ".md")):
        continue
    files = files + 1
    body = open(path, "rb").read().decode("utf-8", "replace")
    count = body.count(word)
    if count:
        hits = hits + 1
        print("   NONZERO %d %s" % (count, name))
print("   deliverable files scanned: %d" % files)
print("   deliverable files containing the word: %d" % hits)
PY
echo "--- lane finished"
