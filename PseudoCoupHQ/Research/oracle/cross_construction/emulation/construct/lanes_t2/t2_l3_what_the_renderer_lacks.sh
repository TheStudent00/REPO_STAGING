#!/bin/bash
# t2_l3_what_the_renderer_lacks.sh -- task t2, lane 3: the width-refused
# places REBUILT and put to the renderer live, so the schema table is
# written against the node the renderer actually refused and not against
# a reading of a cause sentence.
#
# Per (cell, target) the bank refuses by width or kind, this lane
# rebuilds the cell's places from the outer set, and for each place
# prints: the place's own width, the WIDEST NODE in its term, how many
# nodes the term has as a DAG and as the renderer would UNFOLD it (the
# renderer emits one nested expression and names no intermediate, so an
# unfolded count is the size of the source it would write), and the
# renderer's own refusal LITERAL.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=2

i=1
echo "[$i/$total] EVERY WIDTH-REFUSED PLACE, REBUILT AND PUT TO ITS RENDERER"
python3 - "$A" "$H" <<'PY'
import sys, json, resource, collections
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, sys.argv[1])
import autopoly as AP
import handful as H
import emulate as E
import z3
ABORT_KB = 6 * 1024 * 1024

BANK = sys.argv[1] + "/certificates.jsonl"
COMPILED = ("c", "cpp", "rust", "go", "swift")
MARKS = ["has no ", "is not spelled by this renderer",
         "a width c has no holder for",
         "answer home or arrival on the x87 stack",
         "operator not covered by the renderer"]
def is_a_hole(cause):
    for mark in MARKS:
        if mark in cause:
            return True
        continue
    return False
want = collections.defaultdict(set)
handle = open(BANK)
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    if not cert.get("preferred"):
        continue
    if cert["target"] not in COMPILED:
        continue
    if cert["kind"] != "refused":
        continue
    if not is_a_hole(cert.get("cause") or ""):
        continue
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"])
    want[key].add(cert["target"])
    continue
handle.close()
print("cells to rebuild: %d" % len(want))

cells = json.load(open(AP.CELLS))

def widest_node(term, seen):
    here = term.get_id()
    if here in seen:
        return seen[here]
    widest = 0
    if z3.is_bv(term):
        widest = term.size()
    for index in range(term.num_args()):
        child = widest_node(term.arg(index), seen)
        if child > widest:
            widest = child
        continue
    seen[here] = widest
    return widest

def dag_nodes(term, seen):
    here = term.get_id()
    if here in seen:
        return 0
    seen.add(here)
    count = 1
    for index in range(term.num_args()):
        count = count + dag_nodes(term.arg(index), seen)
        continue
    return count

def unfolded_nodes(term, memo, ceiling=2000000):
    here = term.get_id()
    if here in memo:
        return memo[here]
    count = 1
    for index in range(term.num_args()):
        count = count + unfolded_nodes(term.arg(index), memo, ceiling)
        if count > ceiling:
            count = ceiling
            break
        continue
    memo[here] = count
    return count

print("")
print("| target | `mnem` | shape | `key_width` | place | place bits | widest node | DAG nodes | unfolded | the renderer's refusal, LITERAL |")
print("|---|---|---|---|---|---|---|---|---|---|")
rows = 0
for key in sorted(want):
    held = H.cell_input(cells, key)
    if held.get("refusal_cause") is not None:
        print("| (all) | `%s` | %s | %s | - | - | - | - | - | the cell itself: %s |"
              % (key[0], key[1], key[2],
                 held["refusal_cause"].replace("|", "/")))
        continue
    for target in sorted(want[key]):
        for place in held["places"]:
            if place.get("term") is None:
                continue
            term = place["term"]
            widest = widest_node(term, {})
            dag = dag_nodes(term, set())
            unfolded = unfolded_nodes(term, {})
            label = E.sanitize("%s_%s_%d__%s__%s"
                               % (held["mnem"], held["shape"],
                                  held["key_width"],
                                  place["writes"].replace(".", "_"),
                                  target))
            built = H.render_one_place(place, target, label, write=False)
            if built.get("rendered"):
                refusal = "RENDERED"
            else:
                refusal = "%s -- %s" % (built.get("refusal_cause"),
                                        built.get("refusal_detail"))
            print("| %s | `%s` | %s | %s | %s | %s | %d | %d | %d | %s |"
                  % (target, key[0], key[1], key[2], place["writes"],
                     place.get("bits"), widest, dag, unfolded,
                     str(refusal).replace("|", "/")[:150]))
            rows = rows + 1
            continue
        continue
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_T2: %d kB" % peak)
    continue
print("")
print("rows: %d" % rows)
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

i=2
echo "[$i/$total] lane done"
