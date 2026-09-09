#!/usr/bin/env python3
"""acceptance53.py -- TASK 53's instances, printed literally.

Five parts, each one a real unit read out of the canon38 artifacts and
transcribed by layer4c.py in this process:

  (a) ONE WHOLE TRANSCRIPTION -- the ledger as stored, then the term
      that ledger reads to, then the two gate verdicts.  This is the
      brief's step 1 instance.
  (b) THE MACHINE-STACK INSTANCE -- log 152 section 3.2's own unit.
  (c) THE X87 INSTANCE -- log 152 section 3.3's own unit.
  (d) THE DESTINATION-TABLE INSTANCE -- a division unit, showing the
      quotient row and the remainder row each carrying a term.
  (e) LAYER 3 AGAINST LAYER 5 -- the two units log 147 section 8.2
      used, so the pages compare.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import layer4c                                                    # noqa: E402
import layer5                                                     # noqa: E402
import gate48                                                     # noqa: E402
import textwalk48                                                 # noqa: E402

WANTED = ("c/op_104", "c/regen_11491", "cpp/regen_36796",
          "c/op_246", "c/op_109", "go/op_319", "c/op_253")


def load_wanted():
    found = {}
    paths = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        paths.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon38_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "canon38_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name in WANTED:
            if name in found:
                continue
            unit = document["units"].get(name)
            if unit is not None:
                found[name] = unit
        if len(found) == len(WANTED):
            break
    return found


def producer_text(producer):
    if producer.get("kind") == "flag_pair":
        text = " + ".join(producer["mnem"])
    elif producer.get("kind") == "arch_opcode":
        text = producer["mnem"]
        if producer.get("writes_which_half"):
            text = "%s [%s]" % (text, producer["writes_which_half"])
    else:
        text = producer["phrase"]
    return text


def one_line(term):
    if term is None:
        return "(none)"
    return " ".join(str(term).split())


def show(name, unit, with_terms=True):
    print("  %s" % name)
    print("    LITERAL -- body:  %s" % unit["body_text"])
    print("    LITERAL -- the stored ledger:")
    print("      %-9s %-4s %-34s %-44s %s"
          % ("row", "size", "type", "produced by", "operands"))
    for row in unit["ledger"]:
        print("      %-9s %-4d %-34s %-44s %s"
              % (row["row"], row["size"], row["type"],
                 producer_text(row["produced_by"]),
                 ",".join(row["operands"])))
    record = layer4c.transcribe(unit)
    if record.refused is not None:
        print("    the transcription refused: %s" % record.refused)
        return record
    if with_terms:
        print("    LITERAL -- the term each row reads to:")
        for row in record.rows:
            term = record.terms.get(row["row"])
            print("      %-9s %s" % (row["row"], one_line(term)[:150]))
    print("    LITERAL -- the OUT-0 term:  %s"
          % one_line(record.out_term)[:400])
    for entry in record.holes:
        print("    a row with no term: %s -- %s"
              % (entry["row"], entry["why"][:120]))
    verdict, detail = gate48.gate(unit, record)
    print("    route one (the ship simulation): %s" % verdict)
    print("        %s" % detail[:220])
    verdict, detail = textwalk48.gate(unit, record)
    print("    route two (the text-order walk): %s" % verdict)
    print("        %s" % detail[:220])
    return record


def main():
    found = load_wanted()
    print("=" * 78)
    print("(a) ONE WHOLE TRANSCRIPTION, the ledger and the term it "
          "reads to")
    print("=" * 78)
    for name in ("c/op_104",):
        if name in found:
            show(name, found[name])
    print("")
    print("=" * 78)
    print("(b) THE MACHINE-STACK INSTANCE -- log 152 section 3.2's own "
          "unit")
    print("=" * 78)
    for name in ("c/regen_11491",):
        if name in found:
            show(name, found[name])
    print("")
    print("=" * 78)
    print("(c) THE X87 INSTANCE -- log 152 section 3.3's own unit")
    print("=" * 78)
    for name in ("cpp/regen_36796",):
        if name in found:
            show(name, found[name])
    print("")
    print("=" * 78)
    print("(d) THE DESTINATION-TABLE INSTANCE -- both halves carry a "
          "term")
    print("=" * 78)
    for name in ("c/op_246", "c/op_253"):
        if name in found:
            show(name, found[name])
    print("")
    print("=" * 78)
    print("(e) LAYER 3 AGAINST LAYER 5 -- log 147 section 8.2's own "
          "two units")
    print("=" * 78)
    texts = {}
    for name in ("c/op_109", "go/op_319"):
        if name not in found:
            continue
        unit = found[name]
        record = layer4c.transcribe(unit)
        text = None
        if record.out_term is not None:
            text = layer5.normalize(record.out_term)
        texts[name] = (unit["wrapped_text"], text)
        print("  %s" % name)
        print("    LITERAL -- body:      %s" % unit["body_text"])
        print("    LITERAL -- layer 3:   %s" % unit["wrapped_text"])
        print("    LITERAL -- layer 5:   %s" % text)
    if len(texts) == 2:
        left = texts["c/op_109"]
        right = texts["go/op_319"]
        print("")
        print("  layer 3 texts identical: %s" % (left[0] == right[0]))
        print("  layer 5 texts identical: %s" % (left[1] == right[1]))


if __name__ == "__main__":
    main()
