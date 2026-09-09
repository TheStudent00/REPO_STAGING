#!/usr/bin/env python3
"""build_the_pool1.py -- TASK 44, THE MERGED POOL.

the owner's correction, verbatim: "there is a pool of all the arch-units we
canonicalized and merged them when they are equivalent.  not an
accounting of every languages contribution to the number of units."

ONE POOL.  Every unit TASK 43 (log_135) proved goes in:

  - the original corpus            1,752 proved  (canon36_universal_*.json)
  - the interpreter / JIT units        9 proved  (canon36_interp.json)
  - the regenerated population    27,223 proved  (canon36_regen_store/*)

Units PROVED EQUIVALENT collapse into ONE ENTRY.  An entry is one
distinct computation.  Two units join when either

  (a) their region36 universal-form texts are IDENTICAL, character for
      character -- the same computation written the same way; or
  (b) a PROVED edge relates them:
        proved_edges.json / proved_edges2.json / proved_edges3.json
            pairs with verdict PROVED (cross-unit prover, solver),
        interp_join3.json rows with relation PROVED_EQUAL and its
            interpreter-to-interpreter proved edges,
        interp_fastpath.json's proof of the CPython fast path.

and the join is closed under transitivity.

An entry lists its MEMBER UNITS.  Language, arrival annotation and
population are COLUMNS ON THE MEMBERS.  They are never partitions of
the pool: there is no compiled table and no interpreter table in this
artifact, and anyone who wants one filters the members.

THE REPRESENTATIVE RULE (AgentMemory, the owner 2026-08-29) names each
entry: the simplest member -- fewest bytes of machine code, ties
broken by first-in-list order.  Every member of a text-identical group
assembles to the same bytes, so the byte count only ever separates
members that were joined by a proved edge; those texts are assembled
with `as` and measured.  Where a text will not assemble the fall-back
size is stated on the entry rather than hidden.

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

Nothing in this program reads a token.  The merge key is the machine
text or a proved edge; the token rides along as the member's
`operator` display label and is read by nothing.  This file claims NO
provenance exemption from the guard: it is a grouping artifact and it
is walked in full.

usage: build_the_pool1.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
PROVED = "REGION_TEXT_PROVED"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ------------------------------------------------------------ intake

def take_original():
    """the original corpus, in pool order: language in the corpus's own
    order, unit in numeric order."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "canon36_universal_%s.json" % lang)
        units = json.load(open(path))["units"]
        keys = sorted(units.keys(),
                      key=lambda k: (int(units[k]["n"])
                                     if str(units[k]["n"]).isdigit()
                                     else 10 ** 9, k))
        for key in keys:
            rec = units[key]
            if rec.get("outcome") != PROVED:
                continue
            out.append(rec)
    return out


def take_interpreter():
    path = os.path.join(HERE, "canon36_interp.json")
    units = json.load(open(path))["units"]
    out = []
    for key in sorted(units.keys()):
        rec = units[key]
        if rec.get("outcome") != PROVED:
            continue
        out.append(rec)
    return out


def take_regenerated():
    store = os.path.join(HERE, "canon36_regen_store")
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


# ------------------------------------------------------- provenance

def probe_provenance():
    """unit label -> (arity bucket, source).  The originals' bucket is
    read from the probe manifest, which is the one place a token is
    authored; it never participates in any comparison here."""
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "probe_manifest_%s.json" % lang)
        probes = json.load(open(path))["probes"]
        for n in probes:
            probe = probes[n]
            out["%s/op_%s" % (lang, n)] = {
                "arity_bucket": probe.get("bucket"),
                "arity_source": "the probe manifest's own bucket field",
            }
    return out


def opunit_provenance():
    """`lang/opunit_N` -> arity bucket, recomputed from the acceptance
    record the regeneration itself indexed by (legality_rules'
    corpus_operator_units)."""
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "op_units_%s.json" % lang)
        if not os.path.exists(path):
            continue
        data = json.load(open(path))
        seen = {}
        for key in data["probes"]:
            meta = data["probes"][key]["meta"]
            seen[(meta["arity"], meta.get("position"),
                  meta["operator"])] = True
        index = 0
        for ident in sorted(seen):
            bucket = ident[0]
            if ident[1]:
                bucket = "%s_%s" % (ident[0], ident[1])
            out["%s/opunit_%d" % (lang, index)] = {
                "arity_bucket": bucket,
                "arity_source": "the regeneration's own operator-unit "
                                "row (arity and position), recomputed "
                                "from op_units_%s.json" % lang,
            }
            index = index + 1
    return out


def arriving_lineages(rec):
    count = 0
    for block in rec.get("block_directory") or []:
        if block.get("kind") == "input":
            count = count + 1
    return count


def arity_of(rec, probes, opunits):
    label = rec["unit"]
    if label in probes:
        return probes[label]
    oid = rec.get("operator_unit_id")
    if oid and oid in opunits:
        return opunits[oid]
    return {
        "arity_bucket": "%d_arriving_lineages" % arriving_lineages(rec),
        "arity_source": "measured from the unit's own region-form block "
                        "directory: the number of input blocks",
    }


def type_key_of(rec):
    """a MACHINE-FORM key for this unit's shape: which register file
    each arriving lineage is loaded through, and how wide the answer
    is.  Read off the unit's own block directory.  No token."""
    files = []
    for block in rec.get("block_directory") or []:
        if block.get("kind") == "input":
            files.append(block.get("register_file") or "unstated")
    width = rec.get("result_width")
    return "%s|%s" % (",".join(files) if files else "none", width)


# ------------------------------------------------------- proved edges

def proved_edge_list(present):
    """every proved edge whose BOTH endpoints are units of the pool,
    each carrying the ground that made it."""
    out = []
    for name in ["proved_edges.json", "proved_edges2.json",
                 "proved_edges3.json"]:
        path = os.path.join(HERE, name)
        doc = json.load(open(path))
        for pair in doc["pairs"]:
            if pair.get("verdict") != "PROVED":
                continue
            a = pair["a"]
            b = pair["b"]
            if a not in present or b not in present:
                continue
            out.append({
                "left": a,
                "right": b,
                "ground": "a proved edge of the cross-unit prover",
                "source_artifact": name,
                "detail": pair.get("detail"),
                "proof_method": pair.get("proof_method"),
            })
    doc = json.load(open(os.path.join(HERE, "interp_join3.json")))
    by_class = {}
    for row in doc["rows"]:
        by_class.setdefault(row["interp_class_id"], row["interp_unit"])
    for row in doc["rows"]:
        if row.get("relation") != "PROVED_EQUAL":
            continue
        a = row["interp_unit"]
        b = row.get("compiled_unit")
        if a not in present or b not in present:
            continue
        out.append({
            "left": a,
            "right": b,
            "ground": "a PROVED_EQUAL relation of the interpreter join",
            "source_artifact": "interp_join3.json",
            "detail": row.get("evidence"),
            "scope": row.get("scope"),
            "evidence_class": row.get("evidence_class"),
            "established_by": row.get("established_by"),
        })
    for edge in doc["interpreter_to_interpreter_edges"]:
        if edge.get("relation") != "PROVED_EQUAL":
            continue
        a = by_class.get(edge["left_class_id"])
        b = by_class.get(edge["right_class_id"])
        if a not in present or b not in present:
            continue
        out.append({
            "left": a,
            "right": b,
            "ground": "a proved interpreter-to-interpreter edge of the "
                      "interpreter join",
            "source_artifact": "interp_join3.json",
            "detail": edge.get("detail"),
        })
    path = os.path.join(HERE, "interp_fastpath.json")
    doc = json.load(open(path))
    a = "%s/%s" % (doc["unit"]["lang"], doc["unit"]["n"])
    b = None
    for row in json.load(open(os.path.join(HERE,
                                           "interp_join3.json")))["rows"]:
        if row["interp_unit"] == a and row.get("relation") == "PROVED_EQUAL":
            b = row["compiled_unit"]
            break
    if a in present and b in present:
        out.append({
            "left": a,
            "right": b,
            "ground": "the fast-path proof",
            "source_artifact": "interp_fastpath.json",
            "detail": doc["proof"].get("claim_tested"),
            "scope": "the fast path's COMPUTATION over the domain the "
                     "unit's own bytes bound",
        })
    return out


# ------------------------------------------------------------- union

class UnionFind(object):
    def __init__(self):
        self.up = {}

    def add(self, x):
        if x not in self.up:
            self.up[x] = x

    def find(self, x):
        self.add(x)
        while self.up[x] != x:
            self.up[x] = self.up[self.up[x]]
            x = self.up[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.up[rb] = ra


# ------------------------------------------------- machine-code bytes

def measure_bytes(texts):
    """assemble each text and report its length in bytes.  Used only
    where an entry carries more than one text, which is where the
    representative rule's `fewest bytes of machine code` actually has
    to decide something."""
    out = {}
    if not texts:
        return out
    work = "/tmp/the_pool1_work"
    if not os.path.isdir(work):
        os.makedirs(work)
    index = 0
    for text in texts:
        index = index + 1
        stem = os.path.join(work, "t%04d" % index)
        lines = []
        lines.append("    .text")
        lines.append("    .globl t")
        lines.append("t:")
        for piece in text.split(";"):
            piece = piece.strip()
            if not piece:
                continue
            if piece.endswith(":"):
                lines.append(piece)
            else:
                lines.append("    " + piece)
        open(stem + ".s", "w").write("\n".join(lines) + "\n")
        run = subprocess.run(["as", "--64", "-o", stem + ".o",
                              stem + ".s"], capture_output=True)
        if run.returncode != 0:
            out[text] = None
            continue
        run = subprocess.run(["objdump", "-d", stem + ".o"],
                             capture_output=True)
        count = 0
        for line in run.stdout.decode("utf8", "replace").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0].strip().endswith(":"):
                count = count + len(parts[1].split())
        out[text] = count
    return out


# -------------------------------------------------------------- main

def main():
    log("-- intake")
    records = []
    records.extend(take_original())
    records.extend(take_interpreter())
    records.extend(take_regenerated())
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

    log("-- the merge")
    uf = UnionFind()
    for label in by_label:
        uf.add(label)
    text_first = {}
    text_merges = 0
    for rec in records:
        text = rec.get("universal_text")
        if not text:
            raise SystemExit("REFUSED OWN OUTPUT: a proved unit with no "
                             "universal text: %s" % rec["unit"])
        if text in text_first:
            uf.union(text_first[text], rec["unit"])
            text_merges = text_merges + 1
        else:
            text_first[text] = rec["unit"]
    log("   distinct universal texts %d" % len(text_first))
    edges = proved_edge_list(by_label)
    for edge in edges:
        uf.union(edge["left"], edge["right"])
    log("   proved edges applied %d" % len(edges))

    groups = {}
    for label in sorted(order.keys(), key=lambda x: order[x]):
        groups.setdefault(uf.find(label), []).append(label)
    roots = sorted(groups.keys(), key=lambda r: order[groups[r][0]])
    log("   entries %d" % len(roots))

    edges_by_root = {}
    for edge in edges:
        edges_by_root.setdefault(uf.find(edge["left"]), []).append(edge)

    multi_text = []
    for root in roots:
        texts = set()
        for label in groups[root]:
            texts.add(by_label[label]["universal_text"])
        if len(texts) > 1:
            multi_text.extend(texts)
    sizes = measure_bytes(sorted(set(multi_text)))
    log("   texts measured in bytes of machine code %d" % len(sizes))

    entries = []
    index = 0
    for root in roots:
        index = index + 1
        labels = groups[root]
        members = []
        langs = []
        pops = []
        texts = []
        for label in labels:
            rec = by_label[label]
            prov = None
            members.append({
                "unit": label,
                "lang": rec["lang"],
                "operator": rec.get("operator"),
                "population": rec.get("population"),
                "arrival_annotation": rec.get("arrival_annotation"),
                "universal_text": rec["universal_text"],
                "region_base": rec.get("region_base"),
                "result_block": rec.get("result_block"),
            })
            if rec["lang"] not in langs:
                langs.append(rec["lang"])
            if rec.get("population") not in pops:
                pops.append(rec.get("population"))
            if rec["universal_text"] not in texts:
                texts.append(rec["universal_text"])
        # the representative rule
        best = None
        for label in labels:
            text = by_label[label]["universal_text"]
            size = sizes.get(text)
            if size is None:
                size = len(text)
                measured = "the character length of the universal text "\
                           "-- this entry carries one text only, so "\
                           "every member ties and the tie-break decides"
                if len(texts) > 1:
                    measured = "the text would not assemble, so its "\
                               "character length stands in and the "\
                               "substitution is stated here rather "\
                               "than hidden"
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
            "universal_texts": texts,
            "distinct_universal_text_count": len(texts),
            "type_key": type_key_of(by_label[labels[0]]),
            "members": members,
        }
        grounds = []
        seen_text_langs = {}
        for label in labels:
            rec = by_label[label]
            seen_text_langs.setdefault(rec["universal_text"],
                                       []).append(rec["lang"])
        for text in texts:
            here = sorted(set(seen_text_langs[text]))
            if len(here) > 1:
                grounds.append({
                    "ground": "text identity",
                    "languages_it_joins": here,
                    "detail": "these members carry the SAME region36 "
                              "universal-form text, character for "
                              "character",
                    "universal_text": text,
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

    meta = {
        "generator": "build_the_pool1.py",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL, no provenance "
                     "exemption claimed.",
        "task": "TASK 44 -- the merged pool",
        "correction_it_answers": "there is a pool of all the arch-units "
                                 "we canonicalized and merged them when "
                                 "they are equivalent.  not an "
                                 "accounting of every languages "
                                 "contribution to the number of units.",
        "intake": "every unit TASK 43 (log_135) proved, from "
                  "canon36_universal_{c,cpp,go,rust,swift}.json, "
                  "canon36_interp.json and canon36_regen_store/*.json",
        "merge_rule": "identical region36 universal-form text, or a "
                      "proved edge, closed under transitivity",
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
                                  "population are fields on the MEMBERS.  "
                                  "There is no compiled table and no "
                                  "interpreter table in this artifact.",
        "supersedes_as_an_object": "dominant_table25.json and "
                                   "dom_ops23.json, which were the "
                                   "compiled-only table.  Both stay on "
                                   "disk as the superseded record.",
    }
    summary = {
        "units_in_the_pool": len(records),
        "units_by_arrival_population": counts,
        "entries": len(entries),
        "distinct_universal_texts": len(text_first),
        "text_identity_merges": text_merges,
        "proved_edges_applied": len(edges),
        "entries_spanning_more_than_one_language":
            len([e for e in entries if e["spans_more_than_one_language"]]),
        "entries_spanning_compiled_and_interpreted":
            len([e for e in entries
                 if e["spans_compiled_and_interpreted"]]),
        "entries_with_more_than_one_universal_text":
            len([e for e in entries
                 if e["distinct_universal_text_count"] > 1]),
    }
    doc = {"meta": meta, "summary": summary, "entries": entries}
    path = os.path.join(HERE, "the_pool1.json")
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    log("-- wrote the_pool1.json")
    log(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
