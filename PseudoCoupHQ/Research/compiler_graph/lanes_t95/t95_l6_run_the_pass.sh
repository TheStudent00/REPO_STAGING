#!/usr/bin/env bash
# t95 lane 6 -- RUN THE ARCH-OPCODE-NODE PASS over all four regions.
#
# Node: hq.research.compiler_graph.graph, the heading "the arch-opcode-node
# -- a shape this node lacks, added 2026-09-05".  The pass is a METHOD OF
# THE GRAPH under the node's own name, `Graph.arch_opcode_nodes`, beside
# `coverage` and `variant_connections`.
#
# Four states per definition node, from SOURCE ALONE, no run of the
# compiler and no diary:
#   1 names_its_opcode      a call site passes a constant
#   2 one_static_hop        the argument reads a static table, hop followed
#   3 emits_opcode_dynamic  an emitter whose opcode cannot be named
#   4 emits_nothing         everything else -- the droppable set
#
# MEMORY.  Stated bound 6,144 MB, refusal named MemoryCeilingReached, and
# the method raises it itself.  Sampled first in lane t95_l2_recon.sh:
# holding all four compact graphs one after another peaked at 324.1 MB.
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
# An ARCH OPCODE (MOVQ, ADDQ) is machine form and a legitimate key -- the
# opcode index pane already keys by it.  An OPERATOR TOKEN is not.  Every
# opcode entry in the artifacts is a typed row {"text": "..."}, the shape
# task 93 settled, so a mnemonic that is a homograph of an operator-
# inventory word never sits in a row-structure position.
set -u
say() { echo; echo "======== $* ========"; }
CG=/projects/PseudoCoupHQ/Research/compiler_graph
GR=/projects/PseudoCoupGraphs
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/8] the program compiles, and the guard is UNMODIFIED"
python3 -m py_compile graph.py && echo "   graph.py compiles"
md5sum /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
git -C /projects/PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py | sed 's/^/   git says: /'
echo "   (no line above means git reports no change to the guard)"

say "[2/8] rust -- the string literals its inline-assembly path actually carries"
python3 - <<'PY'
import re, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graph as G
region = G.REGIONS["rust"]
shown = 0
for rel in ("compiler/rustc_codegen_llvm/src/asm.rs",
            "compiler/rustc_codegen_ssa/src/mir/naked_asm.rs",
            "compiler/rustc_codegen_ssa/src/mono_item.rs"):
    try:
        text = G.show_file(region.repository, region.pin, rel)
    except Exception as exc:
        print("   %s  ABSENT (%s)" % (rel, type(exc).__name__)); continue
    lits = set(re.findall(r'"((?:[^"\\\n]|\\.){1,60})"', text))
    print("   ---- %s : %d distinct string literals ----" % (rel, len(lits)))
    for one in sorted(lits)[:40]:
        print("      %s" % one)
    shown += 1
print("   files read: %d" % shown)
PY

say "[3/8] go"
python3 graph.py arch-opcode-nodes --graph "$GR/graph_go.json" \
  --out "$GR/arch_opcode_nodes_go.json" \
  --summary "$CG/arch_opcode_nodes_go_summary.json"

say "[4/8] cpp (serving c and cpp)"
python3 graph.py arch-opcode-nodes --graph "$GR/graph_cpp.json" \
  --out "$GR/arch_opcode_nodes_cpp.json" \
  --summary "$CG/arch_opcode_nodes_cpp_summary.json"

say "[5/8] rust"
python3 graph.py arch-opcode-nodes --graph "$GR/graph_rust.json" \
  --out "$GR/arch_opcode_nodes_rust.json" \
  --summary "$CG/arch_opcode_nodes_rust_summary.json"

say "[6/8] swift"
python3 graph.py arch-opcode-nodes --graph "$GR/graph_swift.json" \
  --out "$GR/arch_opcode_nodes_swift.json" \
  --summary "$CG/arch_opcode_nodes_swift_summary.json"

say "[7/8] the four-state marking, per region, every count with its population"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
ORDER = ("names_its_opcode", "one_static_hop", "emits_opcode_dynamic",
         "emits_nothing")
for lang in ("go", "cpp", "rust", "swift"):
    p = graphs_home.path("arch_opcode_nodes_%s.json" % lang)
    doc = json.load(open(p))
    pop = doc["populations"]
    print("   ==== %s ====  artifact %d bytes" % (lang, os.path.getsize(p)))
    print("      region nodes %d, definitions %d, emitter call sites %d"
          % (pop["region_nodes"], pop["definitions"],
             pop["emitter_call_sites"]))
    print("      emitter census: %s" % json.dumps(doc["emitter_census"]))
    for name in ORDER:
        print("      %-22s %6d of %d definitions"
              % (name, doc["by_state"][name], pop["definitions"]))
    print("      call sites by state: %s"
          % json.dumps(doc["by_state_of_call_sites"]))
    print("      distinct arch opcodes %d, distinct pseudo opcodes %d"
          % (doc["distinct_arch_opcodes"], doc["distinct_pseudo_opcodes"]))
    print("      shrink: %s" % json.dumps(doc["shrink"]))
    print("      cost:   %s" % json.dumps(doc["cost"]))
    if doc["unmeasured_by_absence_of_an_emitter"]:
        print("      NAMED FRONTIER: %s"
              % doc["unmeasured_by_absence_of_an_emitter"][:400])
    top = sorted(doc["inverse_index"],
                 key=lambda r: -r["definition_count"])[:15]
    print("      the fifteen opcodes emitted from the most definitions:")
    for row in top:
        print("         %-18s %d definitions"
              % (row["opcode"]["text"], row["definition_count"]))
    del doc
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[8/8] the sites whose hop did NOT resolve, named one by one"
python3 - <<'PY'
import json, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
for lang in ("go", "cpp", "rust", "swift"):
    doc = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    bad = [one for one in doc["call_sites"]
           if one["state"] == "emits_opcode_dynamic"]
    why = collections.Counter(r for one in bad for r in one["reasons"])
    print("   ==== %s ==== %d of %d call sites could not be named"
          % (lang, len(bad), len(doc["call_sites"])))
    for k, v in why.most_common():
        print("      %-58s %d" % (k[:58], v))
    partial = [one for one in doc["call_sites"]
               if one["state"] == "emits_opcode_dynamic" and one["opcodes"]]
    print("      of those, %d DO name an opcode on one branch and not the "
          "other; the opcode is recorded and the site stays dynamic"
          % len(partial))
    for one in bad[:8]:
        print("      %s:%d  %-22s %s"
              % (one["file"].split("/")[-1], one["line"], one["emitter"],
                 one["argument"][:60]))
    del doc
PY

say "lane 6 done"
