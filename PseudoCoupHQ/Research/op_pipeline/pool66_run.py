#!/usr/bin/env python3
"""pool66_run.py -- the driver that runs `pool.py` (node 0_3_5_7) over
CANON40 and `term66_store/`, and writes the pool, the families and the
exception families.

ROUND 15, TASK 83.  `pool65_run.py` is round 13's record and is not
edited; its `shape_families` is IMPORTED and called, not re-typed.

WHAT MOVED UNDER THIS BUILD, said out loud, because two things changed
at once and a reader must be able to tell them apart:

1. THE MEMBER SET.  canon40 proves 30,324 wrapped texts where canon39
   proved 30,432 (log_185 section 4.1).  The difference is 112 swift
   units the reference change of task 64 disproved on the layer-3
   route, less 4 swift units canon39 refused and canon40 proves.
2. THE LAYER-5 TEXTS.  Two independent changes: task 78's corrected
   destination rule, which changes what the ledger says and therefore
   what the term IS; and task 79's corrected normalizer, which changes
   how a proved term PRINTS.  Task 79's prediction (1,831 entries to
   1,813) isolates the second by holding the first fixed, so this
   build's own entry count is NOT that prediction and the difference
   is measured rather than explained away -- see
   `pool6_prediction_check.py`.

WRITES:
  the_pool6.json            the pool, three grounds, transitive closure
  the_pool6_bytes.json      the measured assembled bytes
  the_families6.json        the dom_op rule over the pool's entries
  exception_families6.json  the guard families REBUILT over this pool
  pool5_pool6_delta.json    every split and every merge, cause computed
  the_pool6_entry_E00029_successor_printed.txt   the worked entry

WHY THESE NUMBERS.  Numbered artifacts accumulate and a superseded
record is never edited, so each rebuild takes the next free number.

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
import pool65_run as P65                                         # noqa: E402


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write(name, document):
    path = os.path.join(HERE, name)
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    log("-- wrote %s" % name)


def print_entry(entries, wanted):
    """the worked entry, printed VERBATIM off the artifact just
    written, so the report quotes the object and not a paraphrase."""
    found = None
    for entry in entries:
        if entry["entry_id"] == wanted:
            found = entry
            break
    if found is None:
        return "the entry %s is not in this pool\n" % wanted
    lines = []
    lines.append("-- %s, printed verbatim off the_pool6.json"
                 % found["entry_id"])
    lines.append("")
    lines.append(json.dumps(found, indent=1, sort_keys=True))
    return "\n".join(lines) + "\n"


def successor_of(before_entries, after_entries, wanted):
    """THE SUCCESSOR of an entry is found by MEMBER SET, never by
    number: an entry id is stable only inside one numbered pool, so
    asking for `E00029` in the new pool would be asking a question
    about numbering.  The successor is the new entry holding the
    largest share of the old entry's members."""
    old = None
    for entry in before_entries:
        if entry["entry_id"] == wanted:
            old = entry
            break
    if old is None:
        return None, 0, 0
    names = set()
    for member in old["members"]:
        names.add(member["unit"])
    best = None
    best_shared = 0
    for entry in after_entries:
        mine = set()
        for member in entry["members"]:
            mine.add(member["unit"])
        shared = len(mine & names)
        if shared > best_shared:
            best = entry
            best_shared = shared
    return best, best_shared, len(names)


def main():
    log("-- intake")
    records = P.take_all("canon40")
    log("   units in the pool %d" % len(records))
    populations = {}
    for record in records:
        key = record.get("population")
        populations[key] = populations.get(key, 0) + 1
    log("   by arrival population %s"
        % json.dumps(populations, sort_keys=True))

    terms = P.read_terms("term66_store")
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
    write("the_pool6_bytes.json", sizes)

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
        "generator": "pool66_run.py, running pool.py",
        "node": "hq.research.compiler_graph.pool",
        "task": "TASK 83 -- the pool over canon40, on term66's own "
                "gate, three grounds",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL.  No "
                     "provenance carve-out is claimed and no `role` "
                     "field is declared anywhere in this document.",
        "population": "every unit canon40 proved: 30,324 of 31,078 "
                      "attempted (642 refused, 112 disproved on the "
                      "layer-3 route, not transcribed)",
        "intake": "canon40_wrapped_{c,cpp,go,rust,swift}.json, "
                  "canon40_interp.json, canon40_regen_store/*.json, "
                  "outcome WRAPPED_TEXT_PROVED only",
        "layer4_source": "term66_store/*.json -- task 83's own "
                         "artifacts, written by term.py against "
                         "reference.opcode_table over canon40's "
                         "ledgers, each verdict re-derived by gate.py "
                         "on both routes",
        "grounds": "layer-3 wrapped-text identity, layer-5 normalized "
                   "term identity among PROVED terms, and banked "
                   "proved edges; closed under transitivity",
        "brief_strict_count_note": "entries_under_the_brief_strict_"
                                   "rule is what the pool would be on "
                                   "layer-5 identity and proved edges "
                                   "alone.  It is RECORDED and used "
                                   "for nothing, per ROUND 10 RULINGS "
                                   "(1).",
        "supersedes_as_an_object": "the_pool5.json, which ran the same "
                                   "rule over canon39 and term65_store "
                                   "-- the round-13 gate.  It stays on "
                                   "disk, byte for byte, as the "
                                   "superseded record.",
        "two_changes_at_once": "canon40 changes WHICH units are members "
                               "and WHAT each term is; task 79's "
                               "corrected normalizer changes how a "
                               "proved term prints.  The prediction of "
                               "log_186 section 7 isolates the second; "
                               "pool6_prediction_check.py measures this "
                               "build against it.",
        "operator_note": "the operator field is a display label on the "
                         "member and is read by nothing",
    }
    write("the_pool6.json", {"meta": meta, "summary": summary,
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
    families = P65.shape_families(nodes, kept, components,
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
    write("the_families6.json", {
        "meta": {
            "generator": "pool66_run.py, running pool.Pool.families",
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
            "source_table": "the_pool6.json -- one population, every "
                            "language in the pool",
            "what_a_node_is": "(language, grammar-operator, arity) -- "
                              "the provenance of the probe inside ONE "
                              "language, never a cross-language token. "
                              "The label is a display field and is "
                              "read by nothing.",
            "supersedes_as_an_object": "the_families5.json, which ran "
                                       "the same rule over "
                                       "the_pool5.json.  It stays on "
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
    write("exception_families6.json", {
        "meta": {
            "generator": "pool66_run.py, running "
                         "pool.Pool.exception_families",
            "node": "hq.research.compiler_graph.pool."
                    "exception_families",
            "rule": "guard identity is the CONDITION TESTED and the "
                    "RESPONSE TAKEN together, never the condition "
                    "alone; grouped across languages",
            "population": "the guard rows of guards5.json whose unit "
                          "is a member of the_pool6.json",
            "source": "guards5.json, the_pool6.json",
            "role_note": "GROUPING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL.  No "
                         "provenance carve-out is claimed and no "
                         "`role` field is declared anywhere.",
            "why_this_number": "numbered artifacts accumulate and a "
                               "superseded record is never edited, so "
                               "the round-15 rebuild takes the next "
                               "free number after "
                               "exception_families5.json (task 65).",
            "supersedes_as_an_object": "exception_families5.json, "
                                       "rebuilt over the_pool5.json "
                                       "in task 65.  It stays on disk "
                                       "as the superseded record.",
            "excluded_head": P.EXCLUDED_HEAD,
            "rows_considered": rebuilt["rows_considered"],
            "rows_excluded": rebuilt["rows_excluded"],
            "rows_about_units_outside_the_pool":
                rebuilt["rows_about_units_outside_the_pool"],
        },
        "families": rebuilt["families"],
    })

    log("-- the delta against the_pool5.json")
    before = json.load(open(os.path.join(HERE, "the_pool5.json")))
    delta = pool.compare(before["entries"], entries)
    for split in delta["splits"]:
        split["cause"] = pool.cause_of_split(split["was_entry"],
                                             before["entries"],
                                             entries)
    for merge in delta["merges"]:
        merge["cause"] = pool.cause_of_merge(merge["entry"], entries)
    delta["meta"] = {
        "generator": "pool66_run.py, running pool.Pool.compare",
        "joined_on": "MEMBER SETS, never entry numbers -- a "
                     "renumbering is not a change",
        "before": "the_pool5.json (canon39, term65_store -- the "
                  "round-13 gate of record, task 64)",
        "after": "the_pool6.json (canon40, term66_store -- task 83's "
                 "own gate over canon40's ledgers)",
    }
    write("pool5_pool6_delta.json", delta)
    log("   splits %d, merges %d, units gone %d, units new %d"
        % (len(delta["splits"]), len(delta["merges"]),
           len(delta["units_no_longer_in_the_pool"]),
           len(delta["units_new_to_the_pool"])))

    successor, shared, was_size = successor_of(before["entries"],
                                               entries, "E00029")
    printed = []
    printed.append("E00029's SUCCESSOR IN the_pool6.json")
    printed.append("")
    printed.append("The successor is found by MEMBER SET, never by "
                   "number: an entry id is stable only inside one")
    printed.append("numbered pool.  pool5's E00029 held %d members; "
                   "the pool6 entry holding the largest" % was_size)
    printed.append("share of them shares %d of those members."
                   % shared)
    printed.append("")
    if successor is None:
        printed.append("no pool6 entry shares a member with pool5's "
                       "E00029")
    else:
        printed.append(print_entry(entries, successor["entry_id"]))
    handle = open(os.path.join(
        HERE, "the_pool6_entry_E00029_successor_printed.txt"), "w")
    handle.write("\n".join(printed) + "\n")
    handle.close()
    log("-- wrote the_pool6_entry_E00029_successor_printed.txt")
    if successor is not None:
        log("   E00029's successor is %s: %d members, %d languages, "
            "representative %s"
            % (successor["entry_id"], len(successor["members"]),
               len(successor["languages"]),
               successor["representative"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
