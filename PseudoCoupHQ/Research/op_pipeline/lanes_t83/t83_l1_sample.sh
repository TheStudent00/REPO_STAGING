#!/usr/bin/env bash
# t83 lane 1 -- THE SAMPLE, as the round's memory rule requires.
#
# WHAT IT DOES, in order:
#   0. the path check (which side of the wall we are on);
#   1. the imports term66_run.py needs, each named, so a missing one
#      STOPS the task instead of being worked around;
#   2. the canon check -- canon40 is the newest canon on disk, printed
#      from the tree itself, not asserted;
#   3. a SHORT resume of term66_run.py (240 s budget) whose peak
#      resident size and wall time are pasted before the full pass.
#
# THE MEMORY BOUND, stated: term66_run.py opens ONE canon40 shard,
# walks it, writes its own store shard and drops it before the next.
# Nothing accumulates across shards except the `done` list of names.
# The cap is 6 GB resident, checked after every shard inside the
# process by `check_memory`, with the named abort ABORT_MEMORY.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

say() { echo; echo "======== $* ========"; }

say "0. which side of the wall"
echo "hostname: $(cat /etc/hostname 2>/dev/null)"
ls -d /home/*/Programming 2>&1 || echo "  host path ABSENT (as expected inside the container)"
for p in /projects/PseudoCoupHQ /work /out ; do
  printf '  %-28s ' "$p"; ls -d "$p" >/dev/null 2>&1 && echo present || echo ABSENT
done
python3 --version
nproc
free -g | head -2

say "1. the imports term66_run.py needs, each named"
python3 - <<'PY'
import importlib
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
wanted = ["z3", "canonical_form", "gate", "reference", "regate64_run",
          "term", "pool", "pool65_run", "ledger", "dom_ops",
          "normalize79_pool_prediction", "guard66"]
bad = []
for name in wanted:
    try:
        module = importlib.import_module(name)
        where = getattr(module, "__file__", "(builtin)")
        print("  OK      %-32s %s" % (name, where))
    except Exception as problem:
        bad.append(name)
        print("  MISSING %-32s %s: %s" % (name, type(problem).__name__, problem))
if bad:
    print("STOP: imports missing inside the sandbox: %s" % ",".join(bad))
    sys.exit(4)
PY
rc=$?
if [ "$rc" != "0" ]; then
  echo "STOP RULE HIT: an import is missing inside the sandbox"
  exit "$rc"
fi

say "2. the canon check -- is canon40 the newest canon on disk?"
ls | grep -o '^canon[0-9]\+' | sort -u -V | tail -5
echo "-- canon41 present?"
ls canon41* 2>&1 | head -3 || true
echo "-- the canon40 inputs term66_run.py walks:"
ls -la canon40_wrapped_*.json canon40_interp.json | cat
echo "-- regen shards: $(ls canon40_regen_store/*.json | wc -l)"

say "3. the resume state BEFORE the sample"
python3 -c "
import json
state = json.load(open('term66_state.json'))
print('  done inputs %d' % len(state['done']))
for one in state['done']:
    print('    %s' % one)
"
echo "-- store shards before: $(ls term66_store/*.json | wc -l)"

say "4. THE SAMPLE -- term66_run.py with a 240 s budget"
total=$(( $(ls canon40_regen_store/*.json | wc -l) + 6 ))
echo "total inputs to walk: $total"
(
  while true; do
    if [ ! -f term66_state.json ]; then sleep 10; continue; fi
    n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))" 2>/dev/null || echo 0)
    echo "[$n/$total] shards transcribed"
    sleep 20
  done
) &
poller=$!
start=$(date +%s)
/usr/bin/time -v python3 term66_run.py 240 2>&1 | tee /work/t83_sample.txt
rc=${PIPESTATUS[0]}
kill "$poller" 2>/dev/null || true
end=$(date +%s)
echo
echo "term66_run.py exit $rc (3 = budget spent, resumable)"
echo "sample wall time: $(( end - start )) s"
echo "-- PEAK RESIDENT of the sample, from /usr/bin/time -v:"
grep -i "Maximum resident set size" /work/t83_sample.txt || echo "  (time -v line not found)"

say "5. the resume state AFTER the sample"
python3 -c "
import json
state = json.load(open('term66_state.json'))
print('  done inputs %d' % len(state['done']))
"
echo "-- store shards after: $(ls term66_store/*.json | wc -l)"
n=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "[$n/$total] shards transcribed"
exit 0
