# task61_resume.md — TASK 61 (`term.py`, `pool.py`) resume state

Node home:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/`
and `node_0_3_5_7_pool/`. Report: `DevComms/log_163_task61_term_pool.md`.

## reading done (2026-09-03)

AgentMemory.md in full; LLM_communication_protocol.md (incl. Appendix
B, §3.4a); PlanPlan PROTOCOL.md §2; log_158 (task 61); the term CORE
and its four sub-node COREs; the pool CORE and its five sub-node
COREs; log_159 §10; log_160 §1.

## what the reading settled, so it is not re-derived

- `Reference.opcode_table` (`reference.py` §5, class `OpcodeTable`) is
  THE meanings table. Its `Entry` carries `reads`, `writes`, `build`,
  `cause`. Every builder reads through `reference.Operands`, which
  reads through `reference.MachineState` and nothing else. So a term
  is built by seeding a `MachineState` from the ledger's own wiring
  and running the entry's builder — no second table. `layer4.py`'s
  producer table WAS the second table and is neither imported nor
  copied.
- The canon39 ledger rows carry NO body line. The line is recovered
  by re-running `ledger.Ledger.walk_dataflow` with the `mnemonic_of`
  seam recording the current line and a `Ledger` subclass stamping it
  — the method `relink48.py` used, applied to the landed `ledger.py`.
  The prelude used for the re-run is `canonical_form.Prelude`, so
  IN-i is argument i (the order canon39 was written with).
- The re-run is CHECKED row for row against the stored canon39 ledger
  (row names, typed producers, operands, in order); a disagreement is
  refused by name.
- Every canon39 unit record carries `body_verbatim`,
  `arrival_families`, `result_family`, `result_width`, `body_bytes`,
  `ledger`, `wrapped_text`, `operator` (display only), `lang`,
  `population`, `arrival_annotation`.
- `render_back` stays PLANNED and is NOT attempted; `Term.render_back`
  raises with the debt named.
- Pool merges on THREE grounds; the two-ground count goes on the
  artifact as `entries_under_the_brief_strict_rule` and is used for
  nothing.

## the correction made to the tree (PROTOCOL §2, round rule 2) — DONE

The brief named `exception_families3.json`. That name is TAKEN: the
exception_families CORE's realization table already recorded
`exception_families3.py` / `.json` (2026-09-01, over `guards5.json`).
A superseded record is never edited, so the rebuild is
`exception_families4.json`. The CORE's settled rules and realization
table were corrected FIRST, and the node PROGRESS records it.

## the process error, caught and corrected

The first launch of `term61_run.py` reported a shell error but had in
fact started; a second launch then ran beside it — TWO processes over
one store, against the one-process rule. Both were stopped,
`term61_store/` and `term61_state.json` were deleted, and the run was
restarted as a single process. Recorded in log_163 rather than hidden.

## files written so far

| file | what it is |
|---|---|
| `term.py` | the node: `Term.transcribe` / `.normalize` / `.census`; `render_back` refuses |
| `term61_run.py` | the driver over the canon39 proved population, resumable |
| `name_census5.py` | the census + the delta vs census4 by reason sentence |
| `audit61.py` | the four states per population, transitions, causes, consistency line |
| `show61.py` | one transcription shown literally |
| `pool.py` | the node: `Pool.merge` / `.compare` / `.representative` / `.families` / `.exception_families` |
| `pool61_run.py` | the driver writing pool4, families4, exception_families4, the delta |

## step list

1. [x] correct the exception_families CORE + PROGRESS (the name)
2. [x] `term.py` — Term.transcribe / normalize / census
3. [x] `show61.py` — `go/op_319` prints `v0 + v1`, both routes proved
4. [x] run `term61_run.py` over all 332 shards (one process)
5. [x] `name_census5.py` -> name_census5.json + delta vs census4
6. [x] `audit61.py` -> the four states vs 25,179 / 0 / 3,970 / 1,287
7. [x] `pool61_run.py` -> the_pool4 / the_families4 /
       exception_families4 / pool3_pool4_delta
8. [x] guard over every artifact; the no-carve-out check reads zero
9. [x] PROGRESS on every term and pool node
10. [x] log_163

## how to resume

`cd ~/Programming/PseudoCoupHQ/Research/op_pipeline` and run, in
order, with `/tmp/reconnect_venv/bin/python3`:
`term61_run.py 30000` (resumes from `term61_state.json`),
`name_census5.py`, `audit61.py`, `pool61_run.py`.

## the three defects the gate caught, and the fixes (2026-09-03)

Each was found because a unit task 58 PROVED came back DISPROVED —
the gate doing exactly its job. Each fix is in `term.py`.

1. **The constant-pool counter restarted every row.** The reference
   keys the k-th rip-relative read of a body as `ripconst_k`. This
   walk builds one machine state per row, so every row's first read
   was `ripconst_0`, and a body reading two different pool constants
   was transcribed as reading one. 74 c units of 610. Fix: the
   counter lives on the unit's record and is carried into and out of
   each row's state (`Transcription.rip_reads`).
2. **Both halves of one instruction must read the state before it.**
   `idiv` writes a quotient row and a remainder row from one line;
   publishing the quotient's residence before the remainder was built
   made the remainder read the quotient. Fix: rows are grouped by
   LINE OCCURRENCE and residence is published only when the line is
   finished (`Term.publish`). Instance: `c/op_246`, whose answer is
   now `SRem(Concat(sign, a), b)` and proves on both routes.
3. **The x87 stack was rebuilt by push order, not by wiring.** `fxch`
   swaps two positions and makes no ledger row, so a stack rebuilt by
   pushing the X87 rows in order had the operands reversed after an
   exchange. Fix: `Term.seed_x87` reads the ROW'S OWN operand list,
   which the ledger already recorded in the arch text's operand
   order. Instance: `c/regen_36772`.
4. **A literal row was published as a register's holder.** A CONST
   row is the body's own immediate operand and an OWN row is a stack
   address the body spells; neither resides in the line's destination
   register. Publishing them answered a later read of that register
   with the immediate. Fix: `remember_residence` returns early for a
   non-opcode-phrase producer. Instance: `go/op_206`, where
   `cmp $0x20,%rbx` made the CONST row the holder of the second
   argument. 57 units were DISPROVED by this.
5. **A value-writing flag setter left no flags for its reader.**
   `or %esi,%edi` writes a value row AND flags; only the value was
   kept, so every `set<cc>` reading it refused for want of flags.
   Fix: `Transcription.flag_state` keeps, per row, the flag state that
   row's own builder left, and a flag-pair row picks it up from the
   row the ledger says it reads. 1,364 units. Instance: `c/op_282`,
   now `If(Extract(31, 0, v0) | Extract(31, 0, v1) == 0, 0, 1)`.
