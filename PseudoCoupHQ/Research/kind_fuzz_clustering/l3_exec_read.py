#!/usr/bin/env python3
"""l3_exec_read.py -- fold the execution lanes into answers_<lang>.json.

Self-describing rows: every row carries its operation, both operands as
(form, holder, value class), and either a result -- the language's own
type name plus the encoding and the raw payload -- or the raise, the
death, or the codegen refusal that stood in place of one.

The completeness gate is the phase's standing rule: the row count must
equal the accepted-probe count the value matrix recorded, every accepted
id must appear exactly once, and a `__SUMMARY__` line must be present
per lane.  A lane's exit code is not evidence that it finished.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from l3_exec import accepted, table, LANGS                   # noqa: E402


def split_enc(rest):
    """'INT:64:00..' -> ('INT:64', '00..');  'BOOL:true' -> ('BOOL','true')"""
    if rest.startswith(("INT:", "UINT:", "FLOAT:")):
        a, b, c = rest.split(":", 2)
        return a + ":" + b, c
    if ":" in rest:
        a, b = rest.split(":", 1)
        return a, b
    return rest, ""


def fold(lang):
    ids = accepted(lang)
    want = ["P%d_%d_%d_%d_%d" % t for t in ids]
    T = table(lang)
    HS, OPS = T["holders"], T["ops"]
    seen = {}
    summaries = []
    files = sorted(f for f in os.listdir(RAW)
                   if f.startswith("ex_%s_" % lang) and f.endswith(".txt"))
    for fn in files:
        for line in open(os.path.join(RAW, fn)):
            line = line.rstrip("\n")
            if line.startswith("__SUMMARY__"):
                summaries.append(line.split("|")[1:])
                continue
            if "|" not in line:
                continue
            pid, rest = line.split("|", 1)
            if not pid.startswith("P"):
                continue
            seen[pid] = rest
    rows = []
    n_ans = n_raise = n_death = n_cg = n_miss = 0
    for pid in want:
        i, j, x, y, k = (int(z) for z in pid[1:].split("_"))
        ha, hb = HS[i], HS[j]
        row = dict(id=pid, operation=OPS[k],
                   lhs=dict(form=ha["form"], holder=ha["rep"],
                            value=ha["values"][x][0]),
                   rhs=dict(form=hb["form"], holder=hb["rep"],
                            value=hb["values"][y][0]))
        rest = seen.get(pid)
        if rest is None:
            row["outcome"] = "MISSING"
            n_miss += 1
        elif rest.startswith("-|RAISE:"):
            row["outcome"] = "raise"
            row["raise"] = rest[8:]
            n_raise += 1
        elif rest.startswith("-|DEATH:"):
            row["outcome"] = "death"
            row["death"] = rest[8:]
            n_death += 1
        elif rest.startswith("-|CODEGEN_REFUSE:"):
            row["outcome"] = "codegen_refuse"
            row["codegen_refuse"] = rest[17:]
            n_cg += 1
        elif rest.startswith("-|BUILDFAIL"):
            row["outcome"] = "buildfail"
            n_miss += 1
        else:
            tn, payload = rest.split("|", 1)
            enc, pay = split_enc(payload)
            row["outcome"] = "answer"
            row["result"] = dict(type=tn, encoding=enc, payload=pay)
            n_ans += 1
        rows.append(row)
    complete = (n_miss == 0 and len(rows) == len(want) and bool(summaries))
    doc = dict(language=lang, route="C execution, accepted subset",
               grain="one accepted (operation, holder pair, value pair) probe",
               probes=len(rows), answers=n_ans, raises=n_raise,
               deaths=n_death, codegen_refuse=n_cg, missing=n_miss,
               lanes=len(files), lane_summaries=summaries,
               complete=complete,
               completeness="COMPLETE" if complete else "SHORT",
               operations=OPS,
               holders=[dict(i=n, form=h["form"], rep=h["rep"])
                        for n, h in enumerate(HS)],
               rows=rows)
    p = os.path.join(HERE, "answers_%s.json" % lang)
    json.dump(doc, open(p, "w"))
    if not complete:
        print("!! %s SHORT: %d missing of %d" % (lang, n_miss, len(want)))
    return doc


def main():
    which = sys.argv[1:] or LANGS
    idx = {}
    print("| language | probes | answers | raises | deaths | codegen refuse "
          "| complete |")
    print("|---|---|---|---|---|---|---|")
    for lang in which:
        d = fold(lang)
        idx[lang] = dict(probes=d["probes"], answers=d["answers"],
                         raises=d["raises"], deaths=d["deaths"],
                         codegen_refuse=d["codegen_refuse"],
                         missing=d["missing"], complete=d["complete"])
        print("| %s | %d | %d | %d | %d | %d | %s |"
              % (lang, d["probes"], d["answers"], d["raises"], d["deaths"],
                 d["codegen_refuse"], d["complete"]))
    json.dump(idx, open(os.path.join(HERE, "answers_index.json"), "w"),
              indent=1)
    print("\ntotal probes %d, answers %d"
          % (sum(v["probes"] for v in idx.values()),
             sum(v["answers"] for v in idx.values())))


if __name__ == "__main__":
    main()
