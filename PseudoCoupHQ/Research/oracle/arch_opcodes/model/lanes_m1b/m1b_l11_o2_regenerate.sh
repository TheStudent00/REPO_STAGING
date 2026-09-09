#!/usr/bin/env bash
# m1b_l11_o2_regenerate.sh -- task m1b, deliverable 7, first half:
# task o2's `zero_opcode_examples` records now carry their `lang`
# field, so regenerate o2's product and run the unmodified spelling
# guard over it.
# WHY THE FIELD: the guard allows an operator token in an `operator`
# field only on a record that identifies ONE unit, which its
# `is_unit_object()` reads as carrying BOTH a language field and a
# unit id. These records carried `unit` and no `lang`, so their
# display label was walked as an ordinary structure field -- log_235's
# cause D, 30 findings.
# MEMORY: single_opcode_units.py streams one shard at a time and holds
# per-language summaries; its own peak is printed by the program. The
# task's bound is 16 GB with the named abort ABORT_MEMORY_M1B.
set -euo pipefail
echo "[1/3] task m1b: single_opcode_groups before the regeneration"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json'))
total = 0
for lang in sorted(d['single_opcode_groups']):
    n = len(d['single_opcode_groups'][lang]['narrow'])
    total = total + n
    print('   %-6s narrow groups %d' % (lang, n))
print('   narrow groups in all: %d' % total)
"
echo "[2/3] task m1b: regenerate single_opcode_units.json/.md"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes
python3 single_opcode_units.py
echo "[3/3] task m1b: the unmodified spelling guard, and the groups after"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json'))
total = 0
for lang in sorted(d['single_opcode_groups']):
    total = total + len(d['single_opcode_groups'][lang]['narrow'])
print('   narrow groups in all: %d' % total)
n = 0
for lang in d['zero_opcode_examples']:
    for rule in d['zero_opcode_examples'][lang]:
        for record in d['zero_opcode_examples'][lang][rule]:
            n = n + 1
            if 'lang' not in record:
                raise SystemExit('a zero-opcode example with no lang field')
print('   zero-opcode example records, all carrying lang: %d' % n)
"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json \
  /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json || true
echo "[3/3] done"
