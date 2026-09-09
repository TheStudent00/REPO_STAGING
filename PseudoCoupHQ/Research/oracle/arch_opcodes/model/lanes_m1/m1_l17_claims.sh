#!/usr/bin/env bash
# m1_l17_claims.sh -- task m1: run, inside the instance, exactly the
# commands the DevComms log will paste, and print each with its output
# in the `$ command` / output shape the log uses, so the log's
# transcripts are copied from a run and never typed.
set -euo pipefail
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model

run () {
    echo "\$ $1"
    eval "$1"
    echo ""
}

echo "[1/1] task m1: the log's claims, run"

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
c = d['counts']
print('table', c['table_mnemonics'], 'corpus', c['corpus_mnemonics'], 'both', c['in_both'])
print('table only', ' '.join(r['mnem'] for r in c['table_only']))
print('corpus only', ' '.join(r['mnem'] for r in c['corpus_only']) or '(none)')
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
c = d['counts']
print('attempts', c['sweep_attempts'], 'translated', c['rows_translated'])
print('triples', c['translated_triples'], 'distinct mappings', c['distinct_mappings_after_identical_text'])
print('identical_text pairs', c['identical_text_pairs'], 'classes', len(d['identical_text_classes']))
print('splits', len(c['mnemonics_with_several_mappings']))
print('alias groups', sum(1 for g in c['alias_groups'] if g['is_an_alias_group']))
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
for g in d['counts']['alias_groups']:
    if not g['is_an_alias_group']:
        continue
    print(g['group_id'], g['cells'], ' '.join(m['mnem'] for m in g['members']))
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
for r in d['counts']['mnemonics_with_several_mappings']:
    if r['mnem'] not in ('imul', 'div', 'idiv', 'mul', 'xchg'):
        continue
    print(r['mnem'], '|', ' / '.join(r['place_kind_sets']))
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
seen = {}
for cell in d['named_pair_cells']:
    key = (cell.get('destination_verdict'), cell.get('flags_verdict'), cell.get('flags_refusal'))
    seen[key] = seen.get(key, 0) + 1
print('cells', len(d['named_pair_cells']))
for key in sorted(seen, key=str):
    print(seen[key], 'x destination', key[0], 'flags', key[1], key[2])
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
for row in d['rows']:
    if row['mnem'] != 'add':
        continue
    if row['shape'] != 'gpr_gpr' or row['width'] != 32:
        continue
    if row['outcome'] != 'TRANSLATED':
        continue
    print(row['row_id'], row['text'], row['builder'])
    for m in row['mapping']:
        print(' ', m['writes'], '=', m['text'])
    print(' ', 'attestation', row['attestation']['ledger_rows'], 'rows', row['attestation']['units'], 'units')
    break
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
for outcome in sorted(d['causes']):
    total = sum(r['count'] for r in d['causes'][outcome])
    print(outcome, total, 'rows over', len(d['causes'][outcome]), 'causes')
\""

run "python3 -c \"
import json
d = json.load(open('$M/model_table.json'))
u = d['attestation_unclassified']
for cause in sorted(u, key=lambda c: -u[c]):
    print(u[cause], cause[:60])
\""

echo "[1/1] done"
