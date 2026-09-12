# Task rd1 — a conditional whose branch can trap is rendered as an `if` that dominates the operation, not as a select over values already computed; then rv6 re-run so the divide family is proved on go

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_265` (rv6) and its queue note in the
riscv64 node's PROGRESS (2026-09-12 05:20Z: the defect, with the file
`construct/general/emulations_riscv64/div_gpr_gpr_gpr_64__reg_a0__go__native_first.go`
— read it: `v0 = b / a` is computed BEFORE `sel64(a == 0, ...)`), `log_262`
§2 (the general render's shape: every node a named local),
`render_general.py` (the render you change), the per-target renderers'
notes on trapping operators (`go/go_render.py` SPELLINGS: go checks the
zero divisor and panics; `swift/swift_render.py`: swift traps on
overflow and on zero), `rv6_all_langs.py` (the run you repeat).
Instance `rd1.conf` (copy `rv4.conf`). Lanes under
`Research/oracle/riscv/lanes_rd1/`.

## 1. The defect, in the owner's words and mine
the owner: "how would go div or any other div-mode from other languages be
problematic if zero is checked first?" It is not — when zero IS checked
first. The general render evaluates every node eagerly and prints a
conditional as a select over values already computed, so the guarded
division runs unguarded, and on go it traps at a = 0 where the
definition answers all ones. The compiled shape with the guard first
(lane `rv7_l1_go_div_body.sh`) shows the compiler then drops its own
check entirely: 12 instructions, one `div`, no panic call.

## 2. The change, one rule
`trapping node`
- a node whose target operator can trap: division and remainder on go
  and swift (zero divisor; swift also the signed overflow); the plain
  arithmetic on swift outside the `&` forms; anything the per-target
  renderer already marks as an edge region.
`the rule`
- when a conditional's branch (transitively) contains a trapping node,
  render the conditional as control flow: `if cond { <then-branch's
  nodes> } else { <else-branch's nodes> }`, each branch's nodes computed
  INSIDE its arm, so the guard dominates the operation. Otherwise keep
  the select. Nodes shared by both arms and by the rest stay hoisted.
- the term is unchanged; only the printed order is. The Lean statement
  (`lean_general.py`) is unaffected: it states the term, not the order.

## 3. Then
1. the six-cell sample (the divide family first) with the rendered
   source pasted for go's `div`, and its compiled body; then
2. rv6 again (`rv6_all_langs.py`, every RISC-V cell, c cpp go rust,
   both routes, one process) → the table with "of 255" on every row
   beside log_265's; the disproved column before → after; and
3. the x86 bank's delta on go and swift for the divide family (the
   same render serves x86: `general.py`'s pass), reported beside t4's
   collapse column.
Guard; log (next free number); verifier; PROGRESS on the riscv64 node
and the autopoly node; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_RD1`. `render_general.py` is the ONE shared file this
brief authorises; nothing under `Research/op_pipeline/`.
