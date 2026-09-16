# log 282 — the gate: a dozen c compiler-operators through every stage, and the eye table

2026-09-15, early. the owner: "i dont care about a handful. i want to verify
before doing long runs. especially if there is a bunch of debugging
steps and a threat of drift." This is that verification: one lane, 158
seconds on the tower (lane `lp3_l61`), twelve of c's compiler-operators
through every stage of the plan (`hq.research.lean_proof_path_resistant_to_churn`),
ending in the table below. Nothing wider has run. Nothing wider runs
until the owner has read this.

## 1. walkthrough

Twelve compiler-operators of c (every 29th of the 346 whose meaning the
corpus run certified, in manifest order; a stride over the raw manifest
lands on float probes and exercises nothing) went through: compile at
the corpus's own ship flags for riscv64, decode by Sail's own decoder,
meaning composed from Sail's definitions and certified in Lean
(`ArchUnit.meaning`); then the subterms of Sail's definitions were
proved against those meanings (`operator_for`: three keys filled);
then every arm of every certified definition was rendered from those
three keys and nothing else (`render`: three rendered, 72 refused for
want of a key); the three were compiled, read back and proved
(`equals`); and the table was written (`eye_check`). Two of the three
proved equal to their definition; the third did not, and the table
says why: the corpus unit it was built from takes an `int32_t` on the
right, so the compiler sign-extends that argument (`addiw b, b, 0`)
and the meaning read back is `a - sext32(b)`, not `a - b`. That is the
ABI risk log 281 named, shown by the machine rather than argued.

## 2. names

`compiler-operator` (the owner's) — one operator of a language, function-wrapped: a probe of the operator pipeline.
`meaning` — the compiled body of a compiler-operator read back through Sail's decoder and definitions, as one Lean expression: `ArchUnit.meaning`.
`operator_for` — the swap table: (a subterm of a Sail definition) -> the compiler-operators proved to mean it. Filled by proof only.
`render` — an emulation of a definition written by matching its tree against the table's keys and calling the units the keys hold.
D, E, U, L — Sail's definition; the rendered emulation; its instructions; the meaning read back.

## 3. the dozen and their meanings through Sail (RISC-V read as Lean expressions)

| c compiler-operator | its meaning (L), certified |
|---|---|
| `!` on int32_t | `(pure_ITYPE (a) (0x001#12) (LeanIM.iop.SLTIU))` |
| `__alignof__` on int32_t | `(pure_ITYPE (zero_reg) (((sign_extend (m := 12) (0x04#6)))) (ADDI))` |
| `++` on double | `a` |
| `-` on int64_t, int32_t | `(pure_RTYPE (a) (b) (SUB))` |
| `/` on int64_t, uint64_t | `(pure_DIV (a) (b) (true))` |
| `||` on int32_t, uint64_t | `(pure_RTYPE (zero_reg) ((pure_RTYPE (a) (b) (OR))) (LeanIM.rop.SLTU))` |
| `&&` on bool, uint64_t | `(pure_RTYPE (a) ((pure_RTYPE (zero_reg) (b) (LeanIM.rop.SLTU))) (AND))` |
| `^` on uint64_t, uint64_t | `(pure_RTYPE (a) (b) (XOR))` |
| `==` on int64_t, uint64_t | `(pure_ITYPE ((pure_RTYPE (a) (b) (XOR))) (0x001#12) (LeanIM.iop.SLTIU))` |
| `>` on int32_t, uint64_t | `(pure_RTYPE (b) (a) (LeanIM.rop.SLTU))` |
| `>=` on bool, uint64_t | `(pure_ITYPE ((pure_RTYPE (a) (b) (LeanIM.rop.SLTU))) (0x001#12) (LeanIM.iop.XORI))` |
| `<` on uint64_t, uint64_t | `(pure_RTYPE (a) (b) (LeanIM.rop.SLTU))` |

## 4. `operator_for` after the dozen: three keys, each a proof

| key: a subterm of Sail's definitions | compiler-operator proved to mean it | stage |
|---|---|---|
| `(a - b)` | `-` on int64_t, int32_t | integer_level |
| `(a ^^^ b)` | `^` on uint64_t, uint64_t | integer_level |
| `(zero_extend (m := 64) (bool_to_bit (zopz0zI_u a b)))` | `<` on uint64_t, uint64_t | integer_level |

The other nine units' meanings carry an immediate or a chain (`!a` is
`sltiu a, 1`; `==` is `xor` then `sltiu 1`), and no subterm over the
reads alone equals them at this size; they are found by pass A's step 1
(a whole definition) or by a larger table, not by this step.

## 5. the eye table: D beside E beside U beside L

| definition | D: Sail's text over the reads | E: the composition | E: built from (subterm -> compiler-operator) | U: instructions | L: the meaning read back | walk | proof |
|---|---|---|---|---|---|---|---|
| RTYPE SLTU | `(zero_extend (m := 64) (bool_to_bit (zopz0zI_u v_rs1 v_rs2)))` | `op_656(a, b)` | `(zero_extend (m := 64) (bool_to_bit (zopz0zI_u a b)))` -> `<` on uint64_t, uint64_t | `sltu a0, a0, a1; c.jr ra` | `(pure_RTYPE (a) (b) (LeanIM.rop.SLTU))` | CERTIFIED | PROVED equal to RTYPE rop.SLTU, by same_text |
| RTYPE XOR | `(v_rs1 ^^^ v_rs2)` | `op_404(a, b)` | `(a ^^^ b)` -> `^` on uint64_t, uint64_t | `c.xor a0, a1; c.jr ra` | `(pure_RTYPE (a) (b) (XOR))` | CERTIFIED | PROVED equal to RTYPE rop.XOR, by same_text |
| RTYPE SUB | `(v_rs1 - v_rs2)` | `op_144(a, b)` | `(a - b)` -> `-` on int64_t, int32_t | `c.addiw a1, 0x0; c.sub a0, a1; c.jr ra` | `(pure_RTYPE (a) ((pure_ADDIW (b) ((sign_extend (m := 12) (0x00#6))))) (SUB))` | CERTIFIED | NOT PROVED (52 candidates tried) |

Refused at render: 72, all "a subterm the table has no key for" (the table has three keys). The full
table with every refused row: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_c/eye_table.md`.

## 6. what the eye should take from it

- every stage runs, in one lane, in under three minutes, and each
  stage's output passes the spelling guard
- the meanings are right by inspection (`^` on `uint64_t` is `xor`;
  `<` on `uint64_t` is `sltu`; `>` is `sltu` with the operands swapped;
  `||` is `or` then `sltu zero`)
- the two proofs that close are the same text after unfolding: the
  emulation compiled back to the one instruction its definition names
- the one that does not close is a true difference (the ABI width of a
  parameter), not a defect of the path: `render` calls the unit as it
  is, byte for byte, and the unit's own parameter type travels with it

## 7. decided, recorded for audit

- the gate lane (`lanes_lp1/lp3_l61_gate_a_dozen_certified_units_through_every_stage_again.sh`) is the check before any wide run
- three defects found and fixed on the way, each recorded in the plan's PROGRESS: the library index's phantom `Sail.Vector`; the typing pass letting coerced candidates through; a proof stage failing on a goal the unfolding had already closed

## 8. awaiting the owner

- read the table; say whether it looks right and what to expect
- only then: the wide run (every c unit, then cpp, rust, go; every readable definition)
- the ABI-width case: a rule for `render` (prefer a unit whose parameter holders are the language's 64-bit word when several prove the same key) is a design choice, the owner's

## 9. pointers

- the run: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_c/`
- the lane: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lanes_lp1/lp3_l61_gate_a_dozen_certified_units_through_every_stage_again.sh`
- the plan: `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/`
- the record of the start-over and the audit: log 280 §1–§12
