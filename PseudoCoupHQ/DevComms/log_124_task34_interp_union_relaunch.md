# log_124 — TASK 34: the interpreter table, the join and the union, relaunched on the universal canonical form

Date: 2026-09-01. Author: Claude Code (implementer), no sub-agents.
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

# 1. What is on disk, audited against the ruling, before anything new

## 1.1 The brief believed the run was lost; it was not

The round-7 brief (log_123) says TASK 32 "was LOST MID-RUN when its
host process exited". Five of its artifacts are on disk, and its report
is too:

```
$ ls -la interp_table1.json interp_join1.json union_table1.json
-rw-rw-r-- 1 <user> <user>   29587 Sep  1 17:10 interp_join1.json
-rw-rw-r-- 1 <user> <user>   25070 Sep  1 17:07 interp_table1.json
-rw-rw-r-- 1 <user> <user>  828414 Sep  1 17:11 union_table1.json
$ ls -la PseudoCoupHQ/DevComms/log_119*
-rw-rw-r-- 1 <user> <user> 36483 Sep  1 17:15 log_119_task32_interp_table_union.md
```

So the first act of this lap is an audit, not a rebuild from nothing.

## 1.2 Kept or superseded, per artifact, with the reason

The audit question is single: does the artifact state the
REGISTER-BASED form as primary? the owner's ruling of 2026-09-01 supersedes
that description, so anything whose primary statement is a register
render is superseded as a statement while remaining valid as evidence.

| artifact on disk | audit verdict | reason |
|---|---|---|
| `interp_canon34.json` | **evidence KEPT, render SUPERSEDED** | its carves, seats and refusal texts are measurements and stand; its rendered texts put a memory-arriving operand in a raw park-reload line inside the core (`mov -0x8(%rsp),%r11`) while a register-arriving operand is read directly — two arrival dialects, which the ruling dissolves |
| `interp_table1.json` | **SUPERSEDED as the primary table** | its texts are those register renders, its class key carries the arrival mode as a KEY COMPONENT, and it answers for 8 of 11 units |
| `interp_join1.json` | **proofs KEPT, table SUPERSEDED** | the 18 PROVED_EQUAL rows are solver results over unit semantics and do not depend on the render; the table itself is rebuilt because its interpreter side is superseded |
| `union_table1.json` | **SUPERSEDED** | it indexes the superseded interpreter table |
| `dominant_table24.json` | **UNTOUCHED, and proved untouched** | §6 |

## 1.3 The brief's premise about the three refusals is not what the disk says

The brief describes "3 register-scarcity/plumbing refusals" and rules
them defects. Read from the artifacts, none of the three is a scarcity
refusal. Their verbatim causes, from `interp_canon34.json` and
`lineage_carve.json`:

- `php/add_function` — "the core's last instruction 'cmp $0x44,%al'
  leaves its result in the FLAGS, not in a register". A carve-boundary
  fact, not a register shortage. **This one IS fixed this lap**, and
  the ruling is what fixes it (§2.3).
- `ruby/vm_opt_plus` — "no slice exists for this symbol at this build:
  the symbol's label line is absent from the dump — the build has no
  body for this symbol". An absence of code.
- `ruby/rb_big_plus` — "the lineages leave this unit through a call, so
  the confluence is inside a callee, not here … call 3aa330 \<bigadd\>".
  An interprocedural fact.

Said plainly so the record is not left implying otherwise: **register
scarcity refuses no unit in this population, and refused none before
the ruling either.** The ruling's "scarcity is now a defect" clause has
no work to do here; its real effect on this population is §2.

## 1.4 Log 121 does not exist, verified against the whole tree

```
$ ls PseudoCoupHQ/DevComms/log_12*.md
.../log_120_task33_bank_round6.md
.../log_122_swift_source_obtained.md
.../log_123_claude_code_task_briefs_round7.md
$ find ~/Programming -name "log_121*" 2>/dev/null
StressBot/RelevantProjects/PseudoCoup_v0/DevComms/log_121_reactivity_model.md
```

- The one hit is in an unrelated repo (`PseudoCoup_v0`) and is about a
  reactivity model, not about this line.
- WHICH SIDE OF THE CONTAINER WALL: this check ran on the HOST — the
  shell's `hostname` is `<user>` and `PseudoCoupHQ`
  resolves, which it does not inside the Airlock container. So the
  absence is an absence in the real tree, not a mount artefact.
- Citations in this log therefore go to **log_116, log_118, log_119**.

---

# 2. The universal form, with values in motion

## 2.1 The form, stated once

Every unit, no exceptions:

```
    <one standardized load per traced value, in designation order>
    <the unit's own computation core, reading the designated registers>
    ret
```

plus a DIRECTORY (S0 holds `a`, S1 holds `b`) and an ARRIVAL
ANNOTATION per value. `S0` is `-0x8(%rsp)`, `S1` is `-0x10(%rsp)`, from
`designated_memory.slot_text` unchanged.

## 2.2 One php handler, with values in motion

Take `php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER`, `a = 20`,
`b = 3`. Its register-form text on record was:

```
mov %rdi,%rax          %rax = 20        a read from its register
mov -0x8(%rsp),%r11    %r11 = 3         b reloaded from memory
add %r11,%rax          %rax = 23
ret
```

The two operands are read in two different shapes. Under the ruling
both live in the designated virtual memory and both are loaded the same
way, so the reload leaves the core and becomes a standardized load:

```
mov -0x8(%rsp),%rdi    %rdi = 20        S0 -> a          [standardized]
mov -0x10(%rsp),%rsi   %rsi = 3         S1 -> b          [standardized]
mov %rdi,%rax          %rax = 20
add %rsi,%rax          %rax = 23
ret
```

- The move is not deleted, it is DELETE-AND-SUBSTITUTE as one act: the
  reload disappears and every downstream read of `%r11` is rewritten to
  `%rsi`, which is `b`'s standardized vehicle.
- The arrival annotation `typed-pointer(zval*)` rides beside the text.
  It is no longer visible IN the text, which is the whole point.

## 2.3 php/add_function, the refusal the ruling actually dissolves

Its ship body's first eight instructions, from its own recorded
objdump (`lineage_carve.json`, ship walk), with `a = 20`, `b = 3` and
both operands long:

```
 1  movzbl 0x8(%rsi),%eax     the TYPE TAG of operand 1
 2  shl    $0x4,%eax
 3  or     0x8(%rdx),%al      the TYPE TAG of operand 2 folded in
 4  cmp    $0x44,%al          GUARD: are both long?
 5  jne    40c0a8             -> not taken
 6  mov    (%rsi),%rax        %rax = 20   the VALUE of operand 1
 7  add    (%rdx),%rax        %rax = 23   <- the confluence
 8  jo     40c080             GUARD: did it overflow?
```

- The OLD carve put the confluence at line 3, because `%rsi` and `%rdx`
  both feed it — and line 3 combines TAGS, not values. Its result lands
  in the FLAGS, so the renderer refused, correctly, for the boundary it
  had been given.
- Under the ruling, arrival is an ANNOTATION and a pointer arrival's
  dereference is part of the standardized load. So the rule this lap
  applies, mechanically: **a read at a NONZERO displacement from a
  pointer arrival is the arrival's metadata; the value lineage is what
  `(%p)` yields.** Lines 1–3 become arrival machinery.
- The confluence is then line 7, `add (%rdx),%rax`, and the universal
  text is `mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax;
  add %rsi,%rax; ret`.
- One implementation detail that was a real bug in the first run of
  this lap's walker: `add` READS its destination. Without that, line 7
  looks like a one-lineage instruction and no confluence is ever found.
  Fixed at first observation, in `READ_MODIFY_WRITE`.
- Line 5's branch is recorded as a guard passed on the normal path;
  line 8's overflow branch is in the recorded after-the-answer
  segment. Nothing measured is discarded.

## 2.4 The two that still carry no text, and why neither is a defect

- `ruby/vm_opt_plus`. `op_units_ruby.json` probe 1 records
  `ship.present = false`, reason: "the symbol's label line is absent
  from the dump — the build has no body for this symbol". There is
  nothing to canonicalise. The gate is "prove against the unit's OWN
  ship code", so the anchor build's body may not stand in for it.
- `ruby/rb_big_plus`. Ship body present; its two lineages leave through
  `call 3aa330 <bigadd>` and `call 3ae420 <big2dbl>`, neither of which
  is an extracted unit — `op_units_ruby.json` holds six symbols and
  those two are not among them. The confluence is interprocedural.
- What would change each is recorded in the artifact, not left as a
  mystery: a ship build that does not inline `vm_opt_plus` away (or a
  ruled decision to canonicalise its anchor build); extraction of the
  callee units plus a ruled interprocedural seed for `rb_big_plus`.
  Both are the owner's calls, and neither was taken here.

---

# 3. The gate, which is what makes the new texts admissible

Every universal text is z3-proved equal to **that unit's own prior
text**, with each designated location bound to the same symbol as the
operand it seats (the entry-contract binding, reused unchanged from
`interp_join_prover33.py`). A unit that does not prove keeps no text.

```
$ /tmp/reconnect_venv/bin/python3 interp_canon35.py
cpython/long_add_fastpath          UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
java/op_1                          UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; and $-1,%eax; mov %rsi,%r10; and $-1,%r10d; add %r10d,%eax; ret
java/op_2                          UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%edi; mov -0x10(%rsp),%esi; mov %edi,%eax; cltd; idiv %esi; ret
ruby/rb_fix_plus                   UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rsi,%rax; add %rdi,%rax; ret
ruby/rb_int_plus                   UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
php/ZEND_ADD_SPEC_...              UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
php/ZEND_ADD_LONG_SPEC_...         UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
php/ZEND_ADD_LONG_NO_OVERFLOW_...  UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rsi,%rax; add %rdi,%rax; ret
php/add_function                   UNIVERSAL_TEXT_PRODUCED  mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
ruby/vm_opt_plus                   NO_CANONICAL_TEXT        no text; not a scarcity refusal
ruby/rb_big_plus                   NO_CANONICAL_TEXT        no text; not a scarcity refusal
summary: {"universal_text_produced": 9, "no_universal_text": 2}
PASS interp_canon35.json -- no operator token in any key, grouping, pairing or row structure
```

- **All 9 gate verdicts are PROVED**, verified from the artifact:

```
$ /tmp/reconnect_venv/bin/python3 -c "import json; d=json.load(open('interp_canon35.json')); print(sorted(set(r['gate_verdict'] for r in d['records'])))"
['PROVED']
```

- POPULATION for the 9: the 11 interpreter/JIT units on record —
  cpython 1, java 2, ruby 4, php 4. Not a sample of a larger set.
- Two hoist preconditions are checked per unit and would refuse by
  name: the core writes no memory (P1), and the core does not write a
  designated operand register before its last read of it (P2).
- One cause fixed at first observation, in the gate rather than in the
  artifact: the register form parked an operand at `-0x8(%rsp)`, and
  the universal form's S0 is also `-0x8(%rsp)` — but they may seat
  DIFFERENT operands. Binding both texts by slot text would have bound
  one operand's symbol onto the other's seat and asked the wrong
  question (it showed up as two php DISPROVED rows). The prior text's
  slots are renamed to gate-private names before either side is bound.

---

# 4. The three views, rebuilt

## 4.1 The interpreter table — `interp_table2.json`

Class key is **(type_pair, result_type, universal_text)**: three
machine facts, no token. Arrival is deliberately NOT in the key —
keeping it there would re-create the separate dialects the ruling
dissolves, and the owner's own instruction is that same-instructions/
different-modes is a finding to record.

```
$ /tmp/reconnect_venv/bin/python3 build_interp_table2.py
IU0001  type_pair=PyLongObject*,PyLongObject*  result=PyLongObject*  arrivals=['typed-pointer(PyLongObject*)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
            cpython/long_add_fastpath
IU0002  type_pair=None  result=None  arrivals=['plain']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; and $-1,%eax; mov %rsi,%r10; and $-1,%r10d; add %r10d,%eax; ret
            java/op_1
IU0003  type_pair=None  result=None  arrivals=['plain']
        mov -0x8(%rsp),%edi; mov -0x10(%rsp),%esi; mov %edi,%eax; cltd; idiv %esi; ret
            java/op_2
IU0004  type_pair=None  result=None  arrivals=['typed-pointer(zval*)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rsi,%rax; add %rdi,%rax; ret
            php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER
IU0005  type_pair=None  result=None  arrivals=['typed-pointer(zval*)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
            php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER
            php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER
IU0006  type_pair=zval*,zval*  result=int  arrivals=['typed-pointer(zval*)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
            php/add_function
IU0007  type_pair=VALUE,VALUE  result=VALUE  arrivals=['tagged-value(Fixnum, 2n+1 encoding)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rsi,%rax; add %rdi,%rax; ret
            ruby/rb_fix_plus
IU0008  type_pair=VALUE,VALUE  result=VALUE  arrivals=['tagged-value(Fixnum, 2n+1 encoding)']
        mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
            ruby/rb_int_plus
no class: ['ruby/vm_opt_plus', 'ruby/rb_big_plus']
summary: {"class_count": 8, "member_count": 9, "mode_row_count": 9,
          "same_text_different_arrival_count": 0,
          "cross_language_identity_count": 2}
PASS interp_table2.json -- no operator token in any key, grouping, pairing or row structure
```

## 4.2 The result the owner's ruling predicted, measured

Read IU0005, IU0006 and IU0008 together. Their texts are
CHARACTER-IDENTICAL:

```
mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rdi,%rax; add %rsi,%rax; ret
```

- Four units, two languages (php and ruby), and **two different arrival
  annotations** — `typed-pointer(zval*)` and
  `tagged-value(Fixnum, 2n+1 encoding)`. This is the "meet in the
  middle" in the owner's own words, and it is now a measurement rather than
  an argument. It was INVISIBLE under the register form, where the same
  four units rendered as three different texts.
- A second identity does the same for IU0004 and IU0007:
  `mov -0x8(%rsp),%rdi; mov -0x10(%rsp),%rsi; mov %rsi,%rax; add %rdi,%rax; ret`,
  php and ruby again.
- **The classes are NOT merged.** The declared type keys differ
  (`null`, `zval*,zval*`/`int`, `VALUE,VALUE`/`VALUE`) and the
  result-type split stands (the owner, 2026-08-26). The coincidence is
  recorded under `cross_language_text_identities` as an observation, at
  level 1 — character identity, no proof needed.
- `same_text_different_arrival_count` is 0 WITHIN a class, which is the
  count the ruling names. Across classes it is 2, which is the pair of
  rows above; both numbers are in the artifact so neither can be read
  as the other.

## 4.3 The join — `interp_join2.json`

```
$ /tmp/reconnect_venv/bin/python3 build_interp_join2.py
cpython/long_add_fastpath   PROVED_EQUAL  c/op_109
java/op_1                   PROVED_EQUAL  c/op_102
ruby/rb_fix_plus            PROVED_EQUAL  c/op_109, c/op_116, cpp/op_109, cpp/op_116, go/op_319, go/op_326, rust/op_541, rust/op_548
ruby/rb_int_plus            PROVED_EQUAL  (the same eight)
java/op_2                   TYPE_INCOMPARABLE
php/ZEND_ADD_LONG_NO_OVERFLOW_...  TYPE_INCOMPARABLE
php/ZEND_ADD_LONG_SPEC_...         TYPE_INCOMPARABLE
php/ZEND_ADD_SPEC_...              TYPE_INCOMPARABLE
php/add_function                   TYPE_INCOMPARABLE
interp<->interp IU0007 IU0008 PROVED_EQUAL
summary: {"join_row_count": 23, "by_relation": {"PROVED_EQUAL": 18, "TYPE_INCOMPARABLE": 5},
          "interpreter_to_interpreter_edge_count": 1, "guard_join_row_count": 6,
          "guard_join_by_relation": {"UNDECIDED_CONDITION_NOT_COMPARABLE": 6}}
PASS interp_join2.json -- no operator token in any key, grouping, pairing or row structure
```

- 23 rows against log_119's 22. The extra row is `php/add_function`,
  which had no class at all before this lap.
- The candidate rule is IMPORTED from `build_interp_join1.py`, not
  copied, so it cannot drift: a compiled 0-branch unit whose class key
  is comparable with the interpreter unit's own DWARF-read typed key.
  No token participates in choosing what gets compared.
- One mechanical consequence of the ruling, worth naming: every
  interpreter text now carries a designated location, so EVERY row goes
  through one prover (`interp_join_prover33.prove_pair_33`, Sim33).
  Under the register form the prover was chosen per unit.

## 4.4 java/op_2, which proved nothing last lap and proves something now

log_119 §1.3 reported `java/op_2`'s observation proving nothing against
50 candidates, with the prover's own words: "mnemonic 'cltd' has no
symbolic model in this checker". This lap, same unit, same 50
candidates:

```
java/op_2   cand=50   counts={'proved': 2, 'disproved': 48, 'undecided': 0, 'refused': 0}
            proved_equal_to: ['c/op_210', 'cpp/op_210']
```

- The cause of the change is the uniform prover route, not a new
  proof technique: Sim33 (through `canon10_behaviour_check`) models the
  divide family that Sim8 did not. Under the register form java/op_2's
  text carried no designated location, so it took the Sim8 path.
- 0 undecided out of 50. Every candidate now gets a definite answer.
- This is an OBSERVATION and forms no edge: java's JIT nmethod has no
  ELF file, therefore no DWARF, therefore no measured type key to
  license the comparison. It is recorded where it can be read and it
  changes no relation.

## 4.5 The union — `union_table2.json`

```
$ /tmp/reconnect_venv/bin/python3 build_union_table2.py
U0001  interpreter=['IU0002']  compiled=['C0505']  edges=1
U0002  interpreter=['IU0001', 'IU0007', 'IU0008']  compiled=['C0700', 'C0889']  edges=18
summary: {'compiled_classes': 901, 'interpreter_classes': 8,
          'union_components': 2, 'proved_edges': 19, 'units_indexed': 1654}
PASS union_table2.json -- no operator token in any key, grouping, pairing or row structure
```

- Three views, nothing merged: the compiled view indexes
  `dominant_table24.json`'s 901 classes read-only, the interpreter view
  indexes the 8 classes above, and the union holds only components
  formed by PROVED_EQUAL edges.
- 1,654 units indexed, one more than log_119's 1,653 — `php/add_function`.
- 19 proved edges against log_119's 18, for the same reason.
- U0002 puts cpython's fast path, ruby's two fixnum handlers and two
  compiled classes in one proved component.

---

# 5. The authoritative count, stated once with its population

**Converged 1,676 of 1,779 (compiled five); withdrawn listed
separately: 13.**

Computed, not quoted:

```
$ /tmp/reconnect_venv/bin/python3 interp_zero_regression2.py
status field recomputed from disk: 1635
proofs counted from their own artifacts: {"canon32_sret_units.json": 5, "canon33_units.json": 36, "total": 41}
AUTHORITATIVE: converged 1676 of 1,779 (compiled five); withdrawn listed separately: 13
per language: {"c": {"converged": 583, "unchanged": 20}, "cpp": {"converged": 728, "unchanged": 22}, "go": {"converged": 72, "unchanged": 16}, "rust": {"converged": 112, "unchanged": 2}, "swift": {"converged": 140, "unchanged": 10}}
honest standing converged before the 41: 1622; withdrawn, separate population: 13
PASS
```

- 583 + 728 + 72 + 112 + 140 = 1,635, which is what the `status` field
  of `canon31_units_<lang>.json` still says; the field was not
  rewritten by this lap.
- The 41 are COUNTED from their own artifacts: 5 PROVED_EQUAL members
  in `canon32_sret_units.json` (log_117) and 36 PROVED_EQUAL units in
  `canon33_units.json` (log_118). 1,635 + 41 = 1,676.
- Per ADDENDUM 2, no permission was asked and none is needed.
- **The compiled count does not move again this lap.** TASK 34's nine
  proofs are interpreter/JIT units, which are not members of the
  1,779-unit compiled-five population. Said explicitly so the nine are
  never silently added to a compiled figure.
- The 13 withdrawn stay the one separate population.

---

# 6. Zero regressions, checked against the version control system

```
comparison revision: 61d7a8458a501b7a56bc2852b6645192b9414ea5^
dominant_table24.json        identical to before this lap: True
dom_ops22.json               identical to before this lap: True
guards5.json                 identical to before this lap: True
exception_families3.json     identical to before this lap: True
PASS
```

- The comparison is sha256 of the file NOW against sha256 of the same
  path's content AT the commit before this lap's first artifact landed,
  read with `git show`. A file's current state is not its history; this
  reads the history.
- `dominant_table24.json` was changed in no way, as the brief requires.
- The daemon has already committed everything; `git log` shows this
  lap's artifacts landing (`4beaebc auto: 6 files (interp_canon35.json,
  interp_canon35.py, …)`). This log is the posterity message, and it
  lands after the commits it describes, which is the recorded 2026-08-31
  rule.

---

# 7. The spelling guard, on everything, without exemption

```
$ /tmp/reconnect_venv/bin/python3 interp_union_guard2.py
PASS interp_canon35.json -- no operator token in any key, grouping, pairing or row structure (checked IN FULL, the generator-provenance exemption deliberately bypassed)
PASS interp_table2.json -- ... (exemption deliberately bypassed)
PASS interp_join2.json -- ... (exemption deliberately bypassed)
PASS union_table2.json -- ... (exemption deliberately bypassed)
PASS interp_zero_regression2.json -- ... (exemption deliberately bypassed)
ALL 5 ARTIFACTS PASS THE GUARD WITHOUT EXEMPTION
```

Each generator also refuses its own output on a guard failure, in-line,
before this program runs. The token appears once per unit as a display
label and nowhere else.

---

# 8. Two lists

## 8.1 Decided, recorded for audit (mechanical)

- Arrival is an ANNOTATION and not a key component in `interp_table2`.
  Ground: the ruling's own words, plus the earlier 2026-09-01 ruling
  that same instructions with different modes is a finding.
- The arrival-metadata rule (a read at a nonzero displacement from a
  pointer arrival is metadata, not the value) — the mechanism by which
  `php/add_function` canonicalises.
- Cross-class text identities are recorded as observations and merge
  nothing; the result-type split stands.
- Gate-private renaming of the prior form's slots, so the gate asks the
  right question.
- `READ_MODIFY_WRITE`: the destination of `add`/`or`/`sub`/… is also a
  read.

## 8.2 Awaiting the owner (kept minimal)

- `ruby/vm_opt_plus`: its ship build has no body. Canonicalising its
  ANCHOR body instead would break "prove against the unit's own ship
  code", so it is not done.
- `ruby/rb_big_plus`: closing it needs the callee units extracted and
  an interprocedural seed ruled.

---

# 9. Complete file inventory — every file created this lap

All new. No existing artifact was modified or deleted; §6 is the
version-control proof.

| file | what it is |
|---|---|
| `op_pipeline/interp_canon35.py` | part (a): all eleven units into the universal form; the hoist with P1/P2/P3; the arrival-aware carve; the per-unit z3 gate |
| `op_pipeline/interp_canon35.json` | its output: per unit, universal text, standardized loads, directory, arrival annotation, gate verdict — or the absence with its cause |
| `op_pipeline/build_interp_table2.py` | part (b): the interpreter table generator |
| `op_pipeline/interp_table2.json` | the table: 8 classes, 9 members, 9 mode rows, 2 cross-language text identities, 2 unclassed units with reasons |
| `op_pipeline/build_interp_join2.py` | part (c): the join generator, importing join1's rules rather than copying them |
| `op_pipeline/interp_join2.json` | the join: 23 rows, the interpreter-to-interpreter edge, the guard join |
| `op_pipeline/build_union_table2.py` | part (d): the union generator |
| `op_pipeline/union_table2.json` | the three views and the 1,654-unit navigation index |
| `op_pipeline/interp_union_guard2.py` | the spelling guard over all five artifacts, exemption bypassed |
| `op_pipeline/interp_zero_regression2.py` | the count reconciliation and the version-control comparison |
| `op_pipeline/interp_zero_regression2.json` | its output |
| `DevComms/log_124_task34_interp_union_relaunch.md` | this file |

Files opened READ-ONLY and unchanged: `dominant_table24.json`,
`dom_ops22.json`, `guards5.json`, `exception_families3.json`,
`interp_canon34.json`, `lineage_carve.json`, `op_units_ruby.json`,
`prove_interp_computation.json`,
`proposal_representation_dimension3.json`, `dwarf_typed_key.json`,
`canon_interp_units_cpython.json`, `canon_interp_units_java.json`,
`interp_jvm.json`, `canon31_units_<lang>.json`,
`canon32_sret_units.json`, `canon33_units.json`, `canon33_gate.py`,
`canon10_behaviour_check.py`, `canon8_behaviour_check.py`, `canon.py`,
`cross_unit_prover.py`, `designated_memory.py`,
`interp_join_prover33.py`, `build_interp_join1.py`,
`check_no_spelling_keys.py`.
