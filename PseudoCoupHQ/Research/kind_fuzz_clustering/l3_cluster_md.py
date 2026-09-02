#!/usr/bin/env python3
"""l3_cluster_md.py -- render clusters_preliminary.json as prose + tables.

Reads only.  Writes clusters_preliminary.md.  Nothing here recomputes a
measurement; if a number appears in the markdown it was read out of the
json that l3_cluster.py wrote.
"""

import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
          "java", "typescript"]
ORDER = STATIC + ["python", "ruby", "php"]


def main():
    d = json.load(open(os.path.join(HERE, "clusters_preliminary.json")))
    sig = d["signatures"]
    L = []
    w = L.append

    w("# clusters_preliminary — layer 3, phase 4, PRELIMINARY\n")
    w("Built %s from `clusters_preliminary.json`. **Every number here is\n"
      "PRELIMINARY.** Scope: %s\n" % (d["built"], d["scope"]))

    w("\n## the shape of the pass\n")
    n_sig = len(sig)
    w("\n- **%d operation signatures** over twelve languages; %d have a\n"
      "  non-empty accepted domain and %d are empty and excluded\n"
      "  (`%s`).\n"
      % (n_sig, n_sig - len(d["empty_domain"]), len(d["empty_domain"]),
         "`, `".join(d["empty_domain"])))
    w("- the shared space is the **%d ordered form pairs** over the eight\n"
      "  layer-1 forms, which all twelve languages carry.\n"
      % d["shared_space_cells"])
    w("- **%d clusters** at the 0.70 cut, **%d** at 0.85.\n"
      % (len(d["clusters"]["0.70"]), len(d["clusters"]["0.85"])))
    w("- **%d relation edges**: %s.\n"
      % (sum(d["relation_counts"].values()),
         ", ".join("%s %d" % (k, v)
                   for k, v in sorted(d["relation_counts"].items()))))

    w("\n## the numbered decisions\n")
    for dec in d["decisions"]:
        w("\n**%s.** %s\n" % (dec["n"], dec["text"]))

    w("\n## per-language operation signatures\n")
    w("\nDomain size is the count of accepted ordered form pairs out of %d.\n"
      % d["shared_space_cells"])
    w("\n| language | operations | mean domain | widest operation | "
      "narrowest non-empty |\n")
    w("|---|---|---|---|---|\n")
    for lang in ORDER:
        ks = [k for k in sig if sig[k]["language"] == lang
              and sig[k]["domain"]]
        if not ks:
            continue
        sz = {k: len(sig[k]["domain"]) for k in ks}
        wide = max(sz, key=lambda k: sz[k])
        narrow = min(sz, key=lambda k: sz[k])
        w("| %s | %d | %.1f | %s (%d) | %s (%d) |\n"
          % (lang, len(ks), sum(sz.values()) / len(sz),
             sig[wide]["operation"], sz[wide],
             sig[narrow]["operation"], sz[narrow]))

    w("\n## the value-matrix overlay, under the completeness gate\n")
    w("\nDecisions 8 to 11. A refused matrix contributes NOTHING; it is not\n"
      "partially read.\n")
    w("\n| language | gate | pair cells | split cells | grid disagrees | "
      "operations widened |\n")
    w("|---|---|---|---|---|---|\n")
    for lang in STATIC:
        o = d["value_matrix_overlay"].get(lang)
        if not o:
            continue
        if not o["admitted"]:
            w("| %s | REFUSED | — | — | — | — |\n" % lang)
            continue
        w("| %s | admitted | %d | %d | %d | %d |\n"
          % (lang, o["pair_cells"], o["split"], o["grid_disagree"],
             len(o["widened"])))

    w("\n## the mixed-holder statistic (decision 7)\n")
    w("\nAmong accepted probes whose two holders carry the SAME form, the\n"
      "fraction whose holders DIFFER. Computed without naming any\n"
      "operation. Statically checked languages only — in the open-dispatch\n"
      "three the number is near 1 for almost everything and says little.\n")
    mx = [m for m in d["mixed_holder_by_signature"]
          if m["language"] in STATIC]
    by = collections.defaultdict(list)
    for m in mx:
        by[m["operation"]].append(m)
    rank = sorted(((op, sum(x["mixed_holder_ratio"] for x in v) / len(v),
                    len(v)) for op, v in by.items()), key=lambda t: -t[1])
    w("\n| operation | mean ratio | signatures |\n|---|---|---|\n")
    for op, r, c in rank:
        if c < 2 and r < 0.7:
            continue
        w("| `%s` | %.3f | %d |\n" % (op, r, c))

    w("\n### the same statistic per language, shifts against arithmetic\n")
    w("\n| language | `<<` | `>>` | `+` | `-` | `*` |\n|---|---|---|---|---|"
      "---|\n")
    for lang in STATIC:
        cells = []
        for op in ["<<", ">>", "+", "-", "*"]:
            s = sig.get("%s.%s" % (lang, op))
            cells.append("—" if not s or s["mixed_holder_ratio"] is None
                         else "%.2f (%d/%d)"
                         % (s["mixed_holder_ratio"],
                            s["mixed_holder_accepts"],
                            s["same_form_accepts"]))
        w("| %s | %s |\n" % (lang, " | ".join(cells)))

    w("\n## clusters at the 0.70 cut\n")
    for n, g in enumerate(d["clusters"]["0.70"], 1):
        if len(g) < 2:
            continue
        langs = sorted(set(k.split(".")[0] for k in g))
        w("\n- **cluster %d** — %d members over %d languages: `%s`\n"
          % (n, len(g), len(langs), "`, `".join(g)))

    w("\n## relation edges — a sample of each kind\n")
    seen = collections.Counter()
    for e in d["relations"]:
        if seen[e["relation"]] >= 3:
            continue
        seen[e["relation"]] += 1
        w("\n- **%s** — `%s` vs `%s`, jaccard %.3f. only-in-first: %s. "
          "only-in-second: %s.\n"
          % (e["relation"], e["a"], e["b"], e["jaccard"],
             ", ".join("`%s`" % x for x in e["a_only"][:4]) or "none",
             ", ".join("`%s`" % x for x in e["b_only"][:4]) or "none"))

    p = os.path.join(HERE, "clusters_preliminary.md")
    open(p, "w").write("".join(L))
    print("wrote clusters_preliminary.md (%d bytes)" % os.path.getsize(p))


if __name__ == "__main__":
    main()
