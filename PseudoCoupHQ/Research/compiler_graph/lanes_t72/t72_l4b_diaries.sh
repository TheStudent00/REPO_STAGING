#!/usr/bin/env bash
# t72 lane 4 — compile EVERY go probe of the corpus (590 units) through
# the instrumented compiler, one ORDERED diary per probe.
#
# RESUMABLE: a unit whose diary already exists and is non-empty is
# skipped, and the state file records what has been done. Re-submitting
# this lane after any stop continues where it left off.
set -euo pipefail
REPO=PseudoCoupHQ/Research/compiler_graph
OUT="$REPO/diaries/go"
mkdir -p "$OUT" /work/probe /work/out
printf 'module probe\n\ngo 1.28\n' > /work/probe/go.mod

python3 - <<'PY'
import json, os, shlex, subprocess, sys, time

REPO = 'PseudoCoupHQ/Research/compiler_graph'
OUT = os.path.join(REPO, 'diaries', 'go')
STATE = os.path.join(REPO, 't72', 'diary_state.json')

parts = open('/persist/probecfg/toolline.parts').read().split('\n')
probes = json.load(open(os.path.join(REPO, 't72', 'probes_go.json')))['probes']
units = sorted(probes)
total = len(units)
print('probe corpus: %d go units' % total)

state = {'done': [], 'failed': {}, 'events': {}}
if os.path.exists(STATE):
    state = json.load(open(STATE))
done = set(state['done'])

started = time.time()
for index, unit in enumerate(units, 1):
    stem = unit.split('/', 1)[1]
    target = os.path.join(OUT, stem + '.txt')
    if unit in done and os.path.exists(target) and os.path.getsize(target) > 0:
        continue
    source = probes[unit]['source']
    open('/work/probe/probe.go', 'w').write(source)
    # The diary is written STRAIGHT to its final path. /work is a tmpfs
    # and the repo is a bind mount, so a rename between them is a
    # cross-device link and fails; and a copy of a 1.8 MB file 590 times
    # buys nothing. A partial file cannot survive: the hook appends under
    # a lock and the file is removed before the run and again if the run
    # does not exit 0.
    if os.path.exists(target):
        os.remove(target)
    env = dict(os.environ, COMPILER_DIARY=target)
    result = subprocess.run(parts, env=env, cwd='/work/probe',
                            capture_output=True, text=True)
    if result.returncode != 0:
        state['failed'][unit] = (result.stderr or result.stdout)[-600:]
        print('  FAILED %s exit %d' % (unit, result.returncode))
        if os.path.exists(target):
            os.remove(target)
    else:
        lines = 0
        with open(target) as handle:
            for lines, _ in enumerate(handle, 1):
                pass
        state['events'][unit] = lines
        done.add(unit)
        state['done'] = sorted(done)
    if index % 25 == 0 or index == total:
        json.dump(state, open(STATE, 'w'), indent=1)
        rate = index / max(time.time() - started, 0.001)
        print('[%d/%d] done=%d failed=%d  %.1f probes/s'
              % (index, total, len(done), len(state['failed']), rate))
        sys.stdout.flush()

json.dump(state, open(STATE, 'w'), indent=1)
print('FINAL done=%d failed=%d of %d' % (len(done), len(state['failed']), total))
if state['failed']:
    print('failed units:', sorted(state['failed'])[:20])
PY

echo "--- inventory ---"
echo "diary files : $(ls "$OUT" | wc -l)"
echo "total bytes : $(du -sb "$OUT" | cut -f1)"
du -sh "$OUT"
df -h PseudoCoupHQ | tail -1
echo "DONE t72_l4"
