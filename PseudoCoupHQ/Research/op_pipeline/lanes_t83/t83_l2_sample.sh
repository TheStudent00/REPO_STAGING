#!/usr/bin/env bash
# t83 lane 2 -- THE SAMPLE, re-run.  Lane 1 proved the imports and the
# canon; it could not print the peak because /usr/bin/time is not in
# the image (this is a MISSING MEASURING TOOL, not a missing analysis
# import, so the run continues and the peak is read from the kernel by
# python's own resource.getrusage over the CHILD process instead).
#
# THE MEMORY BOUND, stated: term66_run.py opens ONE canon40 shard,
# walks it, writes its own store shard, and drops it before the next.
# Nothing accumulates across shards except the list of done names.
# The cap is 6 GB resident, checked after every shard INSIDE the
# process by `check_memory`, with the named abort ABORT_MEMORY.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "======== THE SAMPLE -- term66_run.py with a 240 s budget ========"
total=$(( $(ls canon40_regen_store/*.json | wc -l) + 6 ))
echo "total inputs to walk: $total"
(
  while true; do
    n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))" 2>/dev/null || echo 0)
    echo "[$n/$total] shards transcribed"
    sleep 30
  done
) &
poller=$!
python3 - 240 <<'PY'
import resource
import subprocess
import sys
import time
budget = sys.argv[1]
start = time.time()
proc = subprocess.run([sys.executable, "term66_run.py", budget])
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
print("")
print("term66_run.py exit %d (3 = budget spent, resumable)" % proc.returncode)
print("SAMPLE PEAK RESIDENT (child, ru_maxrss) %d kB" % peak)
print("SAMPLE WALL TIME %.0f s" % (time.time() - start))
PY
kill "$poller" 2>/dev/null || true

echo
echo "======== the resume state AFTER the sample ========"
n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "done inputs $n"
echo "store shards: $(ls term66_store/*.json | wc -l)"
python3 -c "
import glob, json
t = 0
for path in sorted(glob.glob('term66_store/*.json')):
    t = t + len(json.load(open(path))['units'])
print('records transcribed so far %d' % t)
"
echo "[$n/$total] shards transcribed"
exit 0
