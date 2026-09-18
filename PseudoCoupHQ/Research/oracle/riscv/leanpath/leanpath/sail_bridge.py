#!/usr/bin/env python3
"""sail_bridge.py -- the bridge from Sail's comparisons to BitVec's, GENERATED
from Sail's own Prelude rather than typed.

THE GAP, measured twice. Sail's Lean backend defines every comparison over
`Int`:

    def zopz0zI_u (x y : BitVec k_n) : Bool :=
      ((BitVec.toNatInt x) <b (BitVec.toNatInt y))

`<b` is `Int.blt`, and `bv_decide` cannot bitblast it: it abstracts the whole
comparison as an opaque variable and answers with a spurious counterexample.
`BitVec.ult` is the SAME PREDICATE and is inside its fragment. Sail ships no
lemma between them -- `@[simp_sail]` marks the definitions so they UNFOLD,
which is what produces the Int spelling in the first place, and a grep for
`ult` or `blt` across the whole Sail Lean library returns nothing.

Lane lp3_l104 measured that no library lemma closes it: all fourteen
candidates elaborate, none reaches it, and dropping Sail's comparison from the
simp set makes the opaque atom BIGGER. Lane lp3_l105 then sized the cost --
35 of 186 classes UNDECIDED, 86 arch-units, concentrated on narrow integer
comparisons.

WHY THIS FILE GENERATES RATHER THAN TYPES. `Bridges.lean` was hand-written and
broke on a Lean minor version within hours; agreement is not derivation. So
the lemma statements here are READ OUT OF THE PRELUDE: this file parses each
`def zopz0z...` , reads which conversion it uses (`toInt` -> signed,
`toNatInt` -> unsigned) and which comparison (`<b`, `>b`, `<=b`, `>=b`), and
writes the matching BitVec spelling. A definition whose shape it does not
recognise is REPORTED AND SKIPPED, never guessed at -- so the day Sail changes
one, this says so instead of silently emitting a false lemma.

The PROOF is not guessed either: each lemma is emitted with a `first | ... `
of candidate tactics, and the lane that elaborates it reports which one
carried, so what lands in the simp set is what Lean actually accepted.

THE HEADER IS NOT WRITTEN HERE. Sail's definitions live inside the module's
own namespace under a stack of opens, so a file that merely imports the
module cannot see `zopz0zI_u` -- measured in lane lp3_l106, where all eight
lemmas failed with "Function expected at zopz0zI_s" while every `#check` of
a BitVec name passed. The header and closers come from
`leanpath.strip.header_of`, the same function the gate's own files use, so
this file cannot drift away from them.

    python3 -m leanpath.sail_bridge <proof project> <module> <out.lean> [matrix]
"""

import json
import os
import re
import sys

# The SECOND family, found by lane lp3_l109's residuals. With the comparison
# bridged, what `bv_decide` still abstracted was the wrapper around it --
# Sail's Bool-to-bit conversion, which unfolds to a `match` it cannot see
# through:
#
#     def bool_bit_forwards (arg_ : Bool) : (BitVec 1) :=
#       match arg_ with | true => 1#1 | false => 0#1
#
# `BitVec.ofBool` IS that function, natively, inside the fragment, and the
# identity holds by `rfl` (checked on this toolchain before this was written).
# Same shape of gap, same shape of fix, same rule: the definition leaves the
# simp set with the lemma.
DEF_BOOL = re.compile(
    r"^def\s+(\w+)\s*\(\s*(\w+)\s*:\s*Bool\s*\)\s*:\s*\(?BitVec\s+1\)?\s*:=\s*\n"
    r"((?:\s+.+\n)+?)(?=\s*$|\ndef |\n/--)",
    re.M)


DEF = re.compile(
    r"^def\s+(zopz0z\w+)\s*\(x\s*:\s*\(?BitVec\s+(\w+)\)?\)\s*"
    r"\(y\s*:\s*\(?BitVec\s+\w+\)?\)\s*:\s*Bool\s*:=\s*\n\s*(.+)$",
    re.M)

# what the body may say, and the BitVec predicate that IS it.  The right-hand
# side is a spelling, never a claim: the lane proves each one or drops it.
CONVERSION = {"BitVec.toInt": "signed", "BitVec.toNatInt": "unsigned"}
COMPARISON = {"<b": "lt", ">b": "gt", "≤b": "le", "≥b": "ge",
              "<=b": "le", ">=b": "ge"}
# (family, comparison) -> (BitVec function, operands swapped?)
TARGET = {
    ("unsigned", "lt"): ("BitVec.ult", False),
    ("unsigned", "gt"): ("BitVec.ult", True),
    ("unsigned", "le"): ("BitVec.ule", False),
    ("unsigned", "ge"): ("BitVec.ule", True),
    ("signed", "lt"): ("BitVec.slt", False),
    ("signed", "gt"): ("BitVec.slt", True),
    ("signed", "le"): ("BitVec.sle", False),
    ("signed", "ge"): ("BitVec.sle", True),
}

# Tried in order; the first that carries is the proof.  None is privileged --
# `rfl` is first only because when it holds the lemma is definitional and
# nothing else need be believed.
TACTICS = [
    "rfl",
    "simp [%(def)s, %(conv)s, %(target)s]",
    "simp [%(def)s, %(conv)s, %(target)s, Int.ofNat_lt, Int.ofNat_le]",
    "unfold %(def)s %(conv)s %(target)s <;> simp <;> omega",
    "decide +kernel",
]


def read_bool_defs(text):
    """[(name, binder, body)] for every Bool -> BitVec 1 definition.

    Both the `match` form and a definition that merely calls one are taken:
    `bool_to_bit x := bool_bit_forwards x` is the same function and needs the
    same lemma, or unfolding it just reaches the `match` again."""
    out = []
    for m in DEF_BOOL.finditer(text):
        body = " ".join(m.group(3).split())
        out.append((m.group(1), m.group(2), body))
    return out


def bool_lemma_for(name, binder, body):
    """The Bool-to-bit bridge for one definition, or (None, why)."""
    looks_right = ("true => 1#1" in body and "false => 0#1" in body)
    calls_one = re.match(r"^\(?\w+ %s\)?$" % re.escape(binder), body)
    if not (looks_right or calls_one):
        return None, "body is neither the 1#1/0#1 match nor a call: %s" % body[:60]
    fill = {"def": name, "conv": name, "target": "BitVec.ofBool"}
    statement = "    %s %s = BitVec.ofBool %s := by" % (name, binder, binder)
    head = "(%s : Bool)" % binder
    if MATRIX:
        lines = []
        for index, tactic in enumerate(TACTICS):
            lines += ["theorem sail_bridge_%s_t%d %s :" % (name, index, head),
                      statement, "  %s" % (tactic % fill), ""]
        lines.pop()
    else:
        lines = ["theorem sail_bridge_%s %s :" % (name, head), statement,
                 "  first"]
        for tactic in TACTICS:
            lines.append("    | %s" % (tactic % fill))
    return ("\n".join(lines),
            {"definition": name, "width_binder": "1", "body": body,
             "family": "bool_to_bit", "comparison": "-",
             "bitvec_predicate": "BitVec.ofBool", "operands_swapped": False}), None


def read_defs(text):
    """[(name, width binder, body)] for every two-BitVec Bool definition."""
    return [(m.group(1), m.group(2), m.group(3).strip())
            for m in DEF.finditer(text)]


def classify(body):
    """(family, comparison) read off the body, or None if unrecognised."""
    family = None
    for token, name in CONVERSION.items():
        if token in body:
            family = name
            break
    if family is None:
        return None
    for token in sorted(COMPARISON, key=len, reverse=True):
        if token in body:
            return family, COMPARISON[token]
    return None


def lemma_for(name, binder, body):
    """The bridge lemma for one definition, or (None, why)."""
    what = classify(body)
    if what is None:
        return None, "body shape not recognised: %s" % body[:60]
    family, comparison = what
    key = (family, comparison)
    if key not in TARGET:
        return None, "no BitVec predicate for %s %s" % key
    target, swapped = TARGET[key]
    left, right = ("y", "x") if swapped else ("x", "y")
    conv = "BitVec.toInt" if family == "signed" else "BitVec.toNatInt"
    fill = {"def": name, "conv": conv, "target": target}
    statement = "    %s x y = %s %s %s := by" % (name, target, left, right)
    if MATRIX:
        # one theorem per candidate tactic, so a run says WHICH carried
        # rather than only that something did.  A tactic that fails is an
        # error at its own theorem and leaves the others elaborating.
        body_lines = []
        for index, tactic in enumerate(TACTICS):
            body_lines += [
                "theorem sail_bridge_%s_t%d {n : Nat} (x y : BitVec n) :"
                % (name, index),
                statement,
                "  %s" % (tactic % fill),
                ""]
        body_lines.pop()
    else:
        body_lines = ["theorem sail_bridge_%s {n : Nat} (x y : BitVec n) :" % name,
                      statement, "  first"]
        for tactic in TACTICS:
            body_lines.append("    | %s" % (tactic % fill))
    return ("\n".join(body_lines),
            {"definition": name, "width_binder": binder, "body": body,
             "family": family, "comparison": comparison,
             "bitvec_predicate": target, "operands_swapped": swapped}), None


MATRIX = False


def main():
    global MATRIX
    project, module, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    # `matrix` emits one theorem per (lemma, tactic) so the run reports which
    # tactic carried; the default emits one theorem per lemma with a `first`
    # over the same candidates, which is the form that goes into use
    MATRIX = len(sys.argv) > 4 and sys.argv[4] == "matrix"
    if MATRIX:
        print("matrix mode: one theorem per candidate tactic")
    lean_dir = os.path.join(project, module)
    prelude = os.path.join(lean_dir, "Prelude.lean")
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    from leanpath.strip import header_of
    header, closers = header_of(lean_dir, module)
    text = open(prelude).read()
    found = [(n, b, y, lemma_for) for n, b, y in read_defs(text)]
    n_cmp = len(found)
    found += [(n, b, y, bool_lemma_for) for n, b, y in read_bool_defs(text)]
    print("two-BitVec Bool definitions in the Prelude: %d" % n_cmp)
    print("Bool -> BitVec 1 definitions in the Prelude: %d" % (len(found) - n_cmp))

    lemmas, record, skipped = [], [], []
    for name, binder, body, maker in found:
        got, why = maker(name, binder, body)
        if got is None:
            skipped.append({"definition": name, "body": body, "why": why})
            print("  SKIPPED %-16s %s" % (name, why))
            continue
        lemma, meta = got
        lemmas.append(lemma)
        record.append(meta)
        print("  %-16s %-9s %-4s -> %-12s%s"
              % (name, meta["family"], meta["comparison"],
                 meta["bitvec_predicate"],
                 "  (operands swapped)" if meta["operands_swapped"] else ""))

    head = [
        "-- GENERATED by leanpath/sail_bridge.py from %s" % os.path.basename(prelude),
        "-- Every statement below is READ OUT OF the definition it bridges;",
        "-- none is typed.  A definition whose shape the generator did not",
        "-- recognise is skipped and named in the json beside this file, so a",
        "-- rename in Sail shows up as a MISSING lemma and never as a wrong one.",
        "-- The header is strip.header_of's, the same one the gate's files\n"
        "-- use: these definitions live inside the module namespace and an\n"
        "-- import alone does not reach them (measured, lane lp3_l106).",
        "",
        "-- the names this file depends on, checked before anything uses them",
        "#check @BitVec.ult",
        "#check @BitVec.ule",
        "#check @BitVec.slt",
        "#check @BitVec.sle",
        "#check @BitVec.toInt",
        "",
    ]
    open(out_path, "w").write(
        "\n".join(list(header) + head + lemmas + [""] + list(closers)) + "\n")
    meta_path = os.path.splitext(out_path)[0] + ".json"
    json.dump({"meta": {"what": "the Sail comparison bridge, generated",
                        "prelude": prelude,
                        "header_from": "leanpath.strip.header_of",
                        "definitions_seen": len(found),
                        "lemmas_emitted": len(lemmas),
                        "tactics_offered": TACTICS,
                        "matrix": MATRIX},
               "lemmas": record, "skipped": skipped},
              open(meta_path, "w"), indent=1, sort_keys=True)
    print()
    print("wrote %s (%d lemmas) and %s" % (out_path, len(lemmas), meta_path))


if __name__ == "__main__":
    main()
