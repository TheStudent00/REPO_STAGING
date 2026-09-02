#!/usr/bin/env python3
"""legality_filter.py -- apply the extracted legality rules, count the
reduction, and validate the filter against the corpus.

TASK 36 (report-only).  Nothing here compiles a probe.

Two measurements come out of it:

1. THE REDUCTION (`legality_reduction.json`).  For each language: the
   naive cross-product candidate count over the extracted scalar core
   (every operator unit x every type, or type pair), the count the
   extracted rules admit, and the factor between them.

2. THE VALIDATION (`legality_validation.json`).  The same filter run over
   the corpus that exists on disk -- the compiled five's 4,440 candidates,
   1,779 accepted and 2,661 refused -- with every disagreement listed as a
   finding: the probe, its expression, the compiler's own refusal text and
   the rule that mis-fired.

THE SPELLING BAN.  Candidates are selected and grouped by (operator UNIT
id, type pair) -- machine-form evidence.  No key, grouping, pairing or row
structure is an operator token; a token appears only in the `spelling`
display field of a unit object carrying `language` and `id`.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

# How each language's OWN class marking is normalised to the four classes
# the rules speak in.  The left side is the marking the type inventory
# extracted from that language's authority; the right side is the class.
CLASS_NORMALISATION = {
    "c": {"integer_signed": "integer_signed",
          "integer_unsigned": "integer_unsigned",
          "float": "float"},
    "cpp": {"integer_signed": "integer_signed",
            "integer_unsigned": "integer_unsigned",
            "float": "float"},
    "go": {"IsInteger": "integer_signed",
           "IsInteger|IsUnsigned": "integer_unsigned",
           "IsFloat": "float",
           "IsBoolean": "truth_value"},
    "rust": {"integer_signed": "integer_signed",
             "integer_unsigned": "integer_unsigned",
             "float": "float"},
    "swift": {"integer_signed": "integer_signed",
              "integer_unsigned": "integer_unsigned",
              "float": "float",
              "truth_value": "truth_value"},
}

# Spellings whose class NO authority on this machine states, resolved here
# so the corpus validation can run at all.  Each is declared, not
# extracted; evidence class: human interpretation of stated design.  These
# are log 116's finding F3 (the stdint.h typedefs) and rust's grammar
# non-numeric split.
DECLARED_CLASSES = {
    ("c", "int32_t"): "integer_signed",
    ("c", "int64_t"): "integer_signed",
    ("c", "uint64_t"): "integer_unsigned",
    ("cpp", "int32_t"): "integer_signed",
    ("cpp", "int64_t"): "integer_signed",
    ("cpp", "uint64_t"): "integer_unsigned",
    ("rust", "bool"): "truth_value",
}

NUMERIC_MARKS = ("integer_signed", "integer_unsigned", "float",
                 "numeric_grammar_marked")

GO_SCALAR_FLAGS = ("IsInteger", "IsFloat", "IsBoolean")

GO_DISQUALIFY = ("IsUntyped", "IsComplex", "IsString")


def scalar_core(lang, inv):
    """The extracted scalar core, by log 116's own rule, re-implemented.

    Re-implemented rather than imported because log 116's file is not
    modified by this task and its module does other work on import.
    """
    core = []
    for entry in inv["languages"][lang]["types"]:
        spelling = entry["spelling"]
        if "::" in spelling:
            continue
        cls = entry.get("class")
        if lang == "go":
            flags = cls.split("|") if cls else []
            if any(f in GO_DISQUALIFY for f in flags):
                continue
            if any(f in GO_SCALAR_FLAGS for f in flags):
                core.append((spelling, cls))
            continue
        if cls in NUMERIC_MARKS:
            core.append((spelling, cls))
    return sorted(set(core))


def normalised_class(lang, spelling, marking):
    if (lang, spelling) in DECLARED_CLASSES:
        return DECLARED_CLASSES[(lang, spelling)]
    table = CLASS_NORMALISATION[lang]
    return table.get(marking)


def admits(rule_bodies, lhs_class, lhs_spelling, rhs_class, rhs_spelling,
           arity):
    """Does ANY of a unit's rules admit this operand shape?"""
    for body in rule_bodies:
        if body["arity"] != arity:
            continue
        if lhs_class not in body["lhs_classes"]:
            continue
        if arity == "unary":
            return True
        if body["rhs_classes"] is None:
            continue
        if rhs_class not in body["rhs_classes"]:
            continue
        if body["same_type_required"] and lhs_spelling != rhs_spelling:
            continue
        return True
    return False


def load():
    rules_doc = json.load(open(os.path.join(HERE, "legality_rules.json")))
    inv = json.load(open(os.path.join(HERE, "type_inventory2.json")))
    by_id = {}
    for record in rules_doc["rules"]:
        by_id[(record["language"], record["rule_id"])] = record["shape"]
    units = {}
    for lang in LANGS:
        units[lang] = []
    for row in rules_doc["operator_units"]:
        units[row["language"]].append(row)
    return rules_doc, inv, by_id, units


def unit_bodies(by_id, row):
    bodies = []
    for rule_id in row["rule_ids"]:
        key = (row["language"], rule_id)
        if key in by_id:
            bodies.append(by_id[key])
    return bodies


def reduction(rules_doc, inv, by_id, units):
    out = {}
    out["population"] = (
        "the five compiled languages' operator units as the corpus's own "
        "acceptance record carries them, crossed with each language's "
        "EXTRACTED SCALAR CORE from type_inventory2.json (log 125's "
        "current inventory); no probe is written or compiled")
    out["languages"] = []
    totals = {"naive": 0, "legal": 0, "units": 0, "units_with_a_rule": 0}
    for lang in LANGS:
        core = scalar_core(lang, inv)
        typed = []
        for spelling, marking in core:
            cls = normalised_class(lang, spelling, marking)
            typed.append((spelling, cls))
        naive = 0
        legal = 0
        naive_without_rule = 0
        unary_units = 0
        binary_units = 0
        with_rule = 0
        per_unit = []
        for row in units[lang]:
            bodies = unit_bodies(by_id, row)
            has_rule = len(bodies) > 0
            if has_rule:
                with_rule = with_rule + 1
            unit_naive = 0
            unit_legal = 0
            if row["arity"] == "unary":
                unary_units = unary_units + 1
                for spelling, cls in typed:
                    unit_naive = unit_naive + 1
                    if has_rule and admits(bodies, cls, spelling, None, None,
                                           "unary"):
                        unit_legal = unit_legal + 1
            else:
                binary_units = binary_units + 1
                for lspell, lcls in typed:
                    for rspell, rcls in typed:
                        unit_naive = unit_naive + 1
                        if has_rule and admits(bodies, lcls, lspell, rcls,
                                               rspell, "binary"):
                            unit_legal = unit_legal + 1
            naive = naive + unit_naive
            legal = legal + unit_legal
            if not has_rule:
                naive_without_rule = naive_without_rule + unit_naive
            per_unit.append({
                "language": lang,
                "id": row["id"],
                "spelling": row["spelling"],
                "arity": row["arity"],
                "position": row["position"],
                "has_extracted_rule": has_rule,
                "naive_candidates": unit_naive,
                "legal_candidates": unit_legal,
            })
        record = {}
        record["language"] = lang
        record["extracted_scalar_core_size"] = len(typed)
        record["operator_units_unary"] = unary_units
        record["operator_units_binary"] = binary_units
        record["operator_units_with_an_extracted_rule"] = with_rule
        record["operator_units_without_an_extracted_rule"] = (
            len(units[lang]) - with_rule)
        record["naive_cross_product"] = naive
        record["filtered_legal"] = legal
        record["reduction_factor"] = (
            round(float(naive) / legal, 2) if legal else None)
        # A unit with no extracted rule is NOT dropped: the filter has
        # nothing to say about it, so every one of its candidates still has
        # to go to the compiler.  This is the honest residue.
        record["naive_of_units_without_a_rule"] = naive_without_rule
        record["must_compile"] = legal + naive_without_rule
        record["reduction_factor_including_no_rule_residue"] = (
            round(float(naive) / (legal + naive_without_rule), 2)
            if (legal + naive_without_rule) else None)
        record["per_unit"] = per_unit
        out["languages"].append(record)
        totals["naive"] = totals["naive"] + naive
        totals["legal"] = totals["legal"] + legal
        totals["units"] = totals["units"] + len(units[lang])
        totals["units_with_a_rule"] = totals["units_with_a_rule"] + with_rule
        totals["must_compile"] = totals.get("must_compile", 0) + \
            legal + naive_without_rule
    totals["reduction_factor"] = (
        round(float(totals["naive"]) / totals["legal"], 2)
        if totals["legal"] else None)
    totals["reduction_factor_including_no_rule_residue"] = (
        round(float(totals["naive"]) / totals["must_compile"], 2)
        if totals["must_compile"] else None)
    out["totals"] = totals
    return out


def validation(rules_doc, inv, by_id, units):
    """Run the filter over the corpus that is on disk and score it."""
    out = {}
    out["population"] = (
        "the compiled five's candidate corpus on disk: 4,440 candidates, "
        "1,779 accepted, 2,661 refused, as op_units_<lang>.json's own tally "
        "states; six hand-written holder types per language")
    out["languages"] = []
    misses = []
    totals = {"candidates": 0, "accepted": 0, "refused": 0,
              "in_rule_scope": 0, "out_of_rule_scope": 0,
              "hit_accepted": 0, "hit_refused": 0,
              "predicted_legal_but_refused": 0,
              "predicted_illegal_but_accepted": 0,
              "out_of_scope_accepted": 0, "out_of_scope_refused": 0}
    for lang in LANGS:
        data = json.load(open(os.path.join(HERE, "op_units_%s.json" % lang)))
        index = {}
        for row in units[lang]:
            key = (row["arity"], row["position"], row["spelling"])
            index[key] = row
        counts = {"candidates": 0, "accepted": 0, "refused": 0,
                  "in_rule_scope": 0, "out_of_rule_scope": 0,
                  "hit_accepted": 0, "hit_refused": 0,
                  "predicted_legal_but_refused": 0,
                  "predicted_illegal_but_accepted": 0,
                  "out_of_scope_accepted": 0, "out_of_scope_refused": 0}
        for key in data["probes"]:
            probe = data["probes"][key]
            meta = probe["meta"]
            accepted = "refused" not in probe or not probe.get("refused")
            accepted = ("ship" in probe) and (probe.get("refused") in
                                              (None, "", False))
            counts["candidates"] = counts["candidates"] + 1
            if accepted:
                counts["accepted"] = counts["accepted"] + 1
            else:
                counts["refused"] = counts["refused"] + 1
            row = index.get((meta["arity"], meta.get("position"),
                             meta["operator"]))
            bodies = unit_bodies(by_id, row) if row else []
            if not bodies:
                counts["out_of_rule_scope"] = counts["out_of_rule_scope"] + 1
                if accepted:
                    counts["out_of_scope_accepted"] = (
                        counts["out_of_scope_accepted"] + 1)
                else:
                    counts["out_of_scope_refused"] = (
                        counts["out_of_scope_refused"] + 1)
                continue
            counts["in_rule_scope"] = counts["in_rule_scope"] + 1
            lspell = meta["lhs_type"]
            lcls = corpus_class(lang, lspell, inv)
            rspell = meta.get("rhs_type")
            rcls = corpus_class(lang, rspell, inv) if rspell else None
            legal = admits(bodies, lcls, lspell, rcls, rspell, meta["arity"])
            if legal and accepted:
                counts["hit_accepted"] = counts["hit_accepted"] + 1
            elif (not legal) and (not accepted):
                counts["hit_refused"] = counts["hit_refused"] + 1
            elif legal and not accepted:
                counts["predicted_legal_but_refused"] = (
                    counts["predicted_legal_but_refused"] + 1)
                misses.append(miss_record(lang, key, meta, probe, row,
                                          "predicted_legal_but_refused"))
            else:
                counts["predicted_illegal_but_accepted"] = (
                    counts["predicted_illegal_but_accepted"] + 1)
                misses.append(miss_record(lang, key, meta, probe, row,
                                          "predicted_illegal_but_accepted"))
        record = {"language": lang}
        record.update(counts)
        in_scope = counts["in_rule_scope"]
        hits = counts["hit_accepted"] + counts["hit_refused"]
        record["agreement_in_rule_scope"] = (
            round(100.0 * hits / in_scope, 1) if in_scope else None)
        out["languages"].append(record)
        for field in totals:
            totals[field] = totals[field] + counts[field]
    totals_hits = totals["hit_accepted"] + totals["hit_refused"]
    totals["agreement_in_rule_scope"] = (
        round(100.0 * totals_hits / totals["in_rule_scope"], 1)
        if totals["in_rule_scope"] else None)
    predicted_legal = (totals["hit_accepted"]
                       + totals["predicted_legal_but_refused"])
    corpus = {}
    corpus["candidates_today"] = totals["candidates"]
    corpus["predicted_legal_in_rule_scope"] = predicted_legal
    corpus["out_of_rule_scope_passed_through"] = totals["out_of_rule_scope"]
    corpus["would_be_compiled"] = predicted_legal + totals["out_of_rule_scope"]
    corpus["accepted_today"] = totals["accepted"]
    corpus["accepted_that_the_filter_would_have_dropped"] = (
        totals["predicted_illegal_but_accepted"])
    corpus["note"] = (
        "the same filter run at the corpus's own six holder types, stated "
        "as a compile budget: how many of the 4,440 candidates would be "
        "handed to a compiler, and how many of the 1,779 accepted units "
        "would be lost by not handing over the rest")
    out["corpus_sized_restatement"] = corpus
    out["totals"] = totals
    out["misses"] = misses
    return out


CLASS_CACHE = {}


def corpus_class(lang, spelling, inv):
    key = (lang, spelling)
    if key in CLASS_CACHE:
        return CLASS_CACHE[key]
    marking = None
    for entry in inv["languages"][lang]["types"]:
        if entry["spelling"] == spelling:
            marking = entry.get("class")
            break
    value = normalised_class(lang, spelling, marking)
    CLASS_CACHE[key] = value
    return value


def miss_record(lang, key, meta, probe, row, kind):
    record = {}
    record["language"] = lang
    record["id"] = "%s/probe_%s" % (lang, key)
    record["spelling"] = meta["operator"]
    record["kind"] = kind
    record["expression"] = meta["expression"]
    record["lhs_holder"] = meta["lhs_type"]
    record["rhs_holder"] = meta.get("rhs_type")
    record["refusal"] = probe.get("refused")
    record["rule_that_misfired"] = list(row["rule_ids"])
    return record


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    rules_doc, inv, by_id, units = load()
    red = reduction(rules_doc, inv, by_id, units)
    val = validation(rules_doc, inv, by_id, units)
    red_path = os.path.join(HERE, "legality_reduction.json")
    val_path = os.path.join(HERE, "legality_validation.json")
    fh = open(red_path, "w")
    json.dump(red, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    fh = open(val_path, "w")
    json.dump(val, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("REDUCTION")
    for record in red["languages"]:
        print("  %-6s core=%-3d units=%d/%d  naive=%-8d legal=%-7d x%s"
              % (record["language"], record["extracted_scalar_core_size"],
                 record["operator_units_with_an_extracted_rule"],
                 record["operator_units_with_an_extracted_rule"]
                 + record["operator_units_without_an_extracted_rule"],
                 record["naive_cross_product"], record["filtered_legal"],
                 record["reduction_factor"]))
    print("  TOTAL naive=%d legal=%d x%s"
          % (red["totals"]["naive"], red["totals"]["legal"],
             red["totals"]["reduction_factor"]))
    print("VALIDATION")
    for record in val["languages"]:
        print("  %-6s cand=%-5d in-scope=%-5d out=%-5d hit_acc=%-5d "
              "hit_ref=%-5d legal_but_refused=%-4d illegal_but_accepted=%-4d "
              "agree=%s%%"
              % (record["language"], record["candidates"],
                 record["in_rule_scope"], record["out_of_rule_scope"],
                 record["hit_accepted"], record["hit_refused"],
                 record["predicted_legal_but_refused"],
                 record["predicted_illegal_but_accepted"],
                 record["agreement_in_rule_scope"]))
    t = val["totals"]
    print("  TOTAL cand=%d acc=%d ref=%d in-scope=%d out=%d "
          "legal_but_refused=%d illegal_but_accepted=%d agree=%s%%"
          % (t["candidates"], t["accepted"], t["refused"], t["in_rule_scope"],
             t["out_of_rule_scope"], t["predicted_legal_but_refused"],
             t["predicted_illegal_but_accepted"],
             t["agreement_in_rule_scope"]))
    refuse_own_output_on_spelling_failure([red_path, val_path])


if __name__ == "__main__":
    main()
