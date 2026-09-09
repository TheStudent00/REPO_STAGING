#!/usr/bin/env bash
# t87 lane 7 — THE THIRD CONNECTION KIND, c and cpp (one compiler, one
# graph: graph_cpp.json serves both). SAMPLE first, then the full pass
# over all 1,380 ORIGINAL probes.
#
# THE MEMORY BOUND, STATED BEFORE THE PASS. Same shape as lane 6, with
# the fixed cost measured for THIS graph: graph_cpp.json loaded whole is
# 1,043.1 MB peak resident (lane t87_l1, printed there). The pass adds
# O(distinct coordinates) + O(distinct transitions) + one variant's two
# sets; the go full pass added 9 MB over its own graph load. Two
# measured points are taken (100 probes, then 400) and the fixed and
# per-probe terms are FITTED before the full pass is allowed, because
# one measurement cannot separate them -- the error that made lane 10 of
# task 81 refuse a pass that fitted comfortably (log_190 section 3.4).
# `memory_ceiling_mb` = 6,144 and `max_transitions` = 8,000,000 both
# refuse BY NAME (MemoryCeilingReached).
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
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
cd "$REPO"

say "[1/5] the population, RECOUNTED here"
python3 - <<'PY'
import json, os
base = '/projects/PseudoCoupHQ/Research/compiler_graph/diaries/c_and_cpp'
names = sorted(n for n in os.listdir(base) if n.endswith('.txt'))
c = [n for n in names if n.startswith('c__')]
cpp = [n for n in names if n.startswith('cpp__')]
print("   diaries/c_and_cpp : %d files  (c %d, cpp %d)" % (len(names), len(c), len(cpp)))
for lang, n in (("c", 610), ("cpp", 770)):
    doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                         'canon39_wrapped_%s.json' % lang))
    print("   canon39_wrapped_%-3s : %d units" % (lang, len(doc["units"])))
PY

say "[2/5] MEMORY GATE -- two measured points, then the fit"
for N in 100 400; do
  rm -rf /work/var_s$N && mkdir -p /work/var_s$N
  python3 - "$N" <<'PY'
import os, sys
n = int(sys.argv[1])
source = '/projects/PseudoCoupHQ/Research/compiler_graph/diaries/c_and_cpp'
names = sorted(x for x in os.listdir(source) if x.endswith('.txt'))
for name in names[:n]:
    os.symlink(os.path.join(source, name), os.path.join('/work/var_s%d' % n, name))
PY
  python3 t81/run_with_peak.py graph.py variant-connections \
      --graph graph_cpp.json --diaries /work/var_s$N \
      --units "$PIPE/canon39_wrapped_c.json" \
      --units "$PIPE/canon39_wrapped_cpp.json" \
      --subject probe_own --memory-ceiling-mb 6144 \
      --max-transitions 8000000 --exclusive-examples 8 \
      --cache /work/vs_$N.i32 \
      --out /work/vc_sample_$N.json 2>&1 | grep -E "PEAK RESIDENT|operator_traced_variants|distinct_transitions|probes_with_a_machine_form"
done
python3 - <<'PY'
import json, re, os
# the two peaks are re-read from the artifacts themselves, not from notes
a = json.load(open('/work/vc_sample_100.json'))["cost"]["peak_resident_mb"]
b = json.load(open('/work/vc_sample_400.json'))["cost"]["peak_resident_mb"]
per = (b - a) / (400 - 100)
fixed = a - per * 100
print("   peak at 100 probes     : %.1f MB" % a)
print("   peak at 400 probes     : %.1f MB" % b)
print("   fitted fixed cost      : %.1f MB (the graph in memory)" % fixed)
print("   fitted per-probe cost  : %.4f MB" % per)
print("   PROJECTION for 1,380   : %.0f MB" % (fixed + per * 1380))
print("   PROJECTION for 3,980   : %.0f MB" % (fixed + per * 3980))
allowed = (6144 - fixed) / per if per > 0 else float('inf')
print("   probes the 6,144 MB ceiling allows at this rate : %s"
      % ("no bound from this fit" if per <= 0 else "%.0f" % allowed))
if fixed + per * 3980 > 6144:
    print("   MEMORY GATE: REFUSED -- the extended pass does not fit")
else:
    print("   MEMORY GATE: under the ceiling; the full passes may run.")
PY

say "[3/5] the FULL pass -- all 1,380 original c and cpp probes"
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_cpp.json --diaries diaries/c_and_cpp \
    --units "$PIPE/canon39_wrapped_c.json" \
    --units "$PIPE/canon39_wrapped_cpp.json" \
    --subject probe_own --memory-ceiling-mb 6144 \
    --max-transitions 8000000 --exclusive-examples 8 \
    --cache /work/variant_streams_c_and_cpp.i32 \
    --out variant_connections_c_and_cpp.json 2>&1 | tail -60
RC=${PIPESTATUS[0]}
echo "   full pass exit=$RC"
[ -s variant_connections_c_and_cpp.json ] || { echo "   STOP: no artifact"; exit 8; }
ls -la variant_connections_c_and_cpp.json | awk '{print "   artifact bytes:", $5}'

say "[4/5] the two single-language passes, for the per-language populations"
for L in c cpp; do
  python3 t81/run_with_peak.py graph.py variant-connections \
      --graph graph_cpp.json --diaries diaries/$L --language $L \
      --units "$PIPE/canon39_wrapped_$L.json" \
      --subject probe_own --memory-ceiling-mb 6144 \
      --max-transitions 8000000 --exclusive-examples 8 \
      --cache /work/variant_streams_$L.i32 \
      --out variant_connections_$L.json 2>&1 \
    | grep -E "PEAK RESIDENT|\"diaries_on_disk\"|operator_traced_variants|distinct_nodes_entered|distinct_transitions|walked_by_exactly_one_variant"
  echo "   --- $L done"
done

say "[5/5] the guard, UNMODIFIED, over what this lane wrote"
md5sum "$PIPE/check_no_spelling_keys.py"
python3 "$PIPE/check_no_spelling_keys.py" \
    variant_connections_c_and_cpp.json \
    variant_connections_c.json variant_connections_cpp.json
echo "   guard exit=$?"
df -h /work | tail -1
echo "DONE t87_l7"
