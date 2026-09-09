#!/usr/bin/env bash
# ap1_l12_guard_and_branch.sh -- task ap1: the spelling guard over every
# json this task wrote, the `grep -c exempt` count over every file it
# added, and ONE function of the imported driver quoted LITERAL.
#
# WHY THE FUNCTION IS QUOTED: `handful.renderer_input` decides which
# form of a cell's term the renderer is handed, and it names two tasks
# by name. This lane prints it so the log can say which branch ran
# under this task's setting rather than assert it.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1. Nothing
# here reads more than one source file.
set -euo pipefail
echo "[1/3] the spelling guard, unmodified"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.json
echo "[2/3] grep -c exempt over every file this task added"
grep -c exempt \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l1_cells.sh \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l5_run.sh || true
echo "[3/3] which term the renderer is handed, per task"
python3 - <<'PY'
import inspect
import sys

sys.path.insert(0, "PseudoCoupHQ/Research/oracle/"
                   "cross_construction/emulation/handful")
import handful as H

print(inspect.getsource(H.renderer_input))
for task in ("h1", "h2", "g1", "g1b", "g1c"):
    H.TASK = task
    if task in ("h2", "g1"):
        which = "the normalised term (task h2's fix 1)"
    else:
        which = "order_commutative(simplify(term)), task h1's own"
    print("TASK %-4s fixes_are_on %-5s primitive_first %-5s "
          "setup_is_allowed %-5s -> %s"
          % (task, H.fixes_are_on(), H.primitive_first(),
             H.setup_is_allowed(), which))
PY
