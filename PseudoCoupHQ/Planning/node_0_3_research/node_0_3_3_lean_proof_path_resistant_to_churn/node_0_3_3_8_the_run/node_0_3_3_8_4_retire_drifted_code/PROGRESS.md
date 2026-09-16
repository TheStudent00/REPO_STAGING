---
id: hq.research.lean_proof_path_resistant_to_churn.the_run.retire_drifted_code.progress
status: living
---

# PROGRESS — retire_drifted_code

- 2026-09-14: planned (status: planned). Written fresh at the owner's order of 2026-09-14 ("start over. in a different research node ... the parts that are fucked up are deleted before you start them over again"); nothing of the superseded node's `retire_drifted_code` was copied.
- 2026-09-14: done. `construct.py`, `propose_all.py` -> `leanpath/leanpath/.archive/`; `construct_table.py`, `construct_all/`, `construct_all.log` -> `leanpath/.archive/`; lane l48 -> `lanes_lp1/.archive/`; each with `WHY_retired_2026-09-14.txt`; the `construct` command removed from `__main__.py`. `lean_to_z3.py` kept whole for now: its parser feeds `operator_for` and `render`; its z3 half is unused (status: done).
- 2026-09-15: the rest, after the audit of log 281: `lean_to_z3.py` archived (parser carried to `lean_tree.py`), `language.py`, `system.py` and the commands `harness`/`handful`/`pass_a`/`corpus` with `CORPUS_FLAGS` archived (`leanpath/leanpath/.archive/`, why-file dated 2026-09-15); z3 in no live file; one compiler invocation line left (status: done).
