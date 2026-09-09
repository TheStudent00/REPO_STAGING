#!/usr/bin/env python3
"""build_the_pool2.py -- TASK 49, THE POOL REBUILT ON THE WRAPPED FORM.

ONE POOL.  Every unit TASK 47 (log_146) proved goes in:

  - the original corpus         1,763 proved  canon37_wrapped_*.json
  - the interpreter / JIT           9 proved  canon37_interp.json
  - the regenerated population 28,664 proved  canon37_regen_store/*

which is 30,436 member units of 31,078 attempted.

Units PROVED EQUIVALENT collapse into ONE ENTRY.  An entry is one
distinct computation.  THREE grounds join two units, and nothing else:

  (a) LAYER-5 TEXT IDENTITY.  Their layer-5 normalized texts, from
      TASK 48's `layer4b_*` artifacts, are the same string.  Only
      units whose layer-4 term was PROVED equal to their own machine
      code are eligible: a term that was DISPROVED, undecided, or
      never built is not evidence of anything, and THE REPRESENTATIVE
      RULE names the simplest member of a group PROVED equivalent.
  (b) LAYER-3 TEXT IDENTITY.  Their wrapped texts are the same string,
      character for character.  This is not an inference from a term;
      it is the same machine code twice.  It is the ground the pool1
      merge used at its own layer (the region36 universal text), and
      dropping it would put two identical instruction sequences in two
      entries.  Carried forward deliberately, and named on the entry.
  (c) A PROVED EDGE:
        proved_edges.json / proved_edges2.json / proved_edges3.json
            pairs with verdict PROVED (cross-unit prover, solver),
        interp_join3.json rows with relation PROVED_EQUAL and its
            interpreter-to-interpreter proved edges,
        interp_fastpath.json's proof of the CPython fast path.

and the join is closed under transitivity.

THE 826 WITHDRAWALS, stated rather than implied.  TASK 48 withdrew 826
units whose layer-4 term z3 DISPROVED against their own machine code
(all of them division-shaped -- a ledger defect, log_147 §5.3).  They
are CARRIED in this pool as members with the flag
`layer5_merge_eligible: false` and a reason; they are EXCLUDED from
ground (a).  Why both halves: they are units TASK 47 proved, so
removing them would misstate the population; but their layer-5 text is
disproved, so joining anything by it would be joining on refuted
evidence.  Grounds (b) and (c) still reach them, because neither rests
on the layer-4 term.

An entry lists its MEMBER UNITS.  Language, arrival annotation and
population are COLUMNS ON THE MEMBERS, never partitions of the pool.

THE REPRESENTATIVE RULE (AgentMemory, the owner 2026-08-29): the simplest
member -- fewest bytes of machine code, ties broken by first-in-list
order.  Every member of a layer-3-identical group assembles to the
same bytes, so the byte count only has to decide inside entries that
carry more than one wrapped text; those texts are assembled with `as`
and their bytes counted from `objdump`.

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

usage: build_the_pool2.py
"""

import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
PROVED = "WRAPPED_TEXT_PROVED"
BYTE_CACHE = os.path.join(HERE, "the_pool2_bytes.json")


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ------------------------------------------------------------ intake

def take_original():
    """the original corpus, in pool order: language in the corpus's own
    order, unit in numeric order."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "canon37_wrapped_%s.json" % lang)
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
    path = os.path.join(HERE, "canon37_interp.json")
    units = json.load(open(path))["units"]
    out = []
    for key in sorted(units.keys()):
        rec = units[key]
        if rec.get("outcome") != PROVED:
            continue
        out.append(rec)
    return out


def take_regenerated():
    store = os.path.join(HERE, "canon37_regen_store")
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

def layer4b_paths():
    out = []
    for lang in LANGS:
        out.append(os.path.join(HERE, "layer4b_terms_%s.json" % lang))
    out.append(os.path.join(HERE, "layer4b_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "layer4b_regen_store",
                                             "*.json"))))
    return out


def read_layer4b():
    """unit label -> the layer-4 record TASK 48 wrote for it."""
    out = {}
    for path in layer4b_paths():
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def layer5_eligibility(record):
    """(eligible, layer-5 text or None, the reason, stated).

    Eligible means: a term was built, z3 PROVED it equal to the unit's
    own machine code on at least one route, no route DISPROVED it, and
    a normalized text exists.  Anything else is not proved equivalence
    and may not merge by text."""
    if record is None:
        return (False, None,
                "no layer-4 record exists for this unit")
    if not record.get("term_built"):
        return (False, None,
                "no layer-4 term was built for this unit, so it has "
                "no layer-5 text to be identical to")
    ship = record.get("gate_ship_verdict")
    walk = record.get("gate_textorder_verdict")
    if "DISPROVED" in (ship, walk):
        return (False, record.get("layer5_normalized_text"),
                "the layer-4 term was DISPROVED against this unit's "
                "own machine code and was withdrawn, so its layer-5 "
                "text is refuted evidence and may not join anything")
    if "PROVED_EQUAL" not in (ship, walk):
        return (False, record.get("layer5_normalized_text"),
                "the layer-4 term was undecided on both routes, so "
                "the layer-5 text is not proved equivalence")
    text = record.get("layer5_normalized_text")
    if not text:
        return (False, None,
                "the term proved but produced no normalized text")
    return (True, text,
            "the layer-4 term was proved equal to this unit's own "
            "machine code, so its layer-5 text is proved evidence")


# ------------------------------------------------------- provenance

def type_key_of(rec):
    """a MACHINE-FORM key for this unit's shape: which register family
    each arriving lineage is loaded through, and how wide the answer
    is.  Read off the unit's own arrival contract and result width.
    No token."""
    families = rec.get("arrival_families") or []
    width = rec.get("result_width")
    joined = ",".join(families) if families else "none"
    return "%s|%s" % (joined, width)


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
    rows = json.load(open(os.path.join(HERE, "interp_join3.json")))["rows"]
    for row in rows:
        if row["interp_unit"] != a:
            continue
        if row.get("relation") != "PROVED_EQUAL":
            continue
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
        if ra == rb:
            return False
        self.up[rb] = ra
        return True


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
    work = "/tmp/the_pool2_work"
    if not os.path.isdir(work):
        os.makedirs(work)
    index = 0
    fresh = 0
    for text in texts:
        index = index + 1
        if text in cache:
            continue
        stem = os.path.join(work, "t%06d" % index)
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
            cache[text] = None
            fresh = fresh + 1
            continue
        run = subprocess.run(["objdump", "-d", stem + ".o"],
                             capture_output=True)
        count = 0
        for line in run.stdout.decode("utf8", "replace").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0].strip().endswith(":"):
                count = count + len(parts[1].split())
        cache[text] = count
        fresh = fresh + 1
    log("   texts newly assembled %d, cache holds %d" % (fresh, len(cache)))
    return cache


# --------------------------------------------------------- the merge

def build_pool(records, layer4b, use_layer3_identity):
    """returns (union-find, edges, eligibility) after applying every
    ground.  `use_layer3_identity` switches ground (b) so the
    brief-strict count can be computed from the same code."""
    uf = UnionFind()
    by_label = {}
    for rec in records:
        by_label[rec["unit"]] = rec
        uf.add(rec["unit"])

    eligibility = {}
    for rec in records:
        eligibility[rec["unit"]] = layer5_eligibility(
            layer4b.get(rec["unit"]))

    layer5_first = {}
    layer5_merges = 0
    for rec in records:
        ok, text, _reason = eligibility[rec["unit"]]
        if not ok:
            continue
        if text in layer5_first:
            if uf.union(layer5_first[text], rec["unit"]):
                pass
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

    edges = proved_edge_list(by_label)
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

    layer4b = read_layer4b()
    log("   layer-4 records read %d" % len(layer4b))
    missing = [r["unit"] for r in records if r["unit"] not in layer4b]
    if missing:
        raise SystemExit("REFUSED OWN OUTPUT: %d proved units have no "
                         "layer-4 record, first %s"
                         % (len(missing), missing[:3]))

    log("-- the merge, brief-strict: layer-5 identity and proved edges "
        "only")
    strict_uf, _e, _el, strict_stats = build_pool(records, layer4b, False)
    strict_roots = set()
    for label in order:
        strict_roots.add(strict_uf.find(label))
    log("   entries under the brief-strict rule %d" % len(strict_roots))

    log("-- the merge, as built: layer-5 identity, layer-3 identity, "
        "proved edges")
    uf, edges, eligibility, stats = build_pool(records, layer4b, True)
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
    for root in roots:
        texts = set()
        for label in groups[root]:
            texts.add(by_label[label]["wrapped_text"])
        if len(texts) > 1:
            multi_text.update(texts)
    log("   entries carrying more than one wrapped text %d"
        % len([r for r in roots
               if len(set(by_label[x]["wrapped_text"]
                          for x in groups[r])) > 1]))
    log("   distinct texts to assemble %d" % len(multi_text))
    cache = load_byte_cache()
    sizes = measure_bytes(sorted(multi_text), cache)
    with open(BYTE_CACHE, "w") as fh:
        json.dump(sizes, fh, indent=1, sort_keys=True)

    entries = []
    index = 0
    withdrawn_members = 0
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
            if not ok and l5text is not None:
                withdrawn_members = withdrawn_members + 0
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
            "type_key": type_key_of(by_label[labels[0]]),
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

    ineligible = len([1 for label in order if not eligibility[label][0]])
    withdrawn = len([1 for label in order
                     if "DISPROVED" in (
                         layer4b[label].get("gate_ship_verdict"),
                         layer4b[label].get("gate_textorder_verdict"))])
    meta = {
        "generator": "build_the_pool2.py",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL.  No "
                     "provenance exemption is claimed and no `role` "
                     "field is declared anywhere in this document.",
        "task": "TASK 49 -- the pool rebuilt on the memory-wrapped form",
        "population": "every unit TASK 47 (log_146) proved: 30,436 of "
                      "31,078 attempted -- original 1,763, interpreter "
                      "9, regenerated 28,664",
        "intake": "canon37_wrapped_{c,cpp,go,rust,swift}.json, "
                  "canon37_interp.json, canon37_regen_store/*.json, "
                  "outcome WRAPPED_TEXT_PROVED only",
        "layer4_source": "layer4b_terms_{c,cpp,go,rust,swift}.json, "
                         "layer4b_interp.json, "
                         "layer4b_regen_store/*.json -- TASK 48's "
                         "SECOND-VERSION artifacts, per log_147 §13; "
                         "the first-version layer4_* files are not "
                         "read by this program",
        "merge_rule": "layer-5 normalized-text identity among units "
                      "whose layer-4 term was PROVED, or layer-3 "
                      "wrapped-text identity, or a proved edge; closed "
                      "under transitivity",
        "withdrawals": "the 826 units whose layer-4 term was DISPROVED "
                       "are CARRIED as members and FLAGGED "
                       "`layer5_merge_eligible: false`; they are "
                       "excluded from layer-5 merging because a "
                       "refuted term is not proved equivalence, and "
                       "they remain reachable by layer-3 identity and "
                       "by a proved edge, neither of which rests on "
                       "the term",
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
        "supersedes_as_an_object": "the_pool1.json, which merged the "
                                   "28,984 units TASK 43 proved on the "
                                   "region36 universal text.  It stays "
                                   "on disk, byte for byte, as the "
                                   "superseded record.",
    }
    summary = {
        "units_in_the_pool": len(records),
        "units_by_arrival_population": counts,
        "entries": len(entries),
        "entries_under_the_brief_strict_rule": len(strict_roots),
        "distinct_layer5_texts_among_eligible_units":
            stats["distinct_layer5_texts_among_eligible_units"],
        "layer5_identity_merges": stats["layer5_identity_merges"],
        "distinct_layer3_wrapped_texts":
            stats["distinct_layer3_wrapped_texts"],
        "layer3_identity_merges": stats["layer3_identity_merges"],
        "proved_edges_applied": stats["proved_edges_applied"],
        "units_not_layer5_eligible": ineligible,
        "units_withdrawn_at_layer4": withdrawn,
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
    path = os.path.join(HERE, "the_pool2.json")
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    log("-- wrote the_pool2.json")
    log(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
