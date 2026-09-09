#!/usr/bin/env bash
# t81 lane 6 — `Graph.coverage`: the c and cpp diaries joined to
# graph_cpp.json.
#
# THE MEMORY BOUND, STATED BEFORE THE PASS (round 15's added rule).
#   * `Graph.load` holds the whole region graph as Python objects. That
#     is ONE bound, MEASURED in step 2, not estimated.
#   * `Graph.diary` holds, for every probe, the ORDERED list of the
#     declaration coordinates it visited. Its bound is therefore
#     (total diary lines) x (one Python string plus one list slot). It
#     is NOT a whole-corpus enumeration -- nothing here enumerates
#     sub-paths, which is what reached 13.2 GB on 2026-09-03 -- but it
#     is linear in the corpus, so it is SAMPLED FIRST at 50 probes,
#     projected onto the full population, and REFUSED BY NAME if the
#     projection passes 6,144 MB.
#   * `coverage` adds one dict keyed by node id and one list per probe;
#     both are bounded by the two above.
# Every peak below is the kernel's own ru_maxrss, taken by
# t81/run_with_peak.py, which adds no behaviour to the program it runs.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/6] the instrumented population, from the injector's OWN report"
python3 - <<'PY'
import json, os
REPO = 'PseudoCoupHQ/Research/compiler_graph'
report = json.load(open(os.path.join(REPO, 't81', 'inject_report_cpp2.json')))
rows = []
for coordinate, node_id in zip(report['instrumented_coordinates'],
                               report['instrumented_ids']):
    file_name, line = coordinate.rsplit(':', 1)
    rows.append({'id': node_id, 'file': file_name, 'start_line': int(line)})
out = os.path.join(REPO, 't81', 'instrumented_cpp.json')
json.dump(rows, open(out, 'w'), indent=1)
print('   entry hooks actually placed       : %d' % len(rows))
print('   distinct declaration coordinates  : %d'
      % len({'%s:%d' % (r['file'], r['start_line']) for r in rows}))
print('   skipped, each a NAMED FRONTIER    : %d' % report['skipped'])
print('   by cause : %s' % json.dumps(report['skipped_by_cause']))
print('   wrote %s' % out)
PY

say "[2/6] graph_cpp.json: its recorded counts, RECOUNTED, and its load cost"
python3 - <<'PY'
import json, resource, sys, time
sys.path.insert(0, 'PseudoCoupHQ/Research/compiler_graph')
import graph as graph_module
started = time.time()
instance = graph_module.Graph.load(
    'PseudoCoupHQ/Research/compiler_graph/graph_cpp.json')
seconds = time.time() - started
nodes = instance.static_structure['nodes']
edges = instance.static_structure['edges']
kinds = {}
files = set()
for record in nodes.values():
    kinds[record.get('kind')] = kinds.get(record.get('kind'), 0) + 1
    if record.get('file'):
        files.add(record['file'])
print('   load seconds : %.1f' % seconds)
print('   PEAK RESIDENT after load : %.1f MB'
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
print('   nodes RECOUNTED : %d   (log_183 records 112,364)' % len(nodes))
print('   edges RECOUNTED : %d   (log_183 records 386,065)' % len(edges))
print('   nodes by kind   : %s' % json.dumps(dict(sorted(kinds.items()))))
print('   distinct files carried by nodes : %d   (record: 269 files)'
      % len(files))
print('   file-kind nodes : %d' % kinds.get('file', 0))
PY

say "[3/6] the SAMPLE join -- 50 cpp diaries, so the bound is measured"
rm -rf /work/sample_diaries && mkdir -p /work/sample_diaries
python3 - <<'PY'
import os
source = 'PseudoCoupHQ/Research/compiler_graph/diaries/cpp'
names = sorted(name for name in os.listdir(source) if name.endswith('.txt'))
for name in names[:50]:
    os.symlink(os.path.join(source, name),
               os.path.join('/work/sample_diaries', name))
print('   diaries on disk (cpp) : %d' % len(names))
print('   sampled               : %d' % min(50, len(names)))
PY
python3 t81/run_with_peak.py graph.py join \
    --graph graph_cpp.json --diaries /work/sample_diaries \
    --instrumented t81/instrumented_cpp.json \
    --out /work/coverage_sample.json | tee /work/sample_peak.txt
echo "   sample artifact bytes: $(stat -c %s /work/coverage_sample.json)"

say "[4/6] the MEMORY GATE: project the sample onto the full population"
python3 - <<'PY'
import os, re, sys
text = open('/work/sample_peak.txt').read()
found = re.search(r'PEAK RESIDENT ([0-9.]+) MB', text)
peak_mb = float(found.group(1)) if found else -1.0
source = 'PseudoCoupHQ/Research/compiler_graph/diaries'
counts = {}
for language in ('c', 'cpp', 'c_and_cpp'):
    path = os.path.join(source, language)
    counts[language] = len([n for n in os.listdir(path)
                            if n.endswith('.txt')]) \
        if os.path.isdir(path) else 0
sampled = min(50, counts['cpp'])
print('   sample peak resident   : %.1f MB over %d cpp diaries'
      % (peak_mb, sampled))
print('   diaries to join, c     : %d' % counts['c'])
print('   diaries to join, cpp   : %d' % counts['cpp'])
print('   diaries to join, joint : %d' % counts['c_and_cpp'])
scaled = peak_mb * counts['c_and_cpp'] / max(sampled, 1)
print('   WORST-CASE projection for the joint join : %.0f MB' % scaled)
print('   (worst case: the graph is a fixed cost, counted here as if it '
      'scaled with the probes, so the true figure is lower)')
if scaled > 6144:
    print('   MEMORY GATE: the projection passes the stated 6,144 MB '
          'ceiling. The full join is REFUSED BY NAME rather than run.')
    sys.exit(9)
print('   MEMORY GATE: under the ceiling; the full joins may run.')
PY
if [ $? -ne 0 ]; then echo "   STOP at the memory gate"; exit 9; fi

say "[5/6] the full joins -- cpp, c, and the two together"
for D in cpp c c_and_cpp ; do
  echo "   --- diaries/$D"
  python3 t81/run_with_peak.py graph.py join \
      --graph graph_cpp.json --diaries "diaries/$D" \
      --instrumented t81/instrumented_cpp.json \
      --out "coverage_$D.json"
  RC=$?
  echo "   join exit=$RC"
  ls -la "coverage_$D.json" 2>/dev/null | awk '{print "   artifact bytes:", $5}'
  if [ $RC -ne 0 ]; then echo "   STOP: the join failed"; exit 7; fi
done

say "[6/6] the never-visited set BY FILE, from the joint join"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
result = json.load(open(REPO + '/coverage_c_and_cpp.json'))
by_file = result['never_visited_by_file']
for name in ('population_region_nodes', 'population_defs',
             'population_instrumented', 'population_probes',
             'instrumented_visited_by_at_least_one_probe',
             'defs_visited_by_at_least_one_probe',
             'never_visited_count',
             'uninstrumented_defs_a_named_frontier',
             'visited_keys_outside_the_region'):
    print('   %-40s %s' % (name, result[name]))
print('   never-visited FILES                      : %d' % len(by_file))
print('   the twenty files with the most never-visited bodies:')
for name, count in list(by_file.items())[:20]:
    print('      %6d  %s' % (count, name))
summary = {name: result[name] for name in (
    'population_region_nodes', 'population_defs', 'population_instrumented',
    'population_probes', 'instrumented_visited_by_at_least_one_probe',
    'defs_visited_by_at_least_one_probe', 'never_visited_count',
    'uninstrumented_defs_a_named_frontier',
    'visited_keys_outside_the_region', 'outside_the_region_by_key',
    'never_visited_by_file')}
summary['per_language'] = {}
for language in ('c', 'cpp'):
    one = json.load(open('%s/coverage_%s.json' % (REPO, language)))
    summary['per_language'][language] = {
        name: one[name] for name in (
            'population_instrumented', 'population_probes',
            'instrumented_visited_by_at_least_one_probe',
            'never_visited_count', 'visited_keys_outside_the_region')}
    print('   %-4s : %s of %s instrumented bodies visited by %s probes'
          % (language,
             one['instrumented_visited_by_at_least_one_probe'],
             one['population_instrumented'], one['population_probes']))
out = REPO + '/coverage_cpp_summary.json'
json.dump(summary, open(out, 'w'), indent=1)
print('   wrote %s' % out)
PY
df -h PseudoCoupHQ | tail -1
echo "DONE t81_l6"
