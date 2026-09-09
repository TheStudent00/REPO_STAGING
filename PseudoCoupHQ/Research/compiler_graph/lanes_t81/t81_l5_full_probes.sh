#!/usr/bin/env bash
# t81 lane 5 — compile EVERY c and cpp probe of the ORIGINAL corpus
# through the instrumented clang, one ORDERED diary per probe.
#
# THE POPULATION, recounted from the canon rather than inherited:
# canon39_wrapped_c.json holds 610 units and canon39_wrapped_cpp.json
# holds 770, so 1,380 probes. t81/probes_cpp.json carries exactly those
# 1,380 sources, keyed `c/op_N` and `cpp/op_N`.
#
# RESUMABLE, exactly as task 72's go lane is: a unit whose diary already
# exists and is non-empty is skipped, and the state file records what has
# been done. Re-submitting after any stop continues where it left off.
#
# THE PID SUFFIX. clang's driver forks a `-cc1` process, so the hook
# writes `<COMPILER_DIARY>.<pid>`; the driver process never enters the
# region and so never opens a file. Each compile's pid files are merged
# in pid order into the final diary and the count is recorded, so a
# compile that produced more than one is visible rather than silently
# concatenated.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
mkdir -p "$REPO/diaries/c" "$REPO/diaries/cpp" /work/probe

say "the binary under test"
/persist/llvmbuild/bin/clang --version 2>&1 | head -2

say "the two inputs REPRODUCED inside the sandbox"
# WHY THIS STEP EXISTS, stated rather than hidden: t81/probes_cpp.json
# and t81/diary_targets_cpp.json were first written by a HOST run of
# t81/diary_inputs_build.py on 2026-09-03, before the owner's 2026-09-04
# ruling that every computation is an Airlock lane. They are not
# discarded and not trusted: the program is re-run HERE, and the two
# files it writes are compared byte for byte with the two on disk. A
# difference would mean the tracked inputs are not what the sandbox
# produces, which is a finding, not a detail.
rm -rf /work/repro && mkdir -p /work/repro/t81
ln -sfn PseudoCoupHQ/Research/op_pipeline /work/op_pipeline
for F in graph_cpp_defs.json graph_cpp_files.json ; do
  ln -sfn "$REPO/$F" "/work/repro/$F"
done
cp "$REPO/t81/diary_inputs_build.py" /work/repro/t81/
python3 /work/repro/t81/diary_inputs_build.py 2>&1 | tail -14
for F in probes_cpp.json diary_targets_cpp.json ; do
  if diff -q "/work/repro/t81/$F" "$REPO/t81/$F" >/dev/null 2>&1; then
    echo "   $F : IDENTICAL to the tracked file"
  else
    echo "   $F : DIFFERS from the tracked file -- this is a finding"
    diff "/work/repro/t81/$F" "$REPO/t81/$F" | head -20
  fi
done

say "the population, RECOUNTED from the canon itself"
# The brief says 610 + 770 = 1,380. This recounts it from
# canon39_wrapped_c.json and canon39_wrapped_cpp.json rather than
# accepting the figure, and checks that probes_cpp.json carries exactly
# those unit ids and no others.
python3 - <<'PY'
import json, os
PIPELINE = 'PseudoCoupHQ/Research/op_pipeline'
REPO = 'PseudoCoupHQ/Research/compiler_graph'
canon = {}
for language in ('c', 'cpp'):
    payload = json.load(open(os.path.join(
        PIPELINE, 'canon39_wrapped_%s.json' % language)))
    canon[language] = set(payload['units'])
    print('   canon39_wrapped_%s.json : %d units, tally %s'
          % (language, len(payload['units']), json.dumps(payload['tally'])))
print('   RECOUNTED TOTAL : %d + %d = %d'
      % (len(canon['c']), len(canon['cpp']),
         len(canon['c']) + len(canon['cpp'])))
probes = json.load(open(os.path.join(REPO, 't81',
                                     'probes_cpp.json')))['probes']
print('   probes_cpp.json  : %d probes' % len(probes))
both = canon['c'] | canon['cpp']
print('   in the canon but not a probe : %d' % len(both - set(probes)))
print('   a probe but not in the canon : %d' % len(set(probes) - both))
# WHERE THE PROBE SOURCE COMES FROM. The diary is only about the corpus
# if the text compiled here is the text the corpus's unit was compiled
# from. The canon's own unit record is inspected for a source field and
# compared where it carries one.
sample = json.load(open(os.path.join(PIPELINE, 'canon39_wrapped_c.json')))
one = sample['units']['c/op_0']
print('   canon39 unit record fields : %s' % sorted(one))
for field in ('source', 'probe_source', 'src'):
    if field in one:
        same = 0
        for unit in sorted(canon['c']):
            if sample['units'][unit].get(field) == probes[unit]['source']:
                same = same + 1
        print('   c probe sources identical to canon39 `%s` : %d of %d'
              % (field, same, len(canon['c'])))
        break
else:
    print('   the canon unit record carries no source field; the probe '
          'sources come from t81/diary_inputs_build.py, whose own '
          'provenance is in t81/probes_cpp.json meta')
print('   probes_cpp.json meta : %s'
      % json.dumps(json.load(open(os.path.join(
          REPO, 't81', 'probes_cpp.json')))['meta'])[:900])
PY

python3 - <<'PY'
import glob, json, os, resource, subprocess, sys, time

REPO = 'PseudoCoupHQ/Research/compiler_graph'
STATE = os.path.join(REPO, 't81', 'diary_state_cpp.json')
CLANG = '/persist/llvmbuild/bin/clang'
CLANGXX = '/persist/llvmbuild/bin/clang++'

probes = json.load(open(os.path.join(REPO, 't81', 'probes_cpp.json')))['probes']
units = sorted(probes)
total = len(units)
print('probe corpus: %d units (c and cpp of the original corpus)' % total)

state = {'done': [], 'failed': {}, 'events': {}, 'pid_files': {}}
if os.path.exists(STATE):
    state = json.load(open(STATE))
    state.setdefault('pid_files', {})
done = set(state['done'])

started = time.time()
for index, unit in enumerate(units, 1):
    language, stem = unit.split('/', 1)
    target = os.path.join(REPO, 'diaries', language, stem + '.txt')
    if unit in done and os.path.exists(target) and os.path.getsize(target) > 0:
        continue
    suffix = 'c' if language == 'c' else 'cpp'
    source_path = '/work/probe/unit.%s' % suffix
    open(source_path, 'w').write(probes[unit]['source'])
    for stale in glob.glob(target + '.*'):
        os.remove(stale)
    if os.path.exists(target):
        os.remove(target)
    tool = CLANG if language == 'c' else CLANGXX
    standard = '-std=c17' if language == 'c' else '-std=c++20'
    command = [tool, standard, '-O1', '-c', source_path,
               '-o', '/work/probe/unit_ship.o']
    result = subprocess.run(command,
                            env=dict(os.environ, COMPILER_DIARY=target),
                            capture_output=True, text=True)
    pid_files = sorted(glob.glob(target + '.*'),
                       key=lambda name: int(name.rsplit('.', 1)[1]))
    if result.returncode != 0:
        state['failed'][unit] = (result.stderr or result.stdout)[-600:]
        print('  FAILED %s exit %d' % (unit, result.returncode))
        for name in pid_files:
            os.remove(name)
        continue
    if not pid_files:
        state['failed'][unit] = 'compiled, but the hook produced no diary file'
        print('  NO DIARY %s' % unit)
        continue
    if len(pid_files) == 1:
        os.rename(pid_files[0], target)
    else:
        with open(target, 'wb') as sink:
            for name in pid_files:
                with open(name, 'rb') as source:
                    sink.write(source.read())
                os.remove(name)
    state['pid_files'][unit] = len(pid_files)
    lines = 0
    with open(target, errors='replace') as handle:
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
print('FINAL done=%d failed=%d of %d'
      % (len(done), len(state['failed']), total))
if state['failed']:
    print('failed units:', sorted(state['failed'])[:20])
counts = {}
for unit, number in state['pid_files'].items():
    counts[number] = counts.get(number, 0) + 1
print('pid files per compile, by count: %s' % sorted(counts.items()))
print('PEAK RESIDENT, replay driver : %.1f MB'
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
print('PEAK RESIDENT, largest child : %.1f MB'
      % (resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0))
PY

say "the REGENERATED c and cpp population, counted but not yet run"
# The brief allows extending past the original corpus only if the
# MEASURED per-probe cost allows. The compile cost plainly does (0.02 s
# a probe). The cost that actually binds is the DOWNSTREAM one: the
# coverage join holds one ordered coordinate list per probe, so the
# 6,144 MB ceiling is a ceiling on PROBES, not on compile time. This
# step counts the population and prints the arithmetic; it runs nothing.
python3 - <<'PY'
import json, os
STORE = ('PseudoCoupHQ/Research/op_pipeline/canon39_regen_store')
counts = {}
for name in sorted(os.listdir(STORE)):
    if not name.startswith('op_units2_'):
        continue
    language = name[len('op_units2_'):].rsplit('_c', 1)[0]
    if language not in ('c', 'cpp'):
        continue
    payload = json.load(open(os.path.join(STORE, name)))
    units = payload.get('units', payload)
    counts[language] = counts.get(language, 0) + len(units)
print('   regenerated units in the store, by language: %s' % counts)
print('   original corpus (this lap)                 : 1,380')
total = sum(counts.values())
print('   regenerated c and cpp, total               : %d' % total)
print('   at the measured 0.02 s a probe that is     : %.0f s of compile'
      % (total * 0.02))
print('   at the measured 690 KB a diary that is     : %.1f GB on disk'
      % (total * 690e3 / 1e9))
print('   at the measured 5,320 events a diary that is: %d events'
      % (total * 5320))
PY

say "the joint directory, for the c-AND-cpp coverage join"
# HARD LINKS, not copies: the same bytes under a name that says which
# language the probe is, so one join can read both populations without a
# second gigabyte on disk. `Graph.diary` keys a probe by the file stem.
python3 - <<'PY'
import os
REPO = 'PseudoCoupHQ/Research/compiler_graph'
joint = os.path.join(REPO, 'diaries', 'c_and_cpp')
os.makedirs(joint, exist_ok=True)
made = 0
for language in ('c', 'cpp'):
    source_directory = os.path.join(REPO, 'diaries', language)
    for name in sorted(os.listdir(source_directory)):
        if not name.endswith('.txt'):
            continue
        link = os.path.join(joint, '%s__%s' % (language, name))
        if os.path.exists(link):
            os.remove(link)
        os.link(os.path.join(source_directory, name), link)
        made = made + 1
print('   hard links made : %d' % made)
PY

say "inventory"
for D in c cpp c_and_cpp; do
  echo "   diaries/$D : $(ls "$REPO/diaries/$D" | wc -l) files, $(du -sh "$REPO/diaries/$D" | cut -f1)"
done
echo "   stray pid files left behind (must be 0):"
find "$REPO/diaries" -name '*.txt.*' | wc -l
df -h PseudoCoupHQ | tail -1
echo "DONE t81_l5"
