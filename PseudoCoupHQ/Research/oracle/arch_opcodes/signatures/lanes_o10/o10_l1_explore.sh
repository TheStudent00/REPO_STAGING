#!/bin/bash
# o10_l1_explore.sh -- task o10: enumerate every ledger row `type`
# string and `block` value across the whole canon40 corpus, before
# writing the class-inference rule ledger_signatures.py needs (IN
# rows read a holder from types101_entry_holders.json; every other
# row reads its class off its own `type` string, "unknown" unless
# that string names a class). This is exploration only, run inside
# the instance per "ALL compute through Airlock" -- no deliverable
# json is written here.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/1] task o10: enumerate ledger row type/block/produced_by.kind values"
python3 - <<'PY'
import glob
import json
import os
import resource
import sys

sys.path.insert(0, ".")
import term66_run as TR

types = {}
blocks = {}
kinds = {}
shard_paths = TR.shards()
total = len(shard_paths)
units_seen = 0
for i, path in enumerate(shard_paths, 1):
    doc = json.load(open(path))
    for name, record in doc["units"].items():
        units_seen += 1
        for row in record.get("ledger") or []:
            t = row.get("type")
            types[t] = types.get(t, 0) + 1
            b = row.get("block")
            blocks[b] = blocks.get(b, 0) + 1
            pb = row.get("produced_by") or {}
            k = pb.get("kind")
            kinds[k] = kinds.get(k, 0) + 1
    del doc
    if i % 50 == 0 or i == total:
        used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print("   [%d/%d] shards read, %d units, peak %d kB" % (i, total, units_seen, used))

print("shards", total, "units", units_seen)
print("TYPES", json.dumps(types, indent=1, sort_keys=True))
print("BLOCKS", json.dumps(blocks, indent=1, sort_keys=True))
print("KINDS", json.dumps(kinds, indent=1, sort_keys=True))
used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("collector peak %d kB" % used)
PY
echo "[1/1] done"
