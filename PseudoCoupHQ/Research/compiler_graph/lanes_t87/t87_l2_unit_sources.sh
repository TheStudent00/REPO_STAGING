#!/usr/bin/env bash
# t87 lane 2 — SURVEY ONLY. Lane 1 found that only 107 of go's 590
# diaried probes have a unit record in canon39_wrapped_go.json. The
# third connection kind groups probes into operator traced variants by
# MACHINE-FORM EVIDENCE, so it needs a machine form for every probe it
# speaks about. This lane finds which artifact on disk carries one, for
# each of the three diaried populations, and for the 2,600 regenerated
# probes.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line. The token appears exactly once per unit: as a
# display label on the member. Nothing in this lane reads an operator
# field for any purpose but printing one single unit whole.
set -u
say() { echo; echo "======== $* ========"; }
PIPE=PseudoCoupHQ/Research/op_pipeline
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$PIPE"

say "[1/5] the go diary stems, and the go unit artifacts on disk"
python3 - <<'PY'
import json, os, glob
stems = sorted(n[:-4] for n in os.listdir(
    'PseudoCoupHQ/Research/compiler_graph/diaries/go')
    if n.endswith('.txt'))
print("   diaries/go stems      : %d, first five %s" % (len(stems), stems[:5]))
for name in ("canon31_units_go.json", "canon39_wrapped_go.json",
             "canon40_wrapped_go.json"):
    path = 'PseudoCoupHQ/Research/op_pipeline/' + name
    doc = json.load(open(path))
    units = doc.get("units") if isinstance(doc, dict) else None
    if not isinstance(units, dict):
        print("   %-28s top-level %s" % (name, sorted(doc)[:12]))
        continue
    hit = sum(1 for s in stems if ("go/%s" % s) in units)
    withbytes = sum(1 for u in units.values()
                    if isinstance(u, dict) and u.get("body_bytes"))
    print("   %-28s %5d units, %4d of the 590 stems join, %5d carry body_bytes"
          % (name, len(units), hit, withbytes))
    first = units[sorted(units)[0]]
    print("        fields: %s" % ", ".join(sorted(first))[:400])
PY

say "[2/5] the same question for c and cpp, and for the outcome column"
python3 - <<'PY'
import json, collections
for lang in ("go", "c", "cpp"):
    doc = json.load(open('PseudoCoupHQ/Research/op_pipeline/'
                         'canon39_wrapped_%s.json' % lang))
    tally = collections.Counter(u.get("outcome") for u in doc["units"].values())
    pops = collections.Counter(u.get("population") for u in doc["units"].values())
    print("   %-4s outcomes %s  populations %s" % (lang, dict(tally), dict(pops)))
    print("        meta: %s" % json.dumps(doc.get("meta"))[:400])
    print("        tally: %s" % json.dumps(doc.get("tally"))[:400])
PY

say "[3/5] canon31_units_go.json -- does it cover all 590, and with what"
python3 - <<'PY'
import json, os
doc = json.load(open('PseudoCoupHQ/Research/op_pipeline/'
                     'canon31_units_go.json'))
print("   top-level: %s" % sorted(doc)[:12])
units = doc.get("units")
if isinstance(units, dict):
    keys = sorted(units)
    print("   units: %d, first five %s" % (len(units), keys[:5]))
    one = units[keys[0]]
    print("   one unit's fields: %s" % ", ".join(sorted(one))[:600])
    for f in ("body_bytes", "body_text", "body_as_read", "entry_contract",
              "ledger", "outcome", "lang", "n"):
        print("      %-16s %s" % (f, json.dumps(one.get(f))[:180]))
PY

say "[4/5] the regenerated population: store shape and the diary stems"
python3 - <<'PY'
import json, os
store = 'PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
names = sorted(os.listdir(store))
print("   shards: %d" % len(names))
doc = json.load(open(os.path.join(store, names[0])))
print("   %s top-level: %s" % (names[0], sorted(doc)[:12] if isinstance(doc, dict) else type(doc)))
units = doc.get("units") if isinstance(doc, dict) else None
if isinstance(units, dict):
    keys = sorted(units)
    print("   units in that shard: %d, first five %s" % (len(units), keys[:5]))
    one = units[keys[0]]
    print("   fields: %s" % ", ".join(sorted(one))[:600])
    for f in ("body_bytes", "body_text", "entry_contract", "outcome",
              "population", "lang", "n"):
        print("      %-16s %s" % (f, json.dumps(one.get(f))[:180]))
stems = sorted(n[:-4] for n in os.listdir(
    'PseudoCoupHQ/Research/compiler_graph/diaries/regen')
    if n.endswith('.txt'))
print("   regen diary stems: %d, first five %s" % (len(stems), stems[:5]))
# how many shards would have to be opened to cover them, and do the ids match
total = 0
found = 0
seen_ids = set()
for name in names:
    d = json.load(open(os.path.join(store, name)))
    u = d.get("units") or {}
    total += len(u)
    seen_ids.update(u)
print("   units across every shard: %d, distinct ids %d" % (total, len(seen_ids)))
sample = [s for s in stems[:20]]
for s in sample[:5]:
    lang, _, rest = s.partition('__')
    print("      stem %-18s -> tried %-24s present=%s"
          % (s, "%s/%s" % (lang, rest), ("%s/%s" % (lang, rest)) in seen_ids))
hit = sum(1 for s in stems
          if ("%s/%s" % (s.split('__')[0], s.split('__', 1)[1])) in seen_ids)
print("   regen stems joining the store by lang/rest: %d of %d" % (hit, len(stems)))
PY

say "[5/5] extended = original + regen? check the union"
python3 - <<'PY'
import os
def stems(d):
    p = 'PseudoCoupHQ/Research/compiler_graph/diaries/' + d
    return set(n[:-4] for n in os.listdir(p) if n.endswith('.txt'))
ext = stems('extended'); orig = stems('c_and_cpp'); regen = stems('regen')
print("   extended %d  c_and_cpp %d  regen %d  union %d  extended==union %s"
      % (len(ext), len(orig), len(regen), len(orig | regen), ext == (orig | regen)))
PY
echo "DONE t87_l2"
