---
id: hq.research.arch_unit_oracle.architectures.riscv64.language_axis.progress
status: living
---

# PROGRESS — language_axis

- 2026-09-13: node registered by hand (a session without a shell);
  brief `Research/briefs/task_lx1_brief.md` written; instance
  `lx1.conf` in place (`proxy = yes`, for the swift install lane
  only). Status: planned; the launch waits for a session that can
  spawn implementers.
- 2026-09-13: task lx1 run. Section 1 (swift on riscv64, an install
  question): FLAG, no guess — five network lanes found no swift SDK
  for any riscv64 triple published by swift.org (the `static-sdk`
  bundle's own manifest names only `x86_64-swift-linux-musl` and
  `aarch64-swift-linux-musl`) and no maintained community riscv64
  Linux compiler distribution. Section 2 (the seven interpreted
  languages against the RISC-V definitions): a new driver,
  `Research/oracle/riscv/rv_interp.py`, ran all 255 RISC-V cells x 7
  languages (1,785 runs, one pass, zero timeouts); agreement 237–246
  of 255 per language, 237 of 255 on all seven; two genuine defect
  classes found and left unfixed (an `fcvt.*.lu` unsigned-to-float
  construction defect shared by dart/java/php at 2^63, and one `div`
  edge disagreement in php). Report:
  `PRIVATE/PseudoCoupHQ/DevComms/log_272_lx1_riscv64_language_axis.md`.
  Status: done, awaiting the owner on the two named follow-ons.
