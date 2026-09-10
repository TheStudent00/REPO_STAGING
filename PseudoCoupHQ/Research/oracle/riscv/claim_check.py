#!/usr/bin/env python3
"""claim_check.py -- THE COMPILER'S CROSS-TARGET CLAIM, MEASURED.

Node: hq.research.arch_unit_oracle.  Task rv1, brief section 4.

THE CLAIM, in one sentence: a source unit compiled for two architectures
should compute the same mapping, so the term read off its riscv64 body and
the term read off its x86-64 body should be the same function of the same
arriving values.

HOW THE TWO TERMS ARE PUT IN ONE PLACE, and it is the only place the two
architectures meet:

  * the ARGUMENTS.  Each language's calling rule names a place per
    argument, per KIND.  The k-th integer argument of a c function is in
    `rdi, rsi, rdx, rcx, r8, r9` on x86-64 and in `a0 .. a7` on riscv64;
    the k-th floating-point argument is in `xmm0 .. xmm7` and in
    `fa0 .. fa7`.  Go's own register rule names `rax, rbx, rcx, rdi, rsi,
    ...` on x86-64 and `a0 .. a7` on riscv64.  This file binds the k-th
    argument of a kind to ONE shared z3 symbol on both sides, so the two
    terms are functions of the same unknowns and z3 can be asked whether
    they are equal.
  * an x86 arrival family that is NOT an argument -- a register the body
    reads before writing because the instruction it uses writes only part
    of it -- gets its own free symbol on the x86 side and has no
    counterpart on the riscv64 side.  That is not an error to paper over:
    it is one of the differences this task is here to name.
  * the ANSWER.  The comparison is at THE UNIT'S OWN ANSWER WIDTH, which
    the term store records (`result_width`), read out of `rax` / `xmm0` on
    one side and out of `a0` / `fa0` on the other.

WHERE THE x86 TERM COMES FROM, said plainly: it is RE-DERIVED here by
walking the unit's own recorded ship body with the pipeline's own
`op_pipeline/reference.py`, because the term store holds the term as TEXT
and this line has no reader that turns that text back into a z3 object.
The store's recorded text is printed beside the re-derivation and the two
are compared AS TEXT after `term.Term.normalize`, so the re-derivation is
shown to be the stored term and not a second reading of the unit.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

The pairing here is ONE UNIT WITH ITSELF ON A SECOND ARCHITECTURE.  Nothing
is grouped by an operator token; the candidate set is the ten rows the
model table's attestation gave.

usage:
  claim_check.py <op_pipeline dir> <units.json> <carved.json> <out prefix>
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import z3                                                   # noqa: E402


SOLVER_TIMEOUT_MS = 3000

# The calling rules, per language, per kind, in argument order.  Each is a
# fact of the published application binary interface, stated here once.
X86_INTEGER = {
    "c": ["rdi", "rsi", "rdx", "rcx", "r8", "r9"],
    "go": ["rax", "rbx", "rcx", "rdi", "rsi", "r8", "r9", "r10", "r11"],
}
X86_FLOAT = {
    "c": ["xmm%d" % i for i in range(8)],
    "go": ["xmm%d" % i for i in range(15)],
}
RISCV_INTEGER = {
    "c": ["a%d" % i for i in range(8)],
    "go": ["a%d" % i for i in range(8)],
}
RISCV_FLOAT = {
    "c": ["fa%d" % i for i in range(8)],
    "go": ["fa%d" % i for i in range(8)],
}

FLOAT_TYPES = frozenset(["float", "double", "float32", "float64",
                         "long double"])


def kind_of(type_name):
    if type_name is None:
        return None
    if type_name in FLOAT_TYPES:
        return "float"
    return "integer"


def argument_places(row):
    """[(kind, x86 family, riscv register)] in argument order."""
    lang = row["lang"]
    kinds = []
    for name in (row.get("lhs_type"), row.get("rhs_type")):
        kind = kind_of(name)
        if kind is not None:
            kinds.append(kind)
    integers = 0
    floats = 0
    out = []
    for kind in kinds:
        if kind == "float":
            out.append((kind, X86_FLOAT[lang][floats],
                        RISCV_FLOAT[lang][floats]))
            floats = floats + 1
            continue
        out.append((kind, X86_INTEGER[lang][integers],
                    RISCV_INTEGER[lang][integers]))
        integers = integers + 1
    return out


def x86_term(reference, term_node, row, places):
    """(the term, the shared symbols, the extra arrivals) for the unit's
    own x86 ship body."""
    shared = {}
    symbols = {}
    for index, (kind, family, _register) in enumerate(places):
        width = 128 if family.startswith("xmm") else 64
        symbol = z3.BitVec("arg%d" % index, width)
        shared[family] = symbol
        symbols[family] = symbol
    state = reference.simulate(row["x86_ship_body"], None, shared)
    home = {"result_family": row["x86_result_family"],
            "result_width": row["x86_result_width"]}
    answer = reference.answer_of(state, home)
    extra = []
    for family in (row.get("x86_arrival_families") or []):
        if family not in symbols:
            extra.append(family)
    return answer, symbols, extra


def riscv_term(reference, carved, row, places, symbols):
    """the term the carved riscv64 body leaves in its answer place, over
    the SAME symbols the x86 walk used."""
    contract = []
    for index, (kind, family, register) in enumerate(places):
        symbol = symbols[family]
        if kind == "float":
            if symbol.size() != 64:
                symbol = z3.Extract(63, 0, symbol)
            contract.append((register, symbol))
            continue
        contract.append((register, symbol))
    home = "a0"
    if str(row["x86_result_family"]).startswith("xmm"):
        home = "fa0"
    state = reference.simulate(carved["body"], contract, {})
    return reference.answer_of(state, home)


def at_width(term, width):
    if term.size() == width:
        return term
    if term.size() > width:
        return z3.Extract(width - 1, 0, term)
    return z3.ZeroExt(width - term.size(), term)


def decide(left, right):
    """(outcome, counterexample) for `left == right` on every input."""
    solver = z3.Solver()
    solver.set("timeout", SOLVER_TIMEOUT_MS)
    solver.add(left != right)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "EQUAL_BY_Z3", None
    if verdict == z3.unknown:
        return "UNDECIDED", None
    model = solver.model()
    shown = {}
    for declaration in model.decls():
        shown[declaration.name()] = str(model[declaration])
    return "DIFFER", shown


def main():
    op_dir = sys.argv[1]
    units_path = sys.argv[2]
    carved_path = sys.argv[3]
    out_prefix = sys.argv[4]

    sys.path.insert(0, op_dir)
    import reference as X86                                 # noqa: E402
    import term as TERMS                                    # noqa: E402

    x86_reference = X86.Reference()
    rv_reference = RV.RiscvReference()
    normaliser = TERMS.Term(x86_reference)

    units = {}
    order = []
    for row in json.load(open(units_path))["rows"]:
        if row.get("outcome") != "PICKED":
            order.append(row)
            continue
        units[row["unit"]] = row
        order.append(row)
    carved = {}
    for row in json.load(open(carved_path))["rows"]:
        carved[row["unit"]] = row

    rows = []
    total = len([r for r in order if r.get("outcome") == "PICKED"])
    seen = 0
    for row in order:
        if row.get("outcome") != "PICKED":
            rows.append({
                "mnem": row["mnem"], "shape": row["shape"],
                "key_width": row["key_width"], "unit": None,
                "outcome": "NO_CORPUS_UNIT", "why": row["why"],
            })
            continue
        seen = seen + 1
        print("[%d/%d] %s" % (seen, total, row["unit"]))
        sys.stdout.flush()
        record = {
            "mnem": row["mnem"], "shape": row["shape"],
            "key_width": row["key_width"], "unit": row["unit"],
            "lang": row["lang"], "operator": row.get("operator"),
            "expression": row.get("expression"),
            "x86_body": " ; ".join(row["x86_ship_body"]),
            "riscv_body": " ; ".join(carved[row["unit"]].get("body") or []),
            "x86_term_from_the_store": row.get("x86_term"),
            "answer_width": row.get("x86_result_width"),
        }
        places = argument_places(row)
        record["argument_places"] = [
            {"kind": k, "x86": f, "riscv": r} for k, f, r in places]
        try:
            left, symbols, extra = x86_term(x86_reference, TERMS, row,
                                            places)
        except Exception as exc:
            record["outcome"] = "X86_WALK_REFUSED"
            record["cause"] = "%s: %s" % (type(exc).__name__, exc)
            rows.append(record)
            print("      %s" % record["cause"])
            continue
        record["x86_arrivals_beyond_the_arguments"] = extra
        try:
            right = riscv_term(rv_reference, carved[row["unit"]], row,
                               places, symbols)
        except Exception as exc:
            record["outcome"] = "RISCV_WALK_REFUSED"
            record["cause"] = "%s: %s" % (type(exc).__name__, exc)
            rows.append(record)
            print("      %s" % record["cause"])
            continue
        width = row["x86_result_width"]
        left_cut = at_width(left, width)
        right_cut = at_width(right, width)
        try:
            record["x86_term_rederived"] = normaliser.normalize(left_cut)
        except Exception as exc:
            record["x86_term_rederived"] = "NORMALISE_REFUSED: %s" % exc
        try:
            record["riscv_term"] = normaliser.normalize(right_cut)
        except Exception as exc:
            record["riscv_term"] = "NORMALISE_REFUSED: %s" % exc
        record["identical_after_normalize"] = (
            record["x86_term_rederived"] == record["riscv_term"])
        record["rederivation_matches_the_store"] = (
            record["x86_term_rederived"] ==
            record["x86_term_from_the_store"])
        outcome, counterexample = decide(left_cut, right_cut)
        if record["identical_after_normalize"]:
            record["outcome"] = "IDENTICAL_AFTER_NORMALIZE"
        else:
            record["outcome"] = outcome
        record["z3_outcome"] = outcome
        record["counterexample"] = counterexample
        rows.append(record)
        print("      %-26s answer width %s" % (record["outcome"], width))
        print("      x86   : %s" % record["x86_term_rederived"])
        print("      riscv : %s" % record["riscv_term"])
        if counterexample:
            print("      counterexample: %s" % counterexample)
        sys.stdout.flush()

    doc = {
        "meta": {
            "task": "rv1",
            "what": "each unit's riscv64 term against its own x86-64 term, "
                    "per written place, at the unit's own answer width",
            "solver_timeout_ms": SOLVER_TIMEOUT_MS,
            "x86_term_note": "re-derived by walking the unit's recorded "
                             "ship body with op_pipeline/reference.py; the "
                             "term store's recorded text is on every row "
                             "as `x86_term_from_the_store`",
        },
        "rows": rows,
    }
    fh = open(out_prefix + ".json", "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    tally = {}
    for row in rows:
        tally[row["outcome"]] = tally.get(row["outcome"], 0) + 1
    print("outcomes: %s" % json.dumps(tally, sort_keys=True))


if __name__ == "__main__":
    main()
