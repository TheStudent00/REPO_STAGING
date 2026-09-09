# log_119 — TASK 32: the interpreter table, the join, and the union view

**Role:** Claude Code implementer, TASK 32 of
`log_115_claude_code_task_briefs_round6.md`. Date: 2026-09-01. No
sub-agents were used — every artifact below was written and run in
this session with `/tmp/reconnect_venv/bin/python3`.

**Evidence class is stated per claim.** Every "I verified X" sentence
pastes the command and its output.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in \"which pairs
get compared\", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as \"same-operator pairs\"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

---

# 1. What happened, at the top level

## 1.1 The three views exist, and they are three files

- **The interpreter table is built.** `interp_table1.json` holds 7
  classes over 8 units, in `dominant_table24.json`'s own row shape
  plus the representation column. Population: the 11 interpreter/JIT
  units on record (cpython 1, ruby 4, php 4, java 2); 8 of them now
  carry canonical text, 3 do not and each says why.
- **The join table is built.** `interp_join1.json` holds 22 rows
  relating an interpreter class to a compiled class: 18 PROVED_EQUAL,
  4 TYPE_INCOMPARABLE. Nothing is forced; the four carry a proof RUN
  as an OBSERVATION that forms no relation.
- **The union view is built.** `union_table1.json` holds all three
  views navigable from one index of 1,653 units, and 2 union
  components formed by proved relations only.
- **`dominant_table24.json` and `dom_ops22.json` were not written.**
  Checked against the version control system, not against the files —
  §6.2.

## 1.2 The counts, with their populations named

- **6 of the 9 refused interpreter units now carry canonical text.**
  The nine are the ones log_107 (TASK 21) refused: java unit 2, ruby's
  4 handlers, php's 4 handlers. Before this lap, 0 of those 9 had
  canonical text. The 3 that still refuse are `ruby/vm_opt_plus`,
  `ruby/rb_big_plus` and `php/add_function`, each with a mechanical
  reason quoted verbatim in §2.4.
- **Three php handlers were proved equal to 8 compiled units each**,
  out of 88 candidates, by a solver — a result that did not exist
  before this lap, and one that TASK 27's prover reported as 267
  consecutive UNDECIDEDs. The cause was our own simulator, not php;
  §4.3.
- **The compiled corpus is unchanged: 1,635 recorded / 1,622 honest /
  13 withdrawn as a separate population**, recomputed from disk in
  §6.1. log_117's 5 and log_118's 36 proofs are NOT advanced — the owner's
  call, still open.

## 1.3 The one number that is smaller than it looks, said first

`java/op_2`'s canonical text exists but its join row is
TYPE_INCOMPARABLE and its observation proved nothing, against 50
candidates. That is not a finding about java. The prover's own words:

```
this file's reused integer simulator (canon8_behaviour_check.Sim8)
has no model for a mnemonic in this pair's text -- an instrument
limit, not an unknowable-input case: mnemonic 'cltd' has no symbolic
model in this checker
```

No simulator on this line models the divide family. That is named
here as a cause with a status, not carried as a mystery.

---

# 2. Part (a): the nine, through the canonicalizer

## 2.1 The names, glossed before use

- **A designated location** is a standardized virtual stack slot named
  `S0`, `S1`, … — a designation, exactly as `a` is a designation and
  `%rdi` is the register it maps to. Slot `i` sits at `-8*(i+1)(%rsp)`.
  Built by TASK 30 (`designated_memory.py`, log_118 §2).
- **A seat** is where one traced value arrives. A seat is either a
  designated register (`%rdi` for `a`, `%rsi` for `b`) or a designated
  location.
- **The carve** is the arrival/computation split: arrival is the
  maximal prefix of each lineage that touches one lineage only,
  computation begins at the first instruction whose super-chain
  includes both lineages. Built by TASK 27 (`lineage_carve.py`).
- **`+` and `/`** are the operator tokens that appear on these units.
  They appear in this log only as display labels on units, never as a
  key, a grouping, or a reason two things were compared.

## 2.2 What was actually blocking six of the nine

TASK 27's prover refuses any computation core that reads an operand
out of memory, in its own words
(`prove_interp_computation.py`, quoted from disk):

```
        return None, ("the core reads or writes MEMORY (%r): placing that "
                      "value in a designated register would be re-plumbing "
                      "the unit, not renaming it, so no canonical text is "
                      "produced and no proof is attempted" % line)
```

That refusal was correct **while memory was anonymous overflow**.
the owner's 2026-09-01 ruling removes its ground: memory is designated, like
registers. So an operand arriving in memory is not re-plumbed into a
register — it is given its designated location, and the entry contract
records the seat. That single change is what this lap's part (a) is.

## 2.3 The php handler, with values in motion

`php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER` is
php's specialised executor handler for an addition it has already
proved cannot overflow. Its whole ship body is ten instructions. Take
`a = 5` and `b = 7`, sitting in the VM stack at the slots the
instruction word names.

### 2.3.1 What the ship build does with those values

```
  2257ba: movslq 0x8(%r15),%rcx     %rcx = 0x40    a's slot offset
  2257be: movslq 0xc(%r15),%rax     %rax = 0x50    b's slot offset
  2257c2: add    $0x20,%r15                       frame advance
  2257c6: movslq -0x10(%r15),%rdx   %rdx = 0x60    answer slot offset
  2257ca: mov    (%r14,%rax,1),%rax %rax = 7       b's VALUE loaded
  2257ce: add    (%r14,%rcx,1),%rax %rax = 7 + 5   <- the confluence
  2257d2: mov    %rax,(%r14,%rdx,1) answer 12 stored
  2257d6: movl   $0x4,0x8(%r14,%rdx,1)             the result type tag
  2257df: ret
```

- The carve's boundary is `add (%r14,%rcx,1),%rax` at `0x2257ce`, and
  the carve's own record names which place carries which lineage:
  `{"rax": ["slot_lineage_2"], "rcx": ["slot_lineage_1"]}`.
- So `a` (lineage 1) is read THROUGH MEMORY at the boundary — `%rcx`
  holds an offset, not the value — while `b` (lineage 2) is already a
  value in `%rax`.

### 2.3.2 What the seat assignment does with them

- `b` is read as a plain register operand, so its seat is the
  designated register `%rsi`. Under the values above, `%rsi = 7`.
- `a` is read through a memory operand, so its seat is the next
  designated location in first-needed order — `S0`, at `-0x8(%rsp)`.
  Under the values above, `memory[-0x8(%rsp)] = 5`.
- The answer goes to `%rax`.

### 2.3.3 The canonical text this produces, and it runs

```
    mov %rsi,%rax          %rax = 7          b into the answer seat
    mov -0x8(%rsp),%r11    %r11 = 5          S0 reloaded, one instruction
    add %r11,%rax          %rax = 12
    ret
```

- `%r11` is the reserved general reload register from TASK 30's
  scheme: it is held out of the value pools, so nothing live can
  occupy it, and it is dead the instant the `add` has read it.
- `-0x8(%rsp)` is inside the System V 128-byte red zone, so the text
  is runnable with no prologue — the property TASK 30 built the slot
  series to preserve.
- The directory the record carries for this unit is
  `{"S0": {"slot_index": 0, "offset": -8, "text": "-0x8(%rsp)",
  "file": "general", "holds": "operand_1"}}`.

### 2.3.4 Nothing was re-plumbed

The point of the whole exercise, stated against the refusal it
replaces: `a` did not arrive in a register in php's handler and it
does not arrive in a register in the canonical text either. It arrived
in memory and it keeps a memory seat. What changed is that the memory
seat now has a NAME and a directory entry, so two units can be
compared through it.

## 2.4 The three that still refuse, verbatim

- **`php/add_function`** — the generic routine, which dispatches on
  the zval type tags before it ever adds:

  > the core's last instruction 'cmp $0x44,%al' leaves its result in
  > the FLAGS, not in a register: the unit never materialises a value
  > here, and materialising one so an answer register could be named
  > would be inventing computation, not canonicalising it

  Reading: the carve's confluence for this handler lands on the TYPE
  DISPATCH (`or 0x8(%rdx),%al` combines the two operands' type-tag
  bytes and `cmp $0x44,%al` asks whether both are long), not on an
  arithmetic. That is a true fact about where this routine's two
  lineages first meet, and it is not a failure of the renderer.

- **`ruby/vm_opt_plus`** —

  > no instruction in this unit reads both lineages: the lineages
  > leave this unit through a call, so the confluence is inside a
  > callee, not here. Call instructions reached: call 24c993
  > \<FIXNUM_2_P\>; call 2437a5 \<rb_fix_plus_fix\>; call 24c9c7
  > \<FLONUM_2_P\>; … | no slice exists for this symbol at this build:
  > the symbol's label line is absent from the dump — the build has no
  > body for this symbol

- **`ruby/rb_big_plus`** —

  > no instruction in this unit reads both lineages: the lineages
  > leave this unit through a call … call 3cf3da \<bigsub_int\>; call
  > 3cf69f \<bigadd_int\> …

- **Task 30's machinery does not reach any of the three, and the
  record says so rather than implying it might.** Designated memory
  answers where an operand LIVES; these two ruby refusals are that the
  two lineages never meet inside the unit at all.

## 2.5 Java unit 2, carved for the first time

### 2.5.1 Why the old refusal stood

log_107's refusal was `jvm_canon.py`'s own: "the residual core
branches; this file handles one straight run only (at 'je
0x7f99346a9b46')". A straight-line stripper cannot carve a unit with
guards in it.

### 2.5.2 The carve, with values in motion

`interp_canon34.py` walks the unit's own recorded objdump along the
fall-through normal path, seeding the two lineages from the JVM's own
printed parameter comments (`# parm0: rsi`, `# parm1: rdx` — the
tool's own testimony, marked as such on the record). Take `a = 20`,
`b = 3`.

```
  ...b1a: mov  %edx,%r11d      %r11d = 3     b copied
  ...b1d: test %edx,%edx                     GUARD: divisor zero?
  ...b1f: je   ...b46                        -> not taken (b = 3)
  ...b21: mov  %esi,%eax       %eax  = 20    a into the dividend seat
  ...b23: cmp  $0x80000000,%eax              GUARD: a == INT_MIN?
  ...b28: jne  ...b32                        -> taken (a = 20)
  ...b32: cltd                 %edx:%eax = 20 sign-extended
  ...b33: idiv %r11d           %eax = 6      <- the confluence
```

- The confluence is `idiv %r11d`. It reads BOTH lineages, and one of
  those reads is INVISIBLE in the instruction text: the dividend is
  the hardware-pinned `%edx:%eax` pair. The walk counts that implicit
  read, which is the only reason the boundary is found at all.
- `cltd` is kept, not erased. It is not a move: the hardware splits
  one operation across the pair `cltd` + `idiv`, which is
  AgentMemory's own example of an alpha travelling as one component.

### 2.5.3 The canonical text

```
    mov %edi,%eax    a into the answer/dividend seat
    cltd
    idiv %esi        b in its designated register
    ret
```

Both operands arrive in registers, so this unit needs no designated
location and its directory is empty.

### 2.5.4 The finding that fell out, from a second route

The walk recorded four conditional branches on the normal path. Every
one of them is a guard row ALREADY on record in
`exception_families3.json`, found there by a completely different
route (the JVM's own annotations, TASK 19):

| branch measured this lap | family already on record |
|---|---|
| `cmpl $0x0,0x20(%r15)` / `jne` | EF0025, `call-out-and-return`, nmethod-entry barrier |
| `test %edx,%edx` / `je` | EF0040, `deopt-continue-elsewhere`, zero-divisor check |
| `cmp $0x80000000,%eax` / `jne` + `cmp $0xffffffff,%r11d` / `je` | EF0038, `branch-around-in-place`, most-negative-over-minus-one check |

- **Two independent grounds agreeing** is the standing pattern of the
  evidence doctrine, and here they agree with nothing left over: no
  branch this lap measured is missing from the guard record, and no
  java guard row in the record is missing from this walk.
- Evidence class: **forced by construction** — the branch list is
  derived from the unit's own recorded bytes by a deterministic walk;
  the family list is read from `exception_families3.json` unchanged.

---

# 3. Part (b): the interpreter table

## 3.1 The class key is four machine facts

`type_pair`, `result_type`, `representation`, `canonical_text`. The
first two come from `dwarf_typed_key.json` — the compiler's own
`DW_AT_type` chain over the handler's formal parameters, which log_111
established. The third is the recorded arrival representation. The
fourth is the unit's canonical runnable text. No token participates.

## 3.2 The seven rows, as the generator printed them

```
$ /tmp/reconnect_venv/bin/python3 build_interp_table1.py
IC0001  type_pair=PyLongObject*,PyLongObject*    result=PyLongObject*      rep=typed-pointer(PyLongObject*)              mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
        cpython/long_add_fastpath
IC0002  type_pair=None                           result=None               rep=plain                                     mov %rdi,%rax; and $-1,%eax; mov %rsi,%r10; and $-1,%r10d; add %r10d,%eax; ret
        java/op_1
IC0003  type_pair=None                           result=None               rep=plain                                     mov %edi,%eax; cltd; idiv %esi; ret
        java/op_2
IC0004  type_pair=None                           result=None               rep=typed-pointer(zval*)                      mov %rsi,%rax; mov -0x8(%rsp),%r11; add %r11,%rax; ret
        php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER
IC0005  type_pair=None                           result=None               rep=typed-pointer(zval*)                      mov %rdi,%rax; mov -0x8(%rsp),%r11; add %r11,%rax; ret
        php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER
        php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER
IC0006  type_pair=VALUE,VALUE                    result=VALUE              rep=tagged-value(Fixnum, 2n+1 encoding)       mov %rsi,%rax; add %rdi,%rax; ret
        ruby/rb_fix_plus
IC0007  type_pair=VALUE,VALUE                    result=VALUE              rep=tagged-value(Fixnum, 2n+1 encoding)       mov %rdi,%rax; add %rsi,%rax; ret
        ruby/rb_int_plus
no class: ['ruby/vm_opt_plus', 'ruby/rb_big_plus', 'php/add_function']
summary: {'class_count': 7, 'member_count': 8, 'mode_row_count': 9}
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_table1.json -- no operator token in any key, grouping, pairing or row structure
```

## 3.3 Three things worth reading off those rows

- **IC0005 has two members.** Two php handlers — the generic
  specialisation and the LONG specialisation — produce
  character-identical canonical text, so they are ONE class by text
  identity, with no proof needed. That is level-1 matching working on
  interpreter units for the first time.
- **IC0006 and IC0007 differ only in which operand reaches `%rax`
  first.** `mov %rsi,%rax; add %rdi,%rax` against
  `mov %rdi,%rax; add %rsi,%rax`. Under AgentMemory's ruling this is
  canonicalization not yet finished on those units, not evidence of a
  difference — and the join's interpreter-to-interpreter edge proves
  them equal (§4.5).
- **`type_pair` is null on four rows and that is a measurement.** php's
  specialised handlers declare zero formal parameters (their operands
  reach them through the `execute_data` frame) and a JIT nmethod has
  no ELF file and therefore no DWARF at all. A null key merges with
  nothing, which is the correct behaviour and is why IC0003, IC0004
  and IC0005 stay separate despite three of them sharing a `null`.

## 3.4 The mode rows

`interp_table1.json` carries 9 mode rows, read from `guards5.json` —
the guard record of record — filtered by each row's own `language`
field to the interpreter/JIT languages, and cross-referenced to
`exception_families3.json` by family membership. The growing family
your brief named is among them:

- `cpython/long_add_fastpath`, condition "the operands are not both
  compact", response `grows`, detection
  `branch-to-alternate-computation`, family **EF0039** — the first
  recorded instance of both that response and that detection route.
- 8 java rows: 3 on `java/op_1` and 5 on `java/op_2`. Their families,
  as the artifact records them per unit: `java/op_1` in EF0020,
  EF0025, EF0026; `java/op_2` in those three plus EF0038 and EF0040.
  1 + 8 = 9, which is the mode-row count. ruby and php carry no guard
  rows in the record at all.

Nothing was added to `guards5.json` or `exception_families3.json`.
This lap only reads them; §6.2 proves it against the version control
system.

---

# 4. Part (c): the join table

## 4.1 The relation values, and what each one costs to claim

- `PROVED_EQUAL` — a solver proved the two canonical texts equal for
  every value of every seat either text reads before writing.
- `UNDECIDED` — the proof was attempted and neither proved nor
  refuted, or the simulator refused the text by name.
- `TYPE_INCOMPARABLE` — the interpreter side has no measured declared
  operand type to license the comparison. **No relation is recorded.**
- `DIFFERS_BY_DESIGN` — same answer, different recorded guard.

## 4.2 The rows already on record, read and not re-derived

18 of the 22 rows are proofs TASK 21 and TASK 27 established. They are
read out of their own artifacts read-only and carried with their own
provenance: cpython/long_add_fastpath to `c/op_109`; java/op_1 to
`c/op_102`; ruby/rb_fix_plus and ruby/rb_int_plus to 8 compiled units
each.

## 4.3 The cause fixed at first observation

### 4.3.1 What the first run said

The join's first run put php's three canonicalised handlers to
`cross_unit_prover.prove_pair` and got UNDECIDED on every one of 267
candidate pairs. The prover's own words, quoted from the run:

```
this file's reused integer simulator (canon8_behaviour_check.Sim8)
has no model for a mnemonic in this pair's text -- an instrument
limit, not an unknowable-input case: operand '-0x8(%rsp)' is neither
an immediate nor a plain register
```

### 4.3.2 Why that is not a fact about php

It is the simulator predating the owner's designated-memory ruling by one
day. TASK 30 already built the simulator that models a designated
location — `canon33_gate.Sim33`, whose own docstring calls the
addition "the designated-location store". Carrying the UNDECIDED as a
finding would have been reporting a known mechanical gap, which is the
process failure AgentMemory names.

### 4.3.3 The fix, and the soundness argument it rests on

`interp_join_prover33.py` (new file; `cross_unit_prover.py` is
imported for its population and NOT edited) proves a pair through
Sim33, with one addition that is the whole argument:

- An interpreter unit whose `a` arrives in `S0` and a compiled unit
  whose `a` arrives in `%rdi` must be asked whether they compute the
  same thing FROM THE SAME INPUTS.
- So the simulator's seed for slot `-0x8(%rsp)` is set to the SAME z3
  symbol the compiled side's `%rdi` seed uses. That is the entry
  contract's own rule — "value-here + needed-there produces the
  adapter by rule" — applied to the seed dict instead of to emitted
  text.
- Without the binding the proof would be vacuously undecidable. With
  it, the proof is the real question.

### 4.3.4 What it then proved

```
php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER {'proved': 8, 'disproved': 74, 'undecided': 6, 'refused': 0} of 88 ['c/op_109', 'c/op_116', 'cpp/op_109', 'cpp/op_116', 'go/op_319', 'go/op_326', 'rust/op_541', 'rust/op_548']
php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER            {'proved': 8, 'disproved': 74, 'undecided': 6, 'refused': 0} of 88 ['c/op_109', 'c/op_116', 'cpp/op_109', 'cpp/op_116', 'go/op_319', 'go/op_326', 'rust/op_541', 'rust/op_548']
php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                 {'proved': 8, 'disproved': 74, 'undecided': 6, 'refused': 0} of 88 ['c/op_109', 'c/op_116', 'cpp/op_109', 'cpp/op_116', 'go/op_319', 'go/op_326', 'rust/op_541', 'rust/op_548']
```

The prover's verdict text on each proved pair:

```
z3 proved bit-level equality at 64 bits for every value of every seat
either text reads before writing, with the designated locations bound
to the compiled side's designated registers (12000ms timeout)
```

- **8 of 88, with 74 disproved and 6 undecided — the same shape ruby's
  proofs took** (also 8 of 88). The 74 disproved are units in the same
  class key computing something else; the prover separating them is
  the machinery working.
- Evidence class: **forced by construction** (solver unsat over a
  seed binding derived from the units' own recorded seats).

## 4.4 And it still forms no relation, deliberately

All three php rows are recorded `TYPE_INCOMPARABLE`, with the proof
carried as an OBSERVATION and marked `forms_no_edge: true`. The
artifact's own wording:

> an observation is a proof RUN without the type key that would
> license the comparison; the owner's ruling joins the views by PROVED
> RELATIONS, so an observation is recorded and never merged

The refusal that keeps it there is measured, not assumed — the DWARF
read ran against the clean anchor AND the clean ship build and found
zero formal parameters both times (log_113). **This is the one place
in TASK 32 where the evidence is strong enough to tempt a merge and
the rule says do not, so it is stated at the top of its own section
rather than buried.**

## 4.5 The interpreter-to-interpreter edge

```
interp<->interp IC0006 IC0007 PROVED_EQUAL
```

`mov %rsi,%rax; add %rdi,%rax; ret` and
`mov %rdi,%rax; add %rsi,%rax; ret` are proved equal. Candidate
selection was machine form: both rows carry the same DWARF type pair
`VALUE,VALUE` and the same result type, and their texts differ — the
same two conditions `cross_unit_prover` already uses.

## 4.6 The guard join, and its honest zero

Six interpreter exception families were put to the join by CONDITION.
All six came back `UNDECIDED_CONDITION_NOT_COMPARABLE`, and the cause
is named on every row rather than left as a count:

> the compiled families' condition labels are SOLVER-LOCALIZED
> PREDICATES over in0/in1 (core_modes.py's own output, e.g. "in0 ==
> -2147483648 (INT32_MIN) and in1 == -1"), while these interpreter
> families' condition labels are MEASURED ANNOTATIONS in the runtime's
> own words (e.g. "most-negative-over-minus-one check"). The two are
> not one vocabulary, so a string comparison is not a proof either
> way, and none is forced.

- The case this loses is visible and worth naming for the owner: EF0038
  (java, `branch-around-in-place`, most-negative-over-minus-one) and
  EF0021/EF0022 (rust, `panic-call`, `in0 == INT32_MIN and in1 == -1`)
  are, to a reader, the same condition with two different responses —
  a `DIFFERS_BY_DESIGN` row waiting to be formed. It is not formed
  here because forming it would mean a person deciding two label
  strings mean the same thing, which is exactly the judgement this
  line removes from the machinery.
- Closing it needs the interpreter guard conditions put through the
  same solver localisation the compiled ones went through. Named here,
  not attempted this lap.

---

# 5. Part (d): the union view

## 5.1 What it is, and what it deliberately is not

`union_table1.json` is a NAVIGATION object over three views. It copies
no table and changes no table. Its edge rule is one line: a
PROVED_EQUAL relation forms an edge; an observation, an UNDECIDED and
a TYPE_INCOMPARABLE form none.

```
$ /tmp/reconnect_venv/bin/python3 build_union_table1.py
U0001  interpreter=['IC0002']  compiled=['C0505']  edges=1
U0002  interpreter=['IC0001', 'IC0006', 'IC0007']  compiled=['C0700', 'C0889']  edges=18
summary: {'compiled_classes': 901, 'interpreter_classes': 7, 'union_components': 2, 'proved_edges': 19, 'units_indexed': 1653}
```

## 5.2 Component U0002, read out in full

| view | class | key | canonical text |
|---|---|---|---|
| compiled | C0700 | `i64,i64` → `i64` | `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret` |
| compiled | C0889 | `u64,u64` → `u64` | `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret` |
| interpreter | IC0001 | `PyLongObject*,PyLongObject*` → `PyLongObject*`, representation `typed-pointer(PyLongObject*)` | `mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret` |
| interpreter | IC0006 | `VALUE,VALUE` → `VALUE`, representation `tagged-value(Fixnum, 2n+1 encoding)` | `mov %rsi,%rax; add %rdi,%rax; ret` |
| interpreter | IC0007 | `VALUE,VALUE` → `VALUE`, representation `tagged-value(Fixnum, 2n+1 encoding)` | `mov %rdi,%rax; add %rsi,%rax; ret` |

- **Five classes, three of which have different type keys and three of
  which have different representations, all proved to compute one
  thing.** The classes stay five separate objects with their own ids;
  the component names them. That is "nothing merged, nothing
  destroyed" as a data structure rather than as a promise.
- The representation column is what makes the component readable: it
  says, in one line each, that cpython reaches this computation
  through a pointer, ruby through a tagged word, and c/cpp/go/rust
  through plain values — and that after arrival the computation is the
  same one. That is precisely the difference the owner ruled is INFORMATION
  for dominant-operator decisions, kept rather than discarded.
- U0001 is the smaller case: java's 32-bit addition class IC0002 and
  the compiled class C0505, one edge.

## 5.3 Navigation

`unit_index` maps all 1,653 unit ids (1,645 compiled members of the
901 classes plus the 8 interpreter members) to `{view, class_id,
node_id, union_component_id}`, so any unit can be reached from any of
the three views.

---

# 6. Zero regressions

## 6.1 The baseline, recomputed from disk

```
$ /tmp/reconnect_venv/bin/python3 interp_zero_regression.py
wrote ~/Programming/PseudoCoupHQ/Research/op_pipeline/interp_zero_regression.json
recorded converged recomputed from disk: 1635  (baseline 1635, matches: True)
per language: {"c": {"converged": 583, "unchanged": 20}, "cpp": {"converged": 728, "unchanged": 22}, "go": {"converged": 72, "unchanged": 16}, "rust": {"converged": 112, "unchanged": 2}, "swift": {"converged": 140, "unchanged": 10}}
honest standing converged: 1622; withdrawn, separate population: 13
comparison revision: 951400c7fcad09e734529f917463a0701bb2b16e^
dominant_table24.json        identical to before this lap: True
dom_ops22.json               identical to before this lap: True
guards5.json                 identical to before this lap: True
exception_families3.json     identical to before this lap: True
PASS
```

- The population behind 1,635 is the 1,779-unit compiled-five corpus
  (c, cpp, go, rust, swift). 583 + 728 + 72 + 112 + 140 = 1,635.
- 1,622 honest and 13 withdrawn are carried as a SEPARATE population,
  not folded into one number.
- **log_117's 5 sret proofs and log_118's 36 designated-memory proofs
  are NOT advanced by this lap.** Both remain the owner's call.

## 6.2 The write-claim, checked against the version control system

The four tables are compared by sha256 against the content the
repository holds at the commit BEFORE this lap's first artifact
landed, not against a claim about what was opened. The daemon commits
every 30 seconds, so that commit exists and the comparison is real.
All four are identical, as the transcript above shows.

## 6.3 What this lap did NOT do

- It did not open `dominant_table24.json` or `dom_ops22.json` for
  writing, and did not change membership in either.
- It did not add a row to `guards5.json` or a family to
  `exception_families3.json`.
- It did not advance any unit's recorded status.
- It did not edit any existing program. `cross_unit_prover.py`,
  `canon33_gate.py`, `designated_memory.py`, `lineage_carve.py`,
  `canon.py` and `check_no_spelling_keys.py` are imported unmodified.

---

# 7. The spelling guard, without exemption

`check_no_spelling_keys.py` grants a generator-provenance exemption to
a document whose top-level meta declares that role and carries no
top-level grouping field. Every artifact of this lap is
grouping-shaped or pairing-shaped, so `interp_union_guard.py` calls
the checker's own `inventory` and `walk` directly, exemption bypassed:

```
$ /tmp/reconnect_venv/bin/python3 interp_union_guard.py
PASS interp_canon34.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS interp_table1.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS interp_join1.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS union_table1.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS interp_zero_regression.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
ALL 5 ARTIFACTS PASS THE GUARD WITHOUT EXEMPTION
```

Each of the four generators also runs the checker over its own output
and refuses that output on failure — the mechanical-guard requirement,
wired into the program rather than left to a person to remember.

## 7.1 The guard caught this lap's own work, recorded rather than quietly fixed

`build_interp_table1.py`'s first output FAILED:

```
FAIL interp_table1.json -- 1 spelling-keyed place(s)
     $.normal_path_branches_measured_this_lap[0].operator
         operator token '/' on a object that does not identify one unit -- this is a grouping/row key, not a per-unit label
```

It was right. That entry is a MEASUREMENT ROW, not a unit record, and
a token on a measurement row is a row structure. The field was removed
from the artifact — not the finding suppressed, not the guard relaxed.
The token stays where it belongs: once per unit, on that unit's own
member record. This is the third time the guard has caught the work of
the session that ran it (log_113 §"the guard caught this session's own
work", log_118 §8), which is the guard doing its job.

---

# 8. Two lists

## 8.1 Decided, recorded for audit (mechanical)

- An operand read through a memory operand at the carve's boundary
  keeps a MEMORY seat — the next designated location in first-needed
  order — and is brought into the reserved reload register `%r11` for
  the length of one instruction. Nothing is re-plumbed into a register
  that did not arrive in one.
- A computation core whose last instruction leaves its result in the
  FLAGS is refused by name rather than given an invented
  materialisation (`php/add_function`).
- The divide family's implicit `%edx:%eax` dividend read is counted by
  the java walk; without it the confluence is invisible.
- A self-xor is treated as a zeroing, not a lineage read.
- The candidate set for every proof is snapshotted from the COMPILED
  population before any interpreter text enters the population dicts,
  so one interpreter unit can never become a candidate for another and
  silently widen the compiled table.
- `interp_join_prover33.py` is used for exactly those texts that carry
  a designated location, chosen by a machine fact about the text;
  every other text goes to `cross_unit_prover.prove_pair` unchanged.
- The interpreter class key is four machine facts and a null key
  merges with nothing.
- Observations form no edge in the union view.

## 8.2 Awaiting the owner (kept minimal)

1. **May a proved computation part join the union view when the
   interpreter side has no declared operand type?** php's three
   specialised handlers are now PROVED equal to eight compiled units
   each, at 64 bits, with the designated locations bound to the
   compiled seats — but their DWARF read returns zero formal
   parameters at both builds, so no type key licenses the comparison
   and this lap recorded them as TYPE_INCOMPARABLE observations that
   form no edge. Admitting them would need a ruling on what stands in
   for a declared type when a runtime passes its operands through a
   frame rather than as parameters. This is the ontology question of
   the lap and it is the only one.
2. **Should the divide family be modelled in a simulator?** `cltd` and
   `idiv` have no symbolic model in any checker on this line, which is
   why `java/op_2`'s 50 candidate pairs all returned UNDECIDED. It is
   a bounded piece of work with a clear payoff (java's division would
   become comparable with c's, rust's and swift's), and it is not a
   question this lap could answer by itself.

---

# 9. Complete file inventory — every file created this lap

All new. No existing artifact was modified or deleted; §6.2 is the
version-control proof.

| file | bytes | what it is |
|---|---|---|
| `op_pipeline/interp_canon34.py` | 27193 | part (a): the nine refused units through the canonicalizer, with the designated-location seat rule and the java carve |
| `op_pipeline/interp_canon34.json` | 22433 | its output: per unit, canonical text with its seats and directory, or the refusal verbatim |
| `op_pipeline/build_interp_table1.py` | 16715 | part (b): the interpreter table generator |
| `op_pipeline/interp_table1.json` | 25070 | the interpreter table: 7 classes, 8 members, 9 mode rows, 3 unclassed units with reasons |
| `op_pipeline/interp_join_prover33.py` | 5917 | the designated-location prover: Sim33 plus the entry-contract seed binding |
| `op_pipeline/build_interp_join1.py` | 24780 | part (c): the join generator |
| `op_pipeline/interp_join1.json` | 29587 | the join table: 22 rows, the interpreter-to-interpreter edges, the guard join |
| `op_pipeline/build_union_table1.py` | 12020 | part (d): the union view generator |
| `op_pipeline/union_table1.json` | 828414 | the three views and the 1,653-unit navigation index |
| `op_pipeline/interp_union_guard.py` | 2411 | the spelling guard over all five artifacts, exemption bypassed |
| `op_pipeline/interp_zero_regression.py` | 6850 | the baseline recount and the version-control comparison |
| `op_pipeline/interp_zero_regression.json` | 3822 | its output |
| `DevComms/log_119_task32_interp_table_union.md` | this file | the report |

Files opened READ-ONLY and unchanged: `dominant_table24.json`,
`dom_ops22.json`, `guards5.json`, `exception_families3.json`,
`lineage_carve.json`, `prove_interp_computation.json`,
`proposal_representation_dimension3.json`, `dwarf_typed_key.json`,
`dwarf_typed_key_t27.json`, `canon_interp_units_cpython.json`,
`canon_interp_units_java.json`, `canon_interp_units_ruby_php.json`,
`interp_jvm.json`, `canon33_arrival_modes.json`,
`canon31_units_<lang>.json`, `canon.py`, `canon2.py`,
`canon8_behaviour_check.py`, `canon10_behaviour_check.py`,
`canon33_gate.py`, `cross_unit_prover.py`, `designated_memory.py`,
`lineage_carve.py`, `check_no_spelling_keys.py`.

---

# 10. Banking

The daemon commits and pushes every 30 seconds; every artifact above
has already landed, and §6.2 reads the history rather than asserting a
state. This log is the message written for posterity, per the
2026-08-31 ruling.
