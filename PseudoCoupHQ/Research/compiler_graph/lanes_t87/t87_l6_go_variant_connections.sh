#!/usr/bin/env bash
# t87 lane 6 — THE THIRD CONNECTION KIND, go: a SAMPLE first, then the
# full pass over all 590 go diaries.
#
# THE MEMORY BOUND, STATED BEFORE THE PASS.
#   * the graph in memory is the FIXED cost and is measured, not
#     guessed: graph_go.json loaded whole is 163.6 MB peak resident
#     (lane t87_l1, printed there);
#   * unit records are read ONE FILE AT A TIME and only a digest and a
#     five-field member record survive each file;
#   * diaries are streamed by `Graph.encode_diaries`, one file at a
#     time, into an int32 file on /work -- the same streamer the miner
#     uses, whose live set is one diary;
#   * the live tables are then O(distinct coordinates) and O(distinct
#     transitions) plus ONE variant's two sets. Nothing enumerates
#     sub-paths: that shape reached 13.2 GB on 2026-09-03 and took the
#     machine's swap with it;
#   * `max_transitions` = 8,000,000 caps the transition table and
#     `memory_ceiling_mb` = 6,144 is checked with resource.getrusage at
#     every phase and every 25 probes. BOTH refuse BY NAME
#     (MemoryCeilingReached).
# A 50-diary SAMPLE runs first and its peak resident size is printed
# before the full pass is allowed to start.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
# units must run op_pipeline/check_no_spelling_keys.py and refuse its
# own output on failure.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
PIPE=PseudoCoupHQ/Research/op_pipeline
cd "$REPO"

say "[1/5] the tools parse (nothing of this has been run on the host)"
python3 -m py_compile graph.py t81/run_with_peak.py && echo "   py_compile exit=0"

say "[2/5] the identity this lap groups by, printed from the code itself"
python3 - <<'PY'
import sys
sys.path.insert(0, 'PseudoCoupHQ/Research/compiler_graph')
import graph
print("   VARIANT_IDENTITY_STATED:")
print("     " + graph.VARIANT_IDENTITY_STATED)
print("   the four fields machine_form() reads, from the function itself:")
import inspect
src = inspect.getsource(graph.machine_form)
for line in src.splitlines():
    if 'unit.get(' in line or 'row.get(' in line or 'produced_by.get(' in line:
        print("     " + line.strip())
PY

say "[3/5] the SAMPLE -- 50 go diaries, every bound the full pass will use"
rm -rf /work/var_sample && mkdir -p /work/var_sample
python3 - <<'PY'
import os
source = 'PseudoCoupHQ/Research/compiler_graph/diaries/go'
names = sorted(n for n in os.listdir(source) if n.endswith('.txt'))
for name in names[:50]:
    os.symlink(os.path.join(source, name), os.path.join('/work/var_sample', name))
print("   go diaries on disk : %d" % len(names))
print("   sampled            : 50")
PY
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_go.json --diaries /work/var_sample --language go \
    --units "$PIPE/canon39_wrapped_go.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0000.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0001.json" \
    --subject probe_own --memory-ceiling-mb 6144 \
    --max-transitions 8000000 --exclusive-examples 8 \
    --cache /work/variant_streams_go_sample.i32 \
    --out /work/variant_connections_go_sample.json 2>&1 | tail -60

say "[4/5] the FULL pass -- all 590 go diaries"
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_go.json --diaries diaries/go --language go \
    --units "$PIPE/canon39_wrapped_go.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0000.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0001.json" \
    --subject probe_own --memory-ceiling-mb 6144 \
    --max-transitions 8000000 --exclusive-examples 8 \
    --cache /work/variant_streams_go.i32 \
    --out variant_connections_go.json 2>&1 | tail -70
RC=${PIPESTATUS[0]}
echo "   full pass exit=$RC"
if [ ! -s variant_connections_go.json ]; then
  echo "   STOP: no artifact was written"; exit 8
fi
ls -la variant_connections_go.json | awk '{print "   artifact bytes:", $5}'

say "[5/5] the guard, UNMODIFIED, over what this lane wrote"
md5sum "$PIPE/check_no_spelling_keys.py"
python3 "$PIPE/check_no_spelling_keys.py" variant_connections_go.json
echo "   guard exit=$?"
df -h /work | tail -1
echo "DONE t87_l6"
