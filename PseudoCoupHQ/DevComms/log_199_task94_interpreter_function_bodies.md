# log 199 — TASK 94 round 18: the eleven interpreter units re-carved to their handler function's body

Date: 2026-09-05. Report shape: LLM_communication_protocol Appendix B
(one numbered tree, high to low, values in motion at the leaves).
Renderings are labelled **LITERAL** or **GLOSS** per §5.1a.
Every claim below either carries a `$ ` command that reproduces it, or
says in its own line that it cannot.

All computation ran through Airlock, default instance, one lane per
step. The lane logs are named where their output is used.

---

# 0. The two lists

## 0.1 Decided, recorded for audit

- **The eleven interpreter units are re-carved to their handler
  function's body.** Bounds are READ from the ELF symbol table and,
  where DWARF carries the function, cross-read against
  `DW_AT_low_pc`/`DW_AT_high_pc`. No taint propagation was used for a
  boundary anywhere in this lap.
- **`lineage_carve.py` keeps its taint propagation and its outputs.**
  One header line was added saying the BOUNDARY use is retired,
  2026-09-05, and by what. Nothing was deleted.
- **All eleven verdicts moved: 9 PROVED to UNDECIDED, 1
  NO_CANONICAL_TEXT to UNDECIDED, 1 NO_CANONICAL_TEXT to NO_BODY.**
  None moved to DISPROVED and none stayed PROVED. Under the brief's own
  statement this is a correct result: the old proofs rested on a
  boundary someone chose. No body was narrowed to keep a proof.
- **`cpython/long_add_fastpath` is renamed `cpython/long_add`** in the
  re-carved record — the `_fastpath` suffix named a slice that no longer
  exists. The old records stay on disk under their old names.
- Three new files, no existing file rewritten: `t94_read_bounds.py`,
  `t94_recarve.py`, `t94_analysis.py`, and their three JSON outputs.
  `region36.py`, `canon36_universal.py`, `super_op_miner.py`,
  `check_no_spelling_keys.py` were imported or run UNMODIFIED.

## 0.2 Awaiting the owner

- **The universal canonical form's virtual memory does not reach a
  whole handler body, in three named ways** (§3.2). Two of them —
  `%r15` as the region base against `%r15` as the interpreter's own VM
  frame pointer, and the absence of a block kind for memory the unit
  obtains at run time — need a ruling, not a patch. Five of the eleven
  units are refused by name on the first alone.
- **The super-op route does not cover this machinery today** (§5.3).
  The miner's population is the five compiled languages; no interpreter
  unit has ever been mined. Whether to point it at the interpreter
  population is the owner's call.

---

# 1. The boundary, read instead of computed

## 1.1 The rule this lap implements

**LITERAL**, the ruling in its own file:

```
$ sed -n '167,177p' /projects/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/CORE_0_3_5_1_arch_unit.md
## the unit's boundary — RULED by the owner 2026-09-05

**A unit is a function body: from just after the wrapper-function call
to just before the return.** For a compiled probe the wrapper is the
probe function we wrote. For an interpreter there is no wrapper of
ours, so the interpreter's OWN handler function is the wrapper and the
unit is that function's body.

the owner, 2026-09-05: "everything is wrapped in a function. it should be
just after the wrapper-function call to just before the return
statement. no?"
```

**GLOSS.** A boundary that is READ off the binary cannot be disputed.
The lineage carve COMPUTED one, and `lineage_carve.py`'s own header
records that the computation was wrong once (ruby's optimised
`rb_fix_plus` places its slow path at lower addresses than its fast
path). This lap replaces the computed boundary with a read one.

## 1.2 What was read, per binary

Lane log: `~/Programming/Airlock/agent/logs/20260905T060329Z__t94_l12_transcripts2.sh.log`.
These three come back REFUSED from `check_conventions_log_claims.py`
with the rule `head_not_on_the_read_only_allowlist` — `readelf` is not
on its allowlist. They are kept because they are the primary evidence;
§1.2a repeats the same facts through a command the verifier does run.

```
$ readelf -sW /persist/cpython_ship/python | grep -w long_add
   287: 0000000000137370   377 FUNC    LOCAL  DEFAULT   14 long_add

$ readelf -sW /persist/ruby_ship/ruby | grep -wE 'rb_fix_plus|rb_int_plus|rb_big_plus|vm_opt_plus'
  1918: 00000000003b6ad0   583 FUNC    GLOBAL DEFAULT   13 rb_big_plus
 12295: 00000000000faa90   846 FUNC    LOCAL  DEFAULT   13 rb_int_plus
 12675: 0000000000104750   585 FUNC    LOCAL  DEFAULT   13 rb_fix_plus
 14170: 00000000003b6ad0   583 FUNC    GLOBAL DEFAULT   13 rb_big_plus

$ readelf -sW /persist/php_c_ship/sapi/cli/php | grep -wE 'add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER' | grep FUNC
  2133: 000000000040c050   202 FUNC    GLOBAL DEFAULT   14 add_function
  6226: 00000000002257b6    42 FUNC    LOCAL  DEFAULT   14 ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER
  6227: 00000000002257e0    75 FUNC    LOCAL  DEFAULT   14 ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER
  6607: 0000000000228c75   170 FUNC    LOCAL  DEFAULT   14 ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER
 11206: 000000000040c050   202 FUNC    GLOBAL DEFAULT   14 add_function
```

**GLOSS.** Column three is `st_size`, the function's byte length. Low
bound = `st_value`, high bound = `st_value + st_size`. That pair is the
unit's bounds under the ruling.

## 1.2a The same symbol rows, as this lap stored them

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json'))
for r in d['records']:
    print(r['unit'], '| symbol table:', r['symbol_table_rows'], '| dwarf:', r['dwarf_rows'])
"
cpython/long_add_fastpath | symbol table: [{'section': '.symtab', 'st_value': 1274736, 'st_size': 377, 'bind': 'STB_LOCAL'}] | dwarf: []
java/op_1 | symbol table: None | dwarf: None
java/op_2 | symbol table: None | dwarf: None
ruby/vm_opt_plus | symbol table: [] | dwarf: []
ruby/rb_fix_plus | symbol table: [{'section': '.symtab', 'st_value': 1066832, 'st_size': 585, 'bind': 'STB_LOCAL'}] | dwarf: [{'cu_offset': 2266900, 'DW_AT_low_pc': 1066832, 'DW_AT_high_pc': 1067417, 'high_pc_form': 'DW_FORM_data8'}]
ruby/rb_int_plus | symbol table: [{'section': '.symtab', 'st_value': 1026704, 'st_size': 846, 'bind': 'STB_LOCAL'}] | dwarf: [{'cu_offset': 2266900, 'DW_AT_low_pc': 1026704, 'DW_AT_high_pc': 1027550, 'high_pc_form': 'DW_FORM_data8'}]
ruby/rb_big_plus | symbol table: [{'section': '.dynsym', 'st_value': 3893968, 'st_size': 583, 'bind': 'STB_GLOBAL'}, {'section': '.symtab', 'st_value': 3893968, 'st_size': 583, 'bind': 'STB_GLOBAL'}] | dwarf: [{'cu_offset': 11760217, 'DW_AT_low_pc': 3893968, 'DW_AT_high_pc': 3894551, 'high_pc_form': 'DW_FORM_data8'}]
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER | symbol table: [{'section': '.symtab', 'st_value': 2264181, 'st_size': 170, 'bind': 'STB_LOCAL'}] | dwarf: []
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER | symbol table: [{'section': '.symtab', 'st_value': 2250720, 'st_size': 75, 'bind': 'STB_LOCAL'}] | dwarf: []
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER | symbol table: [{'section': '.symtab', 'st_value': 2250678, 'st_size': 42, 'bind': 'STB_LOCAL'}] | dwarf: []
php/add_function | symbol table: [{'section': '.dynsym', 'st_value': 4243536, 'st_size': 202, 'bind': 'STB_GLOBAL'}, {'section': '.symtab', 'st_value': 4243536, 'st_size': 202, 'bind': 'STB_GLOBAL'}] | dwarf: [{'cu_offset': 4590058, 'DW_AT_low_pc': 4243536, 'DW_AT_high_pc': 4243738, 'high_pc_form': 'DW_FORM_data8'}]
```

**GLOSS.** `st_value` 1274736 is 0x137370 and `st_size` 377 — the same
row `readelf` printed above, stored by this lap's own reader. Empty
`dwarf` lists are the four functions DWARF carries no named subprogram
for; `None` marks the two JIT nmethods, which have no ELF at all;
`ruby/vm_opt_plus`'s empty symbol list is the symbol that does not exist
in the ship build.

- `ruby/vm_opt_plus` has NO row. It has no ship body at all — the
  optimiser inlined the symbol away. That was already on record
  (`op_units_ruby.json` `symbol_absences`) and this lap confirms it from
  the symbol table rather than from the dump.

## 1.3 DWARF, where it exists

- DWARF agrees with the symbol table exactly for all four functions it
  carries a `DW_TAG_subprogram` for: `ruby/rb_fix_plus`,
  `ruby/rb_int_plus`, `ruby/rb_big_plus`, `php/add_function`. The field
  `symbol_table_and_dwarf_agree` is `true` for each.
- DWARF carries NO named subprogram for `cpython/long_add` in
  `/persist/cpython_ship/python`, and none for the three php
  `ZEND_ADD_*` handlers. FLAGGED, not resolved: those four bounds rest
  on the symbol table alone. The symbol table is one of the ruling's two
  named sources, so the boundary is still read; it simply has one
  witness rather than two.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json'))
for r in d['records']:
    print('%-58s %-10s %-10s %5s %5s  dwarf_agrees=%s' % (r['unit'], r.get('new_low'), r.get('new_high'), r.get('new_byte_length'), r.get('new_instruction_count'), r.get('symbol_table_and_dwarf_agree')))
"
cpython/long_add_fastpath                                  0x137370   0x1374e9     377    92  dwarf_agrees=None
java/op_1                                                  None       None        None  None  dwarf_agrees=None
java/op_2                                                  None       None        None  None  dwarf_agrees=None
ruby/vm_opt_plus                                           None       None        None  None  dwarf_agrees=None
ruby/rb_fix_plus                                           0x104750   0x104999     585   126  dwarf_agrees=True
ruby/rb_int_plus                                           0xfaa90    0xfadde      846   190  dwarf_agrees=True
ruby/rb_big_plus                                           0x3b6ad0   0x3b6d17     583   132  dwarf_agrees=True
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                0x228c75   0x228d1f     170    48  dwarf_agrees=None
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           0x2257e0   0x22582b      75    20  dwarf_agrees=None
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER 0x2257b6   0x2257e0      42    10  dwarf_agrees=None
php/add_function                                           0x40c050   0x40c11a     202    55  dwarf_agrees=True
```

**GLOSS.** `dwarf_agrees=True` means DWARF's `DW_AT_low_pc` and
`DW_AT_high_pc` equal the symbol table's `st_value` and
`st_value + st_size` exactly. `None` means DWARF carries no named
subprogram to compare against; the two java rows are `None` throughout
because a JIT has neither table (§1.4).

## 1.4 The one place the ruling's named sources do not exist — FLAGGED

- `java/op_1` and `java/op_2` are JIT-emitted nmethods. A JIT has no ELF
  symbol table and no DWARF.
- What was read instead: the JVM's OWN printed nmethod base and length,
  recorded in `interp_jvm.json` (`arch_unit[0].base`, `.length`,
  `nmethod_header`). That is the JIT's own testimony and it is READ, not
  computed — the property the ruling is after — but it is not one of the
  two sources the ruling names. Recorded on each record's
  `bounds_source` field, in those words.
- A defect fixed at first observation while doing this: the JVM's dump
  prints an instruction as `address\tbytes\tmnemonic`, and a long
  instruction's leftover bytes as `address\tbytes` with only two fields.
  Reading a two-field line as an instruction gave `java/op_1` a
  27th instruction whose mnemonic was `00`. Corrected count:

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/interp_jvm.json'))
for u in d['units']:
    rows=[l for r in u['arch_unit'] for l in r['objdump'] if not len(l.split(chr(9))) < 3]
    cont=[l for r in u['arch_unit'] for l in r['objdump'] if len(l.split(chr(9))) < 3]
    print(u['id'], u['nmethod_header'], '| base', u['arch_unit'][0]['base'], '| length', u['arch_unit'][0]['length'], '| instructions', len(rows), '| byte-continuation lines', len(cont))
"
u1 12    4             Probe::af (4 bytes) | base 0x7f99346aa400 | length 104 | instructions 26 | byte-continuation lines 2
u2 14    7             Probe::af2 (4 bytes) | base 0x7f99346a9b00 | length 152 | instructions 43 | byte-continuation lines 3
```

**GLOSS.** 43 for `u2` is the same number `interp_canon34.json` recorded
as that unit's `walk_instruction_count`, which is an independent
agreement rather than a re-use.

## 1.5 Old bounds against new, all eleven side by side

Lane log: `20260905T060329Z__t94_l12_transcripts2.sh.log`.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json'))
for r in d['records']:
    o=r['old']; n=r['recarved']
    print('%-58s old %-14s n=%-3s  new %-14s %-14s %4s %4s' % (r['unit'], o['old_low'], o['old_body_instruction_count'], n.get('new_low'), n.get('new_high'), n.get('new_byte_length'), n.get('new_instruction_count')))
"
cpython/long_add_fastpath                                  old 0x1373d8       n=1    new 0x137370       0x1374e9        377   92
java/op_1                                                  old 0x7f99346aa41a n=1    new 0x7f99346aa400 0x7f99346aa468  104   26
java/op_2                                                  old 0x7f99346a9b33 n=1    new 0x7f99346a9b00 0x7f99346a9b98  152   43
ruby/vm_opt_plus                                           old None           n=0    new None           None           None None
ruby/rb_fix_plus                                           old 0x104834       n=1    new 0x104750       0x104999        585  126
ruby/rb_int_plus                                           old 0xfac1f        n=1    new 0xfaa90        0xfadde         846  190
ruby/rb_big_plus                                           old None           n=0    new 0x3b6ad0       0x3b6d17        583  132
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                old 0x228ca1       n=1    new 0x228c75       0x228d1f        170   48
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           old 0x2257fc       n=1    new 0x2257e0       0x22582b         75   20
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER old 0x2257ce       n=1    new 0x2257b6       0x2257e0         42   10
php/add_function                                           old 0x40c065       n=2    new 0x40c050       0x40c11a        202   55
```

**GLOSS**, column by column: unit; the old boundary's low address; how
many of the unit's OWN instructions the old boundary kept; the new low
and high bound; the function's byte length; the new instruction count.

Read as a table:

| unit | old low | old n | new bounds | new bytes | new n |
|---|---|---|---|---|---|
| cpython/long_add (was `long_add_fastpath`) | 0x1373d8 | 1 | 0x137370..0x1374e9 | 377 | 92 |
| java/op_1 | 0x7f99346aa41a | 1 | 0x7f99346aa400..0x7f99346aa468 | 104 | 26 |
| java/op_2 | 0x7f99346a9b33 | 1 | 0x7f99346a9b00..0x7f99346a9b98 | 152 | 43 |
| ruby/vm_opt_plus | — | 0 | no ship body | — | — |
| ruby/rb_fix_plus | 0x104834 | 1 | 0x104750..0x104999 | 585 | 126 |
| ruby/rb_int_plus | 0xfac1f | 1 | 0xfaa90..0xfadde | 846 | 190 |
| ruby/rb_big_plus | — | 0 | 0x3b6ad0..0x3b6d17 | 583 | 132 |
| php/ZEND_ADD_SPEC_… | 0x228ca1 | 1 | 0x228c75..0x228d1f | 170 | 48 |
| php/ZEND_ADD_LONG_SPEC_… | 0x2257fc | 1 | 0x2257e0..0x22582b | 75 | 20 |
| php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_… | 0x2257ce | 1 | 0x2257b6..0x2257e0 | 42 | 10 |
| php/add_function | 0x40c065 (confluence) | 2 | 0x40c050..0x40c11a | 202 | 55 |

Two readings of "old n", kept apart because they are different numbers:

- **the unit's own instructions the old boundary kept** — the column
  above. It is 1 for eight of the eleven, 2 for `php/add_function`.
- **the instruction count of the canonical TEXT those units carried** —
  3 to 6 lines, because the canonical text adds standardized loads, a
  relocating move and a `ret` that the compiler never emitted. The
  brief's "four instructions" for cpython is this second reading:
  `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret`, of which exactly
  one line traces to `long_add`'s own bytes.

## 1.6 A count that did not reproduce, said plainly

- `interp_fastpath.json` records `"function_instruction_count": 94` for
  `long_add`. Counted straight off objdump this lap, `long_add` holds
  **92** instructions inside its symbol-table bounds and **93** counting
  to the next symbol (one `nopl 0x0(%rax)` of alignment padding at
  0x1374e9, before `long_invert` at 0x1374f0).

```
$ objdump -d -w --start-address=0x137370 --stop-address=0x1374e9 /persist/cpython_ship/python | grep -cE '^ +[0-9a-f]+:'
92
```

This one comes back REFUSED from the log verifier with the rule
`head_not_on_the_read_only_allowlist` — `objdump` is not on its
allowlist. The same 92 is in `t94_bounds.json`'s
`new_instruction_count`, which §1.3's transcript prints.

- I did not resolve the remaining difference of one. It is recorded here
  as a disagreement between an old artifact and this lap's own count,
  not silently averaged away.

---

# 2. The case that showed it, with values in motion

## 2.1 The unit as it stood

**LITERAL**, `Research/op_pipeline/interp_canon35.json`, record 0,
field `prior_text`:

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/interp_canon35.json'));print(d['records'][0]['prior_text'])"
mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
```

**GLOSS.** Four lines. Of them, exactly one — the addition — traces to
CPython's own bytes, and even that is a substitute: the instruction
`long_add` actually emits at the confluence is
`lea (%rax,%rdx,1),%rdi`, and `canon_interp_units_cpython.json` proved
that instruction equal to the c-population's own canonical text, then
carried the c text forward as this unit's.

## 2.2 The function those four lines were cut out of

`long_add` at 0x137370, 377 bytes, 92 instructions. Take
`a = 3`, `b = 4`, both small CPython integers.

**LITERAL**, the entry, from `t94_bounds.json`'s `body` (objdump's own text):

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(0,11)):
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
"
 0  0x137370  sub $0x28,%rsp
 1  0x137374  mov 0x10(%rdi),%rax
 2  0x137378  mov 0x10(%rsi),%rdx
 3  0x13737c  mov %rsi,%rcx
 4  0x13737f  mov %rax,%r8
 5  0x137382  mov %rdx,%rsi
 6  0x137385  or %rdx,%rax
 7  0x137388  and $0x3,%r8d
 8  0x13738c  and $0x3,%esi
 9  0x13738f  cmp $0xf,%rax
10  0x137393  jbe 1373d8 <long_add+0x68>
```

**GLOSS, values moving.** `%rdi` holds a's object address, `%rsi` holds
b's.

```
mov 0x10(%rdi),%rax     %rax = 8      a's lv_tag: one digit, sign 0
mov 0x10(%rsi),%rdx     %rdx = 8      b's lv_tag
mov %rsi,%rcx           %rcx = &b     b's address kept
mov %rax,%r8            %r8  = 8
mov %rdx,%rsi           %rsi = 8
or  %rdx,%rax           %rax = 8      8 | 8
and $0x3,%r8d           %r8  = 0      a's sign bits
and $0x3,%esi           %rsi = 0      b's sign bits
cmp $0xf,%rax           8 vs 15
jbe 1373d8              taken         both are compact -> fast path
```

That `jbe` is the branch the OLD boundary's entry point sat behind:
`interp_fastpath.json` names its entry as 0x1373d8, reached by "the
`jbe` at `long_add+0x1f` taking its branch".

**LITERAL**, the fast path itself:

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(26,38)):
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
"
26  0x1373d8  mov $0x1,%edx
27  0x1373dd  mov 0x18(%rcx),%ecx
28  0x1373e0  mov %rdx,%rax
29  0x1373e3  sub %r8,%rdx
30  0x1373e6  sub %rsi,%rax
31  0x1373e9  imul %rcx,%rax
32  0x1373ed  mov 0x18(%rdi),%ecx
33  0x1373f0  imul %rcx,%rdx
34  0x1373f4  lea (%rax,%rdx,1),%rdi
35  0x1373f8  lea 0x5(%rdi),%rax
36  0x1373fc  cmp $0x105,%rax
37  0x137402  jbe 1374c0 <long_add+0x150>
```

**GLOSS, values moving.**

```
mov $0x1,%edx           %rdx = 1
mov 0x18(%rcx),%ecx     %rcx = 4      b's first digit
mov %rdx,%rax           %rax = 1
sub %r8,%rdx            %rdx = 1      1 - a's sign bits
sub %rsi,%rax           %rax = 1      1 - b's sign bits
imul %rcx,%rax          %rax = 4      (1 - b_sign) * b_digit
mov 0x18(%rdi),%ecx     %rcx = 3      a's first digit
imul %rcx,%rdx          %rdx = 3      (1 - a_sign) * a_digit
lea (%rax,%rdx,1),%rdi  %rdi = 7      <- THE ADDITION.  the whole of
                                         the old unit is this one line
lea 0x5(%rdi),%rax      %rax = 12     7 + 5
cmp $0x105,%rax         12 vs 261
jbe 1374c0              taken         7 is inside the cached range
```

**LITERAL**, where the taken branch lands, and the return:

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(83,89))+[63,64]:
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
"
83  0x1374c0  add $0x5,%edi
84  0x1374c3  lea 0x49fb36(%rip),%rax
85  0x1374ca  movslq %edi,%rdi
86  0x1374cd  shl $0x5,%rdi
87  0x1374d1  lea 0x36f0(%rax,%rdi,1),%rax
88  0x1374d9  jmp 137474 <long_add+0x104>
63  0x137474  add $0x28,%rsp
64  0x137478  ret
```

**GLOSS, values moving.**

```
add $0x5,%edi                %rdi = 12          index into the cache
lea 0x49fb36(%rip),%rax      %rax = &interpreter state
movslq %edi,%rdi             %rdi = 12
shl $0x5,%rdi                %rdi = 384         12 * 32 bytes per object
lea 0x36f0(%rax,%rdi,1),%rax %rax = the ADDRESS of the cached object 7
ret                          the answer is a POINTER, not the number 7
```

## 2.3 What the old boundary hid, said as facts

- The unit answered **7**. The function answers **the address of a
  PyLong object holding 7**. Those are different values of different
  kinds, and only the second is what CPython's addition returns.
- Three whole capabilities of the function were outside the old
  boundary: the compact-integer test (index 9–10), the small-integer
  cache (index 83–87), and — on the path 3+4 does not take — an
  allocation and the field writes that fill the new object
  (`call 131d70 <long_alloc>` at index 52, then
  `mov %rcx,0x10(%rax)`, `mov %edx,0x1c(%rax)`, `mov %ecx,0x18(%rax)`).
- The old boundary's own artifact says so in its own words.
  **LITERAL**, `canon_interp_units_cpython.json`, `unit.arrival_boundary_note`:

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/canon_interp_units_cpython.json'));print(d['unit']['arrival_boundary_note'])"
lineage confluence, per AgentMemory 2026-08-31 -- the first instruction reading BOTH unpacked operand values; the 8 arrival instructions before it are REPRESENTATION only (typed-pointer(PyLongObject*) unpacking), not part of this canonicalization
```

## 2.4 The name

- `cpython/long_add_fastpath` becomes **`cpython/long_add`** in the
  re-carved record's `handler_function` field. `_fastpath` named a slice
  behind a branch; the slice no longer exists.
- The old records keep the old name, as superseded evidence.
  `t94_recarve.json` keys each record by the OLD unit name so the two
  can be joined; the handler function is named separately.

---

# 3. The whole body through the universal canonical form

## 3.1 The form used, and that it was not modified

- The form is `region36.py` — the ruled virtual region (base `%r15`,
  `REGION_SIZE 0x400`), its six allocation kinds (input, constant, temp,
  result, guard-outcome, own-address) and its block allocator. Rendered
  by `canon36_universal.render`. Both were IMPORTED, not edited. No new
  memory model was invented anywhere in this lap.
- Each whole body was first cut into a BLOCK LIST — labels `L0, L1, …`
  in address order, which is `canon2_branching`'s own convention — with
  every transfer whose target lies inside the unit's own bounds
  rewritten onto its label, and every transfer out of bounds left
  exactly as the compiler wrote it.

## 3.2 Where the form does not reach — three shortfalls, by cause

### 3.2.1 `%r15` is the region's base and also the interpreter's frame pointer

- `region36.py` section 2: "%r15 is a SYMBOLIC BASE … no unit's core may
  mention it (a core that does is REFUSED BY NAME)".
- php's specialized executor handlers read their operands out of the VM
  frame through `%r15`, and DWARF records ZERO formal parameters for
  them. HotSpot uses `%r15` as the thread pointer, so both JIT nmethods
  name it too.
- **Five of eleven units are refused by name on this alone**:
  `java/op_1`, `java/op_2`, and the three php `ZEND_ADD_*` handlers.
  They carry two different refusal texts — the java pair reach
  `canon36_universal.render`, which refuses because the core names the
  region base; the php trio are refused one step earlier, because they
  declare no formal parameters at all and their operands only exist
  behind `%r15`. Same collision, two places it surfaces.
- This is a collision between two conventions, not a bug in either. It
  needs a ruling.

### 3.2.2 There is no block kind for memory the unit obtains at run time

- The six kinds are input, constant, temp, result, guard-outcome,
  own-address. A `PyLongObject` returned by `long_alloc`, a `zval` a php
  handler writes into, an object a ruby handler fills — none of them is
  any of the six.
- Nine of the eleven bodies write through a pointer they obtained rather
  than one they arrived with (§5.1). The store has no block to land in,
  so the answer cannot be read off the result block.

### 3.2.3 An input block holds a POINTER, not the object it addresses

- The arrival contract binds input block `i` to the same symbol as the
  argument arriving in register `i`. For an interpreter that argument is
  an address.
- So `mov 0x10(%rdi),%rax` — CPython reading a's tag — asks the region
  for a byte the region does not model. That is the FIRST thing the gate
  refused for `cpython/long_add`, quoted verbatim in §4.2.
- Four of eleven bodies read at a fixed displacement from an arriving
  pointer (§5.1).

---

# 4. The gate, against each unit's OWN ship code

## 4.1 The movement, all eleven, with cause

Lane log: `20260905T060329Z__t94_l12_transcripts2.sh.log`.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json'))
for m in d['verdict_movements']:
    print('%-58s %-18s  to  %-12s %s' % (m['unit'], m['from'], m['to'], m['cause'][:100]))
"
cpython/long_add_fastpath                                  PROVED              to  UNDECIDED    the unit's own ship body: NotModeled: operand '0x10(%rdi)' is neither an immediate nor a plain regis
java/op_1                                                  PROVED              to  UNDECIDED    the universal form refused by name: the core names the region base -- this unit's own core mentions 
java/op_2                                                  PROVED              to  UNDECIDED    the universal form refused by name: the core names the region base -- this unit's own core mentions 
ruby/vm_opt_plus                                           NO_CANONICAL_TEXT   to  NO_BODY      no STT_FUNC symbol named 'vm_opt_plus' exists in this binary's own symbol table, so this handler's f
ruby/rb_fix_plus                                           PROVED              to  UNDECIDED    the unit's own ship body: NotModeled: mnemonic 'endbr64' has no symbolic model in this checker
ruby/rb_int_plus                                           PROVED              to  UNDECIDED    the unit's own ship body: NotModeled: mnemonic 'endbr64' has no symbolic model in this checker
ruby/rb_big_plus                                           NO_CANONICAL_TEXT   to  UNDECIDED    the unit's own ship body: NotModeled: mnemonic 'endbr64' has no symbolic model in this checker
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                PROVED              to  UNDECIDED    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           PROVED              to  UNDECIDED    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER PROVED              to  UNDECIDED    this handler declares ZERO formal parameters and reads its operands out of the VM frame through %r15
php/add_function                                           PROVED              to  UNDECIDED    the unit's own ship body: NotModeled: mnemonic 'endbr64' has no symbolic model in this checker
```

Summary of the movement: **9 PROVED → UNDECIDED, 1 NO_CANONICAL_TEXT →
UNDECIDED, 1 NO_CANONICAL_TEXT → NO_BODY. Nothing moved to DISPROVED,
and nothing stayed PROVED.**

## 4.2 The causes, reported by cause and not by sighting

The gate names the FIRST thing it cannot carry, which is one sighting.
`t94_analysis.py` walks each body to the end and inventories every
cause. Four causes carry all eleven units:

1. **The universal form refuses by name on `%r15`** — 5 units
   (`java/op_1`, `java/op_2`, three php `ZEND_ADD_*`). §3.2.1.
2. **The reference has no model for a memory operand that dereferences
   an arriving pointer** — this is what stopped `cpython/long_add`
   first. **LITERAL**, the checker's own words, from
   `t94_recarve.json` record 0, field `cause`:
   `the unit's own ship body: NotModeled: operand '0x10(%rdi)' is neither an immediate nor a plain register`.
3. **The reference has no model for `endbr64`** — this is what stopped
   the four remaining gated units first, because `endbr64` is their
   first instruction. It is a CET landing pad and computes nothing. It
   is a table gap, and it MASKS the causes below rather than being the
   real obstruction.
4. **Behind those, in every gated body: branching and transfers out.**
   Counted per unit by `t94_analysis.py`:

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json'))
for r in d['records']:
    c=r.get('causes')
    if c is None: print('%-58s no body' % r['unit']); continue
    print('%-58s inside %2d  runtime %2d  ptr-reads %2d  writes %2d' % (r['unit'], len(c['transfers_inside_its_own_bounds']), len(c['transfers_into_the_runtime']), len(c['reads_through_an_arriving_pointer']), len(c['memory_writes'])))
"
cpython/long_add_fastpath                                  inside 10  runtime  2  ptr-reads  3  writes  7
java/op_1                                                  inside  3  runtime  2  ptr-reads  0  writes  4
java/op_2                                                  inside  6  runtime  3  ptr-reads  0  writes  4
ruby/vm_opt_plus                                           no body
ruby/rb_fix_plus                                           inside 19  runtime  5  ptr-reads  0  writes  7
ruby/rb_int_plus                                           inside 34  runtime  7  ptr-reads  1  writes  8
ruby/rb_big_plus                                           inside 23  runtime  5  ptr-reads  3  writes  6
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                inside 11  runtime  0  ptr-reads  0  writes  6
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           inside  2  runtime  0  ptr-reads  0  writes  4
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER inside  0  runtime  0  ptr-reads  0  writes  2
php/add_function                                           inside 10  runtime  1  ptr-reads 12  writes 10
```

   The same numbers as a table:

| unit | transfers inside its own bounds | transfers into the runtime | reads through an arriving pointer | memory writes |
|---|---|---|---|---|
| cpython/long_add | 10 | 2 | 3 | 7 |
| java/op_1 | 3 | 2 | 0 | 4 |
| java/op_2 | 6 | 3 | 0 | 4 |
| ruby/rb_fix_plus | 19 | 5 | 0 | 7 |
| ruby/rb_int_plus | 34 | 7 | 1 | 8 |
| ruby/rb_big_plus | 23 | 5 | 3 | 6 |
| php/ZEND_ADD_SPEC_… | 11 | 0 | 0 | 6 |
| php/ZEND_ADD_LONG_SPEC_… | 2 | 0 | 0 | 4 |
| php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_… | 0 | 0 | 0 | 2 |
| php/add_function | 10 | 1 | 12 | 10 |

  `gate.py` already rules on the first column: a body that transfers to
  a place it defines itself has a page order that is not its run order,
  so a text-order walk has no one answer to reach. Nine of ten bodies
  are in that state. `php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_…` is the one
  straight-line whole handler in the population, and it is refused
  earlier, on `%r15`.

**Honest limit of that table, stated rather than hidden.** The
"unmodelled mnemonic" inventory behind it asks the checker one
instruction at a time from a fresh simulator, so refusals worded "no
preceding cmp/test" and "empty symbolic push stack" are artefacts of the
probe, not gaps in the checker. `t94_analysis.py` labels each row with
which of the two it is, in its `kind` field.

## 4.3 Solver time — no verdict here was a timeout

- Each gate is asked at 20,000 ms, and re-asked at 120,000 ms if and
  only if the first answer was UNDECIDED FOR TIME.
- **No unit reached the solver.** Every UNDECIDED in §4.1 comes from the
  simulator refusing to build a term, before any solver call. So the
  longer run was not triggered for any unit, and
  `answer_changed_with_more_room` is `false` for all eleven.
- This means task 91's finding (120,000 ms turns some UNDECIDED into
  DISPROVED and never into a proof) has no purchase on this population
  yet: nothing here is solver-bound.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json'))
for r in d['records']:
    print('%-58s %-10s changed_with_more_room=%s' % (r['unit'], r.get('gate_at_120000ms',{}).get('verdict'), r.get('answer_changed_with_more_room')))
"
cpython/long_add_fastpath                                  NOT_RUN    changed_with_more_room=False
java/op_1                                                  None       changed_with_more_room=None
java/op_2                                                  None       changed_with_more_room=None
ruby/vm_opt_plus                                           None       changed_with_more_room=None
ruby/rb_fix_plus                                           NOT_RUN    changed_with_more_room=False
ruby/rb_int_plus                                           NOT_RUN    changed_with_more_room=False
ruby/rb_big_plus                                           NOT_RUN    changed_with_more_room=False
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                None       changed_with_more_room=None
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER           None       changed_with_more_room=None
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER None       changed_with_more_room=None
php/add_function                                           NOT_RUN    changed_with_more_room=False
```

**GLOSS.** `NOT_RUN` means the 20,000 ms run did not hit its time limit,
so the longer run would have asked the same solver the same question.
`None` means the unit never reached a gate at all — it was refused by
name by the form, so no `gate_at_120000ms` field exists on its record.

---

# 5. Recurring paths, and the super-op route checked rather than assumed

## 5.1 The recurring paths, found in the bodies themselves

Lane log: `20260905T060329Z__t94_l12_transcripts2.sh.log`.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json'))
c={}
for r in d['records']:
    for p in r.get('recurring_paths',[]):
        c.setdefault(p['recurring_path'],[]).append(r['unit'])
for k in sorted(c, key=lambda x: 0-len(c[x])):
    print('%2d  %s' % (len(c[k]), k))
"
 9  answer written through a pointer the body obtained, not through one it arrived with
 9  the body chooses between alternative computations
 4  operand unpacking -- a read at a fixed displacement from an arriving pointer
 3  allocation preamble and its answer test
```

**LITERAL**, one instance of the allocation preamble, from
`t94_analysis.json`, record `cpython/long_add_fastpath`:

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for p in r['recurring_paths']:
    if p['recurring_path'].startswith('allocation'):
        for line in p['instructions']: print(line)
"
cmovns %rdi,%rdx
cmovs %rax,%rcx
mov $0x2,%edi
mov %rdx,0x10(%rsp)
mov %rcx,0x8(%rsp)
mov %rcx,0x18(%rsp)
call 131d70 <long_alloc>
test %rax,%rax
je 137474 <long_add+0x104>
mov 0x8(%rsp),%rcx
```

**GLOSS.** Three arguments are parked in the outgoing frame, the
allocator is called, and its answer is tested for null before anything
is written through it. z3 cannot take this directly because the transfer
leaves the unit: what comes back in `%rax` is not a function of anything
inside these bounds.

## 5.2 The reference-count sequence, and what was actually found

- I looked for a read-modify-write of a word at a fixed displacement
  from a pointer — the shape a reference count takes. In these
  particular ship bodies at these optimisation levels, what is present
  is the more general shape: a field written through a pointer. It is
  reported under that name rather than under "reference count", because
  naming it a refcount would be a claim the bytes here do not carry.
- `cpython/long_add`'s own refcount work sits in `_PyLong_FromMedium`
  and `long_alloc`, which are transfers OUT of these bounds, so they
  belong to the runtime_callee node (0_3_5_1_8), not to this body.

## 5.3 The super-op route — checked, and it does not hold today

Lane log: `20260905T060329Z__t94_l12_transcripts2.sh.log`.

```
$ python3 -c "
import json
d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json'))['super_op_route']
print('candidates in the miner artifact:', d['candidate_count'])
print('languages the miner mined       :', d['languages_the_miner_mined'])
print('interpreter languages among them:', d['interpreter_languages_in_that_population'])
print('candidates occurring in these bodies:', len(d['candidates_occurring_in_these_bodies']))
for h in d['candidates_occurring_in_these_bodies']:
    print('   ', h['unit'], h['candidate_instructions'], 'support', h['support'], h['languages'])
"
candidates in the miner artifact: 2173
languages the miner mined       : ['c', 'cpp', 'go', 'rust', 'swift']
interpreter languages among them: []
candidates occurring in these bodies: 1
    ruby/rb_int_plus ['pop %P0', 'ret'] support 13 ['go']
```

**GLOSS, and this is the answer to the brief's question 4.**

- The miner's population is the five COMPILED languages. Its own
  `load_report` counts 610 c units, 770 cpp, 107 go, 125 rust, 167
  swift, and no interpreter unit has ever been mined.
- Searching the 2,173 candidates against these eleven bodies — using the
  miner's OWN normalizer, `super_op_miner.normalize_positionally`,
  imported unmodified — finds **one** hit, and it is `pop <reg>; ret`,
  a function epilogue mined from go. It covers none of the four
  recurring paths in §5.1.
- So: **the owner's stated route is sound in shape and empty in content
  today.** The miner is the right instrument — recurrence over machine
  form, no operator token anywhere near the grouping — but it has never
  been pointed at interpreter bodies, so it carries no candidate for an
  allocation preamble, an operand unpack, or a store through an obtained
  pointer. Pointing it at the interpreter population is a decision, not
  a repair, so it is in §0.2 rather than done here.

---

# 6. `lineage_carve.py`, retired for boundary use only

**LITERAL**, the lines added at the top of
`Research/op_pipeline/lineage_carve.py` (nothing else in the file
changed, and neither `lineage_carve.json` nor any downstream artifact
was touched):

```
$ sed -n '4,14p' /projects/PseudoCoupHQ/Research/op_pipeline/lineage_carve.py

RETIRED FOR BOUNDARY USE, 2026-09-05, by the owner's ruling "the unit's
boundary" in
`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/CORE_0_3_5_1_arch_unit.md`
-- a unit is a FUNCTION BODY whose bounds are READ from the symbol
table and DWARF (`t94_read_bounds.py`), never computed by the taint
propagation below.  ONLY THE BOUNDARY USE IS RETIRED: this program's
propagation is still the evidence for arrival lineages, and this file
and its outputs stay on disk as records and as that evidence.

THE RULE THIS IMPLEMENTS (the owner, 2026-08-31, AgentMemory: "THE ARRIVAL /
```

---

# 7. Gates

## 7.1 The spelling guard, one process, over every artifact this lap wrote

Lane log: `20260905T060329Z__t94_l12_transcripts2.sh.log`.

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json /projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json /projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS t94_bounds.json -- no operator token in any key, grouping, pairing or row structure
PASS t94_recarve.json -- no operator token in any key, grouping, pairing or row structure
PASS t94_analysis.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt /projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json /projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json /projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json
/projects/PseudoCoupHQ/Research/op_pipeline/t94_bounds.json:0
/projects/PseudoCoupHQ/Research/op_pipeline/t94_recarve.json:0
/projects/PseudoCoupHQ/Research/op_pipeline/t94_analysis.json:0
```

- The checker is unmodified: `git diff --stat -- Research/op_pipeline/check_no_spelling_keys.py`
  printed nothing (lane log `20260905T055219Z__t94_l7_final.sh.log`,
  section [8/8]); its last commit is `fdff0b254fd7ebd8032128803146af0e3092812b`.
- **It caught this lap twice and both were fixed in the artifacts, never
  by exempting anything.** Recorded because the point of a guard is the
  catches, not the passes:
  1. `t94_recarve.json` used the dict key `new` on all eleven records.
     `new` is in the operator inventory. Renamed to `recarved`.
  2. `t94_analysis.json` carried the mnemonic `or` under a field named
     `mnemonic`, which is not one of the checker's prose fields.
     Renamed to `mnem`, which is.
  The failing run is in lane log `20260905T055219Z__t94_l7_final.sh.log`,
  section [5/8], and the passing run is above.

## 7.2 The display label

The operator token appears exactly once per unit, in the field `label`
on a record that also carries `language` and `unit` — the shape the
checker names as a per-unit display label. Nothing in any of the three
programs keys, groups, pairs or selects on it.

---

# 8. Memory and time

- **Stated bound: 6 GB, abort by name.** `T94_BOUNDS_MEMORY_ABORT`,
  `T94_RECARVE_MEMORY_ABORT`, `T94_ANALYSIS_MEMORY_ABORT`. Each program
  checks its own peak and prints it.
- **Measured peaks** (`ru_maxrss`, printed by each program at the end of
  its run, lane log `20260905T055731Z__t94_l9_final.sh.log`):
  - `t94_read_bounds.py` — **1,753,984 kB (1.67 GB)**. This is the DWARF
    scan holding one compilation unit's DIEs at a time across ruby's and
    php's debug info.
  - `t94_recarve.py` — **56,068 kB (55 MB)**.
  - `t94_analysis.py` — **59,636 kB (58 MB)**.
- No run hit a time or memory limit, so no run was re-run with more
  room. Longest lane: 52.6 s (`t94_l8_final.sh`).

---

# 9. Artifacts, every one named

## 9.1 Written this lap (new files only)

| path | what it is |
|---|---|
| `Research/op_pipeline/t94_read_bounds.py` | reads each handler function's bounds from the symbol table and DWARF, dumps the whole body |
| `Research/op_pipeline/t94_bounds.json` | its output: per unit, symbol rows, DWARF rows, bounds, and the body |
| `Research/op_pipeline/t94_recarve.py` | re-carve, render through region36, gate against the unit's own ship code |
| `Research/op_pipeline/t94_recarve.json` | its output: old bounds, new bounds, universal form, verdict, movement |
| `Research/op_pipeline/t94_analysis.py` | causes by cause, recurring paths, the super-op route checked |
| `Research/op_pipeline/t94_analysis.json` | its output |
| `Research/op_pipeline/t94_l1_inventory.sh` … `t94_l10_transcripts.sh` | the lane scripts, one per submission |

## 9.2 Edited this lap

| path | edit |
|---|---|
| `Research/op_pipeline/lineage_carve.py` | one header block added (§6). Nothing removed. |

## 9.3 Read read-only

`interp_canon35.json`, `interp_canon34.json`,
`canon_interp_units_cpython.json`, `canon_interp_units_java.json`,
`interp_fastpath.json`, `interp_jvm.json`, `op_units_ruby.json`,
`op_units_php.json`, `super_op_candidates.json`, `lineage_carve.json`,
and the modules `region36.py`, `canon36_universal.py`, `canon.py`,
`canon2.py`, `block_cutter.py`, `super_op_miner.py`,
`check_no_spelling_keys.py`.

## 9.4 Superseded, kept as records

`interp_canon34.json`, `interp_canon35.json`,
`canon_interp_units_cpython.json`, `canon_interp_units_java.json`,
`lineage_carve.json`. None was edited or deleted.

## 9.5 The lane logs

| lane | log |
|---|---|
| `t94_l1_inventory.sh` | `20260905T053713Z__t94_l1_inventory.sh.log` |
| `t94_l2_read_bounds.sh` | `20260905T054103Z__t94_l2_read_bounds.sh.log` (failed: `/usr/bin/time` absent in the image) |
| `t94_l3_read_bounds.sh` | `20260905T054139Z__t94_l3_read_bounds.sh.log` (failed: pyelftools section-type guard) |
| `t94_l4_read_bounds.sh` | `20260905T054234Z__t94_l4_read_bounds.sh.log` |
| `t94_l5_recarve.sh` | `20260905T054718Z__t94_l5_recarve.sh.log` |
| `t94_l6_recarve_and_analyse.sh` | `20260905T055022Z__t94_l6_recarve_and_analyse.sh.log` |
| `t94_l7_final.sh` | `20260905T055219Z__t94_l7_final.sh.log` (spelling guard FAILED here) |
| `t94_l8_final.sh` | `20260905T055343Z__t94_l8_final.sh.log` |
| `t94_l9_final.sh` | `20260905T055731Z__t94_l9_final.sh.log` |
| `t94_l10_transcripts.sh` | `20260905T055708Z__t94_l10_transcripts.sh.log` |
| `t94_l11_verify_log199.sh` | `20260905T060227Z__t94_l11_verify_log199.sh.log` (the log verifier's first pass over this log; its findings are §11) |
| `t94_l12_transcripts2.sh` | `20260905T060329Z__t94_l12_transcripts2.sh.log` (the transcripts this log now pastes, re-run with absolute paths) |
| `t94_l13_verify_log199.sh` | `20260905T060614Z__t94_l13_verify_log199.sh.log` (the log verifier's second pass; §11) |

All under `~/Programming/Airlock/agent/logs/`. The two failed lanes are
listed rather than hidden; both were program defects fixed the same lap.

---

# 10. What the STOP RULE would have stopped for, and did not

- "A handler's function bounds cannot be read from the binary" — did not
  fire. Ten of eleven read cleanly; `ruby/vm_opt_plus` has no ship body
  at all, which is a recorded absence rather than an unreadable bound.
- "The canonical form's virtual memory cannot carry a body's memory
  traffic and the shortfall needs a new shape" — **this one is live.**
  §3.2 names three shortfalls. I did not design a fourth block kind, did
  not widen the region base rule, and did not touch `region36.py`. The
  shortfalls are in §0.2 as flags.
- "The honest fix needs a role key or field whitelist" — did not fire.
- No proof was kept by keeping an old boundary.

---

# 11. This log run through the log verifier

`check_conventions_log_claims.py` (task 90) was run against this file
inside Airlock, twice.

- **First pass**, lane log `20260905T060227Z__t94_l11_verify_log199.sh.log`:
  27 claims, MATCHES 0, DIFFERS 5, UNVERIFIABLE 15, REFUSED 7. The five
  DIFFERS were all one cause: the verifier's working directory is
  `/projects/PseudoCoupHQ`, and my pasted commands used paths relative
  to `Research/op_pipeline`, so they could not open their own files.
- **Fix applied to this log, not to the verifier**: every pasted command
  now uses an absolute path, and none contains a bare `>` (the
  verifier's `redirects_into_a_path` rule refuses a command whose text
  carries one, and my `->` in a format string tripped it).
- **Second pass**, lane log `20260905T060614Z__t94_l13_verify_log199.sh.log`:
  31 claims, **MATCHES 19, DIFFERS 0, UNVERIFIABLE 8, REFUSED 4**.
- The four REFUSED are the three `readelf` blocks and the one `objdump`
  block, all with the rule `head_not_on_the_read_only_allowlist`. Those
  two programs are not on the verifier's allowlist. They are kept
  because they are the primary evidence for §1.2 and §1.6, and each is
  paired with a verifier-runnable command carrying the same numbers
  (§1.2a, §1.3).
- The eight UNVERIFIABLE are five prose statements and three
  values-in-motion glosses. A gloss has nothing to re-run by
  construction — it is a reading of the literal above it, and the
  literal above each of them MATCHES.

This section itself cannot be verified from inside the file it
describes: adding it changes the line numbers the second pass reported.
The two lane logs named above hold the verifier's own output.
