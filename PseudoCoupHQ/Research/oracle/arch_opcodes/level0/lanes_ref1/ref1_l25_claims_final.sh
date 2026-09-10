#!/usr/bin/env bash
# ref1 lane 25 -- the final transcripts the report pastes, every command
# written so the verifier can re-run it: no redirection character anywhere in
# a command, no elision, absolute paths, deterministic output.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
P=PseudoCoupHQ/Research/op_pipeline
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json
total=9

echo "[1/$total] the mount, the licence, the file count"
ls /sources/X86-64-semantics/
head -1 /sources/X86-64-semantics/LICENSE.md
find /sources/X86-64-semantics/semantics -name '*.k' | wc -l

echo "[2/$total] the bit-index convention, values in motion"
python3 -c "
import sys; sys.path.insert(0, 'PseudoCoupHQ/Research/oracle/arch_opcodes/level0')
import z3, k_to_z3
rule = k_to_z3.parse_file('/sources/X86-64-semantics/semantics/registerInstructions/addl_r32_r32.k')
env = k_to_z3.Environment()
env.register_of['R1'] = z3.BitVecVal(0x00000000ffffffff, 64)
env.register_of['R2'] = z3.BitVecVal(0x0000000000000001, 64)
print('R1 is our %rsi = 0x00000000ffffffff, R2 is our %rdi = 0x0000000000000001')
for place, expression in rule.writes:
    value = k_to_z3.evaluate(expression, env)
    name = place.get('name') or ('convToRegKeys(%s)' % place['var'])
    print('  %-20s 0x%x' % (name, z3.simplify(value.term).as_long()))
"

echo "[3/$total] the grammar's vocabulary over every regstate cell"
python3 PseudoCoupHQ/Research/oracle/arch_opcodes/level0/k_to_z3.py --vocabulary /sources/X86-64-semantics/semantics | head -2
python3 PseudoCoupHQ/Research/oracle/arch_opcodes/level0/k_to_z3.py --vocabulary /sources/X86-64-semantics/semantics | tail -1

echo "[4/$total] the key map"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/key_map.json'))
c = d['counts']
print('their variants %d, matched %d, unmatched %d' % (c['their_variants'], c['matched'], c['unmatched_theirs']))
print('our translated triples %d, reached %d, unmatched %d' % (c['our_translated_triples'], c['our_triples_reached'], c['unmatched_ours']))
for r in d['causes_theirs'][:8]:
    print('%6d  %s' % (r['count'], r['reason']))
"

echo "[5/$total] the headline over OUR cells"
python3 -c "
import json
key = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/key_map.json'))
chk = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json'))
cells = {}
for v in chk['variants']:
    k = '%s|%s|%s' % (v['mnem'], v['shape'], v['key_width'])
    c = cells.setdefault(k, {'unsat':0,'sat':0,'unknown':0,'undefined':0,'refused':0,'rows':0})
    for p in v['places']:
        c[p['outcome']] = c[p['outcome']] + 1
    c['rows'] = max(c['rows'], v['attestation_ledger_rows'])
agree = [k for k in cells if cells[k]['sat'] == 0 and cells[k]['unsat']]
dis = [k for k in cells if cells[k]['sat']]
none = [k for k in cells if cells[k]['sat'] == 0 and cells[k]['unsat'] == 0]
print('our translated triples %d, reached by an independent reading %d' % (key['counts']['our_translated_triples'], len(cells)))
print('  agree on every place compared %4d, corpus ledger rows %d' % (len(agree), sum(cells[k]['rows'] for k in agree)))
print('  disagree on at least one place %3d, corpus ledger rows %d' % (len(dis), sum(cells[k]['rows'] for k in dis)))
print('  nothing comparable %19d, corpus ledger rows %d' % (len(none), sum(cells[k]['rows'] for k in none)))
print('  no counterpart at all %16d' % key['counts']['unmatched_ours'])
t = chk['totals']
print('places %d: unsat %d sat %d unknown %d undefined %d refused %d' % (sum(t.values()), t['unsat'], t['sat'], t['unknown'], t['undefined'], t['refused']))
print('variants agreeing on every place compared %d, with a disagreement %d' % (chk['variants_agreeing_on_every_place'], chk['variants_with_a_disagreement']))
print('re-poses at the wider ceiling that fired: %d' % sum(1 for v in chk['variants'] for p in v['places'] if 'reposed_outcome' in p))
"

echo "[6/$total] the disagreements, by cause"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json'))
for g in d['disagreements']:
    print('%4d  %-38s %s' % (g['count'], g['cause_key'], ' '.join(m['mnem'] for m in g['mnems'])))
"

echo "[7/$total] the undefined regions"
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json'))
for r in d['undefined_regions']:
    print('%-8s undefined on every input: %-24s undefined on part: %s' % (r['mnem'], ' '.join(r['whole']) or 'none', ' '.join(r['partial']) or 'none'))
"

echo "[8/$total] the AT&T size-letter width rule on a memory destination"
python3 -c "
import sys; sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline')
import reference as R
state = R.MachineState()
for mnem in ('add', 'sub', 'sbb', 'xor'):
    ops = R.Operands(state, mnem, ['%esi', '(%rax)'])
    print('destination_width of %-4s %%esi,(%%rax) is %d' % (mnem, ops.destination_width()))
print('table mnemonics whose last letter is a size letter and which WIDTH_IS_NOT_A_SUFFIX does not hold: %d' % len([m for m in R.REFERENCE.opcode_table.entries if m[-1:] in R.SIZE_LETTER and m not in R.WIDTH_IS_NOT_A_SUFFIX]))
"
python3 -c "
import json, collections
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json'))
c = collections.Counter()
for v in d['variants']:
    if v['mnem'] not in ('sub', 'sbb'):
        continue
    for p in v['places']:
        if p['outcome'] == 'sat':
            c[(v['mnem'], v['shape'])] = c[(v['mnem'], v['shape'])] + 1
for k in sorted(c, key=str):
    print('%s at shape %-10s disagrees at %d places' % (k[0], k[1], c[k]))
"

echo "[9/$total] the guard, unmodified, and the count over the files this task added"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/arch_opcodes/level0/key_map.json PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json
grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/level0/k_to_z3.py || true
grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/level0/key_map.py || true
grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.py || true
grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.md || true
python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/level0/level0_check.json'))
m = d['meta']
print('peak RSS %.1f MB, stated ceiling %d MB, named abort %s' % (m['peak_mb'], m['memory_ceiling_mb'], m['named_abort']))
print('wall clock %.1f s, solver ceiling %d ms, wide ceiling %d ms, solver processes %d' % (m['seconds'], m['solver_ceiling_ms'], m['wide_solver_ceiling_ms'], m['workers']))
"
