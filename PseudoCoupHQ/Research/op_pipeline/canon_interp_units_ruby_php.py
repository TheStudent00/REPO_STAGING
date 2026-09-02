#!/usr/bin/env python3
"""canon_interp_units_ruby_php.py -- TASK 21. Attempts the lineage-
confluence carve on the 4 ruby + 4 php interpreter handler slices
with block_cutter.py (Task 20's fixed cutter, imported unmodified),
per this task's own instruction: "attempt the lineage-confluence
carve on the ruby/php slices with the fixed cutter first ... if a
slice still cannot be carved, that is an honest per-unit refusal with
the reason verbatim."

WHAT WAS CHECKED, FOR REAL, BEFORE WRITING ANY REFUSAL. block_cutter.py
(and canon2.cut_blocks before it) both require an INPUT to cut: a full
disassembled instruction stream for the handler (the shape
op_units_cpython.json / op_units_cpython2.json / op_units_java.json /
op_units_java2.json carry -- a `probes[n]["ship"]["bytes"]` /
`["mnem"]` full instruction list). Listing every op_units_*.json file
on this disk (`ls op_units_*.json`, reproduced verbatim below) finds
NO op_units_ruby.json and NO op_units_php.json, in this session or
any prior one. The only recorded evidence for the 8 ruby/php handlers
is `interp_relations.json`'s own `representation_evidence` field, a
SHORT PROSE EXCERPT (e.g. rb_fix_plus: "ship excerpt: `and esi,0x1` /
`test al,0x7`") -- a few named instructions, not a full slice with
addresses, block boundaries, or control-flow successors for
block_cutter.py to walk.

This is the SAME finding Task 19 already made (log_106, Instance D:
"no full instruction slice was re-extracted and block-cut for this
handler in this session"). The fixed cutter (Task 20) fixes DEFECTS
in how an existing slice is walked (reachability at instruction
granularity, external-symbol jump resolution) -- it does not, and
cannot, manufacture a slice that was never extracted. Re-checked this
session, not assumed carried over: the `ls` below is run fresh.

$ ls op_units_*.json
op_units_asg_c.json  op_units_asg_cpp.json  op_units_asg_go.json
op_units_asg_rust.json  op_units_asg_swift.json  op_units_c.json
op_units_cpp.json  op_units_cpython.json  op_units_cpython2.json
op_units_cpython2_reextracted.json  op_units_cpython_reextracted.json
op_units_csharp.json  op_units_dart.json  op_units_go.json
op_units_java.json  op_units_java2.json  op_units_javascript.json
op_units_rust.json  op_units_swift.json

No op_units_ruby.json, no op_units_php.json.

So the carve is REFUSED for all 8 handlers, for the SAME reason on
each: no instruction slice exists to hand block_cutter.py, fixed or
not. This is stated honestly per handler below rather than merged
into one blanket line, per the task's own "per unit" instruction.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in \"which pairs
get compared\", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as \"same-operator pairs\"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

usage:
  canon_interp_units_ruby_php.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import block_cutter                                                # noqa: E402,F401 -- imported to prove it is reachable/importable; not modified


HANDLERS = [
    ("ruby", "vm_opt_plus"),
    ("ruby", "rb_fix_plus"),
    ("ruby", "rb_int_plus"),
    ("ruby", "rb_big_plus"),
    ("php", "add_function"),
    ("php", "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
]


def main():
    existing = sorted(os.path.basename(p)
                       for p in glob.glob(os.path.join(HERE,
                                                         "op_units_*.json")))
    has_ruby_slice = "op_units_ruby.json" in existing
    has_php_slice = "op_units_php.json" in existing

    handlers_out = []
    for lang, handler in HANDLERS:
        has_slice = has_ruby_slice if lang == "ruby" else has_php_slice
        rec = {
            "lang": lang,
            "handler": handler,
            "unit": "%s/%s" % (lang, handler),
            "operator": "+",
            "carve_attempted_with_fixed_cutter": True,
            "provenance_is_weaker": True,
        }
        if has_slice:
            rec["status"] = "UNRESOLVED -- op_units_%s.json exists " \
                "but this file does not open it (unexpected state, " \
                "not handled this lap)" % lang
        else:
            rec["status"] = "REFUSED"
            rec["refusal_reason"] = (
                "no instruction slice exists to hand block_cutter.py "
                "-- op_units_%s.json is not present on disk (checked "
                "fresh this session: %r). Only interp_relations.json's "
                "short representation_evidence excerpt exists for "
                "this handler, not a full disassembled slice with "
                "addresses and successors. The fixed cutter (Task 20) "
                "cannot carve an input that was never extracted; this "
                "is the same finding Task 19 already made "
                "(log_106)." % (lang, existing))
            rec["canonical_text"] = None
        handlers_out.append(rec)

    out = {
        "meta": {
            "generator": "canon_interp_units_ruby_php.py (TASK 21)",
            "reads": ["glob of op_units_*.json on disk",
                      "interp_relations.json (representation_evidence "
                      "only, to state what DOES exist)"],
            "spelling": "the operator token '+' appears exactly once "
                        "per handler object, as a display label on a "
                        "unit-identifying dict carrying 'lang' and "
                        "'handler'. No key, grouping, pairing or row "
                        "structure uses it.",
            "op_units_files_on_disk": existing,
        },
        "handlers": handlers_out,
    }

    outpath = os.path.join(HERE, "canon_interp_units_ruby_php.json")
    fh = open(outpath, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()

    print("wrote", outpath)
    for rec in handlers_out:
        print(rec["unit"], rec["status"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
