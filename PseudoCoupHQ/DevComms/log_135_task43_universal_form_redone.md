# log 135 — TASK 43: the universal form, redone to the owner's statement

Date: 2026-09-02. Author: Claude Code (implementer), no sub-agents.
Working directory: `PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim.

---

# 1. What was done, in plain words, before any figure

Round 8's form kept a register as each value's home and put its three
memory slots just below the stack pointer. This lap throws both away.
Every unit now works in a block of virtual memory with a base of its
own, held in one register that no value is ever allowed to occupy.
Each thing a unit deals with — each argument, each literal, the
answer, each address the unit takes of its own scratch — gets its own
typed block in that memory, at an address fixed the same way for every
unit in every language. The unit's first act is to load its arguments
out of their blocks; its last act is to store the answer into the
answer's block. Which registers the loads and stores ride in is
decided by one rule applied identically everywhere, not by whichever
registers the original compiler happened to pick.

Three populations were put through it: the original corpus of 1,779
compiled units, the 11 interpreter/JIT units, and the 29,288
regenerated units. Each rendered unit was proved against its own ship
code (or, where a unit has one, against its own canonical text, which
already carries a ship proof) with the arguments bound to their
blocks. The texts were then assembled with `as` and read back with
`objdump`, and a sample was executed for real against the original
code.

The one thing this lap set out to fix above all else did get fixed.
Six units answer with the address of their own stack scratch. Round 8
could not place them at all — its directory sat in the same bytes
those units use, so moving the scratch moved the answer, and all six
were disproved. Under the new form their scratch has a block of its
own inside the region, at an address every unit computes the same way,
so all six now prove AND all six now read identically to each other.

---

# 2. The form, with values moving through it

## 2.1 The names, each introduced before it is used

- **The region** — 0x408 bytes of ordinary stack memory the CALLER
  provides. Every address a unit names is written `0xNN(%r15)` and
  nothing is written `%rsp`-relative or `%rbp`-relative.
- **The ruled base** — `%r15`. It anchors the region. No lineage is
  ever allocated to it, and a unit whose own text mentions it is
  refused by name (measured: 4 of the 1,779).
- **A lineage** — one value's history through the unit: an argument's,
  a literal's, an intermediate's, the answer's, or the address of one
  of the unit's own stack locations.
- **A block** — the piece of the region one lineage owns.

## 2.2 The fixed layout, the same for every unit in every population

```
  kind            offsets              slots   what a block holds
  ------------------------------------------------------------------
  input           0x000 .. 0x03f       8 x 8   one input argument's
                                               lineage per block
  constant        0x040 .. 0x17f      40 x 8   one literal's lineage
  temp            0x180 .. 0x1ff      16 x 8   one intermediate
  result          0x200 .. 0x20f       2 x 8   the answer's lineage
  guard-outcome   0x210 .. 0x23f       6 x 8   one guard's outcome
  own-address     0x300 .. 0x407      0x108    the unit's OWN stack
                                               addresses, as one
                                               lineage
```

- The sizes are measured demand, not guesses: the widest unit in the
  corpus carries 34 distinct literals (12 units do), and the deepest
  own stack displacement any unit spells is 0x20.

## 2.3 The run-time mapping, and why the form stays runnable

- The caller reserves the region immediately below its stack pointer
  and hands the base over:

```
      %r15 = %rsp - 0x400
```

- Three things make this runnable, and none of them is a promise:
  - every operand `0xNN(%r15)` is an ordinary x86-64 `disp32(base)`
    encoding — §5 assembles 2,578 of them with `as` and reads them
    back with `objdump`;
  - `%r15` is callee-saved, so a caller that sets it saves and
    restores it;
  - the unit itself needs NO PROLOGUE — it never adjusts `%rsp`, never
    pushes, and never touches the red zone.

## 2.4 One fixed rule chooses the scratch registers — RULE R

- **R1** walk the finished text in order and collect the distinct
  register families in first-mention order, general and vector
  separately. The standardized loads come first, so an input
  lineage is mentioned first, in arrival order.
- **R2** a family the hardware pins in this core (`%rax`/`%rdx` for
  the sign-extend and divide forms, `%rcx` for a variable shift
  count) is a FIXED POINT: it maps to itself and leaves the pool.
- **R3** every other family takes the next free register of the fixed
  pool:

```
      general: r10 r11 rax rcx rdx rsi rdi r8 r9 rbx r12 r13 r14
      vector:  xmm0 .. xmm13
```

- **R4** `%rsp`, `%rbp`, `%rip` are never renamed; `%r15` may not
  appear at all.
- The map is a permutation, so applying it preserves meaning by
  construction — and the gate proves it anyway.

## 2.5 One unit walked end to end, with real values

`c/op_109` takes two 64-bit integers. Take `a = 20`, `b = 3`.

### 2.5.1 What it looked like before this lap

```
    mov %rdi,%rax     %rax = 20    a is simply FOUND in a register
    mov %rsi,%r10     %r10 = 3     b is simply FOUND in a register
    add %r10,%rax     %rax = 23
    ret                            the answer is in %rax and nowhere
                                   else
```

### 2.5.2 What it is now

```
    mov 0x0(%r15),%r10    %r10 = 20   input block 0 holds a
    mov 0x8(%r15),%r11    %r11 = 3    input block 1 holds b
    mov %r10,%rax         %rax = 20   the core, renamed by rule R
    mov %r11,%rcx         %rcx = 3    the core, renamed by rule R
    add %rcx,%rax         %rax = 23
    mov %rax,0x200(%r15)  block 0x200 = 23   the answer reaches its
                                             own block
    ret
```

- Rule R's four assignments here, verbatim from the artifact:
  `rdi -> r10`, `rsi -> r11`, `rax -> rax`, `r10 -> rcx`. Note the
  last one: the compiler's own choice of `%r10` as a temporary was
  itself renamed. Under round 8 it would have survived untouched.
- The value 20 now has a stated ORIGIN (input block 0) and a stated
  ROUTE (the load into `%r10`, chosen by rule, not by the compiler).
  The value 23 has one home, and it is memory.

## 2.6 The transformations applied to a unit's own core, all three

- **T1, the own-stack rewrite.** Every `-0xN(%rsp)` becomes
  `0x(0x400 - N)(%r15)` — ONE affine map, the same constant for every
  displacement in every unit, so the unit's internal spacing is
  preserved and only the base moves. With the run-time mapping of
  §2.3 the rewritten operand is THE SAME BYTE. A bare `(%rsp)` is
  displacement zero and is placed the same way (round 8 refused it by
  name; 2,185 regenerated units spell it).
- **T2, the rule-R rename** of §2.4.
- **T3, constant materialization.** A literal is loaded from its own
  block into a VEHICLE — a register the rule-R map's image does not
  contain — and consumed on the very next line:

```
      xor $0x1,%dil   ->   mov 0x40(%r15),%r12 ; xor %r12b,%dil
```

  Where the encoding at a site does not admit this, the literal stays
  an immediate and its block is still allocated and directoried; the
  record says which of the two it carries in
  `constant_materialization`, and the whole render is gated either
  way.

## 2.7 The one thing NOT done, said plainly rather than implied

- A register-resident intermediate gets a temp block allocated and
  directoried, but it is NOT spilled to that block. Spilling every
  intermediate rewrites the computation, not its plumbing, and that is
  a different act from the one the owner ruled. Same for a guard outcome:
  the block is allocated from the unit's own recorded branch shape and
  the outcome value is not materialized. Both are recorded per unit.

---

# 3. The address-of units — the case the form exists to fix

## 3.1 What round 8 recorded, quoted

> the answer of this unit is the ADDRESS of one of its own private
> stack locations, and that location collides with the directory

## 3.2 What the six do now, printed verbatim from the artifacts

```
=== c/op_31 ===
BEFORE : mov %edi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : mov 0x0(%r15),%r10; mov %r10d,0x3f8(%r15); lea 0x3f8(%r15),%r11; mov %r11,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP
DETAIL : z3 proved the region text's RESULT BLOCK 0x200(%r15) equal to the unit's own ship code at 64 bits, for every value of every input block, with each input block bound to the same symbol as the argument the reference text reads and the region base bound to %rsp - 0x400

=== c/op_32 ===
BEFORE : mov %edi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : mov 0x0(%r15),%r10; mov %r10d,0x3f8(%r15); lea 0x3f8(%r15),%r11; mov %r11,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP

=== c/op_34 ===
BEFORE : movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : movq 0x0(%r15),%xmm0; movsd %xmm0,0x3f8(%r15); lea 0x3f8(%r15),%r10; mov %r10,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP

=== cpp/op_43 ===
BEFORE : mov %edi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : mov 0x0(%r15),%r10; mov %r10d,0x3f8(%r15); lea 0x3f8(%r15),%r11; mov %r11,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP

=== cpp/op_44 ===
BEFORE : mov %edi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : mov 0x0(%r15),%r10; mov %r10d,0x3f8(%r15); lea 0x3f8(%r15),%r11; mov %r11,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP

=== cpp/op_46 ===
BEFORE : movsd %xmm0,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
AFTER  : movq 0x0(%r15),%xmm0; movsd %xmm0,0x3f8(%r15); lea 0x3f8(%r15),%r10; mov %r10,0x200(%r15); ret
VERDICT: PROVED_ON_SHIP
```

- The own-address block record each of them carries, verbatim:

```
{"kind": "own-address", "lineage": "stack_-0x8", "was": "-0x8(%rsp)",
 "offset": 1016, "text": "0x3f8(%r15)",
 "placed_by": "the affine map REGION_SIZE - displacement",
 "evidence": "the address escapes: a line of the core takes its `lea`,
              so the lineage is the ADDRESS, not the value"}
```

## 3.3 The brief's demand, answered directly

- **Two address-of units now compare equal.** `c/op_31`, `c/op_32`,
  `cpp/op_43` and `cpp/op_44` carry the SAME text, character for
  character; `c/op_34` and `cpp/op_46` carry the same text as each
  other. Under round 8 they carried none at all.
- The reason the answer survives is not luck: the gate binds the
  region base to `%rsp - 0x400`, which is the run-time mapping the
  form rules, so `0x3f8(%r15)` and `-0x8(%rsp)` are the same byte and
  z3 proves the answers identical rather than merely similar.
- The lineage kind is decided by MEASURED EVIDENCE — the address
  escapes through a `lea`, so it is an own-address lineage; a stack
  address only ever loaded and stored is a temp lineage instead.

---

# 4. The gates

## 4.1 What is proved, stated as the obligation

For all values in the input blocks, THE VALUE THE REGION FORM LEAVES
IN THE RESULT BLOCK equals the value the reference text leaves in its
answer home. The answer is read out of memory, never out of a
register — which is the concrete sense in which no register is a home
any more.

- **The bindings, made before anything is proved:** each input block
  to the same symbol as the argument the reference text reads; each
  constant block to its own literal's value; the region base to
  `%rsp - 0x400`.

## 4.2 The three routes, and when each is used

- **The direct ship gate** — against the unit's own ship code. This is
  the admission gate for the regenerated population, which has no
  canonical text at all.
- **The prior-text gate** — against the unit's own canonical text,
  which already carries a ship proof, so the chain is a ship proof.
- **The structural route** — a proof BY CONSTRUCTION, used only where
  the solver's own table has no model for a mnemonic the unit spells
  (the branch mnemonics, `div`, the packed float operations, `sbb`).
  It verifies that nothing but T1, T2 and T3 happened: the rule-R map
  is injective and every pinned family is a fixed point; every own
  stack address was placed by the one affine map; every literal is
  loaded into a vehicle no lineage holds and consumed on the next
  line; the loads are one line per input lineage from its own block;
  no core line names an input block or the result block; every `ret`
  is immediately preceded by the result store.

## 4.3 The evidence class of each route, stated rather than assumed

- The solver routes are solver analysis over a lifted model — proof
  about the MODEL, which is the lifter's testimony.
- T1, T2 and the block checks are FORCED BY CONSTRUCTION over
  artifacts this lap built.
- T3 additionally rests on `mov` leaving the flags alone, which is
  human interpretation of stated design — the weakest class. That is
  precisely why §5 assembles the texts and §6 runs them.

---

# 5. The texts assemble

```
$ /tmp/reconnect_venv/bin/python3 canon36_assemble.py
offered 2669  assembled 2578  failed 91
```

- **All 1,752 original-population texts and all 9 interpreter texts
  assemble.** Every one of the 91 failures is in the regenerated
  population, and all 91 have one cause: a regenerated unit's ship
  text carries objdump's SYMBOLIC branch targets
  (`jmp c <op_400+0xc>`), which is an extraction notation and not
  assemblable. That is a property of that population's extraction, not
  of the form.
- The regenerated population is SAMPLED and named as sampled: a fixed
  stride of 30 over the whole population, 908 of 27,223, recorded in
  the artifact's `meta`.
- Batching, the per-unit re-run on a failing batch, the reading-
  annotation strip, the rip-relative constant pool and the local-label
  scheme are `canon35_assemble.py`'s, IMPORTED rather than copied, so
  they cannot drift.

---

# 6. The texts run

```
$ /tmp/reconnect_venv/bin/python3 canon36_realrun.py
eligible 960  sampled 90
pairs 17640 differing 0
```

- Each sampled unit is called through a wrapper that does exactly what
  the arrival contract says a caller does:

```
    w_u_<unit>:
        push %r15                 %r15 is callee-saved
        sub  $0x408,%rsp          reserve the region
        mov  %rsp,%r15            the ruled base
        mov  %rdi,0x0(%r15)       argument 1 into input block 0
        mov  %rsi,0x8(%r15)       argument 2 into input block 1
        movabs $<literal>,%rax    one pair of lines per materialized
        mov  %rax,0x40(%r15)      literal, into its constant block
        call u_<unit>
        mov  0x200(%r15),%rax     the answer, read from the RESULT
                                  BLOCK
        add  $0x408,%rsp
        pop  %r15
        ret
```

- The original text is emitted beside it and called with the ordinary
  register contract. Over 14 integer values (0, 1, 2, 3, 7, 20, 255,
  4096, the four sign boundaries at 32 and 64 bits, and the two
  all-ones patterns), every ordered pair: **17,640 comparisons, zero
  differences.**
- **What is excluded, and why, each named:** a vector arrival (596 —
  this harness passes integers), a block-list text (92), a
  rip-relative constant (44 — this harness carries no pool), a divide
  (48 — the sweep includes a zero divisor and would trap the process),
  a unit whose answer is an address in its own region (12 — its answer
  is an address in THIS harness's region and the original's is an
  address in the original's frame, so the two are not comparable here;
  those twelve are proved by the gate under the binding instead), and
  the 27 with no region text.

---

# 7. The counts, per population

## 7.1 The original corpus — 1,779 compiled units

```
$ for L in c cpp go rust swift; do tail -1 /tmp/c36_$L.log; done
c       610 units  {"REGION_TEXT_PROVED": 610}
cpp     770 units  {"REFUSED": 2, "REGION_TEXT_PROVED": 768}
go      107 units  {"REFUSED": 6, "REGION_TEXT_PROVED": 101}
rust    125 units  {"REFUSED": 2, "REGION_TEXT_PROVED": 123}
swift   167 units  {"REFUSED": 17, "REGION_TEXT_PROVED": 150}
```

- 610 + 770 + 107 + 125 + 167 = 1,779, which is the corpus.
- **proved 1,752 · undecided 0 · disproved 0 · refused 27.**
- Every refusal, by cause, with its members named:

```
 23  no text — no canonical text exists for this unit in any
     generation, so there is nothing to render
       go/op_30 go/op_31 go/op_32 go/op_33 go/op_34 go/op_35
       rust/op_699 rust/op_706
       swift/op_128 swift/op_690 swift/op_691 swift/op_692
       swift/op_696 swift/op_697 swift/op_698 swift/op_702
       swift/op_726 swift/op_727 swift/op_728 swift/op_732
       swift/op_733 swift/op_734 swift/op_738
  4  the core names the region base — this unit's own text uses %r15
     as a VALUE, and the form rules %r15 to be the region's base
       cpp/op_765 cpp/op_770 swift/op_703 swift/op_739
```

- The 23 are the same 23 round 8 refused for the same reason.

## 7.2 The interpreter / JIT population — 11 units

```
$ /tmp/reconnect_venv/bin/python3 canon36_interp.py
interpreter 11 units  {"REFUSED": 2, "REGION_TEXT_PROVED": 9}
```

- **proved 9 · undecided 0 · disproved 0 · refused 2.**
- The two refusals are `ruby/vm_opt_plus` and `ruby/rb_big_plus`, and
  the refusal text is QUOTED from `interp_canon35.json` rather than
  restated: the first has no ship body at all, the second's two
  lineages meet inside callees that are not extracted units. Neither
  is a register-scarcity refusal, and neither is new.
- One cause was fixed at first observation here. Round 7's interpreter
  form seated some operands in memory slots rather than registers, so
  the three php handler units' second operand arrives at
  `-0x8(%rsp)`. Read literally this lap took that for the unit's own
  scratch and placed it in a temp block nothing fills; all three
  disproved. A slot the record's own directory declares to be an
  OPERAND SEAT is now recognised as an INPUT lineage, and the rewrite
  is recorded per unit in `operand_seat_rewrites`.

## 7.3 The regenerated population — 29,288 units

```
$ /tmp/reconnect_venv/bin/python3 canon36_regen.py --status
chunks 326/326  units 29288  {"GATE_DISPROVED": 171,
  "GATE_UNDECIDED": 415, "REFUSED": 1479, "REGION_TEXT_PROVED": 27223}
```

```
c      10010  {"GATE_UNDECIDED": 12, "REFUSED": 594, "REGION_TEXT_PROVED": 9404}
cpp    17070  {"GATE_UNDECIDED": 12, "REFUSED": 885, "REGION_TEXT_PROVED": 16173}
go       483  {"GATE_DISPROVED": 170, "GATE_UNDECIDED": 146, "REGION_TEXT_PROVED": 167}
rust     570  {"GATE_DISPROVED": 1, "GATE_UNDECIDED": 24, "REGION_TEXT_PROVED": 545}
swift   1155  {"GATE_UNDECIDED": 221, "REGION_TEXT_PROVED": 934}
```

- 10,010 + 17,070 + 483 + 570 + 1,155 = 29,288, which is the
  population log_131 extracted.
- **proved 27,223 · undecided 415 · disproved 171 · refused 1,479.**
- Every non-proof by cause, with sightings:

```
REFUSED 1479
  1479  upper-lane dependence — the arrival is a vector value and the
        core reads its register with an operation that is not
        lane-wise, so the answer can depend on the upper lanes, which
        a block's eight bytes do not carry (P2).  Sighting:
        cpp/regen_12934, `pextrw $0x0,%xmm0,%eax`.
        This is a FINDING about those units, not a defect of the
        render: a block holds a VALUE.

UNDECIDED 415, by the mnemonic the checker has no model for
   120  jl    e.g. swift/regen_2543
    70  je    e.g. rust/regen_1067
    38  jae   e.g. swift/regen_2006
    37  js    e.g. c/regen_9931
    34  jb    e.g. swift/regen_2471
    19  jo    e.g. swift/regen_298
    17  sbb   e.g. swift/regen_2561
    15  jge   e.g. swift/regen_2018
   (the remainder are further branch mnemonics in the same shape)
        These units branch, and the structural route cannot rescue
        them here because a regenerated ship text spells its branch
        targets as raw addresses rather than labels, so the result
        store cannot be placed before every return.

DISPROVED 171
   170  the entry contract was SEATED BY THE RECORDED ARITY, and the
        gate refuted the seating.  Sighting: go/regen_124.  This is
        the fallback of section 7.4 doing its job honestly rather
        than a silent wrong answer.
     1  the entry contract was inferred from the unit's own ship
        text.  Sighting: rust/regen_1543.
```

## 7.4 What the regenerated population needed that the others did not

- These units have never been canonicalized: their chunk files carry
  ship mnemonics, anchor mnemonics and a DWARF parameter table, and
  nothing else. So the text rendered is the SHIP text, the entry
  contract is inferred from it, and the ship gate is the admission
  gate.
- Where the read-before-write test names no arrival at all — a wide
  float form whose ship code loads a constant into `%xmm1` and
  tail-jumps into a runtime routine, so no argument register is ever
  read — the arrivals are seated by the RECORDED ARITY of the probe on
  the ordinary System V seats. That is machine-form provenance from
  the generator, never a token. It is a FALLBACK, it is recorded as
  one on every record it touches, and the gate still has to prove it —
  which is why 170 of the 171 disproofs sit exactly there.

---

# 8. Zero regression, in the ruled sense

```
$ /tmp/reconnect_venv/bin/python3 canon36_zero_regression.py
population                                     1779
round8_proved                                  1744
round9_proved                                  1752
distinct_texts                                 {"round8": 606, "round9": 626}
texts_carried_by_more_than_one_language        {"round8": 304, "round9": 267}
round8_texts_that_merge_into_one_round9_text   17
round8_texts_that_split_into_more_than_one     36
units_carrying_both_texts                      1742
units that lost proved status: 2
   swift/op_703   round9=REFUSED
   swift/op_739   round9=REFUSED
units that gained proved status: 10
watched artifacts, git status (empty = all unmodified):
  (no lines)
```

## 8.1 The two units that lost proved status, with their named cause

- `swift/op_703` and `swift/op_739`. Their own canonical text uses
  `%r15` as a value:

```
swift/op_703 : L0:; lea -0x41(%rsi),%r9; cmp $0xffffffffffffff7e,%r9;
               ja L2; jmp L1; L2:; test %rsi,%rsi; js L5; jmp L3; ...
```

  (the `%r15` mention is further into the same block list; the file
  carries the whole text).
- The cause is a property of those two units meeting a property of the
  form: the form rules one register to be the region's base, and these
  two units already spend it. Refusing by name is the correct act; the
  alternative would be to rename their `%r15` away, which is a
  transformation of the computation this lap has no proof for.
- **What would change it, named:** a ruled base that is not a register
  at all — a fixed virtual address range with an absolute base — which
  region36's header already names as the other option the owner offered.
  That is the owner's call, not this lap's.

## 8.2 Ten units GAINED proved status

- Six of them are the address-of units of §3. The other four are units
  round 8 refused because its private-region bias made their core
  differ from the prior core, so its structural route's
  character-identity check could not hold; the region form has no bias
  — it has an affine map — so the question does not arise.

## 8.3 The measurement round 8 could not obtain — the form MERGES

- Round 8 measured **zero merges and 77 splits** and reported the
  universal form as a strict refinement, with the cause named: the
  arrival register was still fixed by the argument's identity, so
  there was no register idiosyncrasy left to remove.
- Round 9 measures **17 merges and 36 splits.** Removing the
  compiler's own choice of scratch register is what did it: two units
  that computed the same thing with different temporaries now render
  identically. The clearest instance is the address-of family, where
  four units that carried no text at all now carry one text between
  them.
- The count of texts carried by more than one language falls from 304
  to 267. That is the splits, not a loss: a text that was shared
  because it was UNDER-specified (it did not say how many arguments
  arrived) now says so, and separates.

## 8.4 The artifacts that had to stay untouched, proved untouched

- `canon36_zero_regression.json` carries the sha256 of all fifteen
  watched artifacts — the five `canon35_universal_*`,
  `dominant_table24/25`, `dom_ops22/23`, `interp_table2`,
  `interp_join2/3`, `union_table2/3`, `interp_canon35` — so a later
  reader can recompute rather than trust.
- `git status --porcelain` over all fifteen returns NO LINES, which is
  the check the standing rule requires (check the VCS before ruling a
  write-claim). **New files only, throughout. Round 8's
  `canon35_universal_*` stays on disk as the superseded record.**

---

# 9. The causes fixed at first observation

Each was found by measurement, named, and fixed in the general
mechanism rather than patched per unit.

1. **The shift pin never fired.** `mnemonic.rstrip("bwlq")` strips
   EVERY trailing character in that set, so `shl` became `sh` and no
   variable shift ever pinned `%rcx`. 43 units refused with
   `shl count operand '%sil' is neither %cl nor an immediate`.
   Replaced with `size_stem`, which removes at most one suffix and
   only when the stem is known.
2. **The result lineage took a stale contract.** 90 units disproved
   because a recorded contract said the answer was an rax-family value
   while the unit's own ship code writes `%xmm0` (`c/op_105`). The
   result lineage now takes the GROUND-TRUTH answer home read off the
   unit's own ship text.
3. **The recorded contract named an argument register the text never
   reads.** 52 units disproved; `c/op_300`'s contract says its second
   argument arrives in `%rdi`, its text reads `%rsi` and never
   mentions `%rdi`. The TEXT now outranks the recorded contract, and
   the disagreement is recorded per unit in
   `entry_contract_reconciled` rather than smoothed over.
4. **The move-erased identity.** 6 rust units whose canonical text is
   exactly `ret`: the answer IS the arriving value, because the move
   that parked it was erased by substitution. Now detected — no core
   line touches the result lineage's register — and the store reads
   the first input's vehicle. The register FILE is not required to
   match: `rust/op_39`'s float arrives in `%xmm0` and its recorded
   answer home is an rax-family register, and the eight bytes are the
   same eight bytes.
5. **The result-touched scan asked the wrong question.** It scanned
   the RENAMED core for the result family, which after rule R is
   spelled as its vehicle. 139 units disproved (`c/op_13`). Now
   scanned on the pre-rename core.
6. **Only two arrivals per register file were ever considered.** A
   unit taking a wide value in a REGISTER PAIR (an `__int128` in
   `%rdi`+`%rsi`+`%rdx`) had an argument nothing loaded. 870
   regenerated units disproved (`c/regen_22674`). The arrival sequence
   is now the full System V one, `rdi rsi rdx rcx r8 r9` and
   `xmm0..xmm7`, with designations `a` through `h`.
7. **A bare `(%rsp)` was refused as unplaceable.** It is displacement
   zero and the affine map places it exactly like any other. 2,185
   regenerated units spell it.
8. **The result block's upper bytes were stale for a sub-64-bit
   answer.** Found by REAL EXECUTION, not by the solver: `go/op_2`
   returned `0x7fffffffffffffff` from the block where its own text
   returns `0xffffffff` (42 differing of 17,640). The result block now
   holds the answer ZERO-EXTENDED to eight bytes, by one rule for
   every unit. Without it the block was not the answer's home, which
   is the whole claim of the form.
9. **The answer home fell back to the arrival too eagerly.** Where a
   unit's ship code names no answer home this checker can read, the
   unit's own CANONICAL text is consulted before the arrival is
   assumed — otherwise the gate's question became vacuous
   (`go/op_2` again: its ship code returns in a place the checker
   cannot name, while its canonical text says plainly `mov %edi,%eax`,
   so the answer is 32 bits, not 64).
10. **The real-run harness compared all 64 bits of an answer declared
    narrower.** 960 differing pairs, every one an 8- or 32-bit answer
    (`cpp/op_473`). The harness now masks both sides to the answer's
    own declared width. This one was the harness's fault, not the
    form's, and is recorded as such.
11. **A divide traps the harness.** The sweep includes a zero divisor,
    so the first sample aborted with SIGFPE. Divides are excluded from
    the real-run sample by name and proved by the gate instead.

---

# 10. The guards

## 10.1 Every new artifact, checked

```
PASS canon36_universal_c.json     -- exempt: top-level meta declares role 'generator provenance'
PASS canon36_universal_cpp.json   -- exempt: …
PASS canon36_universal_go.json    -- exempt: …
PASS canon36_universal_rust.json  -- exempt: …
PASS canon36_universal_swift.json -- exempt: …
PASS canon36_interp.json          -- exempt: …
PASS canon36_assemble.json        -- exempt: …
PASS canon36_realrun.json         -- exempt: …
PASS canon36_regen_state.json     -- no operator token in any key, grouping, pairing or row structure
PASS canon36_regen_store/op_units2_c_c0000.json -- exempt: …
```

## 10.2 The exemption is not load-bearing — tested, not asserted

Each file was copied with its `meta.role` declaration REMOVED and
re-checked, so the checker had no exemption to grant:

```
PASS canon36_assemble.json        -- no operator token in any key, grouping, pairing or row structure
PASS canon36_interp.json          -- no operator token in any key, grouping, pairing or row structure
PASS canon36_realrun.json         -- no operator token in any key, grouping, pairing or row structure
PASS canon36_universal_c.json     -- no operator token in any key, grouping, pairing or row structure
PASS canon36_universal_cpp.json   -- no operator token in any key, grouping, pairing or row structure
PASS canon36_universal_go.json    -- no operator token in any key, grouping, pairing or row structure
PASS canon36_universal_rust.json  -- no operator token in any key, grouping, pairing or row structure
PASS canon36_universal_swift.json -- no operator token in any key, grouping, pairing or row structure
PASS op_units2_c_c0000.json       -- no operator token in any key, grouping, pairing or row structure
PASS op_units2_cpp_c0100.json     -- no operator token in any key, grouping, pairing or row structure
```

- **All ten pass with NO exemption claimed.** The operator token
  appears in those files exactly once per unit, as the `operator`
  display label, and is read by nothing.
- Selection and grouping throughout this lap are machine-form: the
  corpus files `canon31_units_<lang>.json`, the chunk files on disk,
  the recorded entry contract, the recorded branch shape, the recorded
  arity. No token participates anywhere.

---

# 11. Complete file inventory

## 11.1 Programs written (6)

| file | bytes | what it is |
|---|---|---|
| `Research/op_pipeline/region36.py` | 28,521 | THE FORM: the ruled base, the six allocation kinds, the fixed layout, the affine own-address map, rule R. The definition lives in its module header. |
| `Research/op_pipeline/canon36_universal.py` | 61,841 | the renderer, the three gate routes and the driver for the original population |
| `Research/op_pipeline/canon36_regen.py` | 13,448 | the regenerated population, per-chunk with a resume file |
| `Research/op_pipeline/canon36_interp.py` | 11,164 | the interpreter / JIT population |
| `Research/op_pipeline/canon36_assemble.py` | 7,178 | `as` + `objdump` over every region text |
| `Research/op_pipeline/canon36_realrun.py` | 12,057 | the region harness; real execution through the blocks |
| `Research/op_pipeline/canon36_zero_regression.py` | 7,280 | the standing counts, the merge measurement, the watched sha256 set |

## 11.2 Artifacts written (10 files + one store of 326)

| file | bytes |
|---|---|
| `Research/op_pipeline/canon36_universal_c.json` | 4,304,200 |
| `Research/op_pipeline/canon36_universal_cpp.json` | 5,788,048 |
| `Research/op_pipeline/canon36_universal_go.json` | 555,412 |
| `Research/op_pipeline/canon36_universal_rust.json` | 708,756 |
| `Research/op_pipeline/canon36_universal_swift.json` | 1,219,585 |
| `Research/op_pipeline/canon36_interp.json` | 40,050 |
| `Research/op_pipeline/canon36_assemble.json` | 548,924 |
| `Research/op_pipeline/canon36_realrun.json` | 2,156 |
| `Research/op_pipeline/canon36_zero_regression.json` | 2,290 |
| `Research/op_pipeline/canon36_regen_state.json` | 35,881 |
| `Research/op_pipeline/canon36_regen_store/` | 326 files, 110 MB — one per chunk, named `op_units2_<lang>_c<NNNN>.json` |

## 11.3 Caches created (3)

- `Research/op_pipeline/__pycache__/region36.cpython-313.pyc`
- `Research/op_pipeline/__pycache__/canon36_universal.cpython-313.pyc`
- `Research/op_pipeline/__pycache__/canon35_assemble.cpython-313.pyc`

Named because the rule says to name EVERY file created including
caches. The fourth `__pycache__` entry with today's later timestamp,
`legality_filter2.cpython-313.pyc`, belongs to the concurrently
running task-45 work, not to this lap.

## 11.4 Work directories outside the repo (4)

- `/tmp/canon36_assemble_work/` — the batch `.s`/`.o` pairs and the
  per-unit re-runs
- `/tmp/canon36_realrun_work/` — `units.s`, `driver.c`, `harness`
- `/tmp/c36_strip/` — 10 role-stripped copies for the §10.2 test
- `/tmp/c36_c.log`, `/tmp/c36_cpp.log`, `/tmp/c36_go.log`,
  `/tmp/c36_rust.log`, `/tmp/c36_swift.log`, `/tmp/c36_regen.log` —
  the per-population run logs

## 11.5 Nothing was overwritten

New files only. §8.4 proves the fifteen artifacts that had to stay
untouched are unmodified in the VCS.

---

# 12. Resume state

## 12.1 The regenerated population is COMPLETE, and its resume file
## remains the mechanism

```
$ /tmp/reconnect_venv/bin/python3 canon36_regen.py --status
chunks 326/326  units 29288  {"GATE_DISPROVED": 171,
  "GATE_UNDECIDED": 415, "REFUSED": 1479, "REGION_TEXT_PROVED": 27223}
```

- `canon36_regen_state.json` records, per chunk file, `done` with its
  tally. `--run` skips every chunk already recorded, so an interrupted
  lap resumes at a chunk boundary and never redoes finished work. All
  326 chunks are recorded; there is nothing outstanding.
- The per-chunk results are separate files in
  `canon36_regen_store/`, so no single artifact has to be rewritten as
  the population grows.

## 12.2 The original and interpreter populations

- `canon36_universal_<lang>.json` is written every 25 units and a
  re-run skips units already present, so those five are resumable the
  same way. All five are complete (610 / 770 / 107 / 125 / 167).
- `canon36_interp.json` is written in one act over 11 units and is
  complete.

## 12.3 Nothing is left running

- No background process of this lap is outstanding. The
  `trickle-runner` container was NOT touched — this lap reads
  `trickle_store/` from disk and never enters the container.

---

# 13. Two lists

## 13.1 Decided, recorded for audit

- The ruled base is the REGISTER `%r15`, not an absolute address
  range. Reason: it keeps the form runnable with no prologue and no
  absolute relocation, and only 4 of 1,779 units spend `%r15`
  themselves. The other option the owner offered — a fixed virtual address
  range — is named in region36's header as the alternative.
- The region sits BELOW the caller's stack pointer, so the
  own-address block ends exactly where a unit's own stack scratch used
  to begin. That is what makes an address-of unit's answer the same
  byte.
- Rule R renames the unit's OWN temporaries as well as its arrivals.
  That is what produced the 17 merges of §8.3.
- Temp and guard-outcome lineages are ALLOCATED and DIRECTORIED but
  not materialized (§2.7), recorded as a stated limit.
- The regenerated population's arity fallback is a fallback, recorded
  per record, and the gate refutes it where it is wrong.

## 13.2 Awaiting the owner

- **The four region-base units.** `cpp/op_765`, `cpp/op_770`,
  `swift/op_703`, `swift/op_739` spend `%r15` themselves. An absolute
  virtual address range instead of a base register would take them.
- **Whether temp and guard-outcome lineages should be MATERIALIZED.**
  the owner's statement says "everything is loading from memory and storing
  in memory". This lap materializes inputs, the result, literals and
  own stack addresses. Spilling every register-resident intermediate
  to its temp block would complete the sentence, and it rewrites the
  computation rather than its plumbing — so it is a ruling, not an
  implementation choice.
- **The 1,479 upper-lane refusals** in the regenerated population.
  Those units read the upper lanes of a vector register, which a
  block's eight bytes do not carry. Either the input block for a
  vector lineage becomes sixteen bytes, or those units are a different
  arrival kind. Both are ontology.
