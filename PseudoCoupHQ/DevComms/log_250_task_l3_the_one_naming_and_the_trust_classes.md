# log_250 — task l3: the check's composer names both sides by the stored line's own rule (19 DISCREPANCY → 0), and the native-evaluation trust class measured

Node: `hq.research.compiler_graph.gate.lean.model_translator`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md`).
Its super-node is the lean node
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`).
Artifacts: `PseudoCoupHQ/Research/op_pipeline/lean/`.
Instance: `Airlock/instances/l3.conf`, on the tower.
Lanes: 12, all kept at
`PseudoCoupHQ/Research/op_pipeline/lean/lanes_l3/`.
Lane logs cited below are TOWER paths
(`<runs>/l3/agent/logs/...`), stated as such.

---

## 0. What was done and found, in plain words, before any figures

Task L2 (log 232) left the single-opcode check at 259 rows: 153 proved, 87
refused before Lean, and 19 that Lean's bit-blasting tactic answered with a
concrete counterexample. L2 recorded those 19 as DISCREPANCY — a located
disagreement between two readings of the hardware — and did not adjudicate
them. This task was asked to verify the coordinator's reading of those 19
first, then to make the check's composer name both sides of every theorem by
one function, and separately to look at the proofs that lean on native
evaluation.

The verification ran before anything was changed and it does not support the
coordinator's reading. The coordinator's account was that the check builds
the model side's binders by the C parameter convention while the unit's own
term names arrivals in ledger order. Neither half is what the rows show.
Both sides are named by a PRINT-ORDER rule — the free symbols of a term
numbered in the order the printed text meets them — and which register lands
on `v0` is a property of the printed shape, not of any convention. What
differs is the term each side prints. The stored line's names come from
`term.Term.normalize`, which puts every commutative operator's arguments in a
fixed order computed from the arguments themselves, both before and after it
simplifies. The check's own `bound_variables` numbered the symbols after a
plain simplify with neither ordering step — which was the whole rule until
task t104 added the first ordering step on 2026-09-07, after the check was
written. On a term whose commutative operands that step permutes, the two
rules put the two arrivals in opposite order. The left of the theorem then
called one register `v0` and the right called the other one `v0`, and the
counterexample the tactic returned was about the two names and not about the
machine.

Two rows show the direction is not fixed, which is what rules out a
"convention versus ledger order" reading outright. For `c/op_113`
(`mov %esi,%eax; add %rdi,%rax`) the stored line calls `%rsi` `v0`, and the
check called `%rdi` `v0`. For `cpp/op_133` (`mov %edi,%eax; add %rsi,%rax`)
it is the other way round: the stored line calls `%rdi` `v0` and the check
called `%rsi` `v0`. The ledger's arrival rows are the same for both units,
IN-0 = `%rdi`, IN-1 = `%rsi`.

The fix is one function. `bound_variables` now calls `term.py`'s own
`order_commutative` and `ordered_symbols`, in the order `term.Term.normalize`
applies them, so the naming rule has one definition and it lives in the
module that owns it. `term.py` was not modified. And the naming is no longer
asserted: with the names substituted the term is printed by the same printer,
and the line must give the stored line back character for character, or the
row is refused by cause. All 19 then prove. The check now reads 259 rows,
172 stated, 87 refused, ZERO discrepancy, and that is the guard value every
later task states.

The second item did not survive contact with the artifacts either. The brief
asked for 61 proofs that used native evaluation to be re-proved by
bit-blasting. `native_decide` appears nowhere in this project — not in task
L1's edge theorems, not in the check's theorems, not anywhere. The 61 is a
figure from log 232 §6, not log 227, and it counts rows that were ALREADY
closed by `bv_decide`: the axiom `Lean.ofReduceBool` is `bv_decide`'s own,
built in whenever it actually calls the SAT solver, because the solver's
certificate is read back in by compiled code. So "re-prove them with
`bv_decide`" is a no-op on its own terms. The measurement that answers the
question behind it was run instead. The only route out of that trust class is
a goal closed WITHOUT the solver, and `bv_decide`'s own rewriting stage is a
tactic in its own right; every row carrying the axiom was re-posed with the
model definitions unfolded and that stage alone. None closed. The population
also grew from 61 to 72, because 11 of the 19 newly-proved rows need the
solver (the other 8 close in the rewriting stage, in the stronger class).

---

## 1. What the objects are, one sentence each, in relation

- **the check** (`model_translate.py check`, then `run`) — one Lean theorem
  per single-opcode compiled unit that carries its own proved term, saying
  that the term equals the model's operations applied in the order the unit's
  own body spells them.
- **the stored line** (`layer5_normalized_text` on a unit's term66 record) —
  the unit's proved term as the pipeline printed it, one line, with its free
  symbols already renamed `v0`, `v1`, …; it is the LEFT of every theorem and
  this task did not touch it.
- **the composer** (`compose_body` and `bound_variables` in
  `model_translate.py`) — the code that builds the RIGHT of a theorem by
  walking the unit's body and applying one model definition per line, and
  that decides which bound variable stands where an arrival is read.
- **`term.Term.normalize`** (`PseudoCoupHQ/Research/op_pipeline/term.py`)
  — the pipeline's fixed print rule, and therefore the rule that gave the
  stored line its `v0`/`v1`: order the commutative operators' arguments,
  simplify, order again, number the free symbols in first-met printed order,
  substitute, simplify and order once more, print on one line.
- **`order_commutative`** (same file) — a term to the same term with every
  commutative operator's arguments in an order computed from the arguments
  themselves, so the printed text is a function of the unit and not of what
  the solver built earlier; task t104 moved the first call of it to BEFORE
  the first simplify on 2026-09-07.
- **a DISCREPANCY** — a row whose theorem the bit-blasting tactic answered
  with a concrete counterexample; L2's 19 were all of this kind and all 19
  were the naming defect above.
- **the trust class of a proof** — what a proved theorem depends on beside
  Lean's kernel, read off `#print axioms`: nothing, Lean's own axioms, or
  those plus `Lean.ofReduceBool` and `Lean.trustCompiler`, which admit the
  answer of compiled code and so trust the Lean COMPILER as well.

---

## 2. The 19, verified on the rows BEFORE anything was changed

Lane `l3_l2_verify_the_nineteen_b.sh` reads `check_L2.json`, re-transcribes
each unit's term from the store, and computes the naming under each of the
two rules. It writes nothing. Host log
`<runs>/l3/agent/logs/20260910T024432Z__l3_l2_verify_the_nineteen_b.sh.log`.

### 2.1 One row, walked

**LITERAL**, that lane, the `c/op_113` block:

```
   ---- ModelCheck_c_0   c/op_113  row 0  mnem 'add'  NAMING DIFFERS
      body_verbatim:
         mov %esi,%eax
         add %rdi,%rax
         ret
      arrival_contract_bindings (the LEDGER's own arrival rows):
         [{'bound_to_the_same_symbol_as': '%rdi', 'row': 'IN-0', 'size': 8}, {'bound_to_the_same_symbol_as': '%rsi', 'row': 'IN-1', 'size': 8}]
      result_family 'rax'  result_width 64
      stored layer-5 text (LEFT of the theorem, LITERAL):
         Concat(0, Extract(31, 0, v0)) + v1
      rule S (the stored text's rule)  : [('seed_rsi', 'v0'), ('seed_rdi', 'v1')]
      rule C (the check's composer)    : [('seed_rdi', 'v0'), ('seed_rsi', 'v1')]
      check_L2 left  : (((0#32) ++ (v0.extractLsb 31 0)) + v1)
      check_L2 right : (model_add_52 (model_mov_15 v1) v0)
```

**GLOSS.** The body moves the low 32 bits of `%rsi` into `%eax`, which on
this machine zeroes the upper half of `%rax`, and adds `%rdi`. The stored
line says `Concat(0, Extract(31, 0, v0)) + v1`, so the register whose low
half is extracted — `%rsi` — is the one the stored line calls `v0`, and rule S
agrees. The check called `%rdi` `v0` (rule C), so its right-hand side
extracted the low half of `v1`. The two sides disagree about nothing but
which name is on which arrival, and the tactic duly produced a
counterexample.

### 2.2 The direction is not fixed, which is what the reading has to explain

**LITERAL**, same lane, the `cpp/op_133` block, cut to the four lines that
carry it:

```
   ---- ModelCheck_cpp_1   cpp/op_133  row 1  mnem 'add'  NAMING DIFFERS
      body_verbatim:
         mov %edi,%eax
         add %rsi,%rax
      rule S (the stored text's rule)  : [('seed_rdi', 'v0'), ('seed_rsi', 'v1')]
      rule C (the check's composer)    : [('seed_rsi', 'v0'), ('seed_rdi', 'v1')]
```

**GLOSS.** Same two arrivals, same ledger rows, and the two rules swap the
other way. Rule C is not "the C parameter convention" (it gives `%rsi` `v0`
here and `%rdi` `v0` in §2.1) and rule S is not ledger order (it gives `%rsi`
`v0` in §2.1, where IN-0 is `%rdi`). Both are print-order rules over
different terms.

### 2.3 The two rules over the whole population

**LITERAL**, same lane, §[3/4] and §[4/4]:

```
   the 19: 0 row(s) with the SAME naming, 19 with DIFFERENT naming
   the control sample: 12 row(s) with the SAME naming, 0 with DIFFERENT naming

   rows with a proved term: 243
   same naming under both rules : 214
   different naming             : 29
   skipped (no store record / no proved term / no term): 16
   by (outcome, closed_by, naming agrees):
      ('DISCREPANCY', None, False)             19
      ('REFUSED', None, False)                 10
      ('REFUSED', None, True)                  61
      ('STATED', 'bv_decide', True)            114
      ('STATED', 'rfl', True)                  39
```

**GLOSS.** Every row the two rules disagree on is a DISCREPANCY or a row
already refused for another cause, and every row that proved is a row they
agreed on. The control sample of twelve proved rows was taken by POSITION
over the proved list, never by mnemonic, so nothing about the sample comes
from an operator token. That is the whole finding: the 19 are exactly the
naming disagreement and nothing else is.

---

## 3. The one function, and what the composer does now

The change is inside `bound_variables` in
`PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py`,
which is the one shared file this brief authorises and the composer is the
only part of it touched.

**LITERAL**, the body of the function as it now stands:

```
    ordered = TRM.order_commutative(unit_term)
    ordered = z3.simplify(ordered)
    ordered = TRM.order_commutative(ordered)
    symbols = TRM.ordered_symbols(ordered)
    names = {}
    widths = []
    substitution = []
    for index, symbol in enumerate(symbols):
        fresh_name = "v%d" % index
        names[symbol.decl().name()] = fresh_name
        widths.append(sort_width(symbol))
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec(fresh_name, symbol.size())
        else:
            fresh = z3.Const(fresh_name, symbol.sort())
        substitution.append((symbol, fresh))
    if stored is not None:
        renamed = ordered
        if substitution:
            renamed = z3.substitute(renamed, *substitution)
        renamed = z3.simplify(renamed)
        renamed = TRM.order_commutative(renamed)
        printed = TRM.one_line(renamed)
        if printed != stored:
            raise Refused("NAMING_NOT_THE_STORED_ONE",
                          "the names this composer gives the arrivals print "
                          "%r, and the stored line is %r" % (printed, stored))
    return names, widths
```

**GLOSS.** `TRM` is `term.py`, imported read-only; `order_commutative` and
`ordered_symbols` are its own functions and the rule is not restated here.
The `stored is not None` block is the per-row proof: the naming has to
reproduce the stored line character for character or the row is refused by
cause `NAMING_NOT_THE_STORED_ONE` instead of being carried into a theorem.
Zero rows took that refusal.

**The tally, before and after** (lane `l3_l3_check_with_the_one_naming.sh`,
host log
`<runs>/l3/agent/logs/20260910T024551Z__l3_l3_check_with_the_one_naming.sh.log`,
§[1/3]; and §9 [1/8] below for the after, re-runnable):

| what | task L2 left it | task l3 leaves it |
|---|---|---|
| rows | 259 | 259 |
| STATED | 153 | **172** |
| — closed by `rfl` | 39 | 39 |
| — closed by `bv_decide` | 114 | 133 |
| REFUSED | 87 | 87 |
| DISCREPANCY | 19 | **0** |

**THE NEW GUARD VALUE IS `259 / 172 / 87`, DISCREPANCY 0.** The check as L2
left it is kept beside the new one as
`PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json.before_task_l3`,
so the before/after is auditable without git.

---

## 4. The per-row fate of the 19

Every one is STATED and proved. **Table 1**, from the final `check_L2.json`
(§9 [3/8] re-runs the fates in one line each):

| theorem | unit | mnem | outcome now | closed by | wall s | peak kB | native-evaluation axiom |
|---|---|---|---|---|---|---|---|
| ModelCheck_c_0 | c/op_113 | `add` | STATED | bv_decide | 0.458 | 464992 | no |
| ModelCheck_c_1 | c/op_133 | `add` | STATED | bv_decide | 0.446 | 469324 | no |
| ModelCheck_c_22 | c/regen_8997 | `imul` | STATED | bv_decide | 0.459 | 470724 | no |
| ModelCheck_c_23 | c/regen_9822 | `imul` | STATED | bv_decide | 0.448 | 466388 | no |
| ModelCheck_c_68 | c/op_138 | `sub` | STATED | bv_decide | 0.832 | 498280 | yes |
| ModelCheck_c_69 | c/op_145 | `sub` | STATED | bv_decide | 0.826 | 497324 | yes |
| ModelCheck_c_70 | c/op_149 | `sub` | STATED | bv_decide | 0.845 | 502916 | yes |
| ModelCheck_cpp_0 | cpp/op_113 | `add` | STATED | bv_decide | 0.416 | 464744 | no |
| ModelCheck_cpp_1 | cpp/op_133 | `add` | STATED | bv_decide | 0.421 | 468180 | no |
| ModelCheck_cpp_22 | cpp/regen_8581 | `imul` | STATED | bv_decide | 0.412 | 466408 | no |
| ModelCheck_cpp_23 | cpp/regen_8966 | `imul` | STATED | bv_decide | 0.404 | 473760 | no |
| ModelCheck_cpp_67 | cpp/op_138 | `sub` | STATED | bv_decide | 0.894 | 495668 | yes |
| ModelCheck_cpp_68 | cpp/op_145 | `sub` | STATED | bv_decide | 0.902 | 499288 | yes |
| ModelCheck_cpp_69 | cpp/op_149 | `sub` | STATED | bv_decide | 0.924 | 498436 | yes |
| ModelCheck_go_20 | go/op_348 | `sub` | STATED | bv_decide | 0.962 | 498464 | yes |
| ModelCheck_go_21 | go/op_355 | `sub` | STATED | bv_decide | 0.941 | 500228 | yes |
| ModelCheck_rust_39 | rust/op_570 | `sub` | STATED | bv_decide | 0.988 | 496524 | yes |
| ModelCheck_rust_40 | rust/op_577 | `sub` | STATED | bv_decide | 0.911 | 498020 | yes |
| ModelCheck_rust_41 | rust/regen_1043 | `sub` | STATED | bv_decide | 0.907 | 496260 | yes |

The two sides of `ModelCheck_c_0` now read, **LITERAL**, lane
`l3_l3_check_with_the_one_naming.sh` §[3/3]:

```
   c/op_113           STATED       ModelCheck_c_0
      left  : (((0#32) ++ (v0.extractLsb 31 0)) + v1)
      right : (model_add_49 (model_mov_16 v0) v1)
```

**GLOSS.** `v0` is now the same arrival on both sides — the register whose
low half the `mov` takes. The definition numbers moved from `model_add_52` to
`model_add_49` because task ap5 widened the sweep's operand shapes on
2026-09-09 and this task re-ran the sweep (§6.1); the definitions themselves
are the reference's, unchanged.

---

## 5. Native evaluation: what the 61 actually is, and the measurement

### 5.1 The brief's premise, checked against the artifacts

Three claims in the brief's §2, each checked:

- **"L1 proved some edges by native evaluation."** No. `native_decide`
  occurs zero times in the whole `archproof` project; the only tactic words
  are `bv_decide` (158) and one `decide`. **LITERAL**, lane
  `l3_l5_native_evaluation_census.sh` §[1/6], host log
  `<runs>/l3/agent/logs/20260910T025449Z__l3_l5_native_evaluation_census.sh.log`:
  ```
      158 bv_decide
        1 decide
  ```
  L1's own result files (`L1_ten_edges.json`, `L1_three_undecided.json`,
  `L1_divide_ladder*.json`) record an outcome and a wall clock per row and no
  axioms field at all (same lane, §[3/6]).
- **"log_227 recorded 61."** No: the 61 is log 232 §6's axiom-line census
  over the CHECK's rows, not an L1 figure.
- **"re-prove each with `bv_decide`."** They already were. All 61 were rows
  `run_command` closed with `bv_decide`; the axiom rides along with the
  tactic.

### 5.2 Why the axiom is `bv_decide`'s own and no configuration turns it off

**LITERAL**, the installed toolchain's own source, lane
`l3_l6_read_the_toolchain_on_native_evaluation.sh` §[3/5] (§9 [6/8] re-runs
it):

```
/opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean:298:      (mkConst ``Lean.ofReduceBool)
/opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean:310:    throwError m!"Failed to check the LRAT certificate in the kernel:\n{e.toMessageData}"
```

**GLOSS.** The tactic builds an application of the axiom `Lean.ofReduceBool`
and then has the kernel type-check it: the certificate is checked in the
kernel, but the certificate itself is READ IN by compiled code, which is what
the axiom admits. `BVDecideConfig` (`Std/Tactic/BVDecide/Syntax.lean` lines
21-71) has ten fields — `timeout`, `trimProofs`, `binaryProofs`, `acNf`,
`andFlattening`, `embeddedConstraintSubst`, `structures`, `fixedInt`,
`enums`, `graphviz`, `maxSteps`, `shortCircuit` — and not one of them turns
that path off. A row closed inside the tactic's REWRITING stage never reaches
the solver and so carries no such axiom; that stage is `bv_normalize`, a
tactic in its own right (`Syntax.lean` line 98).

### 5.3 The attempt, and how many moved

Every row carrying the axiom was re-posed with the same model definitions
unfolded and `bv_normalize` alone, one `lean` process each, into one scratch
theorem file so that nothing already proved was disturbed. Lane
`l3_l9_trust_classes_guard_and_build.sh`, host log
`<runs>/l3/agent/logs/20260910T031250Z__l3_l9_trust_classes_guard_and_build.sh.log`,
§[1/6], **LITERAL**:

```
   before: proved 153, native-evaluation axiom on 61
   after : proved 172, native-evaluation axiom on 72
   attempted 72; moved to the stronger class 0; kept bv_decide 72
   attempts wall 26.2 s total, highest peak RSS 473732 kB
```

**ZERO of the 72 moved.** Every attempt came back `unsolved goals`; the
per-row outcome, wall clock, peak RSS, tactic and Lean output are one record
each in
`PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json`.
The 61 the brief names are all still in the weaker class and all 61 are still
proved.

**Why 72 and not 61**, stated as a contrast rather than a change of subject:

- **Was 61 (task L2's check).** 114 rows closed by `bv_decide`, of which 61
  needed the solver.
- **Is 72 (this task's check).** 133 rows closed by `bv_decide`, of which 72
  needed the solver. The 11 new ones are exactly the `sub` rows among the 19:
  `ModelCheck_c_68/69/70`, `ModelCheck_cpp_67/68/69`, `ModelCheck_go_20/21`,
  `ModelCheck_rust_39/40/41`. The other 8 of the 19 — the `add` and `imul`
  rows — close in the rewriting stage and land in the STRONGER class.

### 5.4 The four trust classes over the 172 proved theorems

**Table 2**, from the final `check_L2.json` (§9 [4/8] re-runs it). None
depends on `sorryAx`; `grep -rln sorry` over every `.lean` file of the
project matches nothing (lane 9 §[4/6]).

| axioms as `#print axioms` gives them | tactic | count | what it trusts beside the kernel |
|---|---|---|---|
| does not depend on any axioms | `rfl` | 20 | nothing |
| `propext, Quot.sound` | `rfl` | 19 | nothing beyond Lean's own |
| `propext, Classical.choice, Quot.sound` | `bv_decide`, no solver call | 61 | nothing beyond Lean's own |
| `propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound` | `bv_decide`, solver called | 72 | the Lean compiler |

---

## 6. The artifact as this task leaves it

### 6.1 The sweep was re-run so the census describes the file on disk

Task ap5 (log 249) widened `model_translate.shapes_for` with four
symbolic-immediate shapes on 2026-09-09 and restored every file it touched,
so `model_L2.json` on disk was the census of the sweep BEFORE that widening
while any fresh `check` writes a `Model.lean` from the sweep AFTER it. Lane
`l3_l8_model_check_run_in_order.sh` ran `model`, then `check`, then `run`, in
that order, so the census and the file agree. **LITERAL**, that lane §[4/5]
and §[5/5], host log
`<runs>/l3/agent/logs/20260910T025940Z__l3_l8_model_check_run_in_order.sh.log`:

```
   mnemonics in the reference table : 173
   definitions in model_L2.json     : 4135
   opaque float primitives          : 27
   a census row, no builder         : 6
   at least one shape translated    : 162
   builder, no shape this sweep spells: 5
   check rows 259
   REFUSED        87
   bv_decide      133
   rfl            39
   STATED 172   REFUSED 87   DISCREPANCY 0
4175
16669 archproof/Archproof/Model.lean
```

**GLOSS.** 4135 definitions from the sweep, 13 more added by the check for
body lines the sweep's shapes do not spell (4148), plus the 27 opaque float
primitives, is the 4175 `def`/`opaque` lines in `Model.lean`. The 162
mnemonics with at least one translated shape is the same 162 the
arch_unit_oracle line's vocabulary names.

### 6.2 The build and the sorry keyword

**LITERAL**, lane `l3_l9_trust_classes_guard_and_build.sh` §[3/6] — `lake
build` of the whole project, exit 0, 318 jobs:

```
✔ [313/318] Built Archproof (335ms)
✔ [315/318] Built Main (351ms)
✔ [317/318] Built Archproof.Model:c.o (18s)
✔ [318/318] Built archproof:exe (165ms)
Build completed successfully (318 jobs).
```

`grep -rln sorry` over every `.lean` file of the project: no match (lane 9
§[4/6], `grep exit 1`).

### 6.3 The spelling-ban guard, pasted verbatim as required

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
> second violation).** No operator token may appear in ANY key, grouping,
> pairing, row structure, candidate selection, or comparison scope, anywhere
> in this line — not in matching, not in "which pairs get compared", not in
> report rows, not in dropdowns. The candidate set for comparison comes from
> machine-form evidence (clusters, connections, type pairs) or from ratified
> intention — never from the token. The token appears exactly once per unit:
> as a display label on the member. HISTORY OF VIOLATIONS, so the pattern is
> visible: (1) the arch campaign's cross-language matrix (caught by the owner
> 2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 — the
> fix brief itself reintroduced it as "same-operator pairs"). MECHANICAL
> GUARD REQUIRED: every pipeline stage that groups or pairs units must run
> the spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
> its own output on failure. A brief handed to any subagent for this line
> MUST paste this paragraph verbatim.

**LITERAL**, lane `l3_l9_trust_classes_guard_and_build.sh` §[5/6] — the guard
run unmodified over every json this task wrote, its output filtered to the
verdict lines by the lane's own `grep -E "^(FAIL|PASS)"` (§9 [7/8] re-runs
the two that pass, unfiltered):

```
PASS check_L2.json -- no operator token in any key, grouping, pairing or row structure
PASS l3_trust_classes.json -- no operator token in any key, grouping, pairing or row structure
FAIL model_L2.json -- 24520 spelling-keyed place(s)
```

`model_L2.json`'s failure is log 232 §7's, unchanged in kind and larger in
count only because the sweep now writes more rows: `per_mnemonic` is keyed by
the reference's own opcode mnemonics and `flag_setter` names which mnemonic's
flag rule a flags definition uses, and four of the reference's mnemonic
spellings (`and`, `not`, `or`, `xor`) are also entries in the guard's
cross-language operator inventory. Nothing was renamed or restructured to
route around it; it is still awaiting the owner (§8).

`grep -c exempt` over every file this task added: **0** on
`l3_trust_classes.json` and on eight of the nine lane scripts; the ninth is
`l3_l9_trust_classes_guard_and_build.sh` with 2, which are the lane's own
`echo` of the phrase and the `grep -c exempt` command itself, on lines 135
and 136 of that script — no exemption in any data.

---

## 7. What was NOT done, by this task's own stop rules

- **`term.py` was not modified.** The composer CALLS its two functions; the
  naming rule keeps one definition, in the module that owns it.
- **`reference.py` was not modified**, and no Lean definition was written by
  hand: every one of the 4175 in `Model.lean` came from the sweep or from the
  check's own composition of a body line.
- **No theorem statement or tactic was edited to make a row pass.** The 19
  prove because the composer names the arrivals correctly, and the tactic
  sequence (`rfl`, then unfold and bit-blast) is L2's, unchanged.
- **The 72 rows carrying the native-evaluation axiom were not re-labelled.**
  The attempt to move them failed and is reported as failing.
- **The spelling guard was not modified** and `model_L2.json`'s failure was
  not worked around.
- **Nothing outside `Research/op_pipeline/lean/` was written**, apart from
  the one authorised composer inside `model_translate.py` (which lives in
  that folder), this log, and the lean node's PROGRESS.
- **No Mathlib, no network**: `l3.conf` runs `proxy = no`, and `lake build`
  built 318 jobs with no route out.

---

## 8. Two lists

**Decided, recorded for audit:**

- The coordinator's reading of the 19 is corrected, not implemented: neither
  side named arrivals by the C parameter convention and neither by ledger
  arrival order; both are print-order rules, and the defect was that they
  print different terms (§2). The correction was made on the rows before the
  composer was touched.
- The one function is `term.Term.normalize`'s own rule, reached by calling
  `term.py`'s `order_commutative` and `ordered_symbols`, because the LEFT of
  every theorem is the stored line and its naming is not this task's to
  change.
- The naming is PROVED per row against the stored line, with the refusal
  cause `NAMING_NOT_THE_STORED_ONE` if it ever fails to reproduce it. Zero
  rows took it. This is a new refusal cause on a row of `check_L2.json`; it
  names a defect, not a new outcome — the outcome is the existing `REFUSED`.
- `model_translate.py model` was re-run before the check so `model_L2.json`
  describes the `Model.lean` on disk after task ap5's widened shapes (§6.1).
- The check as task L2 left it is kept as `check_L2.json.before_task_l3`.
- The brief's §2 was answered by the measurement its question implies, since
  its literal instruction ("re-prove the 61 with `bv_decide`") is a no-op:
  they were already `bv_decide` proofs (§5.1).

**Awaiting the owner:**

- Whether the spelling-ban guard's scope covers `model_L2.json`'s
  `per_mnemonic` keys and `flag_setter` values — log 232 §9's open item,
  unchanged and unresolved by this task.
- Whether the 72 theorems that trust the Lean compiler are acceptable as
  they stand, given that Lean 4.24's `bv_decide` offers no route out and the
  alternative is a lemma library (the lean node's own "cache patterns →
  lemmas", log 228 §4.1) that does not exist yet.

---

## 9. The same facts as commands that re-run

Run by `l3_l10_rerunnable_claims.sh` (host log named in §10); working
directory `PseudoCoupHQ`.

**[1/8] The check's tally over the 259 rows — the new guard value:**

```
$ python3 -c 'import collections, json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); rows = d["rows"]; t = collections.Counter(r.get("closed_by") or r.get("outcome") for r in rows); print("rows", len(rows)); print("STATED", sum(1 for r in rows if r["outcome"] == "STATED")); print("REFUSED", sum(1 for r in rows if r["outcome"] == "REFUSED")); print("DISCREPANCY", sum(1 for r in rows if r["outcome"] == "DISCREPANCY")); [print(" ", k, t[k]) for k in sorted(t, key=str)]'
rows 259
STATED 172
REFUSED 87
DISCREPANCY 0
  REFUSED 87
  bv_decide 133
  rfl 39
```

**[2/8] The same tally over the check as task L2 left it:**

```
$ python3 -c 'import collections, json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json.before_task_l3")); rows = d["rows"]; t = collections.Counter(r.get("closed_by") or r.get("outcome") for r in rows); print("rows", len(rows)); print("STATED", sum(1 for r in rows if r["outcome"] == "STATED")); print("REFUSED", sum(1 for r in rows if r["outcome"] == "REFUSED")); print("DISCREPANCY", sum(1 for r in rows if r["outcome"] == "DISCREPANCY")); [print(" ", k, t[k]) for k in sorted(t, key=str)]'
rows 259
STATED 153
REFUSED 87
DISCREPANCY 19
  DISCREPANCY 19
  REFUSED 87
  bv_decide 114
  rfl 39
```

**[3/8] The per-row fate of the 19 (Table 1's outcome columns):**

```
$ python3 -c 'import json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json.before_task_l3")); was = sorted(r["unit"] for r in d["rows"] if r["outcome"] == "DISCREPANCY"); e = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); by = dict((r["unit"], r) for r in e["rows"]); print(len(was)); [print(u, by[u]["theorem_name"], by[u]["outcome"], by[u]["closed_by"], "native" if "ofReduceBool" in (by[u]["axioms"] or "") else "kernel-only") for u in was]'
19
c/op_113 ModelCheck_c_0 STATED bv_decide kernel-only
c/op_133 ModelCheck_c_1 STATED bv_decide kernel-only
c/op_138 ModelCheck_c_68 STATED bv_decide native
c/op_145 ModelCheck_c_69 STATED bv_decide native
c/op_149 ModelCheck_c_70 STATED bv_decide native
c/regen_8997 ModelCheck_c_22 STATED bv_decide kernel-only
c/regen_9822 ModelCheck_c_23 STATED bv_decide kernel-only
cpp/op_113 ModelCheck_cpp_0 STATED bv_decide kernel-only
cpp/op_133 ModelCheck_cpp_1 STATED bv_decide kernel-only
cpp/op_138 ModelCheck_cpp_67 STATED bv_decide native
cpp/op_145 ModelCheck_cpp_68 STATED bv_decide native
cpp/op_149 ModelCheck_cpp_69 STATED bv_decide native
cpp/regen_8581 ModelCheck_cpp_22 STATED bv_decide kernel-only
cpp/regen_8966 ModelCheck_cpp_23 STATED bv_decide kernel-only
go/op_348 ModelCheck_go_20 STATED bv_decide native
go/op_355 ModelCheck_go_21 STATED bv_decide native
rust/op_570 ModelCheck_rust_39 STATED bv_decide native
rust/op_577 ModelCheck_rust_40 STATED bv_decide native
rust/regen_1043 ModelCheck_rust_41 STATED bv_decide native
```

**[4/8] Table 2, the four trust classes over the 172 proved theorems:**

```
$ python3 -c 'import collections, json, re; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json")); p = [r for r in d["rows"] if r.get("closed_by")]; print("proved", len(p), "missing", sum(1 for r in p if not r.get("axioms")), "sorryAx", sum(1 for r in p if "sorryAx" in (r.get("axioms") or ""))); t = collections.Counter((r["closed_by"], re.sub(chr(39) + "[^" + chr(39) + "]+" + chr(39), "THEOREM", r["axioms"])) for r in p); [print(t[k], k) for k in sorted(t, key=str)]'
proved 172 missing 0 sorryAx 0
72 ('bv_decide', 'THEOREM depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]')
61 ('bv_decide', 'THEOREM depends on axioms: [propext, Classical.choice, Quot.sound]')
19 ('rfl', 'THEOREM depends on axioms: [propext, Quot.sound]')
20 ('rfl', 'THEOREM does not depend on any axioms')
```

**[5/8] The stronger-class attempt, off `l3_trust_classes.json`:**

```
$ python3 -c 'import json; d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json")); a = d["attempts"]; print("before", len(d["rows_carrying_ofReduceBool_before"])); print("after", len(d["rows_carrying_ofReduceBool_after"])); print("attempted", len(a)); print("moved", sum(1 for r in a if r["moved_to_the_stronger_class"])); print("kept bv_decide", sum(1 for r in a if not r["moved_to_the_stronger_class"])); print("outcomes", sorted(set(r["bv_normalize_attempt"]["outcome"] for r in a)))'
before 61
after 72
attempted 72
moved 0
kept bv_decide 72
outcomes ['LEAN_REFUSED']
```

**[6/8] Where `Lean.ofReduceBool` enters, in the toolchain's own source:**

```
$ grep -c ofReduceBool /opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean
1
```

**[7/8] The spelling-ban guard over the two json files this task wrote that
it passes** (`model_L2.json`'s failure is quoted in §6.3 and is log 232 §7's
open item):

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS check_L2.json -- no operator token in any key, grouping, pairing or row structure
PASS l3_trust_classes.json -- no operator token in any key, grouping, pairing or row structure
```

**[8/8] `native_decide` in the project, over every `.lean` file it holds:**

```
$ python3 -c 'import os; paths = sorted(os.path.join(r, f) for r, ds, fs in os.walk("PseudoCoupHQ/Research/op_pipeline/lean/archproof") for f in fs if f.endswith(".lean")); print("lean files", len(paths)); print("native_decide", sum(open(p).read().count("native_decide") for p in paths)); print("bv_decide", sum(open(p).read().count("bv_decide") for p in paths))'
lean files 197
native_decide 0
bv_decide 158
```

---

## 10. Verifier tally

`check_conventions_log_claims.py`, unmodified, run FROM the l3 instance over
this log. Two passes. Pass 1 (`l3_l11_verify.sh`, host log
`<runs>/l3/agent/logs/20260910T031955Z__l3_l11_verify.sh.log`)
read 28 claims, 8 MATCHES, **0 DIFFERS**, and named two blocks in §6 as
`pasted_without_source` — the `lake build` transcript and the guard
transcript, both of which named their lane in the prose above them but not in
a lead-in the checker recognises. Both were given a `**LITERAL**` lead-in
naming the lane and the section, and pass 2 (`l3_l12_verify2.sh`, host log
`<runs>/l3/agent/logs/20260910T032138Z__l3_l12_verify2.sh.log`)
reads, **LITERAL**:

```
population: 28 claims across 1 logs
  MATCHES          8
  DIFFERS          0
  UNVERIFIABLE     20
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 8 of 28 claims reproduce; 20 (71%) carry nothing to re-run

causes, by name:
  prose_only                       10
  attribution_only                 10
```

**TALLY LINE: claims 28 | MATCHES 8 | DIFFERS 0 | UNVERIFIABLE 20 | REFUSED 0
| NOT_RERUNNABLE 0. Zero DIFFERS.** The 8 MATCHES are §9's eight commands.
The 20 UNVERIFIABLE are ten prose sentences and ten attributions, each of the
latter carrying its host lane log path. A third pass with this section present
(`l3_l13_verify3.sh`, host log
`<runs>/l3/agent/logs/20260910T032349Z__l3_l13_verify3.sh.log`)
reads 30 claims, 8 MATCHES, **0 DIFFERS**, 22 UNVERIFIABLE — the two extra
claims are this section's own prose and its own pasted tally. It is not
pasted here as a live transcript, because a transcript that compares its own
output to itself is the self-reference log 232 §11 hit.

---

## 11. See also

- `PseudoCoupHQ/Research/op_pipeline/lean/README.md` — the
  check's tally, what it means, and the trust classes, as reference
  documentation rather than an account of a day.
- `PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py` —
  the translator and the checker; `bound_variables` is the only part this
  task changed.
- `PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json` — the
  259-row population as this task leaves it, and
  `check_L2.json.before_task_l3` as task L2 left it.
- `PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json`
  — one record per row carrying the native-evaluation axiom, with the
  attempt to close it without the SAT solver.
- `PseudoCoupHQ/Research/op_pipeline/lean/lanes_l3/` — all nine
  lane scripts, in submission order.
- `PseudoCoupHQ/DevComms/log_232_task_L2_model_translator.md`
  §5 — the 19 as task L2 recorded them, and §7 the guard finding this task
  inherits.
- `PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md`
  — the `archproof` project this check builds inside; §4 is where the brief's
  "61 native-evaluation proofs" was expected and is not.
- `PseudoCoupHQ/DevComms/log_249_task_ap5_autopoly_fifth_pass.md`
  §2.2 — the widened `shapes_for` this task re-ran the sweep for, and §8.1
  the guard reading of `check` at `259 / 172 / 87` that this task's tally
  keeps.
