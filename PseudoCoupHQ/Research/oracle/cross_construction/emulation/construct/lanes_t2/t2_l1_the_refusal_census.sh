#!/bin/bash
# t2_l1_the_refusal_census.sh -- task t2, lane 1: what the second tier is
# FOR, read off the bank before a line of it is written.
#
# The brief's tier constructs what a target lacks from the primitives it
# has, so the first question is which certificates the bank holds that
# say the target lacked something.  This lane reads `certificates.jsonl`
# once, streaming, and prints:
#   [1/5] every refusal cause the bank carries, by count, per target
#   [2/5] the causes that are a WIDTH or a KIND hole -- the four the
#         brief names and any other that reads the same way -- with the
#         cells behind them
#   [3/5] the (cell, target) pairs with no `proved`/`agreed` certificate
#         at any place, which is the population the tier is offered
#   [4/5] the widest integer holder each target has, read off the
#         renderer's own tables rather than recalled
#   [5/5] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.  The bank is
# 36 MB and is STREAMED line by line; nothing here holds it whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=5

i=1
echo "[$i/$total] EVERY REFUSAL CAUSE THE BANK CARRIES, per target"
python3 - "$A" <<'PY'
import sys, json, resource, collections
BANK = sys.argv[1] + "/certificates.jsonl"
ABORT_KB = 6 * 1024 * 1024
per_cause = collections.Counter()
per_cause_target = collections.defaultdict(collections.Counter)
total = 0
refused = 0
handle = open(BANK)
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    total = total + 1
    if not cert.get("preferred"):
        continue
    if cert["kind"] != "refused":
        continue
    refused = refused + 1
    cause = cert.get("cause") or "(no cause on the certificate)"
    per_cause[cause] += 1
    per_cause_target[cause][cert["target"]] += 1
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_T2: %d kB" % peak)
    continue
handle.close()
print("certificates on the bank: %d" % total)
print("of them PREFERRED and `refused`: %d" % refused)
print("")
print("| the cause, LITERAL | c | cpp | rust | go | swift | all |")
print("|---|---|---|---|---|---|---|")
for cause, count in per_cause.most_common():
    row = per_cause_target[cause]
    print("| %s | %d | %d | %d | %d | %d | %d |"
          % (cause.replace("|", "/"), row["c"], row["cpp"], row["rust"],
             row["go"], row["swift"], count))
    continue
PY
echo

i=2
echo "[$i/$total] THE CAUSES THAT ARE A WIDTH OR A KIND HOLE, with their cells"
python3 - "$A" <<'PY'
import sys, json, collections
BANK = sys.argv[1] + "/certificates.jsonl"
# A width-or-kind hole is a refusal whose cause sentence is one the
# RENDERER raises about the target's own holders, or the driver's own
# x87 sentence.  The test is on the sentence the renderer wrote, which
# is machine form: no mnemonic is read anywhere in this lane.
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
per = collections.defaultdict(lambda: collections.defaultdict(set))
detail = collections.Counter()
handle = open(BANK)
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    if not cert.get("preferred"):
        continue
    if cert["kind"] != "refused":
        continue
    cause = cert.get("cause") or ""
    if not is_a_hole(cause):
        continue
    cell = (cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"])
    per[cause][cert["target"]].add(cell)
    detail[(cause, cert["target"])] += 1
    continue
handle.close()
print("| the cause, LITERAL | target | certificates | distinct cells |")
print("|---|---|---|---|")
for cause in sorted(per, key=lambda c: -sum(len(v) for v in per[c].values())):
    for target in sorted(per[cause]):
        print("| %s | %s | %d | %d |"
              % (cause.replace("|", "/"), target,
                 detail[(cause, target)], len(per[cause][target])))
        continue
    continue
print("")
print("the distinct cells behind each, at most twelve per cause and target:")
for cause in sorted(per, key=lambda c: -sum(len(v) for v in per[c].values())):
    for target in sorted(per[cause]):
        cells = sorted(per[cause][target])[:12]
        print("  %s | %s" % (target, cause.replace("|", "/")))
        for cell in cells:
            print("      mnem %-10s shape %-14s key_width %s"
                  % (cell[0], cell[1], cell[2]))
            continue
        continue
    continue
PY
echo

i=3
echo "[$i/$total] THE (cell, target) PAIRS WITH NO PROOF AT ANY PLACE"
python3 - "$A" <<'PY'
import sys, json, collections
BANK = sys.argv[1] + "/certificates.jsonl"
kinds = collections.defaultdict(set)
places = collections.Counter()
handle = open(BANK)
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    if not cert.get("preferred"):
        continue
    pair = (cert["cell"]["mnem"], cert["cell"]["shape"],
            cert["cell"]["key_width"], cert["target"])
    kinds[pair].add(cert["kind"])
    places[pair] += 1
    continue
handle.close()
proved = set()
for pair in kinds:
    if "proved" in kinds[pair] or "agreed" in kinds[pair]:
        proved.add(pair)
        continue
    continue
per_target = collections.Counter()
per_target_all = collections.Counter()
for pair in kinds:
    per_target_all[pair[3]] += 1
    if pair not in proved:
        per_target[pair[3]] += 1
    continue
print("| target | (cell, target) pairs on the bank | with no proof at any place |")
print("|---|---|---|")
for target in ("c", "cpp", "rust", "go", "swift"):
    print("| %s | %d | %d |" % (target, per_target_all[target],
                                per_target[target]))
    continue
print("| all | %d | %d |" % (sum(per_target_all.values()),
                             sum(per_target.values())))
PY
echo

i=4
echo "[$i/$total] THE WIDEST HOLDER EACH TARGET HAS, off the renderers' own tables"
python3 - "$H" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
import handful as H
import emulate as E
import rust_render as RR
import go_render as GR
import swift_render as SR
tables = {
    "c": (sorted(E.UNSIGNED), sorted(E.FLOAT)),
    "cpp": (sorted(E.UNSIGNED), sorted(E.FLOAT)),
    "rust": (sorted(RR.RU), sorted(RR.RF)),
    "go": (sorted(GR.GU), sorted(GR.GF)),
    "swift": (sorted(SR.SU), sorted(SR.SF)),
}
print("| target | integer holders, bits | float holders, bits | the word |")
print("|---|---|---|---|")
for target in ("c", "cpp", "rust", "go", "swift"):
    ints, floats = tables[target]
    word = max(b for b in ints if b <= 64)
    print("| %s | %s | %s | %d |"
          % (target, " ".join(str(b) for b in ints),
             " ".join(str(b) for b in floats), word))
    continue
PY
echo

i=5
echo "[$i/$total] peak resident of this lane's own last process"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo
echo "lane done"
