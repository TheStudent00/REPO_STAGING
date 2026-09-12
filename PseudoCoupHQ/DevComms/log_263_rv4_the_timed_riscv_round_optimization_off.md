# log — task rv4: the timed RISC-V round with optimization off, and what it measured

Written 2026-09-12 by the coordinator (Fable), who ran the round itself
after stopping the implementer. the owner's timing: ten minutes from the lane's
submit.

## §0. In plain words
The round took t4's RISC-V driver unchanged and compiled every emulation
with optimization OFF (c `-O0`; go `-gcflags=all=-N -l`; rust
`opt-level=0`), on the idea that the machine code would then follow the
source statement by statement and the check would close by structure.
It ran in two minutes. The result is WORSE than the same population at
ship flags, and the cause is the lifter, not the method: with
optimization off the compiler moves every intermediate through the
stack, and the RISC-V lifter refuses loads and stores by name, so the
walked meaning is not the body's meaning. Ship flags keep the values in
registers, which is why t4's run proved 144 of the same 188.

## §1. The lanes
| lane | submitted | done | what |
|---|---|---|---|
| rv4_l1 (implementer) | 00:47:13Z | 00:47:17Z | five pairs, 4 s: the mapping is instantaneous |
| rv4_l2 (implementer) | 00:48:37Z | 00:58:07Z | eight-worker pool; one worker alive; 5 of 196 handled; the pool was the defect |
| rv4_l4 (coordinator) | 01:14:37Z | 01:14:38Z | failed at once: `/usr/bin/time` absent in the image |
| rv4_l5 (coordinator) | 01:20:48Z | 01:22:48Z | THE ROUND: 188 runs, one process, 120 s, peak 474 MB |

## §2. The round's census, beside t4's ship-flag run of the same 188
| verdict | ship flags (t4) | optimization off (rv4) |
|---|---|---|
| proved | 144 | 36 |
| undecided | 13 | 81 |
| disproved (sat) | 8 | 48 |
| refused | 23 | 23 |
Per (cell, target): proved→undecided 65, proved→sat 43, proved→proved 36.
Cells added over rv3's 117: 0. Store: `construct/general/rv4_o0.jsonl`,
driver `construct/general/rv4_o0.py` (t4's `rv_general.py` with the
three flag substitutions and nothing else).

## §3. The finding that matters more than the round
The 136 RISC-V cells without a proof, counted by why:
| bucket | cells | examples | what it is |
|---|---|---|---|
| twinned, integer, NEVER ATTEMPTED | 16 | add, addiw, addw, or, mul, mulw, mulh, czero.eqz | rv2's loop ran only over UNTWINNED cells; a twinned cell whose x86 twin holds no proved certificate was skipped by both routes |
| twinned, float, NEVER ATTEMPTED | 26 | fmv.*, fcvt.s.l, fld, flw | same gap |
| untwinned, float | 3 | fcvt.d.lu, fcvt.s.lu, fsub.d | attempted; refused or undecided |
| untwinned, integer | 7 | div, rem, remu, mulh, mulhsu | attempted; the checker runs out (divide, multiply-high) |
| loads and stores | 84 | lb…ld, sb…sd, and their float forms | need a MEMORY model in the lifter; outside the method as built |
So 42 cells were never tried for a reason that is bookkeeping, 7 are the
known hard checks, and 84 are the memory frontier.

## §4. Next round, ready
The loop at ship flags over every unproved RISC-V cell that is not a
load or store: 52 cells on c and go (and rust where it renders). One
process, t4's driver, expected under three minutes.
