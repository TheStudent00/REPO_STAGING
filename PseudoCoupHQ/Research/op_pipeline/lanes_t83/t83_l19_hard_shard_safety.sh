#!/usr/bin/env bash
# t83 lane 19 -- WAS 4096 MB ITSELF SAFE ON THE HARD SHARD?
#
# Lane 18 is the correction to lane 8's conclusion.  On an ordinary
# shard the ceiling changed nothing (99 of 99 identical at 4096, 1024
# and 512 MB).  On the HARD shard op_units2_c_c0004 it changes a great
# deal: 12 of 24 records differ at 512 MB, 12 at 1024, 9 at 2048 -- and
# the low ceilings are fast precisely BECAUSE they stop the work early.
# The walk's peak under 4096 MB was 3,887,352 kB, pinned against its
# own ceiling, so 4096 is not obviously on the safe side of that line.
#
# THE TEST, in three parts:
#   1 WHY the records differ at 512 MB -- printed, not guessed;
#   2 whether the STORE as it stands carries any record whose written
#     reason names a memory failure;
#   3 whether 6144 MB -- above the 3,887,352 kB peak and below the
#     instance's 8 GB cap -- reproduces the shard 4096 MB wrote.  If it
#     does, the answer had converged by 4096 and the shard stands.  If
#     it does not, the shard must come out of the store.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "======== [1/3] WHY the records differ at 512 MB ========"
rm -rf /work/t83_check_store /work/t83_check_state.json
python3 term66_bounded.py 512 100000 --check \
  canon40_regen_store/op_units2_c_c0004.json > /work/t83_512.txt 2>&1
tail -6 /work/t83_512.txt
python3 - <<'PY'
import json
fresh = json.load(open("/work/t83_check_store/"
                      "canon40_regen_store__op_units2_c_c0004.json"))
stored = json.load(open("term66_store/"
                        "canon40_regen_store__op_units2_c_c0004.json"))
shown = 0
for name in sorted(stored["units"]):
    a = fresh["units"].get(name)
    b = stored["units"][name]
    if a == b:
        continue
    print("=== %s" % name)
    print("   stored term_state %s proved %s holes %d"
          % (b.get("term_state"), b.get("proved"),
             len(b.get("holes") or [])))
    print("   fresh  term_state %s proved %s holes %d"
          % (a.get("term_state"), a.get("proved"),
             len(a.get("holes") or [])))
    for hole in (a.get("holes") or [])[:2]:
        print("   fresh hole: %s" % json.dumps(hole)[:260])
    if a.get("why_no_term"):
        print("   fresh why_no_term: %s" % a["why_no_term"][:260])
    shown = shown + 1
    if shown >= 3:
        break
PY

echo
echo "======== [2/3] does the STORE carry a memory failure as a written reason? ========"
python3 - <<'PY'
import glob, json
records = 0
tainted = []
for path in sorted(glob.glob("term66_store/*.json")):
    document = json.load(open(path))
    for name in sorted(document.get("units", {})):
        record = document["units"][name]
        records = records + 1
        if "MemoryError" in json.dumps(record):
            tainted.append((document.get("shard"), name))
print("records in term66_store: %d" % records)
print("records naming MemoryError: %d" % len(tainted))
for one in tainted[:10]:
    print("   %s %s" % one)
PY

echo
echo "======== [3/3] 6144 MB against the shard 4096 MB wrote ========"
rm -rf /work/t83_check_store /work/t83_check_state.json
start=$(date +%s)
python3 term66_bounded.py 6144 100000 --check \
  canon40_regen_store/op_units2_c_c0004.json
rc=$?
end=$(date +%s)
echo "ceiling 6144 MB: wall $(( end - start )) s, check exit $rc"
echo "[3/3] done"
exit 0
