# log_117 — TASK 31, the result-destination seat

**Role:** Claude Code implementer, TASK 31 of
`log_115_claude_code_task_briefs_round6.md`. Date: 2026-09-01. No
sub-agents used — every artifact below was built and run directly in
this session with `/tmp/reconnect_venv/bin/python3`.

**Evidence class is stated per claim.** Every "I verified X" sentence
pastes the command and its output.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

---

# 1. The walkthrough, in plain words

## 1.1 What was asked and what happened

Your ruling this round gave the entry contract a third seat, called
"result-destination". I built it, taught the anchoring layer the
displaced calling convention it implies, and re-ran the five rust
units that log_112 diagnosed and left with you.

- **All five now carry canonical text, and all five are proved
  against their own ship code.** No refusals, no undecided verdicts.
  Verdict tally, pasted from the driver: `{'PROVED_EQUAL': 5}`.
- **The corpus survey found no sixth unit.** The four machine-form
  tests were run over every one of the 1,779 units of the five
  compiled languages — c, cpp, go, rust, swift. Exactly 5 members.
  The 1,774 non-members are broken down by the test that refused
  them in §4, and the two near-misses (c/cpp stack spills, go's
  callee-allocated pointer) are shown so the test is visibly
  discriminating rather than vacuously narrow.
- **Nothing else moved.** The converged baseline is unchanged, verified
  programmatically: 1,635 recorded, 1,622 honest standing, 13
  withdrawn as their own separate population. These five units are
  NOT among the 1,635 — they sat in the 144 not-converged, and this
  lap did not rewrite their recorded status.

## 1.2 The one thing that was missing, stated without machinery

These five units never compute anything. They copy their two
arguments into a small block of memory that the caller allocated, and
hand the caller back the address of that block. The pipeline could
not render them for one reason only: **it did not know that the
address occupies an argument seat.** It believed the first argument
`a` arrived in `%rdi`; `%rdi` actually held the address, and `a` had
been pushed one seat to the right, into `%rsi`. Everything downstream
— "the answer never entered a tracked register", "value w0 is read
before it is defined" — was that single wrong belief showing two
faces.

The third seat fixes the belief. Once the contract says `%rdi` is the
result destination, `a` is in `%rsi` and `b` is in `%rdx`, the units
render on the first attempt.

## 1.3 What is genuinely new versus what was already there

- **New:** a seat LIST with designations, replacing the fixed pair
  `a`/`b` plus a result register. The list is ordered and its length
  is not fixed at two — that is the arity relaxation your ruling
  named, discussed in §7.
- **New:** an exit contract for these units — the answer is the
  N-byte image at the result destination, at stated offsets and
  widths, with `%rax` carrying the address back unchanged.
- **Not new:** the five units themselves, their diagnosis, and the
  machine-form membership test. log_112 §2 established all of that
  and reserved the ontology for you. This lap builds what you ruled,
  and nothing beyond it.

---

# 2. The unit, with values in motion

## 2.1 The names used below, glossed before use

- **`..=`** is rust's inclusive-range operator. `a ..= b` builds a
  range value: a small object holding a start, an end, and one extra
  byte the standard library uses as an internal flag. It is what you
  write in `for i in 0 ..= 10`. **The token appears here as a display
  label on the unit and nowhere else** — no key, no grouping, no
  comparison scope uses it.
- **Ship code** is the optimized build of the probe; it is the ground
  truth every gate in this line proves against.
- **A seat** is a physical register a named value is required to
  arrive in. The entry contract is the list of seats.
- **The answer image** is the block of memory the caller allocated for
  the answer; the callee writes into it.

## 2.2 The unit

`rust/op_793` is `a ..= b` with `a` and `b` both signed 64-bit
integers. Its answer is 17 bytes — two 8-byte fields and one flag
byte — which is more than the two return registers can hold, so the
System V convention returns it in memory.

Take a concrete run: `a = 5`, `b = 9`, and the caller has allocated
its 17 bytes at address `0x7ffd0000`.

## 2.3 What the ship code does with those values

Evidence class: **tool testimony, reproducible** — the ship text is
`canon4_units_rust.json`'s own `mnem`, and the values were run through
the gate's executor with the registers bound to the constants above.

```
    mov  %rdi,%rax          %rax  = 0x7ffd0000   the address, handed back
    mov  %rsi,(%rdi)        [0x7ffd0000] = 5     a into field 0
    mov  %rdx,0x8(%rdi)     [0x7ffd0008] = 9     b into field 8
    movb $0x0,0x10(%rdi)    [0x7ffd0010] = 0     the flag byte
    ret
```

The command and its output:

```
$ /tmp/reconnect_venv/bin/python3 -c "
import sys; sys.path.insert(0,'.')
import z3, sret_gate as G
ship=['mov %rdi,%rax','mov %rsi,(%rdi)','mov %rdx,0x8(%rdi)','movb \$0x0,0x10(%rdi)','ret']
seed={'rdi':z3.BitVecVal(0x7ffd0000,64),'rsi':z3.BitVecVal(5,64),'rdx':z3.BitVecVal(9,64)}
s=G.run(ship,seed,'ship')
print('rax =',hex(z3.simplify(s.get_family('rax')).as_long()))
for k in sorted(s.mem): print('   cell',k,'=',z3.simplify(s.mem[k]))"
rax = 0x7ffd0000
   cell ('rdi', 0, 64) = 5
   cell ('rdi', 8, 64) = 9
   cell ('rdi', 16, 8) = 0
```

## 2.4 What the OLD contract said about those same values

`canon4_units_rust.json`'s recorded entry contract for this unit,
quoted from the artifact:

```
   entry_contract = {"a": "rdi", "b": "rsi", "result": "rax"}
```

Walk the same three instructions under that belief:

- `mov %rsi,(%rdi)` — the contract calls `%rsi` the value `b`, so this
  reads `b = 9`. Wrong: the register held `a = 5`.
- `mov %rdx,0x8(%rdi)` — the contract names no value in `%rdx` at all.
  The erasure invented a placeholder called `w0`, found it had never
  been defined, and refused the whole unit: *"value w0 is read before
  it is defined or before the unit's entry contract names it"*.
- The float pair, `op_807` and `op_814`, hit the same wall from the
  other side. Their two arguments really are in `%xmm0`/`%xmm1`, so
  no read went unnamed; instead the erasure reached the end and found
  nothing had ever been written to the answer register, and refused:
  *"the answer value never entered a tracked register"*.

One wrong belief, two refusal texts, five units — which is exactly
what log_112 §2.4 concluded.

## 2.5 What the NEW contract says

```
  ENTRY CONTRACT AFTER (three seats, sysv-displaced):
      result-destination   -> %rdi     (integer)
      a                    -> %rsi     (integer)
      b                    -> %rdx     (integer)
  EXIT CONTRACT: the 17-byte image at the result destination;
                 %rax holds the result destination address,
                 returned unchanged
```

Walk the same instructions again with `a = 5`, `b = 9`:

- `mov %rsi,(%rdi)` reads `a = 5` and writes it at offset 0 of the
  image. Named, correct.
- `mov %rdx,0x8(%rdi)` reads `b = 9` and writes it at offset 8. Named,
  correct — `%rdx` is a seat now, so nothing is invented.
- `movb $0x0,0x10(%rdi)` writes the literal flag byte at offset 16.
- `mov %rdi,%rax` is the exit adapter: the destination address goes
  back to the caller unchanged.

---

# 3. The mechanism, from the wrong seat to the right one

## 3.1 Where the wrong seat came from, quoted from source

Evidence class: **forced by the file's own source.**
`sem_anchored.py` lines 114–137, its `argument_registers`, hands out
ABI seats starting at index 0 and knows nothing about a hidden
pointer:

```
SYSV_INT = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
...
    ni = 0
    ns = 0
    out = []
    for rep in reps:
        if rep in FLOAT_REPS:
            out.append(sses[ns]); ns += 1
        else:
            out.append(ints[ni]); ni += 1
```

`reps` is the DECLARED parameter list — `parameter_reps(meta)` returns
`[lhs_rep, rhs_rep]` and nothing else. So the first declared
parameter always gets `ints[0] = rdi`. For a unit whose answer is
returned in memory, `ints[0]` is already taken.

## 3.2 The displaced ABI, stated as one rule

- When a result-destination seat is present it takes the FIRST
  INTEGER seat, and every declared INTEGER parameter shifts one place
  to the right.
- Floating parameters do not shift. The destination pointer is an
  integer-class argument and consumes an integer seat only — which is
  why `op_807`/`op_814` keep `a` in `%xmm0` and `b` in `%xmm1` while
  `op_786`/`op_793`/`op_800` shift to `%rsi`/`%rdx`.
- The rule lives in `entry_contract3.seat_list`, a new file. Nothing
  in `sem_anchored.py`, `canon.py`, `canon4.py` or any recorded
  artifact was edited (§8 and §9 are the proof).

## 3.3 How a unit is judged to have that seat — four tests, machine form only

A unit is anchored with a result-destination seat when its OWN SHIP
TEXT satisfies all four, and for no other reason:

1. every store in the unit writes through ONE base register B;
2. B is never written by any instruction of the unit, so its value
   arrived from outside;
3. some instruction copies B into the answer register `%rax`;
4. B is never read as data — it appears only as a store base and as
   the source of that copy.

- **No operator token, no `result_type` string, no source expression
  takes part.** The spelling ban holds: the token rides on the row as
  a display label and is never a selector, a key, or a comparison
  scope.
- **Test 2 is the one that keeps the family honest.** Without it, go's
  six pointer-returning units would join — they store through `%rax`
  too, but that `%rax` came back from a call to `runtime.newobject`,
  so the memory is callee-allocated, not caller-provided. §4.3 shows
  them.
- **Refusal by name, never a guess.** An instruction shape the module
  does not recognise raises `NotAnchorable` and the unit is not
  anchored, rather than silently passing the tests.

## 3.4 The round trip: erase, then re-render

Worked on `rust/op_786` (32-bit fields, so the widths differ from
§2's unit and the width rule is visible):

```
  SHIP TEXT (ground truth)
      mov %rdi,%rax
      mov %esi,(%rdi)
      mov %edx,0x4(%rdi)
      movb $0x0,0x8(%rdi)
      ret

  ERASED FORM  (registers replaced by the designation of their seat;
                the copy into the answer register recorded as the
                exit adapter, not as computation)
      store offset 0x0   width 32  value a
      store offset 0x4   width 32  value b
      store offset 0x8   width 8   value $0x0
      exit adapter: result-destination -> answer register

  CANONICAL TEXT (re-rendered from the erased form plus the contract:
                  field writes in ascending offset order, then the
                  adapter, then ret)
      mov %esi,(%rdi)
      mov %edx,0x4(%rdi)
      movb $0x0,0x8(%rdi)
      mov %rdi,%rax
      ret
```

- **The width is not assumed, it is read.** `store ... width 32` came
  from the source register's own spelling `%esi`; the re-render then
  looked 32 up in its seat table and emitted `%esi` again. On
  `op_793` the same path reads `%rsi` and emits `%rsi` at 64 bits.
- **The re-rendered text is NOT a copy of the ship text.** The exit
  adapter moved from the first line to the second-to-last. That is
  what keeps this gate away from the defect log_112 found in
  `canon4.py`, where `blocks` and `derived_blocks` were the same list
  object and the gate compared a text with itself. Verified per unit
  by the driver's own field:
  `candidate differs from the ship text: True` on all five.
- **Moving the adapter is sound only under stated guards, and the
  guards are mechanical.** `sret_render.erase` refuses by name unless
  (a) no field write's source is in the answer register's family,
  (b) the destination register is written by nothing except the
  adapter, and (c) no two field writes overlap in any byte. All three
  hold on all five units; a unit failing any one is refused, not
  rendered.

---

# 4. The corpus survey

## 4.1 What was surveyed, and the result

Evidence class: **tool testimony, reproducible.** The four tests were
run over every unit of all five compiled languages — the population
is the 1,779 compiled units, not the interpreter/JIT set.

```
$ /tmp/reconnect_venv/bin/python3 canon32_sret.py
SURVEY -- the four machine-form tests run over every unit of all five compiled languages
   corpus size: 1779 units (c 610, cpp 770, go 107, rust 125, swift 167)
   members (all four tests hold): 5
   non-members, by the test that refused them:
      t1-no-store                                                            1756
      t1-own-frame                                                           12
      t1-many-bases                                                          6
   breakdown adds up: 1774 non-members + 5 members = 1779
```

## 4.2 The breakdown, read out

| refusal | count | what it is |
|---|---|---|
| `t1-no-store` | 1,756 | the unit contains no store through a register base at all |
| `t1-own-frame` | 12 | the only store base is `%rsp` — the unit's own stack frame, not a caller-provided destination |
| `t1-many-bases` | 6 | the unit's stores use two different base registers |
| **member** | **5** | all four tests hold |
| **total** | **1,779** | |

- **The 1,756 are excluded by an argument, not only by a count.** A
  unit that returns an answer too large for the return registers MUST
  write that answer into memory; a unit with no store therefore cannot
  be returning in memory. So "no store" is a sound exclusion, not a
  narrow one.
- **The corpus does contain other struct returns, and they converge
  without any of this.** `rust/op_721` returns a 16-byte answer — it
  fits two return registers, its ship code is
  `mov %rsi,%rdx ; mov %rdi,%rax ; ret`, and it is already converged.
  That is log_112 §2.3's forced-by-construction evidence: the same
  intention at four answer sizes, register roles changing with the
  SIZE and nothing else.

## 4.3 The two near-misses, so the test is visibly discriminating

Evidence class: **tool testimony, reproducible.**

```
$ /tmp/reconnect_venv/bin/python3 -c "... detect_memory_return over all five languages, printing every non-member that is not t1-no-store ..."
c/30      t1-own-frame     test 1 fails: the store base is the stack pointer or frame pointer %rsp, ...
c/31 c/32 c/33 c/34 c/35            (same)
cpp/42 cpp/43 cpp/44 cpp/45 cpp/46 cpp/47   (same)
go/30     t1-many-bases    test 1 fails: the unit's stores use 2 different base registers ['rax', 'rsp'], not one
go/31 go/32 go/33 go/34 go/35       (same)
```

- The 12 c/cpp units store into their own frame — an unoptimized-style
  spill and reload, which is the pipeline's own separate
  "two-operands-in-memory" bucket, not a memory return.
- The 6 go units are the interesting negative. Their ship code reads
  `lea 0x6da6(%rip),%rax ; call 41a7a0 <runtime.newobject> ;
  mov 0x20(%rsp),%rcx ; mov %rcx,(%rax)` — a store through `%rax`,
  but `%rax` was WRITTEN by the call, so the memory is allocated by
  the callee. Test 2 would refuse them on that ground even if test 1
  did not refuse them first on the mixed bases.

---

# 5. The gate, and why its five acceptances are load-bearing

## 5.1 Why the existing gate could not be used unchanged

`canon10_behaviour_check` compares ONE register: `answer_home_from_real`
finds the last instruction of the real ship text that writes `%xmm0`
or an rax-family register, and z3 is asked whether the two texts agree
there. On these units that register holds an ADDRESS. A gate looking
only there would accept a candidate that stored the WRONG VALUES into
the RIGHT PLACE.

## 5.2 What the new gate compares

`sret_gate.check` proves two things together, and reports which one
failed when one does:

1. the value left in the answer register, and
2. every cell of the answer image, keyed by (base register family,
   byte offset, width in bits).

- **Cell sets are compared first, as sets.** If the candidate writes a
  cell the ship code does not, or misses one it does, the verdict is
  DISPROVED with the differing cells named. It is never quietly
  ignored.
- **Keying is by base family and offset, not by operand spelling.**
  So `(%rdi)` and `0x0(%rdi)` are the same cell — a spelling
  difference is harmless, an offset difference is caught.
- **Nothing is uninterpreted.** The five modelled instruction shapes
  (register copy, integer field write, immediate field write, float
  field write, `ret`) do no arithmetic, so every one is modelled
  exactly. Any other mnemonic raises `OutsideVocabulary` and the unit
  is UNDECIDED by name — the honest boundary of this gate.

## 5.3 The three controls

Evidence class: **tool testimony, reproducible.**

```
$ /tmp/reconnect_venv/bin/python3 canon32_sret_controls.py
CONTROL 1 (negative, mutation): {'applied': 22, 'rejected': 22, 'still_proved': 0, 'not_applicable': 3}
   PASS -- every applied mutation was rejected
CONTROL 2 (positive, real against real): {'tested': 5, 'proved': 5, 'not_proved': 0}
   PASS -- every unit's own ship text proves equal to itself, so a DISPROVED verdict is about the candidate, not about this checker
CONTROL 3 (harmless difference, writes reordered): {'tested': 5, 'proved': 5, 'not_proved': 0, 'not_applicable': 0}
   PASS -- reordering disjoint field writes does not change the answer and the gate still proves equality, so the gate compares meaning rather than text
wrote canon32_sret_controls.json
```

- **Control 1** mutates each accepted canonical text five ways —
  `swap-values`, `drop-write`, `flip-immediate`, `wrong-exit`,
  `narrow-write` — and re-runs the identical gate. 22 of 25 applied;
  the 3 not applicable are `narrow-write` on the three units whose
  field writes are already narrow or floating (`op_786`'s `%esi`/`%edx`
  and the two float units' `%xmm0`/`%xmm1`). Every applied mutation
  was rejected.
- **Worked mutation, with the counterexample z3 returned.** Swapping
  `a` and `b` on `op_793`:

  ```
  $ ... G.check(ship, ['mov %rdx,(%rdi)','mov %rsi,0x8(%rdi)','movb $0x0,0x10(%rdi)','mov %rdi,%rax','ret'])
  ('DISPROVED', "z3 found a counterexample under which the candidate and the unit's own real
    ship code disagree in the image cell base=%rdi offset=0x0 width=64:
    [seed_rsi = 18446744073709551615, seed_rdx = 0]")
  ```

  With `a = -1` and `b = 0` the ship code writes `-1` at offset 0 and
  the mutant writes `0`. The gate names the cell, not just "not
  equal".
- **Control 2** is what makes a DISPROVED verdict a statement about a
  candidate rather than about the checker.
- **Control 3** is the complement of control 1: it shows the gate is
  not a disguised text comparison. Reversing the order of disjoint
  field writes changes the text and not the answer, and the gate still
  proves equality.

---

# 6. Per unit — the five results

All five: **canonical text produced, PROVED_EQUAL against the unit's
own ship code.** No refusals. The full transcript is in §6.2; the
table is the summary.

## 6.1 The table

| unit | display label | operand type | entry contract BEFORE (recorded) | entry contract AFTER (three seats) | image | verdict |
|---|---|---|---|---|---|---|
| rust/786 | `..=` | i32 | `{a: rdi, b: rsi, result: rax}` | dest→`%rdi`, a→`%rsi`, b→`%rdx` | 9 bytes; 32/32/8 at 0x0/0x4/0x8 | PROVED_EQUAL |
| rust/793 | `..=` | i64 | `{a: rdi, b: rsi, result: rax}` | dest→`%rdi`, a→`%rsi`, b→`%rdx` | 17 bytes; 64/64/8 at 0x0/0x8/0x10 | PROVED_EQUAL |
| rust/800 | `..=` | u64 | `{a: rdi, b: rsi, result: rax}` | dest→`%rdi`, a→`%rsi`, b→`%rdx` | 17 bytes; 64/64/8 at 0x0/0x8/0x10 | PROVED_EQUAL |
| rust/807 | `..=` | f32 | `{a: xmm0, b: xmm1, result: rax}` | dest→`%rdi`, a→`%xmm0`, b→`%xmm1` | 9 bytes; 32/32/8 at 0x0/0x4/0x8 | PROVED_EQUAL |
| rust/814 | `..=` | f64 | `{a: xmm0, b: xmm1, result: rax}` | dest→`%rdi`, a→`%xmm0`, b→`%xmm1` | 17 bytes; 64/64/8 at 0x0/0x8/0x10 | PROVED_EQUAL |

- The operator token in column 2 is a **display label on the member**
  and appears nowhere in any key, grouping, or comparison scope.
- **The float pair's recorded contract was not wrong about `a` and
  `b`** — `%xmm0`/`%xmm1` were right all along. It was wrong about
  `result: rax`, which named a register that holds an address. That
  is why their refusal text differed from the integer three's.
- **The canonical texts of `op_793` and `op_800` are byte-identical.**
  They differ only in the signedness of the declared operand type,
  which this computation does not touch. Under the representative
  rule (AgentMemory, 2026-08-29) they are a group of two whose
  representative is the first in list order; that grouping step is
  the table's, not this lap's, and no table was rebuilt.

## 6.2 The driver transcript, one unit in full

Evidence class: **tool testimony, reproducible.** `rust/807` is shown
because it is the float case; the other four blocks are identical in
shape and are all in the run output and in
`canon32_sret_units.json`.

```
$ /tmp/reconnect_venv/bin/python3 canon32_sret.py
...
====================================================================
rust/807   [display label only: '..=']
  SHIP TEXT (ground truth):
      mov %rdi,%rax
      movss %xmm0,(%rdi)
      movss %xmm1,0x4(%rdi)
      movb $0x0,0x8(%rdi)
      ret
  canon4's `mnem` is line-identical to op_units' own ship `mnem` (5 lines)
  ENTRY CONTRACT BEFORE (canon4's record): {'a': 'xmm0', 'b': 'xmm1', 'result': 'rax'}
  ENTRY CONTRACT AFTER (three seats, sysv-displaced):
      result-destination   -> %rdi     (integer)
      a                    -> %xmm0    (float)
      b                    -> %xmm1    (float)
  EXIT CONTRACT: the 9-byte image at the result destination; %rax holds the result destination address, returned unchanged
  ERASED FORM:
      store offset 0x0   width 32  value a
      store offset 0x4   width 32  value b
      store offset 0x8   width 8   value $0x0
      exit adapter: result-destination -> answer register
  CANONICAL TEXT (re-rendered):
      movss %xmm0,(%rdi)
      movss %xmm1,0x4(%rdi)
      movb $0x0,0x8(%rdi)
      mov %rdi,%rax
      ret
  candidate differs from the ship text: True
  VERDICT: PROVED_EQUAL
  z3 proved the candidate equal to the unit's own real ship code in every one of the 4 compared places (answer register %rax; image cell base=%rdi offset=0x0 width=32; image cell base=%rdi offset=0x4 width=32; image cell base=%rdi offset=0x8 width=8), for every value of every register either text reads before writing
====================================================================
VERDICT TALLY: {'PROVED_EQUAL': 5}
wrote canon32_sret_units.json -- 5 members
wrote canon32_sret_survey.json
```

## 6.3 The ground-truth check every unit passed first

Before any unit is gated, `canon4_units_<lang>.json`'s `mnem` is
compared line by line with `op_units_<lang>.json`'s
`probes[n]["ship"]["mnem"]`. A member whose two records disagree is
refused, not gated. All five reported
`canon4's mnem is line-identical to op_units' own ship mnem (5 lines)`.
This exists because log_112's circular gate was caused by exactly this
kind of unchecked assumption about which field is ground truth.

---

# 7. The arity note for the owner — the fourth seat, described and NOT built

Your ruling said the third seat "begins relaxing the fixed-arity
ceiling". Here is what the next relaxation is and what it costs. **No
code for any of this was written.**

## 7.1 What the fourth seat would be

- A three-argument operator needs a third VALUE designation. Under
  the displaced convention the seats would read:
  result-destination→`%rdi`, a→`%rsi`, b→`%rdx`, **c→`%rcx`**; without
  a result destination they read a→`%rdi`, b→`%rsi`, c→`%rdx`.
- The seat machinery already handles this. `entry_contract3.seat_list`
  walks a list of representations and hands out seats from the ABI
  lists in order; it is written against `["a", "b"]` in one line
  (`designations = ["a", "b"]`) and against `lhs_rep`/`rhs_rep` in
  another. Both are two-element lists, not two variables. The seat
  layer is the cheap part.

## 7.2 What would break, named

- **The probe generator's shape.** `meta` carries `lhs_rep`, `lhs_type`,
  `rhs_rep`, `rhs_type`, `arity: "binary"`. A third operand has no
  field to live in. Every reader of `meta` — `sem_anchored.parameter_reps`
  included — assumes at most two.
- **The seed/anchor pair.** `canon8_behaviour_check.real_arg_families`
  returns exactly `(in0, in1)`, read from `sem.anchor_registers`, and
  `canon10_behaviour_check._prepare_seed` binds exactly two families.
  A third input would be silently unseeded — the two texts would each
  invent their own symbol for it and a false DISPROVED could follow.
  This is the failure I would expect to appear first, and it would
  appear as spurious counterexamples, not as an error.
- **The canonical register standard itself.** The ratified form names
  a→`%rdi`, b→`%rsi`, temps→`%r10`/`%r11`. A `c` designation needs a
  ratified home, and on the displaced convention `c` lands in `%rcx` —
  which is also x86's shift-count register, so a three-argument
  operator containing a variable shift would collide with an
  instruction pin. The traced-variables-priority rule would evict, and
  whether it evicts the pinned occupant or the traced one is a
  ruling, not a mechanical detail.
- **The lifted form's operand names.** The pyvex path says `in0`/`in1`;
  a third would need `in2` threaded through the name→z3 table.

## 7.3 What would NOT break

- The four detection tests, the erasure, the re-render and the gate in
  this lap are all written over a LIST of seats and a LIST of field
  writes. None of them counts to two anywhere.
- The corpus has no three-argument operator today, so nothing is
  currently mis-anchored by the ceiling. The cost of the fourth seat
  is entirely in the probe and anchor layers, and it is only paid when
  a three-argument operator is probed.

## 7.4 The one question this raises for you, stated and not answered

The third seat is a designation for a value that is **not an operand**
— it is a place to put the answer. The fourth would be a designation
for a **third operand**. Those are different kinds of thing sharing
one list. Whether the entry contract should hold one list with mixed
kinds, or two lists (operand seats, and machinery seats such as a
destination pointer or a context pointer), is an ontology question. I
have built the one-list form because that is what your ruling
described. Flagging, not deciding.

---

# 8. Zero regressions

## 8.1 The baseline, stated precisely and not flattened

- **RECORDED converged: 1,635** — what the `status` field of
  `canon31_units_<lang>.json` says.
- **HONEST standing converged: 1,622** — after log_112's branching
  audit re-gated 18 recorded-converged branching units against blocks
  cut from their own ship bytes.
- **The 13 withdrawn are a SEPARATE POPULATION**, not a subtraction
  folded into one number. They still carry `status: converged` with a
  `job8_branching_audit_verdict` of DISPROVED beside them; whether the
  record is rewritten is your call.

## 8.2 The check, recomputed from disk

Evidence class: **tool testimony, reproducible.**

```
$ /tmp/reconnect_venv/bin/python3 canon32_zero_regression.py
recorded converged, recomputed from disk, per language:
   c        583
   cpp      728
   go        72
   rust     112
   swift    140
   TOTAL   1635
withdrawn by log_112's branching audit (recorded converged, re-gate did not prove): 13
honest standing converged: 1622

the five displaced-ABI units, as canon31 still records them (this lap wrote no existing file):
   rust/786   status='no_canon4_text'  canon4 refusal still recorded: ''
   rust/793   status='no_canon4_text'  canon4 refusal still recorded: ''
   rust/800   status='no_canon4_text'  canon4 refusal still recorded: ''
   rust/807   status='no_canon4_text'  canon4 refusal still recorded: ''
   rust/814   status='no_canon4_text'  canon4 refusal still recorded: ''

sha256 of every file this lap read:
   canon31_units_c.json         3d95a83b88157fe17df71b081ea90e2e9b28accd0b5169907714b81a6b7e8754
   canon4_units_c.json          20972578a86dc004a37dd7c2e362c4c7989150ac7787bbd155d9bcab8010e3c7
   op_units_c.json              f0a5808f3926f35f7f352513d89355c491b40b6d26dc8068c2fa3d93194cfffd
   canon31_units_cpp.json       23b49b7b93307370252c37d8ed58ac4c7c727628059781cf7e2da09307565491
   canon4_units_cpp.json        89e2072fec179b1547e7fcda8f9ff07eec27a4ab74e4934736e35d26441cdf17
   op_units_cpp.json            26748437b0aad338abe1d49bab3383f22a90dff3946948f61d722b2cd75541eb
   canon31_units_go.json        124ade6c26abcc62bf63b133974d09e418c9eb05927f4f48302a3432f9b472db
   canon4_units_go.json         6e977ea6f9d2175c54ffd4db4282037d8fc0f52f29c306397687c7ea86297948
   op_units_go.json             5ac65ecf3622450ed5c19f926520bcc72a0828b67614244c3f60f062f7a87e88
   canon31_units_rust.json      8cebafe2687022f6f6777589e9ccd085673689544df0d01b1a7e483774bb81dc
   canon4_units_rust.json       413626ec5e526b61351b410830ed823ca8ddd37d5427cbbb4e4f855560cbae08
   op_units_rust.json           d84e616d59eed02700eaaf9ca2673266d97e02cf6c2b69aebffbe3b0e77b11ba
   canon31_units_swift.json     fd98a9f1b6de5fd3f9d2f310b6463444831a0a4fcc80a40844626f37ec2a38be
   canon4_units_swift.json      8ab4d315add492b42f7df70ebacc2acc4fff5f29f268ec58c02fe761f447c33c
   op_units_swift.json          684ea836d66bd33e8ee49ce00b1d43f436856c31d34912be9972008d2ecef3c9

ZERO-REGRESSION CHECK: PASS
wrote canon32_zero_regression.json
```

## 8.3 The write-claim, checked against the vcs and not against the files

Evidence class: **tool testimony, reproducible.** The daemon commits
every 30 seconds, so `git status` is clean and proves nothing; the
history is what proves it. Every path this session added or modified:

```
$ cd PseudoCoupHQ && git log --since="3 hours ago" --name-status --pretty=format:'%h %ad' --date=short | grep -E '^[AMD]\s' | sort | uniq -c | sort -rn
      2 M	Research/op_pipeline/entry_contract3.py
      1 M	Research/op_pipeline/canon32_sret_units.json
      1 M	Research/op_pipeline/canon32_sret_survey.json
      1 M	Research/op_pipeline/canon32_sret.py
      1 A	Research/op_pipeline/type_inventory_validation.md
      1 A	Research/op_pipeline/type_inventory_validation.json
      1 A	Research/op_pipeline/type_inventory_validate.py
      1 A	Research/op_pipeline/type_inventory.py
      1 A	Research/op_pipeline/type_inventory.md
      1 A	Research/op_pipeline/type_inventory.json
      1 A	Research/op_pipeline/sret_render.py
      1 A	Research/op_pipeline/sret_gate.py
      1 A	Research/op_pipeline/entry_contract3.py
      1 A	Research/op_pipeline/canon32_sret_units.json
      1 A	Research/op_pipeline/canon32_sret_survey.json
      1 A	Research/op_pipeline/canon32_sret_controls.py
      1 A	Research/op_pipeline/canon32_sret_controls.json
      1 A	Research/op_pipeline/canon32_sret.py
      1 A	DevComms/log_115_claude_code_task_briefs_round6.md
```

- Every `M` is a file THIS lap created and then re-ran (its own
  output, re-written by its own driver). Not one pre-existing pipeline
  file appears.
- The `type_inventory*` files are TASK 29's, running in parallel; they
  are named here for honesty about what else landed in the same
  window, not claimed as this lap's work.
- No table was rebuilt. `dominant_table24` / `dom_ops22` were not
  opened.

## 8.4 What the converged count would become, stated but not recorded

- These five are NOT in the 1,635. They sat in the 144 not-converged,
  in log_112 §7's row "caller-provided destination (§2)".
- If their recorded status is advanced on the strength of this lap's
  proofs, the counts become **1,640 recorded / 1,627 honest**, and the
  remaining not-converged becomes 139.
- **I did not advance them.** Rewriting recorded statuses is a call
  about the record, and the same restraint log_112 applied to the 13
  withdrawals applies here. It is in the awaiting-the owner list, §10.

---

# 9. The spelling guard, on every artifact this lap produced

Evidence class: **tool testimony, reproducible.**

```
$ for f in canon32_sret_units.json canon32_sret_survey.json canon32_sret_controls.json canon32_zero_regression.json; do printf '%-32s ' "$f"; /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py "$f" 2>&1 | tail -1; done
canon32_sret_units.json          PASS canon32_sret_units.json -- no operator token in any key, grouping, pairing or row structure
canon32_sret_survey.json         PASS canon32_sret_survey.json -- no operator token in any key, grouping, pairing or row structure
canon32_sret_controls.json       PASS canon32_sret_controls.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
canon32_zero_regression.json     PASS canon32_zero_regression.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
```

- **The two grouping-shaped artifacts claim NO exemption.**
  `canon32_sret_units.json` and `canon32_sret_survey.json` genuinely
  group units, so they are checked in full and pass in full. Only the
  two controls/verification files, which group nothing, carry the
  provenance role.

---

# 10. Two lists

## 10.1 Decided, recorded for audit (mechanical)

- The result-destination seat takes the first INTEGER seat and shifts
  integer parameters right; floating parameters do not shift. Forced
  by the machine form of `op_807`/`op_814`, whose arguments really are
  in `%xmm0`/`%xmm1`.
- The canonical rendering order for these units: field writes in
  ascending offset order, then contract adapters, then `ret`. Chosen
  so the re-rendered text is not a copy of the ship text, and guarded
  by the commuting and disjointness checks in §3.4.
- The exit contract records the image size, and each field's offset
  and width, plus the fact that `%rax` returns the address unchanged.
- The gate is a purpose-built exact executor over five instruction
  shapes, with loud refusal outside them, rather than an extension of
  `Sim10` — because none of these five instructions does arithmetic,
  so exactness is available and no uninterpreted function is needed.
- The five units' RECORDED statuses were left untouched.

## 10.2 Awaiting the owner (kept minimal)

1. **Should the five be advanced to converged?** They are proved
   against their own ship code with three passing controls. Advancing
   them makes the counts 1,640 recorded / 1,627 honest. That is a call
   about the record.
2. **One seat list or two?** §7.4: the result-destination seat holds a
   machinery value, not an operand; a future third-operand seat holds
   an operand. Whether they share one list is ontology.

---

# 11. Complete file inventory — every file created this lap

All new. No existing artifact was modified or deleted; §8.3 is the
vcs proof.

| file | bytes | what it is |
|---|---|---|
| `op_pipeline/entry_contract3.py` | 18175 | the three-seat entry contract: the seat vocabulary, the displaced-ABI seat rule, the four machine-form detection tests, the exit contract |
| `op_pipeline/sret_render.py` | 9360 | the erase-and-re-render round trip, with the commuting and disjointness guards |
| `op_pipeline/sret_gate.py` | 10449 | the ground-truth-anchored gate: answer register plus every cell of the answer image, exact model, refusal by name outside its five shapes |
| `op_pipeline/canon32_sret.py` | 10433 | the driver: corpus survey, ground-truth check, contract, re-render, gate |
| `op_pipeline/canon32_sret_controls.py` | 10374 | the three controls — mutation, real-against-real, harmless reorder |
| `op_pipeline/canon32_zero_regression.py` | 5926 | the baseline recount, the five units' untouched records, input hashes |
| `op_pipeline/canon32_sret_units.json` | 14573 | the five members: contracts before and after, erased form, canonical text, verdict, detail |
| `op_pipeline/canon32_sret_survey.json` | 615 | the computed corpus survey and its per-test breakdown |
| `op_pipeline/canon32_sret_controls.json` | 10563 | every mutation, its text, and its verdict, per unit |
| `op_pipeline/canon32_zero_regression.json` | 1882 | the recount and the input sha256 list |
| `DevComms/log_117_task31_result_destination_seat.md` | this file | the report |

Files opened READ-ONLY and unchanged: `canon4_units_<lang>.json`,
`canon31_units_<lang>.json`, `op_units_<lang>.json`,
`sem_anchored.py`, `sem_anchored_spill_rust.json`, `canon.py`,
`canon10_behaviour_check.py`, `canon8_behaviour_check.py`,
`real_blocks.py`, `diag_caller_destination.py`,
`check_no_spelling_keys.py`.

---

# 12. Banking

The daemon commits and pushes every 30 seconds; every artifact above
has already landed, and §8.3 reads the history rather than asserting a
state. This log is the message written for posterity, per the
2026-08-31 ruling.
