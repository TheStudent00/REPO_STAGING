# Task ap2 — AutoPoly loop, second pass: fix the mechanical causes ap1 counted, re-run the loop, and measure the change

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then `task_ap1_brief.md` beside it and `DevComms/log_243` (ap1: the loop,
its by-cause table, its §"Awaiting the owner"), `log_242` §7–§11 (g1b), the
driver `Research/oracle/cross_construction/emulation/handful/handful.py`
and `.../autopoly/autopoly.py`, the four renderers, and
`Research/oracle/arch_opcodes/model/model_table.py`. Instance `ap2.conf`
(copy from `PUBLIC/Airlock/instances/ap2.conf`; it mounts
`sandbox-persist` read-only). Artifact folder: the same `.../emulation/autopoly/`,
writing `autopoly2_*` files; ap1's products are not overwritten; lanes
under `lanes_ap2/`.

## 1. What this is
ap1 proved 120 of 253 cells on all four targets (57.6% of attested ledger
rows). Of the 445 runs carrying a cause, most causes are OURS and
mechanical. This task fixes those, one cause = one fix in the layer that
owns it (never a per-cell patch), re-runs the whole loop, and reports the
change per cause and the new all-four count. Two causes are NOT touched:
the arrival-contract question (`idiv` 3-vs-2, `xor` gpr_same 1-vs-2, `mov`
imm 0-vs-1: awaiting the owner's ruling) and every `sat` (those are results).

## 2. The fixes, each with where it lives and its guard
| cause in ap1 | runs / rows | fix | where | guard |
|---|---|---|---|---|
| "term reads state that is not an arrival register" | 134 / 37,874 | the driver's parameter plan learns the two non-arrival inputs a cell can read: a MEMORY operand (the cell's `mem_*` forms: render the memory cell as one more parameter of the operand's width, passed by value — the mapping reads its contents, and the carve/gate compares the body's load against that parameter as o8's memory rows did) and the ARRIVING FLAGS of a flag-reading cell (see next row) | driver | the h2 handful re-runs unchanged |
| "no setter row to compose the flag pair from" | 128 / 6,284 | for a flag consumer whose cell records no `setter`, choose the setter from the attestation itself: the setter most often recorded before this consumer in the corpus's ledger flag-pair rows (m1b counted 22,741 of them; the pair (setter, consumer) is in the ledger row's `mnem` list); if none exists, the cause stands | driver, reading the model table's attestation | the h1 `cmovne`/`setne` runs unchanged |
| a whole-register vector cell: no lane to project, no 128-bit holder (+ the 128-bit flags place on go/swift) | 56 + 30 / 19,324 + 25,130 | render the 128-bit place as TWO 64-bit halves (low, high) in every target, each half its own written place for the gate; go and swift get the same two-halves spelling as c and rust | driver (the projection), and one spelling per renderer for a 128-bit literal split in halves if the term carries one | the four vector cells of the handful unchanged |
| six cells with `key_width: null` crashed the driver | 24 / 19,448 | `widen_*` cells take the DESTINATION width as key width: fix in `model_table.key_width` (m1b's rule, one more case), regenerate the table's rows for those cells only, and re-run the attestation join for them | table | m1b's coverage totals unchanged except those six cells now carry a width; paste before/after |
| reference gaps: `cmovg`, `movswq`, `lea 0x0(,%rdi,8)` | 16 / 7,843 | `cmovg` and `movswq` are registered like their siblings (`cmovl` / `movslq`: same builder, the condition or widths from the mnemonic); the `lea` form with no base register is the existing `build_lea` accepting an absent base as zero | `reference.py`, three additive registrations | `check_L2` tally unchanged (259 / 172 / 87); paste |
| h2's normalise-before-render is gated on task name and OFF since g1b | — | make it unconditional in the driver | driver | h2's own measurement: the 24 handful sources unchanged |

Every fix is measured by a lane that re-runs the exact cells it targets
BEFORE the full loop, with the cause count before and after.

## 3. The loop, again
Exactly ap1's loop (its ordering, incremental jsonl, one 30 s re-pose),
over the same 253 cells (plus the six re-widthed), writing `autopoly2_*`.
Then THE table, per target, as ap1's; the all-four count with its
ledger-row share; and a **change table**: per cause, ap1 runs → ap2 runs,
and which cells moved to proved / to `sat` / to another cause. A cell that
moved from refused to `sat` is a finding, not a regression: say what
region the counterexample names.

## 4. Deliverable
`autopoly2.md` with the three tables and the `sat` list; guard over every
json; log (next free number, check right before writing); verifier lane;
PROGRESS on the autopoly node; sync-back; instance down. Memory: bound 6g
inside the cap (ap1 peaked at 2.4 GB), sample the first 20 runs, paste
peak RSS, named abort `ABORT_MEMORY_AP2`. Stop rules per LAW; a fix that
would need a NEW outcome name or a new record field is a flag, not an
invention. Reply with the per-target table, the all-four count and share
(ap1 → ap2), the change table, the `sat` count, the `check_L2` tally, the
tally, the two lists.
