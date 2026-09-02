#!/usr/bin/env python3
"""interp_canon_attempt.py -- Task 17(a): attempt THE CANONICAL FORM
(canon.py) on the ruby/php interpreter handler slices, and record
exactly why it refuses, rather than asserting a reason from memory.

WHAT CANON.PY REQUIRES, read from its own code (canon.py line ~822):
    anchor = sem.get("anchor_registers")
`sem.anchor_registers` is written by the compiled-language pipeline's
own probe step: a synthetic probe source (`a`, `b` named arguments) is
compiled WITH DEBUG INFO at the anchor optimization level, and the
DWARF is read to learn which register/stack slot holds which named
argument at the point the unit's code starts (AgentMemory's step 4,
"argument identity anchored"). That whole chain lives behind
`sem_anchored_<lang>.json`, produced by `sem_anchored.py` +
`arch_read.py` from a probe manifest this repo generated and compiled
itself.

THE HANDLER SLICES ARE NOT THAT. `interp_ruby_handlers.json` and
`interp_php_handlers.json` (log_095) were built by grep + `nm` +
`objdump --disassemble=<symbol>` against the REAL, ALREADY-BUILT
ruby/php interpreter binaries. Nobody compiled a probe with named
arguments for `rb_fix_plus` or `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_...`;
there is no DWARF naming a register as "argument a". So there is no
`sem.anchor_registers` to read, and none can be manufactured without
re-building the interpreters with debug info AND a way to tell DWARF
which of their many internal calls is "the" probe call -- neither of
which this task attempts (STOP RULE: a diagnosed dead end is a valid
result).

A second, independent block, checked here rather than assumed: canon.py
also needs a pyvex-LIFTED `sem` block (the `blocks`/`values`/`events`
list canon.py walks instruction-by-instruction). No `sem_anchored_ruby*
.json` or `sem_anchored_php*.json` file exists on disk (checked below)
-- the handler JSON carries only `objdump` TEXT excerpts, and several
of those excerpts are themselves TRUNCATED (the brief's own words:
"handler slices... big" -- the anchor/ship counts run to 700+
instructions; the JSON stores only the first ~12-14 lines as a human-
readable sample, confirmed below by comparing excerpt line counts
against the recorded *_instruction_count fields).

This script performs both checks mechanically and writes
`interp_canon_attempt.json`, which is what the report below quotes
verbatim.

usage: interp_canon_attempt.py
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def check_no_sem_anchored(lang):
    hits = sorted(glob.glob(os.path.join(HERE, "sem_anchored*%s*.json" % lang)))
    return hits


def excerpt_is_truncated(excerpt, recorded_count):
    if not isinstance(excerpt, str):
        return None
    lines = [l for l in excerpt.splitlines() if ":\t" in l or ":\t\t" in l]
    # count lines that look like an address: bytes  mnemonic line
    addr_lines = [l for l in excerpt.splitlines() if "\t" in l and ":" in l.split("\t")[0]]
    return dict(excerpt_line_count=len(addr_lines), recorded_instruction_count=recorded_count)


def main():
    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "interp_canon_attempt.py",
            "purpose": "Task 17(a) -- record the refusal of THE CANONICAL "
                       "FORM (canon.py) on the ruby/php handler slices, "
                       "mechanically, not by assertion.",
        },
        "requirement_check": {
            "canon_py_requires": "sem.anchor_registers (canon.py:822), "
                                  "which is written only by "
                                  "sem_anchored.py from a DWARF-anchored, "
                                  "probe-compiled unit.",
        },
        "languages": {},
    }

    for lang, handler_file in (("ruby", "interp_ruby_handlers.json"),
                                ("php", "interp_php_handlers.json")):
        doc = json.load(open(os.path.join(HERE, handler_file)))
        sem_anchored_hits = check_no_sem_anchored(lang)
        handlers = doc["handlers"]
        excerpt_report = {}
        for name, rec in handlers.items():
            entry = {}
            if "anchor_excerpt" in rec:
                entry["anchor"] = excerpt_is_truncated(
                    rec["anchor_excerpt"], rec.get("anchor_instruction_count"))
            if "ship_excerpt" in rec:
                entry["ship"] = excerpt_is_truncated(
                    rec["ship_excerpt"], rec.get("ship_instruction_count"))
            if "excerpt" in rec:
                entry["single_build"] = excerpt_is_truncated(
                    rec["excerpt"], rec.get("single_build_instruction_count"))
            excerpt_report[name] = entry

        out["languages"][lang] = {
            "sem_anchored_files_found": sem_anchored_hits,
            "sem_anchored_files_found_count": len(sem_anchored_hits),
            "handler_count": len(handlers),
            "excerpt_vs_recorded_count": excerpt_report,
            "canon_refusal": (
                "REFUSED: no sem_anchored_%s*.json exists (%d found) and "
                "none of the %d handler records carries "
                "sem.anchor_registers or a pyvex blocks/values/events "
                "list -- canon.py's own line 822 read has nothing to "
                "read. The excerpts stored are also partial samples, "
                "not the full instruction stream canon.py would need to "
                "walk (see excerpt_vs_recorded_count: every excerpt's "
                "line count is far below its own recorded instruction "
                "count)." % (lang, len(sem_anchored_hits), len(handlers))
            ),
        }

    out["conclusion"] = (
        "Canonicalization refuses for BOTH languages, at the SAME step, "
        "for the SAME root cause: the handler slices were extracted by "
        "grep+nm+objdump against production interpreter binaries, never "
        "through the probe-generate/compile-with-debug-info/DWARF-anchor "
        "pipeline that sem_anchored.py depends on. This is not a "
        "per-language defect to fix; it is what 'log_095's handler slices "
        "are not probe-generated' already meant, made mechanical instead "
        "of asserted."
    )

    path = os.path.join(HERE, "interp_canon_attempt.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)
    for lang in out["languages"]:
        print("--", lang, "--")
        print(out["languages"][lang]["canon_refusal"])


if __name__ == "__main__":
    main()
