#!/usr/bin/env python3
"""normalize_order_probe65.py -- A MEASUREMENT, not a change.

THE OBSERVATION that produced it.  Nine of the 35 pool4 -> pool5 splits
contain no member that lost its layer-5 key, so the withdrawal of
disproved terms does not explain them.  Reading their members' layer-5
texts side by side shows the whole difference is the ORDER OF THE
ARGUMENTS of a commutative operator.  LITERAL, `c/regen_16844` and
`c/regen_16900`, the two texts pool5 printed for them, differing only
in the two arguments of one `Or`:

    ... If(Or(Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0)),
              fpIsNaN(fpToFP(Extract(31, 0, v0)))), 1, 0) ...
    ... If(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))),
              Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0))), 1, 0) ...

`Or(p, q)` and `Or(q, p)` are the same value.  The normalize CORE's
definition says the rule exists "so that two units computing the same
thing print the same string"; on these units the three steps it
numbers do not achieve that, because nothing in them fixes the order
of a commutative operator's arguments and `z3.simplify` does not fix
it either.

WHAT THIS FILE DOES.  It re-walks the population and prints, side by
side, how many distinct layer-5 texts there are under the rule as it
stands and under the rule with one further printing step -- the
arguments of a commutative operator sorted by their own printed text.
It CHANGES NOTHING: it does not write into `term65_store`, it does not
edit `term.py`, and it writes only its own two artifacts.  The decision
about whether the rule gains that step is made against the CORE with
this measurement in hand, never the other way round.

WRITES:
  normalize_order_probe65.json
  normalize_order_probe65_printed.txt

ONE PROCESS.

Coding discipline: no compound one-liner statements.

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

No operator token appears in this file.  The z3 constructor names
below (`Or`, `And`, `Concat`, ...) are the SOLVER's own function
names read off `z3.Z3_OP_*` declaration kinds, not any language's
grammar operator, and nothing here is keyed on a unit's spelling.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

LINES = []

# The z3 declaration kinds whose arguments may be reordered without
# changing the value.  Each is commutative AND associative in the
# solver's own semantics, so a fixed order over the argument list is a
# printing choice, never a semantic one.
COMMUTATIVE = set([
    z3.Z3_OP_AND,
    z3.Z3_OP_OR,
    z3.Z3_OP_XOR,
    z3.Z3_OP_EQ,
    z3.Z3_OP_DISTINCT,
    z3.Z3_OP_ADD,
    z3.Z3_OP_MUL,
    z3.Z3_OP_BADD,
    z3.Z3_OP_BMUL,
    z3.Z3_OP_BAND,
    z3.Z3_OP_BOR,
    z3.Z3_OP_BXOR,
])

PROVED = "WRAPPED_TEXT_PROVED"


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def order_commutative(node):
    """the further printing step, applied bottom-up: rebuild the term
    with the arguments of a commutative operator sorted by their own
    printed text.

    It is a PRINTING rule and it is total: a node that is not an
    application, or whose operator is not in the table above, is
    rebuilt from its ordered arguments unchanged."""
    if not z3.is_app(node):
        return node
    rebuilt = []
    for index in range(node.num_args()):
        rebuilt.append(order_commutative(node.arg(index)))
    kind = node.decl().kind()
    if kind in COMMUTATIVE:
        if len(rebuilt) > 1:
            rebuilt = sorted(rebuilt, key=lambda one: str(one))
    if not rebuilt:
        return node
    return node.decl()(*rebuilt)


def normalize_as_ruled(maker, term):
    return maker.normalize(term)


def normalize_with_the_step(maker, term):
    """the rule as it stands, with the further step applied to the
    simplified term before it is printed."""
    simplified = z3.simplify(term)
    symbols = T.ordered_symbols(simplified)
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
    simplified = order_commutative(simplified)
    return T.one_line(simplified)


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE,
                                "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    pattern = os.path.join(HERE, "canon39_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def callee_units():
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        name = unit.get("callee")
        if toolchain is None:
            toolchain = key.split("/", 1)[0]
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def proved_units():
    """unit -> True, for the units this round's gate of record PROVED.
    Read off `term65_store`, which already holds the verdicts."""
    out = set()
    pattern = os.path.join(HERE, "term65_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            if document["units"][name].get("proved"):
                out.add(name)
    return out


def main():
    proved = proved_units()
    log("-- the population")
    log("   units with a proved term %d" % len(proved))
    attached = callee_units()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    as_ruled = {}
    with_step = {}
    refused = 0
    walked = 0
    for path in shards():
        document = json.load(open(path))
        for name in sorted(document.get("units", {}).items()):
            pass
        for name in sorted(document.get("units", {})):
            unit = document["units"][name]
            if unit.get("outcome") != PROVED:
                continue
            if name not in proved:
                continue
            unit = dict(unit)
            unit["unit"] = name
            transcription = maker.transcribe(unit)
            if transcription.out_term is None:
                refused = refused + 1
                continue
            try:
                a = normalize_as_ruled(maker, transcription.out_term)
                b = normalize_with_the_step(maker,
                                            transcription.out_term)
            except Exception:
                refused = refused + 1
                continue
            as_ruled[name] = a
            with_step[name] = b
            walked = walked + 1
    log("   units walked %d, refused %d" % (walked, refused))

    texts_a = set(as_ruled.values())
    texts_b = set(with_step.values())
    log("")
    log("-- DISTINCT LAYER-5 TEXTS, the rule as it stands beside the "
        "rule with the step")
    log("   as ruled (simplify, rename, print)        %d"
        % len(texts_a))
    log("   with the arguments of a commutative       %d"
        % len(texts_b))
    log("     operator sorted by their printed text")
    log("   texts the step collapses                  %d"
        % (len(texts_a) - len(texts_b)))

    moved = []
    for name in sorted(as_ruled):
        if as_ruled[name] != with_step[name]:
            moved.append(name)
    log("   units whose printed text the step changes %d" % len(moved))

    log("")
    log("-- THE INSTANCE, printed")
    if moved:
        one = moved[0]
        log("   unit %s" % one)
        log("   as ruled : %s" % as_ruled[one])
        log("   with step: %s" % with_step[one])

    document = {
        "meta": {
            "generated_by": "normalize_order_probe65.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "a MEASUREMENT of how many distinct layer-5 "
                          "texts collapse when the arguments of a "
                          "commutative operator are sorted by their "
                          "own printed text; it changes nothing",
            "why": "nine pool4 -> pool5 splits contain no member that "
                   "lost its layer-5 key, and their members' texts "
                   "differ only in the argument order of one "
                   "commutative operator",
        },
        "units_walked": walked,
        "units_refused": refused,
        "distinct_texts_as_ruled": len(texts_a),
        "distinct_texts_with_the_step": len(texts_b),
        "texts_the_step_collapses": len(texts_a) - len(texts_b),
        "units_whose_text_the_step_changes": len(moved),
        "units_changed": moved[:200],
    }
    handle = open(os.path.join(HERE,
                               "normalize_order_probe65.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        HERE, "normalize_order_probe65_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote normalize_order_probe65.json and "
        "normalize_order_probe65_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
