#!/usr/bin/env python3
"""legality_filter2.py -- the legality reduction and validation, recomputed
over the CORRECTED scalar core and with the RATIFIED c++ quirk annotated.

WHAT CHANGED SINCE legality_filter.py (task 36, log 127), and nothing else

1. THE CORE.  `core_rule2.scalar_core` decides membership instead of the
   version-1 NUMERIC_MARKS tuple.  rust `bool` and swift `Bool` enter
   their cores; c, cpp and go are unchanged.  This moves the naive and the
   legal counts, because the candidate space is a cross-product over the
   core.
2. THE SCORING.  A candidate scored `predicted_legal_but_refused` whose
   misfired rule id is annotated in `legality_quirks.json` is counted as
   `agreement_by_ratified_quirk` and listed separately, keeping the
   compiler's refusal text verbatim.  The RULES ARE NOT EDITED: they
   already predict legal, which is what the ruling says they should.

Nothing existing is modified.  `legality_filter.py`, `legality_rules.json`
and `legality_reduction.json` are read only; the outputs here are new
names.

THE SPELLING BAN.  Candidates are selected and grouped by (operator UNIT
id, type pair) and quirks are keyed by RULE ID -- machine-form evidence.
No key, grouping, pairing or row structure is an operator token; a token
appears only in the `spelling` display field of a unit object carrying
`language` and `id`.  Both outputs are walked by the guard and this
program deletes its own output on a failure.

usage:
    /tmp/reconnect_venv/bin/python3 legality_filter2.py
writes:
    legality_reduction2.json
    legality_validation2.json
"""

import json
import os
import subprocess
import sys

import core_rule2
import legality_filter as v1

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_quirk_ids():
    path = os.path.join(HERE, "legality_quirks.json")
    doc = json.load(open(path))
    ids = set()
    for row in doc["annotations"]:
        ids.add((row["language"], row["rule_id"]))
    return ids, doc


def typed_core(lang, inv):
    """[(spelling, class)] over the version-2 core."""
    core, _undecided = core_rule2.scalar_core(lang, inv)
    out = []
    for spelling, _marking, cls in core:
        out.append((spelling, cls))
    return out


def reduction(by_id, units, inv):
    out = {}
    out["generated_by"] = "legality_filter2.py"
    out["population"] = (
        "the five compiled languages' operator units as the corpus's own "
        "acceptance record carries them, crossed with each language's "
        "EXTRACTED SCALAR CORE under core_rule2 (the corrected rule); no "
        "probe is written or compiled by this program")
    out["core_rule"] = "core_rule2.py (v2)"
    out["languages"] = []
    totals = {"naive": 0, "legal": 0, "units": 0, "units_with_a_rule": 0,
              "naive_of_units_without_a_rule": 0, "must_compile": 0}
    for lang in LANGS:
        typed = typed_core(lang, inv)
        naive = 0
        legal = 0
        naive_without_rule = 0
        unary_units = 0
        binary_units = 0
        with_rule = 0
        per_unit = []
        for row in units[lang]:
            bodies = v1.unit_bodies(by_id, row)
            has_rule = len(bodies) > 0
            if has_rule:
                with_rule = with_rule + 1
            unit_naive = 0
            unit_legal = 0
            if row["arity"] == "unary":
                unary_units = unary_units + 1
                for spelling, cls in typed:
                    unit_naive = unit_naive + 1
                    if not has_rule:
                        continue
                    if v1.admits(bodies, cls, spelling, None, None, "unary"):
                        unit_legal = unit_legal + 1
            else:
                binary_units = binary_units + 1
                for lspell, lcls in typed:
                    for rspell, rcls in typed:
                        unit_naive = unit_naive + 1
                        if not has_rule:
                            continue
                        if v1.admits(bodies, lcls, lspell, rcls, rspell,
                                     "binary"):
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
        must = legal + naive_without_rule
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
        record["naive_of_units_without_a_rule"] = naive_without_rule
        record["must_compile"] = must
        record["reduction_factor"] = (
            round(float(naive) / legal, 2) if legal else None)
        record["reduction_factor_including_no_rule_residue"] = (
            round(float(naive) / must, 2) if must else None)
        record["per_unit"] = per_unit
        out["languages"].append(record)
        totals["naive"] = totals["naive"] + naive
        totals["legal"] = totals["legal"] + legal
        totals["units"] = totals["units"] + len(units[lang])
        totals["units_with_a_rule"] = totals["units_with_a_rule"] + with_rule
        totals["naive_of_units_without_a_rule"] = (
            totals["naive_of_units_without_a_rule"] + naive_without_rule)
        totals["must_compile"] = totals["must_compile"] + must
    totals["reduction_factor"] = round(
        float(totals["naive"]) / totals["legal"], 2)
    totals["reduction_factor_including_no_rule_residue"] = round(
        float(totals["naive"]) / totals["must_compile"], 2)
    out["totals"] = totals
    out["the_two_residue_figures_named"] = {
        "legal": "candidates an extracted rule ADMITS. Compiling only these "
                 "would skip every operator unit for which no rule exists, "
                 "and log 127 measured that 136 corpus-accepted units live "
                 "on exactly those units -- so this figure is NOT the "
                 "regeneration population.",
        "must_compile": "legal + the candidates of units with NO rule, which "
                        "the filter passes through rather than judging. THIS "
                        "is the regeneration population.",
    }
    return out


def validation(by_id, units, inv, quirk_ids):
    out = {}
    out["generated_by"] = "legality_filter2.py"
    out["population"] = (
        "the compiled five's candidate corpus on disk: the same 4,440 "
        "candidates legality_filter.py scored, at the corpus's own six "
        "hand-written holder types. The corrected core does not change this "
        "population -- the corpus's probes already exist and are not "
        "re-selected here.")
    out["languages"] = []
    misses = []
    quirk_agreements = []
    fields = ["candidates", "accepted", "refused", "in_rule_scope",
              "out_of_rule_scope", "hit_accepted", "hit_refused",
              "agreement_by_ratified_quirk",
              "predicted_legal_but_refused",
              "predicted_illegal_but_accepted",
              "out_of_scope_accepted", "out_of_scope_refused"]
    totals = dict((f, 0) for f in fields)
    for lang in LANGS:
        data = json.load(open(os.path.join(HERE, "op_units_%s.json" % lang)))
        index = {}
        for row in units[lang]:
            index[(row["arity"], row["position"], row["spelling"])] = row
        counts = dict((f, 0) for f in fields)
        for key in data["probes"]:
            probe = data["probes"][key]
            meta = probe["meta"]
            accepted = ("ship" in probe) and (
                probe.get("refused") in (None, "", False))
            counts["candidates"] = counts["candidates"] + 1
            if accepted:
                counts["accepted"] = counts["accepted"] + 1
            else:
                counts["refused"] = counts["refused"] + 1
            row = index.get((meta["arity"], meta.get("position"),
                             meta["operator"]))
            bodies = v1.unit_bodies(by_id, row) if row else []
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
            lcls = class_of(lang, lspell, inv)
            rspell = meta.get("rhs_type")
            rcls = class_of(lang, rspell, inv) if rspell else None
            legal = v1.admits(bodies, lcls, lspell, rcls, rspell,
                              meta["arity"])
            if legal and accepted:
                counts["hit_accepted"] = counts["hit_accepted"] + 1
                continue
            if (not legal) and (not accepted):
                counts["hit_refused"] = counts["hit_refused"] + 1
                continue
            if legal and not accepted:
                hits = [rid for rid in row["rule_ids"]
                        if (lang, rid) in quirk_ids]
                if hits:
                    counts["agreement_by_ratified_quirk"] = (
                        counts["agreement_by_ratified_quirk"] + 1)
                    record = v1.miss_record(lang, key, meta, probe, row,
                                            "agreement_by_ratified_quirk")
                    record["ratified_quirk_rule_ids"] = hits
                    quirk_agreements.append(record)
                    continue
                counts["predicted_legal_but_refused"] = (
                    counts["predicted_legal_but_refused"] + 1)
                misses.append(v1.miss_record(lang, key, meta, probe, row,
                                             "predicted_legal_but_refused"))
                continue
            counts["predicted_illegal_but_accepted"] = (
                counts["predicted_illegal_but_accepted"] + 1)
            misses.append(v1.miss_record(lang, key, meta, probe, row,
                                         "predicted_illegal_but_accepted"))
        record = {"language": lang}
        record.update(counts)
        in_scope = counts["in_rule_scope"]
        hits = (counts["hit_accepted"] + counts["hit_refused"]
                + counts["agreement_by_ratified_quirk"])
        record["agreement_in_rule_scope"] = (
            round(100.0 * hits / in_scope, 1) if in_scope else None)
        out["languages"].append(record)
        for field in fields:
            totals[field] = totals[field] + counts[field]
    all_hits = (totals["hit_accepted"] + totals["hit_refused"]
                + totals["agreement_by_ratified_quirk"])
    totals["agreement_in_rule_scope"] = round(
        100.0 * all_hits / totals["in_rule_scope"], 1)
    out["totals"] = totals
    out["misses"] = misses
    out["quirk_agreements"] = quirk_agreements
    out["scoring_note"] = (
        "agreement_in_rule_scope counts hit_accepted + hit_refused + "
        "agreement_by_ratified_quirk over in_rule_scope. The quirk term is "
        "a RULING, recorded as its own column so the arithmetic without it "
        "is still readable: hit_accepted + hit_refused alone is the "
        "compiler-agreement figure.")
    out["compiler_agreement_without_the_ruling"] = round(
        100.0 * (totals["hit_accepted"] + totals["hit_refused"])
        / totals["in_rule_scope"], 1)
    return out


CLASS_CACHE = {}


def class_of(lang, spelling, inv):
    key = (lang, spelling)
    if key in CLASS_CACHE:
        return CLASS_CACHE[key]
    marking = None
    for entry in inv["languages"][lang]["types"]:
        if entry["spelling"] == spelling:
            marking = entry.get("class")
            break
    value = core_rule2.lookup_class(lang, spelling, marking)
    CLASS_CACHE[key] = value
    return value


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def write(name, doc):
    path = os.path.join(HERE, name)
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    return path


def main():
    _rules_doc, inv, by_id, units = v1.load()
    quirk_ids, quirk_doc = load_quirk_ids()
    red = reduction(by_id, units, inv)
    val = validation(by_id, units, inv, quirk_ids)
    val["quirk_annotations_applied"] = quirk_doc["annotations"]
    p1 = write("legality_reduction2.json", red)
    p2 = write("legality_validation2.json", val)

    old = json.load(open(os.path.join(HERE, "legality_reduction.json")))
    print("core sizes and residue, v1 -> v2")
    print("%-6s %6s %6s   %9s %9s   %9s %9s"
          % ("lang", "core1", "core2", "naive1", "naive2",
             "compile1", "compile2"))
    for i in range(len(LANGS)):
        a = old["languages"][i]
        b = red["languages"][i]
        print("%-6s %6d %6d   %9d %9d   %9d %9d"
              % (b["language"], a["extracted_scalar_core_size"],
                 b["extracted_scalar_core_size"],
                 a["naive_cross_product"], b["naive_cross_product"],
                 a["must_compile"], b["must_compile"]))
    print("%-6s %6s %6s   %9d %9d   %9d %9d"
          % ("TOTAL", "", "", old["totals"]["naive"], red["totals"]["naive"],
             old["totals"]["must_compile"], red["totals"]["must_compile"]))
    print()
    t = val["totals"]
    print("validation: in-scope %d ; agreement %.1f%% "
          "(compiler-only %.1f%%) ; misses %d ; quirk agreements %d"
          % (t["in_rule_scope"], t["agreement_in_rule_scope"],
             val["compiler_agreement_without_the_ruling"],
             len(val["misses"]), len(val["quirk_agreements"])))
    for row in val["quirk_agreements"]:
        print("  quirk agreement  %s %s  %s  | %s"
              % (row["language"], row["id"], row["expression"],
                 (row["refusal"] or "")[:90]))
    for row in val["misses"]:
        print("  MISS  %s %s  %s  | %s"
              % (row["language"], row["id"], row["expression"],
                 (row["refusal"] or "")[:90]))
    print("wrote %s" % p1)
    print("wrote %s" % p2)
    refuse_own_output_on_spelling_failure([p1, p2])


if __name__ == "__main__":
    main()
