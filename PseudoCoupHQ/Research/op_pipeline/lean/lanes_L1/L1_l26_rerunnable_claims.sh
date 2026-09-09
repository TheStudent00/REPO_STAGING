#!/bin/bash
# L1 lane 26 — the commands log_227 will carry so its claims re-run. The
# verifier's first pass over the log found 0 DIFFERS but also 0 MATCHES: every
# claim was prose or an attribution with nothing beside it. These are the
# same facts, stated as commands that reproduce them.
set -u
cd /projects/PseudoCoupHQ || exit 1
echo '[1/5] the ten, by outcome'
python3 -c "
import json
d = json.load(open('Research/op_pipeline/lean/L1_ten_edges.json'))
for r in d['rows']:
    print(r['type_key'], r['entry_a'], r['entry_b'], r['outcome'], r.get('cause','-'))
"
echo '[2/5] Render.lean: line count, and how many times the word appears that a hole would leave'
wc -l Research/op_pipeline/lean/archproof/Archproof/Render.lean
grep -c sorry Research/op_pipeline/lean/archproof/Archproof/Render.lean
echo '[3/5] the eighteen constructors of Term, read off the file'
python3 -c "
import re
s = open('Research/op_pipeline/lean/archproof/Archproof/Render.lean').read()
body = s.split('inductive Term')[1].split('/-- The term')[0]
names = re.findall(r'^  \| (\w+)', body, re.M)
print(len(names), names)
"
echo '[4/5] the division ladder at both SAT ceilings'
python3 -c "
import json
for f in ('L1_divide_ladder.json', 'L1_divide_ladder_t600.json'):
    d = json.load(open('Research/op_pipeline/lean/' + f))
    print(f, 'sat_timeout', d['meta']['sat_timeout_seconds'])
    for r in d['rows']:
        print('   ', r['type_key'], r['outcome'], r['wall_seconds'], 's')
"
echo '[5/5] t100 UNDECIDED pairs: how many, in which machine type keys, and how many carry a term'
python3 -c "
import json
d = json.load(open('Research/op_pipeline/pool100_edges.json'))
u = [e for e in d['pairs'] if e.get('state') == 'UNDECIDED']
k = {}
for e in u:
    k[e['type_key']] = k.get(e['type_key'], 0) + 1
print('UNDECIDED', len(u))
print('type keys', sorted(k.items(), key=lambda kv: -kv[1]))
print('carrying a term_a field', sum(1 for e in u if e.get('term_a')))
"
