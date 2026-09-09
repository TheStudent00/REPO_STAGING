#!/usr/bin/env python3
"""l3_value_fold.py -- fold the value-grain construct shards.

Three jobs, in order.

1. MERGE.  Each shard writes a verdict file and an answer file; go's
   simpler lane writes one merged file.  This joins them into one row
   per probe per language, `raw/vb_<lang>.txt`, in exactly the shape
   `l3_construct_read.py` already reads.

2. GATE.  Rows written against probes planned, per shard and per
   language.  A shard is a unit of SCHEDULING, so the gate reads the
   shards added together and prints COMPLETE only on a match.  exit 0
   is not evidence; this is.

3. MOVEMENT.  The question CHECK 5t asks: does a construct's domain
   MOVE when the value varies?  For every (language, construct, form)
   the holder-grain verdict of log 037 is set beside the value-grain
   verdict of this run and the disagreements are counted.  A form whose
   condition slot SPLITS by value is a truthiness finding and is
   reported as one.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RAW = os.path.join(HERE, "raw")
OUT = ("/sessions/sharp-vigilant-volta/mnt/Programming/SandboxDesign"
       "/agent/out")
if not os.path.isdir(OUT):
    OUT = os.path.expanduser("SandboxDesign/agent/out")

from l3_accept import holders                               # noqa: E402
import l3_construct_read as R                               # noqa: E402

NINE = ["typescript", "csharp", "java", "dart", "rust", "go",
        "cpp", "swift", "kotlin"]
HOLDER_FILE = dict((l, "kg_go.txt" if l == "go" else "kb_%s.txt" % l)
                   for l in NINE)


# ----------------------------------------------------------------- 1
def merge(lang):
    """shards -> raw/vb_<lang>.txt, one row per probe."""
    planned = rows = 0
    out = []
    if lang == "go":
        shards = sorted(f for f in os.listdir(OUT)
                        if re.match(r"vg_go_\d+\.txt$", f))
        for f in shards:
            for line in open(os.path.join(OUT, f), errors="replace"):
                line = line.rstrip("\n")
                if line.startswith("__SUMMARY__"):
                    planned += int(line.split("|")[1])
                    continue
                if line.count("|") >= 2:
                    out.append(line)
    else:
        shards = sorted(f for f in os.listdir(OUT)
                        if re.match(r"vx_%s_\d+\.txt$" % lang, f))
        for f in shards:
            tag = f[3:-4]
            ans = {}
            ay = os.path.join(OUT, "vy_%s.txt" % tag)
            if os.path.exists(ay):
                for line in open(ay, errors="replace"):
                    if line.startswith("__SUMMARY__"):
                        continue
                    p = line.rstrip("\n").split("|", 2)
                    if len(p) == 3:
                        ans[p[0]] = "%s|%s" % (p[1], p[2])
            for line in open(os.path.join(OUT, f), errors="replace"):
                line = line.rstrip("\n")
                if line.startswith("__SUMMARY__"):
                    planned += int(line.split("|")[1])
                    continue
                p = line.split("|", 2)
                if len(p) != 3:
                    continue
                pid, verdict, msg = p
                if pid in ans:
                    out.append("%s|%s" % (pid, ans[pid]))
                elif verdict == "ACCEPT":
                    out.append("%s|-|MISSING:accepted but no answer row"
                               % pid)
                elif R.harness_refusal(msg):
                    out.append("%s|-|HARNESS_REFUSE:%s" % (pid, msg))
                else:
                    out.append("%s|-|REFUSE:%s" % (pid, msg))
    rows = len(out)
    if not rows:
        return None
    out.append("__SUMMARY__|%d|%d|%d|0.000" % (planned, rows, len(shards)))
    open(os.path.join(RAW, "vb_%s.txt" % lang), "w").write(
        "\n".join(out) + "\n")
    return dict(language=lang, shards=len(shards), planned=planned,
                rows=rows, missing=planned - rows,
                complete=(planned == rows))


# ----------------------------------------------------------------- 2
# A refusal message that names the INSTRUMENT running out of room, or
# the harness failing, is not the language refusing the probe.  The
# completeness gate counts ROWS and cannot see the difference, so this
# check sits beside it.  go's first value run wrote 1,031 such rows.
SUSPECT = ("no space left", "write /work", "copying /tmp/go-build",
           "HARNESS:", "Cannot allocate", "Killed", "Out of memory")


def suspect_rows(path):
    n = 0
    for line in open(path, encoding="utf-8", errors="replace"):
        if any(t in line for t in SUSPECT):
            n += 1
    return n


def verdict_of(payload):
    if payload.startswith("HARNESS_REFUSE"):
        return "harness"
    if payload.startswith(("REFUSE", "CODEGEN_REFUSE", "MISSING")):
        return "refuse"
    if payload.startswith(("RAISE", "DEATH", "BUDGET")):
        return "raise"
    return "answer"


def read(path):
    rows = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            continue
        p = line.split("|", 2)
        if len(p) == 3:
            rows[p[0]] = (p[1], p[2])
    return rows


# ----------------------------------------------------------------- 3
def movement(lang):
    """does the verdict move when only the VALUE changes?"""
    vb = os.path.join(RAW, "vb_%s.txt" % lang)
    kb = os.path.join(RAW, HOLDER_FILE[lang])
    if not (os.path.exists(vb) and os.path.exists(kb)):
        return None
    hs, _ = holders(lang)
    val = read(vb)
    hol = read(kb)
    # group the value-grain rows by the holder-grain key they belong to
    grp = collections.defaultdict(set)
    for pid, (ty, payload) in val.items():
        m = re.match(r"^(K[a-z]+\.[a-z]+[^_]*)_(\d+)(?:_(\d+))?_", pid)
        if not m:
            continue
        key = (m.group(1) + "_" + m.group(2)
               + ("_" + m.group(3) if m.group(3) else ""))
        grp[key].add(verdict_of(payload))
    split = sum(1 for v in grp.values() if len(v) > 1)
    agree = disagree = absent = 0
    moved = []
    for key, vs in grp.items():
        if key not in hol:
            absent += 1
            continue
        hv = verdict_of(hol[key][1])
        if vs == {hv}:
            agree += 1
        else:
            disagree += 1
            if len(moved) < 400:
                moved.append(dict(key=key, holder_grain=hv,
                                  value_grain=sorted(vs)))
    return dict(language=lang, holder_keys=len(grp),
                keys_that_split_by_value=split,
                agrees_with_holder_grain=agree,
                disagrees=disagree, not_in_holder_run=absent,
                examples=moved[:40])


def truth_value(lang):
    """the if-condition slot at the VALUE grain: per form, the counts."""
    vb = os.path.join(RAW, "vb_%s.txt" % lang)
    if not os.path.exists(vb):
        return None
    hs, _ = holders(lang)
    per = collections.defaultdict(collections.Counter)
    for pid, (ty, payload) in read(vb).items():
        m = re.match(r"^Kflow\.if_(\d+)_(.+)$", pid)
        if not m:
            continue
        form = hs[int(m.group(1))]["form"]
        v = verdict_of(payload)
        if v == "harness":
            per[form]["HARNESS"] += 1
        elif v == "refuse":
            per[form]["REFUSE"] += 1
        elif v == "raise":
            per[form]["RAISE"] += 1
        elif "BR=then" in payload:
            per[form]["then"] += 1
        elif "BR=else" in payload:
            per[form]["else"] += 1
        else:
            per[form]["?"] += 1
    return {f: dict(per[f]) for f in R.FORMS if f in per}


def main():
    langs = sys.argv[1:] or NINE
    gates, moves, truth = [], {}, {}
    print("value-grain fold")
    print("")
    print("  language      shards   planned      rows   missing  suspect  gate")
    for lang in langs:
        g = merge(lang)
        if not g:
            print("  %-11s  -- no shard output yet" % lang)
            continue
        gates.append(g)
        g["suspect_rows"] = suspect_rows(
            os.path.join(RAW, "vb_%s.txt" % lang))
        print("  %-11s %6d %9d %9d %9d %8d  %s"
              % (lang, g["shards"], g["planned"], g["rows"], g["missing"],
                 g["suspect_rows"],
                 ("COMPLETE" if g["complete"] and not g["suspect_rows"]
                  else "SHORT" if not g["complete"] else "CONTAMINATED")))
        moves[lang] = movement(lang)
        truth[lang] = truth_value(lang)
    tp = sum(g["planned"] for g in gates)
    tr = sum(g["rows"] for g in gates)
    print("")
    print("  TOTAL       %9d %9d %9d  %s"
          % (tp, tr, tp - tr, "COMPLETE" if tp == tr else "SHORT"))
    # a partial run must never delete a language a whole run measured,
    # so both files are MERGED into rather than overwritten.
    def keep(name, new_part):
        path = os.path.join(HERE, name)
        old_part = {}
        if os.path.exists(path):
            try:
                old_part = json.load(open(path))
            except Exception:
                old_part = {}
        old_part.update({k: v for k, v in new_part.items() if v})
        json.dump(old_part, open(path, "w"), indent=1, sort_keys=True)
        return old_part

    keep("truthiness_value.json", truth)
    mv = keep("value_movement.json", dict(movement=moves))
    mv["gate"] = gates
    json.dump(mv, open(os.path.join(HERE, "value_movement.json"), "w"),
              indent=1, sort_keys=True)
    print("")
    print("  movement -- does a verdict move when only the value changes?")
    print("  language     keys   split by value   disagrees with holder")
    for lang in langs:
        m = moves.get(lang)
        if not m:
            continue
        print("  %-11s %6d %14d %19d"
              % (lang, m["holder_keys"], m["keys_that_split_by_value"],
                 m["disagrees"]))


if __name__ == "__main__":
    main()
