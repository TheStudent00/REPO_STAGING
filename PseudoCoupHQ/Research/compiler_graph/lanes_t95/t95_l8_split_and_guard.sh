#!/usr/bin/env bash
# t95 lane 8 -- the CORRECT three-way split against what running the
# compiler showed, the emitter definitions listed, and THE GUARD.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
#
# WHAT LANE 7 GOT WRONG, corrected here rather than quietly.  Lane 7 asked
# `per_def_visitors` whether an emitter was in "the coverage join's
# population".  It is not that population: it holds only the definitions
# that WERE entered (724 for go, 1,331 for cpp).  So its answer merely
# repeated "never entered" under a second name.  The CORE's own rule is
# the one that matters here -- "AN UNINSTRUMENTED NODE IS A FRONTIER,
# NEVER A NEVER-VISITED NODE" -- so the split has to be THREE ways:
#     entered by at least one probe
#     instrumented and entered by NONE          (never_visited_rows)
#     never instrumented -- a NAMED FRONTIER    (everything else)
# ENTERING IS STILL NOT EMITTING, in either direction.
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
GR=/projects/PseudoCoupGraphs
OP=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/t95home
mkdir -p "$HOME/Programming"
ln -sfn /sources "$HOME/Programming/Sources"
cd "$CG"

say "[1/5] the three-way split, go and cpp"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
HERE = "/projects/PseudoCoupHQ/Research/compiler_graph"
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
    print("        of them entered by >=1 of %4d probes %6d"
          % (cov["populations"]["probes"], len(entered)))
    print("        of them entered by none              %6d" % len(never))
    print("      never instrumented -- a NAMED FRONTIER %6d"
          % (defs - len(instrumented)))
    print("      --- and the static marking against it ---")
    print("      statically detected emitters           %6d of %d" % (len(emitters), defs))
    print("      emitters ENTERED by >=1 probe          %6d of %d emitters"
          % (len(emitters & entered), len(emitters)))
    print("      emitters instrumented, entered by NONE %6d of %d emitters"
          % (len(emitters & never), len(emitters)))
    print("      emitters NEVER INSTRUMENTED (frontier) %6d of %d emitters"
          % (len(emitters - instrumented), len(emitters)))
    print("      ENTERED but emitting nothing           %6d of %d entered"
          % (len(entered - emitters), len(entered)))
    print("      (entering is not emitting: a body a probe walked through "
          "may emit no instruction, and a body that emits may not have been "
          "walked by these probes.)")
    where = {}
    for row in arch["definitions_marked"]:
        if row["state"] == "emits_nothing":
            continue
        if row["id"] in entered:
            bucket = "entered"
        elif row["id"] in never:
            bucket = "instrumented, entered by none"
        else:
            bucket = "never instrumented -- a NAMED FRONTIER"
        where.setdefault((row["state"], bucket), 0)
        where[(row["state"], bucket)] += 1
    for key in sorted(where):
        print("         %-22s %-40s %d" % (key[0], key[1], where[key]))
    del arch, cov
print("   peak RSS %.1f MB"
      % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
PY

say "[2/5] go -- all 57 emitter definitions, by file, with state and label"
python3 - <<'PY'
import json, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
doc = json.load(open(graphs_home.path("arch_opcode_nodes_go.json")))
rows = [r for r in doc["definitions_marked"] if r["state"] != "emits_nothing"]
by_file = collections.Counter(r["file"] for r in rows)
print("   %d emitter definitions over %d files" % (len(rows), len(by_file)))
for f, n in by_file.most_common():
    print("      %-52s %d" % (f, n))
for r in rows:
    print("      %-46s %-22s %-28s opcodes %d"
          % ("%s:%s" % (r["file"].split("/")[-1], r["start_line"]),
             r["state"], (r["label"] or "")[:28], len(r["opcodes"])))
PY

say "[3/5] cpp -- the emitter definitions by file, and the state-1 opcode list"
python3 - <<'PY'
import json, sys, collections
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/compiler_graph")
import graphs_home
doc = json.load(open(graphs_home.path("arch_opcode_nodes_cpp.json")))
rows = [r for r in doc["definitions_marked"] if r["state"] != "emits_nothing"]
by_file = collections.Counter(r["file"] for r in rows)
print("   %d emitter definitions over %d files" % (len(rows), len(by_file)))
for f, n in by_file.most_common(25):
    print("      %-62s %d" % (f, n))
print("   the inverse index holds %d arch opcodes; twenty of them with "
      "their definitions:" % len(doc["inverse_index"]))
for row in doc["inverse_index"][:20]:
    print("      %-20s %d definitions  e.g. %s"
          % (row["opcode"]["text"], row["definition_count"],
             row["definitions"][0]))
PY

say "[4/5] every artifact this task emits, with its size and md5"
ls -l "$GR"/arch_opcode_nodes_*.json "$CG"/arch_opcode_nodes_*_summary.json
md5sum "$GR"/arch_opcode_nodes_*.json "$CG"/arch_opcode_nodes_*_summary.json

say "[5/5] THE GUARD -- unmodified, ONE process, over every artifact"
md5sum "$OP/check_no_spelling_keys.py"
git -C /projects/PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py \
  | sed 's/^/   git reports a change: /'
echo "   (nothing above means git reports no change)"
python3 "$OP/check_no_spelling_keys.py" \
  "$GR/arch_opcode_nodes_go.json" \
  "$GR/arch_opcode_nodes_cpp.json" \
  "$GR/arch_opcode_nodes_rust.json" \
  "$GR/arch_opcode_nodes_swift.json" \
  "$CG/arch_opcode_nodes_go_summary.json" \
  "$CG/arch_opcode_nodes_cpp_summary.json" \
  "$CG/arch_opcode_nodes_rust_summary.json" \
  "$CG/arch_opcode_nodes_swift_summary.json" \
  2>&1 | tee "$CG/guard_task95.txt"
echo "   guard exit: ${PIPESTATUS[0]}"
echo -n "   grep -c exempt over the transcript: "
grep -c exempt "$CG/guard_task95.txt" || true

say "lane 8 done"
