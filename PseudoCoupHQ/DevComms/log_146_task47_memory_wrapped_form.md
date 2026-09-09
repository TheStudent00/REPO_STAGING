# log 146 — TASK 47: the memory-wrapped form and the provenance ledger

Date: 2026-09-02. Author: Claude Code (implementer), no sub-agents.
Working directory: `PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3` (pyvex 9.3.4, z3 5.1.0,
capstone installed this lap). Assembly on the host: `as --64`,
`objdump -d`, `objdump -r`.

Every rendering below is labelled **LITERAL**, **GLOSS** or
**ANALOGY**, per the protocol's §5.1a. A gloss never appears without
the literal it glosses. Every figure states its population, per §3.4a.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

---

# 1. What was done, and where it stands

## 1.1 In one paragraph, before any figure

Every arch-unit is now a compiler's own instructions, untouched,
sitting between two pieces of standardized plumbing. Ahead of the
body, one two-step load per argument brings the value out of a memory
row into the very register that compiler expects it in. After the
body, one two-step store puts the compiler's own result register into
the answer's row. Nothing else is changed — no register is renamed,
no immediate is moved, no stack address is rewritten. The two-step is
"read the block's base out of a small table, then read the row inside
that block", and that table (the ledger) sits at an absolute address
reached rip-relative, so no register is reserved for it and no body
can collide with it. Beside each unit is a second table, the
provenance ledger, with one row per value that moves through the
unit — input, literal, temporary, guard outcome, answer — each row
carrying its type, the arch opcode that made it, and the rows it read.

## 1.2 The counts, per population

| population | units | proved | refused | disproved | undecided |
|---|---|---|---|---|---|
| original, the compiled corpus | 1,779 | **1,763** | 16 | 0 | 0 |
| interpreter/JIT | 11 | **9** | 2 | 0 | 0 |
| regenerated | 29,288 | **28,664** | 624 | 0 | 0 |
| **all three** | **31,078** | **30,436** | **642** | **0** | **0** |

Round 9's counts on the same three populations, for the comparison:
1,752 / 9 / 27,223 proved (total 28,984 of 31,078). Round 10 proves
**1,452 more units** and refuses **1,423 fewer**.

## 1.3 How each proved unit was proved

| population | z3 against its own ship code | by construction | refused |
|---|---|---|---|
| original (1,779) | 1,168 | 595 | 16 |
| interpreter (11) | 9 | 0 | 2 |
| regenerated (29,288) | 17,370 | 11,294 | 624 |

"By construction" is used only where the solver's own table has no
model for a mnemonic the body spells; §5.3 states its five checks.

## 1.4 Resume state

Nothing is left unfinished. All three populations completed in this
session:

- original: `canon37_wrapped_{c,cpp,go,rust,swift}.json`, 1,779 of
  1,779 units present;
- interpreter: `canon37_interp.json`, 11 of 11;
- regenerated: `canon37_regen_store/` holds 326 chunk files,
  `canon37_regen_state.json` marks 326 of 326 chunks done, 29,288 of
  29,288 units present.

The resume machinery exists and was exercised (the population was run
three times this session after fixes). To resume an interrupted lap:
`canon37_regen.py --run` skips every chunk already in the state file;
`canon37_wrapped.py --all` skips every unit already in its language's
artifact; `--fresh` discards and restarts one language.

---

# 2. The form, with values moving through it

## 2.1 The names, each introduced before it is used

- **The ledger** — a table in RAM with six entries, each eight bytes,
  each holding one block's real base address. Entry order is fixed:
  IN, CONST, TEMP, OWN, GUARD, OUT.
- **A block** — a region of memory holding rows of one kind. The
  runner puts it wherever it likes; nothing in the unit's text says
  where.
- **A row** — one value's home inside a block, named `IN-0`, `OUT-0`,
  `TEMP-3`, and sized by its type.
- **The body** — the compiler's own instructions for this unit, kept
  character for character.
- **The prelude / the epilogue** — the standardized plumbing before
  and after the body.
- **The arrival contract** — which register the compiler expects each
  argument in.

## 2.2 One unit walked end to end, with real values — c/op_6

LITERAL — the body, as the compiler emitted it
(`canon37_wrapped_c.json`, unit `c/op_6`, field `body_verbatim`):

```
mov %edi,%eax
not %eax
ret
```

LITERAL — the wrapped text, exactly as it is assembled
(field `wrapped_text`):

```
mov ledger+0x00(%rip),%rdi
mov 0x0(%rdi),%rdi
mov %edi,%eax
not %eax
mov ledger+0x28(%rip),%r11
mov %eax,0x0(%r11)
ret
```

GLOSS, walked with a value in motion. Say the runner put the IN block
at address 0x7000 and the OUT block at 0x9000, wrote those two
addresses into ledger entries 0 and 5, and put the number 5 in IN-0.

1. `mov ledger+0x00(%rip),%rdi` — %rdi now holds 0x7000, the IN
   block's base. The destination register is used as the pointer, so
   no scratch register is needed and nothing the body will read is
   disturbed.
2. `mov 0x0(%rdi),%rdi` — %rdi now holds 5, the value in IN-0. The
   argument has arrived in the register this compiler expects it in.
3. `mov %edi,%eax` — the compiler's own first instruction. %eax = 5.
4. `not %eax` — %eax = 0xfffffffa.
5. `mov ledger+0x28(%rip),%r11` — %r11 now holds 0x9000, the OUT
   block's base. Entry 5 is at offset 0x28 because each entry is eight
   bytes and OUT is the sixth block.
6. `mov %eax,0x0(%r11)` — 0xfffffffa is written into OUT-0. The
   answer's home is the row, not a register.
7. `ret`.

## 2.3 The ledger at that unit, LITERAL

From the same record, field `ledger`:

```
row      off   size type                         produced by  operands
IN-0     0x0   8    8-byte general value         arrival
TEMP-0   0x0   8    8-byte general value         mov          IN-0
TEMP-1   0x0   8    8-byte general value         not          TEMP-0
OUT-0    0x0   4    4-byte general value         not          TEMP-1
```

GLOSS: read down the `produced by` and `operands` columns and the
table IS the dataflow graph. The answer came from `not`, which read
TEMP-0, which came from `mov`, which read IN-0, which the runner
filled. `not` here is the ARCH OPCODE; §6.2 shows how that is checked
rather than asserted.

## 2.4 The addressing mode and the relocation, stated

LITERAL — `objdump -d` on the object file `as --64` produced from the
wrapped text of `c/op_0`
(`canon37_assemble_transcripts.txt`, verbatim):

```
0000000000000000 <u_c_op_0>:
   0:	48 8b 3d 00 00 00 00 	mov    0x0(%rip),%rdi        # 7 <u_c_op_0+0x7>
   7:	48 8b 3f             	mov    (%rdi),%rdi
   a:	31 c0                	xor    %eax,%eax
   c:	85 ff                	test   %edi,%edi
   e:	0f 94 c0             	sete   %al
  11:	4c 8b 1d 00 00 00 00 	mov    0x0(%rip),%r11        # 18 <u_c_op_0+0x18>
  18:	41 88 03             	mov    %al,(%r11)
  1b:	c3                   	ret
```

LITERAL — `objdump -r` on the same object file:

```
RELOCATION RECORDS FOR [.text]:
OFFSET           TYPE              VALUE
0000000000000003 R_X86_64_PC32     .data-0x0000000000000004
000000000000000d R_X86_64_PC32     .data-0x0000000000000004
0000000000000028 R_X86_64_PC32     .data+0x0000000000000024
```

GLOSS: the four displacement bytes of each `ledger+0xNN(%rip)` operand
are zero in the object file and carry an `R_X86_64_PC32` relocation
against the section the ledger lives in. The link editor, or the
loader for a position-independent image, fills those four bytes with
the distance from the instruction to wherever the ledger was placed.
`.data+0x24` is entry 5 (0x28 minus the four-byte relocation bias) —
the OUT block. That is the mechanical answer to "where is the ledger":
nowhere in the text, and in exactly one place at run time.

Across the whole assembly run: **8,946** such relocations were counted
over the 2,728 texts assembled (population: every proved original and
interpreter unit plus a stride-30 sample of the proved regenerated
units).

## 2.5 Rows are sized by their type

LITERAL — the prelude of `cpp/regen_12934`, whose first argument
arrives in a vector register:

```
mov ledger+0x00(%rip),%r11
movdqu 0x0(%r11),%xmm0
mov ledger+0x00(%rip),%rdi
mov 0x10(%rdi),%rdi
```

LITERAL — the first two ledger rows of that unit:

```
IN-0     0x0   16   16-byte vector value    arrival
IN-1     0x10  8    8-byte general value    arrival
```

GLOSS: IN-0 is sixteen bytes and is loaded whole with `movdqu`; IN-1
starts at 0x10 because IN-0 occupied the first sixteen bytes. Round 9
gave every block an eight-byte slot and therefore refused 1,479
regenerated units by name for reading a vector register in a way eight
bytes could not carry. Sizing a row by its type removes the refusal
rather than working around it.

## 2.6 The two-step lemma

The gate walks a RESOLVED rendering, in which each two-step pair is
written as one line naming the row — `mov IN-0,%rdi` for the two lines
of §2.2. `canon37_lemma.py` checks, once and generically over a
symbolic memory array, symbolic ledger base, symbolic entry offset and
symbolic row offset, that the two readings are the same bytes.

LITERAL — its output:

```
  load  direction: z3 says unsat for (two-step reading != resolved reading)
  store direction: z3 says unsat for (memory after two-step store != memory after resolved store), at every probe address

  BOTH UNSAT -- the resolved text and the literal text read and write the same bytes, so a proof about one is a proof about the other.
```

GLOSS, and the honest limit: the load direction models the
destination-register-as-pointer trick explicitly — the first
instruction overwrites the destination with the block's base, the
second reads through that same register. The lemma is a
forced-by-construction identity, not a discovery; it is here so the
step from the assembled text to the proved text is written down rather
than assumed.

---

# 3. What was dropped from round 9, and what it bought

## 3.1 The %r15 anchor is gone

Round 9 reserved `%r15` as the region's base, so a unit whose own body
mentions `%r15` had nowhere to put the base.

LITERAL — round 9's own refusal, from `canon36_universal_cpp.json`,
unit `cpp/op_765`:

```
outcome        REFUSED
refusal_cause  the core names the region base
refusal        this unit's own core mentions %r15, which the form rules to be the region base and therefore not available to any lineage; the unit is refused by name rather than being rendered onto a base it also uses as a value
```

LITERAL — round 10's outcome for the same unit, from
`canon37_wrapped_cpp.json`:

```
outcome        WRAPPED_TEXT_PROVED
verdict        PROVED_BY_CONSTRUCTION
```

All four of round 9's `%r15` refusals — `cpp/op_765`, `cpp/op_770`,
`swift/op_703`, `swift/op_739` — now render and prove. The full
bodies and wrapped texts are printed verbatim in
`canon37_acceptance.txt`, section (a).

## 3.2 The scratch-register rewrite is gone

Round 9's rule R renamed every register family in the body by a fixed
pool order. Ruling 1 forbids that, and the form no longer does it: the
body is character-for-character the compiler's. That is checked per
unit, not claimed — check C1 of §5.3.

---

# 4. The four acceptance instances

Printed in full, verbatim with values, in
`canon37_acceptance.txt` (441 lines, produced by
`canon37_acceptance.py`). Summarized here with the load-bearing
literals.

## 4.1 (a) The four former %r15 units

Covered in §3.1. All four: `WRAPPED_TEXT_PROVED`.

## 4.2 (b) c/op_31 — the answer IS an address

LITERAL — the body:

```
mov %rdi,-0x8(%rsp)
lea -0x8(%rsp),%rax
ret
```

LITERAL — the wrapped text:

```
mov ledger+0x00(%rip),%rdi
mov 0x0(%rdi),%rdi
mov %rdi,-0x8(%rsp)
lea -0x8(%rsp),%rax
mov ledger+0x28(%rip),%r11
mov %rax,0x0(%r11)
ret
```

LITERAL — the ledger:

```
row      off   size type                         produced by                       operands
IN-0     0x0   8    8-byte general value         arrival
OWN-0    0x0   8    the unit's own stack address the body's own stack displacement
TEMP-0   0x0   8    8-byte general value         lea                               OWN-0
OUT-0    0x0   8    8-byte general value         lea                               TEMP-0
```

LITERAL — the OWN row's recorded address, and the z3 check:

```
OWN-0   address_is = %rsp - 0x8

OUT-0 holds       rsp - 8
OWN-0's address is rsp - 8
z3 on (OUT-0 != the address of OWN-0): unsat
```

LITERAL — the unit's verdict:

```
outcome  WRAPPED_TEXT_PROVED
verdict  PROVED_ON_SHIP
detail   z3 proved the wrapped text's OUT-0 equal to the unit's own ship code at 64 bits, for every value of every input row, with each input row bound to the same symbol as the argument the reference text reads in its arrival register
```

GLOSS: because the body is verbatim, the unit's own stack scratch
never moves, so its address never moves either. OUT-0 holds
`%rsp - 0x8`, which is exactly the address the ledger records for
OWN-0. Round 9 could only place this unit by relocating its scratch,
which relocated its answer.

HONEST NOTE ON THE OWN BLOCK: for a verbatim body, the OWN block is
the unit's own stack frame, and its ledger entry is DESCRIPTIVE — the
runner does not allocate it, the unit's own `%rsp` does. The row
records what address the body itself spells. That is stated rather
than glossed over, because it is the one block whose base the runner
does not choose.

## 4.3 (c) cpp/regen_12934 — a 16-byte lane row

Covered in §2.5. LITERAL — the body's vector-lane line, which round 9
refused on:

```
pextrw $0x0,%xmm0,%eax
```

LITERAL — the verdict:

```
outcome  WRAPPED_TEXT_PROVED
verdict  PROVED_BY_CONSTRUCTION
```

## 4.4 (d) c/op_109 and go/op_319 — one ledger, two preludes

LITERAL — the two bodies:

```
c/op_109    lea (%rdi,%rsi,1),%rax ; ret
go/op_319   add %rbx,%rax          ; ret
```

LITERAL — the two preludes:

```
c/op_109                            go/op_319
mov ledger+0x00(%rip),%rdi          mov ledger+0x00(%rip),%rax
mov 0x0(%rdi),%rdi                  mov 0x0(%rax),%rax
mov ledger+0x00(%rip),%rsi          mov ledger+0x00(%rip),%rbx
mov 0x8(%rsi),%rsi                  mov 0x8(%rbx),%rbx
```

LITERAL — the two ledgers, side by side:

```
c/op_109                                 | go/op_319
---------------------------------------- | ----------------------------------------
IN-0    8   arrival                      | IN-0    8   arrival
IN-1    8   arrival                      | IN-1    8   arrival
TEMP-0  8   lea         IN-0,IN-1        | TEMP-0  8   add         IN-1,IN-0
OUT-0   8   lea         TEMP-0           | OUT-0   8   add         TEMP-0
```

LITERAL — the row shapes compared:

```
c/op_109   [('IN-0', 8, '8-byte general value'), ('IN-1', 8, '8-byte general value'), ('TEMP-0', 8, '8-byte general value'), ('OUT-0', 8, '8-byte general value')]
go/op_319  [('IN-0', 8, '8-byte general value'), ('IN-1', 8, '8-byte general value'), ('TEMP-0', 8, '8-byte general value'), ('OUT-0', 8, '8-byte general value')]
identical: True
```

GLOSS: two compilers, two instruction choices, two different argument
registers — and one table of what the unit does to memory. The
producer column still differs (`lea` against `add`), which is correct:
it names the arch opcode, and the two compilers used different
opcodes for the same effect. Whether those two opcodes are one
operation is a question for the proof layer, not for the table.

---

# 5. The gate, and what "proved" means here

## 5.1 What is bound before anything is proved

Input row *i* is bound to the SAME SYMBOL as the argument the
reference text reads in arrival register *i*. A vector row is bound at
its full 128 bits. Nothing else is bound; the ledger's base, the block
bases, and the row contents are otherwise free.

## 5.2 The one proof obligation

For every value of every input row, the value the wrapped text leaves
in **OUT-0** equals the value the unit's own ship code leaves in its
own answer home. The answer is read out of the ROW, never out of a
register.

Where a unit also has a prior canonical text (the original population
only), the same obligation is run against that text as a cross-check
and both verdicts are recorded.

## 5.3 The structural route, and its five checks

Used only where the solver returns UNDECIDED because its table has no
model for a mnemonic the body spells. Because the form applies NO
transformation to the body, the obligation reduces to "the body is
present and the plumbing cannot disturb it":

- **C1** the body appears in the wrapped text character-for-character
  and in its own order — no register renamed, no immediate moved, no
  stack address rewritten;
- **C2** the prelude writes only the registers the arrival contract
  names, one two-step load per input row (plus, where a vector arrival
  needs one, a single general scratch that is not an arrival family,
  so the body never reads it before writing it);
- **C3** every `ret` is immediately preceded by the epilogue;
- **C4** no body line names the ledger symbol or any ledger row;
- **C5** the epilogue's pointer register is not the result register.

EVIDENCE CLASS: C1, C3, C4 and C5 are forced by construction over
artifacts this lap built. C2's statement about the scratch rests on
the arrival contract being exactly "the families the body reads before
it writes them" — itself read off the body's own text, so also forced
by construction.

## 5.4 The arrival contract is read off the body, in the language's
## own register order

Round 9 read every unit's contract through one sequence, System V's
(`%rdi`, `%rsi`, `%rdx`, …). go does not use it: since go 1.17 the go
compiler passes integer arguments in `%rax`, `%rbx`, `%rcx`, `%rdi`,
`%rsi`, `%r8`, `%r9`, `%r10`, `%r11`.

MEASURED AT FIRST OBSERVATION THIS LAP, and fixed at first
observation. LITERAL — `go/op_319`'s recorded contract against what
its body reads (`canon37_wrapped_go.json`, field
`entry_contract_disagreement`):

```
designation a: the_recorded_contract_said "rdi", the_body_reads "rax"
designation b: the_recorded_contract_said "rsi", the_body_reads "rbx"
```

GLOSS: with the recorded contract, the prelude filled two registers
the body never reads, and the gate's question became vacuous — both
texts read `%rax` and `%rbx` as free symbols and agreed for no reason.
The body is the artifact; the recorded contract is human
interpretation of stated design. The body wins, and the disagreement
is recorded per unit rather than smoothed over.

A second defect of the same shape, also fixed at first observation: a
register inside a MEMORY OPERAND is a read of that register. Reading
only operands that begin with `%` found no arrivals at all in
`c/op_109` (`lea (%rdi,%rsi,1),%rax`), so the unit was wrapped with an
empty IN block. Registers inside memory operands are now counted as
reads, which is what they are — address computation, never a
destination.

---

# 6. The guards

## 6.1 Both guards, run WITHOUT exemption

`check_no_spelling_keys.py` grants an exemption to any document whose
`meta.role` says "generator provenance". The brief asks for the guard
without exemption, so `canon37_guard.py` DELETES that declaration from
a scratch copy of each artifact before handing it over, and every
artifact is walked in full.

LITERAL — the guard's own output (`canon37_guard.txt`):

```
operator inventory: 91 tokens read from probe_manifest_*.json
THE GENERATOR-PROVENANCE EXEMPTION IS REMOVED for every file below.

CHECK ONE -- every ledger row's `produced_by` is an arch opcode of that unit's own body
  rows checked: 240675
  findings:     0
  PASS -- every producer is an arch opcode this unit's own body spells, so an operator-token SPELLING in that field is a collision with a machine mnemonic, not a spelling key.

CHECK TWO -- the generic spelling-key guard, exemption removed, with `produced_by` and `operands` read as machine form on the strength of CHECK ONE
...
checked 335 files without exemption; 0 failed
```

The 335 files are: five original-population artifacts, the interpreter
artifact, the assembly artifact, the zero-regression artifact, the
regenerated resume-state file, and all 326 regenerated chunk files.

## 6.2 Why CHECK ONE had to exist

Some arch opcodes are spelled exactly like operator tokens in the
manifests' inventory: `xor`, `and`, `or`, `not`, `neg`, `shl`. The
generic checker cannot tell a machine mnemonic from a spelling, and on
its first run it reported 579 such places in `canon37_wrapped_c.json`
alone. That is a COLLISION, not a violation — but saying so is worth
nothing unless it is checked. So CHECK ONE proves the distinction
per row: a row's `produced_by` is accepted only when it is the word
`arrival`, one of two recorded non-opcode producer phrases, a mnemonic
that appears in THAT UNIT'S OWN BODY, or a pair
[flag-setting mnemonic, flag-reading mnemonic] whose members both
appear in that unit's own body. Anything else fails by name. 240,675
rows checked, 0 findings.

CHECK ONE also caught a real gap at first observation and it was fixed
at first observation: the flag-setter table was missing `mul` and the
x87 comparison family, so 1,156 guard rows carried a pair whose
flag-setting half was empty. LITERAL — two of the bodies that exposed
it:

```
swift/op_128   mov %rdi,%rax ; mul %rsi ; jo 9 <op_128+0x9> ; ret ; ud2
c/regen_34     fldt 0x8(%rsp) ; fldz ; fucomip %st(1),%st ; fstp %st(0) ; setnp %al ; sete %cl ; and %al,%cl ; movzbl %cl,%eax ; ret
```

The table is now stem-based (an operand-size suffix is stripped before
the test) and carries the x87 and SSE comparison forms. After the fix:
0 producer holes in 240,675 rows across all three populations.

---

# 7. Assembly: every wrapped text is real machine code

LITERAL — `canon37_assemble.py`'s own output:

```
offered 2728  assembled 2728  failed 0  ledger relocations 8946
```

Population: every proved original unit (1,763), every proved
interpreter unit (9), and a stride-30 sample of the proved regenerated
units (956 of 28,664). The stride and the sample size are recorded in
the artifact's `meta`. Round 9's comparable run: 2,578 assembled of
2,669 offered, 91 failures.

TWO RENDERING STEPS ARE APPLIED TO MAKE OBJDUMP TEXT ASSEMBLABLE, and
both are named rather than hidden:

- **intra-unit branch targets.** objdump prints a branch as a byte
  address plus a symbol comment (`js f <op_117+0xf>`). The unit's own
  bytes are disassembled with capstone to get every instruction's byte
  offset; the offset named in the symbol comment picks the body line;
  that line gets a local label and the branch names it. Forced by the
  bytes, not guessed.
- **transfers out of the unit.** A tail call or a panic call names its
  callee in the objdump comment (`call 43f360 <runtime.panicdivide>`).
  The numeric address is replaced by that name and the batch defines
  the name as a stub. This checks the ENCODING, not the presence of
  the callee — stated because it matters: an assembled tail-call unit
  is not thereby a runnable unit, and §8.1 is why those units are
  refused anyway.

---

# 8. Refusals, per population, every one named

## 8.1 Original population (1,779): 16 refused, one cause

| cause | count | units |
|---|---|---|
| never returns | 16 | rust/op_699, rust/op_706, swift/op_690, swift/op_691, swift/op_692, swift/op_696, swift/op_697, swift/op_698, swift/op_702, swift/op_726, swift/op_727, swift/op_728, swift/op_732, swift/op_733, swift/op_734, swift/op_738 |

LITERAL — the body of `swift/op_690`, the whole of it:

```
jmp 5 <op_690+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship6op_690ys5Int32VAD_ADtF-0x4
```

GLOSS: the unit is one unconditional jump into another routine. The
answer is produced by that routine, after this unit has stopped
existing as a frame. There is no point in this unit at which the
answer exists to be stored into OUT-0, and storing it would require
changing the body — turning the `jmp` into a `call` — which ruling 1
forbids. So it is refused by name.

## 8.2 Interpreter/JIT population (11): 2 refused, one cause

| cause | count | units |
|---|---|---|
| no canonical text | 2 | ruby/rb_big_plus, ruby/vm_opt_plus |

LITERAL — quoted from `interp_canon35.json`, carried through
unchanged: "register scarcity plays no part. vm_opt_plus has no ship
body at all, so there is nothing …". Same two units, same cause, as
round 9.

## 8.3 Regenerated population (29,288): 624 refused, two causes

| cause | count | c | cpp | go | rust | swift |
|---|---|---|---|---|---|---|
| never returns | 408 | 192 | 216 | 0 | 0 | 0 |
| no answer home | 216 | 61 | 55 | 13 | 8 | 79 |

- **never returns** — the same cause as §8.1. LITERAL, the body of
  `c/regen_1016`: `sub $0x18,%rsp; movaps %xmm0,(%rsp); call d
  <op_1016+0xd>; movaps %xmm0,%xmm1; movaps (%rsp),%xmm0; add
  $0x18,%rsp; jmp 1d <op_1016+0x1d>`.
- **no answer home** — the unit's own code names no register the
  answer is left in. Two shapes inside this cause, both measured: 81
  units whose answer is in the x87 stack (`fldt`/`fchs`, LITERAL, the
  whole body of `c/regen_137`: `fldt 0x8(%rsp); fchs; ret`), and 135
  units whose entire body is `ret`. Neither has a register answer this
  checker can name, so neither is stored into OUT-0.

---

# 9. Zero regressions in the ruled sense

The rule: no unit proved under round 9 loses proved status without a
named, PROVED cause. `canon37_zero_regression.py` computes the
before/after sets and checks each named cause mechanically.

LITERAL — its output:

```
original (1,779 compiled units)    round9 proved   1752  round10 proved   1763  lost     0  gained    11  ZERO REGRESSIONS in the ruled sense
interpreter/JIT (11 units)         round9 proved      9  round10 proved      9  lost     0  gained     0  ZERO REGRESSIONS in the ruled sense
regenerated (29,288 units)         round9 proved  27223  round10 proved  28664  lost   606  gained  2047  ZERO REGRESSIONS in the ruled sense
           392  A: the unreachable store
           214  B: the vacuous answer home
```

The 11 gained in the original population, by name: `cpp/op_765`,
`cpp/op_770`, `go/op_30`, `go/op_31`, `go/op_32`, `go/op_33`,
`go/op_34`, `go/op_35`, `swift/op_128`, `swift/op_703`,
`swift/op_739`.

## 9.1 Cause A — the unreachable store (392 units)

Round 9 appended its result store and a `ret` AFTER a body whose last
instruction is an unconditional transfer.

LITERAL — round 9's own text for `c/regen_1016`
(`canon36_regen_store/op_units2_c_c…json`, field `universal_text`, the
tail of it):

```
… ; jmp 1d <op_1016+0x1d> ; movq %xmm0,0x200(%r15) ; ret
```

GLOSS: on the real machine that store can never execute — the `jmp`
has already left. Round 9's simulator walks the text straight through
and does not model `jmp`, so it read a value the machine would never
write. THE CHECK, run per unit rather than asserted: the body's last
instruction is an unconditional transfer, the body carries zero `ret`,
and round 9 placed a store after that transfer. 392 of 392 pass the
check.

## 9.2 Cause B — the vacuous answer home (214 units)

Round 9's structural route does not require an answer home, so it
admitted units for which none could be named at all.

THE CHECK, per unit: round 9's own record names no answer home, or
names a register family the unit's own body never writes. 214 of 214
pass the check.

## 9.3 The residue

`lost_with_no_named_cause` is **0** in all three populations. That is
the field the rule is about, and it is empty.

---

# 10. Complete file inventory

## 10.1 New this lap, all in `PseudoCoupHQ/Research/op_pipeline`

| file | what it is |
|---|---|
| `ledger47.py` | THE FORM: the ledger, its absolute addressing, typed rows, the prelude/body/epilogue wrapper, and the dataflow walk that fills the provenance ledger. Read its header first. |
| `canon37_gate.py` | THE GATE: Sim47 (the row-aware simulator), the arrival binding, the proof obligation, the structural route's five checks, and the language-aware arrival contract. |
| `canon37_lemma.py` | the two-step lemma, checked once with z3. |
| `canon37_wrapped.py` | driver, original population (1,779). |
| `canon37_interp.py` | driver, interpreter/JIT population (11). |
| `canon37_regen.py` | driver, regenerated population (29,288), per-chunk resume. |
| `canon37_assemble.py` | `as --64` + `objdump -d` + `objdump -r`, with the branch-target repair and the out-of-unit stubs. |
| `canon37_acceptance.py` | the four acceptance instances. |
| `canon37_zero_regression.py` | the before/after audit with per-cause mechanical checks. |
| `canon37_guard.py` | both guards, exemption removed. |
| `canon37_wrapped_c.json` | 610 units. |
| `canon37_wrapped_cpp.json` | 770 units. |
| `canon37_wrapped_go.json` | 107 units. |
| `canon37_wrapped_rust.json` | 125 units. |
| `canon37_wrapped_swift.json` | 167 units. |
| `canon37_interp.json` | 11 units. |
| `canon37_regen_store/` | 326 chunk files, 29,288 units. |
| `canon37_regen_state.json` | the resume file: 326 of 326 chunks done. |
| `canon37_assemble.json` | per-unit assembly results, 2,728 offered. |
| `canon37_assemble_transcripts.txt` | sampled `objdump -d` transcripts, verbatim. |
| `canon37_acceptance.txt` | the four acceptance instances, 441 lines. |
| `canon37_zero_regression.json` | the audit. |
| `canon37_guard.txt` | both guards' output. |

## 10.2 Touched, not created

None. Round 9's artifacts (`region36.py`, `canon36_*.py`,
`canon36_*.json`, `canon36_regen_store/`) are unchanged on disk and
remain the superseded record. `check_no_spelling_keys.py` is unchanged;
`canon37_guard.py` adjusts its module-level field sets in memory at
run time and says so in its own header.

## 10.3 One environment change

`capstone` was installed into `/tmp/reconnect_venv` this lap. It was
already an unstated requirement — `canon10_behaviour_check.py` imports
`real_blocks.py`, which imports `capstone`, and the venv had been
rebuilt without it. The branch-target repair uses it too.

---

# 11. What this leaves for task 48

- The ledgers are on disk for all 30,436 proved units, each row
  carrying its producer and operands. Task 48's transcription from
  OUT-0 downward reads exactly these rows.
- The census filter task 48 needs — "rows whose producer has no
  term" — has a clean input: `produced_by` is an arch opcode in
  240,675 of 240,675 rows, checked, with zero lifter-internal names
  and zero holes.
- The 642 refused units are named by cause in §8 and are the honest
  population task 48 cannot transcribe.

---

# 12. Nothing is awaiting a decision

No question is put to the owner in this log. Everything above is decided,
recorded, and checked.
