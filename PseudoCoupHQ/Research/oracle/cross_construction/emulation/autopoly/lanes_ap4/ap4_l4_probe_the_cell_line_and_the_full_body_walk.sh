#!/usr/bin/env bash
# ap4_l4_probe_the_cell_line_and_the_full_body_walk.sh -- task ap4: the
# two things change 1 needs and lane 3 did not print.
#
#  [1] THE CELL'S OWN LINE: `text`, `operands`, `reads` and `writes` of
#      the five cells whose arrival contract differs from the
#      emulation's, so which register each of the cell's own operand
#      positions names is read off the table's own row.
#  [2] THE WALK OVER THE WHOLE BODY, not the narrow-stripped one: the
#      reference simulator stepped over every line of the matched
#      corpus row's body before the cell's own instruction, on a state
#      whose registers are free symbols, and what it leaves in each
#      register there.  Lane 3 walked the STRIPPED body and lost the
#      `mov %edi,%eax` that carries the emulation's first argument into
#      the accumulator; this is the same walk over the body as it
#      stands.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import reference as R
import model_table as MTAB
import single_opcode_units as SOU
import autopoly3 as A

ABORT_KB = 6 * 1024 * 1024


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


A.use_task_ap3()
MTAB._install_gpr_widths()
cells = A.read_json(A.CELLS)
runs = A.read_runs(A.RUNS)

WANTED = [("idiv", "gpr_one", 32), ("idiv", "gpr_one", 64),
          ("xor", "gpr_same", 32), ("mov", "imm_gpr", 8),
          ("mov", "imm_gpr", 32)]

print("[1/2] THE CELL'S OWN LINE, off the table's own row")
for key in WANTED:
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    print("")
    print("== `%s` %s %s   row %s" % (key[0], key[1], key[2],
                                      (row or {}).get("row_id")))
    for name in ("text", "operands", "reads", "writes", "width",
                 "builder", "condition"):
        print("   row[%-10s] = %r" % (name, (row or {}).get(name)))

print("")
print("[2/2] THE WALK OVER THE WHOLE BODY")
for key in WANTED:
    body = None
    for run in runs:
        if (run["mnem"], run["shape"], run["key_width"]) != key:
            continue
        found = run.get("primitive") or {}
        prow = found.get("row") or {}
        if prow.get("body_text"):
            body = prow["body_text"]
            break
    print("")
    print("== `%s` %s %s   the matched body, LITERAL: %s"
          % (key[0], key[1], key[2], body))
    if body is None:
        continue
    lines = body.split("; ")
    at = None
    for index, line in enumerate(lines):
        mnem, operands = SOU.parse_insn(line)
        if mnem is None:
            continue
        shape, width, cause = MTAB.classify_line(mnem, line, 0)
        marker = ""
        if mnem == key[0] and shape == key[1] and width == key[2]:
            if at is None:
                at = index
                marker = "   <== the cell"
        print("   [%d] %-30s (%s, %s, %s)%s"
              % (index, line, mnem, shape, width, marker))
    if at is None:
        print("   the cell's own instruction is not in this body")
        continue
    state = R.MachineState()
    stopped = None
    for line in lines[:at]:
        try:
            R.REFERENCE.step(state, line)
        except Exception as problem:
            stopped = "%s: %s" % (type(problem).__name__, problem)
            break
    if stopped is not None:
        print("   the reference stopped: %s" % stopped)
    print("   the registers the reference leaves at the cell's own "
          "instruction:")
    for family in sorted(state.registers):
        term = state.registers[family]
        if term is None:
            continue
        print("      %%%-5s = %s" % (family, H.T.one_line(term)[:200]))
    print("   the body instruction's operands: %s"
          % (SOU.parse_insn(lines[at])[1],))
print("")
print("peak resident: %d kB" % peak())
PY
echo "done"
