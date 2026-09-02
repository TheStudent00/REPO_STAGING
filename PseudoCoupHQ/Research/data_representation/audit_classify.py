#!/usr/bin/env python3
"""audit_classify.py -- read the lane results and rule on every layer-2 cell.

Plain words first. Each lane script printed one line per probe, in the shared
harness convention `FACT_ID|RESULT`, FACT_ID being `<form>.<representation>.<probe>`.
This script reads those lines back and answers the layer-2 question for each
(form, representation) cell: could that representation hold the layer-1 content?

Four verdicts, and the third is the one the node cares about:

* LOADS   -- every probe of the cell built, ran, and gave back the content.
* PARTIAL -- the base values loaded, some EDGE did not. The edge is named.
             A silently CHANGED whole number counts here too: `ctypes.c_int64`
             took 9223372036854775808 without complaint and gave back
             -9223372036854775808, which is a loss, not a load.
* REFUSES-behavioral -- the representation cannot hold that content by its own
             nature, and the refusal is expected from what the representation IS
             (a 32-bit whole number cannot hold a 64-bit edge; a container with
             one declared element kind cannot hold the mixed row; a holder that
             owns its elements cannot hold one node in two positions). Expected,
             files to layer 3.
* REFUSES-gap -- content layer 1 says is loadable that NO representation of that
             form in that language could hold. This is the only verdict that
             would make layer 1 grow, so it is decided across a whole form, not
             per cell.

Identity is judged on the ANSWER, not on whether the program ran: a probe that
printed `copied` ran perfectly and still did not hold a shared node.
"""

import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "audit", "raw")
OUTD = os.path.join(HERE, "audit")

FORMS = ["nothing", "truth", "whole", "fractional", "text",
         "sequence", "keyed", "nesting", "identity"]

REFUSAL = re.compile(r"^<(compile-error|aborted|error:[^>]*|no-output|absent)>$")

WHOLE_EXPECT = {"base_zero": "0", "base_42": "42",
                "i64max": "9223372036854775807",
                "i64max_plus1": "9223372036854775808",
                "p53_plus1": "9007199254740993",
                "u64max": "18446744073709551615"}

BASE_PROBES = {
    "nothing": ["null"],
    "truth": ["true", "false"],
    "whole": ["base_zero", "base_42"],
    "fractional": ["base_1_5", "base_pi"],
    "text": ["base_empty", "base_hello", "base_lines"],
    "sequence": ["empty", "base", "strs"],
    "keyed": ["empty", "flat"],
    "nesting": ["seq_in_seq", "seq_in_map", "mixed_depth"],
    "identity": ["shared", "diamond", "cycle"],
}

IDENTITY_HOLDS = {"shared": {"shared", "shared-read-only"},
                  "diamond": {"same"},
                  "cycle": {"cycle"}}


def norm_whole(s):
    s = s.strip()
    if s.endswith("n"):            # typescript bigint printed with its suffix
        s = s[:-1]
    if s.endswith(".0"):           # a whole number held in a fractional holder
        s = s[:-2]
    if s.endswith("/1"):           # an exact ratio holder prints 42 as 42/1
        s = s[:-2]
    s = s.replace("_", "").replace("'", "")
    return s


def split_id(fact_id):
    bits = fact_id.split(".")
    return bits[0], ".".join(bits[1:-1]), bits[-1]


def read_lane(path):
    out = OrderedDict()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if "|" not in line:
                continue
            fid, res = line.split("|", 1)
            if fid not in out:      # first line for an id wins
                out[fid] = res
    return out


def judge_probe(form, probe, result):
    """-> ('loaded'|'refused'|'eroded'|'not-held', detail)"""
    if REFUSAL.match(result.strip()):
        return "refused", result.strip()
    if form == "whole" and probe in WHOLE_EXPECT:
        if norm_whole(result) != WHOLE_EXPECT[probe]:
            return "eroded", result.strip()
    if form == "identity":
        if result.strip() not in IDENTITY_HOLDS[probe]:
            return "not-held", result.strip()
    return "loaded", result.strip()


def classify(lang):
    spec = json.load(open(os.path.join(HERE, "representations_%s.json" % lang)))
    lane = read_lane(os.path.join(RAW, "l2_%s.txt" % lang))
    absent = "__ABSENT__" in lane
    cells = []
    for form in FORMS:
        for rep in spec["forms"].get(form, []):
            cell_id = "%s.%s" % (form, rep["rep"])
            probes = OrderedDict()
            for fid, res in lane.items():
                f, r, p = split_id(fid)
                if f == form and r == rep["rep"]:
                    probes[p] = res
            per = OrderedDict()
            for p, res in probes.items():
                per[p] = judge_probe(form, p, res)
            base = [p for p in BASE_PROBES[form] if p in per]
            base_ok = base and all(per[p][0] == "loaded" for p in base)
            trouble = [(p, st, d) for p, (st, d) in per.items() if st != "loaded"]
            if absent or not per:
                verdict, why = "NOT-RUN", "no toolchain reachable in the sandbox"
            elif not trouble:
                verdict, why = "LOADS", "every probe built, ran and gave the content back"
            elif base_ok:
                verdict = "PARTIAL"
                why = "; ".join("%s %s (%s)" % (p, st, d) for p, st, d in trouble)
            else:
                verdict = "REFUSES-behavioral"
                why = "; ".join("%s %s (%s)" % (p, st, d) for p, st, d in trouble)
            cells.append(OrderedDict([
                ("cell", cell_id), ("form", form), ("rep", rep["rep"]),
                ("kind", rep.get("kind")), ("note", rep.get("note")),
                ("verdict", verdict), ("why", why),
                ("probes", OrderedDict((p, {"result": probes[p],
                                            "judgement": per[p][0]})
                                       for p in probes)),
            ]))

    # the layer-1 audit question, decided per form rather than per cell
    form_verdict = OrderedDict()
    for form in FORMS:
        fc = [c for c in cells if c["form"] == form]
        if not fc:
            form_verdict[form] = "NO-REPRESENTATION-ENUMERATED"
        elif any(c["verdict"] == "NOT-RUN" for c in fc):
            form_verdict[form] = "NOT-RUN"
        elif any(c["verdict"] == "LOADS" for c in fc):
            form_verdict[form] = "held"
        elif any(c["verdict"] == "PARTIAL" for c in fc):
            form_verdict[form] = "held-with-edges-refused"
        else:
            form_verdict[form] = "REFUSES-gap"

    counts = OrderedDict()
    for v in ["LOADS", "PARTIAL", "REFUSES-behavioral", "NOT-RUN"]:
        counts[v] = sum(1 for c in cells if c["verdict"] == v)
    doc = OrderedDict([
        ("language", lang), ("layer", 2),
        ("what", "the load-audit: can each layer-2 representation hold layer-1 content"),
        ("evidence", "audit/raw/l2_%s.txt, produced by audit/lanes/l2_%s.sh" % (lang, lang)),
        ("cell_count", len(cells)), ("probe_count", sum(len(c["probes"]) for c in cells)),
        ("verdict_counts", counts), ("form_verdicts", form_verdict),
        ("cells", cells)])
    with open(os.path.join(OUTD, "audit_%s.json" % lang), "w") as fh:
        json.dump(doc, fh, indent=1)
    return doc


def main():
    langs = sys.argv[1:] or ["python", "ruby", "php", "typescript", "go", "cpp",
                             "java", "rust", "kotlin", "dart", "swift", "csharp"]
    grand = OrderedDict()
    for lang in langs:
        if not os.path.exists(os.path.join(RAW, "l2_%s.txt" % lang)):
            print("%-11s no lane output yet" % lang)
            continue
        d = classify(lang)
        grand[lang] = d
        c = d["verdict_counts"]
        print("%-11s cells %3d | LOADS %3d PARTIAL %3d REFUSES-behavioral %3d NOT-RUN %3d"
              % (lang, d["cell_count"], c["LOADS"], c["PARTIAL"],
                 c["REFUSES-behavioral"], c["NOT-RUN"]))
    tot = OrderedDict((k, sum(d["verdict_counts"][k] for d in grand.values()))
                      for k in ["LOADS", "PARTIAL", "REFUSES-behavioral", "NOT-RUN"])
    print("TOTAL cells %d | %s" % (sum(d["cell_count"] for d in grand.values()),
                                   ", ".join("%s %d" % kv for kv in tot.items())))
    gaps = [(l, f) for l, d in grand.items()
            for f, v in d["form_verdicts"].items() if v == "REFUSES-gap"]
    print("REFUSES-gap forms: %s" % (gaps or "none -- layer 1 stands audited"))


if __name__ == "__main__":
    main()
