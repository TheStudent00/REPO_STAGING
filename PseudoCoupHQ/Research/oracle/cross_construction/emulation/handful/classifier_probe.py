#!/usr/bin/env python3
"""classifier_probe.py -- task h2: what the zero-operand width rule
reads, and what the classifier now answers for a line with no operand.

WHAT THIS IS, one sentence, in relation: the three objects the rule of
2026-09-09 rests on, printed LITERAL -- the two reference tables the
width is read from, the map `model_table.zero_operand_widths()` builds
from them, and `model_table.classify_line`'s own answer for each of
those mnemonics and for one control line that already classified.

WHY IT EXISTS: the rule is one `if` in a shared file, so what it reads
and what it answers are put on the record beside it rather than
described.  It measures; it changes nothing.

Coding discipline: no compound one-liner statements.

usage:
  classifier_probe.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
LEAN = os.path.join(OP, "lean")
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, "..", "..", "..",
                                             "arch_opcodes"))
MODEL = os.path.join(ARCH_OPCODES, "model")
sys.path.insert(0, OP)
sys.path.insert(0, LEAN)
sys.path.insert(0, ARCH_OPCODES)
sys.path.insert(0, MODEL)

import reference as R                                            # noqa: E402
import model_table as MTAB                                       # noqa: E402

CONTROL = [("idiv", "idiv %r10"), ("imul", "imul %esi,%eax"),
           ("ret", "ret")]
"""three lines that already classified before the rule was added (or
that are chaff and never reach it), so a move in any of them would be
visible."""


def main():
    MTAB._install_gpr_widths()
    print("reference.SPREAD_SIGN, LITERAL: %s"
          % json.dumps(R.SPREAD_SIGN, sort_keys=True))
    print("reference.ACCUMULATOR_WIDEN, LITERAL: %s"
          % json.dumps(R.ACCUMULATOR_WIDEN, sort_keys=True))
    print("model_table.ZERO_OPERAND_WIDTH, LITERAL: %s"
          % json.dumps(MTAB.ZERO_OPERAND_WIDTH, sort_keys=True))
    print("")
    print("the zero-operand mnemonics, classify_line(mnem, mnem, 0):")
    for mnem in sorted(MTAB.ZERO_OPERAND_WIDTH):
        shape, width, cause = MTAB.classify_line(mnem, mnem, 0)
        key = None
        if width is not None:
            key = MTAB.key_width(mnem, width)
        print("   %-6s shape %s width %s key_width %s cause %s"
              % (mnem, shape, width, key, cause))
    print("")
    print("the control lines, unchanged by the rule:")
    for mnem, line in CONTROL:
        shape, width, cause = MTAB.classify_line(mnem, line, 0)
        key = None
        if width is not None:
            key = MTAB.key_width(mnem, width)
        print("   %-6s shape %s width %s key_width %s cause %s"
              % (line, shape, width, key, cause))
    print("")
    document = json.load(open(MTAB.ROWS_JSON))
    triples = set()
    for row in document["rows"]:
        if row["outcome"] != "TRANSLATED":
            continue
        triples.add((row["mnem"], row["shape"], row["key_width"]))
    print("TRANSLATED triples in %s: %d" % (MTAB.ROWS_JSON,
                                            len(triples)))
    for mnem in sorted(MTAB.ZERO_OPERAND_WIDTH):
        shape, width, cause = MTAB.classify_line(mnem, mnem, 0)
        if width is None:
            print("   %-6s classifies to nothing: %s" % (mnem, cause))
            continue
        key = MTAB.key_width(mnem, width)
        held = (mnem, shape, key) in triples
        print("   %-6s (%s, %s, %s) is a TRANSLATED row of the table: %s"
              % (mnem, mnem, shape, key, held))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
