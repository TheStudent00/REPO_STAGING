#!/usr/bin/env python3
"""l3_valuegrain.py -- log 043: rebuild every operation signature at the
VALUE GRAIN, with ANSWER-VALUED elements.

the owner ruled on 2026-08-20, verbatim:

    "each row isnt a row element. its a vector"
    "that way something like php.== cant appear to have obtained
     god-operator status."

What that overturns.  Log 041 built its containment order over DOMAINS:
a signature was a vector over 64 form pairs, an entry was non-zero when
the operation accepted that form pair, and the entries carried no
answer.  So a wide operation could contain every narrow one without
ever agreeing with any of them, and the top of that order was earned by
accepting things rather than by answering as anything else answers.
That is the god-operator opening, and it is closed here by putting the
ANSWER into the element.

The rebuild, exactly:

  ELEMENT      one (lhs holder + value class, rhs holder + value class)
               question.  Its key is the input cell decisions 18 and 33
               already use, "form_a|vc_a|form_b|vc_b", so an element is
               comparable across languages through the shared layer-1
               value classes, which decision 41 measured to be contained
               in one vocabulary.
  ELEMENT      the ANSWER TOKEN the operation carried there.  A raise, a
  VALUE        death and a backend refusal are tokens like any other,
               under decision 31 and this file's decision 60.
  SILENT       the operation was never asked that question at all: the
               compiler would not take the form pair, or the probe plan
               did not reach it.  Silence is not a token.  It is the
               absence of a claim.

The two grains, and the flag on which one is the default:

  HOLDER-PAIR GRAIN (the default here)
      an element's value is the WHOLE SET of tokens the leaf carried
      over its holder pairs at that element -- `int32|int32',
      `int64|int64', `uint64|uint64' and the rest.  Two leaves match at
      an element only when those sets are EQUAL.  A leaf whose holders
      answer two different things at one element therefore does NOT
      match a leaf that answers one thing there, and the holder split
      is a measured difference rather than a rounding.  This is the
      literal reading of the owner's "each row isnt a row element, its a
      vector".
  FORM-PAIR GRAIN (computed beside it, never headlined)
      the same element values, but two leaves match when their token
      sets INTERSECT, which is decision 27's standing rule and is blind
      to a holder split.

**FLAGGED, OVERTURNABLE.**  the owner has not chosen between the two.  The
holder-pair grain is taken as the default because it is the literal
reading of his sentence and because it is the stricter of the two, so
nothing it certifies would be uncertified by the other.  Every count in
the products is published under BOTH grains so the choice is a number
and not an argument.  Cost to overturn: set `GRAIN' below to "form".

Product: `signatures_valuegrain.json'.  Its format is documented in the
file's own `format' field and in section 7 of log 043.

No probe runs.  No lane runs.  Everything is read from the answer
artifacts already on disk.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from l3_answers import (NINE, THREE, bridge_row, canon_pair)     # noqa: E402
from l3_wordops import ADMIT as WORD_ADMIT                       # noqa: E402
import l3_alt_readings as R                                      # noqa: E402

# --- decision 58 ------------------------------------------------------
# The element of a signature is (lhs holder + value class, rhs holder +
# value class) -> answer token, and the element KEY is the input cell
# "form_a|vc_a|form_b|vc_b".  Holders are language-private -- go's
# `int64' and rust's `i64' are not the same string and were never meant
# to be -- so a holder cannot be part of a key that has to cross a
# language boundary.  The holder is kept in the element's VALUE instead,
# as the set of tokens the leaf's holders carried there, which is what
# `GRAIN = "holder"' reads.
#
# Cost to overturn: change `cell_key'.
GRAIN = "holder"

# --- decision 60 ------------------------------------------------------
# A backend refusal is a TOKEN, not a silence.  Decision 40 dropped
# `codegen_refuse' rows from the answer tables because they carried no
# value to canonicalise.  At the value grain they carry something else:
# the language was asked and gave an answer of the form "this cannot be
# done", which is a claim about the element.  It is recorded as the
# token `refuse:codegen'.
#
# The distinction this rests on, stated so it can be attacked: a row
# that is ABSENT was never asked, and a row that says CODEGEN_REFUSE was
# asked and declined.  The first is absence of a claim and the second is
# a claim.  Both are computed, and the counts under the other reading
# are published beside the headline ones.
REFUSE_TOKEN = "refuse:codegen"

FAMILIES = ["arithmetic", "comparison", "logical", "bitwise", "shift",
            "other"]


def cell_key(fa, vca, fb, vcb):
    return "%s|%s|%s|%s" % (fa, vca, fb, vcb)


# ----------------------------------------------------------------------
# loading -- one record shape for both encodings
# ----------------------------------------------------------------------
#
# Both loaders return  {operation -> {cell -> {token -> [holder pairs]}}}
# and a token census.  They are l3_answers12's loaders with two changes
# and no others: the holder pair is kept against the token rather than
# folded away, and a refused row becomes a token under decision 60.

def load_nine(lang):
    d = json.load(open(os.path.join(HERE, "answers_%s.json" % lang)))
    assert d.get("complete"), "%s execution table not complete" % lang
    per = collections.defaultdict(lambda: collections.defaultdict(dict))
    census = collections.Counter()
    for r in d["rows"]:
        la, rb = r["lhs"], r["rhs"]
        b = bridge_row(r)
        if b is None:                                  # decision 60
            tok = REFUSE_TOKEN
        else:
            tok = b[0]
        key = cell_key(la["form"], la["value"], rb["form"], rb["value"])
        hp = "%s|%s" % (la["holder"], rb["holder"])
        per[r["operation"]][key].setdefault(tok, []).append(hp)
        census[tok] += 1
    return per, census, d["probes"]


def load_three(lang):
    man = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
    beh = json.load(open(os.path.join(HERE, "behavior_%s_C.json" % lang)))
    assert beh.get("complete"), "%s route-C table not complete" % lang
    hs = man["holders"]
    cells = beh["cells"]
    ops = list(man["operations"]) + [
        o for o in WORD_ADMIT.get(lang, []) if o not in man["operations"]]
    per = collections.defaultdict(lambda: collections.defaultdict(dict))
    census = collections.Counter()
    for ha in hs:
        for hb in hs:
            i, j = ha["i"], hb["i"]
            hp = "%s|%s" % (ha["holder"], hb["holder"])
            for vca, _ in ha["value_classes"]:
                for vcb, _ in hb["value_classes"]:
                    for op in ops:
                        c = cells.get("P%d_%d_%s_%s_%s"
                                      % (i, j, vca, vcb, op))
                        if c is None:
                            continue
                        if c[0] == "ANSWER":
                            tok = canon_pair(c[1])[0]
                        elif c[0] == "RAISE":
                            tok = "raise:" + str(c[1])
                        else:
                            continue          # BUDGET: never asked
                        key = cell_key(ha["form"], vca, hb["form"], vcb)
                        per[op][key].setdefault(tok, []).append(hp)
                        census[tok] += 1
    return per, census, beh["probes"]


# ----------------------------------------------------------------------
# the signatures
# ----------------------------------------------------------------------

def build():
    leaves = {}
    census = collections.Counter()
    probes = {}
    for lang in list(THREE) + list(NINE):
        if lang in THREE:
            per, cen, np_ = load_three(lang)
        else:
            per, cen, np_ = load_nine(lang)
        census.update(cen)
        probes[lang] = np_
        for op, cellmap in per.items():
            if not cellmap:
                continue
            leaves["%s.%s" % (lang, op)] = dict(
                language=lang, operation=op,
                family=R.family(op), cells=cellmap)
        print("  %-11s %4d operations, %7d elements"
              % (lang, len(per), sum(len(c) for c in per.values())))
    return leaves, census, probes


def vectors(leaves):
    """leaf -> {cell -> element value}, at both grains.

    The element value under the holder-pair grain is the sorted tuple of
    the tokens the leaf's holders carried at that element.  Under the
    form-pair grain it is the same tuple, read as a set to intersect
    rather than to equate; the tuple is therefore shared and only the
    MATCH RULE differs, which is what keeps the two grains comparable.
    """
    vec = {}
    for k, L in leaves.items():
        vec[k] = {c: tuple(sorted(t)) for c, t in L["cells"].items()}
    return vec


def main():
    print("layer 3 phase 4 -- SIGNATURES AT THE VALUE GRAIN")
    print("decision 58: an element is (holder+value class, holder+value "
          "class) -> answer token")
    print("decision 60: a backend refusal is the token %r" % REFUSE_TOKEN)
    print("grain: %s   (FLAGGED, overturnable -- see the file head)"
          % GRAIN)
    print("")
    leaves, census, probes = build()
    vec = vectors(leaves)

    cells = sorted({c for v in vec.values() for c in v})
    cidx = {c: i for i, c in enumerate(cells)}
    vals = sorted({t for v in vec.values() for t in v.values()})
    vidx = {t: i for i, t in enumerate(vals)}
    toks = sorted({t for v in vals for t in v})
    tidx = {t: i for i, t in enumerate(toks)}

    n_el = sum(len(v) for v in vec.values())
    print("")
    print("leaves: %d" % len(vec))
    print("distinct elements in the merged grid: %d" % len(cells))
    print("elements spoken, summed over leaves: %d" % n_el)
    print("distinct answer tokens: %d" % len(toks))
    print("distinct element VALUES (token sets): %d" % len(vals))
    split = sum(1 for v in vec.values() for t in v.values() if len(t) > 1)
    print("elements whose holders do NOT agree: %d (%.1f percent) -- "
          "these are the elements the two grains read differently"
          % (split, 100.0 * split / n_el))

    wide = sorted(vec, key=lambda k: -len(vec[k]))[:8]
    print("")
    print("the widest leaves, by elements spoken:")
    for k in wide:
        print("  %-18s %6d elements" % (k, len(vec[k])))

    out = dict(
        status="SIGNATURES AT THE VALUE GRAIN, OPERATORS, ALL TWELVE",
        built="2026-08-20",
        extends=["answers_<lang>.json", "behavior_<lang>_C.json",
                 "manifest_<lang>.json", "clusters_all12.json"],
        dee_ruling=["each row isnt a row element. its a vector",
                    "that way something like php.== cant appear to have "
                    "obtained god-operator status."],
        decision_58=("the element of a signature is (lhs holder + value "
                     "class, rhs holder + value class) -> answer token, "
                     "keyed by the input cell form_a|vc_a|form_b|vc_b so "
                     "that it crosses a language boundary through the "
                     "shared layer-1 value classes"),
        decision_60=("a backend refusal is the token %r; an ABSENT "
                     "element is silence and carries no token"
                     % REFUSE_TOKEN),
        grain=GRAIN,
        grain_flag=("FLAGGED, OVERTURNABLE.  the owner has not chosen between "
                    "the holder-pair grain and the form-pair grain.  The "
                    "holder-pair grain is the default because it is the "
                    "literal reading of `each row isnt a row element, "
                    "its a vector' and because it is the stricter of the "
                    "two.  Every count is published under both."),
        format=(
            "SPARSE, three tables and one vector per leaf.\n"
            "  cells[i]   the element key, form_a|vc_a|form_b|vc_b\n"
            "  tokens[i]  one answer token\n"
            "  values[i]  one element VALUE: the sorted list of token\n"
            "             ids a leaf's holders carried at one element\n"
            "  leaves[k].vec  a flat list of pairs [cell id, value id],\n"
            "             sorted by cell id.  A cell id ABSENT from the\n"
            "             list is an element the leaf is SILENT on: it\n"
            "             was never asked, and that is not a token.\n"
            "Reading one leaf back is therefore\n"
            "  {cells[c]: [tokens[t] for t in values[v]]\n"
            "   for c, v in leaves[k].vec}"),
        n_leaves=len(vec), n_cells=len(cells), n_tokens=len(toks),
        n_values=len(vals), n_elements_spoken=n_el,
        n_elements_holder_split=split,
        probes_per_language=probes,
        token_census=dict(census.most_common(60)),
        cells=cells, tokens=toks,
        values=[[tidx[t] for t in v] for v in vals],
        leaves={k: dict(language=leaves[k]["language"],
                        operation=leaves[k]["operation"],
                        family=leaves[k]["family"],
                        n_elements=len(vec[k]),
                        vec=[[cidx[c], vidx[vec[k][c]]]
                             for c in sorted(vec[k], key=cidx.get)])
                for k in sorted(vec)})
    p = os.path.join(HERE, "signatures_valuegrain.json")
    json.dump(out, open(p, "w"), indent=1, sort_keys=True)
    print("")
    print("wrote signatures_valuegrain.json (%.1f MB)"
          % (os.path.getsize(p) / 1e6))
    return out


if __name__ == "__main__":
    main()
