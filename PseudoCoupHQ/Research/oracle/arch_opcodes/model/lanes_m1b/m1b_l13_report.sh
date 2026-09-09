#!/usr/bin/env bash
# m1b_l13_report.sh -- task m1b: model_table.py report, re-run after
# lane m1b_l12_assemble.sh's report step raised KeyError: 'guard_rows'
# -- the two new tables read the guard rows and the width merges at
# the document's top level, where the assembler had put them under
# `counts`. Fixed in model_table.py's own report functions; the
# assembled document itself is unchanged and is not rebuilt here.
# MEMORY: the report holds one document; the bound is the task's 16 GB
# with the named abort ABORT_MEMORY_M1B.
set -euo pipefail
echo "[1/2] task m1b: model_table.py report"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py report
echo "[2/2] task m1b: the counts the closer is judged on"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
c = d['counts']
print('   sweep attempts %d, TRANSLATED %d' % (c['sweep_attempts'], c['rows_translated']))
print('   attested cells %d, placed %d, unplaced %d'
      % (c['attested_cells'], c['attested_cells_placed'],
         len(c['attested_cells_with_no_translated_row'])))
print('   corpus mnemonics with a placed cell: %d' % c['mnemonics_with_a_placed_cell'])
print('   guard rows %d' % c['guard_rows_total'])
print('   flag-consumer ledger rows %d' % c['flag_consumer_rows'])
print('   coverage totals:')
total = 0
for r in c['coverage_totals']:
    total = total + r['mnemonics']
    print('      %-70s %d' % (r['category'], r['mnemonics']))
print('      %-70s %d' % ('SUM', total))
"
echo "[2/2] done"
