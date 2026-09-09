#!/usr/bin/env bash
# m1b_l20_claims.sh -- task m1b: every figure the report claims, each
# printed by the command the report pastes beside it, so the verifier
# lane re-runs the same commands.
set -euo pipefail
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json

echo "[1/7] the coverage table's four totals"
python3 -c "
import json
d = json.load(open('$M'))
total = 0
for r in d['counts']['coverage_totals']:
    total = total + r['mnemonics']
    print('%3d  %s' % (r['mnemonics'], r['category']))
print('%3d  SUM' % total)
"

echo "[2/7] the counts of section 5, with the corrected join"
python3 -c "
import json
d = json.load(open('$M'))
c = d['counts']
print('table %d corpus %d both %d table_only %d corpus_only %d'
      % (c['table_mnemonics'], c['corpus_mnemonics'], c['in_both'],
         len(c['table_only']), len(c['corpus_only'])))
print('attempts %d translated %d triples %d distinct_mappings %d'
      % (c['sweep_attempts'], c['rows_translated'],
         c['translated_triples'],
         c['distinct_mappings_after_identical_text']))
print('identical_text pairs %d classes %d splits %d alias_groups %d'
      % (c['identical_text_pairs'], len(d['identical_text_classes']),
         len(c['mnemonics_with_several_mappings']),
         sum(1 for g in c['alias_groups'] if g['is_an_alias_group'])))
print('attested cells %d placed %d unplaced %d'
      % (c['attested_cells'], c['attested_cells_placed'],
         len(c['attested_cells_with_no_translated_row'])))
print('mnemonics with a placed cell %d, guard rows %d, flag-consumer rows %d'
      % (c['mnemonics_with_a_placed_cell'], c['guard_rows_total'],
         c['flag_consumer_rows']))
"

echo "[3/7] the five example rows, with their attestation"
python3 -c "
import json
d = json.load(open('$M'))
want = [('add','gpr_gpr',32), ('imul','gpr_one',32),
        ('imul','gpr_gpr',32), ('sar','cl_gpr',32),
        ('idiv','gpr_one',32)]
for mnem, shape, width in want:
    for row in d['rows']:
        if row['mnem'] != mnem or row['shape'] != shape:
            continue
        if row['width'] != width or row['outcome'] != 'TRANSLATED':
            continue
        a = row['attestation']
        print('%-6s %-8s width %-3s key_width %-4s %s rows %d units %d flag_pair %d'
              % (mnem, shape, width, row['key_width'], row['row_id'],
                 a['ledger_rows'], a['units'], a.get('flag_pair_rows', 0)))
        break
"

echo "[4/7] a flag consumer's cell, with the setter recorded on it"
python3 -c "
import json
d = json.load(open('$M'))
for row in d['rows']:
    if row['mnem'] != 'setne' or row['shape'] != 'gpr_one':
        continue
    if row['key_width'] != 8 or row['outcome'] != 'TRANSLATED':
        continue
    a = row['attestation']
    print(row['row_id'], row['text'], 'preseeded', row['preseeded'])
    print('  ledger rows %d, of which flag-pair %d, units %d'
          % (a['ledger_rows'], a['flag_pair_rows'], a['units']))
    print('  setters:', ' '.join('%s=%d' % (s['mnem'], s['ledger_rows'])
                                 for s in a['setter']))
    break
"

echo "[5/7] the x87 cells, now that the sweep spells the three shapes"
python3 -c "
import json
d = json.load(open('$M'))
seen = []
for row in d['rows']:
    if row['shape'] not in ('st_st', 'st_one', 'st_none'):
        continue
    if row['outcome'] != 'TRANSLATED':
        continue
    if row['attestation']['ledger_rows'] == 0:
        continue
    key = (row['mnem'], row['shape'])
    if key in seen:
        continue
    seen.append(key)
    print('%-10s %-8s key_width %-4s rows %d units %d'
          % (row['mnem'], row['shape'], row['key_width'],
             row['attestation']['ledger_rows'],
             row['attestation']['units']))
print('x87 cells attested at an st shape:', len(seen))
"

echo "[6/7] the cells the width rule merges"
python3 -c "
import json
d = json.load(open('$M'))
for r in d['counts']['attestation_width_merges']:
    print('%-10s %-10s key_width %-4s classifier widths %s'
          % (r['mnem'], r['shape'], r['key_width'],
             r['classifier_widths']))
"

echo "[7/7] the rows that are not placed, each with its cause"
python3 -c "
import json
d = json.load(open('$M'))
for r in d['counts']['coverage']:
    if r['category'] in ('a value cell on a TRANSLATED row',):
        continue
    if r['category'].startswith('a control transfer'):
        continue
    print('%-9s %-45s %s' % (r['mnem'], r['category'], r['reason'][:110]))
"
echo "[7/7] done"
