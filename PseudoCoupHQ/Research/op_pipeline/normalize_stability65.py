#!/usr/bin/env python3
"""normalize_stability65.py -- A MEASUREMENT of one defect, over the
whole population.  It changes nothing.

THE DEFECT, stated before the figure.  The normalize CORE's definition
says the rule exists "so that two units computing the same thing print
the same string".  Two runs of THAT RULE, over the SAME unit, in the
same code, do not always print the same string.

LITERAL -- `c/op_105`, the text `term65_store` holds and the text a
second walk of the same unit produced:

    term65_store: Concat(Extract(63, 32, v1),
                    fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) +
                      fpToFP(fp.to_ieee_bv(fpToFP(RNE(),
                        Extract(31, 0, v0))))))
    fresh run   : Concat(Extract(63, 32, v1),
                    fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(),
                      Extract(31, 0, v0)))) +
                        fpToFP(Extract(31, 0, v1))))

The two are the same value: the two arguments of one `+` are in the
other order.  The cause is that `z3.simplify` orders the arguments of
a commutative operator by the solver's internal node identity, and
that identity depends on WHAT THE PROCESS BUILT BEFORE -- so the text
a unit prints is a function of the unit AND of the walk order, not of
the unit alone.

WHY THIS MATTERS BEYOND THE TEXT.  The renaming step is
`v0`, `v1`, ... in FIRST-MET order, so when the argument order moves,
the first symbol met moves with it and the numbering swaps.  LITERAL --
`c/op_121`, the same two runs:

    term65_store: Concat(Extract(63, 32, v0), ... v1 ...)
    fresh run   : Concat(Extract(63, 32, v1), ... v0 ...)

WHAT THIS FILE MEASURES: over every unit with a proved term, how many
print a different text on a second walk, and how many distinct texts
each of the two walks produced.

WHAT IT DOES NOT DO: it does not change `term.py`, and the ruled rule
is not edited on the strength of it.  A partial repair was tried and
measured (`normalize_order_probe65.py`, plus a check that sorted the
arguments BEFORE the renaming): sorting the arguments of a commutative
operator collapses 299 of 1,292 texts, and still leaves 39 of 582
units on the `c` shard printing differently when the walk order is
reversed.  A repair that does not make the key a function of the unit
is not the repair, so the correction goes into the CORE as PLANNED and
the round's figures are reported as measured, with this defect named
on them.

WRITES:
  normalize_stability65.json
  normalize_stability65_printed.txt

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

No operator token appears in this file.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

LINES = []

PROVED = "WRAPPED_TEXT_PROVED"


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


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


def stored():
    """unit -> the layer-5 text term65_run wrote, for proved units."""
    out = {}
    pattern = os.path.join(HERE, "term65_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            record = document["units"][name]
            if not record.get("proved"):
                continue
            text = record.get("layer5_normalized_text")
            if text is None:
                continue
            out[name] = text
    return out


def main():
    was = stored()
    log("-- the population")
    log("   units with a proved term and a stored layer-5 text %d"
        % len(was))
    attached = callee_units()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    fresh = {}
    for path in shards():
        document = json.load(open(path))
        for name in sorted(document.get("units", {})):
            if name not in was:
                continue
            unit = document["units"][name]
            if unit.get("outcome") != PROVED:
                continue
            unit = dict(unit)
            unit["unit"] = name
            transcription = maker.transcribe(unit)
            if transcription.out_term is None:
                continue
            try:
                fresh[name] = maker.normalize(transcription.out_term)
            except Exception:
                continue
    log("   units walked a second time %d" % len(fresh))

    differ = []
    for name in sorted(fresh):
        if fresh[name] != was[name]:
            differ.append(name)
    by_language = {}
    for name in differ:
        language = name.split("/", 1)[0]
        by_language[language] = by_language.get(language, 0) + 1

    log("")
    log("-- THE INSTABILITY, over the whole population")
    log("   units whose text DIFFERS between the two walks   %d"
        % len(differ))
    log("   as a share of the units walked                   %.1f%%"
        % (100.0 * len(differ) / max(1, len(fresh))))
    log("   distinct texts, first walk (term65_store)        %d"
        % len(set(was[name] for name in fresh)))
    log("   distinct texts, second walk                      %d"
        % len(set(fresh.values())))
    log("")
    log("   by language")
    for language in sorted(by_language):
        log("       %-10s %6d" % (language, by_language[language]))

    log("")
    log("-- THE INSTANCE, printed")
    if differ:
        one = differ[0]
        log("   unit %s" % one)
        log("   first walk : %s" % was[one])
        log("   second walk: %s" % fresh[one])

    document = {
        "meta": {
            "generated_by": "normalize_stability65.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "how many units print a DIFFERENT layer-5 "
                          "text on a second walk of the same rule over "
                          "the same unit",
            "cause": "z3.simplify orders the arguments of a "
                     "commutative operator by the solver's internal "
                     "node identity, which depends on what the process "
                     "built before, so the printed text is a function "
                     "of the unit AND the walk order; the positional "
                     "renaming then follows the moved order and the "
                     "numbering swaps with it",
            "status": "FINDING.  The repair is written into the "
                      "normalize CORE as a settled correction and "
                      "planned for round 14; the ruled rule is NOT "
                      "edited on a partial fix",
        },
        "units_walked": len(fresh),
        "units_whose_text_differs": len(differ),
        "distinct_texts_first_walk": len(set(was[name]
                                             for name in fresh)),
        "distinct_texts_second_walk": len(set(fresh.values())),
        "by_language": by_language,
        "units_that_differ": differ[:400],
    }
    handle = open(os.path.join(HERE,
                               "normalize_stability65.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        HERE, "normalize_stability65_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote normalize_stability65.json and "
        "normalize_stability65_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
