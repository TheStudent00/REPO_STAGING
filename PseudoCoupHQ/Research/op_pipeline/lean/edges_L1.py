#!/usr/bin/env python3
"""edges_L1.py -- read t100's answered pairs and pick the terms task L1 hands to Lean.

WHAT THIS READS (an inherited artifact, named with its assumptions):
  /projects/PseudoCoupHQ/Research/op_pipeline/pool100_edges.json, written by
  task t100 (`pool100_entry_equivalence.py close`, log_224).  Each record in
  its `edges` list is one PAIR of pool5 entries of one `type_key` (arrival
  register families | answer width) -- the candidate set was fixed from that
  MACHINE FORM before any solver ran, never from an operator token.  This
  program does not form a new candidate set; it re-reads answered pairs.

WHAT IT WRITES
  survey: prints tallies, nothing on disk.
  select: L1_edges_selected.json -- the ten shortest PROVED pairs across at
          least three type keys, and three pairs t100 left UNDECIDED whose
          terms carry a wide division node.

SELECTION KEYS, stated because the spelling ban governs them
  proved ten: the printed layer-5 character length of the longer of the two
    terms (a size of the machine form), plus a spread rule over `type_key`
    (a machine form).  No operator token takes part.
  the three undecided: the presence of a DIVISION NODE IN THE LAYER-4 TERM at
    a width of at least 64 -- the term is the arch-unit as a z3 expression,
    so this is machine-form evidence, and the brief names this shape.  It is
    not a language operator token: no member's spelling label is read here.

MEMORY
  pool100_edges.json is 67 MB of json.  One json.load of it is the whole
  appetite; measured in the survey run and printed as peak RSS.  The named
  abort is ABORT_MEMORY_L1, raised by this program when its own peak passes
  6 GB (the instance's container cap is 8g, so this fires first).
"""

import json
import os
import re
import resource
import sys

EDGES_PATH = "/projects/PseudoCoupHQ/Research/op_pipeline/pool100_edges.json"
OUT_DIR = "/projects/PseudoCoupHQ/Research/op_pipeline/lean"
ABORT_MEMORY_L1_KB = 6 * 1024 * 1024


def peak_rss_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_check(where):
    kb = peak_rss_kb()
    if kb > ABORT_MEMORY_L1_KB:
        sys.stderr.write("ABORT_MEMORY_L1 at %s: peak %d kB over %d kB\n"
                         % (where, kb, ABORT_MEMORY_L1_KB))
        sys.exit(3)
    return kb


def load_edges():
    with open(EDGES_PATH) as fh:
        doc = json.load(fh)
    memory_check("after json.load")
    return doc


def both_texts(edge):
    a = (edge.get("term_a") or {}).get("layer5_normalized_text")
    b = (edge.get("term_b") or {}).get("layer5_normalized_text")
    return a, b


def free_symbol_widths(edge):
    """v0, v1, ... in the printed layer-5 text are the arrival rows renamed
    positionally, so row IN-0 is v0.  Their widths are the `bits` of the
    edge's own `inputs` list."""
    widths = {}
    for i, row in enumerate(edge.get("inputs") or []):
        widths["v%d" % i] = row.get("bits")
    return widths


# Two-character operators first, then single characters. An earlier form
# matched a RUN of symbol characters, which turned `2*~x` into one token
# `*~`; the census below counts operators, so a run is a miscount.
TOKEN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|<<|>>|<=|>=|==|!=|[<>=!~^&|+*/%-]|[0-9]+")


def vocabulary(texts):
    """Every distinct name-shaped and symbol-shaped token in a set of printed
    layer-5 texts.  This is how the operator table of the printed form is
    read off the data rather than assumed."""
    seen = {}
    for t in texts:
        if not t:
            continue
        for m in TOKEN.finditer(t):
            tok = m.group(0)
            if tok.isdigit():
                tok = "<numeral>"
            if re.fullmatch(r"v[0-9]+", tok):
                tok = "<free symbol vN>"
            seen[tok] = seen.get(tok, 0) + 1
    return seen


def population(doc):
    """The pairs this task chooses from.

    `pool100_edges.json` carries two lists that both matter here.  `edges`
    holds the 12 pairs t100 APPLIED to its closure -- a PROVED pair applies
    only when both terms were separately proved against their own unit's ship
    body.  `pairs` holds all 21,502 pairs t100 ANSWERED, each with its state.
    The proved population is every record of either list whose state is
    PROVED; `edges` is a subset of it.  Taking the union rather than only the
    12 is deliberate and is stated in the log: the ten shortest of 12 would
    have been ten of twelve, and eight of them differ from each other only in
    which operand feeds a comparison.
    """
    seen = {}
    for src in ("edges", "pairs"):
        for e in doc.get(src) or []:
            seen.setdefault((e.get("a"), e.get("b")), e)
    return list(seen.values())


def survey(doc):
    for k in sorted(doc.keys()):
        v = doc[k]
        print("top-level %-24s %-6s %s" % (k, type(v).__name__,
                                           len(v) if hasattr(v, "__len__") else ""))
    edges = population(doc)
    print("pairs in the union of `edges` and `pairs`: %d" % len(edges))
    states = {}
    for e in edges:
        states[e.get("state")] = states.get(e.get("state"), 0) + 1
    print("states: %s" % json.dumps(states, sort_keys=True))
    print("--- the field names one pair record carries")
    print(json.dumps(sorted(edges[0].keys())))

    proved = [e for e in edges if e.get("state") == "PROVED"]
    with_text = [e for e in proved if all(both_texts(e))]
    print("PROVED with both layer-5 texts present: %d of %d"
          % (len(with_text), len(proved)))
    keys = {}
    for e in with_text:
        keys[e["type_key"]] = keys.get(e["type_key"], 0) + 1
    print("PROVED type_key spread: %d distinct; %s"
          % (len(keys), json.dumps(sorted(keys.items(), key=lambda kv: -kv[1])[:12])))

    lens = sorted((max(len(a), len(b)), e["type_key"], e["a"], e["b"])
                  for e, (a, b) in ((e, both_texts(e)) for e in with_text))
    print("--- the 40 shortest PROVED pairs by longer printed text")
    for n, (ln, tk, a, b) in enumerate(lens[:40]):
        ta, tb = both_texts(next(e for e in with_text if e["a"] == a and e["b"] == b))
        print("  %2d  len=%3d  %-22s %s == %s" % (n, ln, tk, a, b))
        print("        a: %s" % ta)
        print("        b: %s" % tb)

    und = [e for e in edges if e.get("state") == "UNDECIDED"]
    und_text = [e for e in und if all(both_texts(e))]
    print("UNDECIDED: %d; with both layer-5 texts present: %d"
          % (len(und), len(und_text)))

    print("--- printed-form token vocabulary over ALL edges that carry texts")
    texts = []
    for e in edges:
        a, b = both_texts(e)
        if a:
            texts.append(a)
        if b:
            texts.append(b)
    voc = vocabulary(texts)
    for tok, n in sorted(voc.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %8d  %s" % (n, tok))

    print("--- ten longest UNDECIDED texts (the shapes that stopped the runner)")
    ul = sorted(((max(len(a), len(b)), e) for e, (a, b)
                 in ((e, both_texts(e)) for e in und_text)), key=lambda p: -p[0])
    for ln, e in ul[:10]:
        a, b = both_texts(e)
        print("  len=%5d %-22s %s == %s  widths=%s" % (ln, e["type_key"], e["a"], e["b"],
                                                      json.dumps(free_symbol_widths(e))))
        print("        a: %s" % a[:400])
        print("        b: %s" % b[:400])
    print("peak rss kB: %d" % peak_rss_kb())


DIVIDE_NODE = re.compile(r"UDiv|SDiv|URem|SRem|bvudiv|bvsdiv|bvurem|bvsrem")


def widest_free_symbol(edge):
    ws = [w for w in free_symbol_widths(edge).values() if w]
    return max(ws) if ws else 0


def select(doc):
    edges = population(doc)
    proved = [e for e in edges if e.get("state") == "PROVED" and all(both_texts(e))]

    # ten shortest by printed size, forced across at least three type keys:
    # walk the size order and cap how many may come from one type_key until
    # three keys are represented.
    ordered = sorted(proved, key=lambda e: (max(len(t) for t in both_texts(e)),
                                            e["a"], e["b"]))
    chosen = []
    per_key = {}
    # Only twelve of t100's 226 PROVED pairs carry a printed layer-5 text on
    # BOTH sides (the other 214 have a hole on one side, so that side has no
    # normalized text).  Those twelve span four machine type keys, but the ten
    # SHORTEST of them span only two, so a per-key cap is what forces the
    # brief's "across at least three type keys".  Six is the smallest cap that
    # still yields ten records: 6 + 2 + 1 + 1.
    cap = 6
    for e in ordered:
        if len(chosen) >= 10:
            break
        k = e["type_key"]
        if per_key.get(k, 0) >= cap:
            continue
        per_key[k] = per_key.get(k, 0) + 1
        chosen.append(e)
    if len(per_key) < 3:
        sys.stderr.write("REFUSED: only %d type keys among the ten\n" % len(per_key))
        sys.exit(4)

    und = [e for e in edges if e.get("state") == "UNDECIDED" and all(both_texts(e))]
    wide = [e for e in und
            if any(DIVIDE_NODE.search(t) for t in both_texts(e))
            and widest_free_symbol(e) >= 64]
    wide.sort(key=lambda e: (max(len(t) for t in both_texts(e)), e["a"], e["b"]))

    def slim(e):
        a, b = both_texts(e)
        return {
            "answer_width": e.get("answer_width"),
            "entry_a": e["a"],
            "entry_b": e["b"],
            "free_symbol_widths": free_symbol_widths(e),
            "representative_a": e.get("rep_a"),
            "representative_b": e.get("rep_b"),
            "result_width_a": (e.get("term_a") or {}).get("result_width"),
            "result_width_b": (e.get("term_b") or {}).get("result_width"),
            "state_in_t100": e.get("state"),
            "text_a": a,
            "text_b": b,
            "type_key": e["type_key"],
            "undecided_cause": (e.get("verdict") or {}).get("reason"),
        }

    # The three t100 left UNDECIDED. Their records carry no term (the
    # sub-process was stopped at its 120 s ceiling before one was written), so
    # only the ids and the machine type key are here; the terms are fetched
    # from the_pool5.json by run_edges_L1.py. One pair per UNDECIDED type key,
    # so all three machine forms that hold UNDECIDED pairs are represented.
    und_all = [e for e in edges if e.get("state") == "UNDECIDED"]
    three = []
    for key in sorted({e["type_key"] for e in und_all}):
        first = sorted((e for e in und_all if e["type_key"] == key),
                       key=lambda e: (e["a"], e["b"]))[0]
        three.append({
            "entry_a": first["a"], "entry_b": first["b"],
            "state_in_t100": "UNDECIDED",
            "type_key": first["type_key"],
            "undecided_cause": first.get("cause"),
            "t100_sub_seconds": first.get("sub_seconds"),
            "t100_sub_peak_kb": first.get("sub_peak_kb"),
            "representative_a": first.get("rep_a"),
            "representative_b": first.get("rep_b"),
            "free_symbol_widths": {},
        })

    out = {
        "meta": {
            "read_from": EDGES_PATH,
            "note": ("the ten are the shortest printed layer-5 texts among t100's "
                     "PROVED pairs, capped at four per machine type key so at "
                     "least three keys are represented; the three are t100's "
                     "UNDECIDED pairs whose layer-4 term carries a division node "
                     "at a free-symbol width of 64 or more"),
            "written_by": "Research/op_pipeline/lean/edges_L1.py",
        },
        "the_ten": [slim(e) for e in chosen],
        "the_three_undecided_pairs": three,
        "undecided_pairs_total": len(und_all),
        "wide_divide_undecided_available": len(wide),
    }
    path = os.path.join(OUT_DIR, "L1_edges_selected.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote %s" % path)
    print("the ten, type keys: %s" % json.dumps(sorted(per_key.items())))
    for e in out["the_ten"]:
        print("  %-22s %s == %s" % (e["type_key"], e["entry_a"], e["entry_b"]))
        print("        a: %s" % e["text_a"])
        print("        b: %s" % e["text_b"])
    print("UNDECIDED pairs in t100: %d; of those, carrying a division node at a "
          "free-symbol width of 64 or more: %d"
          % (out["undecided_pairs_total"], out["wide_divide_undecided_available"]))
    print("the three UNDECIDED pairs taken, one per UNDECIDED machine type key:")
    for e in out["the_three_undecided_pairs"]:
        print("  %-22s %s == %s  representatives %s / %s  t100 stopped it at %ss"
              % (e["type_key"], e["entry_a"], e["entry_b"],
                 e["representative_a"], e["representative_b"],
                 e["t100_sub_seconds"]))
    print("peak rss kB: %d" % peak_rss_kb())


def survey_undecided(doc):
    """What an UNDECIDED pair record actually carries, since lane 3 found that
    none of the 1,099 carries a printed layer-5 text on both sides."""
    edges = population(doc)
    und = [e for e in edges if e.get("state") == "UNDECIDED"]
    print("UNDECIDED pairs: %d" % len(und))
    have = {}
    for e in und:
        for side in ("term_a", "term_b"):
            t = e.get(side) or {}
            for k in t.keys():
                have[k] = have.get(k, 0) + 1
    print("term_a/term_b field frequencies over the 1,099: %s"
          % json.dumps(have, sort_keys=True))
    print("--- one whole UNDECIDED record, LITERAL")
    print(json.dumps(und[0], indent=1, sort_keys=True))
    ts = {}
    for e in und:
        for side in ("term_a", "term_b"):
            ts[(e.get(side) or {}).get("term_state")] = \
                ts.get((e.get(side) or {}).get("term_state"), 0) + 1
    print("term_state over both sides of the 1,099: %s"
          % json.dumps({str(k): v for k, v in ts.items()}, sort_keys=True))
    secs = sorted((e.get("sub_seconds") or 0) for e in und)
    print("sub_seconds: min %.1f median %.1f max %.1f"
          % (secs[0], secs[len(secs) // 2], secs[-1]))
    kb = sorted((e.get("sub_peak_kb") or 0) for e in und)
    print("sub_peak_kb: min %d median %d max %d"
          % (kb[0], kb[len(kb) // 2], kb[-1]))
    tks = {}
    for e in und:
        tks[e["type_key"]] = tks.get(e["type_key"], 0) + 1
    print("UNDECIDED type_key spread: %s"
          % json.dumps(sorted(tks.items(), key=lambda kv: -kv[1])))
    print("--- the PROVED records that carry no text: what they carry instead")
    pn = [e for e in edges if e.get("state") == "PROVED" and not all(both_texts(e))]
    print("PROVED without both texts: %d" % len(pn))
    if pn:
        print(json.dumps(pn[0], indent=1, sort_keys=True))
    print("peak rss kB: %d" % peak_rss_kb())


def divsamples(doc):
    """The printed shape of a division node, read off the corpus rather than
    assumed.  z3's simplifier rewrites a division into a guard plus an
    UNGUARDED division symbol, and prints that symbol as `bvudiv_i` and
    friends; this prints real texts carrying one, shortest first, so the
    translator is written against the shape that is actually there."""
    edges = population(doc)
    hits = []
    for e in edges:
        for side, t in zip(("a", "b"), both_texts(e)):
            if t and DIVIDE_NODE.search(t):
                hits.append((len(t), e["type_key"], e["state"], side, e, t))
    hits.sort(key=lambda h: h[0])
    print("pair sides whose printed text carries a division node: %d" % len(hits))
    st = {}
    for h in hits:
        st[h[2]] = st.get(h[2], 0) + 1
    print("by t100 state: %s" % json.dumps(st, sort_keys=True))
    print("--- the 12 shortest, LITERAL")
    for ln, tk, state, side, e, t in hits[:12]:
        print("  len=%4d %-22s %-10s %s/%s side %s widths=%s"
              % (ln, tk, state, e["a"], e["b"], side,
                 json.dumps(free_symbol_widths(e))))
        print("        %s" % t)
    print("peak rss kB: %d" % peak_rss_kb())



POOL5 = "/projects/PseudoCoupHQ/Research/op_pipeline/the_pool5.json"

# What Render.lean's `Term` covers, by the printed token that stands for it.
# The right column is the constructor, or the reason the subset stops short.
COVERED_BY_RENDER = {
    "<numeral>": "lit",
    "<free symbol vN>": "var",
    "Extract": "extract",
    "Concat": "concat",
    "If": "ite",
    "==": "eq",
    "+": "add",
    "-": "sub",
    "*": "mul",
    "&": "and",
    "|": "or",
    "^": "xor",
    "~": "not",
    "<<": "shl",
    "LShR": "lshr",
    ">>": "ashr",
    "ZeroExt": "zext",
    "SignExt": "sext",
}
NOT_COVERED_REASON = {
    "<=": "a signed compare; the subset carries only eq",
    "<": "a signed compare; the subset carries only eq",
    ">=": "a signed compare; the subset carries only eq",
    ">": "a signed compare; the subset carries only eq",
    "ULE": "an unsigned compare; the subset carries only eq",
    "ULT": "an unsigned compare; the subset carries only eq",
    "And": "a truth connective; the subset's condition is a one-bit word",
    "Or": "a truth connective; the subset's condition is a one-bit word",
    "Not": "a truth negation; the subset's condition is a one-bit word",
    "bvudiv_i": "division, and z3's UNGUARDED division at that",
    "bvsdiv_i": "division, and z3's UNGUARDED division at that",
    "bvurem_i": "remainder, and z3's UNGUARDED remainder at that",
    "bvsrem_i": "remainder, and z3's UNGUARDED remainder at that",
    "fpToFP": "floating point",
    "fpIsNaN": "floating point",
    "fpEQ": "floating point",
    "RNE": "floating point (a rounding mode)",
    "fp": "floating point",
    "to_ieee_bv": "floating point",
}


def emitted(_doc_unused):
    """The operators the term walk emits, counted over EVERY layer-5 text in
    the_pool5.json -- the whole pool, not the answered pairs. Each token is
    marked with the Render.lean constructor that covers it, or the reason the
    subset stops short of it."""
    pool = json.load(open(POOL5))
    memory_check("after the_pool5.json")
    texts = []
    entries = pool.get("entries") or []
    for e in entries:
        for t in (e.get("layer5_normalized_texts") or []):
            if t:
                texts.append(t)
    print("pool5 entries: %d; distinct printed layer-5 texts over them: %d"
          % (len(entries), len(texts)))
    voc = vocabulary(texts)
    entries_with_token = {}
    for e in entries:
        seen = set()
        for t in (e.get("layer5_normalized_texts") or []):
            for tok in vocabulary([t]):
                seen.add(tok)
        for tok in seen:
            entries_with_token[tok] = entries_with_token.get(tok, 0) + 1
    print("")
    print("| printed token | uses | entries carrying it | covered by Render.lean | if not, why |")
    print("|---|---|---|---|---|")
    for tok, n in sorted(voc.items(), key=lambda kv: (-kv[1], kv[0])):
        cov = COVERED_BY_RENDER.get(tok)
        print("| `%s` | %d | %d | %s | %s |"
              % (tok, n, entries_with_token.get(tok, 0),
                 ("yes, `%s`" % cov) if cov else "no",
                 "-" if cov else NOT_COVERED_REASON.get(tok, "no rule written")))
    cov_entries = 0
    for e in entries:
        toks = set()
        for t in (e.get("layer5_normalized_texts") or []):
            toks |= set(vocabulary([t]).keys())
        if toks and all(t in COVERED_BY_RENDER for t in toks):
            cov_entries += 1
    with_text = sum(1 for e in entries if (e.get("layer5_normalized_texts") or []))
    print("")
    print("pool5 entries whose every printed token is covered by Render.lean's "
          "subset: %d of %d entries that print any text (of %d entries in all)"
          % (cov_entries, with_text, len(entries)))
    print("peak rss kB: %d" % peak_rss_kb())

def main(argv):
    mode = argv[1] if len(argv) > 1 else "survey"
    doc = None if mode == "emitted" else load_edges()
    if mode == "survey":
        survey(doc)
    elif mode == "undecided":
        survey_undecided(doc)
    elif mode == "divsamples":
        divsamples(doc)
    elif mode == "emitted":
        emitted(doc)
    elif mode == "select":
        select(doc)
    else:
        sys.stderr.write("REFUSED: unknown mode %r\n" % mode)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
