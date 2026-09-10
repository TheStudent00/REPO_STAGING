# Task l3 — the proof system's owed items: the L2 check's composer names arrivals by ledger order, and the 61 native-evaluation proofs re-proved by bv_decide

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it. Node:
`Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/`
(CORE and PROGRESS). Read `DevComms/log_227` (L1) and `log_232` (L2: the
model translator, 160 mnemonics, 153 STATED + 19 DISCREPANCY + 87 REFUSED
over the 259 single-opcode rows), `Research/op_pipeline/lean/model_translate.py`
(`check` and its composer), `check_L2.json` (one DISCREPANCY row, LITERAL:
`left = (((0#32) ++ (v0.extractLsb 31 0)) + v1)`, counterexample
`v0 = 2^64-1, v1 = 2^63-1`), `run_edges_L1.py` (`theorem_file`,
`bv_decide`, its 10 s SAT ceiling), and the L1 rows whose proof used
native evaluation (`Lean.ofReduceBool` / `native_decide` in their
theorem: count them; log_227 recorded 61). Instance `l3.conf` (copy from
`Airlock/instances/l3.conf`; memory 8g is enough: L1's
bv_decide peaked under 500 MB; the one 16-bit division took 12 GB and is
NOT re-posed here). Artifact folder: `Research/op_pipeline/lean/`; lanes
under `lanes_l3/`. Task ap5 must have CLOSED before this task submits a
lane: ap5's guard reads `check` at 259 / 172 / 87, and this task changes
that number on purpose.

## 1. The composer
The coordinator's reading of the 19 DISCREPANCY rows (log_232, and the
row above): the check builds the model side's binders by the C parameter
convention (`v0` = the first C parameter) while the unit's term names
arrivals in LEDGER order (`v0` = IN-0 = `rdi`, `v1` = IN-1 = `rsi`); for
`c/op_113` (`mov %esi,%eax; add %rdi,%rax`) the body extracts the low 32
bits of `rsi` = `v1`, and the model side extracted them from `v0`. Verify
that reading on the 19 rows FIRST (which side holds which binder, quoted
per row), then make the composer name both sides by ledger arrival order
— one function — and re-run `model_translate.py check`. Expected: the 19
become STATED; any that do not are reported by cause with the new
counterexample. The tally after is the new guard value for every later
task: state it as such in the log and in the lean node's PROGRESS
(`259 / <STATED> / 87`, DISCREPANCY <n>).

## 2. The native-evaluation proofs
L1 proved some edges by native evaluation (`Lean.ofReduceBool`, the
weaker trust class, log_227). Re-prove each with `bv_decide` (the SAT
certificate checked inside Lean, the stronger class): per row, the
outcome, wall clock, peak RSS, and the axioms the proof depends on as
Lean prints them (`#print axioms`); a row that `bv_decide` cannot close
inside its ceiling keeps its native proof and is listed with the cost of
the attempt. Report: how many of the 61 moved to the stronger class.

## 3. Deliverable
`lean/README.md` updated (the check's tally and what it means; the trust
classes and the count in each); log (next free number, check right
before writing); verifier lane; PROGRESS on the lean node; sync-back;
instance down. Memory bound 6g, named abort `ABORT_MEMORY_L3`; no
Mathlib, no network in lanes. Shared file this brief authorises:
`model_translate.py` (the composer only). Never delete anything under
`<runs>/` or `Airlock/`. Reply with the check's
before/after tally, the per-row fate of the 19, the count moved to
`bv_decide`, the tally, the two lists.
