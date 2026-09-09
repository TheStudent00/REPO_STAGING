# Task ap1 — AutoPoly's first full loop: every attested cell of the model table, on the four compiled targets, primitive-first

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then, in order: the arch_unit_oracle CORE's "goal" and "Ruling, 2026-09-08"
sections; `task_h1_brief.md`, `task_h2_brief.md`, `task_g1_brief.md`,
`task_g1b_brief.md` beside this file (the handful, four rounds; their logs
238, 240, 241, 242 — read 242 §7–§8 and §11 closely: the widened primitive
lookup, the `idiv` arrival-region finding, the swift thunk); the driver
`Research/oracle/cross_construction/emulation/handful/handful.py` as g1b
left it, and the four renderers. Instance `ap1.conf` (copy from
`Airlock/instances/ap1.conf` with `remote_lane.sh conf`;
bring it up; it mounts `sandbox-persist` read-only, which swift needs).
Artifact folder: `Research/oracle/cross_construction/emulation/autopoly/`;
lanes under `lanes_ap1/`.

## 1. What this is
the owner's loop, run for the first time over its measured outer set:
```
for arch_opcode_i in set_of_unique_arch_opcodes:      # the 253 attested cells with a mapping (m1b)
    for lang_i in {c, rust, go, swift}:
        emulated_arch_opcode = find_emulation(arch_opcode_i)   # g1b's driver, primitive-first, term fallback
```
1,012 runs. Nothing new in method: the driver as g1b left it, unchanged
except for (a) taking its cells from the table instead of a list of ten and
(b) the bookkeeping below. the owner's rule from the handful stands in the other
direction now: a cell the route cannot handle is a RESULT BY CAUSE, never a
reason to touch the method mid-run.

## 2. The cells
Every row of `Research/oracle/arch_opcodes/model/model_table.json` with
`attestation.ledger_rows > 0` and `outcome == TRANSLATED`, one run per
distinct (mnem, shape, key_width) — where a triple has several sweep rows,
choose by g1b's two rules (own `width == key_width`; the flag-reading row
whose setter the attestation records most). Order the runs by attested
ledger rows, descending, so the most-used cells finish first; write results
incrementally (one json line per run, `autopoly_runs.jsonl`) so a stopped
lane loses nothing and resumes by skipping runs already recorded.

## 3. Per run, recorded (the handful's four objects, compact)
cell key; lang; route (`primitive` / `primitive+setup` / `term`); the
primitive row used, if any; rendered source path; compiled (yes/no, the
compiler's first error line if no); landing (LANDED / LANDED_ELSEWHERE on
X / NOT_COLLAPSED (n)); composition (cells, chaff, unmapped counts, the
cell list); gate verdict per written place in z3's words with the
counterexample when `sat`; `cause` when refused, the refusal sentence
LITERAL. Known causes from the handful, to be counted not fixed: the
three-arrival division cells (`idiv`/`div` gpr_one at every width: "the IN
rows cannot be aligned"); a swift body carved as a one-`jmp` thunk; a
vector operand the classifier cannot width; a renderer with no spelling for
an operator the term carries.

## 4. Ceilings and memory
Gate 3,000 ms per place, ONE re-pose at 30,000 ms for UNDECIDED (not 300 s:
1,012 runs), both recorded. Compile timeout 60 s per run. Bound 6g inside
the 20g cap, sample the first 20 runs, paste peak RSS, named abort
`ABORT_MEMORY_AP1`. Expect one to three hours; poll in bounded waits.

## 5. Deliverable
`autopoly.py` (the driver over the table) → `autopoly_runs.jsonl`,
`autopoly.json` (the aggregate), `autopoly.md`:
1. **THE table, per language**: cells attempted / rendered / compiled /
   LANDED / LANDED_ELSEWHERE / NOT_COLLAPSED / proved / proved under
   caller extension / `sat` / undecided / refused — counts AND the share of
   attested ledger rows they cover (a proved cell covering 10,000 rows
   matters more than one covering 3).
2. **Per language, the primitive route's reach**: cells that had a
   primitive row / primitive+setup / term only.
3. **Refusals and non-proofs by cause**, per language, with three example
   cells each and the ledger rows they cover.
4. **Cells proved on ALL four targets** (the polyfill-complete set), on
   three, two, one, none — counts and ledger-row shares; the none-list in
   full with causes.
5. **`sat` verdicts**: every one, with its counterexample and the region it
   names, since a `sat` is where a language's edge region differs from the
   opcode's — the owner's edge-region model made measurable.
6. The five example rows of the handful shown again as they came out of
   the loop, to prove the loop reproduces the handful.
Guard over every json; log (next free number, check right before writing);
verifier lane; PROGRESS on the autopoly node; sync-back; instance down.
Stop rules per LAW. Reply with table 1, the all-four count with its
ledger-row share, the by-cause totals, the `sat` count, the tally, the two
lists.
