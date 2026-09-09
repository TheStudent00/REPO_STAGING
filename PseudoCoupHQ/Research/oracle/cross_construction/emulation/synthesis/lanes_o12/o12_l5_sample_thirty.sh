#!/usr/bin/env bash
# o12 lane 5 -- the plan rebuilt with the holder-table decision
# recorded on it, the literal evidence for that decision, the sample of
# thirty targets across three machine type keys, and the guard over
# both json files this lane writes.
set -u
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
echo "======== 1. the plan ========"
echo "[1/4] census"
python3 synthesize.py census
echo "-- exit $?"
echo
echo "======== 2. the evidence for the holder decision ========"
echo "[2/4] the result holders and slot holders of one bucket"
python3 - <<'PY'
import json
plan = json.load(open("synthesis_plan.json"))
for target in plan["targets"]:
    if target["type_key"] != "rdi,rsi|8":
        continue
    print("bucket             ", target["type_key"])
    print("answer width       ", target["answer_width"])
    print("target slot holder ", target["slot_holder"])
    print("target result      ", target["result_holder"])
    results = {}
    slots = {}
    for component in target["library"]:
        holder = component["result_holder"]
        results[holder] = results.get(holder, 0) + 1
        slot = ",".join(component["parameter_holders"])
        slots[slot] = slots.get(slot, 0) + 1
    print("component result holders, with a count:")
    for holder in sorted(results):
        print("   %-28s %3d" % (holder, results[holder]))
    print("component parameter holders, with a count:")
    for slot in sorted(slots):
        print("   %-28s %3d" % (slot, slots[slot]))
    break
PY
echo
echo "======== 3. the sample ========"
echo "[3/4] sample of thirty"
python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "sample", "30"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "======== 4. the guard ========"
echo "[4/4] guard"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  synthesis_plan.json synthesis_sample.json
echo "-- guard exit $?"
