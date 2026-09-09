#!/usr/bin/env bash
# t81 lane 13 — the extension past the ORIGINAL corpus, as far as the
# MEASURED cost allows, and no further.
#
# WHAT THE MEASUREMENTS SAY, all of them taken by earlier lanes of this
# task and none of them estimated:
#   * compiling a probe costs 0.023 s and 690 KB of diary (lane 5:
#     1,380 probes in 33.6 s, 1,023 MB).
#   * the regenerated c and cpp population is 27,080 units (lane 5),
#     which is 542 s of compile and 18.7 GB of diary. THE COMPILE COST
#     ALLOWS IT.
#   * `Graph.coverage` costs 994.1 MB fixed plus 1.129 MB a probe
#     (lane 11, fitted from peaks at 50 and 400 probes). The stated
#     6,144 MB ceiling therefore allows 4,563 probes IN THE JOIN.
# So the binding cost is the JOIN's, not the compiler's, and this lane
# extends the diary to the largest population the join can actually
# read: 4,563 minus the 1,380 already diaried, taken with margin as
# 2,600 more, for 3,980 probes and a projected 5,487 MB.
#
# WHICH 2,600. Sorted by unit id over the whole regenerated population,
# then every k-th, so the slice is spread across all 308 store chunks
# rather than being the first two of them. The rule is arithmetic on
# unit ids -- machine coordinates, no token anywhere in the selection.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"
mkdir -p "$REPO/diaries/regen" /work/probe

say "[1/5] the slice, and whether a probe source exists for each unit"
python3 - <<'PY'
import json, os
STORE = 'PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
PIPELINE = 'PseudoCoupHQ/Research/op_pipeline'
REPO = 'PseudoCoupHQ/Research/compiler_graph'
WANTED = 2600

units = []
for name in sorted(os.listdir(STORE)):
    if not name.startswith('op_units2_'):
        continue
    language = name[len('op_units2_'):].rsplit('_c', 1)[0]
    if language not in ('c', 'cpp'):
        continue
    payload = json.load(open(os.path.join(STORE, name)))
    holder = payload.get('units', payload)
    for unit in holder:
        units.append((language, unit, name))
units.sort(key=lambda row: (row[0], row[1]))
print('   regenerated units, total : %d' % len(units))
step = max(1, len(units) // WANTED)
slice_rows = units[::step][:WANTED]
print('   every %dth taken          : %d' % (step, len(slice_rows)))
print('   store chunks represented  : %d'
      % len({row[2] for row in slice_rows}))

manifests = {}
for language in ('c', 'cpp'):
    payload = json.load(open(os.path.join(
        PIPELINE, 'probe_manifest_%s.json' % language)))
    holder = payload.get('probes', payload)
    table = {}
    if isinstance(holder, dict):
        rows = holder.values()
    else:
        rows = holder
    for row in rows:
        if isinstance(row, dict) and 'n' in row:
            table[int(row['n'])] = row
    manifests[language] = table
    print('   probe_manifest_%s.json rows keyed by n : %d'
          % (language, len(table)))

probes = {}
absent = []
for language, unit, chunk in slice_rows:
    number = unit.rsplit('_', 1)[-1]
    try:
        row = manifests[language][int(number)]
    except (KeyError, ValueError):
        absent.append(unit)
        continue
    source = row.get('source') or row.get('probe_source')
    if not source:
        absent.append(unit)
        continue
    probes[unit] = {'source': source, 'language': language,
                    'regen_chunk': chunk}
print('   probe source found        : %d' % len(probes))
print('   probe source absent       : %d' % len(absent))
for unit in absent[:10]:
    print('      %s' % unit)
out = os.path.join(REPO, 't81', 'probes_regen_slice.json')
json.dump({'meta': {
    'role': 'a measured slice of the REGENERATED c and cpp population',
    'selection': 'sorted by unit id over the whole regenerated '
                 'population, then every %dth -- arithmetic on unit ids, '
                 'no token in the selection' % step,
    'sized_by': 'Graph.coverage costs 994.1 MB fixed plus 1.129 MB a '
                'probe (lane 11), so the stated 6,144 MB ceiling allows '
                '4,563 probes in the join; 1,380 are already diaried',
    'regenerated_population': len(units),
    'requested': WANTED,
    'selected': len(slice_rows),
    'probe_source_absent': len(absent),
}, 'count': len(probes), 'probes': probes},
    open(out, 'w'), indent=1)
print('   wrote %s' % out)
PY

say "[2/5] the slice compiled through the instrumented clang"
python3 - <<'PY'
import glob, json, os, resource, subprocess, sys, time
REPO = 'PseudoCoupHQ/Research/compiler_graph'
STATE = os.path.join(REPO, 't81', 'diary_state_regen.json')
CLANG = '/persist/llvmbuild/bin/clang'
CLANGXX = '/persist/llvmbuild/bin/clang++'
probes = json.load(open(os.path.join(
    REPO, 't81', 'probes_regen_slice.json')))['probes']
units = sorted(probes)
total = len(units)
print('slice corpus: %d units' % total)
state = {'done': [], 'failed': {}, 'events': {}}
if os.path.exists(STATE):
    state = json.load(open(STATE))
done = set(state['done'])
started = time.time()
for index, unit in enumerate(units, 1):
    language = probes[unit]['language']
    target = os.path.join(REPO, 'diaries', 'regen',
                          '%s__%s.txt' % (language, unit))
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
    result = subprocess.run(
        [tool, standard, '-O1', '-c', source_path,
         '-o', '/work/probe/unit_ship.o'],
        env=dict(os.environ, COMPILER_DIARY=target),
        capture_output=True, text=True)
    pid_files = sorted(glob.glob(target + '.*'),
                       key=lambda name: int(name.rsplit('.', 1)[1]))
    if result.returncode != 0:
        state['failed'][unit] = (result.stderr or result.stdout)[-300:]
        for name in pid_files:
            os.remove(name)
        continue
    if not pid_files:
        state['failed'][unit] = 'compiled, but the hook produced no diary'
        continue
    if len(pid_files) == 1:
        os.rename(pid_files[0], target)
    else:
        with open(target, 'wb') as sink:
            for name in pid_files:
                sink.write(open(name, 'rb').read())
                os.remove(name)
    lines = 0
    with open(target, errors='replace') as handle:
        for lines, _ in enumerate(handle, 1):
            pass
    state['events'][unit] = lines
    done.add(unit)
    state['done'] = sorted(done)
    if index % 100 == 0 or index == total:
        json.dump(state, open(STATE, 'w'), indent=1)
        print('[%d/%d] done=%d failed=%d  %.1f probes/s'
              % (index, total, len(done), len(state['failed']),
                 index / max(time.time() - started, 0.001)))
        sys.stdout.flush()
json.dump(state, open(STATE, 'w'), indent=1)
print('FINAL done=%d failed=%d of %d'
      % (len(done), len(state['failed']), total))
if state['failed']:
    print('a failing unit and its diagnostic, LITERAL:')
    unit = sorted(state['failed'])[0]
    print('   %s -> %s' % (unit, state['failed'][unit]))
print('PEAK RESIDENT, replay driver : %.1f MB'
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[3/5] the extended join population, as one directory of hard links"
python3 - <<'PY'
import os
REPO = 'PseudoCoupHQ/Research/compiler_graph'
joint = os.path.join(REPO, 'diaries', 'extended')
os.makedirs(joint, exist_ok=True)
made = 0
for source_directory, prefix in ((os.path.join(REPO, 'diaries', 'c'), 'c__'),
                                 (os.path.join(REPO, 'diaries', 'cpp'), 'cpp__'),
                                 (os.path.join(REPO, 'diaries', 'regen'), '')):
    if not os.path.isdir(source_directory):
        continue
    for name in sorted(os.listdir(source_directory)):
        if not name.endswith('.txt'):
            continue
        link = os.path.join(joint, prefix + name)
        if os.path.exists(link):
            os.remove(link)
        os.link(os.path.join(source_directory, name), link)
        made = made + 1
print('   hard links in diaries/extended : %d' % made)
PY
du -sh "$REPO/diaries/regen" "$REPO/diaries/extended" 2>/dev/null
df -h PseudoCoupHQ | tail -1

say "[4/5] the coverage join over the extended population"
python3 t81/run_with_peak.py graph.py join \
    --graph graph_cpp.json --diaries diaries/extended \
    --instrumented t81/instrumented_cpp.json \
    --out coverage_extended.json 2>&1 | tail -14
ls -la coverage_extended.json | awk '{print "   artifact bytes:", $5}'

say "[5/5] what the extra probes bought, against the 1,380-probe join"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
before = json.load(open(REPO + '/coverage_c_and_cpp.json'))
after = json.load(open(REPO + '/coverage_extended.json'))
for name in ('population_instrumented', 'population_probes',
             'instrumented_visited_by_at_least_one_probe',
             'never_visited_count', 'visited_keys_outside_the_region'):
    print('   %-44s %8s -> %8s' % (name, before[name], after[name]))
gained = (set(before['never_visited']) - set(after['never_visited']))
print('   bodies visited by the extra probes and by no original probe : %d'
      % len(gained))
by_file = {}
nodes_by_file = {}
for node_id in gained:
    file_name = node_id.split('#', 1)[0]
    by_file[file_name] = by_file.get(file_name, 0) + 1
for name, count in sorted(by_file.items(), key=lambda row: -row[1])[:10]:
    print('      %5d  %s' % (count, name))
summary = {
    'what_this_is': 'the coverage join over the original 1,380 probes '
                    'plus a measured slice of the regenerated '
                    'population, and the difference between the two',
    'before': {k: before[k] for k in (
        'population_instrumented', 'population_probes',
        'instrumented_visited_by_at_least_one_probe',
        'never_visited_count')},
    'after': {k: after[k] for k in (
        'population_instrumented', 'population_probes',
        'instrumented_visited_by_at_least_one_probe',
        'never_visited_count')},
    'bodies_gained_by_the_extra_probes': len(gained),
    'bodies_gained_by_file': dict(sorted(by_file.items(),
                                         key=lambda row: -row[1])),
    'never_visited_by_file_after': after['never_visited_by_file'],
}
out = REPO + '/coverage_extended_summary.json'
json.dump(summary, open(out, 'w'), indent=1)
print('   wrote %s' % out)
PY
echo "DONE t81_l13"
