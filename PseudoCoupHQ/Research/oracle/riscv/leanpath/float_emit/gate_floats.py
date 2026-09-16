#!/usr/bin/env python3
"""gate_floats.py -- the gate for the float arch-units, and its eye table.

  select  the dozen, by rule over data:
            the refusal   the old walk refused the unit because Sail's decoder (the
                          evaluable build the walk decodes with) answered ILLEGAL for
                          one of its words
            the holders   both holders are float holders; a holder representation is
                          a float holder when EVERY compiled unit that holds it was
                          refused that way (the decoder's own answer, not a spelling)
          ordered by probe number, taken by stride.
  merge   one strip record: the corpus run's record, with the rows of the clauses the
          effects rule certified in the working copy laid over it.
  table   the eye table: per unit its holders, its instructions (the disassembler's text,
          a display label only), what Sail's decoder gave for each word, the walk's
          verdict, and the Lean expression when there is one.

Nothing is keyed by an operator token.
"""
import argparse
import glob
import json


def load_walk(pattern):
    rows = {}
    for p in sorted(glob.glob(pattern)):
        for r in json.load(open(p))["rows"]:
            rows[r["unit"]] = r
    return rows


def illegal(r):
    return r is not None and r["verdict"] == "REFUSED" and "no certified pure form for ILLEGAL" in (r.get("why") or "")


def compiled(r):
    return r is not None and not (r.get("why") or "").startswith("compile rc=")


def cmd_select(a):
    units = json.load(open(a.units))
    rows = load_walk(a.walk)
    held = {}
    for u in units:
        r = rows.get(u["name"])
        reps = [u["probe"].get("lhs_rep"), u["probe"].get("rhs_rep")]
        if not compiled(r) or None in reps:        # two-holder units, the arity the gate takes
            continue
        for rep in set(reps):
            held.setdefault(rep, []).append(illegal(r))
    float_reps = sorted(rep for rep, v in held.items() if v and all(v))
    print("  | holder representation | compiled two-holder units holding it | refused at ILLEGAL | a float holder |")
    print("  |---|---|---|---|")
    for rep, v in sorted(held.items()):
        print("  | %s | %d | %d | %s |" % (rep, len(v), sum(v), "yes" if rep in float_reps else "no"))
    cands = sorted((u for u in units if illegal(rows.get(u["name"]))
                    and u["probe"].get("lhs_rep") in float_reps and u["probe"].get("rhs_rep") in float_reps),
                   key=lambda u: u["probe"]["n"])
    stride = max(1, len(cands) // a.count)
    dozen = cands[::stride][:a.count]
    json.dump(dozen, open(a.out, "w"), indent=1)
    print("  refused at ILLEGAL with both holders float: %d; stride %d; taken %d" % (len(cands), stride, len(dozen)))
    for u in dozen:
        print("   %-12s %-16s %s" % (u["name"], "%s, %s" % (u["probe"]["lhs_type"], u["probe"]["rhs_type"]),
                                   "; ".join(i["display"] for i in rows[u["name"]].get("instructions", []))))


def cmd_merge(a):
    base = json.load(open(a.base))
    new = json.load(open(a.new))
    by = {r["clause"]: r for r in base["rows"]}
    for r in new["rows"]:
        by[r["clause"]] = r
    summary = dict(base["summary"])
    summary.update({"merged": {"base": a.base, "laid_over": a.new, "rows_laid_over": len(new["rows"]),
                               "laid_over_certified": new["summary"]["certified"]}})
    json.dump({"summary": summary, "rows": list(by.values())}, open(a.out, "w"), indent=1, sort_keys=True)
    print("  merged: %d rows; %d laid over (%d certified)" % (len(by), len(new["rows"]), new["summary"]["certified"]))


def short_ctor(decoded):
    t = (decoded or "").split(" ", 1)[0]
    return t.rsplit(".", 1)[-1] if t else ""


def cmd_table(a):
    units = json.load(open(a.units))
    old = load_walk(a.old_walk)
    new = load_walk(a.new_walk)
    lines = ["| unit | holders | instructions (display) | Sail's decoder, per word | old walk | walk against the working copy | the Lean expression, or the refusal |",
             "|---|---|---|---|---|---|---|"]
    tally = {}
    for u in units:
        o, n = old.get(u["name"]), new.get(u["name"])
        ins = (n or o or {}).get("instructions", [])
        disp = "<br>".join("`%s`" % i["display"] for i in ins)
        dec = "<br>".join("`%s`" % short_ctor(i.get("decoded")) for i in ins)
        verdict = n["verdict"] if n else "absent"
        tally[verdict] = tally.get(verdict, 0) + 1
        expr = ("`%s`" % n["proposal"]) if n and n.get("proposal") else (n.get("why", "") if n else "")
        lines.append("| %s | %s, %s | %s | %s | %s | %s | %s |" % (
            u["name"], u["probe"]["lhs_type"], u["probe"]["rhs_type"], disp, dec,
            o["verdict"] if o else "absent", verdict, expr.replace("|", "\\|")))
    head = ["# the gate: a dozen c float arch-units walked against the working copy", "",
            "| verdict | units |", "|---|---|"] + ["| %s | %d |" % kv for kv in sorted(tally.items())] + [""]
    open(a.out, "w").write("\n".join(head + lines) + "\n")
    print("\n".join(head + lines))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("--units", required=True)
    s.add_argument("--walk", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--count", type=int, default=12)
    m = sub.add_parser("merge")
    m.add_argument("--base", required=True)
    m.add_argument("--new", required=True)
    m.add_argument("--out", required=True)
    t = sub.add_parser("table")
    t.add_argument("--units", required=True)
    t.add_argument("--old-walk", required=True)
    t.add_argument("--new-walk", required=True)
    t.add_argument("--out", required=True)
    a = ap.parse_args()
    {"select": cmd_select, "merge": cmd_merge, "table": cmd_table}[a.cmd](a)


if __name__ == "__main__":
    main()
