#!/usr/bin/env bash
# t93 lane 6 -- PROVE THE READERS, AND REBUILD THE SUMMARIES PANE 4 DRAWS.
#
# The graphs moved and changed form. This lane is the proof that every
# path which reads one was updated: the file-level summary builder is run
# again over the MOVED, COMPACT graphs and its output is compared with
# the summaries already tracked in this repository. If a reader had been
# left pointing at the old place or the old form, it would fail here
# rather than quietly answering nothing.
#
# It also builds the per-file coverage summary for CLANG, which pane 4's
# dynamic and directional figures need and which has never existed:
# coverage_files_build.py was written for go alone.
#
# AND IT CARRIES ONE MEASURED CORRECTION. The `entered` flag of a file
# was read off `file_runs`, which is the summary's CAPPED slice of a
# probe's path (600 runs), so a file a probe reached only after its first
# 600 runs was written down as never entered. The cap belongs to what the
# summary CARRIES, not to what it COUNTS. Both numbers are printed below.
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
# MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
# units must run op_pipeline/check_no_spelling_keys.py and refuse its own
# output on failure.
set -u
CG=PseudoCoupHQ/Research/compiler_graph
GR=PseudoCoupGraphs
cd "$CG"
git config --global --add safe.directory PseudoCoupHQ 2>/dev/null
git config --global --add safe.directory PseudoCoupGraphs 2>/dev/null
total=7; i=0
step() { i=$((i+1)); echo; echo "======== [$i/$total] $* ========"; }

step "where the graphs are now, as the code itself answers"
python3 "$CG/graphs_home.py"

step "the file-level summaries, REBUILT from the moved compact graphs"
for L in go cpp rust swift; do
  cp -p graph_${L}_files.json /work/was_${L}_files.json
  cp -p graph_${L}_defs.json  /work/was_${L}_defs.json
done
python3 graph_files_build.py go cpp rust swift
echo "   against the summaries already tracked in this repository:"
for L in go cpp rust swift; do
  if cmp -s /work/was_${L}_files.json graph_${L}_files.json; then A=IDENTICAL; else A=DIFFERENT; fi
  if cmp -s /work/was_${L}_defs.json graph_${L}_defs.json; then B=IDENTICAL; else B=DIFFERENT; fi
  printf '   %-6s graph_%s_files.json %-9s   graph_%s_defs.json %-9s\n' "$L" "$L" "$A" "$L" "$B"
done

step "a reader that reads a graph WHOLE, and passes"
python3 - <<'PY'
import resource, sys, time
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graph as G, graphs_home
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
t = time.time()
g = G.Graph.load(graphs_home.path("graph_go.json"))
print("   Graph.load over the COMPACT graph_go.json in the companion folder")
print("     region            %s" % g.pins.get("region"))
print("     nodes             %s" % "{:,}".format(len(g.static_structure["nodes"])))
print("     edges             %s" % "{:,}".format(len(g.static_structure["edges"])))
print("     frontier          %s" % "{:,}".format(len(g.frontier)))
print("     %.1f s, peak resident %.1f MB" % (time.time()-t, peak()))
one = "src/cmd/compile/internal/abi/abiutils.go#657#def#0"
print("     one node read back: %r" % (g.static_structure["nodes"].get(one),))
PY

step "report_graph.py, the node's own reader, over the moved graph"
python3 report_graph.py 2>&1 | head -40 || true

step "the per-file coverage summary: go REBUILT, and clang BUILT for the first time"
python3 - <<'PY'
import json, os
p = "PseudoCoupHQ/Research/compiler_graph/coverage_go_files.json"
was = json.load(open(p))
print("   go, as tracked before this lane:")
print("     files_never_entered %s   files_with_a_row %s"
      % (was["populations"]["files_never_entered"], was["populations"]["files_with_a_row"]))
print("     never_entered_files: %s" % json.dumps(sorted(was["never_entered_files"])))
PY
python3 coverage_files_build.py go cpp
python3 - <<'PY'
import json
for lang, name in (("go", "coverage_go_files.json"), ("cpp", "coverage_cpp_files.json")):
    d = json.load(open("PseudoCoupHQ/Research/compiler_graph/" + name))
    p = d["populations"]
    print("   %s -> %s" % (lang, name))
    print("     %s" % json.dumps(p))
    print("     never_entered_files (%d): %s"
          % (len(d["never_entered_files"]), json.dumps(sorted(d["never_entered_files"])[:20])))
PY

step "PANE 4 RENDERED, headless, for every compiler, at the present moment"
cd PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import re, resource, sys, time
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as D
def peak(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0
for lang in ("go", "cpp", "rust", "swift"):
    t = time.time()
    html = D.render(4, lang, None, None)
    figs = html.count('<svg class="dg"')
    boxes = html.count('class="dg-box')
    edges = html.count('class="dg-edge')
    arrows = html.count('class="dg-arrow')
    bad = ("error" in html[:400]) or ("Traceback" in html)
    print("   %-6s %8d bytes html   svg figures %d   boxes %5d   edges %4d   arrows %4d   %.1f s   error-frame: %s"
          % (lang, len(html), figs, boxes, edges, arrows, time.time()-t, bad))
    if bad:
        print(re.sub(r"<[^>]+>", " ", html)[:1200])
print("   NO JAVASCRIPT IN WHAT THIS PANE EMITS:")
html = D.render(4, "go", None, None)
for needle in ("<script", "javascript:", "onload=", "onerror=", " on" + "click=\"python:"):
    print("     %-24s %d" % (needle, html.count(needle)))
print("   peak resident of the whole render pass %.1f MB (page cap %d MB)"
      % (peak(), D.MEMORY_CAP_MB))
PY

step "the guards, UNMODIFIED, over every artifact this task wrote"
md5sum PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
git -C PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py
echo "   -- one process, over the four moved compact graphs and every summary:"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupGraphs/graph_go.json \
    PseudoCoupGraphs/graph_cpp.json \
    PseudoCoupGraphs/graph_rust.json \
    PseudoCoupGraphs/graph_swift.json \
    PseudoCoupGraphs/variant_connections_go.json \
    PseudoCoupGraphs/variant_connections_c.json \
    PseudoCoupGraphs/variant_connections_cpp.json \
    PseudoCoupGraphs/variant_connections_c_and_cpp.json \
    PseudoCoupGraphs/variant_connections_extended.json \
    PseudoCoupGraphs/variant_connections_rust.json \
    PseudoCoupGraphs/variant_connections_swift.json \
    "$CG/graph_go_files.json" "$CG/graph_cpp_files.json" \
    "$CG/graph_rust_files.json" "$CG/graph_swift_files.json" \
    "$CG/graph_go_defs.json" "$CG/graph_cpp_defs.json" \
    "$CG/graph_rust_defs.json" "$CG/graph_swift_defs.json" \
    "$CG/coverage_go_files.json" "$CG/coverage_cpp_files.json" \
    | tee "$CG/guard_task93.txt"
echo "   guard exit: ${PIPESTATUS[0]}"
echo "   grep -c exempt over the guard's own output: $(grep -c exempt "$CG/guard_task93.txt")"
echo "   -- the python page's own code guard, over the two files this task touched:"
python3 PseudoCoupHQ/Research/op_pipeline/check_dashboard_py_no_spelling.py \
    PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.py \
    PseudoCoupHQ/Research/op_pipeline/dashboard_graph_draw.py \
    PseudoCoupHQ/Research/compiler_graph/graph_compact.py \
    PseudoCoupHQ/Research/compiler_graph/graphs_home.py
echo "   py-guard exit: $?"

echo
echo "======== lane 6 finished ========"
