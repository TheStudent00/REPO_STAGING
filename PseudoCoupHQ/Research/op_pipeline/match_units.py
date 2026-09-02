#!/usr/bin/env python3
"""match_units.py -- steps 5 and 6 of the ratified pipeline: matching.

Every SHIP unit of every language goes into one pool.  The pool is
clustered twice, on two keys, in this order:

  1. BYTE IDENTITY.  The same machine bytes are the same unit, and no
     argument about lifting or normalization is needed to say so.
  2. SEM IDENTITY.  The anchored lifted form from `sem_anchored.py`.
     A byte cluster is always inside a sem cluster; the sem clustering
     is the coarser one and the difference between the two counts is
     exactly what the lifter bought.

Operator SPELLING and LANGUAGE are carried on every member as LABELS.
Neither is ever part of a key.  Two units spelled `+` in two languages
are in one cluster only because their bytes or their lifted forms put
them there, and two units in one cluster spelled differently is a
result, not an error.

The OPERAND TYPE PAIR is recorded per cluster, because it is part of
what a unit is: an i32 addition and an f64 addition are two rows of the
final table and must never be folded into one.

usage:
  match_units.py            write clusters.json, print the counts
"""

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sem_anchored as SA                                    # noqa: E402

LANGS = SA.LANGS


def load_units():
    """every ship unit of every language, as one flat list."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_%s.json" % lang)
        if not os.path.exists(path):
            print("!! no %s -- run sem_anchored.py first" % path)
            return None
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            meta = u["meta"]
            out.append(dict(
                lang=lang,
                n=n,
                operator=meta.get("operator"),
                arity=meta.get("arity"),
                position=meta.get("position"),
                lhs_rep=meta.get("lhs_rep"),
                rhs_rep=meta.get("rhs_rep"),
                result_rule=meta.get("result_rule"),
                expression=meta.get("expression"),
                bytes=u["bytes"],
                mnem=u["mnem"],
                sem_ok=u["sem"]["ok"],
                sem_key=u["sem"].get("key"),
                sem_reason=u["sem"].get("reason"),
            ))
    return out


def cluster(units, keyfn, label):
    """one clustering pass.  Units the key cannot be taken of are
    returned separately rather than dropped."""
    groups = defaultdict(list)
    unkeyed = []
    for u in units:
        k = keyfn(u)
        if k is None:
            unkeyed.append(u)
            continue
        groups[k].append(u)
    out = []
    for k, members in groups.items():
        langs = sorted(set(m["lang"] for m in members))
        spellings = sorted(set("%s/%s" % (m["lang"], m["operator"])
                               for m in members))
        typepairs = sorted(set("%s,%s" % (m["lhs_rep"], m["rhs_rep"])
                               for m in members))
        out.append(dict(
            kind=label,
            key=k,
            size=len(members),
            languages=langs,
            cross_language=len(langs) > 1,
            spelling_labels=spellings,
            type_pairs=typepairs,
            members=[dict(lang=m["lang"], n=m["n"], operator=m["operator"],
                          type_pair="%s,%s" % (m["lhs_rep"], m["rhs_rep"]))
                     for m in members],
        ))
    out.sort(key=lambda c: (-c["size"], c["key"]))
    return out, unkeyed


def main():
    units = load_units()
    if units is None:
        return 2

    byte_clusters, _ = cluster(units, lambda u: u["bytes"], "byte")
    sem_clusters, unkeyed = cluster(
        units, lambda u: u["sem_key"] if u["sem_ok"] else None, "sem")

    doc = dict(
        languages=LANGS,
        units=len(units),
        byte_clusters=len(byte_clusters),
        sem_clusters=len(sem_clusters),
        sem_unkeyed=[dict(lang=u["lang"], n=u["n"], reason=u["sem_reason"])
                     for u in unkeyed],
        cross_language_byte_clusters=sum(1 for c in byte_clusters
                                         if c["cross_language"]),
        cross_language_sem_clusters=sum(1 for c in sem_clusters
                                        if c["cross_language"]),
        clusters=dict(byte=byte_clusters, sem=sem_clusters),
    )
    path = os.path.join(HERE, "clusters.json")
    json.dump(doc, open(path, "w"), indent=1)

    print("== step 6: matching")
    print("   ship units pooled              %d" % doc["units"])
    print("   byte clusters                  %d" % doc["byte_clusters"])
    print("   sem clusters (anchored)        %d" % doc["sem_clusters"])
    print("   byte clusters spanning >1 lang %d"
          % doc["cross_language_byte_clusters"])
    print("   sem clusters spanning >1 lang  %d"
          % doc["cross_language_sem_clusters"])
    print("   units with no sem key          %d" % len(unkeyed))
    print()
    print("   the widest cross-language sem clusters:")
    shown = 0
    for c in sem_clusters:
        if not c["cross_language"]:
            continue
        print("   %2d members  %-28s  %s"
              % (c["size"], ",".join(c["languages"]),
                 " ".join(c["spelling_labels"])[:70]))
        print("        types %s" % " ".join(c["type_pairs"])[:80])
        shown += 1
        if shown >= 8:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
