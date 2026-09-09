#!/usr/bin/env bash
# m1_l18_final_guard.sh -- task m1: the spelling guard and the `exempt`
# count re-run over the FINAL artifacts, plus the two figures the log
# asserts that no earlier lane printed on its own (the `imul` gpr_gpr 32
# attestation, and what the 83 attested cells with no table row are).
set -euo pipefail
M=/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
cd "$M"
echo "[1/3] task m1: check_no_spelling_keys.py over the four json"
echo "\$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py model_table.json model_table_rows.json model_table_attest.json model_table_edges.json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  model_table.json model_table_rows.json model_table_attest.json \
  model_table_edges.json || true
echo ""
echo "[2/3] task m1: grep -c exempt over the files this task added"
echo "\$ grep -c exempt $M/model_table.py"
grep -c exempt "$M/model_table.py" || true
echo "\$ grep -c exempt $M/model_table.md"
grep -c exempt "$M/model_table.md" || true
echo ""
echo "[3/3] task m1: the two figures the log asserts"
python3 -c "
import json
d = json.load(open('$M/model_table.json'))
for row in d['rows']:
    if row['mnem'] != 'imul':
        continue
    if row['shape'] != 'gpr_gpr' or row['width'] != 32:
        continue
    if row['outcome'] != 'TRANSLATED':
        continue
    print('imul gpr_gpr 32:', row['row_id'],
          row['attestation']['ledger_rows'], 'rows',
          row['attestation']['units'], 'units',
          [m['writes'] for m in row['mapping']])
    break
cells = d['counts']['attested_cells_with_no_translated_row']
print('attested cells with no translated row:', len(cells))
by_width = {}
for c in cells:
    by_width[c['width']] = by_width.get(c['width'], 0) + 1
print('by width:', sorted(by_width.items(), key=str))
for c in cells:
    if c['width'] != 128:
        print('not at 128:', c['mnem'], c['shape'], c['width'],
              c['ledger_rows'], 'rows')
"
echo "[3/3] done"
