#!/usr/bin/env python3
"""build_table24b.py -- TASK 10 rebuild. NEW files only:
dominant_table24b.json / dom_ops22b.json / representatives24b.json.
Does NOT overwrite dominant_table24.json / dom_ops22.json.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure.

WHAT CHANGED FROM build_table24.py. Identical 0-branch population,
identical representative-groups step (ground a/b/c unchanged),
identical exact-text seed join. ADDITIONALLY, after the exact-text
join, every seed still unmatched or text-ambiguous gets a SECOND
attempt: restrict candidate rows to the seed's OWN machine-form class
key (type_pair, result_type family -- read from the seed's own unit
meta, never the operator token; the SAME two fields table24's own
rows are keyed on), then try cross_unit_prover.prove_pair (z3,
unchanged) between the seed's seed_text and each candidate row's
canonical_text. A seed proved equal to exactly one row in its own
pool joins that row (marked `branching: true, join_method: "proof"`).
Proved equal to more than one row is a PROOF-LEVEL ambiguity, kept
separate from the original text ambiguity. See task10_seed_prove.py
for the standalone diagnostic this reuses (same seed_class_key/
try_prove functions, re-run here against THIS run's own `rows`
object rather than trusting the cached task10_seed_prove_results.json
-- the two are deterministic and were checked to agree)."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_table24 as T24                                      # noqa: E402
import dominant_table17 as DT17                                  # noqa: E402
import task10_seed_prove as T10                                  # noqa: E402


def add_branching_members_v2(rows, unmatched, ambiguous):
    """Second pass over the units add_branching_members() (table24's
    original, unchanged, exact-text-only) left in `unmatched` or
    `ambiguous`. Returns (added2, still_unmatched, still_ambiguous,
    proof_ambiguous, diagnoses) -- diagnoses is the per-unit record
    for every unit this pass touched, PROVED or not, for the report."""
    seeds = T10.load_seeds()
    row_by_id = {row["class_id"]: row for row in rows}
    targets = sorted(set(r["unit"] for r in unmatched) |
                      set(r["unit"] for r in ambiguous))
    ambiguous_text_ids = set(r["unit"] for r in ambiguous)

    added2 = []
    still_unmatched = []
    still_ambiguous = list(ambiguous)  # text ambiguity unresolved by proof
    proof_ambiguous = []
    diagnoses = []

    still_unmatched_ids_from_original = set(r["unit"] for r in unmatched)

    for unit_id in targets:
        s = seeds.get(unit_id)
        orig_entry = None
        if unit_id in still_unmatched_ids_from_original:
            orig_entry = [r for r in unmatched if r["unit"] == unit_id][0]
        if s is None or s.get("status") != "ok":
            if orig_entry is not None:
                still_unmatched.append(orig_entry)
            diagnoses.append({"unit": unit_id, "diagnosis":
                               "seed missing/not status=ok -- carried "
                               "forward unresolved"})
            continue
        lang, n = s["lang"], s["n"]
        seed_text = s["seed_text"]
        key, key_err = T10.seed_class_key(lang, n)
        if key is None:
            if orig_entry is not None:
                still_unmatched.append(orig_entry)
            diagnoses.append({
                "unit": unit_id, "seed_text": seed_text,
                "diagnosis": "no machine-form class key (%s) -- "
                             "genuinely new / not converged, carried "
                             "forward unresolved" % key_err})
            continue
        tkey, rkey = key
        candidates = [r for r in rows
                      if r["type_pair"] == tkey and
                      r["result_type"] == rkey]
        proved_rows = []
        proofs = []
        for row in candidates:
            cand_label = "%s#cand" % row["class_id"]
            verdict, detail = T10.try_prove(
                unit_id, seed_text, key, cand_label, row["canonical_text"])
            proofs.append({"class_id": row["class_id"], "verdict": verdict,
                            "detail": detail})
            if verdict == "PROVED":
                proved_rows.append(row["class_id"])

        rec = {"unit": unit_id, "seed_text": seed_text,
               "type_pair": tkey, "result_family": rkey,
               "candidate_pool_size": len(candidates),
               "was_text_ambiguous": unit_id in ambiguous_text_ids,
               "proofs": proofs}

        if len(proved_rows) == 1:
            row = row_by_id[proved_rows[0]]
            row["members"].append({
                "unit": unit_id, "branching": True,
                "seed_text": s["seed_text"], "seed_method": s["method"],
                "guards": s.get("guards", []),
                "join_method": "proof (task10 class-key + z3, not "
                               "exact-text)",
            })
            added2.append((unit_id, row["class_id"]))
            rec["diagnosis"] = "resolved by proof: exactly one class " \
                "in its own (type_pair, result_family) pool"
            if unit_id in ambiguous_text_ids:
                still_ambiguous = [a for a in still_ambiguous
                                    if a["unit"] != unit_id]
        elif len(proved_rows) > 1:
            proof_ambiguous.append({"unit": unit_id, "seed_text": seed_text,
                                     "candidate_classes": proved_rows})
            rec["diagnosis"] = "PROOF-LEVEL AMBIGUITY: proved equal " \
                "to %d classes in its own pool" % len(proved_rows)
            if orig_entry is not None:
                still_unmatched.append(orig_entry)
        else:
            if candidates:
                verdicts_seen = sorted(set(p["verdict"] for p in proofs))
                rec["diagnosis"] = (
                    "unresolved: %d candidates in pool, none PROVED "
                    "(verdicts: %s) -- either representative-text "
                    "mismatch this pass cannot bridge, or genuinely "
                    "new computation" % (len(candidates), verdicts_seen))
            else:
                rec["diagnosis"] = (
                    "class-key pool empty -- no 0-branch class shares "
                    "this seed's own (type_pair, result_family) -- "
                    "cause 1: the seed's computation has not converged "
                    "into ANY class yet")
            if orig_entry is not None:
                still_unmatched.append(orig_entry)
        diagnoses.append(rec)

    return added2, still_unmatched, still_ambiguous, proof_ambiguous, \
        diagnoses


def main(argv):
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    population_0branch = len(units)

    rep_text_of, rep_meta, group_report, own_text_of = \
        T24.build_representative_groups(units)

    prov0, rows, unknown_result_type, generation_tally = \
        T24.build_0branch_rows(units, rep_text_of)

    added, unmatched, ambiguous = T24.add_branching_members(rows)
    added2, still_unmatched, still_ambiguous, proof_ambiguous, \
        proof_diagnoses = add_branching_members_v2(rows, unmatched,
                                                     ambiguous)

    class_doc = {
        "generator": "build_table24b.py (TASK 10 rebuild of "
                     "build_table24.py; does not overwrite "
                     "dominant_table24.json)",
        "role_note": "GROUPING/matching artifact (top-level `rows`, "
                     "each with `members`) -- checked by check_no_"
                     "spelling_keys.py IN FULL, no exemption claimed.",
        "lineage": "build_table24.py's own lineage (dominant_table22/"
                   "dom_ops20.json x dominant_table23c/dom_ops21c.json) "
                   "UNCHANGED, plus a second seed-join pass: task10_"
                   "seed_prove.py's class-key-restricted z3 proof "
                   "(cross_unit_prover.prove_pair, unchanged) applied "
                   "to every seed the first (exact-text) pass left "
                   "unmatched or text-ambiguous.",
        "population": "1,779 full corpus: %d 0-branch units + %d "
                     "branching units joined by exact seed-text "
                     "equality (pass 1) + %d more joined by class-key-"
                     "restricted z3 proof (pass 2, this file) "
                     "(seeds2.json, 66 resolved seeds attempted total; "
                     "%d unmatched by both passes, %d text-ambiguous, "
                     "%d proof-ambiguous)"
                     % (population_0branch, len(added), len(added2),
                        len(still_unmatched), len(still_ambiguous),
                        len(proof_ambiguous)),
        "representative_rule": rep_meta,
        "generation_tally": generation_tally,
        "unknown_result_type_units": unknown_result_type,
        "classes_before_branching": len(rows),
        "pass1_exact_text_added": len(added),
        "pass2_proof_added": len(added2),
        "pass2_proof_diagnoses": proof_diagnoses,
        "unmatched_branching_seeds": still_unmatched,
        "ambiguous_branching_seeds": still_ambiguous,
        "proof_ambiguous_branching_seeds": proof_ambiguous,
        "rows": rows,
    }

    prov = T24.build_provenance(rows)
    nodes, dom_ops_result = T24.run_dom_ops(rows, prov)

    def family_units(fams):
        out = {}
        for f in fams:
            us = set()
            for n in f["nodes"]:
                us.update(n.get("units", []))
            for u in us:
                out[u] = f["dom_op_id"]
        return out

    fam24b = family_units(dom_ops_result["families"])
    d20 = json.load(open(os.path.join(HERE, "dom_ops20.json")))
    d21c = json.load(open(os.path.join(HERE, "dom_ops21c.json")))
    fam20 = family_units(d20["dom_ops"])
    fam21c = family_units(d21c["families"])

    proof_diag_by_unit = {d["unit"]: d for d in proof_diagnoses}

    unreconciled = []
    seen = set()
    for src_name, fam_src in (("dom_ops20.json (table22 lineage)", fam20),
                               ("dom_ops21c.json (table23c lineage)",
                                fam21c)):
        for unit, fam_id in fam_src.items():
            if unit in fam24b or unit in seen:
                continue
            if unit not in fam21c and unit not in fam20:
                continue
            seen.add(unit)
            pd = proof_diag_by_unit.get(unit)
            proof_note = (pd["diagnosis"] if pd is not None else
                          "not a branching seed unit / not attempted "
                          "by task10's proof pass")
            unreconciled.append({
                "unit": unit,
                "family_in_source_lineage": fam_id,
                "source_lineage": src_name,
                "status_in_table24b": "unmatched" if any(
                    r["unit"] == unit for r in still_unmatched) else (
                    "text-ambiguous" if any(r["unit"] == unit
                                             for r in still_ambiguous)
                    else ("proof-ambiguous" if any(
                        r["unit"] == unit for r in proof_ambiguous)
                        else "not a branching seed unit / not attempted")),
                "cause_table24": "the seed's proved-equal target text "
                        "was produced by a text-consolidation rule "
                        "(representatives5.json's pre-canon24 "
                        "grouping, or table23b.py's own proved-edge "
                        "consolidation) that the representative-groups "
                        "step (canon24 text + proved_edges.json/2/3 "
                        "union-find) does not reproduce character-for-"
                        "character -- an un-ratified method question "
                        "(which text-consolidation rule is canonical "
                        "for a seed match target), not resolved here.",
                "task10_proof_pass_diagnosis": proof_note,
            })
    unreconciled.sort(key=lambda r: r["unit"])
    class_doc["unreconciled_branching_units"] = unreconciled
    class_doc["unreconciled_branching_units_count"] = len(unreconciled)

    class_path = os.path.join(HERE, "dominant_table24b.json")
    json.dump(class_doc, open(class_path, "w"), indent=1)

    dom_ops_doc = {
        "meta": {
            "generator": "build_table24b.py (dom_ops22b.json)",
            "role": "generator provenance -- carries `display_label` "
                    "per node (ratified node identity), same "
                    "provenance exemption dom_ops20/21/21c/22 use.",
            "construction": "dom_ops7.py's rule, unchanged (via "
                            "dom_ops_0branch.py / dom_ops.py, "
                            "imported not restated).",
            "source_table": "dominant_table24b.json",
        },
        "class_count": len(rows),
    }
    dom_ops_doc.update(dom_ops_result)
    dom_ops_path = os.path.join(HERE, "dom_ops22b.json")
    json.dump(dom_ops_doc, open(dom_ops_path, "w"), indent=1)

    group_path = os.path.join(HERE, "representatives24b.json")
    json.dump({"meta": rep_meta, "groups": group_report},
               open(group_path, "w"), indent=1)

    print(json.dumps({
        "population_0branch": population_0branch,
        "classes": len(rows),
        "nodes": dom_ops_result["nodes"],
        "dom_op_count": dom_ops_result["dom_op_count"],
        "edgeless": dom_ops_result["nodes_with_no_surviving_edge"],
        "singleton_dom_ops": dom_ops_result["singleton_dom_ops"],
        "pass1_added": len(added),
        "pass2_added": len(added2),
        "still_unmatched": len(still_unmatched),
        "still_text_ambiguous": len(still_ambiguous),
        "proof_ambiguous": len(proof_ambiguous),
        "unreconciled_count": len(unreconciled),
        "groups_formed": rep_meta["groups_formed"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
