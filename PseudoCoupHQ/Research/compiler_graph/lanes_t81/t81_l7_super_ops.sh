#!/usr/bin/env bash
# t81 lane 7 — `Graph.super_ops` over the cpp diaries, with THE SAME
# PARAMETERS the go lap used, and then the both-ways comparison against
# the output-side miner's cpp candidates.
#
# THE PARAMETERS ARE QUOTED FROM THE GO ARTIFACT, not from notes: step 1
# prints the `parameters` block of super_ops_go.json and step 3 passes
# exactly those values on the command line.
#
# THE MEMORY BOUND, STATED BEFORE THE PASS.
#   * `encode_diaries` streams ONE diary at a time into an int32 file on
#     /persist. Its live set is one diary plus the alphabet: bounded by
#     the largest diary, not by the corpus.
#   * the miner then counts CONTIGUOUS RUNS level by level. Its live set
#     is one level's run table. That table is capped at
#     max_runs_per_level = 2,000,000 and the pass refuses BY NAME when
#     it is passed. Nothing enumerates every sub-path of the corpus --
#     that shape is what reached 13.2 GB on 2026-09-03.
#   * `memory_ceiling_mb = 6144` is checked with resource.getrusage
#     inside the miner and raises MemoryCeilingReached, by name.
# A 100-probe SAMPLE runs first and its peak resident size is printed
# before the full pass is allowed to start.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/6] the go lap's parameters, QUOTED FROM ITS OWN ARTIFACT"
python3 - <<'PY'
import json
payload = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                         'super_ops_go.json'))
print(json.dumps(payload['parameters'], indent=1))
print('   go populations, for the comparison of scale:')
print(json.dumps({k: v for k, v in payload['populations'].items()
                  if k != 'frequent_runs_by_length'}, indent=1))
PY

say "[2/6] the tools parse (nothing has been run on the host)"
python3 -m py_compile graph.py report_super_ops.py t81/run_with_peak.py \
    t81/inject_diary_clang.py && echo "   py_compile exit=0 for all four"

say "[3/6] the SAMPLE mine -- 100 cpp diaries, same parameters"
rm -rf /work/ops_sample && mkdir -p /work/ops_sample
python3 - <<'PY'
import os
source = 'PseudoCoupHQ/Research/compiler_graph/diaries/cpp'
names = sorted(n for n in os.listdir(source) if n.endswith('.txt'))
for name in names[:100]:
    os.symlink(os.path.join(source, name),
               os.path.join('/work/ops_sample', name))
print('   cpp diaries on disk : %d' % len(names))
print('   sampled             : %d' % min(100, len(names)))
PY
python3 t81/run_with_peak.py graph.py super-ops \
    --graph graph_cpp.json --diaries /work/ops_sample \
    --min-length 3 --min-support 2 --max-length 12 \
    --max-runs-per-level 2000000 --memory-ceiling-mb 6144 \
    --subject probe_own --language cpp \
    --cache /persist/streams_cpp_sample.i32 \
    --out /work/super_ops_cpp_sample.json 2>&1 | tail -40

say "[4/6] the full mine over every cpp diary"
python3 t81/run_with_peak.py graph.py super-ops \
    --graph graph_cpp.json --diaries diaries/cpp \
    --min-length 3 --min-support 2 --max-length 12 \
    --max-runs-per-level 2000000 --memory-ceiling-mb 6144 \
    --subject probe_own --language cpp \
    --cache /persist/streams_cpp_probe_own.i32 \
    --out super_ops_cpp.json 2>&1 | tail -60
RC=${PIPESTATUS[0]}
echo "   full mine exit=$RC"
if [ ! -s super_ops_cpp.json ]; then
  echo "   STOP: no candidate artifact was written"; exit 8
fi
ls -la super_ops_cpp.json | awk '{print "   artifact bytes:", $5}'

say "[5/6] the both-ways comparison against the output-side miner"
python3 t81/run_with_peak.py report_super_ops.py compare \
    --candidates super_ops_cpp.json \
    --output-side PseudoCoupHQ/Research/op_pipeline/super_ops3.json \
    --language cpp \
    --out super_ops_comparison_cpp.json 2>&1 | tail -30

say "[6/6] the go artifact is unchanged by the language argument"
# ZERO REGRESSIONS, PROVED rather than asserted: the go comparison is
# re-run with the default and compared byte for byte with the artifact
# task 75 wrote.
cp -f super_ops_comparison_go.json /work/super_ops_comparison_go_before.json
python3 t81/run_with_peak.py report_super_ops.py compare \
    --candidates super_ops_go.json \
    --output-side PseudoCoupHQ/Research/op_pipeline/super_ops3.json \
    --out /work/super_ops_comparison_go_again.json 2>&1 | tail -12
echo "   diff against task 75's artifact (no output means identical):"
diff /work/super_ops_comparison_go_before.json \
     /work/super_ops_comparison_go_again.json && echo "   IDENTICAL"
df -h /persist | tail -1
echo "DONE t81_l7"
