#!/usr/bin/env bash
# ref1 lane 22 -- every transcript the report quotes, produced in one place so
# each claim carries the command that reproduces it.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
P=PseudoCoupHQ/Research/op_pipeline
total=10

echo "[1/$total] the mount and the licence's first line"
ls /sources/X86-64-semantics/
head -1 /sources/X86-64-semantics/LICENSE.md
find $S -name '*.k' | wc -l

echo "[2/$total] the bit-index convention, values in motion"
python3 -c "
import sys; sys.path.insert(0, '$L0')
import z3, k_to_z3
rule = k_to_z3.parse_file('$S/registerInstructions/addl_r32_r32.k')
env = k_to_z3.Environment()
rsi = z3.BitVecVal(0x00000000FFFFFFFF, 64)
rdi = z3.BitVecVal(0x0000000000000001, 64)
env.register_of['R1'] = rsi
env.register_of['R2'] = rdi
print('R1 is our %%rsi = 0x%016x, R2 is our %%rdi = 0x%016x' % (rsi.as_long(), rdi.as_long()))
for place, expression in rule.writes:
    value = k_to_z3.evaluate(expression, env)
    print('  %-28s = 0x%x' % (place.get('name') or ('convToRegKeys(%s)' % place['var']),
                              z3.simplify(value.term).as_long()))
"

echo "[3/$total] the function vocabulary of every regstate cell, known and not"
python3 $L0/k_to_z3.py --vocabulary $S | head -4
python3 $L0/k_to_z3.py --vocabulary $S | grep -c 'NOT KNOWN'
python3 $L0/k_to_z3.py --vocabulary $S | tail -1

echo "[4/$total] the key map's counts"
python3 -c "
import json
d = json.load(open('$L0/key_map.json'))
c = d['counts']
print('their variants %d, matched %d, unmatched %d' % (c['their_variants'], c['matched'], c['unmatched_theirs']))
print('our translated triples %d, reached %d, unmatched %d' % (c['our_translated_triples'], c['our_triples_reached'], c['unmatched_ours']))
for r in d['causes_theirs'][:6]:
    print('%6d  %s' % (r['count'], r['reason']))
"

echo "[5/$total] the check's totals"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
t = d['totals']
print('places %d: unsat %d sat %d unknown %d undefined %d refused %d'
      % (sum(t.values()), t['unsat'], t['sat'], t['unknown'], t['undefined'], t['refused']))
print('variants agreeing on every place compared %d, with a disagreement %d'
      % (d['variants_agreeing_on_every_place'], d['variants_with_a_disagreement']))
print('re-poses at the wider ceiling that fired:',
      sum(1 for v in d['variants'] for p in v['places'] if 'reposed_outcome' in p))
"

echo "[6/$total] the disagreements, by cause"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
for g in d['disagreements']:
    print('%4d  %-40s %s' % (g['count'], g['cause_key'],
          ' '.join(m['mnem'] for m in g['mnems'])))
"

echo "[7/$total] the undefined-region table"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
for r in d['undefined_regions']:
    print('%-8s whole: %-24s partial: %s' % (r['mnem'],
          ' '.join(r['whole']) or '--', ' '.join(r['partial']) or '--'))
"

echo "[8/$total] the AT&T-suffix width rule, measured on a memory destination"
python3 -c "
import sys; sys.path.insert(0, '$P')
import reference as R
s = R.MachineState()
for mnem in ('add', 'sub', 'sbb', 'xor'):
    ops = R.Operands(s, mnem, ['%esi', '(%rax)'])
    print('%-4s %%esi,(%%rax) -> destination_width %d' % (mnem, ops.destination_width()))
print('table mnemonics whose last letter is a size letter and which WIDTH_IS_NOT_A_SUFFIX does not hold:',
      len([m for m in R.REFERENCE.opcode_table.entries
           if m[-1:] in R.SIZE_LETTER and m not in R.WIDTH_IS_NOT_A_SUFFIX]))
"

echo "[9/$total] the guard, unmodified, and the exempt count over the files this task added"
python3 $P/check_no_spelling_keys.py $L0/key_map.json $L0/level0_check.json
grep -c exempt $L0/k_to_z3.py || true
grep -c exempt $L0/key_map.py || true
grep -c exempt $L0/level0_check.py || true
grep -c exempt $L0/level0_check.md || true
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
print('peak RSS of the check: %.1f MB against the stated %d MB ceiling and the named abort %s'
      % (d['meta']['peak_mb'], d['meta']['memory_ceiling_mb'], d['meta']['named_abort']))
print('wall clock %.1f s, solver ceiling %d ms, workers %d'
      % (d['meta']['seconds'], d['meta']['solver_ceiling_ms'], d['meta']['workers']))
"

echo "[10/$total] the three examples of each disagreement group, both readings and the counterexample"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
for g in d['disagreements']:
    print('=== %s -- %d places' % (g['cause_key'], g['count']))
    for e in g['examples']:
        print('  %s | our line %s | shape %s width %s | place %s'
              % (e['variant'], e['line'], e['shape'], e['key_width'], e['place']))
        print('    ours  : %s' % (e['ours'] or '')[:150])
        print('    theirs: %s' % (e['theirs'] or '')[:150])
        print('    at the counterexample: ours %s, theirs %s'
              % (e.get('ours_at_the_counterexample'), e.get('theirs_at_the_counterexample')))
        print('    counterexample: %s'
              % ', '.join('%s=%s' % (r['symbol'], r['text']) for r in (e.get('counterexample') or [])))
"
