# Task rv2 — the transfer: RISC-V's model table, its cells matched to x86's by TERM, inherited certificates re-verified on riscv64, the loop only over what has no twin

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `task_rv1_brief.md` and its log (rv1 runs FIRST: the RISC-V
reference checked against Sail, the carve, the calling convention, the
surface count), `task_m1_brief.md`/`task_m1b_brief.md` and logs 236/237
(the x86 model table: key (mnem, shape, key_width), `identical_text`
classes, `Term.normalize`), `task_bank1_brief.md`/`log_253` and
`task_ap6_brief.md`/`log_255` (the bank; certificates carry the term
text, the source, the compiler and flags, the verdict, the code version),
`log_221` §3 and L1's preservation theorem (`log_227`: rendering
preserves the term, an induction over the term, architecture-neutral).
Instance `rv2.conf`. Artifact folder: `Research/oracle/riscv/`; lanes under
`lanes_rv2/`.

## 1. The hypothesis this task measures (the owner, 2026-09-10)
"If we already know what is proven in x86 with their combination of
high-level compiler-operators to emulate arch-opcodes, it should also be
true in RISC-V … it should shrink the workload substantially." The
library is keyed by MAPPINGS, not opcode names: a certificate says "this
source computes this term", and that is architecture-neutral by
construction. What can differ is the compiler's RISC-V backend. So:
transfer by term identity, re-verify at the machine level, run the loop
only where no twin exists — and COUNT each of the three.

## 2. Steps
1. **RISC-V's model table**: rv1's `riscv_reference.py` swept over RV64I+M
   (and F/D if rv1 reached them) at every operand form and width the ISA
   has (register/register, register/immediate, the `w` 32-bit forms; no
   flags anywhere), one row per (mnem, shape, key_width) in the x86
   table's exact shape, terms per written place. Attestation: the ten rv1
   units, plus the corpus's c and go units compiled for riscv64 (clang
   `--target=riscv64-unknown-linux-gnu -c`, `GOARCH=riscv64 go build`) —
   how many of the 590 go units and a sample of 500 c units compile,
   carve and lift; the attested cells.
2. **The match, by term**: for every RISC-V cell, its term normalised by
   `Term.normalize` against every x86 cell's; identical text ⇒ twin;
   else z3 at 3,000 ms against the x86 cells of the same width and
   arity; else no twin. Table: RISC-V cells with a text twin / a z3 twin /
   none, and the none list by mnemonic (expected: `slt`/`sltu`, `mulh*`,
   the divides' zero and MIN/−1 values, `auipc`/`lui`, anything with no
   x86 counterpart).
3. **Inherit and re-verify**: for every twinned RISC-V cell and every
   target the x86 twin holds a `proved` or `agreed` certificate for, take
   the certificate's SOURCE unchanged; for c and go (and rust if the
   riscv64 target is in the image; swift is not available for riscv64,
   say so), compile for riscv64 at the corpus's ship flags, carve, lift
   with the RISC-V reference, gate against the term: PROVED / DISPROVED
   (counterexample; quote both bodies) / UNDECIDED. Bank the results as
   certificates with `arch = riscv64` and `inherited_from = <the x86 key>`.
   Interpreted targets: an `agreed` certificate transfers as it is
   (nothing to compile; the interpreter's answer does not depend on the
   host architecture — say so, and re-run ONE interpreter's handful to
   show it).
4. **The loop on the delta**: ap6's driver in bank mode over the
   un-twinned RISC-V cells only, on c and go (rust if available), the
   x86-style primitive lookup replaced by RISC-V's attested singletons.
5. **The count**: RISC-V cells total / twinned / inherited-and-proved /
   inherited-and-disproved / run through the loop / proved there — the
   shrinkage of the workload as a number, and the three readings of the
   RISC-V polyfill-complete set beside x86's (strict is the only reading
   with no flags: say that destination-only and strict coincide).

## 3. Deliverable
`riscv/model_table_rv.json/.md`, `riscv/twins.json/.md`,
`riscv/transfer.md` (§2.3–2.5); certificates appended to the bank with
`arch`; guard over every json; log (next free number); verifier lane;
PROGRESS on the arch_unit_oracle and research nodes; sync-back; instance
down. Memory bound 6g, sample 20, peak RSS, abort `ABORT_MEMORY_RV2`.
Shared-file changes: none outside `riscv/`; the driver is called with an
`arch` argument only if it already takes one, else the RISC-V glue lives
in `riscv/`. Never delete anything under `<runs>/` or
`PUBLIC/Airlock/`. Reply with the count of §2.5, the twin table,
the disproved inheritances with their counterexamples, the three
readings, the tally, the two lists.
