#!/usr/bin/env bash
# rv1 lane 6 -- section 2 again, with lane 5's three remedies in the carver:
# -nostdlibinc for the missing riscv64 headers, -M no-aliases for the
# disassembler's own spelling, --mattr for go's undeclared extensions, and
# the body bounded by the symbol's own size.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv1carve
total=4

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

echo "[4/$total] the x86 body beside the riscv64 body, per unit"
python3 -c "
import json
u = {r['unit']: r for r in json.load(open('$RV/units.json'))['rows']}
d = json.load(open('$RV/carved.json'))
for r in d['rows']:
    row = u[r['unit']]
    print('=== %s  (%s %s %s)  %s' % (r['unit'], r['mnem'], r['shape'], r['key_width'], r['outcome']))
    print('    source     : %s' % (row.get('expression'),))
    print('    x86   ship : %s' % ' ; '.join(row.get('x86_ship_body') or []))
    print('    riscv ship : %s' % ' ; '.join(r.get('body') or []))
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
