---
id: hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail.progress
status: living
---

# PROGRESS — lifter_from_sail

- 2026-09-13: node registered by hand (a session without a shell);
  brief `Research/briefs/task_sl1_brief.md` written; instance
  `sl1.conf` in place. Status: planned; the launch waits for a session
  that can spawn implementers.
- 2026-09-13, later: task sl1 launched (instance `sl1.conf`) and its
  session lost mid-run while probing route (a), Sail's SMT export; its
  lanes and probes stay under `Research/oracle/riscv/sail_lifter/`. The
  same afternoon the direction moved to the co-node `lean_proof_path`
  (log 274): the generated table is Sail's Lean output read directly,
  and the walk is Sail's own `execute` composed, so this node's
  "drop-in" into `riscv_reference.py` is no longer the plan. Status:
  superseded in direction, pending the owner's word on the node itself.
- 2026-09-14: task sl1 run (log 277,
  `PRIVATE/PseudoCoupHQ/DevComms/log_277_sl1_the_lifter_generated_from_the_sail_model.md`).
  Route (a), Sail's SMT export: no output in three selections (6 h,
  90 min, 60 min); route (c) not in the image; route (b), the Lean
  export, closes: 101,330 lines in 53 min at 17.6 GB (over the 6 GB
  bound, flagged). The lifter is now a reader of that Lean
  (`Research/oracle/riscv/sail_lifter/`), `riscv_reference.py` a
  drop-in with its builders and table removed. Guard: 1,551 rows, 0
  disagreements at 448,176 evaluated points. rv6 again and the
  regeneration test: in the log. Status: done, with flags (memory
  instructions refused by the reader; the emit's memory; z3 on the
  132-bit widening). See log 274's `lean_proof_path` node beside this one.
