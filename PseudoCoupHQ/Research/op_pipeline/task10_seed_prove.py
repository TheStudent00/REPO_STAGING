#!/usr/bin/env python3
"""task10_seed_prove.py -- TASK 10 mechanical extension.

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

WHAT THIS FILE DOES. dominant_table24.json's add_branching_members
step (build_table24.py) matches a seed to a class row by TEXT
EQUALITY only, against two pools (the row's representative text and
every 0-branch member's own raw text). 58 of 66 seeds hit no pool
member; 4 hit more than one. This file adds a THIRD pool: for each
unmatched/ambiguous seed, restrict candidates to rows sharing the
seed unit's OWN machine-form class key (type_pair, result-type
family -- the SAME two fields dom_ops_0branch.type_pair_of and
result_type_norm.class_family already key table24's rows on, read
from the seed's OWN unit meta, never from the operator token), then
try z3 proof (cross_unit_prover.prove_pair's own Sim8/Sim20/Sim20Cmp,
reused unchanged) between the seed's seed_text and each candidate
row's canonical_text. A seed proved equal to exactly one candidate
row's text joins that row, marked with the proof. Proved equal to
more than one row is reported as a PROOF-LEVEL ambiguity (not
resolved by preference). Proved equal to none, or refused/undecided
against all candidates, stays unmatched -- diagnosed, not silently
dropped.

Writes task10_seed_prove_results.json (the per-seed diagnosis, not a
grouping artifact itself -- build_table24b.py consumes it)."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops_0branch as DB                                     # noqa: E402
import result_type_norm as RTN                                   # noqa: E402
import cross_unit_prover as CUP                                  # noqa: E402


def load_table24():
    return json.load(open(os.path.join(HERE, "dominant_table24.json")))


def load_seeds():
    return json.load(open(os.path.join(HERE, "seeds2.json")))["seeds"]


CANON4_CACHE = {}


def canon4_unit(lang, n):
    if lang not in CANON4_CACHE:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        CANON4_CACHE[lang] = json.load(open(path))["units"]
    return CANON4_CACHE[lang].get(n)


def seed_class_key(lang, n):
    """(type_pair, family_key) for a seed's OWN unit, computed the
    SAME way build_table24.build_0branch_rows computes a 0-branch
    row's key -- machine-form only (meta's lhs_rep/rhs_rep + DWARF-
    derived result-type family), never the operator token."""
    u4 = canon4_unit(lang, n)
    if u4 is None:
        return None, "no canon4 record for %s/op_%s" % (lang, n)
    tkey = DB.type_pair_of(u4)
    fam, note = RTN.class_family(lang, n, u4.get("meta"))
    rkey = fam if fam is not None else ("unknown(%s)" % note[:40])
    return (tkey, rkey), None


def try_prove(seed_label, seed_text, seed_key, cand_label, cand_text):
    """Wrap cross_unit_prover.prove_pair for a (seed, candidate-row-
    text) pair sharing the seed's own machine-form class key."""
    text_of = {seed_label: seed_text, cand_label: cand_text}
    class_of = {seed_label: seed_key, cand_label: seed_key}
    if seed_text == cand_text:
        return "PROVED", "text-identical (should have matched at " \
            "build_table24.py's exact-text step already)"
    try:
        return CUP.prove_pair(seed_label, cand_label, text_of, class_of)
    except Exception as exc:                      # noqa: BLE001
        return "REFUSED", "prove_pair raised %r on this pair" % exc


def main():
    table24 = load_table24()
    rows = table24["rows"]
    seeds = load_seeds()

    unmatched_ids = set(r["unit"] for r in
                         table24["unmatched_branching_seeds"])
    ambiguous_ids = set(r["unit"] for r in
                         table24["ambiguous_branching_seeds"])
    targets = sorted(unmatched_ids | ambiguous_ids)

    results = []
    for unit_id in targets:
        s = seeds.get(unit_id)
        if s is None or s.get("status") != "ok":
            results.append({"unit": unit_id, "diagnosis":
                             "seed missing or not status=ok in "
                             "seeds2.json -- cannot re-attempt"})
            continue
        lang, n = s["lang"], s["n"]
        seed_text = s["seed_text"]
        key, key_err = seed_class_key(lang, n)
        if key is None:
            results.append({"unit": unit_id, "seed_text": seed_text,
                             "diagnosis": "no machine-form class key: "
                             "%s -- new-computation candidate, cannot "
                             "restrict a candidate pool" % key_err})
            continue
        tkey, rkey = key
        candidates = [r for r in rows
                      if r["type_pair"] == tkey and
                      r["result_type"] == rkey]
        proofs = []
        proved_rows = []
        for row in candidates:
            cand_label = "%s#cand" % row["class_id"]
            verdict, detail = try_prove(
                unit_id, seed_text, key, cand_label, row["canonical_text"])
            proofs.append({"class_id": row["class_id"],
                            "candidate_text": row["canonical_text"],
                            "verdict": verdict, "detail": detail})
            if verdict == "PROVED":
                proved_rows.append(row["class_id"])
        diag = {
            "unit": unit_id, "seed_text": seed_text,
            "type_pair": tkey, "result_family": rkey,
            "candidate_pool_size": len(candidates),
            "was_text_ambiguous": unit_id in ambiguous_ids,
            "proofs": proofs,
            "proved_class_ids": proved_rows,
        }
        if len(candidates) == 0:
            diag["diagnosis"] = (
                "class-key pool empty -- no 0-branch class shares "
                "this seed's own (type_pair, result_family); the "
                "seed's computation has not converged into ANY class "
                "yet (cause 1: not converged / genuinely new)")
        elif len(proved_rows) == 1:
            diag["diagnosis"] = "resolved: proved equal to exactly " \
                "one class in its own type/result pool"
        elif len(proved_rows) > 1:
            diag["diagnosis"] = (
                "PROOF-LEVEL AMBIGUITY: proved equal to %d classes "
                "in its own pool -- not resolved by preference order"
                % len(proved_rows))
        else:
            reasons = sorted(set(p["verdict"] for p in proofs))
            diag["diagnosis"] = (
                "unresolved: %d candidates in pool, none PROVED "
                "(verdicts seen: %s) -- representative-text mismatch "
                "or genuinely new computation, per-candidate detail "
                "carried above" % (len(candidates), reasons))
        results.append(diag)

    out = {
        "generator": "task10_seed_prove.py",
        "inputs": ["dominant_table24.json", "seeds2.json"],
        "method": "seed_class_key() restricts candidates to rows "
                  "sharing the seed's own machine-form (type_pair, "
                  "result_family) -- never the operator token -- then "
                  "cross_unit_prover.prove_pair (unchanged) attempts "
                  "z3 bit-level equality between seed_text and each "
                  "candidate row's canonical_text.",
        "targets_count": len(targets),
        "results": results,
    }
    out_path = os.path.join(HERE, "task10_seed_prove_results.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote %s (%d targets)" % (out_path, len(targets)))
    resolved = sum(1 for r in results if r.get("proved_class_ids") and
                   len(r["proved_class_ids"]) == 1)
    ambig = sum(1 for r in results
                if r.get("diagnosis", "").startswith("PROOF-LEVEL"))
    print("resolved(1 proof)=%d proof-ambiguous=%d of %d"
          % (resolved, ambig, len(results)))


if __name__ == "__main__":
    main()
