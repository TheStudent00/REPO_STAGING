#!/usr/bin/env bash
# t93 lane 3 -- THE COMPACT FORM, PROVED ON THE TWO SMALLER GRAPHS.
#
# LANE 2 ABORTED, and is kept as the record: `parse_errors` is the number
# 0 in graph_go.json and the head reader graph_compact.py borrowed
# assumed every top-level member opens with a brace, so it raised
# KeyError: '0'. The fix carves a scalar too, and reads a member that
# sits at the END of the file from the line it opens on rather than by
# holding the file. Nothing else changed.
#
# Nothing is replaced here. The compact form is written beside the
# original and then EXPANDED BACK, and the rebuilt file is compared with
# the original BYTE FOR BYTE by md5 and by `cmp`. Only a lane that passes
# this earns the right to replace anything.
#
# Ceiling 6,144 MB, abort named MemoryCeilingReached (graph_compact.py).
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
# units must run op_pipeline/check_no_spelling_keys.py and refuse its own
# output on failure.
#
# The string table here is ordered by FREQUENCY IN THE DOCUMENT, which is
# machine-form evidence, and it is a list with no keys at all.
set -u
say() { echo; echo "======== $* ========"; }
CG=PseudoCoupHQ/Research/compiler_graph
cd "$CG"
mkdir -p /work/t93
total=10; i=0
step() { i=$((i+1)); echo; echo "======== [$i/$total] $* ========"; }

for LANG in go rust; do
  step "$LANG: compact"
  python3 graph_compact.py compact --graph graph_$LANG.json \
      --out /work/t93/graph_$LANG.compact.json || exit 1
  step "$LANG: expand, and the byte-for-byte diff"
  python3 graph_compact.py expand --compact /work/t93/graph_$LANG.compact.json \
      --out /work/t93/rebuilt_$LANG.json --verify || exit 1
  echo "   cmp against the original:"
  if cmp graph_$LANG.json /work/t93/rebuilt_$LANG.json; then
    echo "   cmp: IDENTICAL, 0 differing bytes"
  else
    echo "   cmp: DIFFERENT -- refusing"; exit 1
  fi
  diff -q graph_$LANG.json /work/t93/rebuilt_$LANG.json \
      && echo "   diff -q: the files are identical"
  BEFORE=$(stat -c%s graph_$LANG.json)
  AFTER=$(stat -c%s /work/t93/graph_$LANG.compact.json)
  python3 -c "print('   SIZES  graph_$LANG.json  before %d  after %d  (%.1f%% of the original, %.1fx smaller)' % ($BEFORE, $AFTER, 100.0*$AFTER/$BEFORE, $BEFORE/float($AFTER)))"
  step "$LANG: the head read still works -- pins and counts in the first 256 KB"
  python3 - <<PY
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import viewer_build
head = open("/work/t93/graph_$LANG.compact.json").read(262144)
counts = viewer_build.carve(head, "counts")
pins = viewer_build.carve(head, "pins")
print("   counts carved from the head:", counts is not None,
      "nodes", (counts or {}).get("nodes"), "edges", (counts or {}).get("edges"),
      "frontier", (counts or {}).get("frontier"))
print("   pins carved from the head:  ", pins is not None,
      len((pins or {}).get("directories") or []), "directories")
PY
  step "$LANG: streaming the compact form back, a record at a time"
  python3 - <<PY
import json, resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph_compact, graph_files_build
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
for section in ("nodes", "edges", "frontier"):
    old = [r for s, r in graph_files_build.stream("graph_$LANG.json") if s == section]
    new = list(graph_compact.stream_records("/work/t93/graph_$LANG.compact.json", section))
    same = old == new
    print("   %-9s old form %7d records  compact %7d records  every record equal: %s"
          % (section, len(old), len(new), same))
    if not same:
        for a, b in zip(old, new):
            if a != b:
                print("      first difference:"); print("      old", json.dumps(a)[:300]); print("      new", json.dumps(b)[:300]); break
        raise SystemExit(1)
    del old, new
print("   peak resident of the stream check %.1f MB" % peak())
PY
done

step "the frontier, COMPLETE, counted both ways"
python3 - <<'PY'
import collections, json, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph_compact, graph_files_build
for lang in ("go", "rust"):
    a = collections.Counter()
    for section, record in graph_files_build.stream("graph_%s.json" % lang):
        if section == "frontier":
            a[record["kind"]] += 1
    b = collections.Counter()
    for record in graph_compact.stream_records("/work/t93/graph_%s.compact.json" % lang, "frontier"):
        b[record["kind"]] += 1
    print("   %-5s frontier by kind, old form: %s" % (lang, json.dumps(dict(sorted(a.items())))))
    print("   %-5s frontier by kind, compact:  %s" % (lang, json.dumps(dict(sorted(b.items())))))
    print("   %-5s identical: %s   total %d records" % (lang, a == b, sum(b.values())))
PY

step "the guard, UNMODIFIED, over the two compact graphs, ONE process"
md5sum PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /work/t93/graph_go.compact.json /work/t93/graph_rust.compact.json
echo "   guard exit: $?"

echo
echo "======== lane 3 finished ========"
