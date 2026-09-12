#!/bin/bash
# cov1 lane 5 -- re-run, verbatim, the commands log_266's claims cite, so
# each can be pasted as a `$ ` shell transcript per
# check_conventions_log_claims.py's shape A instead of prose. Read-only.
set -u
P=PseudoCoupHQ
OP=$P/Research/op_pipeline
COV=$P/Research/oracle/coverage
echo "[1/6] the guard, verbatim"
python3 "$OP/check_no_spelling_keys.py" "$COV/bank_x86.json" "$COV/bank_riscv64.json" "$COV/coverage_x86.json" "$COV/coverage_riscv64.json"
echo "[2/6] x86 destination-only matrix, N and M, no arrows"
python3 -c "
import json
d = json.load(open('$COV/coverage_x86.json'))
mat = d['matrices']['destination_only']
for x in ['c','cpp','rust','go','swift']:
    for y in ['c','cpp','rust','go','swift']:
        c = mat[x][y]
        print('destination_only source=%s target=%s n=%d m=%d' % (x, y, c['n'], c['m']))
"
echo "[3/6] x86 strict matrix, N and M, no arrows"
python3 -c "
import json
d = json.load(open('$COV/coverage_x86.json'))
mat = d['matrices']['strict']
for x in ['c','cpp','rust','go','swift']:
    for y in ['c','cpp','rust','go','swift']:
        c = mat[x][y]
        print('strict source=%s target=%s n=%d m=%d' % (x, y, c['n'], c['m']))
"
echo "[4/6] riscv64 matrix, both readings, N and M, no arrows"
python3 -c "
import json
d = json.load(open('$COV/coverage_riscv64.json'))
for reading in ('destination_only','strict'):
    mat = d['matrices'][reading]
    for x in ['c','go']:
        for y in ['c','cpp','go','rust']:
            c = mat[x][y]
            print('%s source=%s target=%s n=%d m=%d' % (reading, x, y, c['n'], c['m']))
"
echo "[5/6] the c/cpp identical destination-only coverage check"
python3 -c "
import json
d = json.load(open('$COV/bank_x86.json'))
cells = d['cells']
both_present = 0
same = 0
diff = 0
for entry in cells:
    t = entry['targets']
    if 'c' in t and 'cpp' in t:
        both_present = both_present + 1
        if t['c']['destination_only'] == t['cpp']['destination_only']:
            same = same + 1
        else:
            diff = diff + 1
c_only = sum(1 for e in cells if 'c' in e['targets'] and 'cpp' not in e['targets'])
print('both_present=%d same=%d diff=%d c_only_no_cpp=%d' % (both_present, same, diff, c_only))
"
echo "[6/6] riscv64 out-of-population check: c.nop must now be absent from every unit's cells"
python3 -c "
import json
population = set()
for row in json.load(open('$P/Research/oracle/riscv/twins.json'))['rows']:
    population.add((row['mnem'], row['shape'], row['key_width']))
outside = 0
nop_seen = 0
for line in open('$COV/units_riscv64.jsonl'):
    row = json.loads(line)
    for c in row['cells']:
        key = (c['mnem'], c['shape'], c['key_width'])
        if c['mnem'] == 'c.nop':
            nop_seen = nop_seen + 1
        if key not in population:
            outside = outside + 1
print('cells_outside_255_population=%d nop_cells_seen=%d' % (outside, nop_seen))
"
