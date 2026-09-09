#!/usr/bin/env bash
# t95 lane 7 -- RERUN the arch-opcode-node pass after three defects the
# first run exposed, then COMPARE the statically detected emitter set with
# what RUNNING the compiler showed.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# THE THREE DEFECTS, from lane t95_l6_run_the_pass.sh, each fixed in
# graph.py and each named here so the correction is on the record:
#   1. A DECLARATION WAS READ AS A CALL SITE.  `func opregreg(s
#      *ssagen.State, op obj.As, ...)` in go and `fn inline_asm_call(&mut
#      self, asm: &str, ...)` in rust both match their opener; grading
#      either reported the PARAMETER as a dynamic opcode and invented an
#      emitter that emits nothing.  Declarations are now skipped and the
#      skipped ones are written onto the artifact.
#   2. THE FOUR STATES DID NOT SUM to the definition population.  A
#      definition whose only sites emit nothing (swift's three empty
#      inline-assembly templates) was counted in neither `emits_nothing`
#      nor anything else: 1 + 0 + 1 + 10,083 = 10,085 against 10,088
#      definitions.  The pass now asserts the partition.
#   3. THE EMITTER/TABLE ROLE was derived from a broken split of the
#      declaration line, so go's own `(*State).Prog` was labelled a table.
#      The role is now read from the parameter list and the return type.
#
# THE COMPARISON.  `coverage` says 724 of 1,859 go definitions and 1,331
# of 8,871 instrumented clang bodies were ENTERED by a probe.  ENTERING IS
# NOT EMITTING and this lane must not blur them: a body a probe walked
# through may emit nothing, and a body that emits may never have been
# walked by these 590 and 1,380 probes.  Both exclusive parts are reported.
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
# The comparison below pairs a STATIC MARKING with a DYNAMIC ENTRY SET by
# NODE IDENTITY -- the graph's own machine coordinate `file#line#kind#n`.
# No token takes part in the pairing.
set -u
say() { echo; echo "======== $* ========"; }
CG=/projects/PseudoCoupHQ/Research/compiler_graph
GR=/projects/PseudoCoupGraphs
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/6] the program compiles"
python3 -m py_compile graph.py && echo "   graph.py compiles"

say "[2/6] the four regions, rerun"
i=0
for lang in go cpp rust swift; do
  i=$((i+1))
  echo "   [$i/4] $lang"
  python3 graph.py arch-opcode-nodes --graph "$GR/graph_${lang}.json" \
    --out "$GR/arch_opcode_nodes_${lang}.json" \
    --summary "$CG/arch_opcode_nodes_${lang}_summary.json" || exit 1
done

say "[3/6] the four-state marking, per region, every count with its population"
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
    print("      region nodes %d, definitions %d, emitter call sites %d, "
          "sites outside any definition %d"
          % (pop["region_nodes"], pop["definitions"],
             pop["emitter_call_sites"],
             pop["emitter_call_sites_outside_any_definition"]))
    print("      emitter census: %s" % json.dumps(doc["emitter_census"]))
    print("      declarations skipped (not call sites): %s"
          % json.dumps(doc["declarations_skipped_because_they_are_not_call_sites"]))
    total = 0
    for name in ORDER:
        total += doc["by_state"][name]
        print("      %-22s %6d of %d definitions"
              % (name, doc["by_state"][name], pop["definitions"]))
    print("      the four states sum to %d, the definition population is %d"
          % (total, pop["definitions"]))
    print("      call sites by state: %s"
          % json.dumps(doc["by_state_of_call_sites"]))
    print("      distinct arch opcodes %d, distinct pseudo opcodes %d"
          % (doc["distinct_arch_opcodes"], doc["distinct_pseudo_opcodes"]))
    print("      state-3 definitions naming arch opcodes elsewhere in their "
          "own body: %d  (CO-LOCATION, not resolution)"
          % doc["state_three_definitions_that_name_arch_opcodes_elsewhere_"
                "in_their_own_body"])
    print("      shrink: %s" % json.dumps(doc["shrink"]))
    print("      cost:   %s" % json.dumps(doc["cost"]))
    print("      reasons a site could not be named: %s"
          % json.dumps(doc["hop_not_resolved_by_reason"]))
    del doc
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[4/6] go and swift -- the emitter declarations, with the role read off each"
python3 - <<'PY'
import json, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
for lang in ("go", "cpp", "rust", "swift"):
    doc = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    rows = doc["emitter_declarations"]
    print("   ==== %s ==== %d declarations of the arch opcode type"
          % (lang, len(rows)))
    for row in rows:
        print("      %-46s %s" % ("%s:%d" % (row["file"].split("/")[-1],
                                             row["line"]), row["role"]))
        print("         %s" % row["declaration"][:110])
    del doc
PY

say "[5/6] swift and rust -- every call site, printed whole; these are small"
python3 - <<'PY'
import json, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
for lang in ("rust", "swift"):
    doc = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    print("   ==== %s ==== %d call sites" % (lang, len(doc["call_sites"])))
    for one in doc["call_sites"]:
        print("      %s:%d  %-16s state=%-22s opcodes=%s"
              % (one["file"], one["line"], one["emitter"], one["state"],
                 [k["text"] for k in one["opcodes"]]))
        print("         argument: %s" % one["argument"][:100])
        print("         reasons:  %s" % one["reasons"])
        print("         definition: %s" % one["definition"])
    print("   NAMED FRONTIERS: %s"
          % json.dumps(doc["named_frontiers"], indent=1)[:1600])
    del doc
PY

say "[6/6] the static emitter set against what RUNNING the compiler showed"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
HERE = "/projects/PseudoCoupHQ/Research/compiler_graph"

for lang, coverage_name in (("go", "coverage_go_files.json"),
                            ("cpp", "coverage_cpp_files.json")):
    arch = json.load(open(graphs_home.path("arch_opcode_nodes_%s.json" % lang)))
    cov = json.load(open(os.path.join(HERE, coverage_name)))
    visitors = cov["per_def_visitors"]
    print("   ==== %s ====" % lang)
    print("      coverage populations: %s" % json.dumps(cov["populations"]))
    sample = list(visitors.items())[:2]
    print("      per_def_visitors is %d rows; two of them: %s"
          % (len(visitors), json.dumps(sample)[:220]))
    entered = {k for k, v in visitors.items()
               if (v if isinstance(v, int) else len(v)) > 0}
    emitters = {row["id"] for row in arch["definitions_marked"]
                if row["state"] != "emits_nothing"}
    both = emitters & entered
    print("      ENTERING IS NOT EMITTING. The two sets, by node identity:")
    print("      statically detected emitters      %6d of %d definitions"
          % (len(emitters), arch["populations"]["definitions"]))
    print("      entered by at least one probe     %6d of %d definitions"
          % (len(entered), arch["populations"]["definitions"]))
    print("      in BOTH                           %6d" % len(both))
    print("      emitters NEVER entered by a probe %6d of %d emitters"
          % (len(emitters - entered), len(emitters)))
    print("      entered but emitting NOTHING      %6d of %d entered"
          % (len(entered - emitters), len(entered)))
    by_state = {}
    for row in arch["definitions_marked"]:
        if row["state"] == "emits_nothing":
            continue
        key = (row["state"], row["id"] in entered)
        by_state[key] = by_state.get(key, 0) + 1
    print("      per state, entered or not:")
    for key in sorted(by_state):
        print("         %-22s entered=%-5s %d" % (key[0], key[1], by_state[key]))
    missing = [row for row in arch["definitions_marked"]
               if row["state"] != "emits_nothing" and row["id"] not in visitors]
    print("      emitters that are not in the coverage join's population at "
          "all (an uninstrumented body is a NAMED FRONTIER, never a "
          "never-entered one): %d" % len(missing))
    for row in missing[:12]:
        print("         %s:%s  %s" % (row["file"].split("/")[-1],
                                      row["start_line"], row["state"]))
    del arch, cov, visitors
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "lane 7 done"
