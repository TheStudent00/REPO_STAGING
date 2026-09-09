#!/usr/bin/env bash
# m1b_l24_transfers_again.sh -- task m1b: the control-transfer split
# again, with the same reading written without a bare `>`, which the
# log verifier refuses in a pasted command because bash would read it
# as a redirection.
set -euo pipefail
echo "[1/1] the control transfers, with and without guard rows"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
with_rows = []
without = []
for r in d['counts']['coverage']:
    if not r['category'].startswith('a control transfer'):
        continue
    if r['attested_by_guard_rows'] != 0:
        with_rows.append('%s=%d' % (r['mnem'], r['attested_by_guard_rows']))
    else:
        without.append(r['mnem'])
print('with guard rows (%d): %s' % (len(with_rows), ' '.join(with_rows)))
print('with none, by nature (%d): %s' % (len(without), ' '.join(without)))
"
echo "[1/1] done"
