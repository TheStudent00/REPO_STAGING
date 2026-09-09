#!/usr/bin/env python3
"""layer5.py -- LAYER 5: THE FIXED-RULE RE-RENDER, THE TEXTUAL
NORMALIZER.

DEE'S RULING 4, which this file implements: "LAYER 5 (the fixed-rule
re-render) is the TEXTUAL NORMALIZER applied after proof so equivalent
units become textually identical; never the only route to a canonical
text -- layer 3 (the wrapped body) exists for every unit regardless."

SO WHAT THIS FILE IS FOR, said plainly.  Layer 3 is the unit's wrapped
text -- real instructions, the compiler's own choices among them.  Two
units that compute the same thing can spell it differently there, and
they do.  Layer 5 takes the PROVED term (layer 4) and prints it by ONE
FIXED RULE, so two units whose terms are the same object print the same
characters.  Nothing here decides equivalence; it only makes proved
equivalence visible to a text-keyed reader.

THE FIXED RULE, stated in full:

  1. The term is put through z3's own simplifier, once, with a fixed
     set of switches.  The simplifier is a function of the term alone,
     so two equal terms in the same shape reach the same normal form.
  2. Free symbols are renamed POSITIONALLY, in the order they first
     appear in a left-to-right walk of the simplified term: the first
     becomes `v0`, the second `v1`, and so on.  A register name never
     survives into the normalized text, so two units that differ only
     in which register an argument arrived in print identically.
  3. The result is printed by z3's own printer with line wrapping
     turned off, so the text is one line and comparison is character
     comparison.

WHAT THIS RULE DOES NOT DO, named rather than glossed over.  It does
not render the term back into arch instructions.  The accumulate ruling
requires a return path from any transform back to canonical runnable
text, and that path is NOT built in this file: layer 3's wrapped text
is the runnable record for every unit, and layer 5 is a comparison key
computed beside it.  A term-to-instructions renderer is named here as
the work that is not done, rather than implied by a word like
"normalized".

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
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                         # noqa: E402


def free_symbols_in_order(term):
    """every free symbol, in the order a left-to-right walk meets it."""
    seen = []
    known = set()
    stack = [term]
    while stack:
        node = stack.pop()
        if z3.is_const(node) and node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            key = node.decl().name()
            if key not in known:
                known.add(key)
                seen.append(node)
            continue
        children = list(node.children())
        children.reverse()
        stack.extend(children)
    return seen


def ordered_symbols(term):
    """the same list, but in the order the PRINTED term shows them, so
    the renaming is a function of the printed shape and nothing else."""
    text = term.sexpr()
    found = free_symbols_in_order(term)
    def position(symbol):
        where = text.find(symbol.decl().name())
        return where if where >= 0 else len(text)
    return sorted(found, key=position)


def normalize(term):
    """THE FIXED RULE.  Returns the normalized text, one line."""
    simplified = z3.simplify(term)
    symbols = ordered_symbols(simplified)
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        substitution.append((symbol, fresh))
    if substitution:
        simplified = z3.substitute(simplified, *substitution)
    simplified = z3.simplify(simplified)
    return one_line(simplified)


def one_line(term):
    z3.set_option(max_width=1000000, max_lines=1000000,
                  max_depth=1000000, max_args=1000000)
    text = str(term)
    text = " ".join(text.split())
    return text
