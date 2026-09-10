# log 166 — task briefs for Claude Code, round 13

Date: 2026-09-03. Point a Claude Code session here. OPUS default.
ONE AIRLOCK INSTANCE PER TASK. All of log_158's binding rules stand
(code carries the node's name; a shape the tree lacks goes into the
tree first; nothing reaches the owner that a CORE or AgentMemory answers;
PROGRESS at the moment of progress; standing requirements).

Tree: `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`.
Every task is a node whose PROGRESS says **planned** after the
round-12 audit (log_165).

STATE AT HANDOFF (log_165): canon39 30,432 / 646; terms 26,040 proved
/ 0 withdrawn / 3,865 undecided / 527 no term; pool4 1,961 entries;
census5 52 producers. Undecided by cause (log_160 §1.7): 3,419
runtime callees, 499 conditional transfers, 32 rip-relative
addresses, 20 narrow division/multiply.

---

## TASK 63 — runtime_callee, generalized (node 0_3_5_1_8; Opus)

CORE: `node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/` (read
the two settled lines added 2026-09-03).

WORK: (a) attach EVERY callee the toolchain's builtins archive
index defines — not the four division names — for every
call-bearing unit (3,419 in canon39; `__extendhfsf2` 2,308
sightings, `__truncsfbf2` 1,168, `__truncsfhf2` 1,143, `__netf2` 536,
…); nested callees inside an archive body are followed the same way
(relocation-aware: read `objdump -dr` and resolve the reloc symbol).
(b) swift: run the extraction as a lane on the `trickle` instance,
where `/persist/swift/usr/bin/swiftc` lives; attach the swift
callers. (c) `endbr64`, `bsr` and any other mnemonic the archive
bodies spell that the opcode table lacks: add them to
`Reference.opcode_table` (they are arch opcodes with plain
meanings). Report: callers attached / not attached by cause, per
language; print `cpp/regen_12920` (`__extendhfsf2`) with its callee
body attached.

## TASK 64 — the reference follows branches and steps into callees (node 0_3_5_4; Opus; after 63)

CORE: `node_0_3_5_4_reference/` (settled lines added 2026-09-03) and
`machine_state`.

WORK: `Reference.simulate` forks at `j<cc>` on the condition term,
merges at the join label as `If(cond, a, b)` per cell; a side that
transfers out of the unit is unreachable and recorded on the guard
row; at a `call` with an attached callee, enter the callee with its
own arrival contract and return. Add 8/16-bit division and widening
multiply (AH/AL, DX:AX pairs) to `DESTINATION_RULES` and the table;
model rip-relative address computation as `ripconst_<n>`.
Acceptance, printed with values: `go/op_174` (`jl` to a panic path)
proves; `c/op_282`-style logic units unchanged; one `__extendhfsf2`
caller proves through its callee. Re-gate all 30,432 terms with
`gate.py`; expectation to test: the 3,419 + 499 + 32 + 20 decide.
Report the four states per population against 26,040 / 0 / 3,865 /
527; consistency 0; zero regressions with causes.

## TASK 65 — term, pool, census on the round-13 gate (nodes 0_3_5_6, 0_3_5_7; Opus; after 64)

WORK: `term61_run` → `term65`; `name_census6.json`; `the_pool5.json`,
`the_families5.json`, `exception_families5.json`; delta vs pool4
with computed causes; E00029's successor printed; the layer-5 /
layer-3 collapse per population. Guard, unmodified, one process.

## TASK 66 — render_back (node 0_3_5_6_5; Opus; parallel with 63)

CORE: `node_0_3_5_6_term/node_0_3_5_6_5_render_back/`.

WORK: the return path: z3 term → arch text, by one fixed rule
(operator → instruction template over the ledger's rows; free
symbols → IN rows; the result → OUT-0), assembled with `as` and
gate-proved against the unit's own ship code exactly as a wrapped
text is. Population: every proved term of `E00029` first (158
units), then all proved terms. Report rendered / proved / refused
with reasons. This closes log_147 §8.1's named debt; if the CORE's
shape is insufficient, correct the CORE first and say so.

## TASK 67 — bank round 13 (smaller model acceptable)

WORK: as log_158 TASK 62, over pool5; `check_plans.py` pasted;
dashboards regenerated; posterity message with `wc -c`.

---

Order: 63 and 66 in parallel; 64 after 63; 65 after 64; 67 last.
No open calls for the owner.
