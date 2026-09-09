# Task g1b — closer for g1: finish the record, run swift on the rebuilt image, and widen the primitive lookup to a two-cell body

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then `task_g1_brief.md` (the task you are closing) and what g1 left on
disk before its session was cut off by a usage limit: `handful/handful3.json`,
`handful3.md`, `handful3_primitive.json`, `handful3_spellings.json`,
`go/go_render.py`, `go/go_facts.py`, `go/go_facts.json`, `swift/swift_render.py`,
and the lane scripts under `handful/lanes_g1/` (read their logs on the
tower with `remote_lane.sh log --instance g1 <lane>`; the run of record is
`g1_l12_run_of_record2.sh`, guard `g1_l15_guard4.sh` passed). No log was
written; no PROGRESS entry; the `g1` instance is still up. Instance for
you: the same `g1` (it is up; if you bring it down, bring it up again
AFTER the coordinator's image push, see §2). Lanes under `handful/lanes_g1b/`.

## 1. Finish g1's record first, from what is on disk
The log (next free number, check right before writing), with the 40-row
table and by-cause list the g1 brief asked for, every claim carrying its
command; the verifier lane; PROGRESS on the autopoly node; sync-back. Do
this BEFORE §2 and §3 so g1's own result is banked as it stands (swift
rows REFUSED with the literal loader error, if that is what the run of
record holds).

## 2. Swift, on the rebuilt image
`swiftc` failed to load `libncurses.so.6`. The coordinator rebuilt the
image with `libncurses6` and streamed it to the tower; a fresh container
from it runs `swiftc --version` → `Swift version 6.0.3`. An instance picks
the new image only when its container is re-created: run
`remote_lane.sh down --instance g1` then `up --instance g1`, then a probe
lane with `/persist/swift/usr/bin/swiftc --version`, LITERAL. Then re-run
the ten swift rows (a second run of record, `handful3b.json`/`.md`, g1's
files not overwritten) and report them in the same 40-row shape beside
g1's.

## 3. Widen the primitive lookup by one step, then re-run the cells it changes
g1's lookup accepted only a language operator whose whole body is ONE
instruction classifying to the cell. Division in every target lowers to
the cell plus its accumulator setup (`cltd; idiv`, `cqto; idiv`), so
`idiv` went by the term route in all four and stayed undecided. Widen the
lookup to: a `single_opcode_units` row (narrow OR wide rule) whose
chaff-stripped body is the cell's instruction PLUS zero or more
zero-operand setup instructions from the reference's `SPREAD_SIGN` /
`ACCUMULATOR_WIDEN` tables, and nothing else. Record `route = primitive+setup`
and the setup cells in `composition`. Re-run only the cells whose route
changes (expect `idiv` on c, rust, go; say what happens on swift), each
with its gate verdict and, when `sat`, the counterexample and the region
it names (division by zero; MIN / -1).

Deliverable: the log for g1 (§1) and a second log for this closer (or one
log with both, clearly sectioned — say which), each verified; the two
40-row tables; the by-cause lists; the primitive-lookup rule LITERAL;
PROGRESS; sync-back; instance down. Memory bound 4g. Stop rules per LAW.
Reply with both tables, the swift probe line, the `idiv` outcomes on four
targets, the tallies, the two lists.
