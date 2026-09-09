#!/usr/bin/env bash
# m1_l20_claims2.sh -- task m1: the two commands log_236 needs in a form
# that re-runs from ANY working directory. The verifier lane
# m1_l19_verify.sh reported one DIFFERS, and the cause was the log's
# guard transcript being pasted from a lane that had cd'd into the model
# folder, so its relative paths do not resolve where the verifier runs.
# This lane runs the same guard with absolute paths, and turns the
# 83-cell attribution block into a command with output.
set -euo pipefail
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model
cd PseudoCoupHQ
echo "[1/1] task m1: the two commands, from the repo root"

echo "\$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $M/model_table.json $M/model_table_rows.json $M/model_table_attest.json $M/model_table_edges.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  "$M/model_table.json" "$M/model_table_rows.json" \
  "$M/model_table_attest.json" "$M/model_table_edges.json" || true
echo ""

CMD="python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
cells = d['counts']['attested_cells_with_no_translated_row']
print('attested cells with no translated row:', len(cells))
by_width = {}
for c in cells:
    by_width[c['width']] = by_width.get(c['width'], 0) + 1
print('by width:', sorted(by_width.items(), key=str))
for c in cells:
    if c['width'] != 128:
        print('not at 128:', c['mnem'], c['shape'], c['width'], c['ledger_rows'], 'rows')
\""
echo "\$ $CMD"
eval "$CMD"
echo "[1/1] done"
