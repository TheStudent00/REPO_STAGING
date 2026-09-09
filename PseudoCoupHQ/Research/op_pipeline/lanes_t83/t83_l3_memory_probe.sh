#!/usr/bin/env bash
# t83 lane 3 -- WHERE the memory goes.  The sample lane was SIGKILLed
# by the container's 8 GB cgroup after 11 seconds without finishing a
# single further shard, so before anything is re-run the runaway is
# located: setup first, then unit by unit through the next shard the
# resume state owes, with a hard 5 GB address-space bound that names
# the unit that asks for more.
set -u
cd PseudoCoupHQ/Research/op_pipeline

echo "======== [1/2] the next shard the resume owes ========"
python3 -c "
import json
state = json.load(open('term66_state.json'))
print('done inputs %d' % len(state['done']))
"
echo "the next unwalked regen shard: canon40_regen_store/op_units2_c_c0004.json"

echo
echo "======== [2/2] the walk, unit by unit, bounded at 5 GB ========"
python3 probe83b_memory.py canon40_regen_store/op_units2_c_c0004.json 400
echo "probe exit $?"
exit 0
