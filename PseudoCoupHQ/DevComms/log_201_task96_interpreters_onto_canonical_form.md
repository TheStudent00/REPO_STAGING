# log 201 — TASK 96 round 19: the eleven interpreter units onto the canonical form, and the seventh block kind

Date: 2026-09-05. Report shape: CLAUDE.md's two-list rule, then one
numbered tree, high to low, values in motion at the leaves. Where a
machine-level mechanism is explained it is shown as machine state,
stepped, with real values — `LLM_communication_protocol.md` §4.6.

Every claim below either carries a `$ ` command that reproduces it, or
says in its own line that it cannot. Commands use absolute paths so
they resolve wherever the verifier runs them.

All computation ran through Airlock, default instance, one lane per
step, `--no-batch`. The lane logs are named at §9.5 and at each
transcript.

---

# 0. The two lists

## 0.1 Decided, recorded for audit

- **The eleven interpreter units are on `canonical_form.py`.** Ten of
  the eleven wrap; the eleventh (`ruby/vm_opt_plus`) has no ship body
  and is refused by name, as it was before. No body was narrowed, no
  boundary moved: the bodies are character-for-character the ones task
  94 read off the symbol table and DWARF.
- **The `%r15` refusals are gone. All five of them.** `canonical_form
  .py` names no region base, so a body that spells `%r15` collides with
  nothing. Re-measured this lap: **0 of the 1,779** compiled units'
  wrapped texts contain that register name (§1.2).
- **The verdicts moved 10 × UNDECIDED → PROVED_BY_CONSTRUCTION**, with
  `ruby/vm_opt_plus` staying refused. **THIS IS NOT A SOLVER PROOF and
  is not reported as one**: the solver route answered for none of the
  eleven, and `gate.py`'s six mechanical checks carried all ten. §4
  gives the two apart, per unit.
- **The movement is the FORM's, not the instrument's, and that was
  measured rather than argued.** `gate.py`'s own six checks were run
  against FORM 1's text — the same instrument, the other form — and C1
  fails on every one of the five FORM 1 texts that exist. The
  structural route was never available to the region form. §4.3.
- **The seventh block kind exists: `t96_arriving_area.py`.** It follows
  `own-address`'s precedent line for line — an addressable extent, one
  uniform affine map, the unit's own spacing preserved, only the base
  moving, a displacement past the span refused by name. It answers php's
  value frame, php's bytecode pointer, cpython's two object pointers,
  ruby's `rb_big_plus` and `php/add_function`'s three zval pointers.
- **`region36.py` and `canon36_universal.py` were not modified except
  for one header block each**, saying superseded, naming this
  correction and this log. Their bodies are untouched; neither is
  imported by anything this lap wrote.
- Six new files, no existing file rewritten:
  `t96_arriving_area.py`, `t96_onto_canonical_form.py`,
  `t96_analysis.py`, `t96_step.py` and their outputs
  `t96_canonical.json`, `t96_analysis.json`, `t96_wrapped_texts.txt`.
  `canonical_form.py`, `ledger.py`, `gate.py`, `reference.py` and
  `check_no_spelling_keys.py` were imported or run UNMODIFIED.

## 0.2 Awaiting the owner

- **`AREA_SPAN` is `own-address`'s own 0x100, and two units need
  more.** `java/op_1` and `java/op_2` reach the HotSpot thread
  structure at `0x538(%r15)`. They are REFUSED BY NAME under the
  seventh kind (`arriving-area overflow`), which is exactly what
  `own_offset_of_displacement` does past `OWN_SPAN`. **Widening the
  span is a decision the tree does not answer, so it was flagged, not
  taken.** Both units still wrap under Part A. §3.4.

```
$ python3 -c "
import json
import sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import t96_arriving_area as AREA
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
print('AREA_SPAN  = 0x%x   (own-address OWN_SPAN, unchanged)' % AREA.AREA_SPAN)
print('AREA_ORIGIN= 0x%x   (measured, the identity map)' % AREA.AREA_ORIGIN)
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    if f['outcome'] != 'REFUSED':
        continue
    print('%-58s %s' % (r['unit'], f['refusal_cause']))
    print('   ', f['refusal'])
"
AREA_SPAN  = 0x100   (own-address OWN_SPAN, unchanged)
AREA_ORIGIN= 0x0   (measured, the identity map)
java/op_1                                                  arriving-area overflow
    the unit reaches its arriving area at displacement 0x538, which is further than the extent's 0x100 bytes reach; the form refuses by name rather than wrapping it
java/op_2                                                  arriving-area overflow
    the unit reaches its arriving area at displacement 0x538, which is further than the extent's 0x100 bytes reach; the form refuses by name rather than wrapping it
ruby/vm_opt_plus                                           no canonical text
    this handler has no ship body to wrap
```
- **php's frame is reached at an offset the text does not carry.**
  `0x8(%r14,%rax,1)`, where `%rax` came out of the bytecode — the owner's own
  "constants sitting in the bytecode". The recorded reach is a floor,
  never the extent, and every such area says so on its own record. What
  bounds a frame reached that way is not a thing this lap can read.
  §3.5.
- **The seventh kind changes what `IN-i` means, and the CORE's settled
  rule speaks of `IN` rows by name.** Under Part B an argument that is
  an area takes an `AREA` row, so `IN-i` becomes "the i-th value
  arrival" rather than "argument i". Every row carries its binding
  explicitly, so nothing is lost — but the CORE's sentence "IN rows are
  numbered in `arrival_contract` order" now needs one word. §3.6.
- **`gate.py`'s solver route cannot reach a Part B text at all.** Its
  binder requires one two-step load per input row; the seventh kind's
  area load is one step. So Part B is structurally proved and
  solver-unreachable by construction. §4.4.

---

# 1. The correction, and the measurement that carries it

## 1.1 The rule this lap implements

**LITERAL**, the correction in its own file:

```
$ sed -n '/^## the form, as the owner meant it/,/^WHAT WAS MISREAD/p' /projects/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md
## the form, as the owner meant it — CORRECTION 2026-09-05

**The arch-unit is essentially UNCHANGED except for the loading and
unloading of registers into a virtual memory.** the owner, 2026-09-05,
correcting how his 2026-09-02 ruling was read: "you mean my
misinterpreted words? the arch-unit is supposed to be essentially
unchanged except for the loading/unloading of registers into a
virtual memory."

WHAT WAS MISREAD. `region36.py:10` quotes the 2026-09-02 ruling
```

## 1.2 The `%r15` count, re-run

Lane log: `~/Programming/Airlock/agent/logs/20260905T072317Z__t96_l9_r15count.sh.log`.

```
$ python3 -c "
import json
total = 0
hits = 0
seen = 0
for lang in ('c', 'cpp', 'go', 'rust', 'swift'):
    units = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_%s.json' % lang))['units']
    total = total + len(units)
    for label in units:
        text = units[label].get('wrapped_text')
        if text is None:
            continue
        seen = seen + 1
        if '%r15' in text:
            hits = hits + 1
print('compiled units in the canon40 render : %d' % total)
print('of those, carrying a wrapped text    : %d' % seen)
print('wrapped texts containing the r15 name: %d' % hits)
"
compiled units in the canon40 render : 1779
of those, carrying a wrapped text    : 1763
wrapped texts containing the r15 name: 0
```

**GLOSS, with the population said rather than rounded.** The brief's
figure is 1,779 and that is the render's own unit count. Of those,
1,763 carry a wrapped text; the other **16 are refusals** and have no
text to contain anything. So the honest sentence is: 0 of 1,763
wrapped texts, out of a population of 1,779 units.

The same count without a JSON loader in the way, same lane log:

```
$ grep -o '"wrapped_text": "[^"]*%r15[^"]*"' /projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_c.json /projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_cpp.json /projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_go.json /projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_rust.json /projects/PseudoCoupHQ/Research/op_pipeline/canon40_wrapped_swift.json | wc -l
0
```

---

# 2. PART A — the eleven onto `canonical_form.py`

## 2.1 The two forms, on one body, side by side

`cpython/long_add`, 92 instructions. FORM 1 is `region36` +
`canon36_universal` as task 94 rendered it, READ from
`t94_recarve.json` and never re-run. FORM 2 is
`canonical_form.CanonicalForm.wrap`, unmodified.

Lane log: `~/Programming/Airlock/agent/logs/20260905T071648Z__t96_l5_analysis.sh.log` (the full three-way dump for all eleven is `t96_wrapped_texts.txt`).

**LITERAL**, the first eight lines and last six of each:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
r = [x for x in d['records'] if x['unit'].startswith('cpython')][0]
for title, text in (('FORM 1, region36 + canon36_universal', r['the_superseded_form']['wrapped_text']), ('FORM 2, canonical_form.py', r['the_canonical_form']['wrapped_text'])):
    lines = text.split('; ')
    print('%s -- %d lines' % (title, len(lines)))
    for line in lines[:8]:
        print('   ', line)
    print('    [%d lines not printed]' % (len(lines) - 14))
    for line in lines[-6:]:
        print('   ', line)
    print()
"
FORM 1, region36 + canon36_universal -- 137 lines
    L0:
    mov 0x0(%r15),%r10
    mov 0x8(%r15),%r11
    mov 0x40(%r15),%rdi
    sub %rdi,%rsp
    mov 0x10(%r10),%rax
    mov 0x10(%r11),%rcx
    mov %r11,%rdx
    [123 lines not printed]
    jmp L11
    nopl 0x0(%rax,%rax,1)
    L18:
    mov 0x40(%r15),%rdi
    add %rdi,%rsp
    jmp 131fe0 <_PyLong_FromMedium>

FORM 2, canonical_form.py -- 105 lines
    mov ledger+0x00(%rip),%rdi
    mov 0x0(%rdi),%rdi
    mov ledger+0x00(%rip),%rsi
    mov 0x8(%rsi),%rsi
    sub $0x28,%rsp
    mov 0x10(%rdi),%rax
    mov 0x10(%rsi),%rdx
    mov %rsi,%rcx
    [91 lines not printed]
    lea 0x36f0(%rax,%rdi,1),%rax
    jmp L2
    nopl 0x0(%rax,%rax,1)
    L6:
    add $0x28,%rsp
    jmp x__PyLong_FromMedium
```

**GLOSS, the difference read off those lines and nothing else.**

| what the compiler emitted | FORM 1 made it | FORM 2 made it |
|---|---|---|
| `sub $0x28,%rsp` | `mov 0x40(%r15),%rdi` then `sub %rdi,%rsp` — the immediate 0x28 moved into a constant block and read back through the region base | `sub $0x28,%rsp` |
| `mov 0x10(%rdi),%rax` | `mov 0x10(%r10),%rax` — `%rdi` renamed to `%r10` by rule R | `mov 0x10(%rdi),%rax` |
| `mov 0x10(%rsi),%rdx` | `mov 0x10(%r11),%rcx` — both operands renamed | `mov 0x10(%rsi),%rdx` |

FORM 1 rewrote the body. FORM 2 did not touch it: the four lines
before it are the prelude, the two before each `ret` are the epilogue,
and everything between is what `objdump` printed.

## 2.2 What FORM 2 does change, said plainly

The word "verbatim" is exact about registers, immediates and stack
addresses, and it is NOT exact about transfer targets — the form's own
positional-label rule (`ledger.positional_labels`) rewrites those, and
`gate.py` has a whole check, C6, for it. Above:
`jmp 131fe0 <_PyLong_FromMedium>` became `jmp x__PyLong_FromMedium`,
and an in-unit target became `L2`.

**LITERAL**, C6's own count for `php/add_function`, lane log
`20260905T072242Z__t96_l8_transcripts.sh.log` §[5/8]:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
r = [x for x in d['records'] if x['unit'].startswith('php/add_function')][0]
for c in r['form_two']['the_six_checks']:
    print('%-12s %-5s %s' % (c['check'], c['passed'], c['note'][:150]))
"
check_one    True  C1: the body appears in the wrapped text character-for-character and in its own order -- no register was renamed, no immediate was moved, no stack add
check_two    True  C2: the prelude writes only the registers the arrival contract names, one two-step load per input row
check_three  True  C3: every one of the 2 returns is immediately preceded by the epilogue, which stores the compiler's own result register into OUT-0
check_four   True  C4: no body line names the ledger symbol or any ledger row, so the body and the plumbing touch disjoint text
check_five   True  C5: the epilogue's pointer register %r11 is not the result register %rax, so loading the block base cannot destroy the answer
check_six    True  C6: the only text this form changed inside the body is the TARGET operand of 12 transfer(s); every mnemonic, every other operand and every trailing an
```

## 2.3 The five `%r15` refusals, gone

Under FORM 1, five of the eleven never reached a gate: the two JIT
nmethods, refused because the core names the region base, and the three
php `ZEND_ADD_*` handlers, refused one step earlier for the same
collision. Under FORM 2 all five wrap.

**LITERAL**, the refusal that no longer fires, quoted from the
superseded record it is stored in:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    old = r['the_superseded_form']
    if old['wrapped_text'] is not None:
        continue
    print(r['unit'])
    print('   ', (old['refusal'] or '')[:150])
"
java/op_1
    the universal form refused by name: the core names the region base -- this unit's own core mentions %r15, which the form rules to be the region base a
java/op_2
    the universal form refused by name: the core names the region base -- this unit's own core mentions %r15, which the form rules to be the region base a
ruby/vm_opt_plus
    no STT_FUNC symbol named 'vm_opt_plus' exists in this binary's own symbol table, so this handler's function bounds cannot be read here
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER
    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15, which region36 rules to be the region base and t
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER
    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15, which region36 rules to be the region base and t
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER
    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15, which region36 rules to be the region base and t
```

`php/add_function` does not appear: it is the one of the six with a
FORM 1 text, so the loop skips it.

## 2.4 What Part A alone does NOT do, and it matters

For the three php `ZEND_ADD_*` handlers, DWARF records zero formal
parameters, so the arrival contract is empty, so **FORM 2's prelude is
empty**. The unit wraps, the answer is stored, and nothing in the form
says where its operands came from.

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form']
    if f['outcome'] == 'REFUSED':
        continue
    print('%-58s prelude %s' % (r['unit'], f['prelude']))
"
cpython/long_add_fastpath                                  prelude ['mov ledger+0x00(%rip),%rdi', 'mov 0x0(%rdi),%rdi', 'mov ledger+0x00(%rip),%rsi', 'mov 0x8(%rsi),%rsi']
java/op_1                                                  prelude ['mov ledger+0x00(%rip),%rsi', 'mov 0x0(%rsi),%rsi', 'mov ledger+0x00(%rip),%rdx', 'mov 0x8(%rdx),%rdx']
java/op_2                                                  prelude ['mov ledger+0x00(%rip),%rsi', 'mov 0x0(%rsi),%rsi', 'mov ledger+0x00(%rip),%rdx', 'mov 0x8(%rdx),%rdx']
ruby/rb_fix_plus                                           prelude ['mov ledger+0x00(%rip),%rdi', 'mov 0x0(%rdi),%rdi', 'mov ledger+0x00(%rip),%rsi', 'mov 0x8(%rsi),%rsi']
ruby/rb_int_plus                                           prelude ['mov ledger+0x00(%rip),%rdi', 'mov 0x0(%rdi),%rdi', 'mov ledger+0x00(%rip),%rsi', 'mov 0x8(%rsi),%rsi']
ruby/rb_big_plus                                           prelude ['mov ledger+0x00(%rip),%rdi', 'mov 0x0(%rdi),%rdi', 'mov ledger+0x00(%rip),%rsi', 'mov 0x8(%rsi),%rsi']
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                prelude []
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           prelude []
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER prelude []
php/add_function                                           prelude ['mov ledger+0x00(%rip),%rsi', 'mov 0x0(%rsi),%rsi', 'mov ledger+0x00(%rip),%rdx', 'mov 0x8(%rdx),%rdx']
```

An empty prelude passes C2 vacuously. **A php handler's PROVED_BY_
CONSTRUCTION under Part A therefore certifies that the body is intact
and the plumbing is disjoint from it, and certifies nothing about where
the operands arrive.** That is precisely the hole Part B fills, and §3.3
shows the two forms' entry rows side by side so the hole is visible
rather than asserted.

---

# 3. PART B — the seventh block kind, an arriving addressable area

## 3.1 The precedent, and the one word that changes

| `own-address`, region36 §3 and §7 | the seventh kind, `t96_arriving_area.py` |
|---|---|
| an addressable AREA, 0x100 bytes | an addressable AREA, `AREA_SPAN` = 0x100 bytes per extent |
| "an affine image, not a slot series" | the same words; extent `i` at `0x100 * i`, identity map inside it |
| "the same constant for every displacement in every unit, so the unit's own internal spacing is preserved exactly and only the base moves" | the same sentence; the constant is `AREA_ORIGIN`, measured to 0 |
| evidence: a stack address whose ADDRESS ESCAPES (a line takes its `lea`) | evidence: a family the body DEREFERENCES before the body has written it |
| a displacement past `OWN_SPAN` is refused by name (`own-block overflow`) | a displacement past `AREA_SPAN` is refused by name (`arriving-area overflow`) |
| the unit's OWN scratch | an area that ARRIVES |

`AREA_ORIGIN` was measured, not chosen. Lane log
`20260905T071936Z__t96_l6_render2.sh.log` §[1/6]: the smallest
displacement any of the eleven bodies spells from an arriving base is
`0x0`, so the origin is 0 and the map is the plain identity. No
constant was invented.

## 3.2 The evidence, per unit, as the walk found it

Lane log: `20260905T072242Z__t96_l8_transcripts.sh.log` §[7/8].

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    areas = f.get('arriving_areas') or []
    if not areas:
        print('%-58s no arriving area' % r['unit'])
        continue
    for a in areas:
        print('%-58s %%%-4s 0x%x .. 0x%x  n=%-2d indexed=%-5s advanced=%s' % (r['unit'], a['base_family'], a['smallest_displacement'], a['largest_displacement'], a['sightings'], a['reached_through_an_index_register'], len(a['advanced_by'])))
"
cpython/long_add_fastpath                                  %rdi  0x10 .. 0x10  n=1  indexed=False advanced=0
cpython/long_add_fastpath                                  %rsi  0x10 .. 0x18  n=3  indexed=False advanced=0
java/op_1                                                  %r15  0x20 .. 0x538  n=3  indexed=False advanced=0
java/op_2                                                  %r15  0x20 .. 0x538  n=3  indexed=False advanced=0
ruby/vm_opt_plus                                           no arriving area
ruby/rb_fix_plus                                           no arriving area
ruby/rb_int_plus                                           no arriving area
ruby/rb_big_plus                                           %rdi  0x1 .. 0x1  n=1  indexed=False advanced=0
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                %r15  0x8 .. 0x10  n=4  indexed=False advanced=1
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                %r14  0x0 .. 0x8  n=2  indexed=True  advanced=0
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           %r15  0x8 .. 0x10  n=3  indexed=False advanced=1
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER %r15  0x8 .. 0x10  n=3  indexed=False advanced=1
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER %r14  0x0 .. 0x8  n=4  indexed=True  advanced=0
php/add_function                                           %rsi  0x0 .. 0x8  n=6  indexed=False advanced=0
php/add_function                                           %rdx  0x0 .. 0x8  n=6  indexed=False advanced=0
php/add_function                                           %rdi  0x0 .. 0x8  n=10 indexed=False advanced=0
```

**GLOSS.** `ruby/rb_fix_plus` and `ruby/rb_int_plus` have no arriving
area, and that is correct rather than a miss: they take Fixnums, which
are tagged immediates, and they never reach through either arriving
register before writing it. `php/add_function`'s third area is `%rdi`,
the `zval *result` DWARF names as its first parameter — the answer's
home, which arrives as an area and was never in the operand contract.

Three rules the walk needed, each stated because a body forced it:

1. **`lea` is not a dereference.** `java/op_1` spells
   `lea (%rsi,%rdx,1),%eax` — two values being added. Before this rule
   the walk called `%rsi` an area (lane log
   `20260905T070835Z__t96_l2_survey.sh.log`); after it, it does not
   (lane log `20260905T071056Z__t96_l3_survey2.sh.log`).
2. **A copy of a base names the same area.** `cpython/long_add` reads
   `0x18(%rcx)` where `%rcx` holds a copy of `%rsi`; that is why
   `%rsi`'s reach is `0x10 .. 0x18` and not `0x10 .. 0x10`.
3. **A base advanced by a constant names the same area, shifted** —
   `own-address`'s affine image itself. php advances its bytecode
   pointer with `add $0x20,%r15` and then reads `-0x10(%r15)`; that is
   the same area at `0x20 - 0x10 = 0x10`, which is why `%r15`'s reach
   is `0x8 .. 0x10` and not `0x8 .. 0xc`.

## 3.3 THE MECHANISM, AS MACHINE STATE, STEPPED (§4.6)

`php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER` — the
one straight-line whole handler in the population, ten instructions.
The instructions are read from `t96_canonical.json`; the addresses and
the two integers are an illustrative instantiation of a real body, said
once. Everything else is computed by the stepper from the instruction
text.

Lane log: `~/Programming/Airlock/agent/logs/20260905T072154Z__t96_l7_step.sh.log`.

**The instantiation**

| name | address | holds |
|---|---|---|
| the ledger | `0x600000` | its `OUT` entry (`+0x38`) holds `0x500000`; its `AREA` entry (`+0x40`) holds `0x700000` |
| `AREA-0`, extent `0x000` | `0x700000` | the bytecode: slot `0x00` at `+0x8`, slot `0x10` at `+0xc`, and one opcode on (`+0x20`), slot `0x20` at `+0x10` |
| `AREA-1`, extent `0x100` | `0x700100` | the value frame: the php integer 3 at `+0x00`, 4 at `+0x10` |
| `OUT-0` | `0x500000` | the answer |

**FORM 1 — region36.** There is no state to step. The form refused
this unit before rendering it, in its own words: *"this handler
declares ZERO formal parameters and reads its operands out of the VM
frame through `%r15`, which region36 rules to be the region base and
therefore not available to any lineage."*

**FORM 2 — `canonical_form.py`, Part A.**

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '21,35p'
step instruction                        %r15       %r14       %rcx       %rax       %rdx       %r11      
---------------------------------------------------------------------------------------------------------
--   (entry)                            0x700000   0x700100   ?          ?          ?          ?         
0    endbr64                            0x700000   0x700100   ?          ?          ?          ?         
1    movslq 0x8(%r15),%rcx              0x700000   0x700100   0x0        ?          ?          ?         
2    movslq 0xc(%r15),%rax              0x700000   0x700100   0x0        0x10       ?          ?         
3    add $0x20,%r15                     0x700020   0x700100   0x0        0x10       ?          ?         
4    movslq -0x10(%r15),%rdx            0x700020   0x700100   0x0        0x10       0x20       ?         
5    mov (%r14,%rax,1),%rax             0x700020   0x700100   0x0        0x4        0x20       ?         
6    add (%r14,%rcx,1),%rax             0x700020   0x700100   0x0        0x7        0x20       ?         
7    mov %rax,(%r14,%rdx,1)             0x700020   0x700100   0x0        0x7        0x20       ?         
8    movl $0x4,0x8(%r14,%rdx,1)         0x700020   0x700100   0x0        0x7        0x20       ?         
9    mov ledger+0x38(%rip),%r11         0x700020   0x700100   0x0        0x7        0x20       0x500000  
10   mov %rax,0x0(%r11)                 0x700020   0x700100   0x0        0x7        0x20       0x500000  
11   ret                                0x700020   0x700100   0x0        0x7        0x20       0x500000  
```

**READ THE `(entry)` ROW.** `%r15` and `%r14` are already filled, and
NOTHING in FORM 2 put them there. The stepper had to be handed them.

**FORM 3 — the same, plus the seventh block kind, Part B.**

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '67,84p'
step instruction                        %r15       %r14       %rcx       %rax       %rdx       %r11      
---------------------------------------------------------------------------------------------------------
--   (entry)                            ?          ?          ?          ?          ?          ?         
0    mov ledger+0x40(%rip),%r15         0x700000   ?          ?          ?          ?          ?         
1    mov ledger+0x40(%rip),%r14         0x700000   0x700000   ?          ?          ?          ?         
2    lea 0x100(%r14),%r14               0x700000   0x700100   ?          ?          ?          ?         
3    endbr64                            0x700000   0x700100   ?          ?          ?          ?         
4    movslq 0x8(%r15),%rcx              0x700000   0x700100   0x0        ?          ?          ?         
5    movslq 0xc(%r15),%rax              0x700000   0x700100   0x0        0x10       ?          ?         
6    add $0x20,%r15                     0x700020   0x700100   0x0        0x10       ?          ?         
7    movslq -0x10(%r15),%rdx            0x700020   0x700100   0x0        0x10       0x20       ?         
8    mov (%r14,%rax,1),%rax             0x700020   0x700100   0x0        0x4        0x20       ?         
9    add (%r14,%rcx,1),%rax             0x700020   0x700100   0x0        0x7        0x20       ?         
10   mov %rax,(%r14,%rdx,1)             0x700020   0x700100   0x0        0x7        0x20       ?         
11   movl $0x4,0x8(%r14,%rdx,1)         0x700020   0x700100   0x0        0x7        0x20       ?         
12   mov ledger+0x38(%rip),%r11         0x700020   0x700100   0x0        0x7        0x20       0x500000  
13   mov %rax,0x0(%r11)                 0x700020   0x700100   0x0        0x7        0x20       0x500000  
14   ret                                0x700020   0x700100   0x0        0x7        0x20       0x500000  
```

**READ THE `(entry)` ROW.** Every register starts unknown. Steps 0–2
are the form's own prelude and they fill `%r15` and `%r14` out of the
ledger. Steps 3–11 are byte-identical to FORM 2's steps 0–8. Both
forms leave `0x7` in `OUT-0`.

**The memory at the end, identical under both forms**, same lane log:

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '52,59p'
  0x500000     OUT-0 (the answer) + 0x0           0x7
  0x700008     AREA-0 (the bytecode) + 0x8        0x0
  0x70000c     AREA-0 (the bytecode) + 0xc        0x10
  0x700010     AREA-0 (the bytecode) + 0x10       0x20
  0x700100     AREA-1 (the value frame) + 0x0     0x3
  0x700110     AREA-1 (the value frame) + 0x10    0x4
  0x700120     AREA-1 (the value frame) + 0x20    0x7
  0x700128     AREA-1 (the value frame) + 0x28    0x4
```

**GLOSS, one sentence and no more.** Steps 0–2 are the whole of the
seventh block kind: an area that arrives gets its BASE loaded in ONE
step (plus a `lea` when its extent is not the block's own base), where
a value that arrives gets its CONTENTS loaded in TWO. An address, not a
value — which is `own-address`'s "affine image, not a slot series",
written as a prelude line instead of as a rewrite.

## 3.4 The two units the seventh kind refuses, by name

`java/op_1` and `java/op_2` reach `0x538(%r15)` — HotSpot's thread
structure. `0x538` is past `AREA_SPAN` (0x100), so both are refused
with `arriving-area overflow`, which is `own_offset_of_displacement`'s
refusal shape.

**`AREA_SPAN` was not widened.** 0x100 is `own-address`'s own constant;
changing it is a decision the tree does not answer. Both units wrap
under Part A regardless, so nothing is lost by flagging it. §0.2.

## 3.5 The reach the text does not carry

php reaches its value frame as `0x8(%r14,%rax,1)`, where `%rax` was
read out of the bytecode. Two of the areas above carry
`indexed=True`, and their record says in its own words that the
recorded reach is a floor:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    for a in (f.get('arriving_areas') or []):
        if not a['reached_through_an_index_register']:
            continue
        print('%s  %%%s' % (r['unit'], a['base_family']))
        print('   ', a['the_reach_is_a_floor_not_the_extent'])
        break
"
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER  %r14
    this area is reached with an index register, so the byte the body lands on is the displacement above PLUS whatever the index holds at run time; the recorded reach is a floor and the extent this body needs is not readable from its text
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER  %r14
    this area is reached with an index register, so the byte the body lands on is the displacement above PLUS whatever the index holds at run time; the recorded reach is a floor and the extent this body needs is not readable from its text
```

## 3.6 What the seventh kind costs, said rather than hidden

- **`IN-i` changes meaning.** An argument that is an area takes an
  `AREA` row, so `IN-0` under Part B is the first VALUE arrival, not
  argument 0. Visible in `ruby/rb_big_plus`, whose `%rdi` is an area
  and whose `%rsi` is a value: its Part B prelude is
  `['mov ledger+0x40(%rip),%rdi', 'mov ledger+0x00(%rip),%rsi', 'mov 0x0(%rsi),%rsi']`.
  Every row carries `bound_to_the_same_symbol_as`, so no binding is
  lost. Flagged at §0.2.
- **Attribution across a branching body is by TEXT ORDER**, which is
  `Ledger.walk_dataflow`'s own order. In a body with branches, an
  area's recorded reach is the union over text order rather than
  per-path. For `cpython/long_add` this makes both areas read `0x10 ..
  0x18`; both are inside the extent either way, so nothing here turns
  on it.
- **A base changed by anything other than a plain move or a constant
  add or subtract is dropped**, and a later reach through it is
  unattributed. None occurs in this population.

---

# 4. PART C — the gate, against each unit's OWN ship code

## 4.1 The movement, all eleven, three forms

Baseline is log_199's, quoted from its own file:

```
$ grep -n "9 PROVED to UNDECIDED" /projects/PseudoCoupHQ/DevComms/log_199_task94_interpreter_function_bodies.md | head -3
26:- **All eleven verdicts moved: 9 PROVED to UNDECIDED, 1
```

— 9 PROVED→UNDECIDED, 1 NO_CANONICAL_TEXT→UNDECIDED, 1 →NO_BODY.
Nothing proved.

Lane log: `20260905T072242Z__t96_l8_transcripts.sh.log` §[2/8].

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for m in d['verdict_movements']:
    print('%-58s %-18s | %-22s | %s' % (m['unit'], m['from'], m['to_form_two'], m['to_form_three']))
"
cpython/long_add_fastpath                                  UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
java/op_1                                                  UNDECIDED          | PROVED_BY_CONSTRUCTION | REFUSED: arriving-area overflow
java/op_2                                                  UNDECIDED          | PROVED_BY_CONSTRUCTION | REFUSED: arriving-area overflow
ruby/vm_opt_plus                                           NO_BODY            | REFUSED: no canonical text | REFUSED: no canonical text
ruby/rb_fix_plus                                           UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
ruby/rb_int_plus                                           UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
ruby/rb_big_plus                                           UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
php/add_function                                           UNDECIDED          | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION
```

Read as a table, with the cause of each movement:

| unit | log_199 | Part A | Part B | cause of the movement |
|---|---|---|---|---|
| cpython/long_add | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | the form stopped rewriting the body, so C1 can be asked and passes |
| java/op_1 | UNDECIDED | PROVED_BY_CONSTRUCTION | REFUSED `arriving-area overflow` | Part A: the `%r15` refusal is gone. Part B: `0x538` is past the extent |
| java/op_2 | UNDECIDED | PROVED_BY_CONSTRUCTION | REFUSED `arriving-area overflow` | as above |
| ruby/vm_opt_plus | NO_BODY | REFUSED `no canonical text` | REFUSED `no canonical text` | unchanged: the optimiser inlined the symbol away; there is no body |
| ruby/rb_fix_plus | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | C1 passes; no arriving area, so Part B is Part A |
| ruby/rb_int_plus | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | as above |
| ruby/rb_big_plus | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | C1 passes; one arriving area (`%rdi`) |
| php/ZEND_ADD_SPEC_… | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | the `%r15` refusal is gone; Part B declares two arriving areas |
| php/ZEND_ADD_LONG_SPEC_… | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | as above, one area |
| php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_… | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | as above, two areas |
| php/add_function | UNDECIDED | PROVED_BY_CONSTRUCTION | PROVED_BY_CONSTRUCTION | C1 passes; three arriving areas including the answer's home |

## 4.2 WHAT `PROVED_BY_CONSTRUCTION` IS, AND WHAT IT IS NOT

**The solver answered for none of the eleven.** Every verdict above is
the structural route, and `gate.py`'s own wording for it is: *"the
reference has no model for something this body spells (X), and the form
applies NO transformation to the body, so the six mechanical checks
carry it"*.

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
for r in d['records']:
    for name in ('form_two', 'form_three'):
        row = r[name]
        if row['outcome'] == 'REFUSED':
            continue
        passed = len([c for c in row['the_six_checks'] if c['passed']])
        print('%-58s %-11s %-22s checks %d/6  solver_answered=%s  120000ms=%s' % (r['unit'], name, row['verdict'], passed, row['solver_route']['the_solver_answered'], (row['gate_at_120000ms'] or {}).get('verdict')))
"
cpython/long_add_fastpath                                  form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
cpython/long_add_fastpath                                  form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
java/op_1                                                  form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
java/op_2                                                  form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_fix_plus                                           form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_fix_plus                                           form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_int_plus                                           form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_int_plus                                           form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_big_plus                                           form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
ruby/rb_big_plus                                           form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/add_function                                           form_two    PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
php/add_function                                           form_three  PROVED_BY_CONSTRUCTION checks 6/6  solver_answered=False  120000ms=NOT_RUN
```

(the command above skips the REFUSED rows by its own `continue`;
§4.1 lists them. `java/op_1` and `java/op_2` therefore appear once
each, under `form_two` only.)

**THIS PARAGRAPH CARRIES NOTHING TO RE-RUN**: it is what the verdict
MEANS, read off `gate.py`'s six check methods, and a command cannot
settle a meaning. The claim these ten verdicts carry is exactly this
and nothing more: the compiler's body is present in the wrapped text unchanged
except for transfer targets (C1, C6), the added plumbing writes only
what the arrival contract names plus one scratch (C2), every `ret` is
preceded by the store into `OUT-0` (C3), the body and the plumbing
touch disjoint text (C4), and the epilogue's pointer is not the answer
register (C5). It is NOT a claim that z3 proved the two answers equal.

## 4.3 THE INSTRUMENT QUESTION, measured rather than argued

Two things differ between log_199's baseline and this lap: the FORM,
and the GATE (task 94's `gate_against_own_ship` is solver-only; this
lap uses `gate.py`, which has the structural route). So: **would the
structural route have carried FORM 1's texts?**

`gate.py`'s own six checks, run against the five FORM 1 texts that
exist. Lane log `20260905T072242Z__t96_l8_transcripts.sh.log` §[3/8].

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
for r in d['records']:
    one = r['form_one_under_this_instrument']
    if not one.get('asked'):
        print('%-58s not asked (no FORM 1 text)' % r['unit'])
        continue
    f = one['the_first_failure']
    print('%-58s available=%-5s  %s' % (r['unit'], one['the_structural_route_is_available_to_form_one'], f['note'][:110]))
print()
print(json.dumps(d['the_instrument_question'], indent=1, sort_keys=True))
"
cpython/long_add_fastpath                                  available=False  C1 fails: the wrapped text does not carry the body character-for-character; unaccounted lines ['mov 0x0(%r15),
java/op_1                                                  not asked (no FORM 1 text)
java/op_2                                                  not asked (no FORM 1 text)
ruby/vm_opt_plus                                           not asked (no FORM 1 text)
ruby/rb_fix_plus                                           available=False  C1 fails: the wrapped text does not carry the body character-for-character; unaccounted lines ['mov 0x0(%r15),
ruby/rb_int_plus                                           available=False  C1 fails: the wrapped text does not carry the body character-for-character; unaccounted lines ['mov 0x0(%r15),
ruby/rb_big_plus                                           available=False  C1 fails: the wrapped text does not carry the body character-for-character; unaccounted lines ['mov 0x0(%r15),
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                not asked (no FORM 1 text)
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           not asked (no FORM 1 text)
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER not asked (no FORM 1 text)
php/add_function                                           available=False  C1 fails: the wrapped text does not carry the body character-for-character; unaccounted lines ['mov 0x0(%r15),

{
 "form_one_texts_asked": 5,
 "form_one_texts_the_structural_route_would_carry": 0,
 "reading": "if this is 0, gate.py's structural route was never available to the region form, so the instrument difference between log_199 and this lap is the FORM difference and not a second cause"
}
```

**0 of 5.** The structural route was never available to the region
form, and the reason is the form itself: a form that rewrites the body
cannot make C1's claim. The instrument difference is the form
difference wearing another hat.

## 4.4 A cost of Part B: the solver route becomes unreachable

Under Part A the solver route stops on an unmodelled opcode. Under
Part B it stops EARLIER, on the prelude's own shape:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
for r in d['records']:
    for name in ('form_two', 'form_three'):
        row = r[name]
        if row['outcome'] == 'REFUSED':
            continue
        s = row['solver_route']['what_it_had_no_model_for']
        if s is None:
            continue
        print('%-46s %-11s %s' % (r['unit'][:46], name, s[:96]))
"
cpython/long_add_fastpath                      form_two    arch opcode 'jmp' is a census row, not a silent gap: a transfer or trap, and this reference walk
cpython/long_add_fastpath                      form_three  this unit's prelude is not one two-step load per input row (3 lines for 2 loads), so the input r
java/op_1                                      form_two    arch opcode 'cmpl' has no entry in the opcode table -- no body in the corpus this table was buil
java/op_2                                      form_two    arch opcode 'cmpl' has no entry in the opcode table -- no body in the corpus this table was buil
ruby/rb_fix_plus                               form_two    arch opcode 'call' is a census row, not a silent gap: runtime callee not yet attached (Task 59, 
ruby/rb_fix_plus                               form_three  arch opcode 'call' is a census row, not a silent gap: runtime callee not yet attached (Task 59, 
ruby/rb_int_plus                               form_two    arch opcode 'call' is a census row, not a silent gap: runtime callee not yet attached (Task 59, 
ruby/rb_int_plus                               form_three  arch opcode 'call' is a census row, not a silent gap: runtime callee not yet attached (Task 59, 
ruby/rb_big_plus                               form_two    arch opcode 'jmp' is a census row, not a silent gap: a transfer or trap, and this reference walk
ruby/rb_big_plus                               form_three  this unit's prelude is not one two-step load per input row (3 lines for 2 loads), so the input r
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER    form_two    arch opcode 'movl' has no entry in the opcode table -- no body in the corpus this table was buil
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER    form_three  this unit's prelude is not one two-step load per input row (3 lines for 2 loads), so the input r
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDL form_two    arch opcode 'movl' has no entry in the opcode table -- no body in the corpus this table was buil
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDL form_three  this unit's prelude is not one two-step load per input row (1 lines for 1 loads), so the input r
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TM form_two    arch opcode 'movl' has no entry in the opcode table -- no body in the corpus this table was buil
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TM form_three  this unit's prelude is not one two-step load per input row (3 lines for 2 loads), so the input r
php/add_function                               form_two    arch opcode 'movl' has no entry in the opcode table -- no body in the corpus this table was buil
php/add_function                               form_three  this unit's prelude is not one two-step load per input row (5 lines for 3 loads), so the input r
```

The refusal is `gate.py`'s own line, not a reading of it:

```
$ grep -n "lines for" /projects/PseudoCoupHQ/Research/op_pipeline/gate.py
506:                "input row (%d lines for %d loads), so the input rows "
```

`gate.py`'s binder assumes one two-step load per input row. The seventh
kind's area load is one step, so the binder refuses and the solver is
never asked. **On every unit that HAS an arriving area, Part B is
structurally proved and solver-unreachable by construction.**

The exception is instructive rather than a hole: `ruby/rb_fix_plus` and
`ruby/rb_int_plus` have no arriving area, so their Part B prelude IS
Part A's, and their solver route stops where it always did — on `call`.
The two rows read the same because the two forms produced the same
text. Flagged at §0.2; nothing was changed in `gate.py` to paper over
it.

## 4.5 Solver time — no verdict here was a timeout

Every gate was asked at 20,000 ms and would have been re-asked at
120,000 ms if and only if the first answer was UNDECIDED FOR TIME.
`120000ms=NOT_RUN` on every row of §4.2: no unit reached the solver at
all, so no run hit a time limit and `answer_changed_with_more_room` is
`false` for all of them. Task 91's finding (120,000 ms turns some
UNDECIDED into DISPROVED and never into a proof) still has no purchase
on this population: nothing here is solver-bound.

---

# 5. The three shortfalls log_199 flagged, asked per unit

Lane log: `20260905T072242Z__t96_l8_transcripts.sh.log` §[6/8].

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    s = r['the_three_shortfalls']
    a = s['the_r15_collision']
    b = s['memory_obtained_at_run_time']
    c = s['an_input_block_holds_a_pointer']
    print('%-58s r15 body=%-5s form=%-5s gone=%-5s | obtained n=%-2d gone=%-5s | areas=%d gone=%-5s n/a=%s' % (r['unit'], a['the_body_names_r15'], a['the_form_claims_r15'], a['gone'], b['sightings'], b['gone'], c['arriving_areas_found'], c['gone'], c['not_applicable']))
"
cpython/long_add_fastpath                                  r15 body=False form=False gone=True  | obtained n=11 gone=True  | areas=2 gone=True  n/a=False
java/op_1                                                  r15 body=True  form=False gone=True  | obtained n=0  gone=True  | areas=1 gone=False n/a=False
java/op_2                                                  r15 body=True  form=False gone=True  | obtained n=1  gone=True  | areas=1 gone=False n/a=False
ruby/vm_opt_plus                                           r15 body=False form=False gone=False | obtained n=0  gone=False | areas=0 gone=False n/a=True
ruby/rb_fix_plus                                           r15 body=False form=False gone=True  | obtained n=10 gone=True  | areas=0 gone=False n/a=True
ruby/rb_int_plus                                           r15 body=False form=False gone=True  | obtained n=20 gone=True  | areas=0 gone=False n/a=True
ruby/rb_big_plus                                           r15 body=False form=False gone=True  | obtained n=10 gone=True  | areas=1 gone=True  n/a=False
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                r15 body=True  form=False gone=True  | obtained n=16 gone=True  | areas=2 gone=True  n/a=False
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           r15 body=True  form=False gone=True  | obtained n=8  gone=True  | areas=1 gone=True  n/a=False
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER r15 body=True  form=False gone=True  | obtained n=0  gone=True  | areas=2 gone=True  n/a=False
php/add_function                                           r15 body=False form=False gone=True  | obtained n=3  gone=True  | areas=3 gone=True  n/a=False
```

Read as a table, one row per unit, one column per shortfall:

| unit | 1. the `%r15` collision | 2. no block kind for memory obtained at run time | 3. an input block holds a pointer |
|---|---|---|---|
| cpython/long_add | GONE (body never names it) | GONE — 11 sightings, none needs a block | GONE — 2 arriving areas |
| java/op_1 | **GONE** — body names `%r15`, form does not | GONE — 0 sightings | **SURVIVES** — the area is found but refused on the extent |
| java/op_2 | **GONE** — same | GONE — 1 sighting | **SURVIVES** — same |
| ruby/vm_opt_plus | not applicable — no body | not applicable | not applicable |
| ruby/rb_fix_plus | GONE | GONE — 10 sightings | not applicable — no arriving area |
| ruby/rb_int_plus | GONE | GONE — 20 sightings | not applicable — no arriving area |
| ruby/rb_big_plus | GONE | GONE — 10 sightings | GONE — 1 arriving area |
| php/ZEND_ADD_SPEC_… | **GONE** — body names `%r15`, form does not | GONE — 16 sightings | GONE — 2 arriving areas |
| php/ZEND_ADD_LONG_SPEC_… | **GONE** | GONE — 8 sightings | GONE — 1 arriving area |
| php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_… | **GONE** | GONE — 0 sightings | GONE — 2 arriving areas |
| php/add_function | GONE | GONE — 3 sightings | GONE — 3 arriving areas |

Tally, over the ten units that have a body: shortfall 1 gone on 10/10;
shortfall 2 gone on 10/10; shortfall 3 gone on 6, not applicable on 2
(no arriving area exists to be about), **surviving on 2**.

**Why each is gone, and it is a different reason each time:**

1. **The `%r15` collision.** `region36` §2 ruled `%r15` the region base
   and refused by name any core that mentions it.
   `canonical_form.py` rules no register anything: the ledger is at an
   absolute address, reached rip-relative, and the only registers the
   form writes are the ones the unit's own arrival contract names plus
   one scratch. Five bodies name `%r15`; the form claims it in none of
   them. **This is an artifact of the misreading, exactly as the owner said.**
2. **Memory obtained at run time.** The region form had to give every
   byte the body touches a block, because it REWROTE every location
   into the region — so a `PyLongObject` handed back by `long_alloc`
   had nowhere to land. The canonical form rewrites nothing: the store
   through an obtained pointer stays exactly as the compiler wrote it,
   and the answer is read out of the unit's own answer home by the
   epilogue, not off a result block. There is nothing left for a block
   kind to do. **The counts above (0 to 20 sightings per unit) are the
   dereferences that would have needed one, and none does.**
3. **An input block holds a pointer.** This one needed Part B. The
   seventh kind gives the arriving pointer's OBJECT a block — an
   addressable extent the body reaches into at its own displacements —
   instead of an input row holding the pointer's value. It survives on
   `java/op_1` and `java/op_2`, and for one stated reason: their area
   is found correctly and then refused on the extent span. **A
   surviving shortfall is a result.**

---

# 6. `region36.py` and `canon36_universal.py` — one header block each, nothing else

```
$ sed -n '4,13p' /projects/PseudoCoupHQ/Research/op_pipeline/region36.py
SUPERSEDED RECORD, 2026-09-05, by the correction "the form, as the owner
meant it" in `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`:
the arch-unit is essentially UNCHANGED except for the loading and
unloading of registers into a virtual memory, so the form WRAPS a body
it does not touch (`canonical_form.py`) rather than rewriting every
location in it as `0x<offset>(%r15)` as section 2 below does.  The
`%r15` collision is an artifact of that misreading, not a design
conflict.  This file is kept exactly as it is, as the record of the
form it defined, and is neither edited nor imported by the corrected
line; task 96 (log_201) moved the eleven interpreter units off it.
```

```
$ sed -n '5,12p' /projects/PseudoCoupHQ/Research/op_pipeline/canon36_universal.py
SUPERSEDED RECORD, 2026-09-05, by the correction "the form, as the owner
meant it" in `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`:
this file renders `region36.py`'s form, which REWRITES a body rather
than wrapping one, and that reading of the 2026-09-02 ruling is the
misread one.  The form that stands is `canonical_form.py`.  This file
is kept exactly as it is, as the record of what it rendered, and is
neither edited nor imported by the corrected line; task 96 (log_201)
moved the eleven interpreter units off it.
```

Neither file is imported by anything this lap wrote. FORM 1's texts
were READ out of `t94_recarve.json`, never re-rendered.

```
$ grep -c "region36\|canon36_universal" /projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py
/projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py:5
/projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py:5
/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py:2
/projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py:2
```

**GLOSS, so the count is not read as an import count.** Every one of
those hits is inside a docstring or a comment naming the superseded
form; none is an `import`. The check that decides it:

```
$ grep -n "^import\|^ *import " /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py
212:import os
213:import re
214:import sys
219:import canon                                                      # noqa: E402
220:import ledger as L                                                # noqa: E402
```

---

# 7. Gates

## 7.1 The spelling guard, ONE process, over every artifact this lap wrote

Lane log: `20260905T071936Z__t96_l6_render2.sh.log` §[5/6].

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS t96_canonical.json -- no operator token in any key, grouping, pairing or row structure
PASS t96_analysis.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt /projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json /projects/PseudoCoupHQ/Research/op_pipeline/t96_wrapped_texts.txt /projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py
/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json:0
/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json:0
/projects/PseudoCoupHQ/Research/op_pipeline/t96_wrapped_texts.txt:0
/projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py:0
/projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py:0
/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py:0
```

The checker is UNMODIFIED — its bytes, which do not move:

```
$ sha256sum /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7  /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
```

Its last commit is `fdff0b254fd7ebd8032128803146af0e3092812b`
(`git log -1 --format=%H -- Research/op_pipeline/check_no_spelling_keys.py`,
lane log `20260905T072829Z__t96_l10_logtranscripts.sh.log` §[8/8]).
**That command is a MOVING REFERENCE and the verifier is right to
refuse it**: `git log` with no pinned revision answers about whatever
the repository holds when it is asked. The `sha256sum` above is the
claim that does not move.

## 7.2 The display label

The member's operator token travels on the field `label`, on records
that also carry `language` and `unit` — the shape the checker names as
a per-unit display label. The population of every program this lap
wrote is "the eleven records of `t94_recarve.json`, in that file's own
order"; nothing is keyed, grouped, paired, selected or compared by the
token.

## 7.3 This log, run through `check_conventions_log_claims.py`

Lane logs: `20260905T073152Z__t96_l13_verify_this_log.sh.log` (the
first pass, which found one DIFFERS and two NOT_RERUNNABLE),
`20260905T073505Z__t96_l15_verify_this_log2.sh.log`, and
`20260905T073526Z__t96_l16_verify_this_log3.sh.log` (the pass below).

```
population: 34 claims across 1 logs
  MATCHES          28
  DIFFERS          0
  UNVERIFIABLE     6
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 28 of 34 claims reproduce; 6 (18%) carry nothing to re-run

causes, by name:
  prose_only                       6
```

**THAT PASS RAN AGAINST THIS LOG AS IT STOOD BEFORE THIS SECTION
EXISTED**, which is the only honest way to quote it: adding this
section adds claims. The pass over the log INCLUDING this section is
lane `t96_l17_verify_final.sh`
(`20260905T073722Z__t96_l17_verify_final.sh.log`), and it reads
**35 claims, MATCHES 28, DIFFERS 0, UNVERIFIABLE 7 (20%)** — the one
extra unverifiable being the block just above, which is a paste of a
verifier summary and by construction has no command of its own.

Against the brief's bar — task 94 scored 19 matched of 32 with 28%
unverifiable — this is 28 matched of 35 with 20% unverifiable and
nothing disagreeing.

**The three things the first pass caught, and what was done about each,
because the point of a checker is its catches:**

1. **One DIFFERS**, §4.3: the transcript was split across two fenced
   blocks, so the verifier compared the first against the whole output.
   Joined into one block. It matches now.
2. **`elided_command`**, §2.1: the command itself printed `'    ...'`
   between head and tail, and the verifier reads `...` in a command as
   an elided path. Changed to `[%d lines not printed]`, which says the
   same thing and carries a number.
3. **`moving_reference`**, §7.1: `git log -1 --format=%H` answers about
   whatever the repository holds when asked. Replaced with
   `sha256sum` of the file's own bytes; the commit hash is still named,
   as a moving reference, in words.

A fourth was caught on the second pass: the verifier's work directory
is `/projects/PseudoCoupHQ`, not `Research/op_pipeline`, so §0.2's
`import t96_arriving_area` raised `ModuleNotFoundError`. The command
now inserts the path itself.

**The 6 that carry nothing to re-run, named rather than counted**, and
each is prose about a meaning rather than a measurement: this log's own
preamble (line 8); the statement that php's frame reach is not readable
from its text (line 93 — the measurement beside it IS re-runnable, at
§3.5); the restatement of log_199's baseline in this log's own words
(line 601 — the quote from log_199 itself, above it, is re-runnable);
what `PROVED_BY_CONSTRUCTION` MEANS (line 686); why the binder refuses
(line 790 — `gate.py`'s own line, above it, is re-runnable); and lane
8's own format-string fault (line 1088), which lives in a lane log
outside every path Airlock mounts.

---

# 8. Memory and time

- **Stated bound: 6 GB, abort by name.** `T96_MEMORY_ABORT` in
  `t96_onto_canonical_form.py`, `T96_ANALYSIS_MEMORY_ABORT` in
  `t96_analysis.py`. Each checks its own peak after every unit and at
  the end of its run.
- **Measured peaks** (`ru_maxrss`), lane log
  `20260905T072242Z__t96_l8_transcripts.sh.log` §[8/8]:

```
$ python3 -c "
import json
a = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))['meta']
b = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))['meta']
print('t96_onto_canonical_form.py peak resident kB: %d' % a['peak_resident_size_kB'])
print('t96_analysis.py            peak resident kB: %d' % b['peak_resident_size_kB'])
print('bound kB: %d   abort names: %s / %s' % (a['memory_bound_kB'], a['memory_abort_name'], b['memory_abort_name']))
"
t96_onto_canonical_form.py peak resident kB: 60060
t96_analysis.py            peak resident kB: 57920
bound kB: 6291456   abort names: T96_MEMORY_ABORT / T96_ANALYSIS_MEMORY_ABORT
```

- No run hit a time or memory limit, so no run was re-run with more
  room. Longest lane: 0.9 s. The whole task's compute is trivial; the
  cost of this lap is reading, not running.

---

# 9. Artifacts, every one named

## 9.1 Written this lap (new files only)

| path | what it is |
|---|---|
| `Research/op_pipeline/t96_arriving_area.py` | THE SEVENTH BLOCK KIND: the evidence rule, the extent, the affine map, the refusal, the one-step area prelude, `AreaLedger` |
| `Research/op_pipeline/t96_onto_canonical_form.py` | renders each of the eleven three ways and gates each; the three shortfalls asked per unit |
| `Research/op_pipeline/t96_canonical.json` | its output: FORM 1 read, FORM 2 rendered, FORM 3 rendered, verdicts, movements, shortfalls |
| `Research/op_pipeline/t96_analysis.py` | separates the FORM change from the INSTRUMENT change; the six checks one at a time; dumps the texts |
| `Research/op_pipeline/t96_analysis.json` | its output |
| `Research/op_pipeline/t96_wrapped_texts.txt` | all three wrapped texts, in full, for all eleven units |
| `Research/op_pipeline/t96_step.py` | the stepped machine state of §3.3 |
| `Research/op_pipeline/t96_l1_inventory.sh` … `t96_l13_verify_this_log.sh` | the lane scripts, one per submission |

## 9.2 Edited this lap

| path | edit |
|---|---|
| `Research/op_pipeline/region36.py` | one header block added (§6). Nothing removed, no code touched. |
| `Research/op_pipeline/canon36_universal.py` | one header block added (§6). Nothing removed, no code touched. |

## 9.3 Imported or run UNMODIFIED

`canonical_form.py`, `ledger.py`, `gate.py`, `reference.py`,
`canon.py`, `check_no_spelling_keys.py`.

## 9.4 Read read-only

`t94_recarve.json`, `t94_bounds.json`, `canon40_wrapped_c.json`,
`canon40_wrapped_cpp.json`, `canon40_wrapped_go.json`,
`canon40_wrapped_rust.json`, `canon40_wrapped_swift.json`,
`canon40_interp.json`.

## 9.5 Superseded, kept as records

`region36.py`, `canon36_universal.py` (each gaining one header block
and nothing else), and every artifact they produced —
`t94_recarve.json`'s `universal_form` field in particular, which is
where FORM 1's texts were read from. None was deleted, none re-rendered.

## 9.6 The lane logs

| lane | log |
|---|---|
| `t96_l1_inventory.sh` | `20260905T070552Z__t96_l1_inventory.sh.log` |
| `t96_l2_survey.sh` | `20260905T070835Z__t96_l2_survey.sh.log` |
| `t96_l3_survey2.sh` | `20260905T071056Z__t96_l3_survey2.sh.log` |
| `t96_l4_render.sh` | `20260905T071425Z__t96_l4_render.sh.log` |
| `t96_l5_analysis.sh` | `20260905T071648Z__t96_l5_analysis.sh.log` |
| `t96_l6_render2.sh` | `20260905T071936Z__t96_l6_render2.sh.log` |
| `t96_l7_step.sh` | `20260905T072154Z__t96_l7_step.sh.log` |
| `t96_l8_transcripts.sh` | `20260905T072242Z__t96_l8_transcripts.sh.log` |
| `t96_l9_r15count.sh` | `20260905T072317Z__t96_l9_r15count.sh.log` |
| `t96_l10_logtranscripts.sh` | `20260905T072829Z__t96_l10_logtranscripts.sh.log` |
| `t96_l11_logtranscripts2.sh` | `20260905T072915Z__t96_l11_logtranscripts2.sh.log` |
| `t96_l12_steprange.sh` | `20260905T072959Z__t96_l12_steprange.sh.log` |
| `t96_l13_verify_this_log.sh` | `20260905T073152Z__t96_l13_verify_this_log.sh.log` |
| `t96_l14_moreclaims.sh` | `20260905T073325Z__t96_l14_moreclaims.sh.log` |
| `t96_l15_verify_this_log2.sh` | `20260905T073505Z__t96_l15_verify_this_log2.sh.log` |
| `t96_l16_verify_this_log3.sh` | `20260905T073526Z__t96_l16_verify_this_log3.sh.log` |
| `t96_l17_verify_final.sh` | `20260905T073722Z__t96_l17_verify_final.sh.log` |

All in `~/Programming/Airlock/agent/logs/`. **That directory is
outside every path Airlock mounts, so no claim about a lane log's
contents can be re-run by the verifier; the lane logs are named as
provenance and the artifacts they wrote carry the numbers.** **Lanes 10, 11 and 12
exist only to run the commands this log pastes**, so every transcript
above is real output rather than a paraphrase; lane 13 runs the log
verifier against this file.

Lane 8 §[1/8] carries a
fault of its own, said rather than hidden: a literal `%r15` inside a
python format string raised `TypeError` after printing two of its three
numbers. Lane 9 re-ran that step and is the transcript §1.2 pastes.
