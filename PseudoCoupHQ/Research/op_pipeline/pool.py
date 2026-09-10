#!/usr/bin/env python3
"""pool.py -- THE NODE `pool`, node 0_3_5_7 of the compiler graph.

CORE:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_7_pool/CORE_0_3_5_7_pool.md`
and its sub-node COREs: `entry`, `merge_grounds`, `representative`,
`families`, `exception_families`.

WHAT THIS FILE IS, in the CORE's own words.  ONE pool of every
canonicalized arch-unit of every language, in which units proved
equivalent collapse into one entry.  An entry is one distinct
computation; its members carry language, arrival population and
arrival annotation as COLUMNS.  There is no compiled table and no
interpreter table; anyone needing one filters the pool.

THE CLASS IS `Pool`, and its methods are the CORE's sub-nodes:

    merge               units -> entries, closed under transitivity,
                        on the three merge grounds only
    compare             (pool_a, pool_b) -> every split and every
                        merge with its COMPUTED cause
    representative      per entry, the member with the fewest
                        assembled bytes, ties by first-in-list
    families            the dom_op rule over the entries
    exception_families  guard condition-and-response identity over
                        the entries

THE THREE GROUNDS, and only three (merge_grounds CORE):
  1. layer-3 identity -- two units whose WRAPPED TEXTS are the same
     string are the same machine code twice; equivalence by
     construction, no solver asked.
  2. layer-5 identity -- two units whose NORMALIZED TERMS are the same
     string, and ONLY when both terms were PROVED equal to their own
     unit's machine code.  An unproved term is not a weaker key; it is
     no key.
  3. a proved edge -- a pair an earlier prover established equal, read
     from the banked edge files.
The join is closed under transitivity.  The two-ground count is
RECORDED on the artifact as `entries_under_the_brief_strict_rule` and
is used for nothing.

WHAT IS COPIED, AND FROM WHERE.  `build_the_pool2.py` and
`build_the_pool3.py` are superseded records: they are neither edited
nor imported.  Three pieces of theirs are UNCHANGED and are copied
into this file with this line saying so -- the union-find, the
`as`/`objdump` byte measurement, and the proved-edge reader.  The
dom_op rule is NOT copied: `dom_ops.py` is imported unchanged, as the
families CORE requires, so it cannot drift between builds.

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

No operator token appears in this file.  `operator` on a member and
`label` on a family node are DISPLAY fields, read by nothing here.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops                                                   # noqa: E402
import dom_ops_0branch as arity                                  # noqa: E402

ARITY_SOURCE = ("read off the unit's own entry contract -- does a "
                "second lineage arrive at all")
EXCLUDED_HEAD = "continue-with-a-different-answer"

LANGS = ["c", "cpp", "go", "rust", "swift"]
PROVED = "WRAPPED_TEXT_PROVED"
BYTE_CACHE = os.path.join(HERE, "the_pool4_bytes.json")


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ==================================================================
# section 1: the union-find
#
# COPIED UNCHANGED from `build_the_pool2.py` (a superseded record,
# neither edited nor imported).  It is the transitive closure of the
# merge grounds and nothing else.
# ==================================================================

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


# ==================================================================
# section 2: intake
# ==================================================================

def take_original(prefix):
    """the original corpus, in pool order: language in the corpus's own
    order, unit in numeric order."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "%s_wrapped_%s.json" % (prefix, lang))
        units = json.load(open(path))["units"]

        def sort_key(key):
            number = units[key].get("n")
            if number is not None and str(number).isdigit():
                return (int(number), key)
            return (10 ** 9, key)

        for key in sorted(units.keys(), key=sort_key):
            record = units[key]
            if record.get("outcome") != PROVED:
                continue
            out.append(record)
    return out


def take_interpreter(prefix):
    path = os.path.join(HERE, "%s_interp.json" % prefix)
    units = json.load(open(path))["units"]
    out = []
    for key in sorted(units.keys()):
        record = units[key]
        if record.get("outcome") != PROVED:
            continue
        out.append(record)
    return out


def take_regenerated(prefix):
    store = os.path.join(HERE, "%s_regen_store" % prefix)
    out = []
    for name in sorted(os.listdir(store)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(store, name)
        units = json.load(open(path))["units"]
        for key in sorted(units.keys()):
            record = units[key]
            if record.get("outcome") != PROVED:
                continue
            out.append(record)
    return out


def take_all(prefix="canon39"):
    records = []
    records.extend(take_original(prefix))
    records.extend(take_interpreter(prefix))
    records.extend(take_regenerated(prefix))
    return records


def read_terms(store="term61_store"):
    """unit label -> the layer-4 / layer-5 record `term61_run.py`
    wrote for it."""
    out = {}
    pattern = os.path.join(HERE, store, "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


# ==================================================================
# section 3: layer-5 eligibility -- only a PROVED term counts
# ==================================================================

def layer5_eligibility(record):
    """(eligible, layer-5 text or None, the reason, stated).

    Eligible means: a term was built, z3 PROVED it equal to the unit's
    own machine code on at least one route, no route DISPROVED it, and
    a normalized text exists.  Anything else is not proved equivalence
    and may not merge by text.  (The shape is `build_the_pool2.py`'s,
    read against `term.py`'s own field names.)"""
    if record is None:
        return (False, None,
                "no layer-4 record exists for this unit")
    if record.get("term_state") != "TERM":
        return (False, None,
                "no layer-4 term was built for this unit, so it has "
                "no layer-5 text to be identical to")
    outcome = record.get("outcome")
    if outcome == "DISPROVED":
        return (False, record.get("layer5_normalized_text"),
                "the layer-4 term was DISPROVED against this unit's "
                "own machine code and was withdrawn, so its layer-5 "
                "text is refuted evidence and may not join anything")
    if not record.get("proved"):
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


def type_key_of(record):
    """a MACHINE-FORM key for this unit's shape: which register family
    each arriving lineage is loaded through, and how wide the answer
    is.  Read off the unit's own arrival contract and result width.
    No token.  (Copied unchanged from `build_the_pool2.py`.)"""
    families = record.get("arrival_families") or []
    width = record.get("result_width")
    if families:
        joined = ",".join(families)
    else:
        joined = "none"
    return "%s|%s" % (joined, width)


# ==================================================================
# section 4: the proved edges
#
# COPIED UNCHANGED in shape from `build_the_pool2.proved_edge_list`
# (a superseded record, neither edited nor imported).
# ==================================================================

def proved_edge_list(present):
    """every proved edge whose BOTH endpoints are units of the pool,
    each carrying the ground that made it."""
    out = []
    for name in ["proved_edges.json", "proved_edges2.json",
                 "proved_edges3.json"]:
        path = os.path.join(HERE, name)
        document = json.load(open(path))
        for pair in document["pairs"]:
            if pair.get("verdict") != "PROVED":
                continue
            left = pair["a"]
            right = pair["b"]
            if left not in present:
                continue
            if right not in present:
                continue
            out.append({
                "left": left,
                "right": right,
                "ground": "a proved edge of the cross-unit prover",
                "source_artifact": name,
                "detail": pair.get("detail"),
                "proof_method": pair.get("proof_method"),
            })
    path = os.path.join(HERE, "interp_join3.json")
    document = json.load(open(path))
    by_class = {}
    for row in document["rows"]:
        by_class.setdefault(row["interp_class_id"], row["interp_unit"])
    for row in document["rows"]:
        if row.get("relation") != "PROVED_EQUAL":
            continue
        left = row["interp_unit"]
        right = row.get("compiled_unit")
        if left not in present:
            continue
        if right not in present:
            continue
        out.append({
            "left": left,
            "right": right,
            "ground": "a PROVED_EQUAL relation of the interpreter join",
            "source_artifact": "interp_join3.json",
            "detail": row.get("evidence"),
            "scope": row.get("scope"),
            "evidence_class": row.get("evidence_class"),
            "established_by": row.get("established_by"),
        })
    for edge in document["interpreter_to_interpreter_edges"]:
        if edge.get("relation") != "PROVED_EQUAL":
            continue
        left = by_class.get(edge["left_class_id"])
        right = by_class.get(edge["right_class_id"])
        if left not in present:
            continue
        if right not in present:
            continue
        out.append({
            "left": left,
            "right": right,
            "ground": "a proved interpreter-to-interpreter edge of the "
                      "interpreter join",
            "source_artifact": "interp_join3.json",
            "detail": edge.get("detail"),
        })
    path = os.path.join(HERE, "interp_fastpath.json")
    fastpath = json.load(open(path))
    left = "%s/%s" % (fastpath["unit"]["lang"], fastpath["unit"]["n"])
    right = None
    for row in document["rows"]:
        if row["interp_unit"] != left:
            continue
        if row.get("relation") != "PROVED_EQUAL":
            continue
        right = row["compiled_unit"]
        break
    if left in present and right in present:
        out.append({
            "left": left,
            "right": right,
            "ground": "the fast-path proof",
            "source_artifact": "interp_fastpath.json",
            "detail": fastpath["proof"].get("claim_tested"),
            "scope": "the fast path's COMPUTATION over the domain the "
                     "unit's own bytes bound",
        })
    return out


# ==================================================================
# section 5: the byte measurement
#
# COPIED UNCHANGED from `build_the_pool2.measure_bytes` (a superseded
# record, neither edited nor imported).  The bytes are MEASURED, not
# estimated: each distinct text is assembled with `as --64` and its
# bytes counted from `objdump -d`.
# ==================================================================

def load_byte_cache():
    if os.path.exists(BYTE_CACHE):
        return json.load(open(BYTE_CACHE))
    return {}


def measure_bytes(texts, cache):
    work = "/tmp/the_pool4_work"
    if not os.path.isdir(work):
        os.makedirs(work)
    index = 0
    fresh = 0
    would_not_assemble = 0
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
        handle = open(stem + ".s", "w")
        handle.write("\n".join(lines) + "\n")
        handle.close()
        run = subprocess.run(["as", "--64", "-o", stem + ".o",
                              stem + ".s"], capture_output=True)
        if run.returncode != 0:
            cache[text] = None
            fresh = fresh + 1
            would_not_assemble = would_not_assemble + 1
            continue
        run = subprocess.run(["objdump", "-d", stem + ".o"],
                             capture_output=True)
        count = 0
        for line in run.stdout.decode("utf8", "replace").splitlines():
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            if not parts[0].strip().endswith(":"):
                continue
            count = count + len(parts[1].split())
        cache[text] = count
        fresh = fresh + 1
    log("   texts newly assembled %d, would not assemble %d, cache "
        "holds %d" % (fresh, would_not_assemble, len(cache)))
    return cache


# ==================================================================
# section 6: THE NODE ITSELF -- class Pool
# ==================================================================

class Pool(object):
    """the pool of every canonicalized arch-unit of every language."""

    def __init__(self, records, terms):
        self.records = records
        self.terms = terms
        self.by_label = {}
        self.order = {}
        for record in records:
            label = record["unit"]
            if label in self.by_label:
                raise SystemExit(
                    "REFUSED OWN OUTPUT: two records claim the same "
                    "unit label %r" % label)
            self.order[label] = len(self.order)
            self.by_label[label] = record
        self.eligibility = {}
        for record in records:
            self.eligibility[record["unit"]] = layer5_eligibility(
                terms.get(record["unit"]))
        self.entries = []

    # ---------------------------------------------------------------
    # sub-node: merge             (node 0_3_5_7_2, merge_grounds)
    # ---------------------------------------------------------------

    def merge(self, use_layer3_identity=True):
        """units -> entries, closed under transitivity, on the three
        grounds only.  `use_layer3_identity` switches ground one off,
        so the brief-strict count comes from THIS code and not from a
        second rule."""
        joiner = UnionFind()
        for record in self.records:
            joiner.add(record["unit"])

        layer5_first = {}
        layer5_merges = 0
        for record in self.records:
            ok, text, _reason = self.eligibility[record["unit"]]
            if not ok:
                continue
            if text in layer5_first:
                joiner.union(layer5_first[text], record["unit"])
                layer5_merges = layer5_merges + 1
            else:
                layer5_first[text] = record["unit"]

        layer3_first = {}
        layer3_merges = 0
        for record in self.records:
            text = record.get("wrapped_text")
            if not text:
                raise SystemExit(
                    "REFUSED OWN OUTPUT: a proved unit with no wrapped "
                    "text: %s" % record["unit"])
            if text in layer3_first:
                if use_layer3_identity:
                    joiner.union(layer3_first[text], record["unit"])
                layer3_merges = layer3_merges + 1
            else:
                layer3_first[text] = record["unit"]

        edges = proved_edge_list(self.by_label)
        for edge in edges:
            joiner.union(edge["left"], edge["right"])

        stats = {
            "distinct_layer5_texts_among_eligible_units":
                len(layer5_first),
            "layer5_identity_merges": layer5_merges,
            "distinct_layer3_wrapped_texts": len(layer3_first),
            "layer3_identity_merges": layer3_merges,
            "proved_edges_applied": len(edges),
        }
        return joiner, edges, stats

    def groups_of(self, joiner):
        groups = {}
        ordered = sorted(self.order.keys(),
                         key=lambda one: self.order[one])
        for label in ordered:
            groups.setdefault(joiner.find(label), []).append(label)
        roots = sorted(groups.keys(),
                       key=lambda root: self.order[groups[root][0]])
        return groups, roots

    # ---------------------------------------------------------------
    # sub-node: representative    (node 0_3_5_7_4)
    # ---------------------------------------------------------------

    def representative(self, labels, sizes, distinct_text_count):
        """the member with the fewest assembled bytes; ties by
        first-in-list order.  Where a text will not assemble, its
        character length stands in and the substitution is STATED on
        the entry rather than hidden."""
        best = None
        for label in labels:
            text = self.by_label[label]["wrapped_text"]
            size = sizes.get(text)
            if size is None:
                size = len(text)
                if distinct_text_count > 1:
                    measured = ("the text would not assemble, so its "
                                "character length stands in and the "
                                "substitution is stated here rather "
                                "than hidden")
                else:
                    measured = ("the character length of the wrapped "
                                "text -- this entry carries one text "
                                "only, so every member ties and the "
                                "tie-break decides")
            else:
                measured = ("bytes of machine code, assembled with "
                            "`as` and counted from objdump")
            key = (size, self.order[label])
            if best is None or key < best[0]:
                best = (key, label, size, measured)
        return best

    # ---------------------------------------------------------------
    # the entries themselves      (node 0_3_5_7_1, entry)
    # ---------------------------------------------------------------

    def build_entries(self, joiner, edges, sizes):
        groups, roots = self.groups_of(joiner)
        edges_by_root = {}
        for edge in edges:
            root = joiner.find(edge["left"])
            edges_by_root.setdefault(root, []).append(edge)
        entries = []
        index = 0
        for root in roots:
            index = index + 1
            labels = groups[root]
            entry = self.one_entry(index, labels, sizes,
                                   edges_by_root.get(root, []))
            entries.append(entry)
        self.entries = entries
        return entries

    def one_entry(self, index, labels, sizes, edges):
        members = []
        langs = []
        pops = []
        texts = []
        layer5_texts = []
        for label in labels:
            record = self.by_label[label]
            ok, text, reason = self.eligibility[label]
            term = self.terms.get(label) or {}
            members.append({
                "unit": label,
                "lang": record["lang"],
                "operator": record.get("operator"),
                "population": record.get("population"),
                "arrival_annotation": record.get("arrival_annotation"),
                "wrapped_text": record["wrapped_text"],
                "layer5_normalized_text": text,
                "layer5_merge_eligible": ok,
                "layer5_merge_eligibility_reason": reason,
                "term_state": term.get("term_state"),
                "term_outcome": term.get("outcome"),
                "out_row": record.get("out_row"),
                "result_width": record.get("result_width"),
            })
            if record["lang"] not in langs:
                langs.append(record["lang"])
            if record.get("population") not in pops:
                pops.append(record.get("population"))
            if record["wrapped_text"] not in texts:
                texts.append(record["wrapped_text"])
            if ok and text not in layer5_texts:
                layer5_texts.append(text)
        best = self.representative(labels, sizes, len(texts))
        not_eligible = 0
        for member in members:
            if not member["layer5_merge_eligible"]:
                not_eligible = not_eligible + 1
        entry = {
            "entry_id": "E%05d" % index,
            "member_count": len(labels),
            "representative": best[1],
            "representative_size": best[2],
            "representative_size_measured_as": best[3],
            "representative_rule": "the simplest member -- fewest "
                                   "bytes of machine code, ties broken "
                                   "by first-in-list order",
            "languages": sorted(langs),
            "language_count": len(langs),
            "spans_more_than_one_language": len(langs) > 1,
            "arrival_populations": sorted(pops),
            "spans_compiled_and_interpreted": spans_both(pops),
            "wrapped_texts": texts,
            "distinct_wrapped_text_count": len(texts),
            "layer5_normalized_texts": layer5_texts,
            "distinct_layer5_text_count": len(layer5_texts),
            "members_not_layer5_eligible": not_eligible,
            "type_key": type_key_of(self.by_label[labels[0]]),
            "members": members,
        }
        entry["cross_language_grounds"] = self.grounds_of(labels, texts,
                                                          layer5_texts,
                                                          edges)
        return entry

    def grounds_of(self, labels, texts, layer5_texts, edges):
        """which merge ground joined which pair, said per ground."""
        grounds = []
        by_layer3 = {}
        by_layer5 = {}
        for label in labels:
            record = self.by_label[label]
            by_layer3.setdefault(record["wrapped_text"], []).append(
                record["lang"])
            ok, text, _reason = self.eligibility[label]
            if ok:
                by_layer5.setdefault(text, []).append(record["lang"])
        for text in texts:
            here = sorted(set(by_layer3[text]))
            if len(here) < 2:
                continue
            grounds.append({
                "ground": "layer-3 text identity",
                "languages_it_joins": here,
                "detail": "these members carry the SAME wrapped text, "
                          "character for character -- the same machine "
                          "code twice",
                "wrapped_text": text,
            })
        for text in layer5_texts:
            here = sorted(set(by_layer5[text]))
            if len(here) < 2:
                continue
            grounds.append({
                "ground": "layer-5 text identity",
                "languages_it_joins": here,
                "detail": "these members' layer-4 terms were each "
                          "proved equal to their own machine code and "
                          "normalize to the SAME layer-5 text",
                "layer5_normalized_text": text,
            })
        for edge in edges:
            left = self.by_label[edge["left"]]["lang"]
            right = self.by_label[edge["right"]]["lang"]
            if left == right:
                continue
            record = dict(edge)
            record["languages_it_joins"] = sorted([left, right])
            grounds.append(record)
        return grounds

    # ---------------------------------------------------------------
    # sub-node: compare           (pool CORE, `compare`)
    # ---------------------------------------------------------------

    def compare(self, before_entries, after_entries):
        """(pool_a, pool_b) -> every split and every merge with its
        COMPUTED cause, joined on MEMBER SETS.  Entry numbers are not
        compared: a renumbering is not a change."""
        before_of = {}
        for entry in before_entries:
            for member in entry["members"]:
                before_of[member["unit"]] = entry["entry_id"]
        after_of = {}
        for entry in after_entries:
            for member in entry["members"]:
                after_of[member["unit"]] = entry["entry_id"]
        before_members = {}
        for entry in before_entries:
            names = set()
            for member in entry["members"]:
                names.add(member["unit"])
            before_members[entry["entry_id"]] = names
        after_members = {}
        for entry in after_entries:
            names = set()
            for member in entry["members"]:
                names.add(member["unit"])
            after_members[entry["entry_id"]] = names

        splits = []
        merges = []
        for entry_id, names in sorted(before_members.items()):
            landed = set()
            for name in names:
                if name in after_of:
                    landed.add(after_of[name])
            if len(landed) > 1:
                splits.append({
                    "was_entry": entry_id,
                    "became_entries": sorted(landed),
                    "member_count_before": len(names),
                })
        for entry_id, names in sorted(after_members.items()):
            came_from = set()
            for name in names:
                if name in before_of:
                    came_from.add(before_of[name])
            if len(came_from) > 1:
                merges.append({
                    "entry": entry_id,
                    "joined_entries": sorted(came_from),
                    "member_count_after": len(names),
                })
        gone = []
        arrived = []
        for name in sorted(before_of):
            if name not in after_of:
                gone.append(name)
        for name in sorted(after_of):
            if name not in before_of:
                arrived.append(name)
        return {
            "entries_before": len(before_entries),
            "entries_after": len(after_entries),
            "members_before": len(before_of),
            "members_after": len(after_of),
            "splits": splits,
            "merges": merges,
            "units_no_longer_in_the_pool": gone,
            "units_new_to_the_pool": arrived,
        }

    def cause_of_split(self, entry_id, before_entries, after_entries):
        """the COMPUTED cause of one split: which ground the members
        no longer share."""
        was = None
        for entry in before_entries:
            if entry["entry_id"] == entry_id:
                was = entry
                break
        if was is None:
            return "the entry is not in the earlier pool"
        texts = set()
        keys = set()
        for member in was["members"]:
            texts.add(member.get("layer5_normalized_text"))
            record = self.terms.get(member["unit"]) or {}
            keys.add(record.get("term_state"))
        if len(texts) > 1:
            return ("the members no longer print one layer-5 text: "
                    "%d distinct texts now" % len(texts))
        if "NO_TERM" in keys:
            return ("a member lost its term, so its layer-5 key is "
                    "gone and the layer-5 ground no longer joins it")
        return ("the members' layer-3 texts and proved edges no longer "
                "join them")

    def cause_of_merge(self, entry_id, after_entries):
        """the COMPUTED cause of one merge: which ground now joins the
        members that were apart."""
        now = None
        for entry in after_entries:
            if entry["entry_id"] == entry_id:
                now = entry
                break
        if now is None:
            return "the entry is not in the later pool"
        if now["distinct_layer5_text_count"] == 1:
            if now["distinct_wrapped_text_count"] > 1:
                return ("one layer-5 text now stands over %d distinct "
                        "wrapped texts: the layer-5 ground joined them"
                        % now["distinct_wrapped_text_count"])
        for ground in now["cross_language_grounds"]:
            if ground["ground"] == "layer-5 text identity":
                return "the layer-5 ground joined them"
            if ground["ground"] == "layer-3 text identity":
                return "the layer-3 ground joined them"
        return "a proved edge joined them"

    # ---------------------------------------------------------------
    # sub-node: families          (node 0_3_5_7_5)
    # ---------------------------------------------------------------

    def families(self):
        """the dom_op rule over the entries.  The rule is IMPORTED
        from `dom_ops.py` unchanged (build_nodes, fill_nodes,
        build_edges, best_per_language, mutual_edges, components), so
        it cannot drift here.

        A node is (language, grammar-operator, ARITY) -- the
        provenance of the probe inside ONE language, never a
        cross-language token.  An edge runs only BETWEEN languages and
        is weighted by shared entry count.  Each node keeps its single
        strongest counterpart per foreign language, and the edge
        survives only when the choice is MUTUAL.  The families are the
        connected components of what survives."""
        provenance = {}
        for record in self.records:
            provenance[record["unit"]] = {
                "lang": record["lang"],
                "n": record.get("n"),
                "display_label": record.get("operator"),
                "arity_bucket": arity.arity_bucket_of(record),
                "arity_source": ARITY_SOURCE,
            }
        document = self.table_for_dom_ops()
        nodes, index = dom_ops.build_nodes(document, provenance)
        members = dom_ops.fill_nodes(document, nodes, index, provenance)
        edges = dom_ops.build_edges(document, nodes, members, 0)
        best, ties = dom_ops.best_per_language(nodes, edges)
        kept = dom_ops.mutual_edges(nodes, edges, best)
        components = dom_ops.components(kept)
        return {
            "nodes": nodes,
            "edges_raw": edges,
            "edges_mutual": kept,
            "components": components,
            "equally_strongest_ties": ties,
            "provenance": provenance,
        }

    def table_for_dom_ops(self):
        """the entries in the shape `dom_ops`' own edge builder reads:
        one row per entry, its members, and the MACHINE-FORM shape key
        standing where the compiled table carried its operand-type
        key."""
        rows = []
        for entry in self.entries:
            names = []
            for member in entry["members"]:
                names.append({"unit": member["unit"]})
            rows.append({
                "class_id": entry["entry_id"],
                "type_pair": entry["type_key"],
                "members": names,
            })
        return {"table": {"rows": rows}}

    # ---------------------------------------------------------------
    # sub-node: exception_families   (node 0_3_5_7_6)
    # ---------------------------------------------------------------

    def exception_families(self, guard_rows):
        """the same family idea applied to GUARDS rather than to
        computations.

        Guard identity is the CONDITION TESTED and the RESPONSE TAKEN
        together, never the condition alone -- the CORE's own settled
        rule.  The population is the guard rows whose unit is a member
        of THIS pool; a guard row about a unit the pool does not carry
        is counted and named, not silently folded in.  Each family
        carries the pool entries its members sit in, which is what
        makes it a rebuild OVER THE POOL rather than beside it."""
        entry_of = {}
        for entry in self.entries:
            for member in entry["members"]:
                entry_of[member["unit"]] = entry["entry_id"]
        clusters = {}
        excluded = 0
        outside = []
        considered = 0
        for row in guard_rows:
            head = response_head(row.get("response_kind"))
            if head == EXCLUDED_HEAD:
                excluded = excluded + 1
                continue
            if row["unit"] not in entry_of:
                outside.append(row["unit"])
                continue
            considered = considered + 1
            condition = normalize_condition(row.get("condition"))
            key = (condition, head)
            clusters.setdefault(key, []).append(row)
        families = []
        ordered = sorted(clusters.items(),
                         key=lambda pair: (-len(pair[1]),
                                           str(pair[0])))
        number = 0
        for key, rows in ordered:
            number = number + 1
            condition, head = key
            langs = set()
            entries_here = set()
            members = []
            for row in sorted(rows, key=lambda one: (one["language"],
                                                     one["unit"])):
                langs.add(row["language"])
                entries_here.add(entry_of[row["unit"]])
                members.append({
                    "unit": row["unit"],
                    "language": row["language"],
                    "operator": row.get("operator"),
                    "response_kind": row.get("response_kind"),
                    "detection": row.get("detection"),
                    "source": row.get("source"),
                    "pool_entry": entry_of[row["unit"]],
                })
            families.append({
                "family_id": "EF%04d" % number,
                "condition_label": condition,
                "response_head": head,
                "languages": sorted(langs),
                "language_count": len(langs),
                "member_count": len(members),
                "pool_entries": sorted(entries_here),
                "pool_entry_count": len(entries_here),
                "members": members,
            })
        return {
            "families": families,
            "rows_considered": considered,
            "rows_excluded": excluded,
            "rows_about_units_outside_the_pool": sorted(set(outside)),
        }


# ==================================================================
# section 7: the small shared helpers
# ==================================================================

def response_head(kind):
    """the head of a response kind.  COPIED UNCHANGED from
    `exception_families2.py` (a superseded record, neither edited nor
    imported)."""
    if kind is None:
        return None
    return kind.split(":")[0]


def normalize_condition(condition):
    """COPIED UNCHANGED from `exception_families2.py`."""
    if condition is None:
        return None
    return " ".join(condition.split())


def spans_both(pops):
    if "interpreter" not in pops:
        return False
    if "original" in pops:
        return True
    return "regenerated" in pops
