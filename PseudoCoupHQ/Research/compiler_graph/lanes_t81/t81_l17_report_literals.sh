#!/usr/bin/env bash
# t81 lane 17 — the LITERALS the report quotes, printed from the
# artifacts themselves so no figure in log_190 is retyped from notes.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/6] one instrumented body, LITERAL, in the built tree"
grep -n -m1 -B2 -A2 "t81diary::note(\"clang/lib/CodeGen/CGExprScalar.cpp" \
    /persist/llvmsrc/clang/lib/CodeGen/CGExprScalar.cpp | head -12

say "[2/6] the subject spot, LITERAL"
grep -n -A2 "t81diary::enter(" \
    /persist/llvmsrc/clang/lib/CodeGen/CodeGenFunction.cpp | head -6

say "[3/6] one diary, its first line after the subject opens, LITERAL"
grep -n -m1 -A3 "subject_enter" diaries/cpp/op_0.txt | head -6
echo "   lines in that diary : $(wc -l < diaries/cpp/op_0.txt)"
echo "   lines whose subject column is the probe's own function:"
cut -f2 diaries/cpp/op_0.txt | grep -c '^op_0$'

say "[4/6] the ten files with the most never-visited bodies, joint join"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
s = json.load(open(REPO + '/coverage_cpp_summary.json'))
rows = list(s['never_visited_by_file'].items())
print('   never-visited bodies : %d over %d files, from a population of '
      '%d instrumented and %d probes'
      % (s['never_visited_count'], len(rows), s['population_instrumented'],
         s['population_probes']))
for name, count in rows[:10]:
    print('      %6d  %s' % (count, name))
print('   the ten files with the FEWEST (one each), for the shape:')
for name, count in rows[-5:]:
    print('      %6d  %s' % (count, name))
PY

say "[5/6] one super_ops candidate, LITERAL, from super_ops_cpp.json"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
payload = json.load(open(REPO + '/super_ops_cpp.json'))
print('   parameters : %s' % json.dumps(payload['parameters']))
print('   populations: %s' % json.dumps(payload['populations']))
top = payload['candidates'][0]
print('   candidate_id %s length %d probe_support %d of %d'
      % (top['candidate_id'], top['length'], top['probe_support'],
         payload['populations']['probes']))
for span in top['source_spans']:
    print('      %-60s %s' % (span['coordinate'], span.get('label')))
# a DISCRIMINATING one: the highest-support candidate that is not walked
# by every probe
probes = payload['populations']['probes']
for candidate in payload['candidates']:
    if candidate['probe_support'] < probes:
        print('   the highest-support candidate NOT walked by every probe:')
        print('   %s length %d support %d of %d'
              % (candidate['candidate_id'], candidate['length'],
                 candidate['probe_support'], probes))
        for span in candidate['source_spans']:
            print('      %-60s %s' % (span['coordinate'], span.get('label')))
        break
PY

say "[6/6] one STRICT match, LITERAL, from super_ops_comparison_cpp.json"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
payload = json.load(open(REPO + '/super_ops_comparison_cpp.json'))
print('   what_this_join_is : %s' % payload['what_this_join_is'])
print('   populations       : %s' % json.dumps(payload['populations']))
print('   the_two_tests     : %s' % json.dumps(payload['the_two_tests']))
for name in ('output_side_with_a_graph_counterpart_loose',
             'output_side_with_a_graph_counterpart_strict',
             'output_side_without_a_graph_counterpart',
             'graph_candidates_with_an_output_side_counterpart',
             'graph_candidates_without_an_output_side_counterpart'):
    print('   %-52s %s' % (name, payload[name]))
for row in payload['matched']:
    if row['graph_candidates_confined_to_those_units']:
        print('   one strict match, LITERAL:')
        print('      idiom_id  %s' % row['idiom_id'])
        print('      section   %s' % row['section'])
        print('      support   %s' % row['support'])
        print('      units it names (%d): %s'
              % (len(row['cpp_units_named']), row['cpp_units_named'][:8]))
        print('      candidates confined to those units (%d): %s'
              % (len(row['graph_candidates_confined_to_those_units']),
                 row['graph_candidates_confined_to_those_units'][:6]))
        break
PY
echo "DONE t81_l17"
