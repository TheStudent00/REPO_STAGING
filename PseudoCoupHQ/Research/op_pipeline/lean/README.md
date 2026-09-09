# Research/op_pipeline/lean

Lean 4 as a second discharger of the gate's proof obligations, beside z3.
Node: `hq.research.compiler_graph.gate.lean`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`).
Opened 2026-09-07; task L1 filled it. The full account is
`PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md`.

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
