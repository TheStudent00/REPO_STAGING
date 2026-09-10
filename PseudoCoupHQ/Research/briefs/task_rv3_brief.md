# Task rv3 — the RISC-V lifter gains what clang 21 writes, the twins re-run on the corrected x86 reference, the inheritance re-run with the installs, the riscv64 certificates into the bank

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in
short calls; sync paths in the flat form). Then `task_rv1_brief.md` and
`task_rv2_brief.md` with their logs (258, 259; §6 of 259 and its nine
flags are this task's inputs), `task_ref2_brief.md` and its log (ref2
runs BEFORE this task: the corrected `reference.py`, the re-derived
model table, term store, pool and bank; every x86 term you read is the
corrected one), `Research/oracle/riscv/` (rv1's and rv2's deliverables:
READ and CALLED, extended only where this brief says), `Research/GLOSSARY.md`.
Instance `rv3.conf`. Artifact folder: `Research/oracle/riscv/`; lanes under
`lanes_rv3/`.

## 1. What this is
rv2 measured the transfer: 116 of 255 RISC-V cells hold a proved
riscv64 emulation. Four named things kept the rest out, and each is
mechanical:
| flag (log_259) | the change | guard |
|---|---|---|
| clang 21 writes Zba/Zbb/Zbs and compressed forms the lifter has no entry for: `c.zext.w add.uw c.mul bseti fsgnjn.d` (27 rows) | `riscv_reference.py` gains those mnemonics in its own shape, each variant checked against the Sail simulator at points as rv1 did (edge values first, ≤20,000 points per instruction), before any use | `sail_points.py` on the new rows: agree / disagree counts, LITERAL; a disagreement is a defect fixed with the row shown |
| the twins were computed against the PRE-correction x86 reference (hash `3893...56e0`) | `twins.json` re-derived against ref2's corrected model table; both readings (whole place / own width) beside rv2's 102 / 161 | every twin that appeared or vanished, by cell, with the term text that changed |
| rust refused 61 for want of `std` on the freestanding target; c refused 15 for want of `string.h`; cpp 54 and swift 56 not attempted | the image now carries `riscv64gc-unknown-linux-gnu` (rustc, `--emit=obj`, no linker) and `g++-riscv64-linux-gnu` (glibc and libstdc++ headers at `/usr/riscv64-linux-gnu`; clang takes `--target=riscv64-linux-gnu --gcc-toolchain=/usr`, or `--sysroot`, whichever the probe shows); re-run the inheritance for rust, c and cpp; swift stays a flag (no riscv64 swift in the image) | per target: attempted / proved / disproved / undecided / refused-by-cause, beside rv2's row |
| the 734 riscv64 certificates sit in `certificates_riscv64.jsonl`, not the bank | they join `certificates.jsonl` in the bank's record shape with `arch: "riscv64"` and `inherited_from`; `bank.py`'s delta and 5% audit read `arch` as part of the key; an x86 row is untouched | bank count before → after; the audit's 5% on riscv64 rows: differing verdicts 0, LITERAL |

## 2. Then the loop and the readings
The loop over the cells still untwinned after the re-derivation, both
routes; the collapse column per constructed certificate; the count of
cells with a proved riscv64 emulation by either route, beside rv2's 116
of 255; the three readings (they coincide on RISC-V: say so once, then
print one number). Guard over every json/jsonl; log (next free number);
verifier lane; PROGRESS on the riscv64 node
(`Planning/.../node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/PROGRESS.md`)
and the research node; sync-back; instance down. Memory bound 6g, peak
RSS, abort `ABORT_MEMORY_RV3`; z3 30 s hard. Shared files this brief
authorises: `riscv_reference.py` (new rows only), `bank.py` (the `arch`
key), `certificates.jsonl` (append riscv64 rows), nothing else under
`Research/op_pipeline/`. Never delete anything under `<runs>/` or
`PUBLIC/Airlock/`. Reply with the four guards, the per-target
inheritance table, the cells-proved count beside 116, the bank before →
after, the tally, every flag LITERAL.

## 3. Order and stop rule (added 2026-09-10, so the tower is not idle beside ref2)
ref2 may still be running when you start. Do §1's first and third rows
FIRST (the lifter's new rows with their Sail check; the inheritance
re-run on the new image), which read no x86 store. Then look for ref2's
closure: its DevComms log exists AND `Research/op_pipeline/reference.py`
carries the four corrections (its sha256 is `40df3b55…25e2`, recorded in
log_259 flag 1) AND the re-derived model table is on disk beside the
old. If all three hold, do the second and fourth rows and §2. If not,
write your log with those rows marked `WAITS FOR ref2`, with the file
hashes you read, and STOP; a follow-on lane finishes them. Never wait
for ref2 in a loop.
