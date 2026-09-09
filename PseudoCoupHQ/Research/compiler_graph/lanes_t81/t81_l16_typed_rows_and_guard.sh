#!/usr/bin/env bash
# t81 lane 16 — the typed-object SHAPE the guard's refusal asked for,
# then every artifact rebuilt on it, then the guard again.
#
# WHAT LANE 15 FOUND, and it is a real finding rather than a nuisance.
# The unmodified guard refused five artifacts, all for ONE cause: a
# function of the compiler region is named `consume`, `consume` is one
# of the 91 operator tokens the guard reads out of the probe manifests,
# and the row carrying that name as its `label` did not identify itself
# as ONE unit -- it had a unit id but no language field -- so the guard
# could only read the token as a grouping key. It was right to.
#
# THE FIX IS THE RULED ONE (log_158): a flagged machine-form value gets
# a typed-object SHAPE. Not a role key. Not a field whitelist. Not an
# edit to the guard, which is untouched and whose md5 is printed below.
# `Graph.coverage`'s never-visited rows and `diary_inputs_build.py`'s
# target rows now carry a `language` field beside their unit id, so each
# row identifies one unit and its label is a display name on that unit.
#
# NOTHING READS THE NEW FIELD. The injector reads `id`, `file`,
# `start_line`, `end_line` and `label`; step 1 proves the target file
# differs from the one the instrumented build was made from by exactly
# the added lines and nothing else, so the built clang is still the
# clang these targets describe and is not rebuilt.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
PIPELINE=PseudoCoupHQ/Research/op_pipeline
cd "$REPO"

say "[1/5] the two inputs rebuilt, and the difference measured"
cp t81/probes_cpp.json /work/probes_before.json
cp t81/diary_targets_cpp.json /work/targets_before.json
python3 t81/diary_inputs_build.py 2>&1 | tail -8
echo "   probes_cpp.json against the file before this lane:"
if diff -q /work/probes_before.json t81/probes_cpp.json >/dev/null; then
  echo "      IDENTICAL"
else
  echo "      DIFFERS -- a finding"; diff /work/probes_before.json t81/probes_cpp.json | head -10
fi
echo "   diary_targets_cpp.json, lines only in the NEW file:"
diff /work/targets_before.json t81/diary_targets_cpp.json \
    | grep -c '^> ' || true
echo "   lines only in the OLD file (must be 0):"
diff /work/targets_before.json t81/diary_targets_cpp.json \
    | grep -c '^< ' || true
echo "   every added line, by its key (must be one key only):"
diff /work/targets_before.json t81/diary_targets_cpp.json \
    | grep '^> ' | sed 's/.*"\([a-z_]*\)":.*/\1/' | sort | uniq -c

say "[2/5] the four coverage joins rebuilt on the typed rows"
I=0
for D in cpp c c_and_cpp extended ; do
  I=$((I+1))
  echo "   [$I/4] diaries/$D"
  python3 t81/run_with_peak.py graph.py join \
      --graph graph_cpp.json --diaries "diaries/$D" \
      --instrumented t81/instrumented_cpp.json \
      --out "coverage_$D.json" 2>&1 | tail -12
  ls -la "coverage_$D.json" | awk '{print "      artifact bytes:", $5}'
done
mv -f coverage_c_and_cpp.json /work/keep_name_check 2>/dev/null || true
mv -f /work/keep_name_check coverage_c_and_cpp.json 2>/dev/null || true

say "[3/5] the two summaries rebuilt"
python3 - <<'PY'
import json
REPO = 'PseudoCoupHQ/Research/compiler_graph'
result = json.load(open(REPO + '/coverage_c_and_cpp.json'))
by_file = result['never_visited_by_file']
for name in ('population_region_nodes', 'population_defs',
             'population_instrumented', 'population_probes',
             'instrumented_visited_by_at_least_one_probe',
             'defs_visited_by_at_least_one_probe', 'never_visited_count',
             'uninstrumented_defs_a_named_frontier',
             'visited_keys_outside_the_region'):
    print('   %-42s %s' % (name, result[name]))
print('   never-visited FILES : %d' % len(by_file))
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
          % (language, one['instrumented_visited_by_at_least_one_probe'],
             one['population_instrumented'], one['population_probes']))
json.dump(summary, open(REPO + '/coverage_cpp_summary.json', 'w'), indent=1)

before = result
after = json.load(open(REPO + '/coverage_extended.json'))
gained = set(before['never_visited']) - set(after['never_visited'])
by_file_gained = {}
for node_id in gained:
    name = node_id.split('#', 1)[0]
    by_file_gained[name] = by_file_gained.get(name, 0) + 1
print('   extended: %s probes, %s visited, %s never; gained %d bodies'
      % (after['population_probes'],
         after['instrumented_visited_by_at_least_one_probe'],
         after['never_visited_count'], len(gained)))
extended = {
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
    'bodies_gained_by_file': dict(sorted(by_file_gained.items(),
                                         key=lambda row: -row[1])),
    'never_visited_by_file_after': after['never_visited_by_file'],
}
json.dump(extended, open(REPO + '/coverage_extended_summary.json', 'w'),
          indent=1)
print('   both summaries rewritten')
PY

say "[4/5] EVERY artifact, ONE process, guard unmodified"
ARTIFACTS="
$REPO/t81/probes_cpp.json
$REPO/t81/diary_targets_cpp.json
$REPO/t81/inject_report_cpp2.json
$REPO/t81/instrumented_cpp.json
$REPO/t81/diary_state_cpp.json
$REPO/t81/diary_state_regen.json
$REPO/t81/probes_regen_slice.json
$REPO/t81/sample_probe_cost.json
$REPO/coverage_cpp_summary.json
$REPO/coverage_extended_summary.json
$REPO/super_ops_comparison_cpp.json
$REPO/super_ops_cpp.json
$REPO/coverage_c.json
$REPO/coverage_cpp.json
$REPO/coverage_c_and_cpp.json
$REPO/coverage_extended.json
"
cd "$PIPELINE"
# shellcheck disable=SC2086
python3 "$PIPELINE/check_no_spelling_keys.py" $ARTIFACTS \
    > "$REPO/guard_task81.txt" 2>&1
RC=$?
echo "   guard exit=$RC"
cat "$REPO/guard_task81.txt"
echo "   grep -c exempt on that output:"
grep -c exempt "$REPO/guard_task81.txt" || true

say "[5/5] the guard file is unmodified"
git -C PseudoCoupHQ status --porcelain \
    Research/op_pipeline/check_no_spelling_keys.py
echo "   (no line above means the guard file is untouched)"
md5sum "$PIPELINE/check_no_spelling_keys.py"
if [ $RC -ne 0 ]; then echo "   STOP: the guard still refuses"; exit 5; fi
echo "DONE t81_l16"
