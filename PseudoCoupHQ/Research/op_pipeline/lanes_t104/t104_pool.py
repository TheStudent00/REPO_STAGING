#!/usr/bin/env python3
"""t104_pool.py -- the pool rebuilt over the NEW layer-5 texts, and the
same pool rebuilt over the OLD ones, so the difference between them is
the normalizer's and nothing else's.

WHAT IS HELD FIXED.  Both builds use the same member set (`take_all`
over canon40), the same three merge grounds, and the same code --
`pool.Pool.merge(use_layer3_identity=True)`, which is the merge
`pool66_run.py` calls "as ruled".  The ONLY difference between the two
builds is which store the layer-5 texts are read from:
`term66_store/` for the before, `term104_store/` for the after.

WHY NOT `pool66_run.py` ITSELF.  `pool66_run.py` refuses its own
output when a proved unit has no layer-4 record, and 44 units have
none (log_202 section 4.3).  That refusal is why `the_pool6.json` does
not exist and it is NOT worked around here: the lane runs
`pool66_run.py` unmodified first and the report pastes its refusal.
What this program writes is a CANDIDATE, named as one, carrying the
44-unit shortfall in its own summary -- never `the_pool6.json`.

THE t100 EDGES.  `pool100_edges.json` holds the cross-entry proofs task
t100 ran over pool5's entries: 12 applied and 214 proved-but-not-
applied.  Each edge names the two entries' representative units.  For
each edge this program asks the question the brief asks: do those two
units carry the SAME layer-5 text -- before, and after?

MEMORY: the two term stores (30,280 short records each), the canon40
member records, and `pool100_edges.json`.  Hard cap 6 GB with the named
abort ABORT_MEMORY_T104, checked at each stage.

WRITES: pool104_candidate.json, pool104_delta.json

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

No operator token appears in this file.  A member's `operator` field
travels on the member row as a DISPLAY LABEL, exactly as `pool.py`
puts it there, and nothing here reads it.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

import pool as P                                                 # noqa: E402

CANDIDATE = os.path.join(PIPELINE, "pool104_candidate.json")
DELTA = os.path.join(PIPELINE, "pool104_delta.json")
EDGES = os.path.join(PIPELINE, "pool100_edges.json")
CAP_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    used = peak_kb()
    if used > CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: peak resident %d kB passed the stated "
            "cap of %d kB at %s" % (used, CAP_KB, where))
    return used


def build(records, terms, label):
    """the ruled merge over one store's texts -> (groups, roots, the
    union-find, the edges, the stats)."""
    pool = P.Pool(records, terms)
    joiner, edges, stats = pool.merge(use_layer3_identity=True)
    groups, roots = pool.groups_of(joiner)
    sys.stdout.write("   %-8s entries %d\n" % (label, len(roots)))
    for key in sorted(stats):
        sys.stdout.write("   %-8s %-46s %d\n" % (label, key,
                                                 stats[key]))
    sys.stdout.flush()
    return pool, joiner, groups, roots, edges, stats


def member_sets(groups, roots):
    out = []
    for root in roots:
        out.append(frozenset(groups[root]))
    return out


def delta_of(before_sets, after_sets):
    """every group of the before build that is not a group of the after
    build, and the other way round, matched by member set."""
    before = set(before_sets)
    after = set(after_sets)
    only_before = sorted(before - after, key=lambda s: (-len(s),
                                                        sorted(s)[0]))
    only_after = sorted(after - before, key=lambda s: (-len(s),
                                                       sorted(s)[0]))
    return only_before, only_after


def edge_answer(before_texts, after_texts, eligible_before,
                eligible_after):
    """for every t100 edge -- BOTH populations `pool100_edges.json`
    carries, `edges` (the 12 t100 applied) and `proved_but_not_applied`
    (the 214 t100 proved-but-not-applied) -- do the two representatives
    carry one layer-5 text, before and after?

    FIX (2026-09-07, this closer): the first version of this function
    read only `document["edges"]`, so `proved_but_not_applied_edges`
    stayed 0 no matter what the 214-entry population did -- the field
    was declared and never fed.  Both arrays carry the identical row
    shape (`state`, `edge_applies`, `rep_a`, `rep_b`, ...), so both are
    walked here, distinguished by their own `edge_applies` field, never
    by which array they came from."""
    document = json.load(open(EDGES))
    rows = []
    counts = {
        "edges_read": 0,
        "applied_edges": 0,
        "proved_but_not_applied_edges": 0,
        "applied_that_merge_by_text_before": 0,
        "applied_that_merge_by_text_after": 0,
        "not_applied_that_merge_by_text_before": 0,
        "not_applied_that_merge_by_text_after": 0,
        "edges_with_a_representative_missing_a_text": 0,
    }
    both = list(document.get("edges") or [])
    both.extend(document.get("proved_but_not_applied") or [])
    for edge in both:
        if edge.get("state") != "PROVED":
            continue
        counts["edges_read"] = counts["edges_read"] + 1
        applied = bool(edge.get("edge_applies"))
        if applied:
            counts["applied_edges"] = counts["applied_edges"] + 1
        else:
            counts["proved_but_not_applied_edges"] = (
                counts["proved_but_not_applied_edges"] + 1)
        left = edge.get("rep_a")
        right = edge.get("rep_b")
        ok_before = eligible_before.get(left, False)
        ok_before = ok_before and eligible_before.get(right, False)
        ok_after = eligible_after.get(left, False)
        ok_after = ok_after and eligible_after.get(right, False)
        text_left_before = before_texts.get(left)
        text_right_before = before_texts.get(right)
        text_left_after = after_texts.get(left)
        text_right_after = after_texts.get(right)
        if text_left_before is None or text_right_before is None:
            counts["edges_with_a_representative_missing_a_text"] = (
                counts["edges_with_a_representative_missing_a_text"]
                + 1)
        same_before = False
        if ok_before:
            same_before = text_left_before == text_right_before
        same_after = False
        if ok_after:
            same_after = text_left_after == text_right_after
        if applied:
            if same_before:
                counts["applied_that_merge_by_text_before"] = (
                    counts["applied_that_merge_by_text_before"] + 1)
            if same_after:
                counts["applied_that_merge_by_text_after"] = (
                    counts["applied_that_merge_by_text_after"] + 1)
        else:
            if same_before:
                counts["not_applied_that_merge_by_text_before"] = (
                    counts["not_applied_that_merge_by_text_before"]
                    + 1)
            if same_after:
                counts["not_applied_that_merge_by_text_after"] = (
                    counts["not_applied_that_merge_by_text_after"]
                    + 1)
        rows.append({
            "pool5_entry_a": edge.get("a"),
            "pool5_entry_b": edge.get("b"),
            "representative_a": left,
            "representative_b": right,
            "edge_applied_by_t100": applied,
            "one_text_before": same_before,
            "one_text_after": same_after,
            "text_a_after": text_left_after,
            "text_b_after": text_right_after,
        })
    document = None
    return rows, counts


def main():
    started = time.time()
    sys.stdout.write("[1/6] the member set, canon40\n")
    sys.stdout.flush()
    records = P.take_all("canon40")
    sys.stdout.write("   members %d\n" % len(records))
    sys.stdout.flush()
    check_memory("intake")

    sys.stdout.write("[2/6] the two stores\n")
    sys.stdout.flush()
    before_terms = P.read_terms("term66_store")
    after_terms = P.read_terms("term104_store")
    sys.stdout.write("   term66_store records %d, term104_store "
                     "records %d\n"
                     % (len(before_terms), len(after_terms)))
    sys.stdout.flush()
    short = []
    for record in records:
        if record["unit"] not in after_terms:
            short.append(record["unit"])
    sys.stdout.write("   proved members with no layer-4 record %d\n"
                     % len(short))
    sys.stdout.flush()
    check_memory("stores")

    sys.stdout.write("[3/6] the before build, over term66_store's "
                     "texts\n")
    sys.stdout.flush()
    before_pool, _bj, before_groups, before_roots, _be, before_stats = \
        build(records, before_terms, "before")
    before_sets = member_sets(before_groups, before_roots)
    check_memory("before build")

    sys.stdout.write("[4/6] the after build, over term104_store's "
                     "texts\n")
    sys.stdout.flush()
    after_pool, after_joiner, after_groups, after_roots, after_edges, \
        after_stats = build(records, after_terms, "after")
    after_sets = member_sets(after_groups, after_roots)
    check_memory("after build")

    sys.stdout.write("[5/6] the candidate, and the delta\n")
    sys.stdout.flush()
    multi_text = set()
    for root in after_roots:
        texts = set()
        for label in after_groups[root]:
            texts.add(after_pool.by_label[label]["wrapped_text"])
        if len(texts) > 1:
            multi_text.update(texts)
    cache = P.load_byte_cache()
    sizes = P.measure_bytes(sorted(multi_text), cache)
    entries = after_pool.build_entries(after_joiner, after_edges, sizes)
    candidate = {
        "what_this_is":
            "a CANDIDATE pool, not the pool of record: the merge "
            "pool66_run.py calls 'as ruled', over the canon40 member "
            "set, with the layer-5 texts read from term104_store",
        "population_shortfall":
            "%d of the %d proved members carry no layer-4 record, so "
            "pool66_run.py refuses to write the_pool6.json over this "
            "member set; that refusal stands and is not worked around"
            % (len(short), len(records)),
        "members_with_no_layer4_record": sorted(short),
        "summary": {
            "entries": len(after_roots),
            "members": len(records),
            "entries_spanning_more_than_one_language":
                len([one for one in entries
                     if one["spans_more_than_one_language"]]),
        },
        "merge_stats": after_stats,
        "entries": entries,
    }
    handle = open(CANDIDATE, "w")
    json.dump(candidate, handle, indent=1, sort_keys=True)
    handle.close()
    sys.stdout.write("   wrote %s\n" % CANDIDATE)
    sys.stdout.flush()
    check_memory("candidate")

    only_before, only_after = delta_of(before_sets, after_sets)

    sys.stdout.write("[6/6] the t100 edges\n")
    sys.stdout.flush()
    before_texts = {}
    eligible_before = {}
    for name in before_terms:
        ok, text, _why = P.layer5_eligibility(before_terms[name])
        before_texts[name] = text
        eligible_before[name] = ok
    after_texts = {}
    eligible_after = {}
    for name in after_terms:
        ok, text, _why = P.layer5_eligibility(after_terms[name])
        after_texts[name] = text
        eligible_after[name] = ok
    edge_rows, edge_counts = edge_answer(before_texts, after_texts,
                                         eligible_before,
                                         eligible_after)
    check_memory("edges")

    distinct_before = set()
    for name in before_texts:
        if eligible_before[name]:
            distinct_before.add(before_texts[name])
    distinct_after = set()
    for name in after_texts:
        if eligible_after[name]:
            distinct_after.add(after_texts[name])

    delta = {
        "population":
            "the canon40 member set, %d proved units, identical in "
            "both builds; the only difference is the store the "
            "layer-5 texts come from" % len(records),
        "entries_before_over_term66_store_texts": len(before_roots),
        "entries_after_over_term104_store_texts": len(after_roots),
        "distinct_layer5_texts_before": len(distinct_before),
        "distinct_layer5_texts_after": len(distinct_after),
        "groups_only_in_the_before_build": [sorted(one)
                                            for one in only_before],
        "groups_only_in_the_after_build": [sorted(one)
                                           for one in only_after],
        "merge_stats_before": before_stats,
        "merge_stats_after": after_stats,
        "t100_edges": edge_counts,
        "t100_edge_rows": edge_rows,
        "seconds": round(time.time() - started, 1),
        "peak_resident_kb": peak_kb(),
    }
    handle = open(DELTA, "w")
    json.dump(delta, handle, indent=1, sort_keys=True)
    handle.close()
    sys.stdout.write("   wrote %s\n" % DELTA)
    for key in sorted(edge_counts):
        sys.stdout.write("   %-52s %d\n" % (key, edge_counts[key]))
    sys.stdout.write("   entries before %d, after %d\n"
                     % (len(before_roots), len(after_roots)))
    sys.stdout.write("   distinct layer-5 texts before %d, after %d\n"
                     % (len(distinct_before), len(distinct_after)))
    sys.stdout.write("   groups only-before %d, only-after %d\n"
                     % (len(only_before), len(only_after)))
    sys.stdout.write("   peak resident %d kB, %.0f s\n"
                     % (peak_kb(), time.time() - started))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
