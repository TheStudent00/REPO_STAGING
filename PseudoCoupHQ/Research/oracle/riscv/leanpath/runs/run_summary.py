#!/usr/bin/env python3
"""Rebuild the run summary and the key matrix from the run's own products.

Reads, per language: the compiler_corpus manifest (`units.json`), the walk
shards that expressed each arch-unit in Lean (`walk_[0-3]/walk.json`), the
swap table (`operator_for/operator_for.json`), the render
(`pass_b/render.json`), the walk over the rendered emulations
(`pass_b/walk/walk.json`) and the proofs (`pass_b/equals/equals.json`).

Nothing here is keyed by an instruction name or an operator token: the
causes below are read off the walk's own `why` text, and every key of the
matrix is whatever string the swap table holds.

    python3 runs/run_summary.py [out.json] [matrix.md]
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = [("c", "handful_c"), ("cpp", "corpus_cpp"),
         ("rust", "corpus_rust"), ("go", "corpus_go")]


def load(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def cause(why):
    """The four causes an arch-unit is not expressed in Lean."""
    if why.startswith("compile rc="):
        return "the compiler refused the probe"
    if "no certified pure form for ILLEGAL" in why or "C_ILLEGAL" in why:
        return "float probes the pruned decoder does not know"
    if "no certified pure form for JALR" in why:
        return "calls into the runtime"
    return "other walk shapes"


def at64(entry):
    h = entry.get("holders")
    return bool(h) and all(w == 64 for w in h)


def summarise():
    out, matrix = {}, {}
    for lang, d in LANGS:
        R = os.path.join(HERE, d)
        units = load(os.path.join(R, "units.json"), [])
        rows = []
        for p in sorted(glob.glob(os.path.join(R, "walk_[0-3]", "walk.json"))):
            rows += load(p, {"rows": []})["rows"]
        certified = [r for r in rows if r["verdict"] == "CERTIFIED"]
        refused = collections.Counter(cause(r.get("why", "")) for r in rows
                                      if r["verdict"] != "CERTIFIED")

        table = load(os.path.join(R, "operator_for", "operator_for.json"),
                     {"table": {}, "summary": {}})
        keys = table["table"]
        entries = sum(len(v) for v in keys.values())
        keys64 = sum(1 for v in keys.values() if any(at64(e) for e in v))
        for G, us in keys.items():
            matrix.setdefault(G, {})[lang] = (len(us), sum(1 for e in us if at64(e)))

        render = load(os.path.join(R, "pass_b", "render.json"), {})
        walk_b = load(os.path.join(R, "pass_b", "walk", "walk.json"), {"rows": []})
        eq = load(os.path.join(R, "pass_b", "equals", "equals.json"), {"rows": []})
        proved_defs, unproved, proved = set(), [], 0
        for r in eq["rows"]:
            if r.get("proved"):
                proved += 1
                for one in r["proved"]:
                    proved_defs.add("%s %s" % (one[0], " ".join(one[1])))
            else:
                unproved.append([r["unit"], r.get("proposal", "")])

        out[lang] = {
            "probes": len(units),
            "expressed_in_lean": len(certified),
            "refused": dict(refused),
            "keys": len(keys),
            "entries": entries,
            "keys_at_64": keys64,
            "rendered": render.get("rendered", 0),
            "refused_render": render.get("refused", 0),
            "lowered": sum(1 for r in walk_b["rows"] if r["verdict"] == "CERTIFIED"),
            "proved": proved,
            "unproved": unproved,
            "proved_defs": sorted(proved_defs),
        }
    return out, matrix


def matrix_md(matrix):
    esc = lambda s: s.replace("|", "\\|")
    lines = ["| key: a subterm of Sail's definitions | c | cpp | rust | go |",
             "|---|---|---|---|---|"]
    order = sorted(matrix.items(),
                   key=lambda kv: (-sum(n for n, _ in kv[1].values()), kv[0]))
    for G, per in order:
        cells = []
        for lang, _ in LANGS:
            if lang in per:
                n, k = per[lang]
                cells.append("%d (%d at 64)" % (n, k))
            else:
                cells.append("")
        lines.append("| `%s` | %s |" % (esc(G), " | ".join(cells)))
    return "\n".join(lines)


if __name__ == "__main__":
    out, matrix = summarise()
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "run_summary.json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=1)
    md = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "key_matrix.md")
    with open(md, "w") as f:
        f.write(matrix_md(matrix) + "\n")
    hdr = ("| language | probes | arch-units expressed in Lean | keys | entries | "
           "keys at 64 | rendered | lowered | proved | unproved |")
    print(hdr)
    print("|---|---|---|---|---|---|---|---|---|---|")
    for lang, _ in LANGS:
        s = out[lang]
        print("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            lang, s["probes"], s["expressed_in_lean"], s["keys"], s["entries"],
            s["keys_at_64"], s["rendered"], s["lowered"], s["proved"],
            len(s["unproved"])))
    print()
    print(matrix_md(matrix))
    print()
    print("wrote %s and %s" % (dest, md))
