#!/bin/bash
# t2_l2_the_holes_in_detail.sh -- task t2, lane 2: every width-or-kind
# refusal the bank holds on the FIVE COMPILED targets, with the
# refusal's own detail sentence, the written place and the term the
# renderer refused, so the schemas are written against the objects and
# not against a recollection of them.
#
# Lane 1 counted them.  This one prints them, because a schema table is
# a design and a design has to be read against the things it is for.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2; the bank is
# streamed.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=4

i=1
echo "[$i/$total] EVERY WIDTH-OR-KIND REFUSAL ON THE FIVE COMPILED TARGETS"
python3 - "$A" <<'PY'
import sys, json, collections, resource
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
rows = []
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
    cause = cert.get("cause") or ""
    if not is_a_hole(cause):
        continue
    rows.append(cert)
    continue
handle.close()
print("width-or-kind refusals on the five compiled targets: %d" % len(rows))
print("")
print("| target | `mnem` | shape | `key_width` | place | the cause, LITERAL | the detail, LITERAL |")
print("|---|---|---|---|---|---|---|")
def sort_key(cert):
    return (cert["target"], cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"], cert["place"] or "")
for cert in sorted(rows, key=sort_key):
    detail = cert.get("cause_detail") or ""
    print("| %s | `%s` | %s | %s | %s | %s | %s |"
          % (cert["target"], cert["cell"]["mnem"], cert["cell"]["shape"],
             cert["cell"]["key_width"], cert["place"],
             (cert.get("cause") or "").replace("|", "/"),
             str(detail).replace("|", "/")[:140]))
    continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

i=2
echo "[$i/$total] THE SAME POPULATION, one row per (cell, target), with the cell's own term per place"
python3 - "$A" "$H" <<'PY'
import sys, json, collections
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
want = set()
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
    want.add((cert["cell"]["mnem"], cert["cell"]["shape"],
              cert["cell"]["key_width"]))
    continue
handle.close()
print("distinct CELLS behind them: %d" % len(want))
print("")
# the term of each place, from the outer set the loop walks
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, sys.argv[1])
import autopoly as AP
cells = json.load(open(AP.CELLS))
rows_by_cell = {}
for row in cells.get("asked") or cells.get("cells") or []:
    key = (row.get("mnem"), row.get("shape"), row.get("key_width"))
    rows_by_cell.setdefault(key, row)
    continue
print("keys the outer set holds: %d; of the wanted, found: %d"
      % (len(rows_by_cell), len([k for k in want if k in rows_by_cell])))
print("")
print("| `mnem` | shape | `key_width` | what the outer set records |")
print("|---|---|---|---|")
for key in sorted(want):
    row = rows_by_cell.get(key)
    if row is None:
        print("| `%s` | %s | %s | not in the outer set |" % key)
        continue
    keys = sorted(k for k in row if not isinstance(row[k], (dict, list)))
    print("| `%s` | %s | %s | %s |"
          % (key[0], key[1], key[2], " ".join(keys)[:120]))
    continue
PY
echo

i=3
echo "[$i/$total] THE OUTER SET'S OWN SHAPE: what one asked row carries"
python3 - "$A" "$H" <<'PY'
import sys, json
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, sys.argv[1])
import autopoly as AP
cells = json.load(open(AP.CELLS))
print("top-level keys of the cells file: %s" % sorted(cells))
asked = cells.get("asked")
print("asked rows: %d" % len(asked))
one = asked[0]
print("one asked row's keys: %s" % sorted(one))
print(json.dumps(one, sort_keys=True)[:2400])
PY
echo

i=4
echo "[$i/$total] peak resident"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo
echo "lane done"
