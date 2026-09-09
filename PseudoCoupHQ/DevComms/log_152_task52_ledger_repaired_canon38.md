# log 152 — TASK 52: the ledger, repaired (canon38)

Date: 2026-09-02. Round 11, task 52 (the centerpiece). Brief: log 151.
Rulings implemented: 2, 3, 4, 5 of the ROUND 10 RULINGS (AgentMemory;
audit in log 150).

Every rendering below is labelled LITERAL / GLOSS per protocol §5.1a;
a gloss never appears without its literal. Every figure names its
population per §3.4a.

---

# 0. The walkthrough, in plain words, before any figure (§3.5)

`ledger47.py` was not edited. A new file, `ledger48.py`, imports from
it the twenty names that do not change (the refusal class, the
line and operand readers, the scratch-register rule, the weave, the
flag-setter table) and replaces the four things the rulings name: the
block list, the dataflow walk's destination rule, the flag-reader
pattern, and the way a branch target is spelled. Three new drivers
(`canon38_wrapped.py`, `canon38_interp.py`, `canon38_regen.py`) are
the task 47 drivers with the ledger48 import, the body's own bytes
passed in, and the `role` line taken out of every artifact they write.

All three populations were re-rendered: 1,779 original units, 11
interpreter units, 29,288 regenerated units — 31,078 in total, the
same population task 47 wrapped. Every unit was gate-proved against
its OWN ship code as task 47 did, with the same gate module, and 2,728
of the proved texts were assembled with `as --64` and read back with
`objdump -d`.

The outcome is that the repair changed the LEDGER and the STORED TEXT
and changed no verdict at all. 30,436 units proved, 642 refused —
digit for digit task 47's line. Nothing was lost. What moved is what
the rulings aimed at: the answer row of `c/op_210` is now produced by
`idiv` instead of `mov`; 3,408 STACK rows and 3,090 X87 rows exist
where there were none; 325 guard rows made by an unconditional
transfer are gone; 19,934 comparison rows are typed `flags only`
instead of being recorded as writes; and the number of DISTINCT
wrapped texts fell from 6,277 to 2,997, because no stored text carries
a symbol comment any more.

One thing got WORSE-LOOKING and is better: 305 units used to say their
answer was produced by `push`. It was not — those bodies call a
library routine and the answer is the callee's. canon38 says instead
that no row in the body produces it. That is a wrong term withdrawn,
not a right one lost, and §5 names it as the next hole.

The unmodified guard walked all 336 canon38 files in one process:
336 PASS, 0 FAIL, `grep -c exempt` = 0, exit code 0. The same
unmodified guard over task 47's canon37 files with the `role` line
removed (copies in a scratch directory; the canon37 files on disk were
not touched) FAILS on 273 of 332 files, with exactly the 579 places in
`canon37_wrapped_c.json` that log 150 §3 predicted.

---

# 1. The verdict, with its population

## 1.1 The one-line state

LITERAL — `canon38_zero_regression.txt`, the outcome block:

```
OUTCOME, per population
  interpreter   canon37 {"REFUSED": 2, "WRAPPED_TEXT_PROVED": 9}
                canon38 {"REFUSED": 2, "WRAPPED_TEXT_PROVED": 9}
  original      canon37 {"REFUSED": 16, "WRAPPED_TEXT_PROVED": 1763}
                canon38 {"REFUSED": 16, "WRAPPED_TEXT_PROVED": 1763}
  regenerated   canon37 {"REFUSED": 624, "WRAPPED_TEXT_PROVED": 28664}
                canon38 {"REFUSED": 624, "WRAPPED_TEXT_PROVED": 28664}
```

GLOSS: the populations are the ones the brief names — 1,779 original
(610 c, 770 cpp, 107 go, 125 rust, 167 swift), 11 interpreter, 29,288
regenerated. 9 + 1,763 + 28,664 = **30,436 proved**; 2 + 16 + 624 =
**642 refused**; total 31,078. Those are log 146 §1.2's figures for
canon37, unchanged.

## 1.2 Zero regression, computed rather than asserted

LITERAL — same file:

```
EVERY UNIT WHOSE OUTCOME CHANGED
  outcome changed: 0
  lost WRAPPED_TEXT_PROVED: 0

VERDICT CHANGES AMONG UNITS PROVED IN BOTH LAPS
  PROVED_BY_CONSTRUCTION -> PROVED_BY_CONSTRUCTION     11889
  PROVED_EQUAL -> PROVED_EQUAL                         17379
  PROVED_ON_SHIP -> PROVED_ON_SHIP                     1168
```

GLOSS: over the 31,078 units present in both laps, no unit changed
outcome and no unit changed verdict. 11,889 + 17,379 + 1,168 = 30,436,
the whole proved population. So the brief's step 4 ("no unit loses
WRAPPED_TEXT_PROVED without a named, proved cause") is satisfied with
an empty list of causes: none lost it.

## 1.3 The refusals are the same refusals, by cause

LITERAL — computed this session over both laps' artifacts:

```
canon37 {"interpreter/no canonical text": 2,
         "original/never returns": 16,
         "regenerated/never returns": 408,
         "regenerated/no answer home": 216}
canon38 {"interpreter/no canonical text": 2,
         "original/never returns": 16,
         "regenerated/never returns": 408,
         "regenerated/no answer home": 216}
```

GLOSS: four causes, 642 units, identical on both laps. `never
returns` is a body with no `ret`; `no answer home` is a body whose own
code names no register the answer is left in.

---

# 2. Ruling 3 — the per-opcode destination table, with values moving

## 2.1 The table

LITERAL — `ledger48.py`, `DESTINATION_RULES`, the keys and the
`writes` / `reads_implicitly` of each (ACCUMULATOR is the %rax family,
DATA_REGISTER the %rdx family):

| opcode | writes | reads implicitly | only when operand count is |
|---|---|---|---|
| `idiv` | rax = quotient, rdx = remainder | rax, rdx | any |
| `div` | rax = quotient, rdx = remainder | rax, rdx | any |
| `mul` | rax = low half, rdx = high half | rax | 1 |
| `imul` | rax = low half, rdx = high half | rax | 1 |
| `cltd` | rdx | rax | 0 |
| `cqto` | rdx | rax | 0 |
| `cwtl` | rax | rax | 0 |
| `cltq` | rax | rax | 0 |
| `cbtw` | rax | rax | 0 |

GLOSS: `only when operand count is` is how the two- and three-operand
`imul` stays on the ordinary rule — those forms DO name their
destination, so the table must not claim them. The lookup strips one
operand-size suffix first, so `idivl` and `idivq` both find `idiv`.

## 2.2 The values in motion — `c/op_210`, first argument 20, second 6

LITERAL — the body (`canon38_wrapped_c.json`, unit `c/op_210`):

```
mov %edi,%eax; cltd; idiv %esi; ret
```

LITERAL — canon37's ledger for it (`canon38_acceptance.txt`, part a):

```
  row      size type                   produced by            operands
  IN-0     8    8-byte general value   arrival
  IN-1     8    8-byte general value   arrival
  TEMP-0   8    8-byte general value   mov                    IN-0
  TEMP-1   8    8-byte general value   idiv                   IN-1
  OUT-0    4    4-byte general value   mov                    TEMP-0
```

LITERAL — canon38's ledger for the same unit, same file:

```
  row      size type                   produced by                                                                operands
  IN-0     8    8-byte general value   {"kind": "non_opcode_phrase", "phrase": "arrival"}
  IN-1     8    8-byte general value   {"kind": "non_opcode_phrase", "phrase": "arrival"}
  TEMP-0   8    8-byte general value   {"kind": "arch_opcode", "mnem": "mov"}                                      IN-0
  TEMP-1   8    8-byte general value   {"kind": "arch_opcode", "mnem": "cltd", "writes_which_half": "the sign of the accumulator"}  TEMP-0
  TEMP-2   8    8-byte general value   {"kind": "arch_opcode", "mnem": "idiv", "writes_which_half": "quotient"}     TEMP-0,TEMP-1,IN-1
  TEMP-3   8    8-byte general value   {"kind": "arch_opcode", "mnem": "idiv", "writes_which_half": "remainder"}    TEMP-0,TEMP-1,IN-1
  OUT-0    4    4-byte general value   {"kind": "arch_opcode", "mnem": "idiv", "writes_which_half": "quotient"}     TEMP-2
```

GLOSS, step by step, with 20 and 6 moving through:

1. `mov %edi,%eax` — the accumulator becomes 20. Row TEMP-0 holds it,
   produced by `mov`, reading IN-0. Same on both laps.
2. `cltd` — the data register becomes the sign of the accumulator, 0
   for a positive 20. canon37 made NO ROW: the opcode names no
   operand, so ledger47's walk skipped it. canon38's table has a row
   for it: TEMP-1, produced by `cltd`, reading TEMP-0.
3. `idiv %esi` — the machine divides the pair (data register,
   accumulator) = (0, 20) by 6, leaving quotient 3 in the accumulator
   and remainder 2 in the data register. canon37 attached its one row
   to the DIVISOR (TEMP-1, produced by `idiv`, reading IN-1) and left
   the accumulator still pointing at TEMP-0. canon38 makes TWO rows,
   one per written half, each reading (TEMP-0, TEMP-1, IN-1) — the
   accumulator, the data register, and the divisor.
4. The answer. canon37's OUT-0 says "produced by `mov`, reading
   TEMP-0" — that is 20, the DIVIDEND. canon38's OUT-0 says "produced
   by `idiv`, the quotient half, reading TEMP-2" — that is 3.

LITERAL — the verdict on both laps, same file:

```
  canon37 outcome WRAPPED_TEXT_PROVED / verdict PROVED_ON_SHIP
  canon38 outcome WRAPPED_TEXT_PROVED / verdict PROVED_ON_SHIP
```

GLOSS: the ledger is provenance, not text. The wrapped text for this
unit is character-identical except for the OUT block's ledger entry
offset (§3.4), so the proof is the same proof.

## 2.3 The size of the table's effect, over 31,078 units

LITERAL — `canon38_zero_regression.txt`:

```
  units with a row from the destination table                1567
  destination-table rows in total                            3807
```

GLOSS: 1,567 of the 31,078 units have at least one row the table
made; 3,807 rows in all (two per `idiv`/`div`/one-operand
`mul`/`imul`, one per `cltd`/`cqto`/`cwtl`). Log 147 §4.1 counted
1,558 census rows under the implicit-destination cause; the figures
are different measurements (census rows against ledger rows) and both
are stated rather than reconciled by rounding.

## 2.4 An unconditional transfer is no longer a flag reader

LITERAL — same file:

```
THE GUARD ROWS AN UNCONDITIONAL TRANSFER USED TO MAKE
  canon37: 325
  canon38: 0
```

GLOSS: log 147 §5.3 item 3 counted 324 such rows in the census's
scope; over the whole 31,078-unit population there are 325, and there
are now none. `ledger48.is_flag_reading_transfer` returns False for
`jmp` and `jmpq`, and a `jmp` line now makes no row at all.

## 2.5 A comparison writes flags, not its destination

LITERAL — same file:

```
  units with a `flags only` row                              15092
  `flags only` rows in total                                 19934
```

GLOSS — the mechanism, with `cmp $0x40,%ecx` from `go/op_174`:

- canon37: the row's destination was taken as `%ecx`, so a TEMP row
  typed "8-byte general value" was made, produced by `cmp`, and the
  walk repointed the %rcx family at it. Any later reader of %rcx then
  read a row that claims `cmp` wrote it. It did not.
- canon38: the row is typed `flags only`, and the walk does NOT
  repoint %rcx — the register keeps the value it had. The row is
  remembered as the current flag state and becomes the FIRST OPERAND
  of the next flag-reading row, so the pair's lineage is in the
  ledger rather than in prose. `go/op_110`'s `GUARD-0` reads `TEMP-0`
  in canon38 and read nothing in canon37 (§4.2's literal shows both).

---

# 3. Ruling 2 — two more block kinds

## 3.1 The order, and where it is read

LITERAL — `ledger48.py`:

```
BLOCK_ORDER = ("IN", "CONST", "TEMP", "OWN", "STACK", "X87", "GUARD",
               "OUT")
```

GLOSS: eight entries of eight bytes each, so the ledger table is 0x40
bytes and the OUT block's entry moved from offset 0x28 to 0x38. That
offset is the ONLY difference in the wrapped text of a unit with no
branch, and §5.2 of this log shows it in `c/op_109`.

LITERAL — the `.data` the assembler emitted for `go/op_174`
(`canon38_assemble_go_op_174.txt`):

```
ledger:
    .quad 0    # the base address of the IN block, written by the runner
    .quad 0    # the base address of the CONST block, written by the runner
    .quad 0    # the base address of the TEMP block, written by the runner
    .quad 0    # the base address of the OWN block, written by the runner
    .quad 0    # the base address of the STACK block, written by the runner
    .quad 0    # the base address of the X87 block, written by the runner
    .quad 0    # the base address of the GUARD block, written by the runner
    .quad 0    # the base address of the OUT block, written by the runner
```

## 3.2 STACK — the acceptance instance, `c/regen_11491`

LITERAL — `canon38_acceptance.txt`, part (b); the unit was chosen by
the MNEMONICS its body spells (`push` and `pop`), never by a token:

```
canon37 (ledger47) -- no STACK block
  body   : push %rax; call 6 <op_11491+0x6> !!reloc=R_X86_64_PLT32:__divti3-0x4; pop %rcx; ret
  row      size type                   produced by            operands
  IN-0     8    8-byte general value   arrival
  TEMP-0   8    8-byte general value   push
  TEMP-1   8    8-byte general value   pop                    IN-0
  OUT-0    8    8-byte general value   push                   TEMP-0

canon38 (ledger48)
  stored : push %rax; call L0 !!reloc=R_X86_64_PLT32:__divti3-0x4; L0:; pop %rcx; ret
  row      size type                              produced by                             operands
  IN-0     8    8-byte general value              {"kind": "non_opcode_phrase", "phrase": "arrival"}
  STACK-0  8    8-byte value on the machine stack {"kind": "arch_opcode", "mnem": "push"}
  OUT-0    8    8-byte general value              {"kind": "non_opcode_phrase", "phrase": "the body's last write to %rax"}
  STACK rows: STACK-0
```

GLOSS: canon37 invented two TEMP rows saying `push` wrote %rax and
`pop` wrote %rcx from IN-0 — neither is true of the machine. canon38
makes one STACK row for what `push` moved, and `pop %rcx` takes that
row back and binds %rcx to it (no new row, because the value is the
one already recorded). The answer row honestly says nothing in this
body produced it: the answer is `__divti3`'s. That is §5.1's open
hole, not a defect of the STACK block.

## 3.3 X87 — the acceptance instance, `cpp/regen_36796`

LITERAL — `canon38_acceptance.txt`, part (c); chosen by the mnemonic
`fucomip`:

```
  body   : fldt 0x18(%rsp); fldt 0x8(%rsp); fucomip %st(1),%st; fstp %st(0); seta %al; ret

canon37 (ledger47) -- no X87 block
  row      size type                   produced by            operands
  GUARD-0  8    flag-derived value     ['fucomip', 'seta']
  OUT-0    1    1-byte general value   ['fucomip', 'seta']    GUARD-0

canon38 (ledger48)
  row      size type              produced by                                          operands
  X87-0    16   x87 stack value   {"kind": "arch_opcode", "mnem": "fldt"}
  X87-1    16   x87 stack value   {"kind": "arch_opcode", "mnem": "fldt"}
  TEMP-0   8    flags only        {"kind": "arch_opcode", "mnem": "fucomip"}            X87-0,X87-1
  GUARD-0  8    flag-derived value {"kind": "flag_pair", "mnem": ["fucomip", "seta"]}   TEMP-0
  OUT-0    1    1-byte general value {"kind": "flag_pair", "mnem": ["fucomip", "seta"]} GUARD-0
  X87 rows: X87-0, X87-1
```

GLOSS, with values: `fldt 0x18(%rsp)` pushes a long double onto the
x87 register stack — that becomes X87-1 by the time the second load
has pushed above it, and X87-0 is the second load's value. `fucomip
%st(1),%st` compares the two positions the operands name; canon37's
guard row had NO OPERANDS, so log 147 §4.1's recorded reason ("neither
side of the comparison exists as a row") held. canon38's flags row
reads X87-0 and X87-1, the guard row reads the flags row, and the
answer reads the guard row. The lineage is unbroken from OUT-0 to the
two loads.

## 3.4 How big both blocks are, over 31,078 units

LITERAL — `canon38_zero_regression.txt`:

```
  units with a STACK row                                     3360
  units with an X87 row                                      1405
  STACK rows in total                                        3408
  X87 rows in total                                          3090
```

GLOSS: 3,408 STACK rows over 3,360 units, 3,090 X87 rows over 1,405
units. Log 147 §4.1's census figures for the same two causes were
4,298 and 1,072 CENSUS ROWS — a different denominator (census rows are
per producer-instance in layer 4's transcription, ledger rows are per
value). Task 53 measures the census against canon38 and is the place
those two numbers meet; they are not reconciled here.

---

# 4. Ruling 4 — positional branch labels

## 4.1 What is rewritten, and what is not

- A transfer whose target is an instruction INSIDE this unit becomes
  `L0`, `L1`, … in ADDRESS ORDER, and the label is defined on the
  instruction it names. The target is located by reading the unit's
  OWN BYTES with capstone, so the mapping is forced by the bytes
  rather than guessed.
- A transfer OUT of the unit loses its address and its angle-bracket
  comment and keeps its CALLEE: `call 43f300 <runtime.panicshift>`
  becomes `call x_runtime_panicshift`. Stated as a departure from the
  literal words of the ruling ("the objdump symbol comment is
  dropped"): the callee's name is dropped from the comment and kept
  as the operand, because the ruling's purpose is that a unit's own
  name must not be in its own text, and `runtime.panicshift` is not
  this unit's name. Two units that call DIFFERENT routines must not
  become the same text.
- Nothing else on any line changes. `canon38_gate.check_six` (C6)
  verifies this per unit before the structural route is claimed.

## 4.2 The acceptance instance — `go/op_174` and `go/op_180`

LITERAL — `canon38_acceptance.txt`, part (d), canon37:

```
go/op_174 ... test %ebx,%ebx; jl 47a678 <main.op_174+0x18>; mov %ebx,%ecx; ...
go/op_180 ... test %ebx,%ebx; jl 47a678 <main.op_180+0x18>; mov %ebx,%ecx; ...
canon37 identical: False
```

LITERAL — the same two units, canon38, whole texts:

```
go/op_174
   mov ledger+0x00(%rip),%rax; mov 0x0(%rax),%rax; mov ledger+0x00(%rip),%rbx; mov 0x8(%rbx),%rbx; push %rbp; mov %rsp,%rbp; test %ebx,%ebx; jl L0; mov %ebx,%ecx; shl %cl,%rax; cmp $0x40,%ecx; sbb %rdx,%rdx; and %rdx,%rax; pop %rbp; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret; L0:; call x_runtime_panicshift; nop
go/op_180
   mov ledger+0x00(%rip),%rax; mov 0x0(%rax),%rax; mov ledger+0x00(%rip),%rbx; mov 0x8(%rbx),%rbx; push %rbp; mov %rsp,%rbp; test %ebx,%ebx; jl L0; mov %ebx,%ecx; shl %cl,%rax; cmp $0x40,%ecx; sbb %rdx,%rdx; and %rdx,%rax; pop %rbp; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret; L0:; call x_runtime_panicshift; nop
canon38 identical: True
```

GLOSS: the only text that differed between the two was
`main.op_174` against `main.op_180` inside the branch's symbol
comment. The single intra-unit target (byte offset 0x18) is the
lowest — and only — intra-unit target, so it is `L0` in both, and the
two layer-3 texts are now the same string. Log 148 §4.2.2's cause B
is closed.

## 4.3 The collapse, measured over the 30,436 texts

LITERAL — `canon38_zero_regression.txt`:

```
RULING 4 -- THE SYMBOL COMMENT IN THE STORED TEXT
  canon37: wrapped texts 30436, distinct 6277, carrying a symbol comment 4499
  canon38: wrapped texts 30436, distinct 2997, carrying a symbol comment 0
```

GLOSS: log 148 §4.2.2 measured 4,499 members carrying a symbolic
target and predicted 6,277 → about 2,999 distinct texts if the target
were blanked. The realised figure is **2,997**, two below the
prediction, because this form drops the ADDRESS as well as the
comment on out-of-unit transfers, which the prediction's blanking did
not. Zero stored texts carry an angle bracket.

## 4.4 The rewritten text is real machine code — assembled and read back

LITERAL — `canon38_assemble_go_op_174.txt`, the emitted `.s`, the
assembler's exit code, and `objdump -d` on the object file:

```
    .text
x_runtime_panicshift:
    ret
    .globl u_go_op_174
u_go_op_174:
    mov ledger+0x00(%rip),%rax
    ...
    jl .Lu_go_op_174_L0
    ...
    mov ledger+0x38(%rip),%r11
    mov %rax,0x0(%r11)
    ret
.Lu_go_op_174_L0:
    call x_runtime_panicshift
    nop

as --64 exit code: 0

0000000000000001 <u_go_op_174>:
   1:	48 8b 05 00 00 00 00 	mov    0x0(%rip),%rax        # 8 <u_go_op_174+0x7>
   8:	48 8b 00             	mov    (%rax),%rax
   b:	48 8b 1d 00 00 00 00 	mov    0x0(%rip),%rbx        # 12 <u_go_op_174+0x11>
  12:	48 8b 5b 08          	mov    0x8(%rbx),%rbx
  16:	55                   	push   %rbp
  17:	48 89 e5             	mov    %rsp,%rbp
  1a:	85 db                	test   %ebx,%ebx
  1c:	7c 1a                	jl     38 <u_go_op_174+0x37>
  1e:	89 d9                	mov    %ebx,%ecx
  20:	48 d3 e0             	shl    %cl,%rax
  23:	83 f9 40             	cmp    $0x40,%ecx
  26:	48 19 d2             	sbb    %rdx,%rdx
  29:	48 21 d0             	and    %rdx,%rax
```

LITERAL — `objdump -r` on the same object:

```
RELOCATION RECORDS FOR [.text]:
OFFSET           TYPE              VALUE
0000000000000004 R_X86_64_PC32     .data-0x0000000000000004
000000000000000e R_X86_64_PC32     .data-0x0000000000000004
0000000000000030 R_X86_64_PC32     .data+0x0000000000000034
```

GLOSS: the label `L0` assembled to a real relative branch (`7c 1a`);
the third relocation resolves to `.data + 0x34`, which is the OUT
block's entry at 0x38 less the four-byte addend — ruling 2's new block
order, in the encoding rather than in a claim.

## 4.5 The whole assembly lap

LITERAL — the run's own line, and canon37's for comparison:

```
canon38: offered 2728  assembled 2728  failed 0  ledger relocations 8946
canon37: offered 2728  assembled 2728  failed 0  ledger relocations 8946
```

GLOSS: the population is every proved unit of the original and
interpreter populations plus a stride-30 sample of the regenerated
one (`canon38_assemble.json` records `stride 30, sampled 956, of
28664`). Both laps offer and assemble the same 2,728, with the same
8,946 counted relocations against the ledger symbol.

---

# 5. What the repair made visible, named rather than smoothed

## 5.1 THE CALL'S RETURN VALUE HAS NO ROW — 305 units

LITERAL — computed this session over the 31,078 units of both laps:

```
newly phrase 305 of which body spells call: 305
canon37 producer for those: Counter({'push': 300, 'div': 5})
reverse: ['go/op_110']
sample newly-phrase unit: cpp/regen_11542
  push %rax; mov %edx,%edx; xor %ecx,%ecx; call a <op_11542+0xa> !!reloc=R_X86_64_PLT32:__udivti3-0x4; pop %rcx; ret
```

- The mechanism: these bodies compute nothing themselves. They set up
  arguments, `call` a library routine (`__udivti3`, `__divti3`), and
  return what the callee left in the accumulator. No opcode in the
  BODY writes the answer.
- canon37 claimed one anyway: for 300 of them the producer was `push`
  (ledger47's "destination = last named operand" rule, applied to
  `push %rax`), for 5 it was `div`.
- canon38 says `{"kind": "non_opcode_phrase", "phrase": "the body's
  last write to %rax"}` with no operands — the honest state.
- STATUS: open, and it is the natural successor to log 147 §4.1's
  five causes. The fix would be one more row in the destination
  table — a `call` writes the accumulator — but `call` is not in
  ruling 3's list and nothing unruled was added here.
- The count is a WITHDRAWAL OF A WRONG TERM, not a lost proof: all
  305 remain WRAPPED_TEXT_PROVED (§1.2's zero).

## 5.2 One unit moved the other way, and it is the repair working

LITERAL — `canon38_acceptance.txt`, part (b2), `go/op_110`:

```
  body   : push %rbp; mov %rsp,%rbp; test %rbx,%rbx; je 47a670 <main.op_110+0x10>; xor %edx,%edx; div %rbx; pop %rbp; ret; call 43f360 <runtime.panicdivide>; nop

canon37 (ledger47)
  IN-0     8    8-byte general value   arrival
  TEMP-0   8    8-byte general value   test                   IN-0,IN-0
  GUARD-0  8    flag-derived value     ['test', 'je']
  TEMP-1   8    8-byte general value   xor
  TEMP-2   8    8-byte general value   div                    TEMP-0
  OUT-0    4    4-byte general value   the body's last write to %rax

canon38 (ledger48)
  stored : push %rbp; mov %rsp,%rbp; test %rbx,%rbx; je L0; xor %edx,%edx; div %rbx; pop %rbp; ret; L0:; call x_runtime_panicdivide; nop
  IN-0     8    8-byte general value              {"kind": "non_opcode_phrase", "phrase": "arrival"}
  STACK-0  8    8-byte value on the machine stack {"kind": "arch_opcode", "mnem": "push"}
  TEMP-0   8    flags only                        {"kind": "arch_opcode", "mnem": "test"}   IN-0,IN-0
  GUARD-0  8    flag-derived value                {"kind": "flag_pair", "mnem": ["test", "je"]}   TEMP-0
  TEMP-1   8    8-byte general value              {"kind": "arch_opcode", "mnem": "xor"}
  TEMP-2   8    8-byte general value              {"kind": "arch_opcode", "mnem": "div", "writes_which_half": "quotient"}   TEMP-1,IN-0
  TEMP-3   8    8-byte general value              {"kind": "arch_opcode", "mnem": "div", "writes_which_half": "remainder"}  TEMP-1,IN-0
  OUT-0    4    4-byte general value              {"kind": "arch_opcode", "mnem": "div", "writes_which_half": "quotient"}   TEMP-2
```

GLOSS: all four rulings are in this one unit. canon37 had NO producer
for the answer (`div` wrote a row attached to the divisor, so the
accumulator pointed at nothing). canon38's table gives `div` two rows
and the answer reads the quotient half; `push %rbp` gets a STACK row;
`test` is typed `flags only` and feeds the guard row; the branch is
`je L0` with `L0:` defined; and the out-of-unit transfer is
`call x_runtime_panicdivide`.

## 5.3 The answer row's producer, before and after, over 31,078 units

LITERAL — `canon38_zero_regression.txt`:

```
THE ANSWER ROW'S PRODUCER, by kind
  canon37: {"bare string": 20713, "flag_pair": 9723}
  canon38: {"arch_opcode": 20093, "flag_pair": 9723, "non_opcode_phrase": 620}
```

GLOSS: 20,713 = 20,093 + 620, so the split is not a loss of records —
it is the typing of ruling 5 plus the 305 moves of §5.1 (316 answer
rows already carried a phrase in canon37; 316 + 305 − 1 = 620). The
642 units with no ledger at all are the refusals of §1.3.

---

# 6. Ruling 5 — the guard, unmodified, one process

## 6.1 The producer is a typed object everywhere

LITERAL — `ledger48.producer_object`'s kinds, and one row of each
shape from `canon38_wrapped_c.json` / `canon38_regen_store/`:

```
{"kind": "non_opcode_phrase", "phrase": "arrival"}
{"kind": "arch_opcode", "mnem": "mov"}
{"kind": "arch_opcode", "mnem": "idiv", "writes_which_half": "quotient"}
{"kind": "flag_pair", "mnem": ["fucomip", "seta"]}
```

GLOSS: `mnem` is the field `check_no_spelling_keys.py` already carries
in `PROSE_FIELDS` beside `bytes`, `key` and `sem_key` — this
codebase's ratified machine-form field. `kind` is drawn from a fixed
vocabulary (`arch_opcode`, `flag_pair`, `non_opcode_phrase`) that
contains no operator token. This is log 147 §13.3's shape, reused, not
reinvented.

## 6.2 No canon38 artifact declares a role

LITERAL — command and output:

```
$ grep -l '"role"' canon38_*.json canon38_regen_store/*.json | wc -l
0
```

## 6.3 THE AFTER — every canon38 file, one process, no exemption

LITERAL — `canon38_guard_transcript.txt`, its head, its tail, and the
counts computed over it:

```
canon38_guard.py -- THE AFTER: every canon38 artifact, unmodified guard, ONE process. No file declares the provenance role and nothing was added to any field set.
$ python3 check_no_spelling_keys.py <336 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon38_wrapped_c.json -- no operator token in any key, grouping, pairing or row structure
PASS canon38_wrapped_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS canon38_wrapped_go.json -- no operator token in any key, grouping, pairing or row structure
PASS canon38_wrapped_rust.json -- no operator token in any key, grouping, pairing or row structure
...
PASS op_units2_swift_c0010.json -- no operator token in any key, grouping, pairing or row structure

GUARD EXIT CODE = 0
```

```
$ grep -c "^PASS " canon38_guard_transcript.txt
336
$ grep -c "^FAIL"  canon38_guard_transcript.txt
0
$ grep -c exempt   canon38_guard_transcript.txt
0
```

GLOSS: 336 files — the five wrapped artifacts, the interpreter
artifact, the regen state, the zero-regression report, the assemble
report, the guard's own summary, and all 326 regen chunks. Every line
says the guard WALKED the file. Nothing was added to any field set:
`canon38_guard.py` runs `check_no_spelling_keys.py` as a separate
process with `sys.executable` and touches no guard module.

## 6.4 THE BEFORE — canon37 with the role line removed

LITERAL — `canon38_guard_canon37_norole_transcript.txt`, head and the
first failure:

```
canon38_guard.py -- THE BEFORE: task 47's own canon37 artifacts, copied with the one `role` line removed and nothing else changed, walked by the same unmodified guard.  The canon37 files on disk are untouched.
$ python3 check_no_spelling_keys.py <332 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
FAIL canon37_wrapped_c.json -- 579 spelling-keyed place(s)
     $.units.c/op_0.ledger[1].produced_by
         operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
     $.units.c/op_1.ledger[1].produced_by
         operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
     $.units.c/op_11.ledger[2].produced_by
         operator token 'not' on a structure field -- this is a grouping/row key, not a per-unit label

GUARD EXIT CODE = 1
```

LITERAL — the run's summary line:

```
BEFORE : 332 paths  PASS 59  FAIL 273  exempt 0  exit 1  (role removed from 332 copies)
```

GLOSS: **579** in `canon37_wrapped_c.json` — the exact figure log 150
§3.1 predicted. 273 of the 332 canon37 artifacts fail once the role
line is gone; 59 pass, and all 59 are regenerated CHUNK files whose bodies happen
to spell no mnemonic that collides with an operator token (verified:
`grep -c "^PASS"` = 59, every one an `op_units2_*.json`). Against canon38's 336
PASS / 0 FAIL, this is the before beside the after.

LITERAL — the canon37 files on disk were not modified; only copies in
`/tmp/canon38_guard_scratch` were read:

```
$ ls -l --time-style=+%Y-%m-%dT%H:%M canon37_wrapped_c.json canon37_interp.json
2026-09-02T19:59 canon37_interp.json
2026-09-02T19:59 canon37_wrapped_c.json
```

GLOSS: 19:59 is task 47's own write time, hours before this session.

---

# 7. The complete file inventory

## 7.1 Code written this task (nine files, all new; `ledger47.py` was not edited)

| file | what it is |
|---|---|
| `ledger48.py` | THE FORM. Imports 20 names from `ledger47.py` unchanged; replaces the block order, the dataflow walk, the flag-reader pattern and the branch-target spelling. |
| `canon38_gate.py` | the gate. Imports `canon37_gate.py` unchanged, widens the row test to eight blocks, and adds structural check C6 for the branch-label rewrite. |
| `canon38_wrapped.py` | the original population's driver (1,779). |
| `canon38_interp.py` | the interpreter population's driver (11). |
| `canon38_regen.py` | the regenerated population's driver (29,288), per-chunk checkpointing. |
| `canon38_assemble.py` | `as --64` + `objdump -d` + `objdump -r` over the proved texts. |
| `canon38_acceptance.py` | the six acceptance instances (a, b, b2, c, d, e). |
| `canon38_zero_regression.py` | canon38 against canon37, unit by unit, computed. |
| `canon38_guard.py` | runs the UNMODIFIED guard, one process, twice: after and before. |

## 7.2 Data written this task

| file | what it is |
|---|---|
| `canon38_wrapped_c.json` (5,012,800 bytes) | 610 units |
| `canon38_wrapped_cpp.json` (6,654,207) | 770 units |
| `canon38_wrapped_go.json` (863,856) | 107 units |
| `canon38_wrapped_rust.json` (825,388) | 125 units |
| `canon38_wrapped_swift.json` (1,218,438) | 167 units |
| `canon38_interp.json` (56,122) | 11 units |
| `canon38_regen_store/*.json` | 326 chunks, 29,288 units |
| `canon38_regen_state.json` (33,283) | the resume state: 326 of 326 chunks done |
| `canon38_assemble.json` (539,916) | 2,728 offered / 2,728 assembled / 0 failed |
| `canon38_zero_regression.json` (2,243) | the comparison, as data |
| `canon38_guard.json` (552) | the two guard runs' counts |

## 7.3 Transcripts and logs written this task

| file | what it is |
|---|---|
| `canon38_guard_transcript.txt` (32,991) | THE AFTER: 336 PASS, 0 FAIL, 0 exempt, exit 0 |
| `canon38_guard_canon37_norole_transcript.txt` (702,970) | THE BEFORE: 273 FAIL, 579 places in the c file, exit 1 |
| `canon38_assemble_transcripts.txt` (2,983) | six sampled `objdump -d` blocks, verbatim |
| `canon38_assemble_go_op_174.txt` (2,776) | the one-off: the `.s`, the exit code, `objdump -d`, `objdump -r` for the positional-label instance |
| `canon38_acceptance.txt` (10,515) | the six acceptance instances, printed |
| `canon38_zero_regression.txt` (2,341) | the comparison, printed |
| `canon38_wrapped_run.log` (1,323) | the original population's run |
| `canon38_regen_run.log` (21,021) | the regenerated population's run, chunk by chunk |

## 7.4 Scratch, outside the repository (named, not banked)

`/tmp/canon38_assemble_work` (the batch `.s` and `.o` files),
`/tmp/canon38_guard_scratch` (the canon37 copies with the role line
removed), `/tmp/canon38_one` (the `go/op_174` one-off).

---

# 8. Resume state

## 8.1 Nothing is part-done

LITERAL — `canon38_regen.py --status`:

```
chunks 326 of 326 done, 29288 units, {"REFUSED": 624, "WRAPPED_TEXT_PROVED": 28664}
```

GLOSS: the regenerated population finished in-session; the brief's
contingency ("if the regenerated population cannot finish in-session,
leave clean resume state") did not arise. The state file
`canon38_regen_state.json` records every chunk as done with its tally,
so a re-run is a no-op and a `--fresh` re-run is a full redo.

## 8.2 How to resume anyway, if a later lap wants to

- `canon38_wrapped.py --all` skips units already in the artifact;
  `--fresh` starts over. `--lang c --limit N` does one language.
- `canon38_regen.py --run [--chunks N] [--seconds S]` skips chunks
  already marked done in `canon38_regen_state.json`.
- `canon38_interp.py` takes no arguments and rewrites its one file.
- The three read-only steps (`canon38_assemble.py`,
  `canon38_acceptance.py`, `canon38_zero_regression.py`) and then
  `canon38_guard.py` are re-runnable in that order at any time;
  `canon38_guard.py` must be run LAST because it walks
  `canon38_assemble.json` and its own previous summary.

## 8.3 What task 53 reads

`canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`
and `canon38_regen_store/*.json`. Its intake must read the producer's
`.mnem` / `.phrase` off the typed object, never the field as a string,
and it should expect two new blocks in `ledger[*].block` (`STACK`,
`X87`), a new row type (`flags only`), and a new row field
(`written_half`) on rows the destination table made.

---

# 9. Decided and recorded for audit / awaiting the owner

## 9.1 Decided, recorded (no answer needed)

1. An out-of-unit transfer keeps its callee as the operand
   (`call x_runtime_panicshift`) rather than losing it. Reason in
   §4.1: the ruling's purpose is that a unit's own name must not sit
   in its own text, and two units calling different routines must not
   collapse into one text. The address and the angle brackets are
   dropped.
2. A comparison row is kept in the TEMP block, typed `flags only`, and
   is carried as the first operand of the next flag-reading row. The
   ruling required the TYPE; the operand link is this file's own
   choice, and it is what lets task 53 close log 147 §4.1's fifth
   cause ("the flags the setter left are not in the ledger").
3. `canon38_gate.py` adds structural check C6 rather than reusing
   canon37's "character-for-character" claim, which ruling 4 makes
   false as written. `canon37_gate.py` is not edited.

## 9.2 Awaiting the owner (one item, not blocking task 53)

1. **Should `call` join the destination table?** §5.1: 305 units'
   answers are produced by a library routine the ledger cannot see.
   Adding "a `call` writes the accumulator" would give those units an
   answer row again — honestly this time, naming the callee — but
   `call` is not in ruling 3's list, and nothing unruled was added.
   Your call.
\n\n## CORRECTION (2026-09-03, coordinator) — the "call as a producer" open call is WITHDRAWN\n\nThe 300 units whose answer comes from `call __udivti3` / `__umodti3` / `__divti3` / `__modti3` are LIBRARY ROUTINES, not compiler operations. By the standing ruling (AgentMemory line 135: layer 3 is "what the COMPILER can do to a representation — the measured dynamics, never builtins") they are OUT OF SCOPE. They should never have been posed as a question for the owner, and the phrase "library-call units" should not have been coined. Recorded as excluded in `Research/op_pipeline/out_of_scope_library_calls.json`; the next pool/proof rebuild drops them from its population. Nothing in this log's earlier text is edited.\n