#!/usr/bin/env bash
# t87 lane 8 — THE THIRD CONNECTION KIND over the EXTENDED population
# (3,980 c and cpp probes: the 1,380 original plus the 2,600
# regenerated task 81 diaried), and then the two languages that have a
# graph and no diaries, written down as UNMEASURED BY NAME.
#
# THE MEMORY BOUND. Lane 7 fitted the cost of this exact pass from two
# measured points: fixed 1,051.9 MB (graph_cpp.json in memory) and
# 0.0003 MB per probe, projecting 1,053 MB at 3,980 probes against a
# 6,144 MB ceiling. The one term this lane adds is the regenerated unit
# store: 326 shards, 219 MB on disk, read ONE SHARD AT A TIME with only
# a digest and a five-field member record surviving each. `check_memory`
# runs after every shard and refuses BY NAME (MemoryCeilingReached).
#
# RUST AND SWIFT ARE NOT APPROXIMATED. `Graph.variant_connections` with
# no diaries on disk returns state UNMEASURED_BY_ABSENCE_OF_DIARIES and
# carries the reason its caller passes -- quoted here from the cost page
# in log_175 sections 6.3 and 6.4, which measured both.
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

say "[1/4] the extended population, RECOUNTED here"
python3 - <<'PY'
import os
base = '/projects/PseudoCoupHQ/Research/compiler_graph/diaries/'
def stems(d):
    return set(n[:-4] for n in os.listdir(base + d) if n.endswith('.txt'))
ext, orig, regen = stems('extended'), stems('c_and_cpp'), stems('regen')
print("   diaries/extended  : %d" % len(ext))
print("   of which original : %d" % len(ext & orig))
print("   of which regenerated: %d" % len(ext & regen))
store = '/projects/PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
print("   regen store shards: %d" % len(os.listdir(store)))
PY

say "[2/4] the FULL extended pass -- 3,980 probes"
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_cpp.json --diaries diaries/extended \
    --units "$PIPE/canon39_wrapped_c.json" \
    --units "$PIPE/canon39_wrapped_cpp.json" \
    --units "$PIPE/canon39_regen_store" \
    --subject probe_own --memory-ceiling-mb 6144 \
    --max-transitions 8000000 --exclusive-examples 8 \
    --cache /work/variant_streams_extended.i32 \
    --out variant_connections_extended.json 2>&1 | tail -60
RC=${PIPESTATUS[0]}
echo "   extended pass exit=$RC"
[ -s variant_connections_extended.json ] || { echo "   STOP: no artifact"; exit 8; }
ls -la variant_connections_extended.json | awk '{print "   artifact bytes:", $5}'

say "[3/4] rust and swift -- UNMEASURED, by name, with the cost page's reason"
RUST_REASON="rust is BLOCKED on this machine and the block is not build time: /sources/rust is a partial (promisor) clone whose objects are fetched lazily from the network, this instance is configured proxy = no, and the corpus's own rustc commit 31fca3adb283cc9dfd56b49cdee9a96eb9c96ffd is ABSENT from the checkout. Measured in log_175 section 6.3, lanes t72_l5..l7. Two decisions come before any compute: a complete checkout, and a ruling on the pin."
SWIFT_REASON="swiftc CANNOT BE STARTED HERE and that is the measurement: swiftc is not installed in the container, and a swift compiler build wants five repositories side by side at matching tags of which three (cmark-gfm, swift-syntax, swift-corelibs-libdispatch) are absent from this disk and the fifth is Apple's LLVM fork rather than the upstream tree that is present. The direct cmake configure exits in 1 s on 'Could not find a package configuration file provided by cmark-gfm'. Measured in log_175 section 6.4. The cost is a FETCH decision first, roughly 10-15 GB, and a build second."
mkdir -p /work/no_diaries_rust /work/no_diaries_swift
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_rust.json --diaries /work/no_diaries_rust --language rust \
    --unmeasured-reason "$RUST_REASON" \
    --out variant_connections_rust.json 2>&1 | tail -25
python3 t81/run_with_peak.py graph.py variant-connections \
    --graph graph_swift.json --diaries /work/no_diaries_swift --language swift \
    --unmeasured-reason "$SWIFT_REASON" \
    --out variant_connections_swift.json 2>&1 | tail -25
python3 - <<'PY'
import json
for lang in ("rust", "swift"):
    doc = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                         'variant_connections_%s.json' % lang))
    print("   %-6s state=%s  variants=%d  probes=%d"
          % (lang, doc["state"], len(doc["variants"]),
             doc["populations"]["probes_with_a_machine_form"]))
    print("      reason: %s" % doc["reason"][:200])
PY

say "[4/4] the guard, UNMODIFIED, over what this lane wrote"
md5sum "$PIPE/check_no_spelling_keys.py"
python3 "$PIPE/check_no_spelling_keys.py" \
    variant_connections_extended.json \
    variant_connections_rust.json variant_connections_swift.json
echo "   guard exit=$?"
df -h /work | tail -1
echo "DONE t87_l8"
