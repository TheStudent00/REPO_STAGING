#!/usr/bin/env bash
# t83 lane 20 -- ROLL BACK THIS SESSION'S OWN TAINTED SHARDS.
#
# WHY.  The six shards this session wrote (op_units2_c_c0004 ..
# c0009) were written under a 4096 MB address-space ceiling that FIRED:
# two of their records carry `MemoryError` as a written reason
# (c/regen_1859 and c/regen_2079), and re-transcribing c0004 at
# 6144 MB -- the largest ceiling the instance's 8 GB cap allows --
# still disagrees with them on two further records.  Records produced
# by a bound that fired must not sit in the store where a later resume
# would take them as done.
#
# WHAT IS DONE, and what is NOT.
#   * The six shards are COPIED, byte for byte, into
#     term66_store_bound_fired_records/ so the defective artifacts stay
#     as records, unedited, exactly as the rules require.
#   * They are then removed from term66_store and their keys removed
#     from term66_state.json, restoring the resume state EXACTLY as
#     task 83 received it: the ten inputs of the 2026-09-03 part-run.
#   * The ten host-written shards are NOT touched.
#   * Nothing else in the tree is touched.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

KEEP='canon40_wrapped_c.json canon40_wrapped_cpp.json canon40_wrapped_go.json canon40_wrapped_rust.json canon40_wrapped_swift.json canon40_interp.json canon40_regen_store/op_units2_c_c0000.json canon40_regen_store/op_units2_c_c0001.json canon40_regen_store/op_units2_c_c0002.json canon40_regen_store/op_units2_c_c0003.json'

echo "======== [1/4] the store as it stands ========"
python3 -c "
import glob, json
total = 0
for path in sorted(glob.glob('term66_store/*.json')):
    document = json.load(open(path))
    total = total + len(document['units'])
print('shards %d, records %d' % (len(glob.glob('term66_store/*.json')), total))
"
python3 -c "
import json
print('state done: %d' % len(json.load(open('term66_state.json'))['done']))
"

echo
echo "======== [2/4] the shards written under the fired bound, preserved ========"
mkdir -p term66_store_bound_fired_records
python3 - <<PY
import json
import os
import shutil
keep = set("""$KEEP""".split())
state = json.load(open("term66_state.json"))
moved = []
for key in sorted(state["done"]):
    if key in keep:
        continue
    moved.append(key)
records = 0
for key in moved:
    name = key.replace("/", "__")
    source = os.path.join("term66_store", name)
    if not os.path.exists(source):
        print("   (already absent) %s" % key)
        continue
    document = json.load(open(source))
    records = records + len(document["units"])
    shutil.copy2(source, os.path.join(
        "term66_store_bound_fired_records", name))
    print("   preserved %s (%d records)" % (key, len(document["units"])))
handle = open("term66_store_bound_fired_records/README_why.json", "w")
json.dump({
    "produced_by": "t83_l20_rollback.sh, task 83, 2026-09-04",
    "what_these_are": "the shards task 83 wrote under a 4096 MB "
                      "RLIMIT_AS that FIRED, kept unedited as the "
                      "defective record",
    "why_they_are_not_in_the_store": "two of their records carry "
                                     "MemoryError as a written reason "
                                     "(c/regen_1859, c/regen_2079), "
                                     "and re-transcribing "
                                     "op_units2_c_c0004 at 6144 MB -- "
                                     "the largest ceiling this "
                                     "instance's 8 GB cap allows -- "
                                     "disagrees with them on two "
                                     "further records "
                                     "(c/regen_1887, c/regen_1890). A "
                                     "record produced by a bound that "
                                     "fired is not a record of the "
                                     "compiler.",
    "shards": moved,
    "records": records,
    "evidence": "DevComms/log_189_task83_term_pool_canon40.md section 3",
}, handle, indent=1, sort_keys=True)
handle.write("\n")
handle.close()
print("   %d shards, %d records preserved" % (len(moved), records))
handle = open("/work/t83_moved.txt", "w")
handle.write("\n".join(moved) + "\n")
handle.close()
PY

echo
echo "======== [3/4] removed from the store and from the resume state ========"
python3 - <<'PY'
import json
import os
moved = [one.strip() for one in open("/work/t83_moved.txt")
         if one.strip()]
for key in moved:
    path = os.path.join("term66_store", key.replace("/", "__"))
    if os.path.exists(path):
        os.remove(path)
        print("   removed from the store %s" % key)
state = json.load(open("term66_state.json"))
state["done"] = sorted(set(state["done"]) - set(moved))
handle = open("term66_state.json", "w")
json.dump(state, handle, indent=1, sort_keys=True)
handle.close()
print("   state done is now %d" % len(state["done"]))
PY

echo
echo "======== [4/4] the store restored to the handoff state ========"
python3 -c "
import glob, json
total = 0
for path in sorted(glob.glob('term66_store/*.json')):
    document = json.load(open(path))
    total = total + len(document['units'])
print('shards %d, records %d' % (len(glob.glob('term66_store/*.json')), total))
tainted = 0
for path in sorted(glob.glob('term66_store/*.json')):
    document = json.load(open(path))
    for name in document['units']:
        if 'MemoryError' in json.dumps(document['units'][name]):
            tainted = tainted + 1
print('records naming MemoryError: %d' % tainted)
"
cat term66_state.json
echo "[1/1] rollback done"
exit 0
