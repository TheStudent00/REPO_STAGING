#!/usr/bin/env python3
"""probe_gen3.py -- the CORRECTED swift probe emitter.  It supersedes
`probe_gen.py :: emit_swift` and changes nothing else.

probe_gen.py is NOT edited.  This file imports it and replaces one
function; every other emitter, the operator inventory, the result-type
rules, the constant ban and the acceptance-is-the-compiler's rule are
probe_gen.py's, imported rather than copied, so the two cannot drift.
probe_gen2.py (the regeneration's candidate builder) does the same
thing for a different reason, and this file follows its shape.

WHAT WAS WRONG (finding F45-4, log 137; the call in log 140 s4)
---------------------------------------------------------------
LITERAL -- probe_gen.py lines 361 and 369:

    C_REPRESENTABLE = {"Int32", "Int64", "UInt64", "Float", "Double",
                       "Bool"}
    ...
    cdecl = res in C_REPRESENTABLE

GLOSS -- `@_cdecl("op_N")` asks swiftc to export the function under a C
calling convention and a fixed symbol name; the probe pipeline wants
that, because `op_N` is the symbol every later stage looks the unit up
by.  The test above asks only about `res`, the RESULT type.  It never
looks at the parameters.  A function whose result is `Int64` but whose
second parameter is `Int128` therefore gets the attribute, and swiftc
refuses the whole function.  276 refusals in the regeneration, one
cause, no legality content.

THE FIX, IN TWO PARTS
---------------------
1. THE TEST COVERS EVERY POSITION.  The attribute is attached only when
   the result type AND every parameter type is C-representable.
2. THE ANSWER COMES FROM MEASUREMENT, NOT FROM A HAND LIST.  The set is
   read from `swift_cdecl_witness1.json`, which is the compiler's own
   verdict on each type in each of the two positions, measured by
   `swift_cdecl_witness1.py` in the Airlock `trickle` instance.  There
   is no set of spellings written in this file.

A CONSEQUENCE THAT WAS NOT PREDICTED, RECORDED RATHER THAN HIDDEN
-----------------------------------------------------------------
The measurement disagrees with the hand list in BOTH directions.  The
hand list named six spellings; swiftc accepts fifteen of the
inventory's seventeen in both positions, refusing only `Int128` and
`UInt128`.  So the corrected emitter also ATTACHES the attribute to
probes the old emitter left unexported (result `Int8`, `Float16`, and
so on).  `task50a_diff1.py` counts both directions separately; neither
is folded into the other.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim.

The decision this file makes reads TYPES only.  The operator token
rides through untouched, into the probe's `operator` display field and
into the source text of the expression, exactly as probe_gen.py already
carries it.

usage (as a library):
    import probe_gen3
    src, cdecl = probe_gen3.emit_swift(n, op, arity, pos, lt, rt, res)
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import probe_gen                                           # noqa: E402

WITNESS = os.path.join(HERE, "swift_cdecl_witness1.json")

_CACHE = {}


def representable_sets():
    """(parameter_ok, result_ok) -- the spellings swiftc accepted in
    each position, read from the measurement.  Refuses if the witness
    file is not there; there is no fallback list to fall back to."""
    if "sets" in _CACHE:
        return _CACHE["sets"]
    if not os.path.isfile(WITNESS):
        raise SystemExit(
            "REFUSE: no C-representability measurement at %s.\n"
            "        run swift_cdecl_witness1.py --run first; this "
            "emitter has no hand list to fall back to." % WITNESS)
    doc = json.load(open(WITNESS))
    parameter_ok = set()
    result_ok = set()
    for entry in doc["types"]:
        measured = entry["c_representable"]
        if measured["parameter_form"]["verdict"] == "ACCEPT":
            parameter_ok.add(entry["spelling"])
        if measured["result_form"]["verdict"] == "ACCEPT":
            result_ok.add(entry["spelling"])
    _CACHE["sets"] = (parameter_ok, result_ok)
    return _CACHE["sets"]


def cdecl_allowed(lt, rt, res):
    """The corrected test: the result AND every parameter.

    A type the measurement never saw is treated as NOT representable,
    which is the refusing direction: an unmeasured type cannot license
    an attribute.
    """
    parameter_ok, result_ok = representable_sets()
    if res not in result_ok:
        return False
    if lt not in parameter_ok:
        return False
    if rt is not None and rt not in parameter_ok:
        return False
    return True


def emit_swift(n, op, arity, pos, lt, rt, res):
    """probe_gen.py :: emit_swift with the corrected attribute test.

    The source text is byte-for-byte probe_gen.py's apart from the
    presence or absence of the `@_cdecl("op_N")` line, so a probe whose
    verdict is unchanged has unchanged text.
    """
    params = "_ a: %s" % lt
    if arity == "binary":
        params = "_ a: %s, _ b: %s" % (lt, rt)
    body = probe_gen.expression(op, arity, pos)
    cdecl = cdecl_allowed(lt, rt if arity == "binary" else None, res)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    if cdecl:
        lines.append('@_cdecl("op_%d")' % n)
    lines.append("public func op_%d(%s) -> %s {" % (n, params, res))
    lines.append("    return %s" % body)
    lines.append("}")
    return "\n".join(lines) + "\n", cdecl


if __name__ == "__main__":
    parameter_ok, result_ok = representable_sets()
    print("measurement read from %s" % os.path.basename(WITNESS))
    print("  accepted in a parameter position: %d types" % len(parameter_ok))
    print("  accepted in a result position:    %d types" % len(result_ok))
    print("  the old hand list held %d spellings"
          % len(probe_gen.C_REPRESENTABLE))
