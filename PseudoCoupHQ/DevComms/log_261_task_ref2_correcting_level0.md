# log 261 — task ref2: correcting level 0, and everything that rests on it re-derived

Node: `hq.research.arch_unit_oracle`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
The reference is also the object of the operator_equivalence node
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/`),
because every term in the pool is built through it.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_ref2_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It follows task ref1 (`PRIVATE/PseudoCoupHQ/DevComms/log_256_task_ref1_level0_against_an_independent_reading.md`),
which located the four defects and decided nothing about them; the owner gave
the word to correct them on 2026-09-10.

Date: 2026-09-10. Instance `ref2`
(`PUBLIC/Airlock/instances/ref2.conf`), brought up and down by
this task. Every lane ran on the tower guest through
`bash PUBLIC/Airlock/remote_lane.sh`; nothing but file
editing, git and those commands ran on the laptop. A lane log's host path
on the tower is
`<runs>/ref2/agent/logs/<stamp>__<lane>.sh.log`,
and every attribution below names its file.

THE REPOSITORY TREE MOVED WHILE THIS TASK RAN, from outside this session:
`PRIVATE/PseudoCoupHQ` is now `PRIVATE/PseudoCoupHQ`
and `PUBLIC/Airlock` is now `PUBLIC/Airlock`. The
paths in this log are the new ones. The TOWER's tree did not move
(`PseudoCoupHQ`), so the lane paths and
everything inside a lane are unchanged; the laptop side of `sync-to` /
`sync-back` was carried across by running `remote_lane.sh` with `HOME`
pointed at a two-link directory in this session's scratchpad, which is the
same rsync with one path corrected and touches nothing in either repository.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ` and
`/sources` IS `Sources`, both mounted into the instance.
Every rendering is labelled **LITERAL** (the object, quoted) or **GLOSS**
(a plain-words reading beside a literal), per the protocol's
`object.literal-gloss-analogy`.

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

## §0. What was done and found, in plain words, before any figure

Task ref1 put our reference simulator side by side with an independent
reading of the same machine — the K-framework x86-64 semantics, which are
Strata's chip-tested formulas — and asked z3, place by place, whether the
two could differ. 383 places disagreed, and all 383 rested on four lines
of `reference.py` and `condition_table.py`. This task corrected those four
lines, one at a time, and after each one re-ran the same check and the
Lean model check, so what each correction bought is measured and not
argued.

The four are hardware facts, and each is now the machine's own rule.
First, a write into a general register: our reference zero-extended every
write below 64 bits, which is right at 32 and wrong at 8 and 16, where the
machine leaves the register's other bits alone. Second, `adc` and `sbb`:
they add or subtract the carry the previous instruction left, and our
reference put that carry into the destination and then recorded a flag
state that did not have it in — so every flag read after one of them was
computed from the wrong sum. Third, a condition: our reference computed
every condition as if the setter had subtracted, which is right after a
`cmp` and wrong after an `add`, an `adc`, an `sbb` or a `neg`; a condition
is now a reading of the five flags CF, ZF, SF, OF and PF, each computed
from the arithmetic the setter's own builder performed. Fourth, `sub` and
`sbb` were missing from the list of mnemonics whose last letter is not an
operand-size suffix, so `sub %esi,(%rax)` — a 32-bit subtraction into
memory — was modelled at 8 bits.

The result is the headline. Before this task the independent reading
disagreed with ours at 383 of 1,779 written places; after the four
corrections it disagrees at NONE. The number of places their reading
leaves undefined (197) and the number neither reading can state (439) did
not move at all, which is the check that the corrections closed
disagreements rather than hiding them. The Lean model check held at
259 rows / 172 stated / 87 refused / ZERO discrepancy after every one of
the four.

Then everything that rests on the reference was re-derived. The arch-opcode
model table was swept five times, once at each state of the reference, so
each row that moved could be attributed to the correction that moved it
rather than guessed at: 2,370 of 14,534 written places moved, and no
attempt changed its outcome — nothing was gained and nothing was lost, the
terms are simply the machine's now. The term store was walked again into a
store of its own beside the old one: 27,682 records re-printed, 4,874 whose
layer-5 text changed, zero disagreements between a term's own s-expression
before and after printing, and zero operand-order disagreements over
27,642 units. Two hundred canon40 proofs were re-run under the corrected
reading and all two hundred still hold, which is what the shape of that
proof predicts: both of its sides are built by the reference, so a
correction moves both together.

Three things did not go as the brief expected, and each is flagged rather
than worked around. The bank's own re-attempt rule reads the sha256 of the
driver, the loop and the renderer and not the reference's, so a corrected
reference would have held back every key it changed; the rule was widened
IN THIS TASK'S PROCESS by patching two functions, and making it permanent
is one line in a file this brief does not authorise. 184 records of the
term store do not converge at any ceiling this instance can give — they
converged at 7,168 MB under the old reading and do not at 10,240 MB under
the new one. And the first run of the spelling guard refused three of this
task's own json files: they carried mnemonics as bare list elements, which
is a row structure, and the guard was right; they now carry each mnemonic
in the field `mnem`.

---

## §1. The objects, one sentence each, in relation

- **The reference** is
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py`:
  one symbolic simulator of the machine, whose `opcode_table` holds one
  builder per arch mnemonic, and which is the ratified ground truth for
  every term this line proves anything about.
- **The condition table** is
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/condition_table.py`:
  the fourteen condition suffixes of x86-64 and what each one means.
- **A written place** is one thing an instruction writes: a named
  register, a memory cell, or one of the six flags `CF PF AF ZF SF OF` as
  Intel's manual names them.
- **The level-0 check** is
  `Research/oracle/arch_opcodes/level0/level0_check.py` (task ref1): per
  matched instruction variant and per written place, z3's verdict on
  whether our reference's term and the K-framework semantics' term can
  differ, in five outcomes and no sixth — `unsat` (they agree), `sat`
  (they differ, with the counterexample), `unknown`, `undefined` (their
  rule writes Intel's undefined value), `refused` (the comparison could
  not be stated).
- **The L2 check** is `Research/op_pipeline/lean/model_translate.py`'s
  `check`, then `run`: one Lean theorem per single-opcode compiled unit
  saying that the unit's own proved term equals the model's operations
  applied in the order the unit's body spells them. Its guard value since
  task l3 (`log_251`) is 259 rows, 172 stated, 87 refused, zero
  discrepancy.
- **The model table** is
  `Research/oracle/arch_opcodes/model/model_table.json`: one row per
  (mnemonic, operand shape, key width) the sweep spells, holding the z3
  term the reference's builder put in each written place.
- **The term store** is `Research/op_pipeline/term66_store/`: one
  layer-4 / layer-5 record per unit for the 30,280 units canon40 proves,
  each unit's term built by walking its ledger rows through the
  reference's builders.
- **The bank** is
  `Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl`:
  one certificate per (cell, target, written place, setter cell), carrying
  the term text it was posed on, the rendered source and its sha256, the
  compiler and its flags, the carved body and the gate's verdict.
- **The five states** are the reference and the condition table as they
  stood before this task and after each of its four corrections, kept as
  files under `Research/oracle/arch_opcodes/level0/ref2_originals/` and
  checked against the sha256 each correction's own lane printed.

---

## §2. The four corrections, each proved against the independent reading before the next

The order is the brief's: one correction, prove it, next. Each correction
is one edit; after each, `level0_check.py` was re-run into a NEW pair of
files beside every earlier pair, `ref2_compare.py` put the two runs side
by side per written place, and the L2 check was run whole — the sweep,
`lake build`, and one Lean process per stated theorem.

Table 1 — the level-0 check after each correction. Population: the 1,779
written places of the 397 instruction variants both readings hold, as of
2026-09-10. `before` is the reference as it stood this morning, and it
reproduces task ref1's own numbers exactly.

| state | `unsat` (agree) | `sat` (disagree) | `unknown` | `undefined` | `refused` | variants agreeing on every place | variants with a disagreement |
|---|---|---|---|---|---|---|---|
| before | 760 | 383 | 0 | 197 | 439 | 192 | 157 |
| after correction 1 | 876 | 267 | 0 | 197 | 439 | 285 | 64 |
| after correction 2 | 946 | 197 | 0 | 197 | 439 | 285 | 64 |
| after correction 3 | 1,119 | 24 | 0 | 197 | 439 | 343 | 6 |
| after correction 4 | **1,143** | **0** | 0 | 197 | 439 | **349** | **0** |

**GLOSS, and it is the whole headline.** Every disagreement closed. The
`undefined` column never moves, because those are the places their reading
leaves as Intel's undefined value and no correction of ours can touch
them; the `refused` column never moves, because those are places one
reading or the other cannot state at all. So the 383 did not migrate into
a bucket where they stop being counted: they became agreements.

Table 2 — the L2 check after each correction, from that correction's own
lane. The guard value task l3 left (`log_251`) is 259 / 172 / 87 with zero
discrepancy, and it holds at every state.

| state | rows | STATED | REFUSED | DISCREPANCY | closed by `bv_decide` | closed by `rfl` |
|---|---|---|---|---|---|---|
| before | 259 | 172 | 87 | 0 | 133 | 39 |
| after correction 1 | 259 | 172 | 87 | 0 | 134 | 38 |
| after correction 2 | 259 | 172 | 87 | 0 | 134 | 38 |
| after correction 3 | 259 | 172 | 87 | 0 | 134 | 38 |
| after correction 4 | 259 | 172 | 87 | 0 | 134 | 38 |

**GLOSS on the one number that moved.** One theorem changed which tactic
closes it: `rfl` (the two sides reduce to the same normal form) gave way to
`bv_decide` (the bit-blasting solver) at correction 1 and stayed there.
Nothing became unprovable; one row's proof got harder, which is what a
term gaining `Concat(Extract(63, 8, v0), ...)` does to a reduction.

### §2.1 Correction 1 — a write of 8 or 16 bits keeps the register's other bits

**THE FACT.** Intel SDM Vol. 1 §3.4.1.1: a 32-bit operand zero-extends
into the 64-bit register; an 8- or 16-bit operand leaves the upper 56 or
48 bits UNMODIFIED. `reference.place_bits` already carried that rule in
its own docstring and applied it in the narrow division and
widening-multiply forms; the general write path did not.

**THE DIFF, LITERAL**, lane
`20260910T173405Z__ref2_l2_correction1.sh.log` step [1/6] (host path
`<runs>/ref2/agent/logs/20260910T173405Z__ref2_l2_correction1.sh.log`),
the two hunks that change behaviour, with the docstring elided:

```
-def full64(value):
+def full64(value, previous=None):
     if value.size() == 64:
         return value
     if value.size() > 64:
         return z3.Extract(63, 0, value)
+    if value.size() in KEEPS_THE_UPPER_BITS and previous is not None:
+        return place_bits(previous, value, 0)
     return z3.ZeroExt(64 - value.size(), value)

         if self.is_register(text):
-            self.state.set_family(self.family_of(text), full64(term))
+            family = self.family_of(text)
+            previous = self.state.family_value(family)
+            self.state.set_family(family, full64(term, previous))
             return
```

**THE RULE, RUN ON VALUES.** Same lane, step [3/6] — four writes of the
value 1 into a register holding all ones:

```
after  mov $0x1,%al   into 0xffffffffffffffff : 0xffffffffffffff01
after  mov $0x1,%ax   into 0xffffffffffffffff : 0xffffffffffff0001
after  mov $0x1,%eax  into 0xffffffffffffffff : 0x1
after  mov $0x1,%rax  into 0xffffffffffffffff : 0x1
```

**WHAT IT BOUGHT**, same lane, step [5/6]:

```
| outcome | before | after | change |
|---|---|---|---|
| `unsat` | 760 | 876 | +116 |
| `sat` | 383 | 267 | -116 |
| `unknown` | 0 | 0 | +0 |
| `undefined` | 197 | 197 | +0 |
| `refused` | 411 | 411 | +0 |

| direction | places | ledger rows | mnemonics |
|---|---|---|---|
| sat -> unsat | 116 | 25394 | 43 mnemonics |
```

**GLOSS on the 411.** That first comparison keyed a row by (variant,
place) alone, and 28 packed-float variants write `reg_xmm0` TWICE in one
row list — the whole register and its low lane — so 28 of the check's
1,779 rows were covered twice and the refused column read 411 where the
check's own tally reads 439. Every one of the 28 is `refused` on both
readings, so no verdict was hidden; the key gained the occurrence index
and the later tables carry all 1,779.

### §2.2 Correction 2 — `adc` and `sbb` leave the carry in the flag state

**THE FACT.** `adc` computes `L + R + c` and `sbb` computes `L - R - c`.
Every flag those two write is a function of `c`. The line this correction
replaces recorded `(mnemonic, L, R)` and left `c` nowhere.

**WHY THE TUPLE DID NOT GROW.** Three w-bit slots cannot hold (L, R, c),
and folding the carry into either side is not equivalent: at `R` = all
ones the carry-out differs and at `R` = `0x7f` the signed overflow does,
and z3 finds both at once. So the flag state became `reference.FlagState`
— which IS the `(setter, L, R)` triple every reader already unpacks, and
carries the incoming carry BESIDE the three. `isinstance(flags, tuple)` is
still true and `setter, left, right = flags` still works, so no other
file's unpacking changed.

**THE DIFF, LITERAL**, lane
`20260910T175424Z__ref2_l3_correction2.sh.log` step [1/7], the behaviour
hunks:

```
     ops.write(1, result)
-    ops.state.flags = (ops.mnemonic, left, right)
+    ops.state.flags = FlagState(ops.mnemonic, left, right,
+                                carry_in=carry_in)
```

and, in `carry_bit`, the subtract family split so the two carry-reading
opcodes get the carry:

```
-    if setter in ("sub", "cmp", "sbb"):
+    if setter in ("sub", "cmp"):
         return z3.ULT(left, right)
-    if setter in ("add", "adc"):
+    if setter in ("adc", "sbb"):
+        width = left.size()
+        carry_value = z3.ZeroExt(1, carry_value_of(flags, width))
+        if setter == "adc":
+            wide = z3.ZeroExt(1, left) + z3.ZeroExt(1, right) + \
+                carry_value
+        else:
+            wide = z3.ZeroExt(1, left) - z3.ZeroExt(1, right) - \
+                carry_value
+        return z3.Extract(width, width, wide) == z3.BitVecVal(1, 1)
+    if setter == "add":
         width = left.size()
```

**THE RULE, RUN ON VALUES.** Same lane, step [3/7] — `0x08 - 0x08` and
`0x08 + 0x08` at 8 bits, under each incoming carry:

```
carry in 0    sbb %sil,%dil with 0x08 - 0x08 : destination 0xff, CF 1
carry in 1    sbb %sil,%dil with 0x08 - 0x08 : destination 0x0, CF 0
carry in 0    adc %sil,%dil with 0x08 + 0x08 : destination 0x11, CF 0
carry in 1    adc %sil,%dil with 0x08 + 0x08 : destination 0x10, CF 0
```

**GLOSS.** `sbb` at `L = R` with the carry set borrows: `0x08 - 0x08 - 1`
is `0xff` with CF 1. The old reading answered `ULT(0x08, 0x08)`, which is
false, whatever the carry was. (The two `carry in` labels read the seeding
comparison's own answer, so the rows are the machine's two cases and not
a hand-set bit.)

**WHAT IT BOUGHT**, same lane, step [6/7]:

```
| outcome | before | after | change |
|---|---|---|---|
| `unsat` | 876 | 946 | +70 |
| `sat` | 267 | 197 | -70 |
| `unknown` | 0 | 0 | +0 |
| `undefined` | 197 | 197 | +0 |
| `refused` | 411 | 411 | +0 |

| direction | places | ledger rows | mnemonics |
|---|---|---|---|
| sat -> sat | 6 | 0 | `sbb` |
| sat -> unsat | 70 | 6060 | `adc` `sbb` |
```

**GLOSS on the six that moved and still disagree.** They are `sbb` places
whose term changed shape because `carry_bit` changed, and which still
disagree for a different reason — the width defect correction 4 closes.
A place can rest on two defects, and this is what that looks like.

### §2.3 Correction 3 — a condition reads the flags the setter wrote

**THE FACT.** A condition on this machine is a reading of CF, ZF, SF, OF
and PF. `condition_table.cond_to_z3` computed every condition on `L - R`,
which is the result for the subtract family and for the families whose
builders already record `(mnemonic, result, 0)`, and is not the result for
`add`, `adc`, `sbb` or `neg`.

**THE SHAPE OF THE CORRECTION**, and it is three named things rather than
one edit:

- `reference.flag_result(flags)` — the value the setter produced, one row
  per flag-setting opcode, read off the builders that already state it.
- `reference.FlagReading.bit(name)` — CF and OF through the existing
  `carry_bit` and `overflow_bit`; ZF, SF and PF from `flag_result`. Each
  is computed only when it is asked for, so `bt`, which writes CF and
  leaves the rest undefined, answers CF and refuses the others BY CAUSE.
- `condition_table.cond_from_flags(cond, bit, z3mod)` — Intel SDM Vol. 1
  Appendix B's own table, fourteen rows over those five flags.

`cond_to_z3` keeps its body, its 112-row proof against angr's own ccall,
and the caller it is right for: `term.RenderBack` renders a predicate back
to arch text AS a `cmp`, and after a `cmp` the result IS `L - R`.

**THE DIFF, LITERAL**, lane
`20260910T181433Z__ref2_l4_correction3.sh.log` step [1/8], the tail of
`predicate_of` (the three special cases that disappear into the general
rule):

```
-    if setter not in ("cmp", "test") and \
-            suffix in ("b", "c", "nae", "ae", "nb", "nc"):
-        carry = carry_bit(state.flags)
-        if suffix in ("b", "c", "nae"):
-            return carry
-        return z3.Not(carry)
-    if setter == "bt":
-        raise NotModeled(
-            "the condition %r is read after `bt`, which sets only the "
-            "carry flag and leaves the zero and sign flags undefined"
-            % suffix)
-    return CT.cond_to_z3(condition, left, right, z3)
+    reading = FlagReading(state.flags)
+    return CT.cond_from_flags(condition, reading.bit, z3)
```

**THE ACCEPTANCE CRITERION THE BRIEF NAMES, ASKED OF z3 RATHER THAN
ARGUED.** `ref2_condition_proof.py` builds the flag state each builder
leaves for fifteen setters, at four widths, for sixteen condition
suffixes, under the OLD reference (imported from `ref2_originals/`, live
code, not a description of it) and under the new one, and asks z3 whether
the two readings can differ. Same lane, step [3/8]:

```
| `mnem` | rows | the reading did NOT move | it moved | both refuse | other |
|---|---|---|---|---|---|
| `adc` | 64 | 0 | 64 | 0 | 0 |
| `add` | 64 | 16 | 48 | 0 | 0 |
| `and` | 64 | 64 | 0 | 0 | 0 |
| `bsr` | 64 | 24 | 0 | 16 | 24 |
| `bt` | 64 | 8 | 0 | 8 | 48 |
| `cmp` | 64 | 64 | 0 | 0 | 0 |
| `imul` | 64 | 0 | 24 | 16 | 24 |
| `inc` | 64 | 24 | 0 | 16 | 24 |
| `mul` | 64 | 0 | 24 | 16 | 24 |
| `neg` | 64 | 24 | 40 | 0 | 0 |
| `or` | 64 | 64 | 0 | 0 | 0 |
| `sbb` | 64 | 0 | 64 | 0 | 0 |
| `sub` | 64 | 64 | 0 | 0 | 0 |
| `test` | 64 | 64 | 0 | 0 | 0 |
| `xor` | 64 | 64 | 0 | 0 | 0 |
```

**GLOSS, against the brief's own words: "`add`/`neg` rows disagree today;
`sub`/`cmp` rows must not move."** `sub` and `cmp` read 64 of 64 rows
UNCHANGED — z3 says the old operand reading and the new flag reading are
the same function at every width and every condition, which is the proof
that the correction is a generalisation and not a replacement. `add` moves
on 48 of 64: the sixteen that do not are the four carry-and-overflow
conditions at four widths, which already went through `carry_bit`. `neg`
moves on 40 of 64; its zero flag does not move (`-L == 0` is `L == 0`) and
its sign flag does. `adc` and `sbb` move everywhere, which is correction 2
and correction 3 together.

**THE THREE MNEMONICS WHOSE CONDITIONS NOW REFUSE, said out loud rather
than left in the "other" column.** For `inc`, `imul` and `mul` the six
conditions that read the overflow or the carry flag — `l`, `ge`, `le`,
`g`, `a`, `be` — answered before and refuse now. They refuse because this
reference has never written an overflow or carry model for those three
setters (`reference.overflow_bit` says so in its own sentence, and task
ref1 counted 16 places refused under exactly that cause). The old code
answered them from `L - R` anyway. That is not a loss of coverage in the
level-0 check — the `refused` column did not move by one place — and it is
the honest reading of a flag this file states no model for.

**THE RULE, RUN ON VALUES.** Same lane, step [4/8]:

```
add %sil,%dil  %dil=0x08 %sil=0x08 -> result 0x10  ZF 0  SF 0
add %sil,%dil  %dil=0x08 %sil=0xf8 -> result 0x00  ZF 1  SF 0
sub %sil,%dil  %dil=0x08 %sil=0x08 -> result 0x00  ZF 1  SF 0
sub %sil,%dil  %dil=0x08 %sil=0xf8 -> result 0x10  ZF 0  SF 0
neg %edi        %edi=0x40000000 -> result 0xc0000000  SF 1
```

**GLOSS.** After an addition the zero flag is now "the sum is zero"
(`0x08 + 0xf8` is `0x00`), where it used to be "the two operands are
equal". After `neg`, the sign flag is the sign of the NEGATED value —
`0x40000000` negates to `0xc0000000`, which is negative — where it used to
be the sign of the original. That last row is task ref1's own
counterexample (`log_256` §7.3), now answering the way their reading does.

**WHAT IT BOUGHT**, same lane, step [6/8]:

```
| outcome | before | after | change |
|---|---|---|---|
| `unsat` | 946 | 1119 | +173 |
| `sat` | 197 | 24 | -173 |
| `unknown` | 0 | 0 | +0 |
| `undefined` | 197 | 197 | +0 |
| `refused` | 439 | 439 | +0 |

| direction | places | ledger rows | mnemonics |
|---|---|---|---|
| sat -> sat | 10 | 0 | `sbb` `sub` |
| sat -> unsat | 173 | 11897 | `adc` `add` `neg` `sbb` |
```

and what was left, same lane, step [7/8]:

```
   6  the flag CF                            sbb sub
   6  the flag ZF                            sbb sub
   6  the flag SF                            sbb sub
   6  the flag OF                            sbb sub
```

### §2.4 Correction 4 — the last letter of `sub` and `sbb` is not a size

**THE FACT.** `reference.Operands.width_at` gives a memory operand its
width from the mnemonic's own last AT&T size letter unless the mnemonic
sits in `WIDTH_IS_NOT_A_SUFFIX`. `sub` and `sbb` end in `b` and were not
in that list, so `sub %esi,(%rax)` was modelled at 8 bits.

**THE DIFF, LITERAL**, lane
`20260910T183440Z__ref2_l5_correction4.sh.log` step [1/8]:

```
     "jge", "jae", "pand", "por", "movsbw", "movzbw",
+    "sub", "sbb",
 ])
```

**THE RULE, RUN ON VALUES.** Same lane, step [3/8]:

```
destination_width of add   %esi,(%rax) is 32
destination_width of sub   %esi,(%rax) is 32
destination_width of sbb   %esi,(%rax) is 32
destination_width of adc   %esi,(%rax) is 32
destination_width of xor   %esi,(%rax) is 32
destination_width of movb  %esi,(%rax) is 8
```

**WHAT IT BOUGHT**, same lane, step [6/8], and it closes the last
disagreement in the check:

```
| outcome | before | after | change |
|---|---|---|---|
| `unsat` | 1119 | 1143 | +24 |
| `sat` | 24 | 0 | -24 |
| `unknown` | 0 | 0 | +0 |
| `undefined` | 197 | 197 | +0 |
| `refused` | 439 | 439 | +0 |

| direction | places | ledger rows | mnemonics |
|---|---|---|---|
| sat -> unsat | 24 | 0 | `sbb` `sub` |
```

**THE AUDIT THE BRIEF ASKS FOR: which size letters are genuinely
suffixes.** `ref2_suffix_audit.py` runs each builder TWICE over every
operand spelling of the sweep that carries a memory operand — once with
the mnemonic out of `WIDTH_IS_NOT_A_SUFFIX` and once with it in — and
compares the written places by their z3 s-expressions. Identical on every
shape means the letter decides nothing at all; different on some shape
means the letter decides, and the row then carries both widths. A
mnemonic that READS the flags is handed `model_translate.preseeded_state`,
because on a fresh state the reference refuses by name before the width
rule is reached.

Table 3 — the seven mnemonics whose size letter DECIDES a width, out of 41
whose last letter is a size letter and which the table holds with a
builder. Population: the sweep's memory-bearing operand spellings at all
four widths, as of 2026-09-10. The full 41 rows are
`level0/ref2_suffix_audit.json`.

| `mnem` | letter | the letter's width | in the list | shapes where the choice decides | the two widths |
|---|---|---|---|---|---|
| `sub` | b | 8 | now yes | 7 | 8 against 16, 32, 64, 128 |
| `sbb` | b | 8 | now yes | 4 | both readings refuse, different sentence |
| `imul` | l | 32 | yes | 11 | 32 against 8, 16, 64, 128 |
| `mul` | l | 32 | yes | 15 | 32 against 8, 16, 64, 128 |
| `shl` | l | 32 | yes | 4 | both readings refuse, different sentence |
| `movb` | b | 8 | no | 3 | 8 against 16, 32, 64 |
| `movq` | q | 64 | no | 3 | 64 against 8, 16, 32 |

**GLOSS, and it is why 34 mnemonics are not 34 defects.** Thirty-four of
the 41 letters decide nothing: either the builder never asks `width_at`
for the memory slot — the x87 family reads a memory operand as an opaque
float symbol of its own, so `fldl` never consults its `l` — or the
fallback gives the same number. Of the seven that decide, five are already
in the list and use the fallback, which is right. The two that are NOT in
the list are `movb` and `movq`, and for those the letter IS the operand
size: `movb %sil,(%rax)` really is a byte move. So nothing else in this
table is a defect, and nothing else was changed.

**THE ONE PLACE THE AUDIT UNDER-MEASURES, named rather than left to be
found.** `sbb` and `shl` show four differing shapes each, and all four are
the one-memory-operand spelling `mem_one`, where BOTH readings refuse and
only the refusal sentence differs. `sbb`'s real movement is not in this
table at all — it is the 24 places of the level-0 check above and the 28
model-table places of §3 — because the audit compares what the two
readings COMPUTE, and a `sbb` whose flags are seeded computes at the
shapes the level-0 check exercises.

---
