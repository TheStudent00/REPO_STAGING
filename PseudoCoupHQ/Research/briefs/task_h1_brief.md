# Task h1 — a handful of `find_emulation` runs from the model table: ten cells, c and rust, every step literal

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then: the arch_unit_oracle CORE's "goal" and "Ruling, 2026-09-08" sections
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`);
`DevComms/log_220` (task o8, the per-opcode emulation as it ran) and
`log_226` (o11, rust); `Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py`
and `.../emulation/emulate.py` (the c renderer) and `.../emulation/rust/rust_render.py`;
`Research/oracle/arch_opcodes/model/model_table.md` §1 (five rows in full)
and the row shape in `model_table.json`. Instance `h1.conf` (on the tower;
bring it up). Artifact folder:
`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/`;
lanes under `lanes_h1/` there.

## 1. What this is
the owner, 2026-09-09: "id like to see how a handful of `find_emulation` runs go.
like literally just a handful. i dont want to try for long runs and find
out somethings broken or it cant find any." The loop's outer set was
measured by tasks m1/m1b: 253 attested (mnemonic, operand form, width)
cells, each with its mapping as a z3 term. Task o8 ran `find_emulation`
on SINGLETON UNITS (a unit's term → c source → clang → carve → gate
against the unit). This task runs it on CELLS OF THE TABLE, which have no
unit behind them: the check is against the cell's term itself. Ten cells,
two targets, twenty runs, every intermediate object shown.

## 2. The ten cells (all attested; take each row from model_table.json by (mnem, shape, key_width))
`add` gpr_gpr 32 · `sub` imm_gpr 64 · `imul` gpr_gpr 32 · `sar` cl_gpr 32 ·
`shr` cl_gpr 64 · `idiv` gpr_one 32 · `cmovne` gpr_gpr 32 · `setne` gpr_one 8 ·
`addss` xmm_xmm 32 · `cvtsi2sd` gpr_xmm 64.
If a cell is absent at exactly that key, take the nearest attested cell of
the same mnemonic and say which.

## 3. `find_emulation(cell, lang)`, the four steps, each an object in the log
1. **The input**: the cell's term per written place, LITERAL from the
   table (destination; flags; for `idiv` both `rax` and `rdx`; for the
   flag consumers the `setter` the cell records, and the setter's own
   cell's term, since the consumer's mapping reads the flags the setter
   wrote — render the PAIR as one function: the comparison then the
   select).
2. **Render** with the existing renderer for the target (c: `emulate.py`'s
   Renderer; rust: `rust_render.py`), from the term: source LITERAL. Where
   the renderer refuses an operator the table's terms carry (a float
   conversion, `bvsdiv_i`, a flags term), that refusal is a RESULT by cause,
   not something to work around: record it, move on. Do not extend the
   renderers in this task beyond the arity/naming glue a cell needs.
3. **Compile at ship flags and carve**, exactly as o8/o11 did: the
   object's body LITERAL, chaff-stripped body LITERAL, and LANDED /
   LANDED_ELSEWHERE / NOT_COLLAPSED against the cell's own mnemonic.
4. **The check**: the carved body run through the reference to its own
   term (the pipeline's walk), then z3: cell term == body term for every
   input, 3,000 ms ceiling, per written place (for `idiv`: quotient and
   remainder separately). Verdicts in z3's words (`unsat` = proved equal,
   `sat` with the counterexample LITERAL, `unknown`). If the walk over the
   carved body needs arrival/answer facts the body has no unit to supply,
   state the convention you used (the renderer's parameter order, the
   target's calling convention) and show it.

## 4. Deliverable
`handful.py` (the driver; nothing project-new, it wires the existing
pieces) → `handful.json`, `handful.md`: one section per run, twenty, each
with the four objects above; then ONE table, 20 rows: cell | lang | rendered
(one line, casts stripped for reading, marked GLOSS, beside the LITERAL in
the section) | landed mnemonic | gate verdict | cause if refused. Then, by
cause, what did not work. Guard over the json; log (next free number,
check right before writing); verifier lane; PROGRESS entry (append) on
`.../node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`
(create the file if the node has none; do not create the node); sync-back;
instance down.

Small task: each run is one compile and one gate call. Memory bound 4g
inside the cap; state it. Stop rules per LAW. Reply with the 20-row table
and the by-cause list, the tally, the two lists.

## 5. Added 2026-09-09 (the owner's reading, correct): the composition column
A carved body is a sequence of arch opcodes, each a cell of the model
table, so the body's term is a composition of table cells. For every run,
add a column `composition`: the carved body's instructions as the list of
table cells they are, each (mnem, shape, key_width) by the classifier m1b
used, in body order; an instruction that maps to no cell is named as such.
For a LANDED run the list is one cell, the target.
