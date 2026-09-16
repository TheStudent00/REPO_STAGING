---
id: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.progress
status: living
---

# PROGRESS — arch_opcode_axis

- 2026-09-13: node registered by hand (a session without a shell);
  brief `Research/briefs/task_rv9_brief.md` written; instance
  `rv9.conf` in place. Status: planned; the launch waits for a session
  that can spawn implementers. The state it starts from: 251 of 255
  proved on some language, 235 on all four (log_268).

- 2026-09-13: task rv9 RUN and CLOSED, on the tower, instance `rv9`,
  eleven lanes (`Research/oracle/riscv/lanes_rv9/`). Report:
  `DevComms/log_273_rv9_the_arch_opcode_axis_the_multiply_high_cause_named.md`.
  Status: done; the headline does not move and the causes are named.
  The union of every route after this task is unchanged — 251 of 255
  proved on at least one of c, c++, rust, go and 235 of 255 on all four
  — and the same four cells are open. What the task produced instead:
  (1) the native route's cause on those four, measured object by
  object — no reference to any symbol outside the unit on c, c++ or
  rust; the body and the definition agree at 200 sampled points; their
  canonical texts differ at the ROOT node (a sum against an extract)
  because the compiler replaced the doubled-width product with the
  architecture's high-half instruction plus a correction; and z3 does
  not decide at 3,000 ms, at 30,000 ms, through its own bit-blast
  tactic, or narrowed to the low 8, 16 or 32 bits. What would close it
  is the OWED algebraic lemma general in width, which lives in a file
  this brief did not name — flagged, not worked around.
  (2) the bit-blast route at three optimization settings over the 120
  of 255 keys it had left open: ship and level-1 are identical; with
  optimization off the carved bodies are 2 to 4 times LARGER and proofs
  fall from 137 to 117 of 480 attempts, so the "less rewriting closes
  it" idea is refuted by measurement. One key moved the other way
  (`czero.eqz gpr_gpr_gpr 64` on rust, disproved at ship, proved off).
  (3) rv4's regression named at last: all 120 keys that lost a proof
  gained instructions naming a memory address, and 83 of them had the
  walk refused — 82 on one missing lifter entry, `c.addi4spn`, the
  stack-frame address instruction that only appears once optimization
  is off. A two-instruction body at ship flags becomes twenty-six.
  Owed to the lifter now: `bexti`, `orn`, `c.not` (bb1) plus
  `c.addi4spn` and `sh3add` (this task).
