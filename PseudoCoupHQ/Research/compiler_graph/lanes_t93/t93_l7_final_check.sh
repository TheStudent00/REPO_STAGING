#!/usr/bin/env bash
# t93 lane 7 -- THE FINAL CHECK. Nothing is written; everything is read
# back and printed so the report's claims can be compared with the tree.
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
git config --global --add safe.directory PseudoCoupHQ 2>/dev/null
git config --global --add safe.directory PseudoCoupGraphs 2>/dev/null
total=5; i=0
step() { i=$((i+1)); echo; echo "======== [$i/$total] $* ========"; }

step "the planning tree still checks"
if [ -f PlanPlan/check_plans.py ]; then
  python3 PlanPlan/check_plans.py PseudoCoupHQ 2>&1 | tail -25
else
  ls PlanPlan | head -20
fi

step "the JavaScript route and the engine, untouched"
echo "   git diff over dashboard.html and every dashboard_pane*.js:"
git -C PseudoCoupHQ diff -- Research/op_pipeline/dashboard.html \
    'Research/op_pipeline/dashboard_pane*.js' | tee /work/js.diff | wc -l
echo "   (0 lines above means untouched)"
echo "   the guard itself, unmodified:"
git -C PseudoCoupHQ status --porcelain \
    Research/op_pipeline/check_no_spelling_keys.py
md5sum PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py

step "the sizes, read off disk one last time"
echo "   the four graphs, in the companion folder, compact:"
for L in go rust swift cpp; do
  printf '     graph_%-6s %12d bytes  compact=%s\n' "$L.json" \
    "$(stat -c%s "$GR/graph_$L.json")" \
    "$(head -c 200 "$GR/graph_$L.json" | grep -c graph-compact-1)"
done
echo "   folders:"
du -sb "$CG" "$GR" | sed 's/^/     /'
echo "   the superseded laps still here, as records:"
ls -la "$CG"/graph_go2.json "$CG"/graph_go3.json "$CG"/graph_go4.json \
   "$CG"/graph_go_lapone.json "$CG"/graph_cpp2.json "$CG"/graph_cpp3.json \
   "$CG"/coverage_go.json 2>&1 | sed 's/^/     /'

step "pane 4, rendered once more for every compiler, after every edit"
cd PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as D
for lang in ("go", "cpp", "rust", "swift"):
    html = D.render(4, lang, None, None)
    print("   %-6s svg %d  boxes %5d  arcs %4d  arrows %4d  script tags %d  error-frame %s"
          % (lang, html.count('<svg class="dg"'), html.count('class="dg-box'),
             html.count('class="dg-edge'), html.count('class="dg-arrow'),
             html.count("<script"), "Traceback" in html))
print("   peak resident %.1f MB (cap %d MB)"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0, D.MEMORY_CAP_MB))
PY

step "the guard, UNMODIFIED, one process, one more time"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$GR"/graph_go.json "$GR"/graph_cpp.json "$GR"/graph_rust.json \
    "$GR"/graph_swift.json "$GR"/variant_connections_*.json \
    "$CG"/graph_*_files.json "$CG"/graph_*_defs.json \
    "$CG"/coverage_go_files.json "$CG"/coverage_cpp_files.json
echo "   guard exit: $?"

echo
echo "======== lane 7 finished ========"
