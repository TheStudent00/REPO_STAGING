#!/usr/bin/env python3
"""equivalence_classes.py -- the arch-unit corpus quotiented by what its
members actually COMPUTE, so a proof is done once per class and not once per
unit.

the owner, 2026-09-17: "our new system could reduce the number of arch-units by
proving equivalence via emulations."

WHY THIS IS WORTH DOING. A compiler-operator is a (language, operator,
operand types) triple, and many triples lower to the SAME instruction
sequence: c's `a & b` on two 64-bit integers and c++'s `a bitand b` on the
same types are one `c.and a0, a1 ; c.jr ra`. Proving the emulation of one
equal to the arch-unit proves nothing new about the other -- it IS the other.

TWO LEVELS, AND THEY BUY DIFFERENT THINGS. This distinction is the whole
point and is kept explicit everywhere below.

  LEVEL 1, SYNTACTIC.  The instruction sequences are byte-identical.  The
  Lean goal is then LITERALLY THE SAME GOAL, so one proof discharges every
  member and the saving costs nothing -- no second prover, no new axiom, no
  new lemma.  This is free.

  LEVEL 2, SEMANTIC.  The sequences differ but the walked, normalised terms
  agree.  `subw a0, zero, a0` and `sub a0, zero, a0` read at 32 bits are one
  function; so are `c.jr ra` and `jalr zero, 0x0(ra)`.  A proof about one
  member does NOT transfer for free: it needs the equivalence itself proved
  where the proof lives.  z3 saying so is evidence, not a Lean proof.  What
  makes it still worth having is that the merge lemma is SMALL -- a fact
  about two short instruction sequences -- next to the full emulation goal it
  replaces.

So level 1 is a reduction in WORK. Level 2 is a reduction in work TRADED for
a small obligation, and every such obligation is listed by name in the output
rather than folded silently into the count.

THE SPELLING BAN: the class key is the instruction sequence or the walked
term, both machine-formed. No operator token is used for any key, grouping or
comparison scope; the token rides on members as a display label only.

    python3 equivalence_classes.py <riscv dir> <out path>
"""

import collections
import json
import os
import sys


def read_rows(path, outcome="LIFTED"):
    if not os.path.exists(path):
        return []
    doc = json.load(open(path))
    return [r for r in doc["rows"] if r.get("outcome") == outcome]


def body_key(row):
    """The instruction sequence, whitespace-normalised and nothing else.

    Registers and immediates are KEPT. Abstracting them would merge units
    that are not the same computation, which is the one mistake this file
    must not make."""
    return tuple(" ".join(line.split()) for line in (row.get("body") or []))


# ------------------------------------------------------- the arrival shape --
# CORRECTION, 2026-09-17, caught before the classes were used. The body alone
# is the right key for the `plain` goal -- and `plain` is the goal log 294
# section 2.3 showed to be FALSE by construction, because it puts the two
# sides together with no psABI precondition. The goal that is actually true,
# and the only one worth proving, is `abi`, and its statement WIDENS each
# operand according to how that operand arrives. Two units sharing a body but
# arriving differently are therefore DIFFERENT GOALS and must not be merged.
#
# What the widening depends on is the arrival SHAPE, not the type's spelling:
# `int32_t` and `int32` widen identically, and so must key identically.
ARRIVAL = {
    "int32_t": "s32", "int32": "s32", "i32": "s32",
    "uint32_t": "u32", "uint32": "u32", "u32": "u32",
    "float": "u32", "float32": "u32",
    "bool": "b1", "_Bool": "b1",
}


def arrival_shape(row):
    out = []
    for name in (row.get("lhs_type"), row.get("rhs_type")):
        text = (name or "").strip()
        if text in ("", "None", "none"):
            out.append("-")
        else:
            out.append(ARRIVAL.get(text, "w64"))
    return tuple(out)


def goal_key(row):
    """The key for the goal actually proved: the body AND the arrivals."""
    return (body_key(row), arrival_shape(row))


def main():
    rv_dir, out_path = sys.argv[1], sys.argv[2]
    rows = []
    for name in ("attest_rv.json", "attest_rv_langs.json"):
        got = read_rows(os.path.join(rv_dir, name))
        rows += got
        print("  %-24s %d arch-units" % (name, len(got)))
    print("corpus: %d arch-units" % len(rows))

    # ---- level 0: the body alone, which serves only the `plain` goal -------
    by_body_only = collections.defaultdict(list)
    for row in rows:
        by_body_only[body_key(row)].append(row)
    print()
    print("the body alone -- %d classes. This is the number for the `plain`"
          % len(by_body_only))
    print("goal, and `plain` is false by construction (log 294 2.3), so it is")
    print("reported here only so it is not mistaken for the real one.")

    # ---- level 1: the body AND the arrivals, which is the real goal --------
    by_body = collections.defaultdict(list)
    for row in rows:
        by_body[goal_key(row)].append(row)
    print()
    print("LEVEL 1, syntactic -- the same sequence AND the same arrivals")
    print("  classes: %d" % len(by_body))
    print("  %d arch-units -> %d proofs (%.1fx), and the saving is FREE:"
          % (len(rows), len(by_body), len(rows) / float(len(by_body))))
    print("  the Lean goal is literally the same goal, so nothing is owed.")

    # ---- level 2: the walked terms, where a walk exists --------------------
    terms = {}
    claim = os.path.join(rv_dir, "xarch", "claim_all.json")
    if os.path.exists(claim):
        for row in json.load(open(claim))["rows"]:
            text = row.get("riscv_term")
            if not row.get("unit") or not text:
                continue
            if str(text).startswith("NORMALISE_REFUSED"):
                continue
            terms[row["unit"]] = (str(text), row.get("answer_width"))

    # a class gets a term only when EVERY body in it walked to the same one;
    # a class with no walked member, or with disagreeing members, stays its own
    class_term = {}
    for key, members in by_body.items():
        seen = set(terms[m["unit"]] for m in members if m["unit"] in terms)
        if len(seen) == 1:
            class_term[key] = seen.pop()

    merged = collections.defaultdict(list)
    for key in by_body:
        merged[class_term.get(key, ("body", key))].append(key)
    obligations = {k: v for k, v in merged.items() if len(v) > 1}

    print()
    print("LEVEL 2, semantic -- different sequences, the same walked term")
    print("  classes with a term the whole class agrees on: %d of %d"
          % (len(class_term), len(by_body)))
    print("  level-1 classes that MERGE with another: %d groups covering %d classes"
          % (len(obligations), sum(len(v) for v in obligations.values())))
    after = len(by_body) - sum(len(v) - 1 for v in obligations.values())
    print("  %d -> %d proofs, at the cost of %d merge lemmas"
          % (len(by_body), after, len(obligations)))

    # ---- the artifact ------------------------------------------------------
    classes = []
    for key, members in sorted(by_body.items(), key=lambda kv: -len(kv[1])):
        rep = sorted(members, key=lambda r: r["unit"])[0]
        classes.append({
            "representative": rep["unit"],
            "body": list(key[0]),
            "arrival_shape": list(key[1]),
            "instruction_count": len(key[0]),
            "members": sorted(m["unit"] for m in members),
            "member_count": len(members),
            "languages": sorted(set(m["lang"] for m in members)),
            "walked_term": class_term.get(key, [None, None])[0],
            "answer_width": class_term.get(key, [None, None])[1],
        })

    obligation_rows = []
    for term, keys in obligations.items():
        obligation_rows.append({
            "walked_term": term[0],
            "answer_width": term[1],
            "sequences": [list(k[0]) for k in keys],
            "arrival_shapes": [list(k[1]) for k in keys],
            "representatives": sorted(
                sorted(by_body[k], key=lambda r: r["unit"])[0]["unit"]
                for k in keys),
            "what_is_owed": ("a proof that these instruction sequences are one "
                             "function; z3 agreeing is evidence, not that proof"),
        })

    doc = {
        "meta": {
            "what": "the arch-unit corpus quotiented by what its members "
                    "compute, so a proof is done once per class",
            "corpus": len(rows),
            "body_only_classes": len(by_body_only),
            "body_only_note": "the count for the `plain` goal, which is false "
                              "by construction; not the real reduction",
            "level_1_classes": len(by_body),
            "level_1_note": "identical instruction sequences AND identical "
                            "psABI arrival shapes; the Lean goal is the same "
                            "goal, so one proof covers the class and nothing "
                            "is owed",
            "level_2_classes": after,
            "level_2_note": "different sequences with the same walked term; "
                            "each merge OWES a proof that they are one "
                            "function, and they are listed in `obligations`",
            "merge_lemmas_owed": len(obligations),
        },
        "classes": classes,
        "obligations": sorted(obligation_rows,
                              key=lambda r: -len(r["sequences"])),
    }
    fh = open(out_path, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print()
    print("  the ten largest classes:")
    for c in classes[:10]:
        print("    x%-4d %-9s %-10s %s" % (c["member_count"],
                                          ",".join(c["languages"]),
                                          ",".join(c["arrival_shape"]),
                                          " ; ".join(c["body"])[:70]))
    print()
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
