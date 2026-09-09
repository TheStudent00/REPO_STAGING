# Progress

Initialized.

- 2026-09-06 (TASK 103, round 19, log_222): cpython's multiply handler
  (`long_mul`, `Objects/longobject.c`) carved, the same two ways task
  94 read `long_add`'s bounds, and wrapped onto `canonical_form.py`
  the same way task 96 wrapped the eleven addition-line units --
  `PROVED_BY_CONSTRUCTION`, structurally, matching `long_add`'s own
  result. **New for this node**: the term machinery
  (`term97_walk.build` / `term66_run.one_unit`) was run over an
  interpreter handler for the first time; the term built for OUT-0 is
  `UNDECIDED` against the unit's own body on both routes `gate.py`
  tries -- a real backward branch (a digit-store loop) inside
  `long_mul`'s own bytes at `0x1396c0`-`0x1396d3`, and an unmodelled
  machine-stack save/restore. Gating that term against `c/op_181`
  (`imul`, pool entry `E00063`) on the compact projection
  (`_PyLong_BothAreCompact`, both operands' magnitude in
  `[0, 2**30-1]`) is therefore `NO_TERM`: there is no sound term to
  project. Also answered: this ship build's experimental JIT is
  compiled in as an interface but not enabled
  (`sys._jit.is_available()` is `False`; no `jit_stencils.h`). A
  mechanical gap was found and disclosed, not patched: the seventh
  block kind's AREA rows (`t96_arriving_area.py`) are not readable by
  `term66_run.runtime_rows_of`. Evidence:
  `DevComms/log_222_task103_multiply_fastpath_vs_c.md`.
