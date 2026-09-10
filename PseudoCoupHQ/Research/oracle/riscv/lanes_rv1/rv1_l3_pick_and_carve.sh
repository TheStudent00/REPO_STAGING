#!/usr/bin/env bash
# rv1 lane 3 -- the brief's section 2: the ten cells' own corpus units
# picked from the model table's attestation, their sources compiled for
# riscv64 at the corpus's ship optimisation levels, and their bodies carved
# at the function symbol.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv1carve
total=3

echo "[1/$total] pick the ten units"
python3 $RV/pick_units.py $OP $RV/units.json

echo "[2/$total] compile for riscv64 and carve"
python3 $RV/riscv_carve.py $RV/units.json $RV/carved.json /work/rv1carve

echo "[3/$total] the instruction vocabulary these bodies spell"
python3 -c "
import json
d = json.load(open('$RV/carved.json'))
seen = {}
for r in d['rows']:
    for line in r.get('body', []):
        stem = line.split()[0]
        seen[stem] = seen.get(stem, 0) + 1
print('distinct riscv64 mnemonics over the carved bodies:', len(seen))
for k in sorted(seen, key=lambda k: (-seen[k], k)):
    print('%6d  %s' % (seen[k], k))
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
