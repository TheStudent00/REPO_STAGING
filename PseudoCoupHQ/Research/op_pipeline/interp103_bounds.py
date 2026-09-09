#!/usr/bin/env python3
"""interp103_bounds.py -- TASK 103, round 19: read `cpython/long_mul`'s
own bounds off the SAME ship build task 94 read (`/persist/cpython_ship
/python`, v3.14.7, `-DNDEBUG -g -O3`), by task 94's own ruling: a unit
is a FUNCTION BODY, bounds read from the ELF symbol table and DWARF,
never computed.

WHAT IS REUSED, NOT COPIED.  `t94_read_bounds.symbol_rows`,
`.dwarf_rows`, `.objdump_range` and `.memory_guard` are CALLED, not
re-typed.  `t94_read_bounds.py` itself is not edited.

WHY A NEW UNIT RATHER THAN A ROW APPENDED TO `t94_bounds.json`.
`t94_bounds.json` is task 94's own artifact and this brief's stop rule
is "no edits under Research/op_pipeline except the new interp103_*
files."  So this program reads the same binary the same way and writes
its own record under its own name.

THE HANDLER, per the source (`Objects/longobject.c` lines 4244-4257,
this ship build, read in the lane this program's own docstring in
interp103_report.md quotes verbatim):

    static PyLongObject*
    long_mul(PyLongObject *a, PyLongObject *b)
    {
        /* fast path for single-digit multiplication */
        if (_PyLong_BothAreCompact(a, b)) {
            stwodigits v = medium_value(a) * medium_value(b);
            return _PyLong_FromSTwoDigits(v);
        }
        PyLongObject *z = k_mul(a, b);
        ...
    }

The fast path is a BRANCH INSIDE `long_mul`, not a separate symbol
(`_PyLong_FromSTwoDigits` has no ELF symbol of its own either -- the
compiler inlined it).  So, per task 94's own rule ("where the fast
path is a distinct function ... carve it; where it is inlined into
long_mul, carve long_mul and say so"), THE UNIT IS THE WHOLE
`long_mul` FUNCTION, exactly as `long_add` was the whole of `long_add`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

MEMORY BOUND, stated: this program holds one ELF's section headers and
one compilation unit's DIEs at a time, same shape as `t94_read_bounds
.py`.  Named abort at the instance's stated 6 GB ceiling:
`ABORT_MEMORY_T103`.
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import t94_read_bounds as T94                                    # noqa: E402

OUT = os.path.join(HERE, "interp103_bounds.json")

MEMORY_ABORT_KB = 6 * 1024 * 1024

UNIT = {
    "unit": "cpython/long_mul",
    "language": "cpython",
    "handler_function": "long_mul",
    "binary": "/persist/cpython_ship/python",
    "label": "*",
}


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_guard(where):
    now = peak_kb()
    if now > MEMORY_ABORT_KB:
        raise SystemExit(
            "ABORT_MEMORY_T103 at %s: peak resident %d kB is past the "
            "instance's stated 6 GB bound" % (where, now))
    return now


def main():
    binary = UNIT["binary"]
    wanted = {UNIT["handler_function"]}
    print("[1/3] symbol table: %s" % binary, flush=True)
    symbols = T94.symbol_rows(binary, wanted)
    print("   %s" % json.dumps(symbols), flush=True)
    print("   peak resident kB so far: %d" % memory_guard("symbols"),
          flush=True)

    print("[2/3] dwarf: %s" % binary, flush=True)
    dwarf = T94.dwarf_rows(binary, wanted)
    print("   %s" % json.dumps(dwarf), flush=True)
    print("   peak resident kB so far: %d" % memory_guard("dwarf"),
          flush=True)

    record = dict(UNIT)
    rows = symbols.get(UNIT["handler_function"], [])
    drows = dwarf.get(UNIT["handler_function"], [])
    record["symbol_table_rows"] = rows
    record["dwarf_rows"] = drows
    if not rows:
        record["bounds_source"] = "REFUSED"
        record["refusal"] = (
            "no STT_FUNC symbol named %r exists in this binary's own "
            "symbol table" % UNIT["handler_function"])
    else:
        low = rows[0]["st_value"]
        size = rows[0]["st_size"]
        high = low + size
        record["new_low"] = "0x%x" % low
        record["new_high"] = "0x%x" % high
        record["new_byte_length"] = size
        agree = None
        if drows:
            agree = (drows[0]["DW_AT_low_pc"] == low and
                     drows[0]["DW_AT_high_pc"] == high)
        record["symbol_table_and_dwarf_agree"] = agree
        print("[3/3] objdump the whole body, 0x%x..0x%x" % (low, high),
              flush=True)
        body, raw = T94.objdump_range(binary, low, high)
        record["new_instruction_count"] = len(body)
        record["body"] = body
        record["bounds_source"] = (
            "ELF symbol table (st_value, st_size) cross-read against "
            "DWARF DW_AT_low_pc / DW_AT_high_pc, read via "
            "t94_read_bounds.symbol_rows / .dwarf_rows / .objdump_range, "
            "imported and called unmodified")
        print("   %d bytes, %d instructions" % (size, len(body)),
              flush=True)

    out = {
        "meta": {
            "generator": "interp103_bounds.py",
            "task": "TASK 103 round 19 -- cpython's integer multiply "
                    "fast path against c's 64-bit multiply unit",
            "ruling": "the owner 2026-09-05, CORE_0_3_5_1_arch_unit.md, applied "
                      "here exactly as task 94 applied it: a unit is a "
                      "function body, bounds READ from the symbol table "
                      "and DWARF.",
            "reused_unmodified": ["t94_read_bounds.symbol_rows",
                                  "t94_read_bounds.dwarf_rows",
                                  "t94_read_bounds.objdump_range"],
            "peak_resident_kb": peak_kb(),
            "memory_abort_name": "ABORT_MEMORY_T103",
        },
        "record": record,
    }
    handle = open(OUT, "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s, peak resident kB: %d" % (OUT, peak_kb()), flush=True)


if __name__ == "__main__":
    main()
