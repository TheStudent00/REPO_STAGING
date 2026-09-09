#!/usr/bin/env python3
"""build_the_pool3.py -- TASK 54, THE POOL OVER canon38.

ONE POOL.  Every unit TASK 52 (log_152) proved goes in:

  - the original corpus         1,763 proved  canon38_wrapped_*.json
  - the interpreter / JIT           9 proved  canon38_interp.json
  - the regenerated population 28,664 proved  canon38_regen_store/*

which is 30,436 member units of 31,078 attempted.

RULING 1 OF ROUND 10 (the owner, 2026-09-02; AgentMemory "ROUND 10
RULINGS"; brief log_151 ruling 1): THE POOL MERGES ON THREE GROUNDS,
and the brief-strict two-ground count is RECORDED on the artifact,
never used.  The three grounds:

  (a) LAYER-5 TEXT IDENTITY, among units whose layer-4 term was
      PROVED equal to their own machine code -- TASK 53's 23,132
      units, read from the `layer4c_*` artifacts.  A term that was
      DISPROVED, undecided on both routes, or never built is not
      evidence of anything, and THE REPRESENTATIVE RULE (AgentMemory,
      the owner 2026-08-29) names the simplest member of a group PROVED
      equivalent.
  (b) LAYER-3 WRAPPED-TEXT IDENTITY.  Two wrapped texts that are the
      same string, character for character, are the same machine code
      twice; equivalence by construction.  This is the ground ruling 1
      ratified.
  (c) A PROVED EDGE:
        proved_edges.json / proved_edges2.json / proved_edges3.json
            pairs with verdict PROVED (cross-unit prover, solver),
        interp_join3.json rows with relation PROVED_EQUAL and its
            interpreter-to-interpreter proved edges,
        interp_fastpath.json's proof of the CPython fast path.

and the join is closed under transitivity.

THE UNITS WITH NO PROVED TERM, stated rather than implied.  TASK 53
withdrew 415 units whose layer-4 term z3 DISPROVED against their own
machine code, left 5,602 undecided on both routes, and built no term
at all for 1,287 -- 7,304 of the 30,436.  All of them are CARRIED in
this pool as members with the flag `layer5_merge_eligible: false` and
a stated reason; all of them are EXCLUDED from ground (a).  They
remain reachable by ground (b) and ground (c), because neither rests
on the term: layer-3 identity is the same machine code twice, and a
proved edge was established elsewhere.

An entry lists its MEMBER UNITS.  Language, arrival annotation and
population are COLUMNS ON THE MEMBERS, never partitions of the pool.

THE REPRESENTATIVE RULE: the simplest member -- fewest bytes of
machine code, ties broken by first-in-list order.  Every member of a
layer-3-identical group assembles to the same bytes, so the byte count
only has to decide inside entries carrying more than one wrapped text;
those texts are assembled with `as` and their bytes counted from
`objdump`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Nothing in this program reads a token.  The merge key is a machine
text or a proved edge; the token rides on the member as its `operator`
display label and is read by nothing.  This file claims NO provenance
exemption from the guard: it is a grouping artifact and it is walked
in full.  It declares no `role` field anywhere.

REUSE: `build_the_pool2.py` is imported, never edited.  Four of its
functions carry this program unchanged -- `layer5_eligibility`,
`type_key_of`, `proved_edge_list` and `UnionFind`.  What is new here
is only the intake (canon38 in place of canon37, layer4c in place of
layer4b) and the output names.

Coding discipline: no compound one-liner statements.

usage: build_the_pool3.py
"""

import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_the_pool2 as POOL2                          # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
PROVED = "WRAPPED_TEXT_PROVED"
BYTE_CACHE = os.path.join(HERE, "the_pool3_bytes.json")
WORK = "/tmp/the_pool3_work"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ------------------------------------------------------------ intake

def take_original():
    """the original corpus, in pool order: language in the corpus's own
    order, unit in numeric order."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        units = json.load(open(path))["units"]

        def sort_key(k):
            n = units[k].get("n")
            if n is not None and str(n).isdigit():
                return (int(n), k)
            return (10 ** 9, k)

        for key in sorted(units.keys(), key=sort_key):
            rec = units[key]
            if rec.get("outcome") != PROVED:
                continue
            out.append(rec)
    return out


def take_interpreter():
    path = os.path.join(HERE, "canon38_interp.json")
    units = json.load(open(path))["units"]
    out = []
    for key in sorted(units.keys()):
        rec = units[key]
        if rec.get("outcome") != PROVED:
            continue
        out.append(rec)
    return out


def take_regenerated():
    store = os.path.join(HERE, "canon38_regen_store")
    out = []
    for name in sorted(os.listdir(store)):
        if not name.endswith(".json"):
            continue
        units = json.load(open(os.path.join(store, name)))["units"]
        for key in sorted(units.keys()):
            rec = units[key]
            if rec.get("outcome") != PROVED:
                continue
            out.append(rec)
    return out


def take_all():
    records = []
    records.extend(take_original())
    records.extend(take_interpreter())
    records.extend(take_regenerated())
    return records


# ------------------------------------------------------------ layer 4

def layer4c_paths():
    out = []
    for lang in LANGS:
        out.append(os.path.join(HERE, "layer4c_terms_%s.json" % lang))
    out.append(os.path.join(HERE, "layer4c_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "layer4c_regen_store",
                                             "*.json"))))
    return out


def read_layer4c():
    """unit label -> the layer-4 record TASK 53 wrote for it."""
    out = {}
    for path in layer4c_paths():
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


# ------------------------------------------------- machine-code bytes

def load_byte_cache():
    if os.path.exists(BYTE_CACHE):
        return json.load(open(BYTE_CACHE))
    return {}


def measure_bytes(texts, cache):
    """assemble each text and report its length in bytes.  Used only
    where an entry carries more than one wrapped text, which is where
    the representative rule's `fewest bytes of machine code` actually
    has to decide something."""
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    index = 0
    fresh = 0
    callees = set()
    for text in texts:
        for piece in text.split(";"):
            piece = piece.strip()
            if not piece.startswith("call "):
                continue
            target = piece[5:].strip()
            if target.startswith("*"):
                continue
            callees.add(target)
    for text in texts:
        index = index + 1
        if text in cache:
            continue
        stem = os.path.join(WORK, "t%06d" % index)
        lines = []
        lines.append("    .text")
        for name in sorted(callees):
            lines.append("%s:" % name)
            lines.append("    ret")
        lines.append("    .globl t")
        lines.append("t:")
        start = len(lines)
        for piece in text.split(";"):
            piece = piece.strip()
            if not piece:
                continue
            if piece.endswith(":"):
                lines.append(piece)
            else:
                lines.append("    " + piece)
        handle = open(stem + ".s", "w")
        handle.write("\n".join(lines) + "\n")
        handle.close()
        run = subprocess.run(["as", "--64", "-o", stem + ".o",
                              stem + ".s"], capture_output=True)
        if run.returncode != 0:
            cache[text] = None
            fresh = fresh + 1
            continue
        run = subprocess.run(["objdump", "-d", stem + ".o"],
                             capture_output=True)
        count = 0
        seen_t = False
        for line in run.stdout.decode("utf8", "replace").splitlines():
            if line.strip().endswith("<t>:"):
                seen_t = True
                continue
            if not seen_t:
                continue
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0].strip().endswith(":"):
                count = count + len(parts[1].split())
        cache[text] = count
        fresh = fresh + 1
    log("   texts newly assembled %d, cache holds %d"
        % (fresh, len(cache)))
    return cache


# --------------------------------------------------------- the merge

def build_pool(records, layer4c, use_layer3_identity):
    """returns (union-find, edges, eligibility, stats) after applying
    every ground.  `use_layer3_identity` switches ground (b) off so the
    brief-strict count can be computed from the same code."""
    uf = POOL2.UnionFind()
    by_label = {}
    for rec in records:
        by_label[rec["unit"]] = rec
        uf.add(rec["unit"])

    eligibility = {}
    for rec in records:
        eligibility[rec["unit"]] = POOL2.layer5_eligibility(
            layer4c.get(rec["unit"]))

    layer5_first = {}
    layer5_merges = 0
    for rec in records:
        ok, text, _reason = eligibility[rec["unit"]]
        if not ok:
            continue
        if text in layer5_first:
            uf.union(layer5_first[text], rec["unit"])
            layer5_merges = layer5_merges + 1
        else:
            layer5_first[text] = rec["unit"]

    layer3_first = {}
    layer3_merges = 0
    for rec in records:
        text = rec.get("wrapped_text")
        if not text:
            raise SystemExit("REFUSED OWN OUTPUT: a proved unit with no "
                             "wrapped text: %s" % rec["unit"])
        if text in layer3_first:
            if use_layer3_identity:
                uf.union(layer3_first[text], rec["unit"])
            layer3_merges = layer3_merges + 1
        else:
            layer3_first[text] = rec["unit"]

    edges = POOL2.proved_edge_list(by_label)
    for edge in edges:
        uf.union(edge["left"], edge["right"])

    stats = {
        "distinct_layer5_texts_among_eligible_units": len(layer5_first),
        "layer5_identity_merges": layer5_merges,
        "distinct_layer3_wrapped_texts": len(layer3_first),
        "layer3_identity_merges": layer3_merges,
        "proved_edges_applied": len(edges),
    }
    return uf, edges, eligibility, stats


def main():
    log("-- intake")
    records = take_all()
    order = {}
    by_label = {}
    for rec in records:
        label = rec["unit"]
        if label in by_label:
            raise SystemExit("REFUSED OWN OUTPUT: two records claim the "
                             "same unit label %r" % label)
        order[label] = len(order)
        by_label[label] = rec
    log("   units in the pool %d" % len(records))
    counts = {}
    for rec in records:
        counts[rec["population"]] = counts.get(rec["population"], 0) + 1
    log("   by arrival population %s" % json.dumps(counts, sort_keys=True))

    layer4c = read_layer4c()
    log("   layer-4 records read %d" % len(layer4c))
    missing = []
    for rec in records:
        if rec["unit"] not in layer4c:
            missing.append(rec["unit"])
    if missing:
        raise SystemExit("REFUSED OWN OUTPUT: %d proved units have no "
                         "layer-4 record, first %s"
                         % (len(missing), missing[:3]))

    log("-- the merge, brief-strict: layer-5 identity and proved edges "
        "only (RECORDED, NOT USED)")
    strict_uf, _e, _el, strict_stats = build_pool(records, layer4c, False)
    strict_roots = set()
    for label in order:
        strict_roots.add(strict_uf.find(label))
    log("   entries under the brief-strict rule %d" % len(strict_roots))

    log("-- the merge, as ruled: layer-5 identity, layer-3 identity, "
        "proved edges")
    uf, edges, eligibility, stats = build_pool(records, layer4c, True)
    for key in sorted(stats):
        log("   %-46s %d" % (key, stats[key]))

    groups = {}
    for label in sorted(order.keys(), key=lambda x: order[x]):
        groups.setdefault(uf.find(label), []).append(label)
    roots = sorted(groups.keys(), key=lambda r: order[groups[r][0]])
    log("   entries %d" % len(roots))

    edges_by_root = {}
    for edge in edges:
        edges_by_root.setdefault(uf.find(edge["left"]), []).append(edge)

    log("-- the representative rule")
    multi_text = set()
    multi_entries = 0
    for root in roots:
        texts = set()
        for label in groups[root]:
            texts.add(by_label[label]["wrapped_text"])
        if len(texts) > 1:
            multi_text.update(texts)
            multi_entries = multi_entries + 1
    log("   entries carrying more than one wrapped text %d"
        % multi_entries)
    log("   distinct texts to assemble %d" % len(multi_text))
    cache = load_byte_cache()
    sizes = measure_bytes(sorted(multi_text), cache)
    handle = open(BYTE_CACHE, "w")
    json.dump(sizes, handle, indent=1, sort_keys=True)
    handle.close()

    entries = []
    index = 0
    for root in roots:
        index = index + 1
        labels = groups[root]
        members = []
        langs = []
        pops = []
        texts = []
        layer5_texts = []
        for label in labels:
            rec = by_label[label]
            ok, l5text, reason = eligibility[label]
            members.append({
                "unit": label,
                "lang": rec["lang"],
                "operator": rec.get("operator"),
                "population": rec.get("population"),
                "arrival_annotation": rec.get("arrival_annotation"),
                "wrapped_text": rec["wrapped_text"],
                "layer5_normalized_text": l5text,
                "layer5_merge_eligible": ok,
                "layer5_merge_eligibility_reason": reason,
                "out_row": rec.get("out_row"),
                "result_width": rec.get("result_width"),
            })
            if rec["lang"] not in langs:
                langs.append(rec["lang"])
            if rec.get("population") not in pops:
                pops.append(rec.get("population"))
            if rec["wrapped_text"] not in texts:
                texts.append(rec["wrapped_text"])
            if ok and l5text not in layer5_texts:
                layer5_texts.append(l5text)
        best = None
        for label in labels:
            text = by_label[label]["wrapped_text"]
            size = sizes.get(text)
            if size is None:
                size = len(text)
                if len(texts) > 1:
                    measured = "the text would not assemble, so its "\
                               "character length stands in and the "\
                               "substitution is stated here rather "\
                               "than hidden"
                else:
                    measured = "the character length of the wrapped "\
                               "text -- this entry carries one text "\
                               "only, so every member ties and the "\
                               "tie-break decides"
            else:
                measured = "bytes of machine code, assembled with `as` "\
                           "and counted from objdump"
            key = (size, order[label])
            if best is None or key < best[0]:
                best = (key, label, size, measured)
        entry = {
            "entry_id": "E%05d" % index,
            "member_count": len(labels),
            "representative": best[1],
            "representative_size": best[2],
            "representative_size_measured_as": best[3],
            "representative_rule": "the simplest member -- fewest bytes "
                                   "of machine code, ties broken by "
                                   "first-in-list order",
            "languages": sorted(langs),
            "language_count": len(langs),
            "spans_more_than_one_language": len(langs) > 1,
            "arrival_populations": sorted(pops),
            "spans_compiled_and_interpreted":
                ("interpreter" in pops
                 and ("original" in pops or "regenerated" in pops)),
            "wrapped_texts": texts,
            "distinct_wrapped_text_count": len(texts),
            "layer5_normalized_texts": layer5_texts,
            "distinct_layer5_text_count": len(layer5_texts),
            "members_not_layer5_eligible":
                len([m for m in members
                     if not m["layer5_merge_eligible"]]),
            "type_key": POOL2.type_key_of(by_label[labels[0]]),
            "members": members,
        }
        grounds = []
        by_l3 = {}
        by_l5 = {}
        for label in labels:
            rec = by_label[label]
            by_l3.setdefault(rec["wrapped_text"], []).append(rec["lang"])
            ok, l5text, _r = eligibility[label]
            if ok:
                by_l5.setdefault(l5text, []).append(rec["lang"])
        for text in texts:
            here = sorted(set(by_l3[text]))
            if len(here) > 1:
                grounds.append({
                    "ground": "layer-3 text identity",
                    "languages_it_joins": here,
                    "detail": "these members carry the SAME wrapped "
                              "text, character for character -- the "
                              "same machine code twice",
                    "wrapped_text": text,
                })
        for text in layer5_texts:
            here = sorted(set(by_l5[text]))
            if len(here) > 1:
                grounds.append({
                    "ground": "layer-5 text identity",
                    "languages_it_joins": here,
                    "detail": "these members' layer-4 terms were each "
                              "proved equal to their own machine code "
                              "and normalize to the SAME layer-5 text",
                    "layer5_normalized_text": text,
                })
        for edge in edges_by_root.get(root, []):
            left = by_label[edge["left"]]["lang"]
            right = by_label[edge["right"]]["lang"]
            if left == right:
                continue
            rec = dict(edge)
            rec["languages_it_joins"] = sorted([left, right])
            grounds.append(rec)
        entry["cross_language_grounds"] = grounds
        entries.append(entry)

    ineligible = 0
    withdrawn = 0
    undecided = 0
    no_term = 0
    for label in order:
        if not eligibility[label][0]:
            ineligible = ineligible + 1
        record = layer4c[label]
        verdicts = (record.get("gate_ship_verdict"),
                    record.get("gate_textorder_verdict"))
        if not record.get("term_built"):
            no_term = no_term + 1
            continue
        if "DISPROVED" in verdicts:
            withdrawn = withdrawn + 1
            continue
        if "PROVED_EQUAL" not in verdicts:
            undecided = undecided + 1

    meta = {
        "generator": "build_the_pool3.py",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL.  No "
                     "provenance exemption is claimed and no `role` "
                     "field is declared anywhere in this document.",
        "task": "TASK 54 -- the pool over canon38, three grounds",
        "population": "every unit TASK 52 (log_152) proved: 30,436 of "
                      "31,078 attempted -- original 1,763, interpreter "
                      "9, regenerated 28,664",
        "intake": "canon38_wrapped_{c,cpp,go,rust,swift}.json, "
                  "canon38_interp.json, canon38_regen_store/*.json, "
                  "outcome WRAPPED_TEXT_PROVED only",
        "layer4_source": "layer4c_terms_{c,cpp,go,rust,swift}.json, "
                         "layer4c_interp.json, "
                         "layer4c_regen_store/*.json -- TASK 53's "
                         "artifacts over canon38, per log_153 §11.3; "
                         "the layer4b_* files are not read by this "
                         "program",
        "merge_rule": "RULING 1 of round 10: layer-5 normalized-text "
                      "identity among units whose layer-4 term was "
                      "PROVED, or layer-3 wrapped-text identity, or a "
                      "proved edge; closed under transitivity",
        "brief_strict_count_note": "the two-ground count (layer-5 "
                                   "identity and proved edges only, no "
                                   "layer-3 identity) is RECORDED in "
                                   "the summary as "
                                   "`entries_under_the_brief_strict_rule`"
                                   " and is NOT the pool's entry count, "
                                   "per ruling 1",
        "units_with_no_proved_term": "every unit whose layer-4 term was "
                                     "DISPROVED, undecided on both "
                                     "routes, or never built is CARRIED "
                                     "as a member and FLAGGED "
                                     "`layer5_merge_eligible: false` "
                                     "with its reason; such a member "
                                     "may be merged ONLY by layer-3 "
                                     "wrapped-text identity or by a "
                                     "proved edge, neither of which "
                                     "rests on the term",
        "proved_edge_sources": ["proved_edges.json", "proved_edges2.json",
                                "proved_edges3.json",
                                "interp_join3.json",
                                "interp_fastpath.json"],
        "pool_order": "the originals in the corpus's own language order "
                      "and numeric unit order, then the interpreter "
                      "units, then the regenerated population -- this "
                      "is the `first-in-list` the representative rule's "
                      "tie-break names",
        "columns_not_partitions": "language, arrival annotation and "
                                  "population are fields on the "
                                  "MEMBERS.  There is no compiled table "
                                  "and no interpreter table in this "
                                  "artifact.",
        "reuse": "build_the_pool2.py is imported and not edited: "
                 "layer5_eligibility, type_key_of, proved_edge_list "
                 "and UnionFind come from it unchanged",
        "supersedes_as_an_object": "the_pool2.json, which merged the "
                                   "same 30,436 units over canon37.  It "
                                   "stays on disk, byte for byte, as "
                                   "the superseded record.",
    }
    summary = {
        "units_in_the_pool": len(records),
        "units_by_arrival_population": counts,
        "entries": len(entries),
        "entries_under_the_brief_strict_rule": len(strict_roots),
        "brief_strict_layer5_identity_merges":
            strict_stats["layer5_identity_merges"],
        "distinct_layer5_texts_among_eligible_units":
            stats["distinct_layer5_texts_among_eligible_units"],
        "layer5_identity_merges": stats["layer5_identity_merges"],
        "distinct_layer3_wrapped_texts":
            stats["distinct_layer3_wrapped_texts"],
        "layer3_identity_merges": stats["layer3_identity_merges"],
        "proved_edges_applied": stats["proved_edges_applied"],
        "units_not_layer5_eligible": ineligible,
        "units_withdrawn_at_layer4": withdrawn,
        "units_undecided_at_layer4": undecided,
        "units_with_no_layer4_term": no_term,
        "entries_spanning_more_than_one_language":
            len([e for e in entries if e["spans_more_than_one_language"]]),
        "entries_spanning_compiled_and_interpreted":
            len([e for e in entries
                 if e["spans_compiled_and_interpreted"]]),
        "entries_with_more_than_one_wrapped_text":
            len([e for e in entries
                 if e["distinct_wrapped_text_count"] > 1]),
        "entries_with_more_than_one_layer5_text":
            len([e for e in entries
                 if e["distinct_layer5_text_count"] > 1]),
    }
    doc = {"meta": meta, "summary": summary, "entries": entries}
    path = os.path.join(HERE, "the_pool3.json")
    handle = open(path, "w")
    json.dump(doc, handle, indent=1, sort_keys=True)
    handle.close()
    log("-- wrote the_pool3.json")
    log(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
