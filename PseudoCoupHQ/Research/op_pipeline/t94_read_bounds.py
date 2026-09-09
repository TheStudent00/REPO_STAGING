#!/usr/bin/env python3
"""t94_read_bounds.py -- TASK 94, round 18, step 1: READ each interpreter
handler function's bounds from the binary's OWN symbol table and DWARF,
and dump the whole function body.

THE RULE THIS IMPLEMENTS (the owner, 2026-09-05, CORE_0_3_5_1_arch_unit.md
heading "the unit's boundary -- RULED by the owner 2026-09-05"): "everything
is wrapped in a function.  it should be just after the wrapper-function
call to just before the return statement."  A unit is a FUNCTION BODY.
For an interpreter there is no wrapper of ours, so the interpreter's own
handler function is the wrapper and the unit is that function's body.

BOUNDS ARE READ, NEVER COMPUTED.  Two independent readings per unit:

  * the ELF SYMBOL TABLE -- st_value and st_size of the FUNC symbol.
  * DWARF -- the DW_TAG_subprogram's DW_AT_low_pc and DW_AT_high_pc.

They are recorded side by side and any disagreement is reported rather
than resolved silently.  No taint propagation is used anywhere in this
file: `lineage_carve.py`'s boundary use is retired by the ruling above.

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
one compilation unit's DIEs at a time.  Expected peak resident size is
under 1 GB; the abort name if it climbs past 6 GB is
`T94_BOUNDS_MEMORY_ABORT` and the run prints its own peak.
"""

import json
import os
import re
import resource
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "t94_bounds.json")

from elftools.elf.elffile import ELFFile                    # noqa: E402

MEMORY_ABORT_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_guard(where):
    now = peak_kb()
    if now > MEMORY_ABORT_KB:
        raise SystemExit(
            "T94_BOUNDS_MEMORY_ABORT at %s: peak resident %d kB is past "
            "the stated 6 GB bound" % (where, now))
    return now


# the eleven interpreter units on record (interp_canon35.json's
# population block), each named by the HANDLER FUNCTION the ruling makes
# its boundary.  `label` is the display label, once, on the
# member -- it is never a key here and nothing groups or pairs by it.
UNITS = [
    {"unit": "cpython/long_add_fastpath",
     "language": "cpython",
     "handler_function": "long_add",
     "binary": "/persist/cpython_ship/python",
     "label": "+"},
    {"unit": "java/op_1",
     "language": "java",
     "handler_function": "Probe::af (JIT nmethod)",
     "binary": None,
     "label": "+"},
    {"unit": "java/op_2",
     "language": "java",
     "handler_function": "Probe::af2 (JIT nmethod)",
     "binary": None,
     "label": "/"},
    {"unit": "ruby/vm_opt_plus",
     "language": "ruby",
     "handler_function": "vm_opt_plus",
     "binary": "/persist/ruby_ship/ruby",
     "label": "+"},
    {"unit": "ruby/rb_fix_plus",
     "language": "ruby",
     "handler_function": "rb_fix_plus",
     "binary": "/persist/ruby_ship/ruby",
     "label": "+"},
    {"unit": "ruby/rb_int_plus",
     "language": "ruby",
     "handler_function": "rb_int_plus",
     "binary": "/persist/ruby_ship/ruby",
     "label": "+"},
    {"unit": "ruby/rb_big_plus",
     "language": "ruby",
     "handler_function": "rb_big_plus",
     "binary": "/persist/ruby_ship/ruby",
     "label": "+"},
    {"unit": "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "language": "php",
     "handler_function": "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "binary": "/persist/php_c_ship/sapi/cli/php",
     "label": "+"},
    {"unit": "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "language": "php",
     "handler_function": "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "binary": "/persist/php_c_ship/sapi/cli/php",
     "label": "+"},
    {"unit": "php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "language": "php",
     "handler_function": "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "binary": "/persist/php_c_ship/sapi/cli/php",
     "label": "+"},
    {"unit": "php/add_function",
     "language": "php",
     "handler_function": "add_function",
     "binary": "/persist/php_c_ship/sapi/cli/php",
     "label": "+"},
]


def symbol_rows(binary, wanted):
    """-> {name: [ {value,size,bind,type,shndx} ]}, read off the ELF
    symbol table itself, both .symtab and .dynsym."""
    found = {}
    with open(binary, "rb") as handle:
        elf = ELFFile(handle)
        for section in elf.iter_sections():
            if section.header["sh_type"] not in ("SHT_SYMTAB", "SHT_DYNSYM"):
                continue
            if not hasattr(section, "iter_symbols"):
                continue
            for symbol in section.iter_symbols():
                name = symbol.name
                if name not in wanted:
                    continue
                info = symbol["st_info"]
                if info["type"] != "STT_FUNC":
                    continue
                row = {
                    "section": section.name,
                    "st_value": symbol["st_value"],
                    "st_size": symbol["st_size"],
                    "bind": info["bind"],
                }
                rows = found.setdefault(name, [])
                if row not in rows:
                    rows.append(row)
    return found


def dwarf_rows(binary, wanted):
    """-> {name: [ {low_pc, high_pc, cu_offset} ]}, read off DWARF's own
    DW_TAG_subprogram records."""
    found = {}
    with open(binary, "rb") as handle:
        elf = ELFFile(handle)
        if not elf.has_dwarf_info():
            return found
        info = elf.get_dwarf_info()
        for unit in info.iter_CUs():
            memory_guard("dwarf scan of %s" % binary)
            try:
                dies = list(unit.iter_DIEs())
            except Exception:
                continue
            for die in dies:
                if die.tag != "DW_TAG_subprogram":
                    continue
                name_attr = die.attributes.get("DW_AT_name")
                if name_attr is None:
                    continue
                name = name_attr.value
                if isinstance(name, bytes):
                    name = name.decode("utf-8", "replace")
                if name not in wanted:
                    continue
                low = die.attributes.get("DW_AT_low_pc")
                high = die.attributes.get("DW_AT_high_pc")
                if low is None or high is None:
                    continue
                low_pc = low.value
                high_pc = high.value
                if high.form != "DW_FORM_addr":
                    high_pc = low_pc + high_pc
                row = {
                    "cu_offset": unit.cu_offset,
                    "DW_AT_low_pc": low_pc,
                    "DW_AT_high_pc": high_pc,
                    "high_pc_form": high.form,
                }
                rows = found.setdefault(name, [])
                if row not in rows:
                    rows.append(row)
    return found


LINE = re.compile(r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s*(.*)$")


def objdump_range(binary, low, high):
    """the whole function body, objdump's own reading of its own bytes."""
    text = subprocess.check_output([
        "objdump", "-d", "--no-show-raw-insn" if False else "-w",
        "--start-address=0x%x" % low,
        "--stop-address=0x%x" % high,
        binary,
    ], stderr=subprocess.STDOUT).decode("utf-8", "replace")
    rows = []
    for raw in text.split("\n"):
        hit = LINE.match(raw)
        if hit is None:
            continue
        address = int(hit.group(1), 16)
        if address < low or address >= high:
            continue
        mnemonic = hit.group(3).strip()
        if mnemonic == "":
            continue
        mnemonic = re.sub(r"\s+", " ", mnemonic)
        mnemonic = mnemonic.split("#")[0].strip()
        rows.append({"address": "0x%x" % address,
                     "bytes": hit.group(2).strip(),
                     "mnem": mnemonic})
    return rows, text


def main():
    by_binary = {}
    for unit in UNITS:
        if unit["binary"] is None:
            continue
        by_binary.setdefault(unit["binary"], set()).add(
            unit["handler_function"])

    symbols = {}
    dwarf = {}
    for binary in sorted(by_binary):
        wanted = by_binary[binary]
        print("[symbol table] %s" % binary, flush=True)
        symbols[binary] = symbol_rows(binary, wanted)
        print("   %s" % json.dumps(symbols[binary]), flush=True)
        print("[dwarf] %s" % binary, flush=True)
        dwarf[binary] = dwarf_rows(binary, wanted)
        print("   %s" % json.dumps(dwarf[binary]), flush=True)
        print("   peak resident kB so far: %d" % memory_guard(binary),
              flush=True)

    records = []
    for unit in UNITS:
        record = dict(unit)
        binary = unit["binary"]
        name = unit["handler_function"]
        if binary is None:
            record["bounds_source"] = (
                "NOT AN ELF BINARY -- this unit is a JIT-emitted nmethod; "
                "its bounds are the JVM's own printed nmethod base and "
                "length, recorded in interp_jvm.json, which is the JIT's "
                "own testimony and is READ rather than computed.  Flagged: "
                "the ruling says symbol table and DWARF, and a JIT has "
                "neither.")
            record["symbol_table_rows"] = None
            record["dwarf_rows"] = None
            records.append(record)
            continue
        rows = symbols.get(binary, {}).get(name, [])
        drows = dwarf.get(binary, {}).get(name, [])
        record["symbol_table_rows"] = rows
        record["dwarf_rows"] = drows
        if not rows:
            record["bounds_source"] = "REFUSED"
            record["refusal"] = (
                "no STT_FUNC symbol named %r exists in this binary's own "
                "symbol table, so this handler's function bounds cannot "
                "be read here" % name)
            records.append(record)
            continue
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
        body, raw = objdump_range(binary, low, high)
        record["new_instruction_count"] = len(body)
        record["body"] = body
        record["bounds_source"] = (
            "ELF symbol table (st_value, st_size) cross-read against "
            "DWARF DW_AT_low_pc / DW_AT_high_pc")
        records.append(record)
        print("[unit] %-58s 0x%x..0x%x  %4d bytes  %4d instructions"
              % (unit["unit"], low, high, size, len(body)), flush=True)

    out = {
        "meta": {
            "generator": "t94_read_bounds.py",
            "task": "TASK 94 round 18 -- re-carve the interpreter units to "
                    "their handler function's body",
            "ruling": "the owner 2026-09-05, CORE_0_3_5_1_arch_unit.md heading "
                      "'the unit's boundary -- RULED by the owner 2026-09-05': a "
                      "unit is a function body, bounds READ from the symbol "
                      "table and DWARF.",
            "retires_for_boundary_use": "lineage_carve.py's taint "
                                        "propagation, for the BOUNDARY use "
                                        "only; its arrival lineages stay.",
            "spelling": "the member label appears once per unit, as a "
                        "display field on the member.  No key, grouping, "
                        "pairing or row structure in this file uses it.",
            "peak_resident_kb": peak_kb(),
            "memory_abort_name": "T94_BOUNDS_MEMORY_ABORT",
        },
        "records": records,
    }
    with open(OUT, "w") as handle:
        json.dump(out, handle, indent=1)
    print("wrote %s ; peak resident %d kB" % (OUT, peak_kb()))


if __name__ == "__main__":
    main()
