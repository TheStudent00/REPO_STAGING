#!/usr/bin/env python3
"""fold.py -- folds the lane outputs and the probe manifests into one
record per probe.

Input
-----
probe_manifest_<lang>.json      what was asked for (step 1)
<out>/op_<lang>.txt             what the compilers answered (steps 1b-3)
<out>/op_<lang>_s<k>.txt        the same, when the lane was sharded

Output
------
op_units_<lang>.json

    probes  n -> {meta, refused?, anchor{bytes,mnem,dwarf}, ship{bytes,mnem}}

`meta` is the manifest record with the probe SOURCE dropped -- the
source stays in the manifest, which is the one place it is authored,
so the folded file cannot drift from it.

A probe the compiler refused carries `refused` and nothing else.  A
probe with no line at all in the lane output carries `missing`, and
that is reported rather than counted as a refusal: not-run and
refused are different facts.

This tool stops where the ratified pipeline's step 3 stops.  It does
no normalization and no matching -- those are steps 5 and 6.

usage:
  fold.py c cpp go rust swift
  fold.py go --out /somewhere/else
"""

import argparse
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.normpath(
    os.path.join(HERE, "..", "..", "..", "Airlock", "agent", "out"))

LANGS = ["c", "cpp", "go", "rust", "swift"]


def lane_files(outdir, lang):
    got = []
    plain = os.path.join(outdir, "op_%s.txt" % lang)
    if os.path.exists(plain):
        got.append(plain)
    # `op_<lang>_s*` would also match `op_<lang>_smoke`, and folding a
    # smoke lane's 40 probes on top of the full lane's makes the tally
    # count some probes twice.  A shard suffix is `_s` and then DIGITS.
    pattern = os.path.join(outdir, "op_%s_s[0-9]*.txt" % lang)
    shards = sorted(glob.glob(pattern))
    for p in shards:
        got.append(p)
    return got


def read_lanes(paths):
    """probe number -> list of already-split lines."""
    rows = {}
    for p in paths:
        fh = open(p)
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            parts = ln.split("|")
            key = parts[0]
            if not key.startswith("op_"):
                continue
            n = int(key[3:])
            rows.setdefault(n, []).append(parts)
        fh.close()
    return rows


def dwarf_rows(text):
    """`a=fbreg -4;b=fbreg -8` -> [{name, location}]."""
    got = []
    for item in text.split(";"):
        if not item:
            continue
        if "=" not in item:
            got.append(dict(name=item, location=None))
            continue
        name, loc = item.split("=", 1)
        got.append(dict(name=name, location=loc))
    return got


def fold(lang, outdir):
    mpath = os.path.join(HERE, "probe_manifest_%s.json" % lang)
    doc = json.load(open(mpath))
    probes = doc["probes"]

    paths = lane_files(outdir, lang)
    rows = read_lanes(paths)

    folded = {}
    tally = dict(candidates=len(probes), refused=0, accepted=0,
                 anchor_ok=0, ship_ok=0, dwarf=0, missing=0, other=0)

    for key in sorted(probes, key=int):
        rec = dict(probes[key])
        rec.pop("source", None)
        n = int(key)
        mine = rows.get(n)
        entry = dict(meta=rec)
        if not mine:
            entry["missing"] = "no line for op_%d in %s" % (n, paths)
            tally["missing"] += 1
            folded[key] = entry
            continue
        accepted = True
        for parts in mine:
            tag = parts[1]
            if tag == "REFUSED":
                entry["refused"] = parts[2] if len(parts) > 2 else ""
                accepted = False
                continue
            if tag not in ("ANCHOR", "SHIP"):
                tally["other"] += 1
                continue
            what = parts[2]
            slot = "anchor" if tag == "ANCHOR" else "ship"
            if what == "OK":
                entry.setdefault(slot, {})
                entry[slot]["bytes"] = parts[3].split()
                entry[slot]["mnem"] = parts[4].split(";") if parts[4] else []
                if slot == "anchor":
                    tally["anchor_ok"] += 1
                else:
                    tally["ship_ok"] += 1
            elif what == "DWARF":
                entry.setdefault("anchor", {})
                entry["anchor"]["dwarf"] = dwarf_rows(parts[3])
                tally["dwarf"] += 1
            else:
                entry.setdefault(slot, {})
                entry[slot][what.lower()] = "|".join(parts[3:])
                tally["other"] += 1
        if accepted:
            tally["accepted"] += 1
        else:
            tally["refused"] += 1
        folded[key] = entry

    out = dict(meta=doc["meta"], tally=tally,
               lane_files=[os.path.basename(p) for p in paths],
               probes=folded)
    path = os.path.join(HERE, "op_units_%s.json" % lang)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    return tally, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    ap.add_argument("--out", default=OUTDIR, help="Airlock out directory")
    args = ap.parse_args()

    head = ("%-7s %10s %8s %9s %9s %8s %8s %8s"
            % ("lang", "candidates", "refused", "accepted", "anchor-OK",
               "ship-OK", "DWARF", "missing"))
    print(head)
    print("-" * len(head))
    for lang in args.langs:
        if lang not in LANGS:
            print("skip %s" % lang)
            continue
        t, path = fold(lang, args.out)
        print("%-7s %10d %8d %9d %9d %8d %8d %8d"
              % (lang, t["candidates"], t["refused"], t["accepted"],
                 t["anchor_ok"], t["ship_ok"], t["dwarf"], t["missing"]))
        print("        -> %s" % path)


if __name__ == "__main__":
    main()
