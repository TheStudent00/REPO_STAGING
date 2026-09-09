#!/usr/bin/env python3
"""o8_regression.py -- task h2's regression over task o8.

WHAT THIS IS, one sentence, in relation: task o8's own program
(`../per_opcode/per_opcode.py`, the per-opcode emulation check that
renders every single-arch-opcode unit's proved term back to c, compiles
it at the corpus's ship flags, carves it and gates it) imported
UNCHANGED and re-run over its own 243 rows, with every product written
into a scratch copy under this task's artifact folder so task o8's own
artifacts on disk are untouched.

WHY IT EXISTS.  Task h2 changed the DRIVER (`handful.py`, section 2c)
and one width rule in `model_table.py`; it changed neither renderer.
Task o8's four totals over its 243 rows -- rows, LANDED, byte-identical
to the row's own body, proved -- are 243 / 197 / 155 / 216 (log 220, and
`per_opcode_report.md` section 2's `all` row).  If they come back the
same, the renderers wrote the same c for the same 243 terms.

HOW THE SCRATCH COPY IS MADE, and what is NOT copied.  `per_opcode.py`
resolves its inputs and its outputs from its own folder, and the inputs
(`single_opcode_units.json`, the canon40 and term66 stores) are read
only.  So the module is imported from its own place -- no forked copy,
no edited copy -- and the five paths it WRITES are pointed at
`o8_regression/` under this folder before its `main` is called.  Nothing
in `per_opcode.py` is modified, and nothing under `per_opcode/` is
written.

MEMORY BOUND: task o8's own, unchanged -- `ABORT_MEMORY_O8`, 2 GB
resident, checked by task o8's own `check_collector_memory` after every
row.  This file adds no collector of its own.

Coding discipline: no compound one-liner statements.

usage:
  o8_regression.py population   task o8's population, into the scratch
  o8_regression.py run          task o8's 243 rows, into the scratch
  o8_regression.py report       task o8's report, into the scratch
  o8_regression.py totals       the four totals, read off the scratch
                                results
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PER_OPCODE = os.path.normpath(os.path.join(HERE, "..", "per_opcode"))
SCRATCH = os.path.join(HERE, "o8_regression")

sys.path.insert(0, PER_OPCODE)

import per_opcode as PO                                          # noqa: E402


def point_at_the_scratch():
    """the five paths task o8's program WRITES, moved into the scratch
    copy.  Its inputs are untouched and its own folder is never
    written."""
    if not os.path.isdir(SCRATCH):
        os.makedirs(SCRATCH)
    PO.POPULATION = os.path.join(SCRATCH, "per_opcode_population.json")
    PO.HELD = os.path.join(SCRATCH, "per_opcode_held.json")
    PO.RESULTS = os.path.join(SCRATCH, "per_opcode_results.json")
    PO.REPORT = os.path.join(SCRATCH, "per_opcode_report.md")
    PO.SRC_DIR = os.path.join(SCRATCH, "src")
    if not os.path.isdir(PO.SRC_DIR):
        os.makedirs(PO.SRC_DIR)


def totals_command():
    """THE FOUR TOTALS, counted off the scratch copy's own results file
    rather than read out of the rendered report: rows, LANDED,
    byte-identical to the row's own body, and proved."""
    handle = open(PO.RESULTS)
    document = json.load(handle)
    handle.close()
    counted = {"rows": 0, "LANDED": 0, "byte identical": 0,
               "proved": 0}
    for record in document["results"]:
        counted["rows"] = counted["rows"] + 1
        first = record.get("q0") or {}
        second = record.get("q1") or {}
        third = record.get("q3") or {}
        if first.get("verdict") == "LANDED":
            counted["LANDED"] = counted["LANDED"] + 1
        if second.get("verdict") == "BYTE_IDENTICAL":
            counted["byte identical"] = counted["byte identical"] + 1
        if third.get("outcome") == "PROVED_ON_SHIP":
            counted["proved"] = counted["proved"] + 1
    for name in ["rows", "LANDED", "byte identical", "proved"]:
        print("%-16s %d" % (name, counted[name]))
    sys.stdout.flush()
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    point_at_the_scratch()
    if argv[0] == "totals":
        return totals_command()
    return PO.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
