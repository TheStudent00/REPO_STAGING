#!/usr/bin/env python3
"""ref2_condition_proof.py -- the reading of every condition after every
flag-setting arch opcode, BEFORE and AFTER task ref2's correction 3, asked of
z3 rather than argued.

WHAT THIS IS, in relation.  `reference.predicate_of` turns a condition suffix
(`e`, `ne`, `l`, `b`, ...) into a z3 Bool by reading the flag state the last
flag-setting opcode left.  Until 2026-09-10 it computed every condition on
`L - R`; it now reads Intel's own flags, each computed from the setter's own
arithmetic.  This program puts the two readings side by side, one row per
(flag-setting opcode, condition suffix, width), and asks z3 whether they can
differ.  `unsat` means the reading DID NOT MOVE; `sat` means it moved, and the
counterexample says where.

THE BRIEF'S OWN ACCEPTANCE CRITERION is in this table: the `sub` and `cmp`
rows must not move, and the `add` and `neg` rows must.

THE OLD READING IS NOT RE-TYPED HERE.  It is imported from
`level0/ref2_originals/reference.py`, which is `reference.py` byte for byte as
it stood before this task, so the "before" column is the old code running and
not a description of it.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Coding discipline: no compound one-liner statements.

usage:
  ref2_condition_proof.py <out.json>
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
for _path in (PIPELINE, os.path.join(PIPELINE, "lean")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import z3                                                   # noqa: E402
import reference as R                                       # noqa: E402


def load_the_old_reference():
    """`reference.py` as it stood before this task, imported under its
    own name so both readings are LIVE CODE in one process."""
    path = os.path.join(HERE, "ref2_originals", "reference.py")
    spec = importlib.util.spec_from_file_location(
        "reference_before_ref2", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["reference_before_ref2"] = module
    spec.loader.exec_module(module)
    return module


WIDTHS = (8, 16, 32, 64)

SUFFIXES = ("e", "ne", "l", "ge", "le", "g", "b", "ae", "a", "be",
            "s", "ns", "p", "np", "o", "no")
"""one spelling per condition, plus the two overflow readings, which
`condition_table.SUFFIX_TO_COND` does not tabulate and `predicate_of`
answers from the overflow bit."""


def flag_states(module, width, which):
    """the flag state that module's own builders leave for one setter,
    built the way the builder builds it.

    `which` is the machine-form name of the flag-setting arch opcode; it
    is the field this file's rows carry as `mnem`."""
    left = z3.BitVec("proof_L", width)
    right = z3.BitVec("proof_R", width)
    carry = z3.Bool("proof_C")
    zero = z3.BitVecVal(0, width)
    if which in ("add", "sub", "cmp"):
        return (which, left, right)
    if which in ("adc", "sbb"):
        # THE BEFORE AND THE AFTER ARE DIFFERENT OBJECTS HERE, and that
        # IS the correction: before it, `build_carry_binary` left a
        # plain three-tuple with the carry nowhere in it; after it, a
        # `FlagState` carrying the same carry the destination got.
        if not hasattr(module, "FlagState"):
            return (which, left, right)
        return module.FlagState(which, left, right, carry_in=carry)
    if which in ("and", "or", "xor", "test", "inc", "bsr"):
        return (which, left, zero)
    if which == "neg":
        return ("neg", left, zero)
    if which in ("imul", "mul"):
        return (which, left, right)
    if which == "bt":
        return ("bt", left, z3.BitVecVal(3, width))
    raise ValueError("no flag state is built for %r" % which)


SETTERS = ("add", "adc", "sub", "sbb", "cmp", "and", "or", "xor",
           "test", "inc", "neg", "bt", "bsr", "imul", "mul")


def read(module, which, width, suffix):
    """(the z3 Bool, the refusal sentence) for one reading."""
    state = module.MachineState()
    try:
        state.flags = flag_states(module, width, which)
    except Exception as problem:                            # noqa: BLE001
        return None, "%s: %s" % (type(problem).__name__, problem)
    try:
        return module.predicate_of(state, suffix), None
    except module.NotModeled as refusal:
        return None, str(refusal)
    except Exception as problem:                            # noqa: BLE001
        return None, "%s: %s" % (type(problem).__name__, problem)


def ask(before, after):
    """z3's verdict on whether two readings can differ."""
    solver = z3.Solver()
    solver.set("timeout", 10000)
    solver.add(before != after)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "unsat", None
    if verdict == z3.sat:
        model = solver.model()
        values = []
        for symbol in sorted(model.decls(), key=lambda d: d.name()):
            values.append({"symbol": symbol.name(),
                           "text": str(model[symbol])})
        return "sat", values
    return "unknown", None


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    old = load_the_old_reference()
    rows = []
    for which in SETTERS:
        for width in WIDTHS:
            for suffix in SUFFIXES:
                before, before_refusal = read(old, which, width, suffix)
                after, after_refusal = read(R, which, width, suffix)
                row = {"mnem": which, "key_width": width,
                       "suffix": suffix,
                       "before_refusal": before_refusal,
                       "after_refusal": after_refusal}
                if before is None or after is None:
                    if before_refusal == after_refusal:
                        row["verdict"] = "both refuse, same cause"
                    elif before is None and after is None:
                        row["verdict"] = "both refuse, different cause"
                    elif before is None:
                        row["verdict"] = "refused before, answers now"
                        row["after_text"] = str(z3.simplify(after))
                    else:
                        row["verdict"] = "answered before, refuses now"
                        row["before_text"] = str(z3.simplify(before))
                    rows.append(row)
                    continue
                verdict, model = ask(before, after)
                row["verdict"] = verdict
                row["counterexample"] = model
                if verdict != "unsat":
                    row["before_text"] = str(z3.simplify(before))
                    row["after_text"] = str(z3.simplify(after))
                rows.append(row)
    summary = {}
    for row in rows:
        entry = summary.setdefault(row["mnem"], {})
        entry[row["verdict"]] = entry.get(row["verdict"], 0) + 1
    out = {"what": ("every condition after every flag-setting arch "
                    "opcode, the reading before task ref2's correction "
                    "3 against the reading after it, decided by z3"),
           "widths": list(WIDTHS), "suffixes": list(SUFFIXES),
           "rows": rows,
           "summary": [{"mnem": m, "verdicts": summary[m]}
                       for m in sorted(summary)]}
    with open(argv[1], "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
    print("| `mnem` | rows | the reading did NOT move | it moved | "
          "both refuse | other |")
    print("|---|---|---|---|---|---|")
    for name in sorted(summary):
        counts = summary[name]
        total = sum(counts.values())
        same = counts.get("unsat", 0)
        moved = counts.get("sat", 0)
        refused = counts.get("both refuse, same cause", 0)
        other = total - same - moved - refused
        print("| `%s` | %d | %d | %d | %d | %d |"
              % (name, total, same, moved, refused, other))
    print("")
    print("every row whose reading moved, or whose refusal changed:")
    for row in rows:
        if row["verdict"] in ("unsat", "both refuse, same cause"):
            continue
        print("  %-5s width %2d suffix %-3s : %s"
              % (row["mnem"], row["key_width"], row["suffix"],
                 row["verdict"]))
        if row.get("before_text"):
            print("      before: %s" % row["before_text"][:150])
        if row.get("after_text"):
            print("      after : %s" % row["after_text"][:150])
        if row.get("before_refusal") and row["before_refusal"] != \
                row.get("after_refusal"):
            print("      before refusal: %s" % row["before_refusal"])
        if row.get("after_refusal") and row["after_refusal"] != \
                row.get("before_refusal"):
            print("      after refusal : %s" % row["after_refusal"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
