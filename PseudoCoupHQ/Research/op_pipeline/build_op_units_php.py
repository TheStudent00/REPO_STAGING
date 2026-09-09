#!/usr/bin/env python3
"""build_op_units_php.py -- TASK 27, part 1 (php).

Builds `op_units_php.json`: handler slices for php's addition route,
ANCHOR and SHIP per symbol, in the same record shape
`op_units_cpython.json` carries.

THE BUILD THIS USES IS NEW, AND IT IS THE POINT.  log_095 recorded php
as a genuine dead end: PHP 7.4.33's configure insisted on libxml-2.0,
that package is absent from this container and `apt-get` cannot reach a
mirror, so `make` relinked the SAME coverage-instrumented objects into
both the "anchor" and "ship" paths -- 13,359 `gcov` symbols in each and
a byte-identical `add_function` disassembly.  This session got past
that wall with `--disable-all` (php's configure then never reaches its
libxml probe) plus `-std=gnu17` (this container's gcc otherwise rejects
php 7.4 era empty parameter lists).  The result is a real, distinct,
UNINSTRUMENTED pair:

    /persist/php_c_anchor/sapi/cli/php   gcov symbols: 0
    /persist/php_c_ship/sapi/cli/php     gcov symbols: 0

The contaminated pair is NOT used for any slice here, and its facts are
kept in this artifact's meta as the superseded record.

Extraction is `slice_extractor_fix.parse_objdump_text` (task 20's fixed
extractor), over `objdump -d --disassemble=SYM` text produced by the
lane `t27_php_clean_build2.sh`.

Every record carries `provenance_is_weaker: true`.

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

The four symbols below are the ones interp_php.json's dispatch
measurement recorded as executing, and the ones the round-4 proposal
already carries records for -- provenance of the measurement, not a
token match.

Run:
  /tmp/reconnect_venv/bin/python3 build_op_units_php.py
"""

import json
import os
import subprocess
import sys

import slice_extractor_fix

HERE = os.path.dirname(os.path.abspath(__file__))
DUMPS = "Airlock/agent/out/t27"
OUT = os.path.join(HERE, "op_units_php.json")

SYMBOLS = [
    ("add_function", "the generic two-zval routine in the Zend engine",
     "named in interp_php.json's dispatch measurement"),
    ("ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "the unspecialized executor handler",
     "named in interp_php.json's dispatch measurement"),
    ("ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "the integer-specialized executor handler",
     "named in interp_php.json's dispatch measurement"),
    ("ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
     "the integer-specialized handler the compiler proved cannot overflow",
     "named in interp_php.json's dispatch measurement"),
]


def container(cmd):
    proc = subprocess.run(
        ["podman", "exec", "sandbox-runner", "bash", "-lc", cmd],
        capture_output=True, text=True)
    return proc.stdout.strip()


def read_nm(tag):
    out = {}
    path = os.path.join(DUMPS, "phpclean_%s_nm.txt" % tag)
    if not os.path.exists(path):
        return out
    for line in open(path):
        parts = line.split()
        if len(parts) != 3:
            continue
        out[parts[2]] = "0x" + parts[0]
    return out


def parse_side(tag, sym):
    path = os.path.join(DUMPS, "phpclean_%s_%s.txt" % (tag, sym))
    if not os.path.exists(path):
        return None, "no dump file at %s" % path
    text = open(path).read()
    got = slice_extractor_fix.parse_objdump_text(text, sym, exact=True)
    if got is None:
        return None, ("the symbol's label line is absent from the dump -- "
                      "the build has no body for this symbol")
    raw, mnem = got
    if not mnem:
        return None, "the symbol's disassembly is empty in this build"
    return {"bytes": raw, "mnem": mnem}, None


def refuse_own_output_on_spelling_keys(path):
    """THE MECHANICAL GUARD.  Every pipeline stage that groups or pairs
    units must run the spelling-key check and REFUSE ITS OWN OUTPUT on
    failure.  This function is that refusal: it runs
    check_no_spelling_keys.py over the file just written and returns a
    nonzero exit code if the guard fails."""
    import subprocess
    proc = subprocess.run(
        [sys.executable,
         os.path.join(HERE, "check_no_spelling_keys.py"), path],
        capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % path)
    return proc.returncode


def main():
    nm = {"anchor": read_nm("anchor"), "ship": read_nm("ship")}
    dwarf = {}
    doc = json.load(open(os.path.join(HERE, "dwarf_typed_key_t27.json")))
    for rec in doc["records"]:
        if rec.get("lang") != "php":
            continue
        tag = "anchor" if "php_c_anchor" in rec["dwarf_source_binary"] else "ship"
        dwarf[(tag, rec["handler"])] = rec

    probes = {}
    absences = []
    n = 0
    for sym, role, how in SYMBOLS:
        n += 1
        rec = {
            "meta": {
                "n": str(n),
                "language": "php",
                "symbol": sym,
                "operator": "+",
                "arity": "binary",
                "position": "infix",
                "bucket": "binary_arith",
                "lhs_rep": "php zval (tagged union) reached through the execute_data frame",
                "lhs_type": "zval",
                "rhs_rep": "php zval (tagged union) reached through the execute_data frame",
                "rhs_type": "zval",
                "expression": "+",
                "route_role": role,
                "how_this_symbol_was_reached": how,
                "provenance_is_weaker": True,
            },
        }
        for tag in ("anchor", "ship"):
            side, why = parse_side(tag, sym)
            if side is None:
                absences.append({"symbol": sym, "build": tag, "reason": why})
                rec[tag] = {"present": False, "reason": why,
                            "instruction_count": 0}
                continue
            side["present"] = True
            side["load_address"] = nm[tag].get(sym)
            side["instruction_count"] = len(side["mnem"])
            side["source_dump"] = os.path.join(
                DUMPS, "phpclean_%s_%s.txt" % (tag, sym))
            d = dwarf.get((tag, sym))
            side["dwarf"] = [d] if d else []
            rec[tag] = side
        probes[str(n)] = rec

    out = {
        "meta": {
            "language": "php",
            "generator": "build_op_units_php.py",
            "task": "TASK 27 -- php handler slices in the op_units shape, from a CLEAN pair",
            "record_shape": "same as op_units_cpython.json: probes{n:{meta, anchor, ship}}",
            "extractor": "slice_extractor_fix.parse_objdump_text (the task-20 fixed extractor)",
            "pin": {
                "project": "php",
                "tag": "7.4.33",
                "runtime_banner_of_the_clean_anchor": "PHP 7.4.33 (cli) (built: Sep  1 2026 15:43:04) ( NTS )",
                "runtime_banner_of_the_clean_ship": "PHP 7.4.33 (cli) (built: Sep  1 2026 15:43:35) ( NTS )",
                "quoted_from": "interp_php.json meta.pin (tag 7.4.33) plus this session's own -v banners",
                "compromise": True,
                "compromise_history": "7.4.33 is a COMPROMISE pin recorded in interp_php.json: PHP 8.3.0 and 8.2.13 both failed the build in this container (Zend/zend_atomic.h's C11 atomic intrinsics used without the matching declaration under this compiler); 7.4 predates that file.",
            },
            "builds": {
                "anchor": {
                    "binary": "/persist/php_c_anchor/sapi/cli/php",
                    "how": "./configure --disable-all --without-pear --disable-cgi CFLAGS=\"-O0 -g -fwrapv -std=gnu17\"",
                    "recipe_lane": "t27_php_clean_build2.sh",
                },
                "ship": {
                    "binary": "/persist/php_c_ship/sapi/cli/php",
                    "how": "./configure --disable-all --without-pear --disable-cgi CFLAGS=\"-O2 -g -std=gnu17\"",
                    "recipe_lane": "t27_php_clean_build2.sh",
                },
                "what_unblocked_them": "--disable-all keeps configure from ever reaching its libxml-2.0 probe (the wall in log_095); -std=gnu17 keeps this container's gcc from rejecting php 7.4 era empty parameter lists (ext/standard/scanf.c:1044: too many arguments to function 'fn'; expected 0, have 3).",
            },
            "coverage_instrumentation_check": {
                "why": "the round-2 php lesson: a gcov-contaminated build is recorded as such, never passed off",
                "command": "nm <binary> | grep -c gcov",
                "anchor_gcov_symbols": int(container(
                    "nm /persist/php_c_anchor/sapi/cli/php 2>/dev/null | grep -c gcov") or -1),
                "ship_gcov_symbols": int(container(
                    "nm /persist/php_c_ship/sapi/cli/php 2>/dev/null | grep -c gcov") or -1),
            },
            "superseded_contaminated_pair": {
                "binaries": ["/persist/php_anchor/sapi/cli/php",
                             "/persist/php_ship/sapi/cli/php"],
                "gcov_symbols_each": int(container(
                    "nm /persist/php_anchor/sapi/cli/php 2>/dev/null | grep -c gcov") or -1),
                "status": "NOT used for any slice in this artifact; kept on disk as the record of log_095's dead end",
                "why_it_was_not_a_pair": "make relinked the same coverage-instrumented objects into both paths after configure failed; log_095 proved it with a byte-identical add_function disassembly across the two",
            },
            "provenance_is_weaker": True,
            "provenance_note": "handlers located from interp_php.json's dispatch measurement plus nm, not by the probe-generator/compile-twice pipeline; the anchor/ship pairing is a build convention (two configure invocations)",
            "evidence_class": "artifact fact (objdump of the built binaries), parsed by the fixed extractor",
            "symbol_absences": absences,
        },
        "probes": probes,
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    guard_code = refuse_own_output_on_spelling_keys(OUT)
    for k, rec in probes.items():
        print("%-56s anchor=%-4s ship=%s" % (
            rec["meta"]["symbol"],
            rec["anchor"].get("instruction_count"),
            rec["ship"].get("instruction_count")))
    print("gcov: clean anchor=%d clean ship=%d ; contaminated pair=%d each" % (
        out["meta"]["coverage_instrumentation_check"]["anchor_gcov_symbols"],
        out["meta"]["coverage_instrumentation_check"]["ship_gcov_symbols"],
        out["meta"]["superseded_contaminated_pair"]["gcov_symbols_each"]))
    for a in absences:
        print("ABSENT %s/%s -- %s" % (a["build"], a["symbol"], a["reason"]))
    return guard_code


if __name__ == "__main__":
    sys.exit(main())
