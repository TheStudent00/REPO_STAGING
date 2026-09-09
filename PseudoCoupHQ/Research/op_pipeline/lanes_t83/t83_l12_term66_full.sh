#!/usr/bin/env bash
# t83 lane 12 -- THE FULL RESUME of term66 over canon40, under the
# address-space bound.
#
# THE MEMORY BOUND, stated before the full pass as the round requires:
#   * term66_run.py opens ONE canon40 shard, walks it, writes its own
#     store shard and drops it; nothing accumulates across shards but
#     the list of done names.  Its own 6 GB check runs after each
#     shard, with the named abort ABORT_MEMORY.
#   * that check is not enough on its own: it runs BETWEEN shards, and
#     the sample lane was SIGKILLed by the container's 8 GB cgroup
#     INSIDE a shard, in 11 seconds, at 8,391,436 kB.  So this lane
#     adds RLIMIT_AS at 4096 MB, set before the first shard, which the
#     process cannot step over.
#   * that the bound changes no answer is MEASURED, not assumed:
#     probe83g_ceiling.py gave the unit the sample died in five
#     ceilings (512/1024/2048/3072/5120 MB), the peak followed the
#     ceiling every time and the record was identical at all five; and
#     lanes 9, 10 and 11 re-transcribed three stored shards bounded
#     twice and unbounded once, and all three runs differ from the
#     store in exactly the same four go records -- so the difference
#     is the container against the host, not the bound.
#   * and if the bound ever DID fire, a MemoryError inside the row
#     loop would be caught there as a written hole; term66_bounded.py
#     scans every record it wrote for that and refuses its own output.
#
# SAMPLE FIRST, as the rule requires: the sample is lane 9's three
# shards, 241 records, peak 440,308 kB, 7 s.
set -u
cd PseudoCoupHQ/Research/op_pipeline

total=$(( $(ls canon40_regen_store/*.json | wc -l) + 6 ))
echo "total inputs to walk: $total"
python3 -c "
import json
print('done before this lane: %d' % len(json.load(open('term66_state.json'))['done']))
"
(
  while true; do
    n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))" 2>/dev/null || echo 0)
    echo "[$n/$total] inputs transcribed"
    sleep 60
  done
) &
poller=$!
start=$(date +%s)
python3 term66_bounded.py 4096 20000
rc=$?
kill "$poller" 2>/dev/null || true
end=$(date +%s)
echo
echo "term66_bounded.py exit $rc  (0 = every shard walked, 3 = budget spent and resumable, 1 = REFUSED)"
echo "wall time $(( end - start )) s"
n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "[$n/$total] inputs transcribed"
python3 -c "
import glob, json
t = 0
for path in sorted(glob.glob('term66_store/*.json')):
    t = t + len(json.load(open(path))['units'])
print('records in term66_store: %d' % t)
"
exit "$rc"
