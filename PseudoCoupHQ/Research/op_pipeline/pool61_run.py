#!/usr/bin/env python3
"""pool61_run.py -- the driver that runs `pool.py` (node 0_3_5_7) over
canon39 and `term61_store/`, and writes the pool, the families and the
exception families.

WRITES:
  the_pool4.json           the pool, three grounds, transitive closure
  the_pool4_bytes.json     the measured assembled bytes
  the_families4.json       the dom_op rule over the pool's entries
  exception_families4.json the guard families REBUILT over this pool
  pool3_pool4_delta.json   every split and every merge, cause computed

WHY `exception_families4` AND NOT `exception_families3`.  The name
`exception_families3.json` is already taken on disk, by the round-5
line's own later build over `guards5.json` (2026-09-01); the
exception_families CORE's realization table records it.  A superseded
record is never edited, and pools accumulate by number, so the rebuild
is the NEXT number.  The correction is written into the CORE and the
node PROGRESS with this provenance.

ONE PROCESS.  Everything below runs in this single process.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pool as P                                                 # noqa: E402


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write(name, document):
    path = os.path.join(HERE, name)
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    log("-- wrote %s" % name)


def main():
    log("-- intake")
    records = P.take_all("canon39")
    log("   units in the pool %d" % len(records))
    populations = {}
    for record in records:
        key = record.get("population")
        populations[key] = populations.get(key, 0) + 1
    log("   by arrival population %s"
        % json.dumps(populations, sort_keys=True))

    terms = P.read_terms("term61_store")
    log("   layer-4 records read %d" % len(terms))
    missing = []
    for record in records:
        if record["unit"] not in terms:
            missing.append(record["unit"])
    if missing:
        raise SystemExit(
            "REFUSED OWN OUTPUT: %d proved units have no layer-4 "
            "record, first %s" % (len(missing), missing[:3]))

    pool = P.Pool(records, terms)

    log("-- the merge, brief-strict: layer-5 identity and proved edges "
        "only (RECORDED, NOT USED)")
    strict, _edges, strict_stats = pool.merge(use_layer3_identity=False)
    strict_roots = set()
    for label in pool.order:
        strict_roots.add(strict.find(label))
    log("   entries under the brief-strict rule %d" % len(strict_roots))

    log("-- the merge, as ruled: layer-5 identity, layer-3 identity, "
        "proved edges")
    joiner, edges, stats = pool.merge(use_layer3_identity=True)
    for key in sorted(stats):
        log("   %-46s %d" % (key, stats[key]))
    groups, roots = pool.groups_of(joiner)
    log("   entries %d" % len(roots))

    log("-- the representative rule")
    multi_text = set()
    multi_entries = 0
    for root in roots:
        texts = set()
        for label in groups[root]:
            texts.add(pool.by_label[label]["wrapped_text"])
        if len(texts) > 1:
            multi_text.update(texts)
            multi_entries = multi_entries + 1
    log("   entries carrying more than one wrapped text %d"
        % multi_entries)
    log("   distinct texts to assemble %d" % len(multi_text))
    cache = P.load_byte_cache()
    sizes = P.measure_bytes(sorted(multi_text), cache)
    write("the_pool4_bytes.json", sizes)

    entries = pool.build_entries(joiner, edges, sizes)

    term_state = {"TERM": 0, "NO_TERM": 0}
    proved = 0
    withdrawn = 0
    undecided = 0
    ineligible = 0
    for label in pool.order:
        record = terms[label]
        state = record.get("term_state")
        term_state[state] = term_state.get(state, 0) + 1
        if not pool.eligibility[label][0]:
            ineligible = ineligible + 1
        if state != "TERM":
            continue
        if record.get("proved"):
            proved = proved + 1
            continue
        if record.get("outcome") == "DISPROVED":
            withdrawn = withdrawn + 1
            continue
        undecided = undecided + 1

    summary = {
        "entries": len(entries),
        "members": len(records),
        "entries_spanning_more_than_one_language":
            len([one for one in entries
                 if one["spans_more_than_one_language"]]),
        "entries_spanning_compiled_and_interpreted":
            len([one for one in entries
                 if one["spans_compiled_and_interpreted"]]),
        "entries_under_the_brief_strict_rule": len(strict_roots),
        "entries_carrying_more_than_one_wrapped_text": multi_entries,
        "members_with_a_proved_term": proved,
        "members_whose_term_was_withdrawn": withdrawn,
        "members_whose_term_was_undecided": undecided,
        "members_with_no_term": term_state["NO_TERM"],
        "members_not_layer5_eligible": ineligible,
    }
    for key in sorted(stats):
        summary[key] = stats[key]

    meta = {
        "generator": "pool61_run.py, running pool.py",
        "node": "hq.research.compiler_graph.pool",
        "task": "TASK 61 -- the pool over canon39, three grounds",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL.  No "
                     "provenance carve-out is claimed and no `role` "
                     "field is declared anywhere in this document.",
        "population": "every unit canon39 proved: 30,432 of 31,078 "
                      "attempted (646 refused, not transcribed)",
        "intake": "canon39_wrapped_{c,cpp,go,rust,swift}.json, "
                  "canon39_interp.json, canon39_regen_store/*.json, "
                  "outcome WRAPPED_TEXT_PROVED only",
        "layer4_source": "term61_store/*.json -- task 61's own "
                         "artifacts, written by term.py against "
                         "reference.opcode_table",
        "grounds": "layer-3 wrapped-text identity, layer-5 normalized "
                   "term identity among PROVED terms, and banked "
                   "proved edges; closed under transitivity",
        "brief_strict_count_note": "entries_under_the_brief_strict_"
                                   "rule is what the pool would be on "
                                   "layer-5 identity and proved edges "
                                   "alone.  It is RECORDED and used "
                                   "for nothing, per ROUND 10 RULINGS "
                                   "(1).",
        "supersedes_as_an_object": "the_pool3.json, which ran the same "
                                   "rule over canon38 and layer4c.  It "
                                   "stays on disk, byte for byte, as "
                                   "the superseded record.",
        "operator_note": "the operator field is a display label on the "
                         "member and is read by nothing",
    }
    write("the_pool4.json", {"meta": meta, "summary": summary,
                             "entries": entries})
    log(json.dumps(summary, indent=1, sort_keys=True))

    log("-- the families (the dom_op rule, imported from dom_ops.py)")
    built = pool.families()
    nodes = built["nodes"]
    kept = built["edges_mutual"]
    components = built["components"]
    log("   nodes (language, grammar-operator, arity) %d" % len(nodes))
    log("   cross-language edges, raw %d" % len(built["edges_raw"]))
    log("   edges surviving the mutual filter %d" % len(kept))
    log("   families %d" % len(components))
    families = shape_families(nodes, kept, components,
                              built["provenance"])
    attached = set()
    for members in components:
        for one in members:
            attached.add(one)
    unattached = []
    for one in sorted(nodes.keys()):
        if one in attached:
            continue
        unattached.append({
            "id": one,
            "lang": nodes[one]["lang"],
            "label": nodes[one]["label"],
            "arity": nodes[one]["arity"],
            "entry_count": len(nodes[one]["classes"]),
            "unit_count": len(nodes[one]["units"]),
        })
    families_summary = {
        "entry_count": len(entries),
        "unit_count": len(records),
        "nodes": len(nodes),
        "edges_raw": len(built["edges_raw"]),
        "edges_mutual": len(kept),
        "families": len(families),
        "nodes_in_a_family": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "equally_strongest_ties": len(built["equally_strongest_ties"]),
    }
    write("the_families4.json", {
        "meta": {
            "generator": "pool61_run.py, running pool.Pool.families",
            "node": "hq.research.compiler_graph.pool.families",
            "role_note": "GROUPING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL.  No "
                         "provenance carve-out is claimed and no "
                         "`role` field is declared anywhere.",
            "construction": "THE DOM_OP CONSTRUCTION RULE, unchanged, "
                            "imported from dom_ops.py (build_nodes, "
                            "fill_nodes, build_edges, "
                            "best_per_language, mutual_edges, "
                            "components)",
            "source_table": "the_pool4.json -- one population, every "
                            "language in the pool",
            "what_a_node_is": "(language, grammar-operator, arity) -- "
                              "the provenance of the probe inside ONE "
                              "language, never a cross-language token. "
                              "The label is a display field and is "
                              "read by nothing.",
            "supersedes_as_an_object": "the_families3.json, which ran "
                                       "the same rule over "
                                       "the_pool3.json.  It stays on "
                                       "disk as the superseded record.",
        },
        "summary": families_summary,
        "families": families,
        "unattached_nodes": unattached,
        "equally_strongest_ties": built["equally_strongest_ties"],
    })
    log(json.dumps(families_summary, indent=1, sort_keys=True))

    log("-- the exception families, rebuilt over this pool")
    guards = json.load(open(os.path.join(HERE, "guards5.json")))
    rebuilt = pool.exception_families(guards["rows"])
    log("   guard rows read %d" % len(guards["rows"]))
    log("   rows considered %d" % rebuilt["rows_considered"])
    log("   rows excluded (%s) %d"
        % (P.EXCLUDED_HEAD, rebuilt["rows_excluded"]))
    log("   rows about units outside this pool %d"
        % len(rebuilt["rows_about_units_outside_the_pool"]))
    log("   exception families %d" % len(rebuilt["families"]))
    write("exception_families4.json", {
        "meta": {
            "generator": "pool61_run.py, running "
                         "pool.Pool.exception_families",
            "node": "hq.research.compiler_graph.pool."
                    "exception_families",
            "rule": "guard identity is the CONDITION TESTED and the "
                    "RESPONSE TAKEN together, never the condition "
                    "alone; grouped across languages",
            "population": "the guard rows of guards5.json whose unit "
                          "is a member of the_pool4.json",
            "source": "guards5.json, the_pool4.json",
            "role_note": "GROUPING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL.  No "
                         "provenance carve-out is claimed and no "
                         "`role` field is declared anywhere.",
            "why_this_number": "exception_families3.json is taken on "
                               "disk by the round-5 line's own later "
                               "build over guards5.json (2026-09-01), "
                               "recorded in the exception_families "
                               "CORE's realization table.  A "
                               "superseded record is never edited, so "
                               "the rebuild takes the next number.",
            "supersedes_as_an_object": "exception_families2.json "
                                       "(round 5) and "
                                       "exception_families3.json, "
                                       "neither of which was read "
                                       "against a pool.  Both stay on "
                                       "disk as superseded records.",
            "excluded_head": P.EXCLUDED_HEAD,
            "rows_considered": rebuilt["rows_considered"],
            "rows_excluded": rebuilt["rows_excluded"],
            "rows_about_units_outside_the_pool":
                rebuilt["rows_about_units_outside_the_pool"],
        },
        "families": rebuilt["families"],
    })

    log("-- the delta against the_pool3.json")
    before = json.load(open(os.path.join(HERE, "the_pool3.json")))
    delta = pool.compare(before["entries"], entries)
    for split in delta["splits"]:
        split["cause"] = pool.cause_of_split(split["was_entry"],
                                             before["entries"],
                                             entries)
    for merge in delta["merges"]:
        merge["cause"] = pool.cause_of_merge(merge["entry"], entries)
    delta["meta"] = {
        "generator": "pool61_run.py, running pool.Pool.compare",
        "joined_on": "MEMBER SETS, never entry numbers -- a "
                     "renumbering is not a change",
        "before": "the_pool3.json (canon38, layer4c)",
        "after": "the_pool4.json (canon39, term61_store)",
    }
    write("pool3_pool4_delta.json", delta)
    log("   splits %d, merges %d, units gone %d, units new %d"
        % (len(delta["splits"]), len(delta["merges"]),
           len(delta["units_no_longer_in_the_pool"]),
           len(delta["units_new_to_the_pool"])))
    return 0


def shape_families(nodes, kept, components, provenance):
    """the families, written out.  COPIED IN SHAPE from
    `build_the_families2.py` (a superseded record, neither edited nor
    imported)."""
    families = []
    number = 0
    for members in components:
        number = number + 1
        langs = []
        out_nodes = []
        for one in members:
            node = nodes[one]
            if node["lang"] not in langs:
                langs.append(node["lang"])
            out_nodes.append({
                "id": one,
                "lang": node["lang"],
                "label": node["label"],
                "arity": node["arity"],
                "arity_source":
                    provenance[node["units"][0]]["arity_source"],
                "entry_count": len(node["classes"]),
                "unit_count": len(node["units"]),
                "units": sorted(node["units"])[:12],
                "units_listed": min(12, len(node["units"])),
            })
        joins = []
        for key in sorted(kept.keys()):
            if key[0] not in members:
                continue
            if key[1] not in members:
                continue
            record = kept[key]
            joins.append({
                "left": key[0],
                "right": key[1],
                "shared_entries": record["weight_classes"],
                "shared_shape_keys": record["weight_type_keys"],
            })
        families.append({
            "family_id": "F%04d" % number,
            "size": len(members),
            "languages": sorted(langs),
            "language_count": len(langs),
            "nodes": out_nodes,
            "mutual_best_joins": joins,
        })
    return families


if __name__ == "__main__":
    sys.exit(main())
