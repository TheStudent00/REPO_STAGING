#!/usr/bin/env python3
"""build_table25.py -- TASK 39 step 4: the class table REBUILT on the
universal-form text.  dominant_table25.json / dom_ops23.json.

WHAT CHANGES FROM build_table24.py, and what deliberately does not.

CHANGES -- exactly one thing: the TEXT.  Every 0-branch unit's class
key text is now its universal-form text (canon35_universal_<lang>
.json, `universal_text`), not its register-first canonical text.  That
is the point of the lap: the universal texts REPLACE the register-
first texts as the canonical column.

UNCHANGED, so that the two tables are comparable at all:
  * the POPULATION rule -- dominant_table17.load_0branch_units with
    canon24 prepended to the generation order, the same 1,641 units;
  * the REPRESENTATIVE RULE and its three grounds (a) newest text
    character-identical, (b) normal_path_raw3 constant-substituted
    split by type pair and result type, (c) proved_edges.json UNION 2
    UNION 3 -- build_table24.build_representative_groups, IMPORTED,
    not copied, so it cannot drift;
  * the class key shape (type_pair, result_type, text);
  * dom_ops7's rule for nodes, edges and families, via dom_ops.py /
    dom_ops_0branch.py, imported unchanged.

THE ARRIVAL ANNOTATION is carried on every row as RECORDED DATA
(`arrival_annotations`, the set its members carry) and is deliberately
NOT part of the class key.  Reason, and it is the ruling's own: the
whole purpose of the universal form is that a pointer-arriving unit
and a plain-arriving unit MEET on the same memory-based form; putting
the arrival back in the key would re-create the separate dialects the
ruling dissolves.  This is the same choice interp_table2.json made and
the owner accepted (log_124 section 4.1).  Rows whose members disagree on
arrival are counted (`rows_with_more_than_one_arrival`) because "same
instructions, different modes is a finding to record" is a standing
instruction.

A UNIT WITH NO UNIVERSAL TEXT is left OUT of the table and named in
`units_without_a_universal_text`, with the cause canon35_universal
recorded.  It is never carried in on its old text: a table keyed on
the universal form must not contain a row keyed on something else.

THE BRANCHING SEEDS.  seeds2.json's seed texts are register-form
texts, written before this lap existed.  They are matched against a
pool that carries, per row: the representative's universal text, each
member's own universal text, AND each member's PRIOR register-form
text.  The third pool is what keeps table24's four seed joins alive
without inventing a universal render for a seed text nobody has
gated.  Every match records which pool it came from
(`matched_against`), so a reader can see exactly which joins rest on
the register-form pool.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

dominant_table25.json is checked IN FULL, no exemption.  dom_ops23
.json carries `display_label` per node (ratified node identity) and
uses the SAME generator-provenance exemption dom_ops20/21/21c/22 use.

Coding discipline: no complex/compound one-liner statements.

usage:
  build_table25.py [--out DIR]
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table17 as DT17                                  # noqa: E402
import dom_ops as DO                                             # noqa: E402
import dom_ops_0branch as DB                                     # noqa: E402
import result_type_norm as RTN                                   # noqa: E402

DT17.GENERATIONS = ["canon24"] + DT17.GENERATIONS
DT17.BRANCH_CHECK_GENERATIONS = tuple(
    ["canon24"] + list(DT17.BRANCH_CHECK_GENERATIONS))

import build_table24 as T24                                      # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def universal_records():
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon35_universal_%s.json" % lang)
        out.update(json.load(open(path))["units"])
    return out


def substitute_universal(units, universal):
    """(kept units with the universal text, the ones left out)."""
    kept = []
    left_out = []
    for lang, n, u, text, _gen in units:
        label = "%s/op_%s" % (lang, n)
        record = universal.get(label) or {}
        new_text = record.get("universal_text")
        if not new_text:
            reason = record.get("refusal")
            if reason is None:
                reason = record.get("gate_detail")
            left_out.append({
                "unit": label,
                "outcome": record.get("outcome"),
                "cause": reason,
            })
            continue
        kept.append((lang, n, u, new_text, "canon35(universal)"))
    return kept, left_out


def build_rows(units, rep_text_of, universal):
    prov = {}
    classes = {}
    unknown_result_type = 0
    for lang, n, u, text, _gen in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        tkey = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        if fam is not None:
            rkey = fam
        else:
            rkey = "unknown(%s)" % note[:40]
            unknown_result_type = unknown_result_type + 1
        rep_text = rep_text_of.get(label, text)
        ckey = (tkey, rkey, rep_text)
        classes.setdefault(ckey, {"type_pair": tkey, "text": rep_text,
                                  "members": []})
        record = universal.get(label) or {}
        classes[ckey]["members"].append({
            "unit": label,
            "own_text_before_representative_substitution": text,
            "prior_register_form_text": record.get("prior_text"),
            "arrival_annotation": record.get("arrival_annotation"),
            "admitted_by": record.get("admitted_by"),
        })
    rows = []
    index = 0
    for ckey in sorted(classes.keys()):
        index = index + 1
        rec = classes[ckey]
        arrivals = []
        for member in rec["members"]:
            arrivals.append(member.get("arrival_annotation"))
        rows.append({
            "class_id": "C%04d" % index,
            "type_pair": rec["type_pair"],
            "result_type": ckey[1],
            "canonical_text": rec["text"],
            "arrival_annotations": sorted(set(
                [x for x in arrivals if x is not None])),
            "members": rec["members"],
        })
    return prov, rows, unknown_result_type


def add_branching_members(rows):
    seeds = json.load(open(os.path.join(HERE, "seeds2.json")))["seeds"]
    pools = {}

    def add_text(text, class_id, pool_name):
        if text is None:
            return
        entry = pools.setdefault(text, {})
        entry.setdefault(class_id, set()).add(pool_name)

    row_by_id = {}
    for row in rows:
        row_by_id[row["class_id"]] = row
        add_text(row["canonical_text"], row["class_id"],
                 "the representative's universal text")
        for member in row["members"]:
            add_text(member.get(
                "own_text_before_representative_substitution"),
                row["class_id"], "a member's own universal text")
            add_text(member.get("prior_register_form_text"),
                     row["class_id"],
                     "a member's prior register-form text")

    added = []
    unmatched = []
    ambiguous = []
    for unit_id in sorted(seeds):
        seed = seeds[unit_id]
        if seed.get("status") != "ok":
            continue
        seed_text = seed.get("seed_text")
        hits = pools.get(seed_text) or {}
        candidate_ids = sorted(hits)
        if len(candidate_ids) == 0:
            unmatched.append({"unit": unit_id, "seed_text": seed_text})
            continue
        if len(candidate_ids) > 1:
            ambiguous.append({"unit": unit_id, "seed_text": seed_text,
                              "candidate_classes": candidate_ids})
            continue
        class_id = candidate_ids[0]
        row = row_by_id[class_id]
        row["members"].append({
            "unit": unit_id,
            "branching": True,
            "seed_text": seed["seed_text"],
            "seed_method": seed["method"],
            "guards": seed.get("guards", []),
            "matched_against": sorted(hits[class_id]),
        })
        added.append({"unit": unit_id, "class_id": class_id,
                      "matched_against": sorted(hits[class_id])})
    return added, unmatched, ambiguous


def refuse_own_output_on_spelling_keys(path, exemption=False):
    command = [sys.executable,
               os.path.join(HERE, "check_no_spelling_keys.py"), path]
    # the exemption, where it applies, is declared by the file's own
    # top-level meta role and recognised by the checker itself; there
    # is no flag to pass and none is passed.
    proc = subprocess.run(command, capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr.strip())
        raise SystemExit("REFUSING OWN OUTPUT: %s" % path)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args(argv)

    gen_docs = DT17.load_generation_docs()
    units_before = DT17.load_0branch_units(gen_docs)
    universal = universal_records()
    units, left_out = substitute_universal(units_before, universal)

    rep_text_of, rep_meta, group_report, _own = \
        T24.build_representative_groups(units)

    prov0, rows, unknown_result_type = build_rows(units, rep_text_of,
                                                  universal)
    added, unmatched, ambiguous = add_branching_members(rows)

    multi_arrival = []
    for row in rows:
        if len(row["arrival_annotations"]) > 1:
            multi_arrival.append(row["class_id"])

    class_doc = {
        "generator": "build_table25.py",
        "role_note": "GROUPING/matching artifact (top-level `rows`, "
                     "each with `members`) -- checked by "
                     "check_no_spelling_keys.py IN FULL, no exemption "
                     "claimed.",
        "lineage": "dominant_table24.json's own population, "
                   "representative rule and class-key shape, with the "
                   "UNIVERSAL-FORM text (canon35_universal_<lang>"
                   ".json) replacing the register-first canonical "
                   "text as the class key's text component.",
        "population": "1,779 full corpus: %d 0-branch units offered, "
                      "%d carrying a universal text and keyed here, "
                      "%d left out and named; plus %d branching units "
                      "joined by seed-text equality (seeds2.json, %d "
                      "matched, %d unmatched, %d ambiguous)"
                      % (len(units_before), len(units), len(left_out),
                         len(added), len(added), len(unmatched),
                         len(ambiguous)),
        "units_without_a_universal_text": left_out,
        "representative_rule": rep_meta,
        "unknown_result_type_units": unknown_result_type,
        "classes_before_branching": len(rows),
        "rows_with_more_than_one_arrival": multi_arrival,
        "branching_seed_joins": added,
        "unmatched_branching_seeds": unmatched,
        "ambiguous_branching_seeds": ambiguous,
        "rows": rows,
    }

    prov = T24.build_provenance(rows)
    nodes, dom_ops_result = T24.run_dom_ops(rows, prov)

    class_path = os.path.join(args.out, "dominant_table25.json")
    fh = open(class_path, "w")
    json.dump(class_doc, fh, indent=1)
    fh.close()

    dom_ops_doc = {
        "meta": {
            "generator": "build_table25.py (dom_ops23.json)",
            "role": "generator provenance -- carries `display_label` "
                    "per node (ratified node identity), same "
                    "provenance exemption dom_ops20/21/21c/22 use.",
            "construction": "dom_ops7.py's rule, unchanged (via "
                            "dom_ops_0branch.py / dom_ops.py, "
                            "imported not restated).",
            "source_table": "dominant_table25.json",
        },
        "class_count": len(rows),
    }
    dom_ops_doc.update(dom_ops_result)
    dom_ops_path = os.path.join(args.out, "dom_ops23.json")
    fh = open(dom_ops_path, "w")
    json.dump(dom_ops_doc, fh, indent=1)
    fh.close()

    group_path = os.path.join(args.out, "representatives25.json")
    fh = open(group_path, "w")
    json.dump({"meta": rep_meta, "groups": group_report}, fh, indent=1)
    fh.close()

    refuse_own_output_on_spelling_keys(class_path, False)
    refuse_own_output_on_spelling_keys(dom_ops_path, True)

    print(json.dumps({
        "0branch_offered": len(units_before),
        "0branch_keyed": len(units),
        "0branch_left_out": len(left_out),
        "classes": len(rows),
        "nodes": dom_ops_result["nodes"],
        "families": dom_ops_result["dom_op_count"],
        "edgeless_nodes": dom_ops_result["nodes_with_no_surviving_edge"],
        "branching_joined": len(added),
        "rows_with_more_than_one_arrival": len(multi_arrival),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
