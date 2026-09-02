#!/usr/bin/env python3
"""exception_families2.py -- STEP 2/3 of THE JOB (EXCEPTION-FAMILY TABLE).

GUARD IDENTITY (AgentMemory, SEEDED GROUPING UNDER CONDITIONS): two
guard rows from guards4.json are the SAME exception-family component
when

  (a) their CONDITION is the same predicate -- exact text match after
      normalization, since the condition texts already use the
      corpus's own ANCHORED naming (`in0`, `in1`) so "b == 0" in go
      and "b == 0" in swift already read as `in1 == 0` in both, and
      are directly comparable as text; where two texts differ but may
      still be the same predicate, z3 is asked to prove equivalence
      (see VERIFIED_MERGES below) -- never assumed from resemblance.
  (b) their RESPONSE KIND matches at the HEAD (`panic-call`, `trap`,
      `wrap-continue`, `clamp-continue`, `inline-special-case`); the
      callee name after `panic-call:` is metadata (detection route),
      never identity, per AgentMemory's ruling that the callee NAME is
      a display label and never identity.

EXCLUDED FROM FAMILY-BUILDING: rows whose response head is
`continue-with-a-different-answer`. That is core_modes.py's honest
"the pair disagrees here but no named response was proved" outcome
(z3 could not show the region clamps to 0, so `region_response`
records the weaker head) -- it is not one of the five guard-response
names AgentMemory's ruling lists, so it is not a guard component and
is not clustered into an exception family. It stays in guards4.json
as raw data and its count is reported here so the exclusion is
visible, not silent.

THE SPELLING BAN: family identity keys on (condition, response head)
-- MACHINE-FORM evidence -- never on the operator token. `operator`
appears only inside each row echoed under a family's `members`, as a
per-unit display field. check_no_spelling_keys.py is run on the
output.

TASK 8(c): this is round 1's exception_families.py re-pointed, byte
for byte in its clustering LOGIC, at guards4.json (the record of
record, guards2.json's 305 rows plus java's 8 measured rows) instead
of guards2.json alone. Round 1's 34 families were built WITHOUT java's
deopt evidence. See log_092 for whether `deopt-continue-elsewhere`
forms or joins a family, with the family row verbatim.
"""
import json
import os
import z3

HERE = os.path.dirname(os.path.abspath(__file__))

EXCLUDED_HEAD = "continue-with-a-different-answer"


def response_head(rk):
    if rk is None:
        return None
    return rk.split(":")[0]


def normalize_condition(cond):
    if cond is None:
        return None
    return " ".join(cond.split())


# ---------------------------------------------------------------------
# VERIFIED MERGES -- z3-checked equivalences between two DIFFERENT
# condition TEXTS that name the same predicate, both sides modelled as
# bitvector formulas over the corpus's own anchored `in0`/`in1`
# variables. Each entry is checked at generator run time (not assumed
# from resemblance) and the file REFUSES to write if a claimed
# equivalence does not actually hold. This is a short, named list --
# not a general text-similarity engine -- because only these two rust
# bit-trick predicates in the corpus have a second, plainer restatement
# elsewhere that a reader could otherwise mistake for a different
# condition.
# ---------------------------------------------------------------------

def _verify_int_min_and_neg_one(width, bit_trick_text, int_min_const):
    """z3-prove: bit_trick_text (as a formula over in0/in1 of `width`
    bits) is TRUE exactly when (in0 == int_min_const) AND (in1 == -1).
    Returns (proved: bool, note: str)."""
    in0 = z3.BitVec("in0", width)
    in1 = z3.BitVec("in1", width)
    if width == 32:
        bit_trick = ((z3.BitVecVal(-2147483648 & 0xffffffff, 32) + in0)
                     | ~in1) == 0
    elif width == 64:
        c = -9223372036854775808 & 0xffffffffffffffff
        bit_trick = (~in1 | (z3.BitVecVal(c, 64) ^ in0)) == 0
    else:
        raise ValueError(width)
    plain = z3.And(in0 == z3.BitVecVal(int_min_const & ((1 << width) - 1),
                                        width),
                   in1 == z3.BitVecVal(-1 & ((1 << width) - 1), width))
    s = z3.Solver()
    s.add(bit_trick != plain)
    got = s.check()
    if got == z3.unsat:
        return True, ("z3 proved (%s) == (in0 == INT_MIN(%d) AND "
                      "in1 == -1) for all %d-bit inputs (unsat on the "
                      "negation)" % (bit_trick_text, width, width))
    return False, "z3 returned %s -- NOT proved equivalent" % got


VERIFIED_MERGES = [
    dict(width=32,
         text_a="((-2147483648 + in0) | ~in1) == 0",
         canonical="in0 == -2147483648 (INT32_MIN) and in1 == -1",
         int_min_const=-2147483648),
    dict(width=64,
         text_a="(~in1 | (-9223372036854775808 ^ in0)) == 0",
         canonical="in0 == -9223372036854775808 (INT64_MIN) and "
                   "in1 == -1",
         int_min_const=-9223372036854775808),
]


def verify_merges():
    """returns {condition_text: canonical_label} for every claimed
    merge that z3 actually proved, and raises if one did not."""
    out = {}
    log = []
    for m in VERIFIED_MERGES:
        proved, note = _verify_int_min_and_neg_one(
            m["width"], m["text_a"], m["int_min_const"])
        log.append(dict(width=m["width"], text=m["text_a"],
                        canonical=m["canonical"], proved=proved,
                        note=note))
        if not proved:
            raise SystemExit("REFUSED: claimed z3 equivalence did not "
                             "hold -- %s" % note)
        out[m["text_a"]] = m["canonical"]
    return out, log


def family_id(condition_label, head, n):
    return "EF%04d" % n


def main():
    g2 = json.load(open(os.path.join(HERE, "guards4.json")))
    rows = g2["rows"]

    canon_labels, z3_log = verify_merges()

    excluded = 0
    clusters = {}
    for r in rows:
        head = response_head(r["response_kind"])
        if head == EXCLUDED_HEAD:
            excluded += 1
            continue
        cond = normalize_condition(r["condition"])
        label = canon_labels.get(cond, cond)
        key = (label, head)
        clusters.setdefault(key, []).append(r)

    families = []
    n = 0
    for (label, head), members in sorted(
            clusters.items(), key=lambda kv: (-len(kv[1]), str(kv[0]))):
        n += 1
        fid = "EF%04d" % n
        langs = sorted(set(m["language"] for m in members))
        by_lang_response = {}
        for m in members:
            by_lang_response.setdefault(m["language"], set()).add(
                response_head(m["response_kind"]))
        member_rows = []
        for m in sorted(members, key=lambda m: (m["language"], m["unit"])):
            member_rows.append(dict(
                unit=m["unit"], language=m["language"],
                operator=m["operator"], response_kind=m["response_kind"],
                detection=m["detection"], source=m.get("source")))
        families.append(dict(
            family_id=fid,
            condition_label=label,
            response_head=head,
            languages=langs,
            member_count=len(members),
            members=member_rows,
        ))

    out = dict(
        meta=dict(
            generator="exception_families2.py",
            role_note="the EXCEPTION-FAMILY axis of the two-table "
                       "design (AgentMemory SEEDED GROUPING UNDER "
                       "CONDITIONS): guard rows clustered by (condition "
                       "predicate, response-kind head), across "
                       "operators and languages, never merged with the "
                       "OPERATOR axis (dom_ops20.json).  No operator "
                       "token in any key -- see module docstring.",
            source="guards4.json",
            row_count_considered=len(rows) - excluded,
            row_count_excluded=excluded,
            excluded_reason="response head %r excluded: it is core_"
                            "modes.py's honest 'disagree here, no named "
                            "response proved' outcome and is not one of "
                            "the five guard-response names in "
                            "AgentMemory's ruling (panic-call / trap / "
                            "wrap-continue / clamp-continue / "
                            "inline-special-case), so it is not a guard "
                            "component" % EXCLUDED_HEAD,
            family_count=len(families),
            z3_verified_merges=z3_log,
        ),
        families=families,
    )
    json.dump(out, open(os.path.join(HERE, "exception_families2.json"), "w"),
               indent=1)

    print("families: %d (from %d guard rows, %d excluded as %r)"
          % (len(families), len(rows) - excluded, excluded, EXCLUDED_HEAD))
    for fam in families:
        print("\n%s  [%s / %s]  langs=%s  members=%d"
              % (fam["family_id"], fam["condition_label"],
                 fam["response_head"], ",".join(fam["languages"]),
                 fam["member_count"]))
        for m in fam["members"]:
            print("    %-6s %-12s %-10s %s" % (
                m["language"], m["unit"], m["operator"],
                m["response_kind"]))


if __name__ == "__main__":
    main()
