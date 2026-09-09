#!/usr/bin/env bash
# t87 lane 11 — every literal log 193 quotes, printed from the
# artifacts AS THEY NOW STAND on disk, so nothing in the report is
# quoted from notes.
#
# THE MEMORY BOUND. `coverage_c_and_cpp.json` (416,754,589 bytes) and
# `coverage_go2.json` (515,160,866) are read ONE LINE AT A TIME and
# never opened whole; each scan prints its peak resident set.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# Every variant printed below was chosen by a NUMBER (its exclusive
# transition count) and by nothing else.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/6] the five measured populations, from the artifacts"
python3 - <<'PY'
import json
rows = [("go", "variant_connections_go.json"),
        ("c", "variant_connections_c.json"),
        ("cpp", "variant_connections_cpp.json"),
        ("c and cpp", "variant_connections_c_and_cpp.json"),
        ("c and cpp + regen", "variant_connections_extended.json")]
print("   | population | probes | variants | nodes entered | transitions | "
      "transitions walked by exactly one variant | transitions walked by every variant |")
print("   |---|---|---|---|---|---|---|")
for name, path in rows:
    d = json.load(open('PseudoCoupHQ/Research/compiler_graph/' + path))
    p = d["populations"]; c = d["census"]["transitions"]
    print("   | %s | %d | %d | %d | %d | %d | %d |"
          % (name, p["diaries_on_disk"], p["operator_traced_variants"],
             p["distinct_nodes_entered"], p["distinct_transitions"],
             c["walked_by_exactly_one_variant"], c["walked_by_every_variant"]))
    assert p["probes_without_a_machine_form"] == 0, p
print("   probes_without_a_machine_form on every one of the five: 0")
PY

say "[2/6] the two UNMEASURED artifacts, quoted whole"
python3 - <<'PY'
import json
for lang in ("rust", "swift"):
    d = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                       'variant_connections_%s.json' % lang))
    print("   --- variant_connections_%s.json" % lang)
    print("   state  : %s" % d["state"])
    print("   reason : %s" % d["reason"])
    print("   populations: %s" % json.dumps(d["populations"]))
PY

say "[3/6] THE WORKED EXAMPLE, c and cpp -- one variant, its values moving"
python3 - <<'PY'
import json
d = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_c_and_cpp.json'))
row = d["variants"][0]
print("   variant_id : %s" % row["variant_id"])
print("   members %d   probes with a diary %d   languages %s   populations %s"
      % (row["member_count"], row["probes_with_a_diary"],
         row["languages"], row["populations"]))
print("   THE MACHINE FORM IT IS IDENTIFIED BY, and nothing else:")
for k in ("bytes", "text"):
    print("      %-14s %s" % (k, row["machine_form"][k]))
print("      entry_contract %s" % json.dumps(row["machine_form"]["entry_contract"]))
print("      ledger_shape   %s" % json.dumps(row["machine_form"]["ledger_shape"]))
print("   THE MEMBERS, typed unit objects, each carrying its display label:")
for m in row["members"]:
    print("      %-14s language %-4s label %-6s population %-11s outcome %s"
          % (m["id"], m["language"], json.dumps(m["operator"]),
             m["population"], m["outcome"]))
print("   ITS OWN CONNECTIONS: nodes %d (exclusive %d), transitions %d "
      "(exclusive %d, static-backed %d)"
      % (row["nodes_entered"], row["nodes_exclusive_to_this_variant"],
         row["transitions"], row["transitions_exclusive_to_this_variant"],
         row["transitions_backed_by_a_static_call_edge"]))
print("   THE EXCLUSIVE TRANSITIONS, to the stated cap of %d:"
      % d["parameters"]["exclusive_examples_per_variant"])
ids = []
for e in row["exclusive_transition_examples"]:
    a, b = e["from"], e["to"]
    print("      %s %s" % (a["coordinate"], a["label"]))
    print("        -> %s %s   (static call edge: %s)"
          % (b["coordinate"], b["label"], e["backed_by_a_static_call_edge"]))
    for s in (a, b):
        if s.get("in_the_region_graph") and s["id"] not in ids:
            ids.append(s["id"])
open('/work/ids_cc.txt', 'w').write("\n".join(ids))
PY

say "[4/6] WHAT THE UNION SAYS ABOUT THOSE SAME NODES (coverage, streamed)"
python3 - <<'PY'
import json, resource, time
def visitors(path, wanted):
    started = time.time(); inside = False; current = None
    counts = {}; lines = 0
    with open(path) as handle:
        for line in handle:
            lines += 1
            s = line.strip()
            if not inside:
                if s.startswith('"per_node_visitors"'):
                    inside = True
                continue
            if current is not None:
                if s.startswith("]"):
                    current = None
                else:
                    counts[current] += 1
                continue
            if s.startswith('"') and s.endswith("["):
                key = s[1:s.index('": [')]
                if key in wanted:
                    current = key; counts[key] = 0
                continue
            if s.startswith("},") or s == "}":
                break
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("   %s: %d lines, PEAK RESIDENT %.1f MB, wall %.1f s"
          % (path.rsplit('/', 1)[-1], lines, peak, time.time() - started))
    return counts
base = 'PseudoCoupHQ/Research/compiler_graph/'
wanted = [x for x in open('/work/ids_cc.txt').read().split("\n") if x]
counts = visitors(base + 'coverage_c_and_cpp.json', set(wanted))
d = json.load(open(base + 'variant_connections_c_and_cpp.json'))
row = d["variants"][0]
labels = {}
for e in row["exclusive_transition_examples"]:
    for side in ("from", "to"):
        s = e[side]
        if s.get("in_the_region_graph"):
            labels[s["id"]] = s.get("label")
print()
print("   | compiler body | the UNION: probes of 1,380 that entered it | "
      "the THIRD KIND: variants of 512 whose traces walk the transition |")
print("   |---|---|---|")
for node in wanted:
    print("   | %s | %s | 1 |" % (labels.get(node) or "-", counts.get(node, "-")))
PY

say "[5/6] the go worked example, for the second compiler"
python3 - <<'PY'
import json
d = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_go.json'))
row = d["variants"][0]
print("   variant_id %s   members %d   probes %d   populations %s"
      % (row["variant_id"], row["member_count"], row["probes_with_a_diary"],
         row["populations"]))
print("   machine form bytes : %s" % row["machine_form"]["bytes"])
print("   machine form text  : %s" % row["machine_form"]["text"])
print("   members and their display labels:")
for m in row["members"]:
    print("      %-16s label %-6s population %s"
          % (m["id"], json.dumps(m["operator"]), m["population"]))
print("   nodes %d (exclusive %d), transitions %d (exclusive %d, "
      "static-backed %d)"
      % (row["nodes_entered"], row["nodes_exclusive_to_this_variant"],
         row["transitions"], row["transitions_exclusive_to_this_variant"],
         row["transitions_backed_by_a_static_call_edge"]))
for e in row["exclusive_transition_examples"]:
    print("      %s %s" % (e["from"]["coordinate"], e["from"]["label"]))
    print("        -> %s %s   (static call edge: %s)"
          % (e["to"]["coordinate"], e["to"]["label"],
             e["backed_by_a_static_call_edge"]))
PY

say "[6/6] the census, both populations, with its own reading note"
python3 - <<'PY'
import json
for path in ("variant_connections_c_and_cpp.json",
             "variant_connections_extended.json",
             "variant_connections_go.json"):
    d = json.load(open('PseudoCoupHQ/Research/compiler_graph/' + path))
    print("   --- %s" % path)
    print("   %s" % d["census"]["how_to_read_this"])
    for what in ("nodes", "transitions"):
        print("      %s: %s" % (what, json.dumps(d["census"][what])))
    print("      static_backing: %s"
          % json.dumps({k: v for k, v in d["static_backing"].items()
                        if k != "what_an_unbacked_transition_is"}))
    print("      cost: %s" % json.dumps(d["cost"]))
PY
echo "DONE t87_l11"
