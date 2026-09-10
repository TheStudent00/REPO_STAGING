# Research/op_pipeline/lean

Lean 4 as a second discharger of the gate's proof obligations, beside z3.
Node: `hq.research.compiler_graph.gate.lean`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`).
Opened 2026-09-07; task L1 filled it. The full account is
`PRIVATE/PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md`.

## what is in here

- `archproof/` — a `lake` project, core Lean 4 only, no Mathlib and no
  network. `lake new archproof` created it inside a lane with no route out.
  - `Archproof/Smoke.lean` — one 32-bit identity, the smallest check that the
    toolchain proves anything.
  - `Archproof/Api.lean` — every Lean `BitVec` name this task emits, checked
    for existence and type rather than remembered, plus the `#eval`s that
    measured where Lean's arithmetic and SMT-LIB's disagree.
  - `Archproof/Render.lean` — the term language, its evaluation, a C integer
    expression language, its evaluation, the rendering between them, and the
    preservation theorem. 374 lines, no `sorry`, `#print axioms` clean.
  - `Edges/` — one generated file per theorem this task ran.
- `term_to_lean.py` — one printed layer-5 term text to one Lean `BitVec`
  expression: parse, infer the widths the printed form drops, REBUILD THE TERM
  IN Z3 AND DEMAND ITS PRINTER GIVE THE INPUT BACK, then emit Lean. The
  round-trip is what makes the parse checked rather than trusted.
- `edges_L1.py` — reads t100's answered pairs (`pool100_edges.json`), fixes
  which pairs go to Lean, and counts the operators the term walk emits over
  the whole pool.
- `run_edges_L1.py` — states each selected pair as a theorem, runs each in its
  own `lean` process, and records that process's wall clock and peak memory.
- `lanes_L1/` — all 27 lane scripts, in the order submitted.
- `L1_edges_selected.json`, `L1_ten_edges.json`, `L1_three_undecided.json`,
  `L1_divide_ladder.json`, `L1_divide_ladder_t600.json` — the results.

## what the first runs found

- **The install works and needs no network.** Lean 4.24.0 via elan at
  `/opt/elan`; `lake new` and `lake build` both run with `proxy = no`.
- **Eight of the ten pairs are proved by Lean's kernel**, each in about a
  fifth of a second. The other two are floating point and are refused BY
  CAUSE: `bv_decide` bit-blasts bit-vectors and has no floating-point theory.
- **The preservation theorem is proved for the whole integer subset** — all
  eighteen constructors, by structural induction, no `sorry`.
- **Lean's division and SMT-LIB's division are different functions at a zero
  divisor.** `(7#8) / (0#8)` is `0x00#8` in Lean; SMT-LIB's `bvudiv` answers
  all ones. Remainder and the three shifts agree.
- **Division is where bit-blasting gets expensive, and where three different
  ceilings each look like the answer until they are raised.** The division
  identity proves at 8 bits in half a second. At 16 bits it stopped first on
  the SAT solver's 10-second default, then on Lean's elaborator heartbeat
  limit, then on the instance's 1 GiB `/tmp` — which had truncated a proof
  certificate of 1,073,500,160 bytes. With `/tmp` at 4g it PROVES, in 283
  seconds, using about 12 GB. 32 and 64 bits remain undecided at a 600-second
  SAT ceiling.

## what the C model commits to, and why it is not a copy of the term language

`evalC` answers `Option (BitVec w)`, and `none` means "this C expression has
undefined behaviour here". C leaves a shift by a count of `w` or more
undefined, so the renderer has to emit a guard, and the theorem's statement —
`evalC (render t) env = some (eval t env)` — says both that the rendered
expression is always defined and that its value is the term's. Modelling the
undefined region as a convenient number instead would have made the shift
cases hold for free.

One thing the proof forced, which is a fact about C rather than about Lean:
**C's shift count is an `int` after the usual promotions, not a value of the
shifted type.** The first C model gave the shift a count of the same holder
width, and neither the bit-slice nor the append could then be rendered at a
narrow width, because the shift amount did not fit the holder. The model
carries both forms now: a shift by a computed holder (guarded at run time) and
a shift by a plain integer (guarded when the renderer writes it).

## the single-opcode check, and what its tally means (task l3, 2026-09-09)

The check (`model_translate.py check`, then `model_translate.py run`) states
one Lean theorem per single-opcode compiled unit that carries its own proved
term. Left of the equals sign is that stored term — the LEDGER route's
reading of the unit, printed by the pipeline's own layer-5 rule. Right of it
are the model's operations, applied in the order the unit's own body spells
them. A failure is a DISCREPANCY between two readings of the hardware, never
a Lean problem.

**THE TALLY, and it is the guard value every later task states:**

| what | count |
|---|---|
| rows (the single-opcode population of the five compiled languages) | 259 |
| STATED (a theorem written and closed) | 172 |
| REFUSED (no theorem stated, by cause) | 87 |
| DISCREPANCY | 0 |

So `259 / 172 / 87`, DISCREPANCY 0. Task L2 (log 232) left it at
`259 / 153 / 87` with 19 DISCREPANCY; task l3 found those 19 to be one defect
in the check's own composer, not a disagreement about the machine, and all 19
now prove. The check_L2.json as L2 left it is kept beside the new one as
`check_L2.json.before_task_l3`.

**WHAT THE 19 WERE.** The theorem's two sides named the unit's arrivals by
two different rules. The stored line's `v0`/`v1` come from
`term.Term.normalize`, which orders every commutative operator's arguments by
a key computed from the arguments themselves BEFORE it simplifies (task t104
added that first ordering step on 2026-09-07) and then numbers the free
symbols in the order the printed text meets them. `bound_variables` in
`model_translate.py` numbered them after a plain `z3.simplify`, with neither
ordering step — the rule as it stood before t104. On a term whose commutative
operands the ordering step permutes, the two rules put the two arrivals in
opposite order, so the left called one register `v0` and the right called the
other one `v0`, and `bv_decide` answered with a counterexample about the
names. Measured over the 243 rows with a proved term: the two rules agreed on
214 and differed on 29 — the 19 and 10 rows refused for other causes.
`bound_variables` now calls `term.py`'s own `order_commutative` and
`ordered_symbols` in `term.Term.normalize`'s order, and PROVES the naming per
row: with the names substituted the term is printed by the same printer and
must give the stored line character for character, or the row is refused by
cause `NAMING_NOT_THE_STORED_ONE`.

**THE TRUST CLASSES, and how many proved theorems are in each.** Every one of
the 172 is checked by Lean's kernel and none depends on `sorryAx`
(`grep -rln sorry` over the project matches nothing). They differ in what
else they trust:

| class | what it trusts beside the kernel | tactic | count |
|---|---|---|---|
| no axiom at all | nothing | `rfl` | 20 |
| `propext, Quot.sound` | nothing beyond Lean's own axioms | `rfl` | 19 |
| `propext, Classical.choice, Quot.sound` | nothing beyond Lean's own axioms | `bv_decide`, closed in its rewriting stage | 61 |
| the four above plus `Lean.ofReduceBool, Lean.trustCompiler` | the Lean COMPILER, because the SAT solver's LRAT certificate is read back in by compiled code | `bv_decide`, with the solver called | 72 |

`Lean.ofReduceBool` is not a tactic anyone chose here: `native_decide`
appears nowhere in this project, and `bv_decide` itself builds the axiom in
whenever it calls the solver (`Lean/Elab/Tactic/BVDecide/Frontend/
BVDecide.lean`, the `mkConst ``Lean.ofReduceBool` at line 298 of the
toolchain's own source). `BVDecideConfig` has no field that turns it off. The
only route out of that class is a goal closed without the solver, so each of
the 72 was re-posed with the same model definitions unfolded and
`bv_normalize` — `bv_decide`'s own rewriting stage, a tactic in its own right
— alone: **0 of 72 closed**, every one with `unsolved goals`, the whole
attempt costing 26.2 s and peaking at 474 MB. Those 72 keep their `bv_decide`
proofs. The record, per row, with wall clock, peak RSS and the axiom line as
Lean prints it, is `l3_trust_classes.json`.
