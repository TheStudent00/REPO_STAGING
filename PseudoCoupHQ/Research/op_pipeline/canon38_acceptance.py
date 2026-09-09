#!/usr/bin/env python3
"""canon38_acceptance.py -- TASK 52's five acceptance instances, printed
with their values, canon37 beside canon38.

  (a) c/op_210 -- the implicit destination.  The ledger before and
      after, row by row.
  (b) a push/pop unit -- its STACK rows.
  (c) a fucomip unit -- its X87 rows.
  (d) go/op_174 and go/op_180 -- the two layer-3 texts, which must now
      be the same string.
  (e) c/op_109 and go/op_319 -- unchanged in verdict.

Nothing here selects a unit by an operator token: (a), (d) and (e) are
named in the brief, (b) and (c) are found by the MNEMONICS their
bodies spell, which is machine-form evidence.

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

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    path = os.path.join(HERE, name)
    return json.load(open(path))


def population(prefix):
    """every unit of every population, from one lap's artifacts."""
    units = {}
    for lang in LANGS:
        units.update(load("%s_wrapped_%s.json" % (prefix, lang))["units"])
    units.update(load("%s_interp.json" % prefix)["units"])
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "%s_regen_store" % prefix,
                                              "*.json"))):
        units.update(json.load(open(path))["units"])
    return units


def print_ledger(record, title):
    print(title)
    body = record.get("body_text")
    print("  body   : %s" % body)
    stored = record.get("body_verbatim")
    if stored is not None:
        print("  stored : %s" % "; ".join(stored))
    print("  %-8s %-4s %-22s %-38s %s"
          % ("row", "size", "type", "produced by", "operands"))
    for row in record.get("ledger") or []:
        produced = row["produced_by"]
        if isinstance(produced, dict):
            produced = json.dumps(produced, sort_keys=True)
        print("  %-8s %-4s %-22s %-38s %s"
              % (row["row"], row["size"], row["type"], produced,
                 ",".join(row["operands"])))


def find_by_mnemonics(units, wanted, longest):
    """the shortest unit whose body spells every mnemonic in `wanted`."""
    best = None
    for label in sorted(units):
        record = units[label]
        body = record.get("body_text")
        if not body:
            continue
        lines = [x.strip().split(" ")[0] for x in body.split(";")]
        ok = True
        for mnemonic in wanted:
            if mnemonic not in lines:
                ok = False
        if not ok:
            continue
        if len(lines) > longest:
            continue
        if best is None:
            best = label
            continue
        if len(lines) < len(units[best]["body_text"].split(";")):
            best = label
    return best


def main():
    old = population("canon37")
    new = population("canon38")
    print("canon37 units: %d      canon38 units: %d" % (len(old),
                                                        len(new)))

    print("")
    print("=" * 70)
    print("(a) c/op_210 -- THE IMPLICIT DESTINATION")
    print("=" * 70)
    print_ledger(old["c/op_210"], "canon37 (ledger47)")
    print("")
    print_ledger(new["c/op_210"], "canon38 (ledger48)")
    print("")
    print("  canon37 outcome %s / verdict %s"
          % (old["c/op_210"]["outcome"], old["c/op_210"]["verdict"]))
    print("  canon38 outcome %s / verdict %s"
          % (new["c/op_210"]["outcome"], new["c/op_210"]["verdict"]))

    print("")
    print("=" * 70)
    print("(b) A PUSH/POP UNIT -- THE STACK ROWS")
    print("=" * 70)
    label = find_by_mnemonics(new, ["push", "pop"], 12)
    print("unit chosen by the mnemonics its body spells: %s" % label)
    print_ledger(old[label], "canon37 (ledger47) -- no STACK block")
    print("")
    print_ledger(new[label], "canon38 (ledger48)")
    stack_rows = []
    for row in new[label]["ledger"]:
        if row["block"] == "STACK":
            stack_rows.append(row["row"])
    print("  STACK rows: %s" % (", ".join(stack_rows) or "none"))

    print("")
    print("=" * 70)
    print("(b2) go/op_110 -- A PUSH/POP UNIT WHOSE ANSWER THE "
          "DESTINATION TABLE RECOVERS")
    print("=" * 70)
    print_ledger(old["go/op_110"], "canon37 (ledger47)")
    print("")
    print_ledger(new["go/op_110"], "canon38 (ledger48)")
    print("  canon37 outcome %s / verdict %s"
          % (old["go/op_110"]["outcome"], old["go/op_110"]["verdict"]))
    print("  canon38 outcome %s / verdict %s"
          % (new["go/op_110"]["outcome"], new["go/op_110"]["verdict"]))

    print("")
    print("=" * 70)
    print("(c) A fucomip UNIT -- THE X87 ROWS")
    print("=" * 70)
    label = find_by_mnemonics(new, ["fucomip"], 12)
    print("unit chosen by the mnemonics its body spells: %s" % label)
    print_ledger(old[label], "canon37 (ledger47) -- no X87 block")
    print("")
    print_ledger(new[label], "canon38 (ledger48)")
    x87_rows = []
    for row in new[label]["ledger"]:
        if row["block"] == "X87":
            x87_rows.append(row["row"])
    print("  X87 rows: %s" % (", ".join(x87_rows) or "none"))

    print("")
    print("=" * 70)
    print("(d) go/op_174 AND go/op_180 -- THE LAYER-3 TEXTS")
    print("=" * 70)
    for label in ["go/op_174", "go/op_180"]:
        print("canon37 %s" % label)
        print("   %s" % old[label]["wrapped_text"])
    print("canon37 identical: %s"
          % (old["go/op_174"]["wrapped_text"]
             == old["go/op_180"]["wrapped_text"]))
    print("")
    for label in ["go/op_174", "go/op_180"]:
        print("canon38 %s" % label)
        print("   %s" % new[label]["wrapped_text"])
    print("canon38 identical: %s"
          % (new["go/op_174"]["wrapped_text"]
             == new["go/op_180"]["wrapped_text"]))

    print("")
    print("=" * 70)
    print("(e) c/op_109 AND go/op_319 -- UNCHANGED IN VERDICT")
    print("=" * 70)
    for label in ["c/op_109", "go/op_319"]:
        was = old[label]
        now = new[label]
        print("%-12s canon37 %-22s %-24s" % (label, was["outcome"],
                                             was.get("verdict")))
        print("%-12s canon38 %-22s %-24s" % ("", now["outcome"],
                                             now.get("verdict")))
        print("             body    %s" % now.get("body_text"))
        print("             text37  %s" % was.get("wrapped_text"))
        print("             text38  %s" % now.get("wrapped_text"))
        print("             same outcome: %s   same verdict: %s   "
              "same text: %s"
              % (was["outcome"] == now["outcome"],
                 was.get("verdict") == now.get("verdict"),
                 was.get("wrapped_text") == now.get("wrapped_text")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
