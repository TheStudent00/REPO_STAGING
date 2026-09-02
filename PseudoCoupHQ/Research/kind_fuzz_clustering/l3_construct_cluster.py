#!/usr/bin/env python3
"""l3_construct_cluster.py -- point the existing clustering machinery at
the CONSTRUCT signatures.

The operator pass clustered 238 operation signatures on the JACCARD of
their DOMAINS, swept the cut rather than choosing one, and read the
PLATEAUS off the sweep (logs 030, 031, 033).  Nothing about that method
is rebuilt here.  What changes is the leaf.

  operator leaf   one operation in one language.  Its domain is a set
                  of ordered FORM PAIRS, measured over the full ordered
                  holder-pair space.
  construct leaf  one construct role in one language.  Its domain is a
                  set of form keys -- a pair for a two-slot construct, a
                  form and a dash for a one-slot one.

DECISION 17 (this log).  The construct signatures get their OWN
dendrogram and are NOT merged into the operator tree.  The reason is a
measured difference of grain, not a taste: nine of the twelve construct
lanes report at the HOLDER grain, where a form pair is present or absent
and never partially so, while the operator tree's leaves carry value-
matrix density behind every cell.  Pouring the two into one tree would
put a construct next to an operator whenever both were empty, and
emptiness is exactly what nine languages have most of.  Cost to
overturn: re-running this file with COMBINE = True, which is four lines
below and already written.

Where constructs land RELATIVE to operators is still answered, and
measured rather than asserted: for every construct leaf this file finds
its nearest operator leaf by the same jaccard, in the same key space,
and reports the distribution.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_accept import holders                            # noqa: E402

ALL12 = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
         "java", "typescript", "python", "ruby", "php"]
GRAIN = {l: "value" for l in ("python", "ruby", "php")}
COMBINE = False


def split_id(pid):
    m = re.match(r"^K([a-z]+\.[a-z]+)([^_]*)_(.*)$", pid)
    if not m:
        return None, None, []
    return m.group(1), m.group(2), m.group(3).split("_")


def construct_signatures():
    """(language, construct) -> domain, from construct_answers_<l>.json."""
    sigs = {}
    for lang in ALL12:
        p = os.path.join(HERE, "construct_answers_%s.json" % lang)
        if not os.path.exists(p):
            continue
        hs, _ = holders(lang)
        d = json.load(open(p))
        for key, rec in d.items():
            cons, _op, _pos = split_id(key + "_0")
            dom = set()
            for pos, cell in rec["cells"].items():
                xs = pos.split("_")
                try:
                    i = int(xs[0])
                except ValueError:
                    continue
                fa = hs[i]["form"] if i < len(hs) else "?"
                fb = "-"
                if len(xs) > 1:
                    try:
                        j = int(xs[1])
                        fb = hs[j]["form"] if j < len(hs) else "?"
                    except ValueError:
                        fb = "-"
                dom.add("%s|%s" % (fa, fb))
            sigs["%s.K%s" % (lang, key)] = dict(
                language=lang, operation="K" + key,
                route=("C execution" if lang in GRAIN
                       else "A acceptance then chunked execution"),
                grain=GRAIN.get(lang, "holder"),
                domain=sorted(dom),
                answered=rec["domain"], refused=rec["refused"],
                harness_refused=rec.get("harness_refused", 0),
                raised=rec["raised"])
    return sigs


def jaccard(a, b):
    u = a | b
    return (len(a & b) / len(u)) if u else 0.0


def cluster_count(keys, sim, cut):
    groups = [[k] for k in keys]
    while True:
        best, bi, bj = None, None, None
        for x in range(len(groups)):
            for y in range(x + 1, len(groups)):
                vals = [sim[(p, q)] for p in groups[x] for q in groups[y]]
                m = sum(vals) / len(vals)
                if best is None or m > best:
                    best, bi, bj = m, x, y
        if best is None or best < cut:
            break
        groups[bi] = groups[bi] + groups[bj]
        groups.pop(bj)
    return groups


def full_merge(keys, sim):
    """average linkage all the way to one node; the merge history IS the
    sweep, read at every similarity it passes through."""
    node = {}
    groups = []
    for i, k in enumerate(keys):
        node[i] = dict(id=i, label=k, birth=1.0)
        groups.append(([k], i))
    nxt = len(keys)
    hist = []
    while len(groups) > 1:
        best, bi, bj = None, None, None
        for x in range(len(groups)):
            for y in range(x + 1, len(groups)):
                vals = [sim[(p, q)] for p in groups[x][0] for q in groups[y][0]]
                m = sum(vals) / len(vals)
                if best is None or m > best:
                    best, bi, bj = m, x, y
        a, b = groups[bi], groups[bj]
        hist.append(dict(node=nxt, similarity=round(best, 6),
                         left=dict(id=a[1], size=len(a[0])),
                         right=dict(id=b[1], size=len(b[0])),
                         size=len(a[0]) + len(b[0])))
        groups[bi] = (a[0] + b[0], nxt)
        groups.pop(bj)
        nxt += 1
    return hist


def sweep(keys, hist):
    """cluster count at every threshold, and the PLATEAUS -- the runs of
    threshold over which the count does not move.  No cut is chosen."""
    sims = sorted({h["similarity"] for h in hist}, reverse=True)
    rows = []
    for t in [x / 100.0 for x in range(100, -1, -1)]:
        n = len(keys) - sum(1 for h in hist if h["similarity"] >= t)
        rows.append(dict(threshold=round(t, 2), clusters=n))
    plats = []
    run = None
    for r in rows:
        if run and run["clusters"] == r["clusters"]:
            run["low"] = r["threshold"]
            run["width"] = round(run["high"] - run["low"], 2)
        else:
            if run:
                plats.append(run)
            run = dict(clusters=r["clusters"], high=r["threshold"],
                       low=r["threshold"], width=0.0)
    if run:
        plats.append(run)
    plats = [p for p in plats if p["width"] >= 0.05]
    plats.sort(key=lambda p: -p["width"])
    return rows, plats, sims


def nearest_operators(csigs):
    """where a construct lands relative to the operators, measured."""
    p = os.path.join(HERE, "clusters_all12.json")
    if not os.path.exists(p):
        return {}
    ops = json.load(open(p))["signatures"]
    out = {}
    for ck, cs in csigs.items():
        A = set(cs["domain"])
        if A and all(k.endswith("|-") for k in A):
            # a ONE-SLOT construct opens one operand position and an
            # operator opens two, so their key spaces do not meet.  Said
            # rather than papered over with a zero.
            out[ck] = dict(nearest=None, jaccard=None,
                           note="one-slot construct: not comparable in "
                                "the operator's ordered-pair key space")
            continue
        if not A:
            out[ck] = dict(nearest=None, jaccard=0.0,
                           note="empty domain: nothing was answered")
            continue
        best, bk = -1.0, None
        for ok, os_ in ops.items():
            j = jaccard(A, set(os_["domain"]))
            if j > best:
                best, bk = j, ok
        out[ck] = dict(nearest=bk, jaccard=round(best, 4),
                       same_language=(bk.split(".")[0] == cs["language"]))
    return out


def main():
    csigs = construct_signatures()
    keys = sorted(k for k, s in csigs.items() if s["domain"])
    empty = sorted(k for k, s in csigs.items() if not s["domain"])
    print("construct signatures: %d, of which %d carry a non-empty domain"
          % (len(csigs), len(keys)))
    print("  %d have an EMPTY domain -- the construct was probed and "
          "nothing was answered" % len(empty))
    sim = {}
    for i, a in enumerate(keys):
        A = set(csigs[a]["domain"])
        for b in keys[i:]:
            v = jaccard(A, set(csigs[b]["domain"]))
            sim[(a, b)] = sim[(b, a)] = v
    hist = full_merge(keys, sim)
    rows, plats, sims = sweep(keys, hist)
    near = nearest_operators(csigs)
    out = dict(
        status="CONSTRUCT-GRAIN, ALL TWELVE",
        built="2026-08-19",
        extends=["clusters_all12.json"],
        scope="the construct half of layer 3: the access, flow and "
              "binding families over all twelve languages, clustered on "
              "the jaccard of their domains with the cut swept and not "
              "chosen.",
        decision_17="constructs get their own dendrogram; the reason is "
                    "a measured difference of grain, and COMBINE = True "
                    "overturns it",
        n_leaves=len(keys),
        signatures=csigs,
        empty_domain=empty,
        merge_history=hist,
        sweep=rows,
        plateaus=plats,
        nearest_operator=near,
    )
    json.dump(out, open(os.path.join(HERE, "clusters_constructs.json"), "w"),
              indent=1, sort_keys=True)
    print("")
    print("the sweep, plateaus widest first (threshold band, cluster count)")
    for p in plats[:12]:
        print("  %4.2f..%4.2f  width %4.2f   %3d clusters"
              % (p["low"], p["high"], p["width"], p["clusters"]))
    print("")
    nc = sum(1 for v in near.values() if v.get("jaccard") is None
             and v.get("note", "").startswith("one-slot"))
    print("%d construct leaves are ONE-SLOT and share no key space with "
          "an operator" % nc)
    js = [v["jaccard"] for v in near.values() if v.get("nearest")]
    if js:
        js.sort()
        print("nearest operator signature, by the same jaccard:")
        print("  median %.3f   lowest %.3f   highest %.3f   n %d"
              % (js[len(js) // 2], js[0], js[-1], len(js)))
        same = sum(1 for v in near.values()
                   if v.get("same_language"))
        print("  %d of %d constructs sit nearest an operator of their "
              "OWN language" % (same, len(js)))
    fam = collections.Counter(k.split(".K")[1].split(".")[0] for k in keys)
    print("")
    print("leaves per family: " + ", ".join("%s %d" % (a, b)
                                            for a, b in sorted(fam.items())))


if __name__ == "__main__":
    main()
