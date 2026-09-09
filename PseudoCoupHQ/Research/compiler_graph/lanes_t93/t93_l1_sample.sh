#!/usr/bin/env bash
# t93 lane 1 -- SAMPLE AND MEASURE, nothing is written into either tree.
#
# Task 93 moves the compiler graphs to PseudoCoupGraphs, stores them in a
# compact form, and draws them in pane 4.  Three things have to be
# measured before any of that is written:
#
#   1. THE ROUND-TRIP ASSUMPTION.  The compact form is only admissible if
#      the old form can be rebuilt from it BYTE FOR BYTE.  That rests on
#      `json.dumps(document, indent=1)` reproducing the file graph.py
#      wrote.  Measured here on graph_go.json, md5 against md5, before a
#      compactor exists.
#   2. THE MEMORY COST of simply holding one graph, and of streaming it a
#      record at a time -- the two shapes the compactor may take.  The
#      stated ceiling for this task is 6,144 MB and the abort is named
#      MemoryCeilingReached.
#   3. WHAT WOULD MOVE, and what would not, with every size, so the move
#      is a listed decision rather than a wildcard.
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
#
# This lane groups nothing and pairs nothing.  It counts bytes.
set -u
say() { echo; echo "======== $* ========"; }
CG=PseudoCoupHQ/Research/compiler_graph
GR=PseudoCoupGraphs
cd "$CG"

say "[1/6] the instance, and that the graphs mount is present and writable"
python3 -c "import sys;print('   python',sys.version.split()[0])"
ls -la "$GR" || echo "   MOUNT MISSING"
touch "$GR/.t93_write_probe" && echo "   write probe OK" && rm -f "$GR/.t93_write_probe"
git -C "$GR" remote -v | sed 's/^/   remote: /' ; echo "   remote lines above (none expected, by design)"
git -C "$GR" log --oneline | head -3 | sed 's/^/   /'

say "[2/6] sizes of every artifact this task speaks about"
for f in graph_go.json graph_cpp.json graph_rust.json graph_swift.json \
         graph_go2.json graph_go3.json graph_go4.json graph_go_lapone.json \
         graph_cpp2.json graph_cpp3.json \
         coverage_go.json coverage_go2.json coverage_c.json coverage_cpp.json \
         coverage_c_and_cpp.json coverage_extended.json \
         super_ops_go.json super_ops_cpp.json \
         variant_connections_go.json variant_connections_c.json \
         variant_connections_cpp.json variant_connections_c_and_cpp.json \
         variant_connections_extended.json variant_connections_rust.json \
         variant_connections_swift.json ; do
  if [ -f "$f" ]; then printf '   %-38s %14d bytes\n' "$f" "$(stat -c%s "$f")";
  else printf '   %-38s ABSENT\n' "$f"; fi
done
echo "   diaries:"; du -sb diaries/* 2>/dev/null | sed 's/^/     /'
echo "   whole folder:"; du -sb . | sed 's/^/     /'

say "[3/6] THE ROUND-TRIP ASSUMPTION, measured on graph_go.json"
python3 - <<'PY'
import hashlib, json, resource, time
SRC = "graph_go.json"
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
raw = open(SRC, "rb").read()
print("   original bytes            %d" % len(raw))
print("   original md5              %s" % hashlib.md5(raw).hexdigest())
print("   ends with a newline?      %r" % raw.endswith(b"\n"))
t = time.time()
doc = json.loads(raw.decode())
print("   json.loads               %.1f s, peak %.1f MB" % (time.time()-t, peak()))
t = time.time()
again = json.dumps(doc, indent=1).encode()
print("   json.dumps(indent=1)     %.1f s, peak %.1f MB" % (time.time()-t, peak()))
print("   rebuilt bytes             %d" % len(again))
print("   rebuilt md5               %s" % hashlib.md5(again).hexdigest())
print("   BYTE FOR BYTE IDENTICAL:  %s" % (again == raw))
if again != raw:
    for i in range(min(len(again), len(raw))):
        if again[i] != raw[i]:
            print("   first difference at byte %d" % i)
            print("   original: %r" % raw[max(0,i-60):i+60])
            print("   rebuilt : %r" % again[max(0,i-60):i+60])
            break
    print("   trailing of original: %r" % raw[-40:])
    print("   trailing of rebuilt : %r" % again[-40:])
del doc, again, raw
print("   peak resident of this step %.1f MB" % peak())
PY

say "[4/6] THE SHAPES, and what a compact form would cost -- go"
python3 - <<'PY'
import collections, json, resource
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
doc = json.load(open("graph_go.json"))
for section in ("nodes", "edges", "frontier"):
    rows = doc[section]
    shapes = collections.Counter(tuple(r.keys()) for r in rows)
    print("   %s: %d rows, %d distinct key orders" % (section, len(rows), len(shapes)))
    for shape, many in shapes.most_common():
        print("      %8d  %s" % (many, ", ".join(shape)))
        sample = next(r for r in rows if tuple(r.keys()) == shape)
        types = {}
        for key in shape:
            kinds = set()
            for r in rows:
                if tuple(r.keys()) != shape: continue
                v = r[key]
                kinds.add(type(v).__name__)
            types[key] = sorted(kinds)
        print("               types: %s" % types)
        print("               distinct values per field: %s"
              % {k: len({json.dumps(r[k], sort_keys=True) for r in rows
                         if tuple(r.keys()) == shape}) for k in shape})
print("   parse_errors: %r" % (doc.get("parse_errors") if not isinstance(doc.get("parse_errors"), list) else len(doc["parse_errors"])))
print("   top-level key order: %s" % list(doc.keys()))
print("   peak resident %.1f MB" % peak())
PY

say "[5/6] the cpp instrumented-target record, for a per-file coverage summary"
ls -la t81/ 2>/dev/null | head -20
for f in t81/inject_report_cpp2.json t72/diary_targets_all.json; do
  if [ -f "$f" ]; then
    printf '   %-40s %12d bytes\n' "$f" "$(stat -c%s "$f")"
    python3 -c "
import json,sys
d=json.load(open('$f'))
print('     top keys:', list(d)[:14] if isinstance(d,dict) else ('list of %d'%len(d)))
if isinstance(d,dict):
    for k in list(d)[:14]:
        v=d[k]
        print('      ',k, type(v).__name__, (len(v) if isinstance(v,(list,dict)) else repr(v)[:80]))
"
  else printf '   %-40s ABSENT\n' "$f"; fi
done

say "[6/6] who names a graph path in live code (lane scripts are records, not live)"
grep -rn "graph_go\.json\|graph_cpp\.json\|graph_rust\.json\|graph_swift\.json\|coverage_go2\.json\|coverage_c_and_cpp\.json\|coverage_extended\.json\|super_ops_go\.json\|super_ops_cpp\.json\|variant_connections_\|\"diaries\|/diaries" \
  --include=*.py PseudoCoupHQ/Research/compiler_graph PseudoCoupHQ/Research/op_pipeline \
  | grep -v "^.*lanes" | sed 's/^/   /' | head -60
echo
echo "======== lane 1 finished ========"
