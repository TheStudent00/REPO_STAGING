# log 163 — TASK 61: `term.py` and `pool.py`

Date: 2026-09-03. Nodes: `0_3_5_6 term`, `0_3_5_7 pool`. Round 12,
under the plan tree. Home:
`~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

---

# 1. What this lap did, and the numbers with their populations

## 1.1 The two modules

Two nodes had `planned` in their PROGRESS and now have code carrying
their own names: `term.py` with class `Term`, and `pool.py` with class
`Pool`. Their methods are the nodes' own sub-nodes, nothing more and
nothing less.

- `Term.transcribe` — a unit's ledger read from OUT-0 downward into a
  z3 term.
- `Term.normalize` — that term printed by one fixed rule.
- `Term.census` — the rows whose producer has no builder.
- `Term.render_back` — **planned, not attempted**; the method refuses
  by name rather than returning something that looks like a rendering.
- `Pool.merge`, `.compare`, `.representative`, `.families`,
  `.exception_families`.

## 1.2 The term figures, per population

**Population: the 30,432 units canon39 records as
WRAPPED_TEXT_PROVED** (of 31,078 attempted; 646 canon39 refused and
are not transcribed). The baseline is task 58's re-gate over
**canon38's 30,436**.

LITERAL — `audit61_printed.txt`:

```
-- THE FOUR STATES, task 58 over canon38 -> task 61 over canon39
   state           task 58    task 61     move
   proved            25179      26040     +861
   withdrawn             0          0       +0
   undecided          3970       3865     -105
   no term            1287        527     -760
   TOTAL             30436      30432       -4

CONSISTENCY -- units proved on one route and disproved on the other: 0
```

GLOSS. Every unit task 58 proved still proves. 861 units that had no
term at all now have a proved one. 760 fewer units are left with no
term. The four missing from the total are the four swift regenerated
units canon39 itself refused.

## 1.3 Every movement, with its computed cause

LITERAL — `audit61_printed.txt`:

```
-- THE TRANSITION, unit by unit (only units in BOTH runs)
   task 58      task 61         units   sightings
   proved       proved          25179   c/op_0, c/op_1, c/op_101
   undecided    undecided        3865   c/regen_1001, c/regen_10073, c/regen_10087
   no term      proved            861   c/regen_34943, c/regen_35988, c/regen_36007
   no term      no term           426   c/op_100, c/op_21, c/op_22
   undecided    no term           101   c/regen_12973, c/regen_13315, c/regen_15551

-- GAINED, by COMPUTED cause (the reason the unit's OWN task-58 record recorded)
      861 | the old run built no term: no reason recorded

-- LOST, by COMPUTED cause (the reason the unit's OWN task-61 record records)
   (none)

-- units in one run and not the other
   in task 61 and not task 58: 0 []
   in task 58 and not task 61: 4 ['swift/regen_315', 'swift/regen_321', 'swift/regen_327', 'swift/regen_333']
```

GLOSS. The 101 units that moved from undecided to no term are not lost
proofs — they never proved. They lost their TERM, because the shared
opcode table refuses a conditional transfer that `layer4.py`'s own
table used to model; §4.2 is that finding.

## 1.4 The pool figures, per population

**Population: every one of those 30,432 proved units.** The baseline
is `the_pool3.json` over canon38's 30,436.

| quantity | pool3 (canon38) | pool4 (canon39) |
|---|---|---|
| entries | 2,247 | **1,961** |
| members | 30,436 | **30,432** |
| entries spanning more than one language | 632 | **573** |
| entries spanning compiled and interpreted | 3 | **3** |
| families | 36 | **34** |
| entries under the brief-strict rule (recorded, unused) | 8,394 | **5,668** |

## 1.5 The one correction made to the tree before any code ran

Task 61's brief named `exception_families3.json` for the rebuild.
**That name was already taken on disk**: the round-5 line's own later
build over `guards5.json` wrote `exception_families3.py` and
`exception_families3.json` on 2026-09-01, and the exception_families
CORE's realization table already recorded them. A superseded record is
never edited and numbered artifacts accumulate, so the rebuild takes
the next number, `exception_families4.json`.

Per PROTOCOL §2 and round rule 2, the CORE was corrected FIRST — a new
settled rule with its provenance, and the realization table updated —
and the node's PROGRESS records it. Then the code was written.

---

# 2. `term.py` — the node, with values in motion

## 2.1 Meanings come from one table, and this is what that cost

The term CORE's settled rule: *"Meanings come from one table shared
with the reference, so route two tests wiring and route one tests
meaning."* `layer4.py` had its own producer table; that table WAS the
second table, so it is neither imported nor copied. Every arch
opcode's meaning in `term.py` is read from
`reference.Reference.opcode_table` — the same object the gate's
reference route reads.

The mechanical consequence, stated because it is the whole design of
this file. A `reference` builder reads its inputs through
`reference.Operands`, which reads through `reference.MachineState` and
through nothing else. So a ledger row becomes a term like this:

1. The row's own body line is recovered (§2.2).
2. A fresh `MachineState` is seeded from the HOLDER MAP — register
   family to the row that last resides there, filled from the rows'
   own `resident` fields, which is the ledger's wiring written down.
3. The mnemonic is looked up in the shared table; the entry's builder
   runs over that state.
4. The produced value is read back out at the place the row itself
   says it resides.

## 2.2 The relink, and why it exists

A canon39 ledger row carries no body line, and a term needs widths —
`add %esi,%eax` is a 32-bit operation inside an 8-byte row. So the
line is recovered by re-running `ledger.Ledger.walk_dataflow` with two
seams recorded: `ledger.mnemonic_of`, called once per body line, says
which line is being walked; a `Ledger` subclass's `add`, called once
per row, stamps that line onto the row. The re-run is then CHECKED row
for row against the stored ledger — same row names, same typed
producers, same operands, in order — and a unit whose re-run disagrees
is refused by name.

This is `relink48.py`'s method applied to the landed `ledger.py`
instead of to the superseded `ledger47.py`; nothing of `relink48.py`
is imported. The prelude used for the re-run is
`canonical_form.Prelude`, so IN-i is argument i — the arrival-contract
order canon39 was actually written with, not
`ledger.Ledger.build_prelude`'s vector-first order, which task 60
fixed.

## 2.3 One transcription, literally

LITERAL — `show61_go_op_319.txt`, the term CORE's own worked instance:

```
UNIT            go/op_319   (from canon39_wrapped_go.json)
language        go
population      original
arrival         ["rax", "rbx"]
answer home     rax at 64 bits

THE BODY, VERBATIM (the compiler's own text, untouched)
    add %rbx,%rax
    ret

THE WRAPPED TEXT (layer 3, the runnable record)
    mov IN-0,%rax; mov IN-1,%rbx; add %rbx,%rax; mov %rax,OUT-0; ret

THE LEDGER, ROW BY ROW, WITH THE LINE THE RELINK ATTACHED
    row      produced_by (typed)                            line                     term
    IN-0     {"kind": "non_opcode_phrase", "phrase": "arrival"} -                        seed_rax
    IN-1     {"kind": "non_opcode_phrase", "phrase": "arrival"} -                        seed_rbx
    TEMP-0   {"kind": "arch_opcode", "mnem": "add"}         add %rbx,%rax            seed_rax + seed_rbx
    OUT-0    {"kind": "arch_opcode", "mnem": "add"}         -                        seed_rax + seed_rbx

THE READ AT OUT-0 (layer 4, the term)
    seed_rax + seed_rbx

THE TWO GATE ROUTES
    route one  PROVED_ON_SHIP
    route two  PROVED_ON_SHIP

THE NORMALIZED TEXT (layer 5, the comparison key)
    v0 + v1

HOLES 0, CASCADES 0, SLOT DISAGREEMENTS 0
```

GLOSS. IN-0 is bound to `seed_rax` because the ledger's own wiring
says argument zero arrives in `%rax` for go; the reference simulator
spells its own symbol the same way, which is why the two gate routes
need no substitution step between them. OUT-0 is the read: the term is
the ledger from OUT-0 downward, and `v0 + v1` is that term with its
free symbols renamed positionally.

## 2.4 The five defects the gate caught, each with the unit that caught it

Every one of these was found the same way: a unit task 58 had PROVED
came back DISPROVED. That is the gate doing exactly its job, and it is
why the count of withdrawn units in the delivered run is 0.

### 2.4.1 The constant-pool counter restarted every row

The reference keys the k-th rip-relative read of a body as
`ripconst_k`. This walk builds one machine state PER ROW, so every
row's first read was `ripconst_0` — and a body reading two different
pool constants was transcribed as reading one.

Values in motion, `c/op_118`, whose body reads two pool constants:

```
    punpckldq 0x0(%rip),%xmm1      the first pool read   -> ripconst_0
    subpd     0x0(%rip),%xmm1      the second pool read  -> ripconst_0   WRONG
                                                         -> ripconst_1   right
```

74 c units of 610 in the original corpus. Fix: the counter lives on
the unit's record (`Transcription.rip_reads`) and is carried into and
out of each row's state.

### 2.4.2 Both halves of one instruction must read the state before it

`idiv` writes a quotient row and a remainder row from ONE line.
Publishing the quotient's residence before the remainder was built
made the remainder read the quotient.

Values in motion, `c/op_246` — the reference CORE's own acceptance
instance, `a % b` at 32 bits:

```
    mov %edi,%eax      TEMP-0 = a
    cltd               TEMP-1 = sign of a
    idiv %esi          TEMP-2 = quotient,  TEMP-3 = remainder
```

Before: `TEMP-3 = SRem(Concat(sign, QUOTIENT), b)` — the remainder
computed from the quotient. After: `TEMP-3 = SRem(Concat(sign, a), b)`,
and both routes prove.

Fix: rows are grouped by LINE OCCURRENCE, and a row's residence is
published to the holder map only when the line that made it is
finished (`Term.publish`).

### 2.4.3 The x87 stack was rebuilt by push order, not by wiring

`fxch` swaps two x87 positions and makes no ledger row, so a stack
rebuilt by pushing the X87 rows in their own order has the operands
reversed after an exchange.

Values in motion, `c/regen_36772`:

```
    fldt 0x8(%rsp)      push A     X87-0
    filds -0x2(%rsp)    push B     X87-1     stack: st0=B, st1=A
    fxch %st(1)                              stack: st0=A, st1=B
    fucomip %st(1),%st  compares st0 with st1 = (A, B)
```

Push order gives (B, A) — the comparison the wrong way round, and the
gate DISPROVED it. The ledger had already resolved this: the row's
operands are `['X87-1', 'X87-0']`, in the arch text's own operand
order, which says position 1 holds X87-1 and position 0 holds X87-0.
Fix: `Term.seed_x87` reads the row's own operand list. Replaying push
order was a second dataflow analysis, and it was wrong.

### 2.4.4 A literal row was published as a register's holder

Values in motion, `go/op_206`:

```
    cmp $0x20,%rbx     CONST-0 = 32   (the body's own immediate operand)
    ...
    or  %rbx,%rcx      read %rbx -> 32        WRONG
                       read %rbx -> seed_rbx  right
```

A CONST row is the body's own immediate and an OWN row is a stack
address the body spells; neither resides in the line's destination
register. 57 units were DISPROVED by this. Fix:
`Term.remember_residence` returns early for a non-opcode-phrase
producer.

### 2.4.5 A value-writing flag setter left no flags for its reader

A flag pair is one act with two halves, and the setting half is often
an ordinary arithmetic opcode whose row carries a VALUE, not a flag
state — the flags it also left are a second thing the same instruction
produced.

Values in motion, `c/op_282`:

```
    xor %eax,%eax      TEMP-0 = 0
    or  %esi,%edi      TEMP-1 = a | b        and flags
    setne %al          GUARD-0 reads those flags -> refused, no flags
```

1,364 units. Fix: `Transcription.flag_state` keeps, per row, the flag
state that row's own builder left, and a flag-pair row picks it up
from the row the ledger says it reads. `c/op_282` now normalizes to
`If(Extract(31, 0, v0) | Extract(31, 0, v1) == 0, 0, 1)` and proves on
both routes.

---

# 3. `name_census5.json` — the census, printed

## 3.1 The population and the tally

LITERAL — `name_census5_printed.txt`:

```
-- the population
   layer-4 records read 30432
-- the census over canon39
   producers 52
   rows blocked 1877
   units blocked 1283
   cascades (not census entries) 1136
```

GLOSS. Against census4's 54 producers / 1,719 rows / 1,668 units over
canon38. A cascade is a row whose PRODUCER is modelled but whose
operand row has no term; it is counted separately so one hole is never
reported as many.

## 3.2 The census, printed (the head of the table)

LITERAL — `name_census5_printed.txt`:

```
   producer                                           rows    units  languages
   flag_pair:test,js                                   424      424  c,cpp,swift
   arch_opcode:lea                                     154      138  c,cpp,go,rust
   flag_pair:cmp,jae                                   153      115  swift
   flag_pair:cmp,jbe                                   126      126  go,swift
   flag_pair:test,jl                                   122      122  go
   non_opcode_phrase:an x87 stack position this unit did not itself load       84       84  c,cpp
   flag_pair:test,je                                    80       80  go,rust,swift
   runtime_callee:__udivti3                             78       78  c,cpp,rust
   runtime_callee:__umodti3                             78       78  c,cpp,rust
   runtime_callee:__divti3                              74       74  c,cpp,rust
   runtime_callee:__modti3                              74       74  c,cpp,rust
   arch_opcode:div                                      64       32  c,cpp,go,rust,swift
   non_opcode_phrase:the body's last write to %xmm0       32       32  c,cpp,go,rust,swift
```

Every producer is a TYPED object — `{kind, mnem}`, `{kind, mnem:[setter,
reader]}`, `{kind, phrase}`, `{kind, callee}`. The printed key above is
built from those fields; no bare operator token keys anything.

## 3.3 The delta against census4, matched on the reason sentence

LITERAL — `name_census5_printed.txt`, the closures:

```
   causes CLOSED 8
       -400 rows | no z3 term is written for this x87 arch opcode
       -774 rows | the flag-setting arch opcode 'sbb' left flags this file could not build ...
       -186 rows | this suffix reads the carry bit, and the flag-setting arch opcode 'fucomip' has no carry model in this file
       -10 rows  | the flag-setting arch opcode 'mul' left flags this file could not build ...
       -9 rows   | operand '%ah' names the SECOND byte of a register ...
       -2 rows   | the flag-setting arch opcode 'adc' left flags this file could not build ...
       -2 rows   | no z3 term is written for this arch opcode
       -1 rows   | the flag-setting arch opcode 'imul' left flags this file could not build ...
```

LITERAL — the causes that appeared in their place:

```
       +425 rows | arch opcode 'js' is a census row, not a silent gap: a transfer or trap, and this reference walks a body in text order
       +154 rows | the shared opcode table refused: an address computation over base register '%rip' ...
       +88 rows  | the shared opcode table refused: a division at width 16 is not modeled
       +88 rows  | the shared opcode table refused: a division at width 8 is not modeled
       +78 rows  | the attached body of the runtime callee '__udivti3' contains the transfer 'je 79 <__udivti3+0x79>', whose target the attachment did not record ...
       +78 rows  | the attached body of the runtime callee '__udivti3' spells 'endbr64', which the shared opcode table refused ...
       +10 rows  | the shared opcode table refused: a widening multiply at width 8 is not modeled ...
       +9 rows   | the shared opcode table refused: operand '%ah' is neither an immediate, a register nor a memory operand this file reads
   causes that MOVED 1
       335 -> 35 | no arch opcode in this body writes the answer register, so no row produces the answer
```

GLOSS, and it is the honest reading of "one table". The x87 arithmetic
family and the whole `sbb`/`adc` flag family CLOSED, because
`reference.py` models them. What appeared in their place is the price
of sharing one table with a reference that walks a body IN TEXT ORDER:
that reference has no model for a conditional transfer, so a guard
whose reader is a `j<cc>` is now a census row where `layer4.py`'s own
condition table used to build a predicate. It is a real gap, named
rather than patched around, and it is where the 101 undecided-to-no-term
units went.

## 3.4 The runtime-callee expectation, tested and answered

The brief named the formerly runtime-callee-undecided units as the
expectation to test now that `ledger.py` attaches 304 callees.

LITERAL — `audit61_printed.txt`:

```
-- the runtime callee expectation
   units carrying a runtime_callee row 304
   runtime_callee rows 608
```

**The expectation fails, for a named mechanical reason.** Every
attached callee body BRANCHES, and the shared reference walks a body
in text order. Measured over `runtime_callee_units.json`, per
toolchain:

| routine | what blocks it |
|---|---|
| clang / clang++ `__divti3`, `__modti3`, `__umodti3` | `endbr64` (no entry in the table), then an unrelocated `call` |
| clang / clang++ `__udivti3` | `endbr64`, then an unrelocated `jmp` |
| rustc `__divti3`, `__modti3` | an unrelocated `call`, and `ud2` |
| rustc `__udivti3`, `__umodti3` | `bsr` (no entry), and `jae`/`je` |

An archive member's calls are UNRELOCATED — `call 4c
<__divti3+0x4c>` names an offset, not a symbol, because the symbol
lives in the relocation table that `ar x` + `objdump -d` did not
carry. So the nested callee has no name to follow. Each of these is a
census row with its own written reason; nothing was invented to get
past it. The work this needs — a branch model in the reference, and a
relocation-aware attachment — is not task 61's, and is not attempted
here.

One further detail, and it is a correctness point rather than a
limitation: the attached bodies are keyed BY TOOLCHAIN, not by bare
routine name, because the four archives do not agree — clang's
`__udivti3` is three instructions and rustc's is sixty-seven. A rust
caller gets rustc's body.

---

# 4. `pool.py` — the pool, the families, the exception families

## 4.1 The three grounds, with the counts each contributed

LITERAL — `pool61_run.log`:

```
-- the merge, brief-strict: layer-5 identity and proved edges only (RECORDED, NOT USED)
   entries under the brief-strict rule 5668
-- the merge, as ruled: layer-5 identity, layer-3 identity, proved edges
   distinct_layer3_wrapped_texts                  2993
   distinct_layer5_texts_among_eligible_units     1286
   layer3_identity_merges                         27439
   layer5_identity_merges                         24754
   proved_edges_applied                           118
   entries 1961
```

GLOSS. Against pool3's 2,997 / 1,104 / 27,439 / 22,028 / 118 / 2,247.
The layer-5 ground did 2,726 more merges than it did over canon38,
because 861 more units have a proved term to print. The brief-strict
count is on the artifact as
`summary.entries_under_the_brief_strict_rule` and is read by nothing.

## 4.2 The representative rule

LITERAL — `pool61_run.log`:

```
-- the representative rule
   entries carrying more than one wrapped text 480
   distinct texts to assemble 1512
   texts newly assembled 1512, would not assemble 10, cache holds 1512
```

The bytes are MEASURED — `as --64` then counted from `objdump -d`.
The 10 that would not assemble carry an inline constant-pool
relocation note that is not assembler syntax; those entries fall back
to character length and say so in
`representative_size_measured_as`.

## 4.3 E00029's successor, printed

E00029 is integer addition. Its successor in pool4 **is E00029, and it
is unchanged**: same 158 members, same seven languages, same
representative at the same measured size, with no member gained and
none lost.

LITERAL — computed against both pools:

```
E00029 (pool3): 158 members; ['c', 'cpp', 'cpython', 'go', 'php', 'ruby', 'rust'] rep go/op_319 35
successor entries: ['E00029']
E00029 members 158 langs ['c', 'cpp', 'cpython', 'go', 'php', 'ruby', 'rust'] rep go/op_319 35 kept 158 new 0
```

LITERAL — the head of the entry itself,
`pool4_entry_E00029_printed.txt`:

```
 "cross_language_grounds": [
  {
   "detail": "these members carry the SAME wrapped text, character for character -- the same machine code twice",
   "ground": "layer-3 text identity",
   "languages_it_joins": ["c", "cpp", "rust"],
   "wrapped_text": "mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; lea (%rdi,%rsi,1),%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret"
  },
  {
   "detail": "these members carry the SAME wrapped text, character for character -- the same machine code twice",
   "ground": "layer-3 text identity",
   "languages_it_joins": ["php", "ruby"],
   "wrapped_text": "mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; mov %rdi,%rax; add %rsi,%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret"
  },
```

GLOSS. The two texts differ — `lea (%rdi,%rsi,1),%rax` against
`mov %rdi,%rax` + `add %rsi,%rax` — and each joins its own languages
by layer-3 identity; the layer-5 ground is what puts the two groups in
one entry.

## 4.4 The delta against pool3, every cause computed

Joined on MEMBER SETS, never on entry numbers, so a renumbering is not
read as a change.

LITERAL — `pool61_run.log`:

```
   splits 7, merges 107, units gone 4, units new 0
```

The split causes, computed from the entries themselves:

| cause | splits |
|---|---|
| the members no longer print one layer-5 text | 3 |
| the members' layer-3 texts and proved edges no longer join them | 4 |

The merge causes, computed the same way:

| cause | merges |
|---|---|
| one layer-5 text now stands over 2 distinct wrapped texts | 46 |
| a proved edge joined them | 27 |
| one layer-5 text now stands over 4 distinct wrapped texts | 13 |
| the layer-3 ground joined them | 5 |
| one layer-5 text over 3 / 6 / 7 / 9 / 10 / 12 / 44 wrapped texts | 15 |
| the layer-5 ground joined them (no text count recorded) | 1 |

The 4 units no longer in the pool are named:
`swift/regen_315`, `swift/regen_321`, `swift/regen_327`,
`swift/regen_333` — the swift callers canon39 refused because swift's
runtime archive is on neither side of the container wall (log_161
§4.1.1).

## 4.5 The families — 36 became 34, and the cause is computable

LITERAL — `pool61_run.log`:

```
   nodes (language, grammar-operator, arity) 197
   cross-language edges, raw 1014
   edges surviving the mutual filter 322
   families 34
```

Compared BY NODE SET, as the families CORE requires: **32 of the 36
node sets are unchanged**. The other four — each a two-node family in
pool3 — were absorbed pairwise into two six-node families in pool4:

| pool4 family | nodes | languages |
|---|---|---|
| `F0009` | N0024, N0031, N0070, N0079, N0174, N0181 | c, cpp, swift |
| `F0010` | N0027, N0033, N0073, N0081, N0177, N0183 | c, cpp, swift |

Each absorbed the pool3 pair that sat in its own languages. So the
count fell by two because four small families became two larger ones,
not because anything was lost. (Display labels on those nodes, read by
nothing: the two families are the strict and the non-strict
comparisons, at unary arity, across c, cpp and swift.)

## 4.6 The exception families, rebuilt

LITERAL — `pool61_run.log`:

```
-- the exception families, rebuilt over this pool
   guard rows read 314
   rows considered 128
   rows excluded (continue-with-a-different-answer) 186
   rows about units outside this pool 0
   exception families 40
```

**The population, stated:** the guard rows of `guards5.json` whose
unit is a member of `the_pool4.json`. **The rule applied:** guard
identity is the CONDITION TESTED and the RESPONSE TAKEN together,
never the condition alone, grouped across languages — this node's own
settled rule. 186 rows are excluded because their response head is
`continue-with-a-different-answer`, which is `core_modes.py`'s honest
"no named response proved" outcome and is not one of the five ruled
guard responses.

What makes this a rebuild OVER the pool rather than beside it: each
family now carries `pool_entries` — the entries its members sit in —
so a guard family can be read against the computations it guards.

---

# 5. Compliance

## 5.1 One process

The delivered run is one process. **This did not go right the first
time, and the failure is recorded rather than hidden**: the first
launch of `term61_run.py` reported a shell error but had in fact
started, and a second launch then ran beside it — two processes over
one store. Both were stopped, `term61_store/` and `term61_state.json`
were deleted, and the run was restarted as a single process. The
delivered store was written by one process from an empty directory.

## 5.2 The unmodified guard, over every artifact

The guard is unmodified — `git status --porcelain` on
`check_no_spelling_keys.py` prints nothing, and its md5 is
`1d6aba67cbcdb021c3bdfd7f40fd2020`.

LITERAL — the seven grouping artifacts:

```
PASS name_census5.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool4.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families4.json -- no operator token in any key, grouping, pairing or row structure
PASS exception_families4.json -- no operator token in any key, grouping, pairing or row structure
PASS pool3_pool4_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS audit61.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool4_bytes.json -- no operator token in any key, grouping, pairing or row structure
```

LITERAL — every one of the 332 term shards:

```
shards checked 332 failed 0
[]
```

## 5.3 No carve-out claimed

```
$ grep -c exempt term.py pool.py term61_run.py pool61_run.py audit61.py name_census5.py show61.py
term.py:0
pool.py:0
term61_run.py:0
pool61_run.py:0
audit61.py:0
name_census5.py:0
show61.py:0
```

No `role` field is declared on any artifact this pipeline reads; the
`role_note` on each says so in words and claims nothing.

## 5.4 The spelling ban

The ban is pasted verbatim in every module written this lap. No
operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope. `operator` on a pool member
and `label` on a family node are display fields, read by nothing —
which is why §4.5's family description had to name the nodes by id and
put the spelling in a parenthesis.

---

# 6. File inventory

## 6.1 Modules written

| file | what it is |
|---|---|
| `Research/op_pipeline/term.py` | the node `term`: `Term.transcribe`, `.normalize`, `.census`, `.render_back` (refuses) |
| `Research/op_pipeline/pool.py` | the node `pool`: `Pool.merge`, `.compare`, `.representative`, `.families`, `.exception_families` |

## 6.2 Drivers and reporters written

| file | what it is |
|---|---|
| `Research/op_pipeline/term61_run.py` | the run over the canon39 proved population, resumable, one process |
| `Research/op_pipeline/name_census5.py` | the census and its delta against census4 |
| `Research/op_pipeline/audit61.py` | the four states per population, the transitions, the causes, the consistency line |
| `Research/op_pipeline/show61.py` | one transcription shown literally |
| `Research/op_pipeline/pool61_run.py` | the pool, the families, the exception families, the delta |

## 6.3 Artifacts written

| file | what it holds |
|---|---|
| `term61_store/*.json` (332) | per unit: the term's state, both gate verdicts, the layer-5 text, holes, cascades, slot disagreements |
| `term61_state.json` | the resume state of the run |
| `term61_run.log` | the run's own transcript |
| `name_census5.json`, `name_census5_printed.txt`, `name_census5_run.log` | the census, printed, with the delta by reason sentence |
| `audit61.json`, `audit61_printed.txt` | the figures and every movement's cause |
| `show61_go_op_319.txt` and the other `show61_*.txt` | the literal transcriptions |
| `the_pool4.json` | 1,961 entries over 30,432 members |
| `the_pool4_bytes.json` | the 1,512 measured texts |
| `the_families4.json` | 34 families over 197 nodes |
| `exception_families4.json` | 40 guard families over the pool's own members |
| `pool3_pool4_delta.json` | 7 splits, 107 merges, every cause computed |
| `pool4_entry_E00029_printed.txt` | E00029's successor, printed |
| `pool61_run.log` | the pool run's transcript |
| `task61_resume.md` | the resume state, the reading, the corrections, the five defects |

## 6.4 PROGRESS files updated

| file | entries added |
|---|---|
| `node_0_3_5_6_term/PROGRESS.md` | the module; the figures; render_back still planned |
| `node_0_3_5_6_term/node_0_3_5_6_2_transcribe/PROGRESS.md` | the walk and the relink; the five defects; the runtime-callee finding |
| `node_0_3_5_6_term/node_0_3_5_6_3_normalize/PROGRESS.md` | the rule re-expressed; 1,286 distinct texts |
| `node_0_3_5_6_term/node_0_3_5_6_4_census/PROGRESS.md` | census5; what closed and what appeared |
| `node_0_3_5_6_term/node_0_3_5_6_5_render_back/PROGRESS.md` | still planned, deliberately |
| `node_0_3_5_7_pool/PROGRESS.md` | the module; pool4; the delta; the rebuild |
| `node_0_3_5_7_pool/node_0_3_5_7_1_entry/PROGRESS.md` | the entry shape; E00029 unchanged; 4,392 ineligible members |
| `node_0_3_5_7_pool/node_0_3_5_7_2_merge_grounds/PROGRESS.md` | the three grounds' counts; the brief-strict count |
| `node_0_3_5_7_pool/node_0_3_5_7_4_representative/PROGRESS.md` | 480 entries, 1,512 texts, 10 substitutions |
| `node_0_3_5_7_pool/node_0_3_5_7_5_families/PROGRESS.md` | 34 families over 197 nodes |
| `node_0_3_5_7_pool/node_0_3_5_7_6_exception_families/PROGRESS.md` | the name correction; the rebuild |

## 6.5 CORE corrected

| file | what changed |
|---|---|
| `node_0_3_5_7_pool/node_0_3_5_7_6_exception_families/CORE_0_3_5_7_6_exception_families.md` | a new settled rule — the rebuild takes the next number, not a taken one — and the realization table updated |

---

# 7. Resume state

Nothing of task 61 is left running or half-written. To re-derive
everything from the canon39 artifacts, in order, with
`/tmp/reconnect_venv/bin/python3` from
`~/Programming/PseudoCoupHQ/Research/op_pipeline`:

```
term61_run.py 30000      # resumable; ~30 minutes, one process
name_census5.py
audit61.py
pool61_run.py
show61.py <unit-label>   # any single unit, shown literally
```

`term61_run.py` resumes from `term61_state.json`; delete that file and
`term61_store/` to force a clean pass. `pool61_run.py` REFUSES its own
output if any proved unit has no layer-4 record, so it cannot be run
against a partial store.

## 7.1 What is owed, named rather than implied

1. **`render_back`** — node 0_3_5_6_5, still planned. Until it exists,
   layer 3 is the only runnable record and layer 5 is a key beside it.
2. **A branch model in the shared reference** — 425 rows of
   `test`/`j<cc>` pairs and the whole runtime-callee family are census
   rows because the one table's reference walks a body in text order.
   This is the largest single cause in census5.
3. **A relocation-aware runtime-callee attachment** — the archive
   bodies' calls are unrelocated, so nested callees have no name to
   follow; and `endbr64` and `bsr` have no entry in the table, because
   the table was pruned to the mnemonics the corpus's own bodies
   spell and these bodies are new.
4. **Division at widths 8 and 16, and widening multiply at 8 and 16** —
   194 rows between them, refused by the shared table by name.
