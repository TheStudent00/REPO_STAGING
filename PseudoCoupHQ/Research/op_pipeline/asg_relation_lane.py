#!/usr/bin/env python3
"""asg_relation_lane.py -- WHICH RELATION ACTUALLY CARRIES A
COMPOUND-ASSIGNMENT UNIT TO THE PLAIN UNITS.

The question
------------
A compound-assignment probe has the shape `f(a, b): a op= b; return a`.
It performs an operation AND it stores.  The plain probe performs the
operation and returns it.  The expectation handed to this lap was:
the store should make whole-unit identity against a plain unit
impossible, so the relation that carries an asg unit to the plain
population should be the CONNECTION -- a shared core sub-term -- not
byte or sem identity.

That is an expectation to TEST, not to assume.  This program tests it.

How the question is asked WITHOUT reading a token
-------------------------------------------------
The temptation here is enormous and must be named: the obvious way to
ask "did `+=` land with `+`?" is to strip the `=` off the token and
pair them.  THAT IS THE BANNED THING.  It is spell-matching, and it is
exactly the violation the ban was restated in anger about.

So this program never forms a counterpart mapping.  It asks only
machine-form questions, of every asg unit against the whole plain
population:

  BYTE      is there a plain unit with identical machine bytes?
  SEM       is there a plain unit with an identical anchored lifted
            form (the sem key)?
  CONNECT   is there a plain unit that shares a maximal sub-term over
            the anchored variables, on the same operand type pair?

The sub-terms come from `verdicts3.unit_subterms`, imported unchanged,
so the connection here is the pipeline's connection and not a new
notion.  ONE FILTER OF verdicts3 IS DELIBERATELY NOT APPLIED, and it
is named: `verdicts3.connection_groups` keeps only sub-terms shared by
two or more LANGUAGES, because the dom_op construction rule puts edges
only between languages.  An asg unit and the plain unit whose
operation it performs are usually in the SAME language, so that filter
would hide the very relation being measured.  The filter belongs to
the dom_op construction, not to the connection relation, so it is
dropped here and its absence is recorded on the output.

The tokens are read ONCE, at the very end, to LABEL what the machine
already decided -- never to decide it.  That is the one use the ban
allows: a display label on the member.

WHICH UNITS ARE "asg": the staged unit number range (n >= the offset
asg_stage.py used) and the probe generator's own `bucket` provenance
field.  Neither is an operator token.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

Output: asg_relation.json, asg_relation.md

usage:
  asg_relation_lane.py [--out DIR]
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                          # noqa: E402
import verdicts3 as V3                                        # noqa: E402

ASG_N_OFFSET = 100000

RELATION_ORDER = ["byte", "sem", "connection", "none"]


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def is_asg(unit):
    """an asg unit, told apart by the staged number range and by the
    probe generator's own provenance field.  No token is read."""
    try:
        n = int(unit["n"])
    except (TypeError, ValueError):
        return False
    if n >= ASG_N_OFFSET:
        return True
    if unit["meta"].get("bucket") == "assignment":
        return True
    return False


def label(unit):
    """the display label for one unit.  Read at reporting time only."""
    return unit["meta"].get("operator")


def main():
    outdir = HERE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    started = time.time()

    units, excluded, excluded_rows = V.load_units()
    log("units loaded            %d" % len(units))

    plain = []
    asg = []
    for u in units:
        if is_asg(u):
            asg.append(u)
        else:
            plain.append(u)
    log("plain units             %d" % len(plain))
    log("assignment units        %d" % len(asg))

    # ---- the three machine-form indexes over the PLAIN population

    by_bytes = defaultdict(list)
    by_sem = defaultdict(list)
    for u in plain:
        by_bytes[tuple(u["bytes"])].append(u)
        by_sem[u["sem"]["key"]].append(u)

    for u in units:
        u["subterms"] = V3.unit_subterms(u)

    by_subterm = defaultdict(list)
    for u in plain:
        tp = V3.type_pair(u["meta"])
        for t in u["subterms"]:
            by_subterm[(tp, t)].append(u)

    log("plain byte forms        %d" % len(by_bytes))
    log("plain sem forms         %d" % len(by_sem))
    log("plain sub-term keys     %d" % len(by_subterm))

    # ---- ask each asg unit the three questions

    carried = Counter()
    rows = []
    for u in sorted(asg, key=lambda x: (x["lang"], int(x["n"]))):
        tp = V3.type_pair(u["meta"])

        byte_hits = by_bytes.get(tuple(u["bytes"])) or []
        sem_hits = by_sem.get(u["sem"]["key"]) or []

        conn = {}
        for t in u["subterms"]:
            for v in by_subterm.get((tp, t)) or []:
                key = "%s/op_%s" % (v["lang"], v["n"])
                if key not in conn:
                    conn[key] = []
                conn[key].append(t)

        if byte_hits:
            rel = "byte"
        elif sem_hits:
            rel = "sem"
        elif conn:
            rel = "connection"
        else:
            rel = "none"
        carried[rel] += 1

        rec = {}
        rec["unit"] = "%s/op_%s" % (u["lang"], u["n"])
        rec["lang"] = u["lang"]
        rec["n"] = u["n"]
        rec["operator"] = label(u)
        rec["asg_source_n"] = u["meta"].get("asg_source_n")
        rec["operand_types"] = tp
        rec["result_type"] = u["meta"].get("result_type")
        rec["strongest_relation_to_the_plain_population"] = rel
        rec["byte_companions"] = [
            dict(lang=v["lang"], n=v["n"], operator=label(v))
            for v in byte_hits]
        rec["sem_companions"] = [
            dict(lang=v["lang"], n=v["n"], operator=label(v))
            for v in sem_hits]
        rec["connection_companion_count"] = len(conn)
        shared = []
        for key in sorted(conn):
            longest = sorted(conn[key], key=len)[-1]
            shared.append(dict(unit=key, longest_shared_subterm=longest))
        rec["connection_companions"] = shared[:12]
        rec["connection_companions_shown"] = min(len(shared), 12)
        rows.append(rec)

    log("")
    log("== which relation carries an assignment unit to the plain "
        "population")
    for name in RELATION_ORDER:
        log("   %-12s %d" % (name, carried.get(name, 0)))

    # ---- same-language versus cross-language, for the byte and sem hits

    same_lang = Counter()
    for rec in rows:
        rel = rec["strongest_relation_to_the_plain_population"]
        if rel == "none":
            continue
        pool = rec["byte_companions"]
        if rel == "sem":
            pool = rec["sem_companions"]
        if rel == "connection":
            pool = [dict(lang=x["unit"].split("/")[0])
                    for x in rec["connection_companions"]]
        langs = set(x["lang"] for x in pool)
        if rec["lang"] in langs:
            same_lang[rel + " includes a same-language plain unit"] += 1
        if langs - set([rec["lang"]]):
            same_lang[rel + " includes a foreign-language plain unit"] += 1

    doc = {}
    doc["shape"] = "one entry per compound-assignment unit, saying "\
                   "which machine-form relation carries it to the "\
                   "plain population, and which plain units it lands "\
                   "on"
    doc["question"] = "the store is part of an assignment unit.  Does "\
                      "that make whole-unit identity against a plain "\
                      "unit impossible, so that the CONNECTION (a "\
                      "shared core sub-term) is the relation that "\
                      "carries it?"
    doc["candidate_set"] = "machine-form evidence only: identical "\
                           "bytes, identical anchored lifted form, or "\
                           "a shared sub-term on the same operand "\
                           "type pair.  No operator token takes part "\
                           "in any key, grouping, pairing or "\
                           "selection here."
    doc["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on an object that "\
                      "also carries `lang` and `n`.  It is read at "\
                      "reporting time only."
    doc["how_asg_units_are_told_apart"] = "the staged unit number "\
        "range (n >= %d) and the probe generator's `bucket` "\
        "provenance field.  Neither is an operator token." \
        % ASG_N_OFFSET
    doc["filter_deliberately_not_applied"] = "verdicts3."\
        "connection_groups keeps only sub-terms shared by two or more "\
        "LANGUAGES, because the dom_op construction puts edges only "\
        "between languages.  An assignment unit and the plain unit "\
        "whose operation it performs are usually in the SAME "\
        "language, so that filter would hide the relation being "\
        "measured.  It is dropped here; the same-language / "\
        "foreign-language split is reported instead."
    doc["subterms_from"] = "verdicts3.unit_subterms, imported unchanged"
    doc["units_loaded"] = len(units)
    doc["plain_units"] = len(plain)
    doc["assignment_units"] = len(asg)
    doc["carried_by"] = dict(carried)
    doc["reach"] = dict(same_lang)
    doc["wall_seconds"] = round(time.time() - started, 2)
    doc["rows"] = rows

    path = os.path.join(outdir, "asg_relation.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(doc, os.path.join(outdir, "asg_relation.md"))
    log("wrote %s" % os.path.join(outdir, "asg_relation.md"))
    return 0


def write_md(doc, path):
    out = []
    out.append("# which relation carries a compound-assignment unit "
               "to the plain units")
    out.append("")
    out.append("- units loaded: %d (plain %d, assignment %d)"
               % (doc["units_loaded"], doc["plain_units"],
                  doc["assignment_units"]))
    out.append("")
    out.append("| relation | assignment units carried |")
    out.append("|---|---|")
    for name in RELATION_ORDER:
        out.append("| %s | %d |" % (name, doc["carried_by"].get(name, 0)))
    out.append("")
    out.append("## reach")
    out.append("")
    for k in sorted(doc["reach"]):
        out.append("- %s: %d" % (k, doc["reach"][k]))
    out.append("")
    fh = open(path, "w")
    fh.write("\n".join(out))
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
