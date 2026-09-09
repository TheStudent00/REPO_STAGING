#!/usr/bin/env python3
"""normalize79_cause.py -- WHY ROUND 14'S REPAIR WAS NOT ENOUGH, and
what each missing piece was worth, measured on one shard.

THE MEASUREMENT.  The `c` shard's 582 proved units are walked twice in
ONE process -- once in name order, once in the reverse -- under four
printing rules.  A rule whose text is a function of the unit prints the
same text in both walks; the count of units that differ is what each
rule is worth.

    as_ruled_before_task79   simplify, rename, print: the rule as
                             log_147 section 8.1 numbered it
    order_without_parameters the ordering step with an argument key
                             that leaves the operator's PARAMETERS out,
                             so two reads of different bit ranges tie
    order_without_the_float_operators
                             the ordering step whose table of
                             commutative operators holds the bit-vector
                             and boolean ones only -- round 14's table
    the_corrected_rule       `term.Term.normalize` as it now stands

The reversed walk is the cheap form of the acceptance test: it changes
what the process built earlier without needing a second process.  The
acceptance test itself is `acceptance79.py`, three separate processes
over the whole population.

MEMORY BOUND: one shard held at a time; expected peak resident size
under 500 MB; hard cap 6 GB with the named abort ABORT_MEMORY_CEILING.

WRITES:
  normalize79_cause.json
  normalize79_cause_printed.txt

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

The four rules named here are PRINTING rules, never operator tokens.
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

LINES = []
PROVED = "WRAPPED_TEXT_PROVED"
MEMORY_CEILING_MB = 6144


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_resident_mb():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return used / 1024.0


def rename_positionally(simplified):
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
    return simplified


def as_ruled_before_task79(term):
    """simplify, rename, print -- the rule as it stood."""
    simplified = z3.simplify(term)
    simplified = rename_positionally(simplified)
    simplified = z3.simplify(simplified)
    return T.one_line(simplified)


def ordered_with(term, use_parameters, use_float_operators):
    """the corrected rule with one piece removed, so the piece can be
    priced.  The walk is `term.ordering_key`'s own walk, re-run here
    with the key built the narrower way."""
    simplified = z3.simplify(term)
    simplified = order_narrowly(simplified, use_parameters,
                               use_float_operators)
    simplified = rename_positionally(simplified)
    simplified = z3.simplify(simplified)
    simplified = order_narrowly(simplified, use_parameters,
                               use_float_operators)
    return T.one_line(simplified)


def order_narrowly(term, use_parameters, use_float_operators):
    cache = {}
    stack = [(term, False)]
    while stack:
        current, expanded = stack.pop()
        key = current.get_id()
        if key in cache:
            continue
        if not z3.is_app(current):
            spelled = str(current)
            cache[key] = (current, spelled, spelled)
            continue
        if not expanded:
            stack.append((current, True))
            for index in range(current.num_args()):
                stack.append((current.arg(index), False))
            continue
        cache[key] = narrow_node(current, cache, use_parameters,
                                 use_float_operators)
    return cache[term.get_id()][0]


def narrow_node(current, cache, use_parameters, use_float_operators):
    declaration = current.decl()
    kind = declaration.kind()
    if use_parameters:
        name = T.operator_name(current)
    else:
        name = declaration.name()
    sort_text = current.sort().sexpr()
    if current.num_args() == 0:
        if kind == z3.Z3_OP_UNINTERPRETED:
            shape = "?" + sort_text
        else:
            shape = name + ":" + sort_text
        concrete = name + ":" + sort_text
        return (current, shape, concrete)
    pieces = []
    for index in range(current.num_args()):
        pieces.append(cache[current.arg(index).get_id()])
    if kind in T.COMMUTATIVE_OPERATORS:
        if kind == z3.Z3_OP_FPA_EQ and not use_float_operators:
            pieces = pieces
        elif len(pieces) > 1:
            pieces = sorted(pieces, key=T.argument_order)
    elif kind in T.ROUNDED_COMMUTATIVE_OPERATORS:
        if use_float_operators and len(pieces) > 2:
            head = pieces[:1]
            rest = sorted(pieces[1:], key=T.argument_order)
            pieces = head + rest
    arguments = []
    shapes = []
    concretes = []
    for piece in pieces:
        arguments.append(piece[0])
        shapes.append(piece[1])
        concretes.append(piece[2])
    rebuilt = declaration(*arguments)
    shape = "(%s %s)" % (name, " ".join(shapes))
    concrete = "(%s %s)" % (name, " ".join(concretes))
    return (rebuilt, shape, concrete)


def order_without_parameters(term):
    return ordered_with(term, False, True)


def order_without_the_float_operators(term):
    return ordered_with(term, True, False)


def the_corrected_rule(term):
    return T.TERM.normalize(term)


def callee_units():
    path = os.path.join(HERE, "canon39_callee_units.json")
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
    import glob
    out = set()
    pattern = os.path.join(HERE, "term65_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            if document["units"][name].get("proved"):
                out.add(name)
    return out


def walk(names, units, attached, printing_rule):
    maker = T.Term(reference=R.Reference(runtime_units=attached),
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    out = {}
    for name in names:
        unit = dict(units[name])
        unit["unit"] = name
        transcription = maker.transcribe(unit)
        if transcription.out_term is None:
            continue
        try:
            out[name] = printing_rule(transcription.out_term)
        except Exception as problem:
            out[name] = "REFUSED: %s: %s" % (type(problem).__name__,
                                             problem)
        if peak_resident_mb() > MEMORY_CEILING_MB:
            log("ABORT_MEMORY_CEILING: %.0f MB over the %d MB cap"
                % (peak_resident_mb(), MEMORY_CEILING_MB))
            raise SystemExit(3)
    return out


def main():
    proved = proved_units()
    attached = callee_units()
    document = json.load(open(os.path.join(HERE,
                                           "canon39_wrapped_c.json")))
    units = {}
    for name in document.get("units", {}):
        if document["units"][name].get("outcome") != PROVED:
            continue
        if name in proved:
            units[name] = document["units"][name]
    names = sorted(units)
    log("-- THE SHARD")
    log("   the `c` shard's units with a proved term %d" % len(names))
    log("")
    log("-- EACH PRINTING RULE, WALKED FORWARD AND REVERSED IN ONE "
        "PROCESS")

    rules = [
        ("as_ruled_before_task79", as_ruled_before_task79),
        ("order_without_parameters", order_without_parameters),
        ("order_without_the_float_operators",
         order_without_the_float_operators),
        ("the_corrected_rule", the_corrected_rule),
    ]
    rows = {}
    for label, printing_rule in rules:
        forward = walk(names, units, attached, printing_rule)
        backward = walk(list(reversed(names)), units, attached,
                        printing_rule)
        differ = []
        for name in sorted(forward):
            if forward[name] != backward.get(name):
                differ.append(name)
        rows[label] = {
            "units_walked": len(forward),
            "units_whose_text_differs_between_the_two_walks":
                len(differ),
            "distinct_texts_forward": len(set(forward.values())),
            "first_unit_that_differs": (differ + [None])[0],
        }
        log("   %-34s differs %3d of %3d   distinct %3d"
            % (label, len(differ), len(forward),
               len(set(forward.values()))))
        if differ:
            one = differ[0]
            log("       %s" % one)
            log("         forward : %s" % forward[one][:200])
            log("         reversed: %s" % backward[one][:200])

    log("")
    log("   peak resident size %.0f MB, cap %d MB"
        % (peak_resident_mb(), MEMORY_CEILING_MB))

    out = {
        "meta": {
            "generated_by": "normalize79_cause.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "what each piece of the corrected printing "
                          "rule is worth, measured by walking one "
                          "shard forward and reversed in one process",
            "shard": "canon39_wrapped_c.json",
            "memory_bound_mb": MEMORY_CEILING_MB,
            "peak_resident_mb": round(peak_resident_mb(), 1),
        },
        "units": len(names),
        "rules": rows,
    }
    handle = open(os.path.join(HERE, "normalize79_cause.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE,
                               "normalize79_cause_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("-- wrote normalize79_cause.json and "
        "normalize79_cause_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
