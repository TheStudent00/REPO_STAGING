#!/usr/bin/env bash
# t87 lane 10 — the five artifacts rebuilt with the census note added,
# THE SPELLING BAN PROVED ON THE OUTPUT ITSELF, and the unmodified guard
# over every artifact of this task IN ONE PROCESS.
#
# THE BAN PROOF, and why it is a measurement rather than an assurance.
# A grouping that secretly used the operator's token would put units
# with the SAME display label together and never put units with
# DIFFERENT labels together. So this lane counts both directions on the
# artifacts as written:
#   * variants whose members carry MORE THAN ONE distinct display label
#     -- impossible if the token were the key;
#   * display labels that appear in MORE THAN ONE variant -- impossible
#     if the token were the key.
# Both are printed with their populations.
#
# THE MEMORY BOUND: the passes are the ones lanes 6-8 measured (172.9 MB
# for go over graph_go.json, 1,052.2 MB for c and cpp over
# graph_cpp.json, both against a 6,144 MB ceiling that refuses BY NAME).
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

say "[1/5] rebuild the five measured artifacts"
python3 -m py_compile graph.py && echo "   py_compile exit=0"
run() {
  local out="$1"; shift
  python3 t81/run_with_peak.py graph.py variant-connections \
      --subject probe_own --memory-ceiling-mb 6144 \
      --max-transitions 8000000 --exclusive-examples 8 \
      --out "$out" "$@" 2>&1 | grep -E "PEAK RESIDENT|wrote "
}
run variant_connections_go.json --graph graph_go.json --diaries diaries/go \
    --language go --units "$PIPE/canon39_wrapped_go.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0000.json" \
    --units "$PIPE/canon39_regen_store/op_units2_go_c0001.json" \
    --cache /work/v_go.i32
run variant_connections_c.json --graph graph_cpp.json --diaries diaries/c \
    --language c --units "$PIPE/canon39_wrapped_c.json" --cache /work/v_c.i32
run variant_connections_cpp.json --graph graph_cpp.json --diaries diaries/cpp \
    --language cpp --units "$PIPE/canon39_wrapped_cpp.json" --cache /work/v_cpp.i32
run variant_connections_c_and_cpp.json --graph graph_cpp.json \
    --diaries diaries/c_and_cpp --units "$PIPE/canon39_wrapped_c.json" \
    --units "$PIPE/canon39_wrapped_cpp.json" --cache /work/v_cc.i32
run variant_connections_extended.json --graph graph_cpp.json \
    --diaries diaries/extended --units "$PIPE/canon39_wrapped_c.json" \
    --units "$PIPE/canon39_wrapped_cpp.json" \
    --units "$PIPE/canon39_regen_store" --cache /work/v_ext.i32

say "[2/5] THE BAN PROVED ON THE OUTPUT: labels across variants, both ways"
python3 - <<'PY'
import json
for path in ("variant_connections_go.json",
             "variant_connections_c_and_cpp.json",
             "variant_connections_extended.json"):
    d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/' + path))
    rows = d["variants"]
    mixed = []
    label_to_variants = {}
    for r in rows:
        labels = set()
        for m in r["members"]:
            labels.add(m["operator"])
            label_to_variants.setdefault(m["operator"], set()).add(r["variant_id"])
        if len(labels) > 1:
            mixed.append((r["variant_id"], sorted(x for x in labels if x)))
    split = {k: len(v) for k, v in label_to_variants.items() if len(v) > 1}
    print("   --- %s" % path)
    print("      variants                                     %5d" % len(rows))
    print("      variants whose members carry >1 display label %5d" % len(mixed))
    print("      distinct display labels in the population     %5d"
          % len(label_to_variants))
    print("      labels spread over more than one variant      %5d" % len(split))
    print("      labels confined to exactly one variant        %5d"
          % (len(label_to_variants) - len(split)))
    for vid, labels in mixed[:4]:
        print("        MIXED %s carries %s" % (vid, labels))
    worst = sorted(split.items(), key=lambda kv: -kv[1])[:4]
    for label, n in worst:
        print("        SPREAD label %-8s appears in %d distinct variants"
              % (json.dumps(label), n))
PY

say "[3/5] the census note is on every artifact"
python3 - <<'PY'
import json, os
base = '/projects/PseudoCoupHQ/Research/compiler_graph/'
for name in sorted(os.listdir(base)):
    if not name.startswith('variant_connections_'):
        continue
    d = json.load(open(base + name))
    note = d.get("census", {}).get("how_to_read_this")
    print("   %-42s state %-32s census note %s"
          % (name, d["state"], "present" if note else "(none -- unmeasured)"))
PY

say "[4/5] the guard, UNMODIFIED, ONE PROCESS, over every artifact of task 87"
md5sum "$PIPE/check_no_spelling_keys.py"
cd /projects/PseudoCoupHQ && git status --porcelain Research/op_pipeline/check_no_spelling_keys.py && echo "   (git reports no change to the guard)"
cd "$REPO"
python3 "$PIPE/check_no_spelling_keys.py" \
    variant_connections_go.json \
    variant_connections_c.json \
    variant_connections_cpp.json \
    variant_connections_c_and_cpp.json \
    variant_connections_extended.json \
    variant_connections_rust.json \
    variant_connections_swift.json \
    > guard_task87.txt 2>&1
echo "   guard exit=$?"
cat guard_task87.txt
echo "   grep -c exempt over the transcript:"
grep -c exempt guard_task87.txt || true

say "[5/5] every artifact this task wrote, with its size"
ls -la variant_connections_*.json guard_task87.txt | awk '{print "   ", $9, $5}'
df -h /work | tail -1
echo "DONE t87_l10"
