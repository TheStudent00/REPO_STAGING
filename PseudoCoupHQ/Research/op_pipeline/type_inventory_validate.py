#!/usr/bin/env python3
"""type_inventory_validate.py -- TASK 29 (b) and (c): measure the gap
between the EXTRACTED type inventory and the EXISTING corpus.

WHAT IS BEING COMPARED
----------------------
type_inventory.json (TASK 29a, this session) holds, per language, every
scalar type spelling some AUTHORITY admits -- a tree-sitter grammar rule,
or the compiler's own type table.

probe_gen.py holds `HOLDERS`: a HAND-WRITTEN six-row list per language
(i32 i64 u64 f32 f64 bool).  Every probe in the corpus was generated from
that six-row list, so op_units_<lang>.json's 1,779 accepted rows and its
2,661 refused rows are the compiler's testimony about the SIX, and about
nothing else.

THREE MEASUREMENTS, both directions
-----------------------------------
1. INVENTORY -> CORPUS (what the six missed).  Which extracted scalar
   types were never probed at all, and how many candidate probes a
   regeneration over the extracted inventory would produce.  The
   regeneration multiplier is computed from the corpus's own candidate
   counts, NOT from any operator list: with h holder types, a unary
   candidate exists per type (h of them per operator) and a binary
   candidate per ordered pair (h*h per operator), so
       unary_operator_count  = unary_candidates  / h
       binary_operator_count = binary_candidates / (h*h)
   and the predicted count at a new h' is
       unary_operator_count*h' + binary_operator_count*h'*h'.
   This deliberately never touches an operator spelling.

2. CORPUS -> INVENTORY (what the corpus used that the inventory does not
   admit).  Every accepted probe's operand spelling is looked up in the
   extracted inventory.  A spelling used by an accepted probe and NOT
   admitted by any authority is a hole in the extraction and is reported
   as one.

3. REFUSED COMBINATIONS (what a cross product cannot predict).  A type
   cross product predicts CANDIDATES, never ACCEPTANCE.  Every refused
   probe is bucketed by its ORDERED TYPE PAIR and, separately, by a
   cause family read off the compiler's own refusal words.  The point of
   the measurement: how much of the refusal mass is explained by the
   type pair alone (a cell where every candidate was refused) and how
   much is not (a cell that is part accepted, part refused -- which no
   type inventory can predict, because the operator's own rules decide).

THE SPELLING BAN
----------------
Nothing here is grouped, paired, keyed or selected by an operator token.
The grouping keys are TYPE PAIRS ("i32,f64"), language names, and cause
families named after the compiler's diagnostic shape.  Operator tokens
appear only inside per-unit example objects, which carry `lang` and `n`,
and inside quoted refusal text (the compiler's own words).  The output is
checked by check_no_spelling_keys.py.

NOTHING IS REGENERATED.  the owner reserved that decision; this program only
sizes it.

USAGE
  /tmp/reconnect_venv/bin/python3 type_inventory_validate.py
writes:
  type_inventory_validation.json
  type_inventory_validation.md
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

# The scalar-core rule, stated once, applied mechanically.  A type is in
# the scalar core when an EXTRACTED class marking says it is an integer,
# a float or a truth value -- the marking comes from the source (clang's
# SIGNED_TYPE/UNSIGNED_TYPE/FLOATING_TYPE macro, go/types' IsInteger /
# IsFloat / IsBoolean flags, rust.js's numericTypes split).  A type whose
# class marking is missing is NOT guessed: it goes to `undecided`, and
# the gap is reported as a range.
NUMERIC_MARKS = ("integer_signed", "integer_unsigned", "float",
                 "numeric_grammar_marked")
GO_SCALAR_FLAGS = ("IsInteger", "IsFloat", "IsBoolean")
GO_DISQUALIFY = ("IsUntyped", "IsComplex", "IsString")

# Cause families for refusal text.  Each family is named for the SHAPE of
# the diagnostic, and carries the regex that recognises it.  No family is
# named after an operator.
CAUSE_FAMILIES = [
    ("no_such_trait_or_protocol_conformance",
     r"trait bound|is not satisfied|does not conform|no exact matches|"
     r"referencing operator function"),
    ("operand_types_are_not_compatible",
     r"invalid operands|mismatched types|invalid argument type|"
     r"cannot convert|type mismatch|incompatible|operator .* cannot be "
     r"applied|of different types"),
    ("operand_type_is_not_allowed_here",
     r"invalid argument|not defined on|undefined \(type|operand of type|"
     r"cannot be used as|expects argument|requires an? "),
    ("operand_is_not_a_pointer_or_a_reference",
     r"indirection requires pointer|cannot be dereferenced|cannot indirect|"
     r"may only be used to pass an argument|non-channel|"
     r"cannot take the address|not a pointer"),
    ("shift_position_has_its_own_operand_rule",
     r"shifted operand|shift count|invalid shift"),
    ("form_needs_a_generic_bound_the_scalar_does_not_have",
     r"can only be applied to values that implement|does not implement|"
     r"no implementation for"),
    ("the_form_wants_something_that_is_not_a_value_operand",
     r"expects a type on its right|unknown type name|"
     r"doesn't have fields|call to undeclared function|"
     r"expects a type|requires a type"),
    ("this_form_is_withdrawn_or_restricted_for_this_operand",
     r"is unavailable|does not allow incrementing|cannot decrement|"
     r"cannot be narrowed|not unwrapped|does not support concurrency|"
     r"deprecated|is not allowed"),
    ("expression_is_not_well_formed_at_all",
     r"expected |unexpected |syntax error|parse error|cannot find|"
     r"not found|no member|unresolved"),
    ("result_type_does_not_match_the_stated_signature",
     r"mismatched types.*expected|cannot use .* as .* value in return|"
     r"return type|not convertible"),
]


def cause_family(text):
    t = (text or "").lower()
    for name, rx in CAUSE_FAMILIES:
        if re.search(rx, t):
            return name
    return "unclassified_refusal_text"


def scalar_core(lang, inv):
    """Split a language's extracted types into scalar core / not / undecided.

    Entries whose key is prefixed `clang_builtin::` or `rustc_enum::` are
    compiler-table ids, not source spellings; they are counted separately
    because a probe cannot be written with them.
    """
    core, notcore, undecided, ids = [], [], [], []
    for e in inv["languages"][lang]["types"]:
        spelling = e["spelling"]
        if "::" in spelling:
            ids.append(spelling)
            continue
        cls = e.get("class")
        if lang == "go":
            flags = cls.split("|") if cls else []
            if any(f in GO_DISQUALIFY for f in flags):
                notcore.append(spelling)
            elif any(f in GO_SCALAR_FLAGS for f in flags):
                core.append(spelling)
            else:
                notcore.append(spelling)
            continue
        if cls in NUMERIC_MARKS:
            core.append(spelling)
        elif cls is None:
            undecided.append(spelling)
        else:
            undecided.append(spelling)
    return sorted(core), sorted(notcore), sorted(undecided), sorted(ids)


def rows(lang, spellings, tag):
    """Render a list of type spellings as UNIT OBJECTS.

    A bare list of spellings would fail check_no_spelling_keys.py the
    moment a type spelling collides with an operator spelling somewhere
    in the 91-token inventory -- `void` does.  The guard is right to
    refuse that shape, so every spelling here rides on an object that
    carries its own `language` and `id`, with the spelling in the
    `spelling` field: the one place a token-shaped string is allowed,
    a display label on a member.
    """
    if spellings is None:
        return None
    return [{"language": lang, "id": "%s/%s_%d" % (lang, tag, i),
             "spelling": s} for i, s in enumerate(spellings)]


def refuse_own_output_on_spelling_failure(paths):
    """THE MECHANICAL GUARD (AgentMemory, the owner 2026-08-25).

    Every stage that groups or pairs units runs check_no_spelling_keys.py
    over its own output and REFUSES that output on failure -- the file is
    removed and the program exits nonzero, so a spelling-keyed artifact
    can never be left on disk for a later stage to inherit.
    """
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd += paths
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        print("REFUSED OWN OUTPUT: spelling-key check failed; "
              "the written file(s) were removed")
        return False
    return True


def main():
    inv = json.load(open(os.path.join(HERE, "type_inventory.json")))
    out = {
        "generated_by": "type_inventory_validate.py",
        "task": "TASK 29 (b)/(c) -- gap measurement, both directions",
        "reads": ["type_inventory.json", "op_units_<lang>.json",
                  "probe_manifest_<lang>.json", "probe_gen.py :: HOLDERS"],
        "regenerates_nothing": "TASK 29 (c): the regeneration decision is "
                               "the owner's; this file carries the numbers it needs",
        "scalar_core_rule": {
            "statement": "a type is in the scalar core when an EXTRACTED "
                         "class marking calls it an integer, a float or a "
                         "truth value; a type with no extracted marking is "
                         "not guessed, it is listed as undecided",
            "numeric_marks": list(NUMERIC_MARKS),
            "go_scalar_flags": list(GO_SCALAR_FLAGS),
            "go_disqualifying_flags": list(GO_DISQUALIFY),
        },
        "cause_families": [{"family": n, "recogniser": r}
                           for n, r in CAUSE_FAMILIES],
        "languages": {},
        "totals": {},
    }

    # probe_gen's hand-written table, read out of the file rather than
    # restated, so a later edit of probe_gen.py cannot silently desync.
    src = open(os.path.join(HERE, "probe_gen.py")).read()
    m = re.search(r"HOLDERS = \{(.*?)\n\}\n", src, re.S)
    holders = {}
    for lang_block in re.finditer(
            r'"(\w+)": \[(.*?)\]', m.group(1), re.S):
        holders[lang_block.group(1)] = re.findall(
            r'\("(\w+)", "([^"]+)"\)', lang_block.group(2))

    tot = {"accepted": 0, "refused": 0, "candidates": 0,
           "predicted_candidates_at_extracted_core": 0}

    for lang in LANGS:
        core, notcore, undecided, ids = scalar_core(lang, inv)
        hand = [t for _, t in holders[lang]]
        units = json.load(open(os.path.join(HERE, "op_units_%s.json" % lang)))
        probes = units["probes"]

        n_unary = sum(1 for r in probes.values()
                      if r["meta"]["arity"] == "unary")
        n_binary = sum(1 for r in probes.values()
                       if r["meta"]["arity"] == "binary")
        h = len(hand)
        unary_operator_count = n_unary / float(h)
        binary_operator_count = n_binary / float(h * h)

        # measurement 1 -- what the six missed
        missed = sorted(set(core) - set(hand))
        used_not_in_core = sorted(set(hand) - set(core))

        def predict(hp):
            return int(round(unary_operator_count * hp
                             + binary_operator_count * hp * hp))

        h_core = len(core)
        h_max = len(core) + len(undecided)

        # A narrower, still fully extracted subset: the spellings TWO
        # independent authorities admit -- a grammar rule AND the
        # compiler's own table.  For c and cpp this cuts away clang's
        # extension-only rows (the fixed-point `_Accum` / `_Fract`
        # family, `__int128_t`, `wchar_t`), which the tree-sitter
        # grammar's `primitive_type` token list does not carry.
        by_spelling = {e["spelling"]: e
                       for e in inv["languages"][lang]["types"]}
        enumerating = set()
        for t in inv["languages"][lang]["types"]:
            for a in t["admitted_by"]:
                if a["witness"] in ("grammar", "compiler_table"):
                    enumerating.add(a["witness"])
        if len(enumerating) == 2:
            two_witness = sorted(
                t for t in core
                if len({a["witness"] for a in
                        by_spelling[t]["admitted_by"]}
                       & {"grammar", "compiler_table"}) == 2)
        else:
            # fewer than two ENUMERATING witnesses exist for this language,
            # so a two-authority subset is not defined here; saying 0 would
            # read as "no type qualifies", which is a different claim.
            two_witness = None

        # measurement 2 -- corpus spellings the inventory does not admit
        admitted = {e["spelling"] for e in inv["languages"][lang]["types"]}
        accepted_rows = [r for r in probes.values() if "ship" in r]
        unadmitted = {}
        for r in accepted_rows:
            for side in ("lhs_type", "rhs_type"):
                t = r["meta"].get(side)
                if t and t not in admitted:
                    unadmitted[t] = unadmitted.get(t, 0) + 1

        # measurement 3 -- refusal mass, by ordered type pair and by cause
        cells = {}
        families = {}
        for r in probes.values():
            meta = r["meta"]
            pair = "%s,%s" % (meta["lhs_rep"], meta["rhs_rep"])
            cell = cells.setdefault(pair, {"accepted": 0, "refused": 0})
            if "ship" in r:
                cell["accepted"] += 1
            else:
                cell["refused"] += 1
                fam = cause_family(r.get("refused"))
                f = families.setdefault(fam, {"count": 0, "example": None})
                f["count"] += 1
                if f["example"] is None:
                    f["example"] = {
                        "lang": lang, "n": meta["n"], "operator": meta["operator"],
                        "expression": meta["expression"],
                        "refusal": (r.get("refused") or "")[:200]}

        all_refused = {k: v for k, v in cells.items() if v["accepted"] == 0}
        mixed = {k: v for k, v in cells.items()
                 if v["accepted"] and v["refused"]}
        all_accepted = {k: v for k, v in cells.items() if v["refused"] == 0}
        refused_in_all_refused_cells = sum(v["refused"] for v in all_refused.values())
        refused_in_mixed_cells = sum(v["refused"] for v in mixed.values())

        out["languages"][lang] = {
            "extracted": {
                "scalar_core": rows(lang, core, "core"),
                "scalar_core_count": len(core),
                "not_scalar": rows(lang, notcore, "notscalar"),
                "undecided_no_extracted_class": rows(lang, undecided, "undecided"),
                "undecided_count": len(undecided),
                "compiler_table_ids_not_writable_as_a_probe": rows(
                    lang, ids, "tableid"),
            },
            "hand_written_holders_in_probe_gen": rows(lang, hand, "hand"),
            "hand_written_holders_count": len(hand),
            "direction_1_inventory_to_corpus": {
                "scalar_core_types_never_probed": rows(lang, missed, "missed"),
                "scalar_core_types_never_probed_count": len(missed),
                "hand_written_types_not_in_extracted_core": rows(
                    lang, used_not_in_core, "handnotcore"),
                "corpus_candidates": units["tally"]["candidates"],
                "corpus_unary_candidates": n_unary,
                "corpus_binary_candidates": n_binary,
                "derived_unary_operator_count": unary_operator_count,
                "derived_binary_operator_count": binary_operator_count,
                "two_authority_scalar_core": rows(lang, two_witness, "twoauth"),
                "two_authority_scalar_core_count": (
                    None if two_witness is None else len(two_witness)),
                "two_authority_not_defined_because": (
                    None if two_witness is not None else
                    "only these enumerating witnesses exist for this "
                    "language: %s" % sorted(enumerating)),
                "predicted_candidates_at_two_authority_core": (
                    None if two_witness is None else predict(len(two_witness))),
                "predicted_candidates_at_core": predict(h_core),
                "predicted_candidates_at_core_plus_undecided": predict(h_max),
                "growth_factor_at_core": round(
                    predict(h_core) / float(units["tally"]["candidates"]), 2),
            },
            "direction_2_corpus_to_inventory": {
                "accepted_probes": len(accepted_rows),
                "operand_spellings_used_by_accepted_probes": rows(
                    lang, sorted({r["meta"][s] for r in accepted_rows
                                  for s in ("lhs_type", "rhs_type")
                                  if r["meta"].get(s)}), "used"),
                "spellings_no_authority_admits": [
                    {"language": lang, "id": "%s/hole_%d" % (lang, i),
                     "spelling": sp, "sides": n}
                    for i, (sp, n) in enumerate(sorted(unadmitted.items()))],
                "hole_count": len(unadmitted),
            },
            "direction_3_refused_combinations": {
                "refused_probes": units["tally"]["refused"],
                "type_pair_cells": len(cells),
                "cells_all_refused": len(all_refused),
                "cells_mixed": len(mixed),
                "cells_all_accepted": len(all_accepted),
                "refusals_in_all_refused_cells": refused_in_all_refused_cells,
                "refusals_in_mixed_cells": refused_in_mixed_cells,
                "pct_refusals_a_type_pair_alone_explains": round(
                    100.0 * refused_in_all_refused_cells
                    / max(1, units["tally"]["refused"]), 1),
                "cause_families": dict(sorted(
                    families.items(), key=lambda kv: -kv[1]["count"])),
                "cells": dict(sorted(cells.items())),
            },
        }
        tot["accepted"] += len(accepted_rows)
        tot["refused"] += units["tally"]["refused"]
        tot["candidates"] += units["tally"]["candidates"]
        tot["predicted_candidates_at_extracted_core"] += predict(h_core)
        if two_witness is not None:
            tot["predicted_candidates_at_two_authority_core"] = tot.get(
                "predicted_candidates_at_two_authority_core", 0) + predict(
                len(two_witness))

    tot["growth_factor"] = round(
        tot["predicted_candidates_at_extracted_core"]
        / float(tot["candidates"]), 2)
    out["totals"] = tot

    jp = os.path.join(HERE, "type_inventory_validation.json")
    json.dump(out, open(jp, "w"), indent=1)

    md = []
    A = md.append
    A("# type_inventory_validation -- TASK 29 (b)/(c)\n")
    A("Generated by `type_inventory_validate.py`. Nothing regenerated.\n")
    A("## Direction 1 -- what the hand-written six missed\n")
    A("| language | extracted scalar core | two-authority core | undecided | "
      "hand-written | never probed | corpus candidates | predicted at "
      "two-authority core | predicted at full core |")
    A("|---|---|---|---|---|---|---|---|---|")
    for lang in LANGS:
        L = out["languages"][lang]
        d1 = L["direction_1_inventory_to_corpus"]
        A("| %s | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            lang, L["extracted"]["scalar_core_count"],
            -1 if d1["two_authority_scalar_core_count"] is None
            else d1["two_authority_scalar_core_count"],
            L["extracted"]["undecided_count"],
            L["hand_written_holders_count"],
            d1["scalar_core_types_never_probed_count"],
            d1["corpus_candidates"],
            -1 if d1["predicted_candidates_at_two_authority_core"] is None
            else d1["predicted_candidates_at_two_authority_core"],
            d1["predicted_candidates_at_core"]))
    A("")
    A("## Direction 2 -- corpus spellings no authority admits\n")
    A("| language | accepted probes | holes |")
    A("|---|---|---|")
    for lang in LANGS:
        d2 = out["languages"][lang]["direction_2_corpus_to_inventory"]
        A("| %s | %d | %d |" % (lang, d2["accepted_probes"], d2["hole_count"]))
    A("")
    A("## Direction 3 -- refusal mass by type-pair cell\n")
    A("| language | refused | cells | all-refused | mixed | all-accepted | "
      "%% a type pair alone explains |")
    A("|---|---|---|---|---|---|---|")
    for lang in LANGS:
        d3 = out["languages"][lang]["direction_3_refused_combinations"]
        A("| %s | %d | %d | %d | %d | %d | %s |" % (
            lang, d3["refused_probes"], d3["type_pair_cells"],
            d3["cells_all_refused"], d3["cells_mixed"],
            d3["cells_all_accepted"],
            d3["pct_refusals_a_type_pair_alone_explains"]))
    A("")
    mp = os.path.join(HERE, "type_inventory_validation.md")
    open(mp, "w").write("\n".join(md))

    for lang in LANGS:
        L = out["languages"][lang]
        d1 = L["direction_1_inventory_to_corpus"]
        d2 = L["direction_2_corpus_to_inventory"]
        d3 = L["direction_3_refused_combinations"]
        print("%-6s core=%-2d two_auth=%-2d undecided=%-2d missed=%-2d "
              "candidates=%-5d predicted=%-7d holes=%d refused=%-4d "
              "pair_explains=%s%%"
              % (lang, L["extracted"]["scalar_core_count"],
                 -1 if d1["two_authority_scalar_core_count"] is None
                 else d1["two_authority_scalar_core_count"],
                 L["extracted"]["undecided_count"],
                 d1["scalar_core_types_never_probed_count"],
                 d1["corpus_candidates"], d1["predicted_candidates_at_core"],
                 d2["hole_count"], d3["refused_probes"],
                 d3["pct_refusals_a_type_pair_alone_explains"]))
    print("TOTALS", json.dumps(tot))
    if not refuse_own_output_on_spelling_failure([jp]):
        return 1
    print("wrote %s" % jp)
    print("wrote %s" % mp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
