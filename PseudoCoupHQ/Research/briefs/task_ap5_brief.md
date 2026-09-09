# Task ap5 — the two mechanical remainders of the four languages: the x87 stack read end to end, and the immediate as an input of the mapping

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it. Then
`task_ap4_brief.md` beside this file and its log `DevComms/log_246`
(§"Decided" item 5 and §"Awaiting the owner" item 1: exactly the two things this
task does), `log_245` §4 (the x87 probe: `long double` LANDS on c), the
driver `.../emulation/handful/handful.py` and `.../autopoly/autopoly.py` as
task ex1 left them (ex1 runs before this task), `Research/op_pipeline/reference.py`
(`answer_of`), `pool100_entry_equivalence.py` (`align_by_row`),
`Research/op_pipeline/lean/model_translate.py` (`shapes_for`: the `imm_*`
shapes spell `$0x3`). Instance `ap5.conf` (copy from
`Airlock/instances/ap5.conf`). Artifact folder:
`.../emulation/autopoly/`, writing `autopoly5_*`; lanes under `lanes_ap5/`.

## 1. The x87 stack — 114 runs / 6,284 rows, unchanged through ap4
ap4 wrote the ledger's edges (`fstpt OUT-0`, `fldt IN-k`) and read the x87
places in the driver, and the population did not move, because two shared
functions the brief had not named cannot read an x87 value:
`reference.answer_of` (the answer home) and
`pool100_entry_equivalence.align_by_row` (an FP arrival). Authorised, both,
minimal: `answer_of` may name `X87_0` as an answer home when the ledger's
result family is the x87 family; `align_by_row` may align an arrival whose
place is the x87 stack by its IN row like any other. Guards: `check_L2`
259/172/87, o8 243/197/155/216, the h2 handful 24/24, AND task t100's
proved-edge count (`pool100_edges.json`: the number of proved edges, before
and after, unchanged — `align_by_row` is the pool's own aligner). Then the
30 x87 c cells re-run; rust, go, swift refused by nature as before. Every
x87 place's verdict in z3's words; a `sat` with its counterexample — the
80-bit format's explicit integer bit is where one is expected, and if it
appears, it is a finding about `long double` against the reference's
`FPSort(15, 64)`, stated, not patched.

## 2. The immediate as an input — the `imm_*` cells
The cell key (mnem, shape, key_width) carries no immediate, and the sweep
spells `$0x3`, so an `imm_*` cell's term has 3 baked in while the corpus
rows it is attested by carry `$0x1`, `$0x8`, …; `mov` imm_gpr disproved
against them with an empty counterexample. The immediate is an INPUT of
the mapping. Authorised, in `model_translate.shapes_for` (additive: a
second spelling per `imm_*` shape with a SYMBOLIC immediate, the sweep
recording `imm_symbolic = true` on those rows) and in the driver (an
`imm_*` cell's emulation takes the immediate as one more parameter of the
operand's width — `a + k` — and the check quantifies over it; the
attestation counts every corpus immediate under the one cell, listing the
distinct constants seen). Guards: the same three plus m1b's coverage totals
(the cell count may RISE by the symbolic rows: say by how many, and that no
existing row's text changed). Then every `imm_*` cell re-run on the four
targets.

## 3. The loop, fifth pass, and the deliverable
Exactly ap4's loop over the cells, writing `autopoly5_*`; the per-target
table; the all-four line across five passes; the change table (ap4 → ap5);
zero regressions or STOP. Guard over every json; log (next free number,
check right before writing); verifier lane; PROGRESS on the autopoly node;
sync-back; instance down. Memory bound 6g, sample 20, peak RSS, abort
`ABORT_MEMORY_AP5`. Shared files this brief authorises, and no others:
`reference.py` (`answer_of` only), `pool100_entry_equivalence.py`
(`align_by_row` only), `model_translate.py` (`shapes_for` only). Never
delete anything under `<runs>/` or `Airlock/`. Reply
with the per-target table, the five-pass all-four line, the change table,
the x87 verdicts by count, the immediate cells' before/after, the four
guard tallies, the tally, the two lists.
