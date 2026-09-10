# Task rv1 — RISC-V as a second architecture, explored on a handful: the compiler's cross-target claim measured, a level 0 from the ratified model, and the pipeline's per-architecture surface counted

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `log_221` §2–§3 (the term basis is architecture-neutral),
`log_229` §1 (level 0), the ref1 brief and its log (the K check on x86 —
this task is its RISC-V twin, with a formal source), `reference.py` (the
builder shape), `lane_gen.py` (how the corpus's units are compiled per
language), `canonical_form.py` / `ledger.py` (register families, the
calling-convention prelude/epilogue — the per-architecture surface).
Instance `rv1.conf`. Artifact folder: `Research/oracle/riscv/`; lanes under
`lanes_rv1/`. the owner, 2026-09-10: "explore it as an option", not a pivot.

## 1. Installs (the coordinator makes them before the task starts; you verify)
The image gains: the rust target `riscv64gc-unknown-none-elf` (rustup, at
build time), Sail 0.20.2 (opam) and the RISC-V Sail model's C simulator
`sail_riscv_sim` (built from `riscv/sail-riscv`; the model's Sail source
is mounted at `/sources/sail-riscv` (the tower mounts `Sources` at `/sources`)). Isla is NOT in the image: it
builds only against Sail's unreleased master, which fails in opam; a
symbolic route is a later task, not a workaround here.
`clang --target=riscv64-unknown-linux-gnu -c` and
`GOARCH=riscv64 go build` are already there; `llvm-objdump` carves. Verify
each with a one-line probe LITERAL; a tool that is absent is a flag, not a
workaround.

## 2. The handful
Ten corpus units, the handful's cells' own units where one exists
(`add`, `sub` imm, `imul`, `sar`, `shr`, `idiv`, `cmovne` → a select,
`setne` → a compare, `addss`, `cvtsi2sd`), compiled for riscv64 with clang
(c) and go at the same ship optimisation levels as the corpus; carved with
`llvm-objdump` at the function symbol; the calling convention stated
(a0–a7 arrive, a0 answers; no flags register).

## 3. Level 0 for RISC-V
Two readings, so the oracle exists from the first day: (a) `riscv_reference.py`
— builders in `reference.py`'s own shape for the base integer set RV64I
+ M (~50 mnemonics: `add addi sub and or xor sll srl sra slt sltu lui
auipc addiw … mul mulh div divu rem remu`), each a z3 term per written
place, no flags anywhere; (b) the ratified Sail model CONCRETELY through `sail_riscv_sim`: for each
of those instructions, a bare-metal ELF (one instruction between loads of
its inputs and a store of its outputs, linked at the simulator's reset
address, `--help` names the flags) run at the edge values first (0, 1,
-1, the extremes, powers of two and their neighbours) then random points,
at most 20,000 per instruction; (a) EVALUATED at the same points (z3
`simplify` on the substituted term, or the model's own value) against
the simulator's register file after the instruction — a disagreement is
a defect in (a), fixed with the row shown. This is a check at points, not
an equality; say so in the README's first line, with the count of points.
Read the model's own Sail text (`/sources/sail-riscv/model/`) for the
instruction's definition when a defect needs its cause.

## 4. The claim, measured
Per unit: the RISC-V body's term (the walk over (a)) against the unit's x86
term from the store, z3 at 3,000 ms, per written place, the answer width
the unit's own. Table: unit | x86 body | riscv body | terms identical
after `Term.normalize` / equal by z3 / differ (counterexample) / undecided.
Where they differ, say what the compiler did differently (a widening, a
guard, a different rounding) — quoted from both bodies.

## 5. The surface, counted
Every file and function that had to be written or changed to carry the
pipeline from x86 to RISC-V for these ten, by layer: lifter (reference),
carve, calling convention / canonical form, attestation. Lines per layer.
That number is the answer to "does solving one architecture solve the
rest": what transferred untouched (the terms, the emulations, the bank,
the proofs) against what did not.

## 6. Deliverable
`riscv/README.md` with §2–§5; guard over every json; log (next free
number); verifier lane; PROGRESS on the arch_unit_oracle node and the
research node (a new sub-node is the owner's to create, not this task's — say
it is wanted); sync-back; instance down. Memory bound 6g, peak RSS, abort
`ABORT_MEMORY_RV1`. No shared-file change; `reference.py` is READ. Never
delete anything under `<runs>/` or `PUBLIC/Airlock/`. Reply
with the ten-unit table, the (a)-against-(b) count, the surface table,
the tally, the two lists.
