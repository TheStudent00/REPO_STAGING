#!/usr/bin/env bash
# t93 lane 4 -- THE COMPACT FORM OVER ALL FOUR GRAPHS, with the two
# defects lane 3 found fixed, and nothing replaced yet.
#
# WHAT LANE 3 FOUND, and this lane checks is gone:
#   * the head read broke. `provenance` was written before `pins` and its
#     `expanded_key_order` list carries the words "pins" and "counts", so
#     viewer_build.carve -- which takes the FIRST occurrence of a key --
#     landed on the list. The verbatim members now come first, in the
#     original's own order.
#   * the unmodified guard REFUSED both compact graphs, 7 places each:
#     source identifiers `new`, `and`, `not`, `delete`, `in`, `as`, `or`,
#     `with`, `is`, `xor` are in the 91-token operator inventory and were
#     written as BARE LIST ELEMENTS in the string table. Every entry is
#     now a row `{"text": "..."}` -- the token as a VALUE beside an
#     opaque position, which is the shape the CORE ratified for the four
#     x86 mnemonics that are homographs, and the shape the ORIGINAL graph
#     already has at `"detail": "new"`. NO EXEMPTION WAS ADDED and the
#     guard is byte-identical.
#
# Ceiling 6,144 MB, abort named MemoryCeilingReached.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
# campaign's cross-language matrix (caught by the owner 2026-08-24);
# (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
# brief itself reintroduced it as "same-operator pairs"). MECHANICAL
# GUARD REQUIRED: every pipeline stage that groups or pairs units must
# run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
# refuse its own output on failure.
set -u
say() { echo; echo "======== $* ========"; }
CG=/projects/PseudoCoupHQ/Research/compiler_graph
cd "$CG"
rm -rf /work/t93; mkdir -p /work/t93
total=6; i=0
step() { i=$((i+1)); echo; echo "======== [$i/$total] $* ========"; }

for LANG in go rust swift cpp; do
  step "$LANG"
  python3 graph_compact.py compact --graph graph_$LANG.json \
      --out /work/t93/graph_$LANG.compact.json || exit 1
  python3 graph_compact.py expand --compact /work/t93/graph_$LANG.compact.json \
      --out /work/t93/rebuilt_$LANG.json --verify || exit 1
  echo "   THE ROUND-TRIP DIFF, byte for byte:"
  if cmp graph_$LANG.json /work/t93/rebuilt_$LANG.json; then
    echo "     cmp graph_$LANG.json rebuilt_$LANG.json -> IDENTICAL, 0 differing bytes"
  else
    echo "     cmp -> DIFFERENT. refusing"; exit 1
  fi
  diff -q graph_$LANG.json /work/t93/rebuilt_$LANG.json \
      && echo "     diff -q -> the files are identical"
  BEFORE=$(stat -c%s graph_$LANG.json); AFTER=$(stat -c%s /work/t93/graph_$LANG.compact.json)
  python3 -c "print('     SIZE  graph_$LANG.json  before %14d  after %13d  (%.1f%% of the original, %.1fx smaller)' % ($BEFORE,$AFTER,100.0*$AFTER/$BEFORE,$BEFORE/float($AFTER)))"
  echo "   the 256 KB head read, which every existing reader does:"
  python3 - <<PY
import sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
import viewer_build
head = open("/work/t93/graph_$LANG.compact.json").read(262144)
counts = viewer_build.carve(head, "counts"); pins = viewer_build.carve(head, "pins")
print("     counts carved:", counts is not None, "nodes", (counts or {}).get("nodes"),
      "edges", (counts or {}).get("edges"), "frontier", (counts or {}).get("frontier"),
      "files", (counts or {}).get("files"))
print("     pins carved:  ", pins is not None, len((pins or {}).get("directories") or []), "directories")
assert counts and pins, "the head read must keep working"
PY
  echo "   every record of every section, old form against compact:"
  python3 - <<PY
import resource, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph_compact, graph_files_build
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
for section in ("nodes", "edges", "frontier"):
    old = [r for s, r in graph_files_build.stream("graph_$LANG.json") if s == section]
    new = list(graph_compact.stream_records("/work/t93/graph_$LANG.compact.json", section))
    print("     %-9s old %8d  compact %8d  every record equal: %s"
          % (section, len(old), len(new), old == new))
    assert old == new
    del old, new
print("     peak resident of the record comparison %.1f MB" % peak())
PY
done

step "the frontier is COMPLETE in every compact graph -- counted both ways"
python3 - <<'PY'
import collections, json, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph_compact, graph_files_build
for lang in ("go", "rust", "swift", "cpp"):
    a = collections.Counter(); b = collections.Counter()
    for section, record in graph_files_build.stream("graph_%s.json" % lang):
        if section == "frontier": a[record["kind"]] += 1
    for record in graph_compact.stream_records("/work/t93/graph_%s.compact.json" % lang, "frontier"):
        b[record["kind"]] += 1
    print("   %-6s old form %s" % (lang, json.dumps(dict(sorted(a.items())))))
    print("   %-6s compact  %s" % (lang, json.dumps(dict(sorted(b.items())))))
    print("   %-6s identical: %s   total %d frontier records" % (lang, a == b, sum(b.values())))
PY

step "the guard, UNMODIFIED, over all four compact graphs, ONE process"
md5sum /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
git -C /projects/PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /work/t93/graph_go.compact.json /work/t93/graph_rust.compact.json \
    /work/t93/graph_swift.compact.json /work/t93/graph_cpp.compact.json
echo "   guard exit: $?"
echo "   grep -c exempt over the guard: $(grep -c exempt /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py)"

echo
echo "======== lane 4 finished ========"
