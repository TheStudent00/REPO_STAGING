# Research/op_pipeline/lean — the model translator (task L2)

The reference simulator's opcode semantics, turned into Lean `BitVec`
definitions by a program rather than by hand, then checked against every
single-opcode unit that carries a proved term. Node:
`hq.research.compiler_graph.gate.lean.model_translator`
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md`).
Opened 2026-09-06; task L2 filled it. The full account is
`~/Programming/PseudoCoupHQ/DevComms/log_232_task_L2_model_translator.md`.

## what is in here

- `model_translate.py` — the translator and the checker, five commands:
  - `table` — the rule tables (Z3 op kind -> Lean `BitVec`/`Bool` operation;
    float op kind -> the opaque primitive or the identity-on-bits seam).
  - `five` — the five opcodes the brief named, end to end, LITERAL.
  - `model` — sweeps every mnemonic in the reference's opcode table over the
    operand shapes it spells, runs that mnemonic's own builder from
    `reference.py` on symbolic seeds, and writes what came back as Lean
    definitions into `archproof/Archproof/Model.lean`; writes
    `model_L2.json` (the per-mnemonic census).
  - `check` — states, for every single-opcode row `single_opcode_units.json`
    carries a proved term for, the theorem "the unit's own term equals the
    model's operation applied to the same inputs"; writes each theorem file
    and `check_L2.json` (the per-row population and its outcome).
  - `run` — `rfl` first, `bv_decide` on what does not close definitionally,
    over every STATED row; records wall clock and peak RSS
    (`os.wait4`, per theorem, not a running maximum) and closes each row as
    `rfl` / `bv_decide` / `DISCREPANCY` / `LEAN_REFUSED`-by-cause.
  - `imports` — rewrites `Archproof.lean` to import only the CLOSED check
    modules, so `lake build` builds the proofs, not the attempts.
  - `axioms_gap` / `axioms_refresh` — added closing this task (see "two bugs
    found closing this task" below): re-run `lake env lean` on already-written
    theorem files to fill or correct `row["axioms"]`. Neither writes a new
    theorem or changes a tactic; both only read `#print axioms`'s own trace.
- `model_L2.json` — the mnemonic-level census: 171 mnemonics in the
  reference's opcode table, 3,933 Lean definitions written, 27 opaque float
  primitives declared.
- `check_L2.json` — the row-level population: 259 single-opcode rows over the
  five compiled languages (not the brief's estimate of 243 — the population
  was recomputed live off `single_opcode_units.json`, see the log's §1),
  each with its outcome, its two readings (`left`/`right`, LITERAL Lean
  terms), wall clock, peak RSS, and (for every proved row) the full
  `#print axioms` line.
- `archproof/Archproof/Model.lean` — 15,861 lines, 3,933 generated
  definitions. Never hand-written; regenerating it is `model_translate.py
  model`.
- `archproof/Archproof/ModelCheck_<lang>_<row>.lean` — one file per STATED
  row (172 files), each the two-readings theorem plus `#print axioms`.
- `lanes_L2/` — every lane script this task submitted, in submission order
  (19 scripts, `L2_l1_survey.sh` through `L2_l19_final_guard.sh`).

## the five opcodes, end to end (brief's deliverable 1, first part)

`add`, `sar`, `imul`, `ucomiss`, `cvtsi2sd` — `reference.py`'s builder run on
symbolic seeds, then the Lean definitions `model_translate.py five` produced
from that same run. Both LITERAL, in the log's §2. One line each, here:

Definition names carry a local counter (`model_<mnem>_<n>[_flags]`) that
renumbers per invocation of `five`, not a stable global id — the DevComms
log's re-run section pastes one live, current run; the definitions below
are that same run, LITERAL:

| mnemonic | shape | width | builder | Lean definition(s) |
|---|---|---|---|---|
| `add` | gpr_gpr | 64 | `build_binary` | `model_add_0 v0 v1 := v0 + v1` |
| `add` | gpr_gpr | 32 | `build_binary` | `model_add_2 v0 v1 := ((v0.extractLsb 31 0) + (v1.extractLsb 31 0)).zeroExtend 64` |
| `sar` | cl_gpr | 64 | `build_shift` | `model_sar_0 v0 v1 := v0.sshiftRight' (((v1.extractLsb 7 0) &&& 63#8).zeroExtend 64)` |
| `sar` | imm_gpr | 32 | `build_shift` | `model_sar_1 v0 := ((v0.extractLsb 31 0).sshiftRight' (((3#8) &&& 31#8)).zeroExtend 32).zeroExtend 64` |
| `imul` | gpr_gpr | 64 | `build_binary` | `model_imul_0 v0 v1 := v0 * v1` |
| `imul` | gpr_one | 64 | `build_wide_multiply` | `model_imul_2/_3 v0 v1 := ((v0.signExtend 128) * (v1.signExtend 128)).extractLsb {63 0 \| 127 64}` |
| `ucomiss` | xmm_xmm | 32 | `build_float_flag_only` | `model_ucomiss_0_flags v0 v1 := {setter:="ucomiss", L:=v0.extractLsb 31 0, R:=v1.extractLsb 31 0}` (seam NAN_PAYLOAD_SEAM) |
| `cvtsi2sd` | gpr_xmm | 32 | `build_convert_to_float` | `model_cvtsi2sd_0 v0 v1 := (v0.extractLsb 127 64) ++ (ieeeOfSIntW32ToF64Rne (v1.extractLsb 31 0))` |

## the translator over every mnemonic (brief's deliverable 1, second part)

171 mnemonics in the reference's opcode table. 160 carry at least one Lean
definition; 3,933 definitions total.

- **6 mnemonics carry no builder at all** (a census row): `call`, `jmp`,
  `pcmpeqb`, `pcmpeqd`, `pmovmskb`, `ud2`.
- **5 mnemonics have a builder but nothing this sweep's operand shapes
  spell**: `cs`, `endbr64`, `nop`, `nopl`, `ret` (zero-operand or
  prefix-only forms outside the sweep's shape grammar).
- **160 mnemonics translated at least one operand shape into a Lean
  definition**, including every floating-point mnemonic — floating point is
  TRANSLATED (the brief's own instruction: "still TRANSLATE it into
  definitions and mark the check as unavailable, not the model"), using 27
  opaque primitives for the parts z3's own FPA theory names symbolically
  rather than by formula:
  `ieeeAddF32Rne ieeeAddF64Rne ieeeAddF79Rne ieeeConvertF32ToF64Rne
  ieeeDivF32Rne ieeeDivF64Rne ieeeDivF79Rne ieeeEqF32 ieeeEqF64 ieeeIsNanF32
  ieeeIsNanF64 ieeeMulF32Rne ieeeMulF64Rne ieeeMulF79Rne
  ieeeOfSIntW128ToF32Rne ieeeOfSIntW128ToF64Rne ieeeOfSIntW16ToF32Rne
  ieeeOfSIntW16ToF64Rne ieeeOfSIntW32ToF32Rne ieeeOfSIntW32ToF64Rne
  ieeeOfSIntW64ToF32Rne ieeeOfSIntW64ToF64Rne ieeeOfSIntW8ToF32Rne
  ieeeOfSIntW8ToF64Rne ieeeSubF32Rne ieeeSubF64Rne ieeeSubF79Rne`.

No translation-level refusal carried a `cause` in this sweep (`refused: 0`
for all 171 mnemonics in `model_L2.json.per_mnemonic`) — every attempted
operand shape either translated or was `not_modelled` (a shape combination
that mnemonic's own reads/writes do not spell, not a refusal). The refusal
vocabulary the brief anticipated (`UNGUARDED_DIVISION` and friends, in the
`table` command's rule listing) appears at the CHECK level instead — see
below.

## the check over the 259 rows (brief's deliverable 2)

| outcome | count |
|---|---|
| `REFUSED` (no theorem stated) | 87 |
| `STATED`, closed by `rfl` | 39 |
| `STATED`, closed by `bv_decide` | 114 |
| `STATED`, `bv_decide` found a counterexample — **DISCREPANCY** | 19 |
| **total** | **259** |

REFUSED, by cause:

| cause | count | mnemonics |
|---|---|---|
| `FLOATING_POINT` | 44 | addsd addss divsd divss mulsd mulss subsd subss |
| `STATEFUL_PLACE_NOT_COMPOSED` | 21 | lea (16), movb (5) |
| `NO_PROVED_TERM` | 16 | call |
| `WIDTH_UNRESOLVED` | 4 | xorps |
| `RIP_CONSTANT_POSITIONAL` | 2 | pxor |

DISCREPANCY, by mnemonic: `add` 4, `imul` 4, `sub` 11 — all 19 are in
`check_L2.json`, each with its `left` (the unit's own proved term) and
`right` (the model composed over the unit's own steps) LITERAL, and the log's
§5 quotes every one.

Wall clock and peak RSS are per-theorem fields on every row
(`check_L2.json.rows[*].wall_seconds`, `.peak_kb`), from `os.wait4` on that
theorem's own `lake env lean` process. Over the 153 proved: `rfl` theorems
0.14s-0.24s, 373-385 MB; `bv_decide` theorems 0.21s-0.75s, 456-499 MB (the
heavier ones are the wider bit-blasts, `sub`/`imul` at 64 bits).

## `lake build` and `#print axioms` (brief's deliverable 3)

`lake build` of the whole project: **exit 0**, 318 jobs. `grep -rn '\bsorry\b'`
over every `.lean` file in the project: **no match** (`sorryAx` can only
appear in a `#print axioms` trace if a `sorry` term or tactic exists
somewhere in the proof or a dependency it imports, so this is what makes
"no `sorryAx`" checkable without reading all 153 traces by eye).

All 153 proved theorems carry a `#print axioms` line; **zero carry
`sorryAx`**:

| axiom set | count | closed by |
|---|---|---|
| (none — zero-axiom proof) | 20 | `rfl` |
| `propext, Quot.sound` | 19 | `rfl` |
| `propext, Classical.choice, Quot.sound` | 53 | `bv_decide` |
| `propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound` | 61 | `bv_decide` |

`Lean.ofReduceBool` and `Lean.trustCompiler` are `bv_decide`'s own trust
axioms (its LRAT certificate path, for the theorems where the certificate
needed native evaluation rather than pure kernel reduction) — present on 61
of the 114 `bv_decide`-closed theorems, absent from the other 53. Neither is
`sorryAx`; both are named so the claim "no `sorryAx`" is not confused with
"kernel-only, no bit-blasting trust assumptions", which it is not for those
61.

## two bugs found closing this task, both in the checker's own axiom-line
parser (`axiom_line` in `model_translate.py`), neither in a theorem or the
model

1. **20 proved rows came back with `row["axioms"] == None`.** `axiom_line`
   only matched `"depends on axioms"`; Lean's zero-axiom phrasing is
   `"'NAME' does not depend on any axioms"`, a different string. All 20 are
   `rfl`-closed theorems that use no axiom at all — the strongest possible
   outcome, not a gap. Fixed by matching both phrasings (lane 15's probe
   found the exact string; lane 16 re-ran the 20 and filled them).
2. **61 `bv_decide`-closed rows recorded a TRUNCATED axiom list**, e.g.
   `"... depends on axioms: [propext,"` with no closing bracket. Lean wraps a
   long axiom list over several lines; `axiom_line` returned only the first.
   This silently dropped `Lean.ofReduceBool` and `Lean.trustCompiler` from
   61 rows' recorded axioms — exactly the fact `#print axioms` exists to
   surface. Fixed by joining every wrapped line up to the one holding `]`
   (lane 17's probe found the wrap; lane 18 refreshed all 153 proved rows
   with the corrected parser).

Neither fix touched a theorem file, a tactic, or `Model.lean`; both are
read-only re-runs of `lake env lean` on files already on disk, changing only
how their (already-correct) output was parsed into `check_L2.json`.

## the spelling-ban guard, run over every json this task wrote

`check_no_spelling_keys.py` (unmodified) over `model_L2.json` and
`check_L2.json`:

- **`check_L2.json` PASSES.**
- **`model_L2.json` FAILS — 18,112 spelling-keyed places**, all in two
  shapes: (a) `$.per_mnemonic.<mnem>` dict keys for the four mnemonics that
  happen to spell an entry in the guard's 91-token operator inventory
  (`and`, `not`, `or`, `xor`); (b) `$.rows[N].flag_setter` string values
  naming which mnemonic set the flags a definition reads, for every row
  whose flag-setting mnemonic is one of those same four tokens.

This is flagged for the coordinator, not silently worked around (this
task's stop rules forbid a change to a shared file the brief did not name,
and the guard is never modified) — see the log's two-list section. The
per-mnemonic and flag-setter keys are this task's OWN domain object (the
opcode table's own mnemonic names, required by the brief's own deliverable
table), not a cross-language operator-equivalence grouping key of the kind
the ban was written against; whether that makes them exempt from the ban's
scope, or whether `model_L2.json`'s schema needs to change, is the owner's call.

## what NOT to read this artifact folder as

- `Model.lean` is GENERATED. A hand edit to it does not survive the next
  `model_translate.py model` run and is not source; `model_translate.py`
  plus `reference.py` are the source.
- The DISCREPANCY rows are not bugs in `reference.py` (this task never
  edited it) and not automatically bugs in the model translator either —
  each is, per the brief's own framing, "a discrepancy between the two
  readings of the hardware", located but not adjudicated here. The log's §5
  quotes all 19 so the adjudication has what it needs.
