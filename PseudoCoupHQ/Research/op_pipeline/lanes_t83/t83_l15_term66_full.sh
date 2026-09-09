#!/usr/bin/env bash
# t83 lane 15 -- the full resume of term66 over canon40, leg of three.
#
# WHY THREE LEGS.  The instance's script_timeout is 21600 s and the
# measured rate is about 0.83 s per runtime-callee row (lane 3: 288
# rows in 240 s), against 49,362 such rows over the 30,324 units
# canon40 proves -- roughly eleven hours.  So each leg takes an 18000 s
# budget, stops cleanly when it is spent, and the next leg resumes from
# term66_state.json.  A leg that finds every input already walked exits
# at once.
#
# THE MEMORY BOUND, stated before the full pass as the round requires:
#   * term66_run.py opens ONE canon40 shard, walks it, writes its own
#     store shard and drops it; nothing accumulates across shards but
#     the list of done names.  Its own 6 GB getrusage check runs after
#     each shard with the named abort ABORT_MEMORY.
#   * that check runs BETWEEN shards and the excursion is INSIDE one,
#     so RLIMIT_AS is set to 4096 MB before the first shard, which the
#     process cannot step over.  4096 MB is half the instance's 8 GB.
#   * THE BOUND CHANGES NO RECORD, measured three ways: five ceilings
#     over one unit, identical record at all five (probe83g); three
#     stored shards re-transcribed bounded twice and unbounded once,
#     the same four go records differing every time, so the difference
#     is the machine and not the bound (lanes 9, 10, 11); and the same
#     shard re-transcribed at 4096 and 1024 MB, 99 of 99 records
#     identical to the store both times (lane 14).
#   * and if the bound ever DID fire, term66_bounded.py scans every
#     record it wrote for a memory failure that became a written
#     reason and refuses its own output.
#
# SAMPLE FIRST, as the rule requires: lane 14, 99 records, 111 s at
# this ceiling, peak well under it, zero records changed.
set -u
cd PseudoCoupHQ/Research/op_pipeline

total=$(( $(ls canon40_regen_store/*.json | wc -l) + 6 ))
done_now=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "[$done_now/$total] inputs transcribed before this leg"
if [ "$done_now" -ge "$total" ]; then
  echo "every input is already walked; this leg has nothing to do"
  exit 0
fi
(
  while true; do
    n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))" 2>/dev/null || echo 0)
    echo "[$n/$total] inputs transcribed"
    sleep 120
  done
) &
poller=$!
start=$(date +%s)
python3 term66_bounded.py 4096 18000
rc=$?
kill "$poller" 2>/dev/null || true
end=$(date +%s)
echo
echo "term66_bounded.py exit $rc  (0 = every input walked, 3 = budget spent and resumable, 1 = REFUSED OWN OUTPUT)"
echo "leg wall time $(( end - start )) s"
n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "[$n/$total] inputs transcribed"
python3 -c "
import glob, json
t = 0
for path in sorted(glob.glob('term66_store/*.json')):
    t = t + len(json.load(open(path))['units'])
print('records in term66_store: %d' % t)
"
exit 0
