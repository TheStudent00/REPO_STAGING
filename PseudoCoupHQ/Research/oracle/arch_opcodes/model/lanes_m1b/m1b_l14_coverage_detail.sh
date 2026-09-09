#!/usr/bin/env bash
# m1b_l14_coverage_detail.sh -- task m1b: the rows of the coverage
# table that are NOT placed, each with the cause the table records, so
# that every one can be read rather than summarised -- and the four
# attested cells that land on no TRANSLATED row.
set -euo pipefail
echo "[1/4] task m1b: the mnemonics attested at a form the sweep does not spell"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for r in d['counts']['coverage']:
    if r['category'] != 'attested at a form the sweep does not spell':
        continue
    print('   %-10s cells %d ledger rows %d' % (r['mnem'], r['attested_value_cells_at_an_unspelled_form'], r['ledger_rows']))
    print('      %s' % r['reason'])
"
echo "[2/4] task m1b: the mnemonics never placed"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for r in d['counts']['coverage']:
    if r['category'] != 'never placed':
        continue
    print('   %-10s corpus body lines %d' % (r['mnem'], r['corpus_occurrences']))
    print('      %s' % r['reason'])
"
echo "[3/4] task m1b: the attested cells with no TRANSLATED row"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for c in d['counts']['attested_cells_with_no_translated_row']:
    print('   %-10s %-10s width %-5s key_width %-5s rows %d units %d'
          % (c['mnem'], c['shape'], c['width'], c['key_width'], c['ledger_rows'], c['units']))
"
echo "[4/4] task m1b: the control transfers, with their guard rows"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
with_rows = 0
without = []
for r in d['counts']['coverage']:
    if not r['category'].startswith('a control transfer'):
        continue
    if r['attested_by_guard_rows'] > 0:
        with_rows = with_rows + 1
        print('   %-8s guard rows %d' % (r['mnem'], r['attested_by_guard_rows']))
    else:
        without.append(r['mnem'])
print('   with guard rows: %d; with none: %d -- %s' % (with_rows, len(without), ' '.join(without)))
"
echo "[4/4] done"
