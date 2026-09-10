#!/usr/bin/env bash
# ref1 lane 24 -- the headline the brief asks for, counted over OUR cells: of
# our model table's (mnem, shape, key_width) triples, how many an independent
# reading agrees with on every defined place, how many it disagrees with, and
# how many it has no counterpart for.
set -euo pipefail
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json
total=3

echo "[1/$total] the model table this check was run against, as it stands"
python3 -c "
import json, collections
d = json.load(open('$M'))
rows = [r for r in d['rows'] if r['outcome'] == 'TRANSLATED']
print('rows in model_table.json:', len(d['rows']))
print('TRANSLATED rows:', len(rows))
print('distinct (mnem, shape, key_width) triples:',
      len(set((r['mnem'], r['shape'], r['key_width']) for r in rows)))
print('distinct (mnem, shape, width) triples:',
      len(set((r['mnem'], r['shape'], r['width']) for r in rows)))
print('meta.task:', d['meta'].get('task'))
"

echo "[2/$total] our cells, by what an independent reading did with them"
python3 -c "
import json, collections
key = json.load(open('$L0/key_map.json'))
chk = json.load(open('$L0/level0_check.json'))
cells = {}
for v in chk['variants']:
    k = '%s|%s|%s' % (v['mnem'], v['shape'], v['key_width'])
    c = cells.setdefault(k, {'unsat':0,'sat':0,'unknown':0,'undefined':0,'refused':0,'rows':0})
    for p in v['places']:
        c[p['outcome']] = c[p['outcome']] + 1
    c['rows'] = max(c['rows'], v['attestation_ledger_rows'])
agree = [k for k,c in cells.items() if c['sat']==0 and c['unsat']>0]
dis   = [k for k,c in cells.items() if c['sat']>0]
none  = [k for k,c in cells.items() if c['sat']==0 and c['unsat']==0]
print('our cells an independent reading reached:', len(cells))
print('  agree on every place it could compare:', len(agree),
      '(corpus ledger rows behind them: %d)' % sum(cells[k]['rows'] for k in agree))
print('  disagree on at least one place:', len(dis),
      '(corpus ledger rows behind them: %d)' % sum(cells[k]['rows'] for k in dis))
print('  nothing comparable (every place undefined or refused):', len(none),
      '(corpus ledger rows behind them: %d)' % sum(cells[k]['rows'] for k in none))
print('our cells with no counterpart at all:', key['counts']['unmatched_ours'])
print('our translated triples in total:', key['counts']['our_translated_triples'])
"

echo "[3/$total] the same, counted in PLACES rather than cells"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
t = d['totals']
print('places stated by the matched variants: %d' % sum(t.values()))
print('  agree (unsat)     %d' % t['unsat'])
print('  disagree (sat)    %d' % t['sat'])
print('  unknown           %d' % t['unknown'])
print('  undefined         %d' % t['undefined'])
print('  refused           %d' % t['refused'])
"
