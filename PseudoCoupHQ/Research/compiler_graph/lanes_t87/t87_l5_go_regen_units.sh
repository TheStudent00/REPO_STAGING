#!/usr/bin/env bash
# t87 lane 5 — SURVEY ONLY, and a CORRECTION to lane 4's reading.
# This node's own PROGRESS entry for task 72 says the 590 go diaries
# cover 107 ORIGINAL units (canon39_wrapped_go.json) and 483
# REGENERATED ones (canon39_regen_store/op_units2_go_c000{0,1}.json).
# Lane 4 scanned for the id shape `go/op_` only and so could not see the
# regenerated ones. This lane reads the go shards of the regen store and
# settles whether all 590 diaried go probes have a machine form.
#
# THE SPELLING BAN, ABSOLUTE (the owner, 2026-08-25). Nothing here reads an
# operator field.
set -u
say() { echo; echo "======== $* ========"; }
cd /projects/PseudoCoupHQ/Research/op_pipeline

say "[1/3] the go shards of the regen store"
ls canon39_regen_store/ | grep '_go_' | head -20
python3 - <<'PY'
import json, os
store = '/projects/PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
names = sorted(n for n in os.listdir(store) if '_go_' in n)
total = 0
ids = []
for name in names:
    doc = json.load(open(os.path.join(store, name)))
    units = doc.get("units") or {}
    total += len(units)
    ids.extend(units)
    print("   %-32s %5d units, first five %s"
          % (name, len(units), sorted(units)[:5]))
print("   go units in the regen store: %d, distinct %d" % (total, len(set(ids))))
PY

say "[2/3] do the 590 go diary stems all have a machine form somewhere"
python3 - <<'PY'
import json, os
store = '/projects/PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
stems = sorted(n[:-4] for n in os.listdir(
    '/projects/PseudoCoupHQ/Research/compiler_graph/diaries/go')
    if n.endswith('.txt'))
have = {}
doc = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/'
                     'canon39_wrapped_go.json'))
for uid, unit in doc["units"].items():
    have[uid] = ("canon39_wrapped_go.json", bool(unit.get("body_bytes")))
for name in sorted(n for n in os.listdir(store) if '_go_' in n):
    d = json.load(open(os.path.join(store, name)))
    for uid, unit in (d.get("units") or {}).items():
        have[uid] = (name, bool(unit.get("body_bytes")))
print("   go unit ids with a record anywhere: %d" % len(have))
print("   a sample of those ids: %s" % sorted(have)[:6])
hit = [s for s in stems if ("go/%s" % s) in have]
miss = [s for s in stems if ("go/%s" % s) not in have]
print("   diary stems joining by go/<stem> : %d of %d" % (len(hit), len(stems)))
print("   first five that do not join       : %s" % miss[:5])
withbytes = sum(1 for s in hit if have["go/%s" % s][1])
print("   of the joins, carrying body_bytes : %d" % withbytes)
PY

say "[3/3] one regenerated go unit, shown whole in its machine-form fields"
python3 - <<'PY'
import json, os
store = '/projects/PseudoCoupHQ/Research/op_pipeline/canon39_regen_store'
name = sorted(n for n in os.listdir(store) if '_go_' in n)[0]
doc = json.load(open(os.path.join(store, name)))
units = doc["units"]
uid = sorted(units)[0]
unit = units[uid]
print("   shard %s   unit %s" % (name, uid))
for f in ("lang", "n", "unit", "operator", "population", "outcome",
          "body_bytes", "body_text", "entry_contract", "out_row"):
    print("      %-16s %s" % (f, json.dumps(unit.get(f))[:200]))
print("      ledger produced_by kinds: %s"
      % [r.get("produced_by", {}).get("kind") for r in unit.get("ledger") or []])
PY
echo "DONE t87_l5"
