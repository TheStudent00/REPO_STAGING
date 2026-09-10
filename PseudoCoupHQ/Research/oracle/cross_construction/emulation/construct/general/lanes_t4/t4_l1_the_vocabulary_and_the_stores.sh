#!/bin/bash
# t4_l1_the_vocabulary_and_the_stores.sh -- task t4, lane 1: the OPERATION
# KINDS, read off the stores rather than recalled, and the sha256 of every
# store this task reads.
#
# The brief's own definition of `operation kind` is "Term.normalize's own
# node vocabulary, listed from the term store: every kind that occurs, with
# the widths it occurs at, counted".  This lane produces exactly that, over
# the population the task measures on -- the x86 cells the driver answers
# and the RISC-V cells the model table holds -- so the construction table
# is written against the kinds that actually occur and no others.
#
#   [1/6] the sha256 of every store read, RECORDED BEFORE ANYTHING RUNS
#         (task ref2 writes corrected stores BESIDE the old ones; this
#         task reads the ones named here and never switches mid-pass)
#   [2/6] the x86 cells' node vocabulary: (z3 decl kind, width) counted
#   [3/6] the RISC-V cells' node vocabulary, the same way
#   [4/6] the word each target has, off that target's own renderer table
#   [5/6] the bank's population: (cell, target) with no proved certificate
#   [6/6] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.  The bank is
# 47 MB and is STREAMED; nothing here holds it whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
E=$P/Research/oracle/cross_construction/emulation
G=$E/construct/general
total=6

mkdir -p "$G"

i=1
echo "[$i/$total] THE STORES THIS TASK READS, sha256, recorded before anything runs"
for f in \
    $P/Research/op_pipeline/reference.py \
    $P/Research/oracle/arch_opcodes/model/model_table.json \
    $P/Research/oracle/arch_opcodes/model/model_table_rows.json \
    $E/autopoly/autopoly5_cells.json \
    $E/autopoly/certificates.jsonl \
    $E/emulate.py \
    $E/handful/handful.py \
    $E/construct/schemas.py \
    $E/construct/construct.py \
    $P/Research/oracle/riscv/model_table_rv.json \
    $P/Research/oracle/riscv/riscv_reference.py \
    $P/Research/oracle/riscv/twins.json \
    $P/Research/oracle/riscv/attest_rv.json \
    $P/Research/oracle/riscv/certificates_riscv64_rv3.jsonl ; do
    if [ -f "$f" ]; then
        sha256sum "$f"
    else
        echo "ABSENT  $f"
    fi
done

i=2
echo ""
echo "[$i/$total] THE X86 CELLS' NODE VOCABULARY -- every kind that occurs, with its widths"
python3 - "$E" "$G" <<'PY'
import sys, os, json, collections, resource
E = sys.argv[1]
G = sys.argv[2]
sys.path.insert(0, os.path.join(E, "handful"))
import handful as H
import z3
import model_table as MTAB
MTAB._install_gpr_widths()

ABORT_KB = 6 * 1024 * 1024
def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_T4: %d kB at %s" % (peak, where))
    return peak

cells = H.read_json(os.path.join(E, "autopoly", "autopoly5_cells.json"))
counts = collections.Counter()
places = 0
asked_count = 0
widths_of_kind = collections.defaultdict(collections.Counter)

def walk(node, seen):
    key = node.get_id()
    if key in seen:
        return
    seen.add(key)
    decl = node.decl()
    kind = decl.kind()
    name = decl.name()
    if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
        label = "seed (an arrival)"
    elif kind == z3.Z3_OP_BNUM:
        label = "numeral"
    else:
        label = "%s" % name
    try:
        if node.sort().kind() == z3.Z3_BV_SORT:
            width = node.size()
        elif z3.is_fp(node):
            width = node.sort().ebits() + node.sort().sbits()
        elif node.sort().kind() == z3.Z3_BOOL_SORT:
            width = 1
        else:
            width = -1
    except Exception:
        width = -1
    counts[label] += 1
    widths_of_kind[label][width] += 1
    for index in range(node.num_args()):
        walk(node.arg(index), seen)
    return

for record in cells["asked"]:
    asked = (record["asked"]["mnem"], record["asked"]["shape"],
             record["asked"]["key_width"])
    asked_count = asked_count + 1
    try:
        held_list = H.cell_inputs(cells, asked)
    except Exception as problem:
        print("  REFUSED at %s: %s: %s" % (asked, type(problem).__name__, problem))
        continue
    for held in held_list:
        for place in held.get("places") or []:
            term = place.get("term")
            if term is None:
                continue
            places = places + 1
            walk(term, set())
    check("%s" % (asked,))

print("asked cells: %d; written places walked: %d" % (asked_count, places))
print("")
print("| the kind, as z3 declares it | nodes | the widths it occurs at |")
print("|---|---|---|")
for label in sorted(counts, key=lambda k: -counts[k]):
    ws = widths_of_kind[label]
    text = ", ".join("%d(%d)" % (w, ws[w]) for w in sorted(ws))
    print("| %s | %d | %s |" % (label, counts[label], text))

document = {
    "meta": {"what": "the x86 cells' node vocabulary, over every written "
                     "place of every held cell the driver answers",
             "asked_cells": asked_count, "places": places,
             "peak_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    "kinds": [{"kind": label, "nodes": counts[label],
               "widths": {str(w): widths_of_kind[label][w]
                          for w in widths_of_kind[label]}}
              for label in sorted(counts)],
}
handle = open(os.path.join(G, "vocabulary_x86.json"), "w")
json.dump(document, handle, indent=1, sort_keys=True)
handle.close()
print("")
print("peak resident: %d kB" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

i=3
echo ""
echo "[$i/$total] THE RISC-V CELLS' NODE VOCABULARY, the same way"
python3 - "$P" "$G" <<'PY'
import sys, os, json, collections, resource
P = sys.argv[1]
G = sys.argv[2]
RV = os.path.join(P, "Research", "oracle", "riscv")
sys.path.insert(0, RV)
sys.path.insert(0, os.path.join(P, "Research", "op_pipeline"))
import z3
import rv_loop as RL

terms, operands = RL.riscv_terms(os.path.join(RV, "model_table_rv.json"))
counts = collections.Counter()
widths_of_kind = collections.defaultdict(collections.Counter)

def walk(node, seen):
    key = node.get_id()
    if key in seen:
        return
    seen.add(key)
    decl = node.decl()
    kind = decl.kind()
    if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
        label = "seed (an arrival)"
    elif kind == z3.Z3_OP_BNUM:
        label = "numeral"
    else:
        label = "%s" % decl.name()
    try:
        if node.sort().kind() == z3.Z3_BV_SORT:
            width = node.size()
        elif z3.is_fp(node):
            width = node.sort().ebits() + node.sort().sbits()
        elif node.sort().kind() == z3.Z3_BOOL_SORT:
            width = 1
        else:
            width = -1
    except Exception:
        width = -1
    counts[label] += 1
    widths_of_kind[label][width] += 1
    for index in range(node.num_args()):
        walk(node.arg(index), seen)
    return

cells = set()
for (key, place) in terms:
    cells.add(key)
    walk(terms[(key, place)], set())

print("RISC-V cells: %d; written places walked: %d" % (len(cells), len(terms)))
print("")
print("| the kind, as z3 declares it | nodes | the widths it occurs at |")
print("|---|---|---|")
for label in sorted(counts, key=lambda k: -counts[k]):
    ws = widths_of_kind[label]
    text = ", ".join("%d(%d)" % (w, ws[w]) for w in sorted(ws))
    print("| %s | %d | %s |" % (label, counts[label], text))

document = {
    "meta": {"what": "the RISC-V cells' node vocabulary",
             "cells": len(cells), "places": len(terms),
             "peak_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    "kinds": [{"kind": label, "nodes": counts[label],
               "widths": {str(w): widths_of_kind[label][w]
                          for w in widths_of_kind[label]}}
              for label in sorted(counts)],
}
handle = open(os.path.join(G, "vocabulary_riscv64.json"), "w")
json.dump(document, handle, indent=1, sort_keys=True)
handle.close()
print("")
print("peak resident: %d kB" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

i=4
echo ""
echo "[$i/$total] THE WORD each target has, off that target's own renderer table"
python3 - "$E" <<'PY'
import sys, os
E = sys.argv[1]
sys.path.insert(0, os.path.join(E, "construct"))
import construct as CONS
print("| target | the word, off its own renderer table |")
print("|---|---|")
for lang in ("c", "cpp", "rust", "go", "swift"):
    print("| %s | %d |" % (lang, CONS.word_of(lang)))
PY

i=5
echo ""
echo "[$i/$total] THE BANK'S POPULATION: (cell, target) with no proved certificate"
python3 - "$E" <<'PY'
import sys, os, json, collections, resource
E = sys.argv[1]
BANK = os.path.join(E, "autopoly", "certificates.jsonl")
ABORT_KB = 6 * 1024 * 1024
proved = collections.defaultdict(set)
kinds = collections.defaultdict(collections.Counter)
causes = collections.Counter()
cause_target = collections.defaultdict(collections.Counter)
pairs = set()
total = 0
handle = open(BANK)
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    total = total + 1
    if not cert.get("preferred"):
        continue
    pair = (cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"], cert["target"])
    pairs.add(pair)
    kinds[cert["target"]][cert["kind"]] += 1
    if cert["kind"] in ("proved", "agreed"):
        proved[cert["target"]].add(pair)
    if cert["kind"] == "refused":
        cause = cert.get("cause") or "(no cause)"
        causes[cause] += 1
        cause_target[cause][cert["target"]] += 1
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_T4: %d kB" % peak)
handle.close()
print("certificates on the bank: %d; distinct (cell, target) pairs: %d"
      % (total, len(pairs)))
print("")
print("| target | preferred certificates by kind |")
print("|---|---|")
for target in sorted(kinds):
    row = "; ".join("%s %d" % (k, kinds[target][k])
                    for k in sorted(kinds[target]))
    print("| %s | %s |" % (target, row))
print("")
print("| the refusal cause the bank carries | certificates | per target |")
print("|---|---|---|")
for cause in sorted(causes, key=lambda c: -causes[c]):
    per = "; ".join("%s %d" % (t, cause_target[cause][t])
                    for t in sorted(cause_target[cause]))
    print("| %s | %d | %s |" % (cause.replace("|", "/")[:150], causes[cause], per))
print("")
print("peak resident: %d kB" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

i=6
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
