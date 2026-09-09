#!/usr/bin/env bash
# m1b_l15_assemble2.sh -- task m1b: assemble and report again, after
# lane m1b_l14_coverage_detail.sh showed that the cause recorded for
# the three mnemonics attested at a form with no TRANSLATED row said
# "the sweep spells no attempt at all at shape X", which is true but
# is not the cause: all three are entries the reference registers with
# NO BUILDER, so the sweep states one NO_BUILDER row for them and no
# row at any shape. `model_table.unplaced_cause` now quotes the
# entry's own cause where there is no builder.
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B.
set -euo pipefail
echo "[1/3] task m1b: model_table.py assemble"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py assemble
echo "[2/3] task m1b: model_table.py report"
python3 model_table.py report
echo "[3/3] task m1b: the three, with the cause now quoted"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for r in d['counts']['coverage']:
    if r['category'] != 'attested at a form the sweep does not spell':
        continue
    print('   %-10s %s' % (r['mnem'], r['reason']))
"
echo "[3/3] done"
