#!/usr/bin/env bash
# t95 lane 9 -- THE RERUN after the unmodified guard REFUSED go's artifact,
# and the whole verification pass.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# WHAT THE GUARD CAUGHT, in lane t95_l8_split_and_guard.sh, and it was a
# real finding rather than a false alarm:
#
#     FAIL arch_opcode_nodes_go.json -- 1 spelling-keyed place(s)
#          $.call_sites[223].argument
#              operator token 'as' on a structure field -- this is a
#              grouping/row key, not a per-unit label
#
# go's own emitter is `func (s *State) Prog(as obj.As)`, and the call
# sites that hand the parameter straight through write `s.Prog(as)`. The
# argument's TEXT is therefore the string `as`, which is one of the 91
# operator tokens the corpus probes -- exactly the hazard task 93 hit with
# `new` and `not`, and exactly the hazard the brief for this task named in
# advance. THE RULED REMEDY IS THE TYPED SHAPE, never a whitelist and
# never a rename: the argument (and the name of every table a hop read)
# now rides as `{"text": "..."}`, a VALUE on a row, the same shape the
# opcodes already had.
#
# AND THE STAGE NOW REFUSES ITS OWN OUTPUT. `Graph.arch_opcode_nodes` runs
# the unmodified guard over the file it just wrote and raises
# SpellingKeyRefused rather than returning, which is the ban's own
# mechanical-guard requirement.
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
CG=PseudoCoupHQ/Research/compiler_graph
GR=PseudoCoupGraphs
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/7] the program compiles, and the guard is UNMODIFIED"
python3 -m py_compile graph.py && echo "   graph.py compiles"
md5sum "$OP/check_no_spelling_keys.py"
git -C PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py \
  | sed 's/^/   git reports a change: /'
echo "   (nothing above means git reports no change to the guard)"

say "[2/7] the four regions, rerun; the pass now refuses its own output"
i=0
for lang in go cpp rust swift; do
  i=$((i+1))
  echo "   [$i/4] $lang"
  python3 graph.py arch-opcode-nodes --graph "$GR/graph_${lang}.json" \
    --out "$GR/arch_opcode_nodes_${lang}.json" \
    --summary "$CG/arch_opcode_nodes_${lang}_summary.json" || exit 1
done

say "[3/7] the four-state marking, per region, every count with its population"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graphs_home
ORDER = ("names_its_opcode", "one_static_hop", "emits_opcode_dynamic",
         "emits_nothing")
for lang in ("go", "cpp", "rust", "swift"):
    p = graphs_home.path("arch_opcode_nodes_%s.json" % lang)
    doc = json.load(open(p))
    pop = doc["populations"]
    print("   ==== %s ====  artifact %d bytes" % (lang, os.path.getsize(p)))
    print("      region nodes %d, definitions %d, emitter call sites %d, "
          "sites outside any definition %d"
          % (pop["region_nodes"], pop["definitions"],
             pop["emitter_call_sites"],
             pop["emitter_call_sites_outside_any_definition"]))
    print("      emitter census: %s" % json.dumps(doc["emitter_census"]))
    total = 0
    for name in ORDER:
        total += doc["by_state"][name]
        print("      %-22s %6d of %d definitions"
              % (name, doc["by_state"][name], pop["definitions"]))
    print("      the four states sum to %d against a population of %d"
          % (total, pop["definitions"]))
    print("      of the state-1 definitions, %d name at least one ARCH "
          "opcode and %d name only PSEUDO opcodes"
          % (doc["names_its_opcode_with_at_least_one_arch_opcode"],
             doc["names_its_opcode_naming_only_pseudo_opcodes"]))
    print("      call sites by state: %s"
          % json.dumps(doc["by_state_of_call_sites"]))
    print("      distinct arch opcodes %d, distinct pseudo opcodes %d"
          % (doc["distinct_arch_opcodes"], doc["distinct_pseudo_opcodes"]))
    print("      shrink: %s" % json.dumps(doc["shrink"]))
    print("      cost:   %s" % json.dumps(doc["cost"]))
    print("      the pass's own guard verdict: %s"
          % json.dumps(doc.get("spelling_guard", {})))
    del doc
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[4/7] the three-way split against what RUNNING the compiler showed"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graphs_home
HERE = "PseudoCoupHQ/Research/compiler_graph"
for lang, name in (("go", "coverage_go_files.json"),
                   ("cpp", "coverage_cpp_files.json")):
    arch = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    cov = json.load(open(os.path.join(HERE, name)))
    entered = set(cov["per_def_visitors"])
    never = {row["id"] for row in cov["never_visited_rows"]}
    instrumented = entered | never
    emitters = {row["id"] for row in arch["definitions_marked"]
                if row["state"] != "emits_nothing"}
    defs = arch["populations"]["definitions"]
    print("   ==== %s ====" % lang)
    print("      definitions in the region              %6d" % defs)
    print("      instrumented bodies (entry hook placed)%6d" % len(instrumented))
    print("        entered by >=1 of %4d probes         %6d"
          % (cov["populations"]["probes"], len(entered)))
    print("        entered by none                      %6d" % len(never))
    print("      never instrumented -- a NAMED FRONTIER %6d"
          % (defs - len(instrumented)))
    print("      statically detected emitters           %6d of %d" % (len(emitters), defs))
    print("      emitters ENTERED by >=1 probe          %6d of %d" % (len(emitters & entered), len(emitters)))
    print("      emitters instrumented, entered by NONE %6d of %d" % (len(emitters & never), len(emitters)))
    print("      emitters NEVER INSTRUMENTED (frontier) %6d of %d" % (len(emitters - instrumented), len(emitters)))
    print("      ENTERED but emitting nothing           %6d of %d entered"
          % (len(entered - emitters), len(entered)))
    where = {}
    for row in arch["definitions_marked"]:
        if row["state"] == "emits_nothing":
            continue
        bucket = ("entered" if row["id"] in entered else
                  "instrumented, entered by none" if row["id"] in never else
                  "never instrumented -- a NAMED FRONTIER")
        where[(row["state"], bucket)] = where.get((row["state"], bucket), 0) + 1
    for key in sorted(where):
        print("         %-22s %-40s %d" % (key[0], key[1], where[key]))
    del arch, cov
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[5/7] the shrink, stated as a percentage of each graph"
python3 - <<'PY'
import json, sys
sys.path.insert(0, "PseudoCoupHQ/Research/compiler_graph")
import graphs_home
print("   | region | definitions | emitters | +direct callers | +all callers | "
      "emits nothing | dropped |")
print("   |---|---|---|---|---|---|---|")
for lang in ("go", "cpp", "rust", "swift"):
    d = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    s = d["shrink"]
    n = s["definitions"]
    print("   | %s | %d | %d (%.1f%%) | %d (%.1f%%) | %d (%.1f%%) | %d | %.1f%% |"
          % (lang, n, s["emitters_only"], 100.0 * s["emitters_only"] / n,
             s["emitters_and_their_direct_callers"],
             100.0 * s["emitters_and_their_direct_callers"] / n,
             s["emitters_and_all_their_callers"],
             100.0 * s["emitters_and_all_their_callers"] / n,
             d["by_state"]["emits_nothing"],
             100.0 * d["by_state"]["emits_nothing"] / n))
    del d
print()
print("   the caller closure is bounded by the graph's own RESOLVED `calls`")
print("   edges; every unresolved call is already a named frontier of the")
print("   graph, and those counts are:")
for lang in ("go", "cpp", "rust", "swift"):
    doc = json.load(open(graphs_home.path("graph_%s.json" % lang)))
    print("      %-6s frontier by kind: %s"
          % (lang, json.dumps(doc["counts"]["frontier_by_kind"])))
    del doc
PY

say "[6/7] every artifact this task emits, with its size and md5"
ls -l "$GR"/arch_opcode_nodes_*.json "$CG"/arch_opcode_nodes_*_summary.json
md5sum "$GR"/arch_opcode_nodes_*.json "$CG"/arch_opcode_nodes_*_summary.json

say "[7/7] THE GUARD -- unmodified, ONE process, over every artifact"
python3 "$OP/check_no_spelling_keys.py" \
  "$GR/arch_opcode_nodes_go.json" \
  "$GR/arch_opcode_nodes_cpp.json" \
  "$GR/arch_opcode_nodes_rust.json" \
  "$GR/arch_opcode_nodes_swift.json" \
  "$CG/arch_opcode_nodes_go_summary.json" \
  "$CG/arch_opcode_nodes_cpp_summary.json" \
  "$CG/arch_opcode_nodes_rust_summary.json" \
  "$CG/arch_opcode_nodes_swift_summary.json" \
  > "$CG/guard_task95.txt" 2>&1
echo "   guard exit: $?"
cat "$CG/guard_task95.txt"
echo -n "   grep -c exempt over the transcript: "
grep -c exempt "$CG/guard_task95.txt" || true

say "lane 9 done"
