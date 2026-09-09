#!/usr/bin/env python3
"""canon36_assemble.py -- TASK 43: every region text ASSEMBLES.

Each proved region text is written into a real `.s` file as its own
symbol, assembled with `as --64`, and read back with `objdump -d`.  A
unit passes only when its symbol appears in the disassembly with at
least as many instructions as the text spells.  Nothing is simulated:
this is the assembler and the disassembler, on disk, on real bytes.
It is the cross-check the structural route's one interpretation-class
step needs (that a `mov` leaves the flags alone), and it is the check
that `0xNN(%r15)` is a real encoding rather than a notation.

The batching, the per-unit re-run on a failing batch, the reading-
annotation strip, the rip-relative constant pool and the local-label
scheme are canon35_assemble.py's, IMPORTED rather than copied so they
cannot drift.  Only the sources differ: this reads the three round-9
populations.

The regenerated population is SAMPLED and the sample is named as one:
it is 27,000-odd units and the assembler cost is linear, so a fixed
stride is taken over the whole population rather than a prefix, and
the stride is recorded.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon35_assemble as A35                                   # noqa: E402

WORK = "/tmp/canon36_assemble_work"
OUT = os.path.join(HERE, "canon36_assemble.json")
REGEN_STRIDE = 30


def sources():
    """(label, text, population) for every proved region text."""
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, "canon36_universal_%s.json" % lang)
        if not os.path.exists(path):
            continue
        for label, rec in json.load(open(path))["units"].items():
            text = rec.get("universal_text")
            if text:
                out.append((label, text, "original"))
    path = os.path.join(HERE, "canon36_interp.json")
    if os.path.exists(path):
        for label, rec in json.load(open(path))["units"].items():
            text = rec.get("universal_text")
            if text:
                out.append((label, text, "interpreter"))
    regen = []
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon36_regen_store",
                                              "*.json"))):
        for label, rec in json.load(open(path))["units"].items():
            text = rec.get("universal_text")
            if text:
                regen.append((label, text, "regenerated"))
    sampled = regen[::REGEN_STRIDE]
    return out, sampled, len(regen)


def main():
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    A35.WORK = WORK
    whole, sampled, regen_total = sources()
    offered = whole + sampled
    items = []
    per_unit = {}
    for label, text, population in offered:
        symbol = "u_" + label.replace("/", "_")
        lines, count, notes = A35.normalize(symbol, text)
        items.append((symbol, lines, count))
        per_unit[symbol] = {
            "unit": label,
            "population": population,
            "instruction_lines": count,
            "normalizations": notes,
        }
    batches = []
    index = 0
    while index < len(items):
        batches.append(items[index:index + A35.BATCH])
        index = index + A35.BATCH
    assembled = 0
    failures = []
    for number, batch in enumerate(batches):
        source = os.path.join(WORK, "batch_%04d.s" % number)
        obj = os.path.join(WORK, "batch_%04d.o" % number)
        A35.write_batch(source, batch)
        code, err = A35.assemble(source, obj)
        if code != 0:
            for one in batch:
                single = os.path.join(WORK, "one_%s.s" % one[0])
                single_obj = os.path.join(WORK, "one_%s.o" % one[0])
                A35.write_batch(single, [one])
                one_code, one_err = A35.assemble(single, single_obj)
                if one_code != 0:
                    failures.append({
                        "unit": per_unit[one[0]]["unit"],
                        "assembler_message": one_err.strip()[:400],
                    })
                    per_unit[one[0]]["assembles"] = False
                    continue
                dump = A35.disassemble(single_obj)
                seen = A35.counts_from_dump(dump)
                per_unit[one[0]]["assembles"] = True
                per_unit[one[0]]["disassembled_instructions"] = \
                    seen.get(one[0], 0)
                assembled = assembled + 1
            continue
        dump = A35.disassemble(obj)
        seen = A35.counts_from_dump(dump)
        for one in batch:
            got = seen.get(one[0], 0)
            ok = got >= one[2]
            per_unit[one[0]]["assembles"] = ok
            per_unit[one[0]]["disassembled_instructions"] = got
            if ok:
                assembled = assembled + 1
            else:
                failures.append({
                    "unit": per_unit[one[0]]["unit"],
                    "assembler_message":
                        "the symbol disassembled to %d instructions, "
                        "fewer than the %d the text spells"
                        % (got, one[2]),
                })
    document = {
        "meta": {
            "produced_by": "canon36_assemble.py",
            "role": "generator provenance",
            "regenerated_population_is_sampled": {
                "stride": REGEN_STRIDE,
                "sampled": len(sampled),
                "of": regen_total,
            },
        },
        "offered": len(items),
        "assembled": assembled,
        "failed": len(failures),
        "failures": failures[:200],
        "units": per_unit,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("offered %d  assembled %d  failed %d"
          % (len(items), assembled, len(failures)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
