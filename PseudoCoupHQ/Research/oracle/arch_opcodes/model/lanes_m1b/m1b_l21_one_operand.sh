#!/usr/bin/env bash
# m1b_l21_one_operand.sh -- task m1b: what `reference.build_binary`'s
# corrected one-operand branch did to the table, and what the control
# transfers look like once they are counted as guard rows.
set -euo pipefail
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json

echo "[1/3] the one-operand rows of the binary family, after the fix"
python3 -c "
import json
d = json.load(open('$M'))
tally = {}
example = {}
for row in d['rows']:
    if row['shape'] not in ('gpr_one', 'mem_one'):
        continue
    if row['builder'] != 'build_binary':
        continue
    key = (row['mnem'], row['outcome'])
    tally[key] = tally.get(key, 0) + 1
    if key not in example:
        example[key] = row.get('reason') or (row.get('text') or '')
for key in sorted(tally, key=str):
    print('%-6s %-32s %2d  %s'
          % (key[0], key[1], tally[key], example[key][:96]))
"

echo "[2/3] the corpus's attestation of those same rows"
python3 -c "
import json
d = json.load(open('$M'))
total = 0
for row in d['rows']:
    if row['shape'] not in ('gpr_one', 'mem_one'):
        continue
    if row['builder'] != 'build_binary':
        continue
    total = total + row['attestation']['ledger_rows']
print('ledger rows attesting a one-operand binary-family row:', total)
"

echo "[3/3] the control transfers, with and without guard rows"
python3 -c "
import json
d = json.load(open('$M'))
with_rows = []
without = []
for r in d['counts']['coverage']:
    if not r['category'].startswith('a control transfer'):
        continue
    if r['attested_by_guard_rows'] > 0:
        with_rows.append('%s=%d' % (r['mnem'], r['attested_by_guard_rows']))
    else:
        without.append(r['mnem'])
print('with guard rows (%d): %s' % (len(with_rows), ' '.join(with_rows)))
print('with none, by nature (%d): %s' % (len(without), ' '.join(without)))
"
echo "[3/3] done"
