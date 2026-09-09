#!/usr/bin/env bash
# t97 lane 1 -- the ground under the walk, then the SAMPLE the memory
# rule asks for.  Nothing is written into term66_store by this lane.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "======== 1. the imports the walk needs, each named ========"
python3 - <<'PY'
import importlib, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
for name in ["z3", "canonical_form", "gate", "reference", "regate64_run",
             "term", "pool", "pool65_run", "pool66_run", "ledger",
             "dom_ops", "normalize79_pool_prediction", "guard66",
             "term66_run", "name_census7", "audit66"]:
    try:
        module = importlib.import_module(name)
        print("  OK      %-32s %s" % (name, getattr(module, "__file__", "?")))
    except Exception as problem:
        print("  MISSING %-32s %s: %s" % (name, type(problem).__name__, problem))
PY

echo
echo "======== 2. the canon check -- is canon40 still the newest? ========"
ls -d canon3[6-9] canon4* 2>/dev/null | sed 's/_.*//' | sort -u
echo "-- canon41 present?"
ls canon41* 2>&1 | head -2
echo "-- the canon40 inputs the walk reads:"
ls -l canon40_interp.json canon40_wrapped_*.json
echo "-- regen shards: $(ls canon40_regen_store/*.json | wc -l)"

echo
echo "======== 3. THE CORRECTED REFERENCE, quoted from the artifact ========"
echo "-- reference.py on disk:"
ls -l --time-style=long-iso reference.py
echo "-- md5:"
md5sum reference.py
echo "-- SRem / URem, the remainder whose sign follows the dividend:"
grep -n "z3.SRem\|z3.URem" reference.py | head -12
echo "-- the machine stack and the x87 stack on MachineState:"
python3 - <<'PY'
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
import reference as R
state = R.MachineState()
print("   MachineState().stack =", state.stack)
print("   MachineState().x87   =", state.x87)
names = sorted(n for n in dir(state) if "stack" in n or "x87" in n or n in ("pop_value", "push_value"))
print("   the stack and x87 methods:", names)
PY

echo
echo "======== 4. the resume state BEFORE the sample ========"
python3 - <<'PY'
import json, glob, os
os.chdir("/projects/PseudoCoupHQ/Research/op_pipeline")
state = json.load(open("term66_state.json"))
print("  done inputs %d" % len(state["done"]))
for key in state["done"]:
    print("    %s" % key)
shards = sorted(glob.glob("term66_store/*.json"))
records = 0
for path in shards:
    records += len(json.load(open(path))["units"])
print("-- store shards: %d, records: %d" % (len(shards), records))
PY

echo
echo "======== 5. THE SAMPLE -- one hard shard and one easy shard, ========"
echo "========    one forked sub-process per unit                ========"
python3 probe97a_unit_cost.py 1536 120 \
  canon40_regen_store/op_units2_c_c0004.json \
  canon40_regen_store/op_units2_c_c0005.json
echo "probe exit $?"
