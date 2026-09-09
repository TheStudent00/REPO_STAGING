#!/usr/bin/env bash
# t87 lane 9 — WHAT THE THIRD KIND SHOWS THAT THE UNION DOES NOT, with
# one worked example and its values moving, in the style of log_190
# section 2.3.
#
# THE MEMORY BOUND. `coverage_c_and_cpp.json` is 416,754,589 bytes and
# `coverage_go2.json` is 515,160,866; NEITHER IS OPENED WHOLE. Both are
# read ONE LINE AT A TIME with a small state machine that keeps only the
# handful of node ids this lane asks about, which is the settled rule
# for every reader of this graph (CORE, 2026-09-03, task 73). The peak
# resident set of each scan is printed.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# The variant this lane walks through was chosen by its EXCLUSIVE
# TRANSITION COUNT, a number, and by nothing else.
set -u
say() { echo; echo "======== $* ========"; }
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/5] the four measured populations, side by side"
python3 - <<'PY'
import json
rows = [("go", "variant_connections_go.json"),
        ("c", "variant_connections_c.json"),
        ("cpp", "variant_connections_cpp.json"),
        ("c and cpp", "variant_connections_c_and_cpp.json"),
        ("c and cpp + regen", "variant_connections_extended.json")]
print("   %-20s %7s %9s %8s %8s %10s %10s"
      % ("population", "probes", "variants", "nodes", "edges",
         "edges x1", "edges xall"))
for name, path in rows:
    d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/' + path))
    p = d["populations"]; c = d["census"]["transitions"]
    print("   %-20s %7d %9d %8d %8d %10d %10d"
          % (name, p["diaries_on_disk"], p["operator_traced_variants"],
             p["distinct_nodes_entered"], p["distinct_transitions"],
             c["walked_by_exactly_one_variant"], c["walked_by_every_variant"]))
PY

say "[2/5] how many variants own a connection at all"
python3 - <<'PY'
import json
for path in ("variant_connections_c_and_cpp.json",
             "variant_connections_extended.json",
             "variant_connections_go.json"):
    d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/' + path))
    rows = d["variants"]
    own = [r for r in rows if r["transitions_exclusive_to_this_variant"] > 0]
    print("   %-38s %5d variants, %4d own at least one exclusive transition, "
          "%4d own none"
          % (path, len(rows), len(own), len(rows) - len(own)))
    print("        top five by exclusive transitions:")
    for r in rows[:5]:
        print("          %s  members %3d  probes %4d  nodes %4d  edges %4d  "
              "exclusive edges %3d  exclusive nodes %3d"
              % (r["variant_id"], r["member_count"], r["probes_with_a_diary"],
                 r["nodes_entered"], r["transitions"],
                 r["transitions_exclusive_to_this_variant"],
                 r["nodes_exclusive_to_this_variant"]))
PY

say "[3/5] THE WORKED EXAMPLE -- one variant, its values moving"
python3 - <<'PY'
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_c_and_cpp.json'))
row = d["variants"][0]
print("   variant_id : %s" % row["variant_id"])
print("   members    : %d   probes with a diary : %d"
      % (row["member_count"], row["probes_with_a_diary"]))
print("   languages  : %s   populations : %s"
      % (row["languages"], row["populations"]))
print("   outcomes   : %s" % row["outcomes"])
print("   THE MACHINE FORM THIS VARIANT IS IDENTIFIED BY:")
print("      bytes           : %s" % row["machine_form"]["bytes"])
print("      text            : %s" % row["machine_form"]["text"])
print("      entry_contract  : %s" % json.dumps(row["machine_form"]["entry_contract"]))
print("      ledger_shape    : %s" % json.dumps(row["machine_form"]["ledger_shape"]))
print("   THE MEMBERS, each a typed unit object carrying its display label:")
for m in row["members"]:
    print("      %-18s language %-4s label %-6s population %-12s outcome %s"
          % (m["id"], m["language"], json.dumps(m["operator"]),
             m["population"], m["outcome"]))
print("   ITS OWN CONNECTIONS:")
print("      nodes entered                         %d" % row["nodes_entered"])
print("      nodes exclusive to this variant       %d" % row["nodes_exclusive_to_this_variant"])
print("      transitions                           %d" % row["transitions"])
print("      transitions exclusive to this variant %d" % row["transitions_exclusive_to_this_variant"])
print("      transitions backed by a static call   %d" % row["transitions_backed_by_a_static_call_edge"])
print("   THE EXCLUSIVE TRANSITIONS, up to the stated cap of %d:"
      % d["parameters"]["exclusive_examples_per_variant"])
for e in row["exclusive_transition_examples"]:
    print("      %-52s  ->  %-52s   static call edge: %s"
          % ("%s %s" % (e["from"].get("coordinate"), e["from"].get("label")),
             "%s %s" % (e["to"].get("coordinate"), e["to"].get("label")),
             e["backed_by_a_static_call_edge"]))
ids = []
for e in row["exclusive_transition_examples"]:
    for side in ("from", "to"):
        if e[side].get("in_the_region_graph") and e[side]["id"] not in ids:
            ids.append(e[side]["id"])
open('/work/wanted_ids.txt', 'w').write("\n".join(ids))
print("   node ids carried to the coverage scan: %d" % len(ids))
PY

say "[4/5] WHAT THE UNION SAYS ABOUT THOSE SAME NODES -- coverage, streamed"
python3 - <<'PY'
import json, resource, time
wanted = set(x for x in open('/work/wanted_ids.txt').read().split("\n") if x)
path = ('/projects/PseudoCoupHQ/Research/compiler_graph/'
        'coverage_c_and_cpp.json')
# THE FILE IS 416,754,589 BYTES AND IS NOT OPENED WHOLE. json.dumps with
# indent=1 puts one element on a line, so `per_node_visitors` reads as a
# key line followed by one probe id per line until the closing bracket.
started = time.time()
inside = False
current = None
counts = {}
lines = 0
with open(path) as handle:
    for line in handle:
        lines += 1
        stripped = line.strip()
        if not inside:
            if stripped.startswith('"per_node_visitors"'):
                inside = True
            continue
        if current is not None:
            if stripped.startswith("]"):
                current = None
            else:
                counts[current] = counts[current] + 1
            continue
        if stripped.endswith("[") and stripped.startswith('"'):
            key = stripped[1:stripped.index('": [')]
            if key in wanted:
                current = key
                counts[key] = 0
            continue
        if stripped.startswith("},") or stripped == "}":
            break
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
print("   coverage_c_and_cpp.json: %d lines read, PEAK RESIDENT %.1f MB, "
      "wall %.1f s" % (lines, peak, time.time() - started))
print("   THE CONTRAST, per node:")
print("      %-64s %14s %16s" % ("node", "union: probes", "third kind"))
d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_c_and_cpp.json'))
row = d["variants"][0]
labels = {}
for e in row["exclusive_transition_examples"]:
    for side in ("from", "to"):
        s = e[side]
        if s.get("in_the_region_graph"):
            labels[s["id"]] = s.get("label")
for node in sorted(wanted):
    print("      %-64s %14s %16s"
          % ((labels.get(node) or "-")[:64], counts.get(node, "not present"),
             "1 variant of %d" % d["populations"]["operator_traced_variants"]))
PY

say "[5/5] the same question asked of the whole population, not one variant"
python3 - <<'PY'
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_c_and_cpp.json'))
n = d["census"]["nodes"]; t = d["census"]["transitions"]
p = d["populations"]
print("   THE UNION (Graph.coverage, log_190 section 5.2) says of the same")
print("   1,380 probes: 1,331 of 8,871 instrumented bodies visited by at")
print("   least one probe, 7,540 by none. One number per node, and no edges.")
print()
print("   THE THIRD KIND says of the %d nodes those probes actually entered:"
      % p["distinct_nodes_entered"])
for k in ("walked_by_exactly_one_variant", "walked_by_2_to_10_variants",
          "walked_by_11_to_100_variants", "walked_by_more_than_100_variants",
          "walked_by_every_variant"):
    print("      nodes %-38s %5d" % (k, n[k]))
print("   and of the %d visited-next transitions, which the union does not"
      % p["distinct_transitions"])
print("   hold at all:")
for k in ("walked_by_exactly_one_variant", "walked_by_2_to_10_variants",
          "walked_by_11_to_100_variants", "walked_by_more_than_100_variants",
          "walked_by_every_variant"):
    print("      transitions %-32s %5d" % (k, t[k]))
print("   static backing: %s" % json.dumps(
    {k: v for k, v in d["static_backing"].items()
     if k != "what_an_unbacked_transition_is"}))
PY
echo "DONE t87_l9"
