#!/usr/bin/env python3
"""dwarf_typed_key_t27.py -- TASK 27's extension of the DWARF typed-key
read (task 24's `dwarf_typed_key.py`, imported unmodified for its
`scan()` and its type renderer).

WHY A SECOND READ IS NEEDED, stated plainly.  Task 24 read its keys out
of `/persist/php_anchor/sapi/cli/php` and `/persist/ruby_anchor/ruby`.
Task 27 carves and proves over TWO binaries task 24 did not read:

  * `/persist/php_c_anchor/sapi/cli/php` and
    `/persist/php_c_ship/sapi/cli/php` -- the CLEAN php pair built this
    session (zero gcov symbols, PHP 7.4.33), which replaces the
    coverage-instrumented single build log_095 recorded as a dead end.
  * `/persist/ruby_ship/ruby` -- the ship build the ruby carve is taken
    from, where task 24 only read the anchor build.

A key read from a different binary than the bytes it labels is an
assumption.  This program removes that assumption by reading the key
out of each binary the carve actually uses.

Run (inside the sandbox container, because the binaries live there):
  podman exec -e DWARF_T27_OUT=/persist/dwarf_typed_key_t27.json \\
    sandbox-runner bash -lc 'cd PseudoCoupHQ/Research/op_pipeline \\
    && python3 dwarf_typed_key_t27.py'
"""

import json
import os
import sys

import dwarf_typed_key as base

PHP_SYMS = [
    "add_function",
    "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
    "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
    "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
]

RUBY_SYMS = [
    "vm_opt_plus",
    "rb_fix_plus",
    "rb_int_plus",
    "rb_big_plus",
    "fix_plus",
    "rb_fix_plus_fix",
]

TARGETS = [
    ("php", "/persist/php_c_anchor/sapi/cli/php",
     "php 7.4.33 CLEAN anchor build (--disable-all, CFLAGS=-O0 -g -fwrapv -std=gnu17), built by t27_php_clean_build2.sh",
     PHP_SYMS),
    ("php", "/persist/php_c_ship/sapi/cli/php",
     "php 7.4.33 CLEAN ship build (--disable-all, CFLAGS=-O2 -g -std=gnu17), built by t27_php_clean_build2.sh",
     PHP_SYMS),
    ("ruby", "/persist/ruby_anchor/ruby",
     "ruby 3.3.0 anchor build, per interp_ruby.json pin",
     RUBY_SYMS),
    ("ruby", "/persist/ruby_ship/ruby",
     "ruby 3.3.0 ship build, per interp_ruby.json pin -- the build the ruby carve is taken from",
     RUBY_SYMS),
]

OUT = os.environ.get("DWARF_T27_OUT") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "dwarf_typed_key_t27.json")


def main():
    records = []
    read = 0
    refused = 0
    for lang, path, what, syms in TARGETS:
        if not os.path.exists(path):
            for s in syms:
                records.append({
                    "lang": lang,
                    "handler": s,
                    "dwarf_source_binary": path,
                    "dwarf_source_what": what,
                    "outcome": "REFUSED",
                    "refusal": "the binary does not exist on this machine",
                })
                refused += 1
            continue
        found, err = base.scan(path, set(syms))
        for s in syms:
            rec = {
                "lang": lang,
                "handler": s,
                "unit": "%s/%s" % (lang, s),
                "dwarf_source_binary": path,
                "dwarf_source_what": what,
            }
            got = found.get(s)
            if got is None:
                rec["outcome"] = "REFUSED"
                rec["refusal"] = err or (
                    "no DW_TAG_subprogram DIE for this symbol in this "
                    "binary's DWARF")
                rec["typed_key"] = None
                refused += 1
                records.append(rec)
                continue
            rec.update(got)
            params = got["formal_parameters"]
            if len(params) < 2:
                rec["outcome"] = "REFUSED"
                rec["refusal"] = (
                    "the DIE was found and carries %d formal parameter(s); a "
                    "two-operand typed key is not expressible from parameter "
                    "types for this handler -- the operands reach it another "
                    "way (php's specialized executor handlers read them "
                    "through the execute_data frame)" % len(params))
                rec["typed_key"] = None
                refused += 1
            else:
                rec["outcome"] = "READ"
                rec["typed_key"] = "%s,%s" % (
                    params[0]["dwarf_type"], params[1]["dwarf_type"])
                rec["operand_selection_rule"] = (
                    "the first two formal parameters are the operands.")
                types = set(p["dwarf_type"] for p in params)
                rec["typed_key_invariant_under_operand_choice"] = len(types) == 1
                rec["evidence_class"] = (
                    "forced by construction -- the compiler's own DWARF "
                    "DW_AT_type chain on the handler's formal parameters, "
                    "emitted by the same compile that produced the bytes the "
                    "arch-unit was carved from")
                read += 1
            records.append(rec)

    out = {
        "meta": {
            "generator": "dwarf_typed_key_t27.py",
            "task": "TASK 27 -- typed keys read from the binaries this task's carves actually use",
            "imports": "dwarf_typed_key.py (task 24), unmodified",
            "prior_artifact": "dwarf_typed_key.json -- read, never written by this program",
        },
        "records": records,
        "summary": {
            "symbols_considered": len(records),
            "keys_read": read,
            "refused": refused,
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for r in records:
        print("%-6s %-56s %-8s %s" % (
            r["lang"], r["handler"], r["outcome"], r.get("typed_key")))
    print("summary: %s" % out["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
