# Task h2 — the same handful after two printing fixes: normalise the cell's term before rendering, and render a vector cell's lane

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then `task_h1_brief.md` beside it (the handful as first run; its §5 too),
`DevComms/log_238` and `log_239` (what ran and what broke),
`Research/oracle/cross_construction/emulation/handful/handful.py` (the
driver you extend), `Research/op_pipeline/term.py` (`Term.normalize` and the
layer-5 printer; log_233 for what the normaliser does), the two renderers
(`emulation/emulate.py`, `emulation/rust/rust_render.py`), and
`Research/oracle/arch_opcodes/model/model_table.py` (`classify_line`,
`key_width`). Instance `h2.conf` (copy to the tower yourself from
`PUBLIC/Airlock/instances/h2.conf`, bring it up). Artifact folder:
the same `.../emulation/handful/`; lanes under `lanes_h2/`.

## 1. What this is
h1 found two failures, both in how a cell's term is PRINTED, not in the
route. Fix both, add one classifier rule, and re-run the SAME ten cells on
c and rust so the before/after is one table. Nothing else. the owner's rule
stands: a handful before anything long.

## 2. The three changes, each with its regression guard
1. **Normalise before rendering.** The table's terms are the builders'
   raw z3 output; for `idiv` the dividend's sign extension prints as 32
   joined `Extract(31, 31, v)` copies, and the compiler made 51
   instructions of it. Before the renderer sees a cell's term, pass it
   through the pipeline's own normaliser (`Term.normalize`, the one t104
   fixed) and render the normalised term. Show, for `idiv`, the term text
   before and after, LITERAL. Guard: the other eight cells' rendered
   sources must be unchanged or provably equal (z3, both terms); paste.
2. **Render the lane of a vector cell.** A cell whose place is an xmm
   register carries the whole 128-bit place in its term; its `key_width`
   (32 for `addss`, 64 for `cvtsi2sd`) names the lane the operation
   writes, and the other lanes are the arrival's own bits passed through.
   In the DRIVER (not in the renderers): project the place's term to
   `Extract(key_width-1, 0, place)`, render that as a `key_width`-wide
   float or integer holder, and record that the upper lanes are pass-
   through. The check then compares the carved body's low lane against
   the projected term. If a renderer still refuses (a float operator it
   has no spelling for, `fp.add` for instance), that is the result, by
   cause, LITERAL — do not extend the renderers' operator tables in this
   task beyond what a reused spelling from o7/o11 already covers.
3. **Zero-operand opcodes in the classifier**: `cqto cltq cltd cwtd cqo`
   and their like take their width from the reference's own tables
   (`SPREAD_SIGN`, `ACCUMULATOR_WIDEN`), not from an operand. Add that
   rule to `model_table.classify_line`/`key_width` (a shared file; this
   additive rule is authorised), re-run h1b's composition over the 20
   bodies, and show that `cqto` now maps to a cell and nothing else moved.

## 3. Deliverable
`handful.py` extended (a flag or a second entry point; the h1 results are
NOT overwritten: write `handful2.json`, `handful2.md`). One table, 20 rows:
cell | lang | h1 verdict | h2 verdict | landed (h2) | composition (h2) |
cause if refused. Per run, the four literal objects as in h1 §3. For
`idiv`: the before/after term texts, the instruction count of the new
body, and the gate's answer at 3,000 ms (re-pose at 300,000 ms only if
still undecided, and say so). For the two float cells: the projected term,
the rendered lane, and whatever happens next, literal.
Regression: re-run task o8's per-opcode check unchanged on its 243 rows
(its own lane script, its own artifact untouched, into a scratch copy) and
paste its four totals (243/197/155/216 expected) — the renderers were not
changed, so this is the proof of that. Guard over every json; log (next
free number, check right before writing); verifier lane; PROGRESS line on
the autopoly node; sync-back; instance down.

Memory bound 4g inside the cap; the o8 regression re-run is the only lane
that takes minutes. Stop rules per LAW. Reply with the 20-row table, the
`idiv` before/after, the o8 totals, the tally, the two lists.
