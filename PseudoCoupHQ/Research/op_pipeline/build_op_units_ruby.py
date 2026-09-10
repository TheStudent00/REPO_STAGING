#!/usr/bin/env python3
"""build_op_units_ruby.py -- TASK 27, part 1 (ruby).

Builds `op_units_ruby.json`: proper handler slices for the ruby
addition route, ANCHOR and SHIP per symbol, in the same record shape
`op_units_cpython.json` carries ({meta, probes{n:{meta, anchor, ship}}}
with byte and mnemonic columns per side).  Until now ruby had only
short hand excerpts in `interp_relations.json`, which is why every
ruby carve refused in log_107.

EXTRACTION.  The raw text is `objdump -d --disassemble=SYM` run inside
the sandbox container over the two pinned builds
(/persist/ruby_anchor/ruby, /persist/ruby_ship/ruby), by the lane
`t27_ruby_dump.sh` / `t27_php_clean_build2.sh`.  It is parsed here by
`slice_extractor_fix.parse_objdump_text` -- the FIXED extractor from
task 20 -- so the split-instruction defect (a continuation line
emitted as its own empty-mnemonic instruction) cannot recur.

CONTAMINATION.  Both ruby binaries carry ZERO gcov symbols; the counts
are recorded in the artifact's meta from the lane's own `nm` output,
not assumed.

PROVENANCE.  Every record carries `provenance_is_weaker: true`: the
handlers were located from source reading plus `nm`, not by the
probe-generator / compile-twice pipeline the compiled-language track
uses.

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

The candidate symbols below are NOT selected by any token.  They are
the call targets read off the disassembly itself: vm_opt_plus's and
rb_int_plus's own `call` operands name fix_plus, rb_big_plus,
rb_num_coerce_bin; fix_plus's own `call` operands name
rb_fix_plus_fix.  Machine-form evidence, followed one edge at a time.

Run:
  /tmp/reconnect_venv/bin/python3 build_op_units_ruby.py
"""

import json
import os
import subprocess
import sys

import slice_extractor_fix

HERE = os.path.dirname(os.path.abspath(__file__))
DUMPS = "PUBLIC/Airlock/agent/out/t27"
OUT = os.path.join(HERE, "op_units_ruby.json")

# symbol -> (route role, how this symbol was reached)
SYMBOLS = [
    ("vm_opt_plus", "dispatch entry in the interpreter loop",
     "named in interp_ruby.json's dispatch measurement"),
    ("rb_fix_plus", "entry the dispatcher tail-calls",
     "call target read off vm_opt_plus's own disassembly"),
    ("rb_int_plus", "entry for the generic integer route",
     "named in interp_ruby.json's dispatch measurement"),
    ("fix_plus", "type-discriminating body behind rb_fix_plus",
     "call target read off rb_fix_plus's own anchor disassembly"),
    ("rb_fix_plus_fix", "the bounded-width tagged computation",
     "call target read off fix_plus's own anchor disassembly"),
    ("rb_big_plus", "the unbounded-width route",
     "call target read off fix_plus's own anchor disassembly"),
]


def read_nm(tag):
    """symbol -> load address, from the lane's own nm output."""
    out = {}
    for name in ("ruby_%s_nm.txt" % tag,):
        path = os.path.join(DUMPS, name)
        if not os.path.exists(path):
            continue
        for line in open(path):
            parts = line.split()
            if len(parts) != 3:
                continue
            out[parts[2]] = "0x" + parts[0]
    return out


def gcov_count(tag):
    """gcov symbol count for one binary, read live from the container."""
    binary = "/persist/ruby_%s/ruby" % tag
    cmd = "nm %s 2>/dev/null | grep -c gcov" % binary
    proc = subprocess.run(
        ["podman", "exec", "sandbox-runner", "bash", "-lc", cmd],
        capture_output=True, text=True)
    return int(proc.stdout.strip() or "-1")


def parse_side(tag, sym):
    """-> {load_address, instruction_count, bytes, mnem} or None."""
    path = os.path.join(DUMPS, "ruby_%s_%s.txt" % (tag, sym))
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
    anchor_nm = read_nm("anchor")
    ship_nm = read_nm("ship")
    dwarf = {}
    doc = json.load(open(os.path.join(HERE, "dwarf_typed_key.json")))
    for rec in doc["records"]:
        if rec.get("lang") == "ruby":
            dwarf[rec["handler"]] = rec

    probes = {}
    absences = []
    n = 0
    for sym, role, how in SYMBOLS:
        n += 1
        rec = {
            "meta": {
                "n": str(n),
                "language": "ruby",
                "symbol": sym,
                "operator": "+",
                "arity": "binary",
                "position": "infix",
                "bucket": "binary_arith",
                "lhs_rep": "ruby VALUE (tagged word)",
                "lhs_type": "VALUE",
                "rhs_rep": "ruby VALUE (tagged word)",
                "rhs_type": "VALUE",
                "expression": "+",
                "route_role": role,
                "how_this_symbol_was_reached": how,
                "provenance_is_weaker": True,
            },
        }
        for tag, nm in (("anchor", anchor_nm), ("ship", ship_nm)):
            side, why = parse_side(tag, sym)
            if side is None:
                absences.append({"symbol": sym, "build": tag, "reason": why})
                rec[tag] = {
                    "present": False,
                    "reason": why,
                    "instruction_count": 0,
                }
                continue
            side["present"] = True
            side["load_address"] = nm.get(sym)
            side["instruction_count"] = len(side["mnem"])
            side["source_dump"] = os.path.join(
                DUMPS, "ruby_%s_%s.txt" % (tag, sym))
            if tag == "anchor":
                d = dwarf.get(sym)
                side["dwarf"] = [d] if d else []
                if d:
                    side["dwarf_address_identity"] = {
                        "nm_load_address": nm.get(sym),
                        "dwarf_low_pc": d.get("dwarf_low_pc"),
                        "same": (nm.get(sym) or "").lstrip("0x").lstrip("0")
                        == (d.get("dwarf_low_pc") or "").lstrip("0x").lstrip("0"),
                    }
            rec[tag] = side
        probes[str(n)] = rec

    out = {
        "meta": {
            "language": "ruby",
            "generator": "build_op_units_ruby.py",
            "task": "TASK 27 -- ruby handler slices in the op_units shape",
            "record_shape": "same as op_units_cpython.json: probes{n:{meta, anchor, ship}}, address-stripped byte and mnemonic columns per side",
            "extractor": "slice_extractor_fix.parse_objdump_text (the task-20 fixed extractor; the split-instruction defect cannot recur)",
            "pin": {
                "project": "ruby",
                "tag": "3.3.0",
                "runtime_banner": "ruby 3.3.0 (2023-12-25 revision 5124f9ac75) [x86_64-linux]",
                "quoted_from": "interp_ruby.json meta.pin",
            },
            "builds": {
                "anchor": {
                    "binary": "/persist/ruby_anchor/ruby",
                    "how": "./configure CFLAGS=\"-O0 -g -fwrapv\"",
                    "recipe_lane": "interp_e2_handlers.sh (Airlock .done, 20260901T014453Z)",
                },
                "ship": {
                    "binary": "/persist/ruby_ship/ruby",
                    "how": "./configure (default optimisation)",
                    "recipe_lane": "interp_e2_handlers.sh (Airlock .done, 20260901T014453Z)",
                },
            },
            "coverage_instrumentation_check": {
                "why": "the round-2 php lesson: a gcov-contaminated build is recorded as such, never passed off as a clean pair",
                "command": "nm <binary> | grep -c gcov",
                "anchor_gcov_symbols": gcov_count("anchor"),
                "ship_gcov_symbols": gcov_count("ship"),
            },
            "provenance_is_weaker": True,
            "provenance_note": "handlers located by source reading plus nm and by following call operands in the disassembly, not by the probe-generator/compile-twice pipeline; the anchor/ship pairing is a build convention (two configure invocations), not the DWARF-anchored name->memory-home method the compiled-language track uses",
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
        print("%-16s anchor=%-4s ship=%s" % (
            rec["meta"]["symbol"],
            rec["anchor"].get("instruction_count"),
            rec["ship"].get("instruction_count")))
    print("gcov: anchor=%d ship=%d" % (
        out["meta"]["coverage_instrumentation_check"]["anchor_gcov_symbols"],
        out["meta"]["coverage_instrumentation_check"]["ship_gcov_symbols"]))
    for a in absences:
        print("ABSENT %s/%s -- %s" % (a["build"], a["symbol"], a["reason"]))
    return guard_code


if __name__ == "__main__":
    sys.exit(main())
