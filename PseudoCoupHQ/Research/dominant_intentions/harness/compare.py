#!/usr/bin/env python3
"""compare.py -- diff the collected run against the census's claims.

Plain words first: the lane wrote one file of `FACT.PROBE|RESULT` lines per
language into results/. This reads those, looks up what the census page said
each language should do, and marks every fact-by-language cell CONFIRMED,
REFUTED (carrying actual vs expected) or SKIPPED (the language is not in the
container, or the probe does not exist there). It writes
verified_<object>.json and prints a small table.

Canonicalisation happens HERE, never in the probed language, so a language's
printing habits cannot fake a disagreement.

Two expectation spellings carry rulings rather than values:

* `<any>` -- any result is acceptable. This is the owner's cpp-undefined-behaviour
  policy made executable: where a language guarantees NOTHING, the probe is
  still run and its answer still recorded as evidence, but no answer can be
  wrong, because there was no promise to break.
* `<raise:*>` -- the language must refuse at runtime, by any name. The exact
  exception name is preserved in the results file and quoted in the log; it is
  not pinned here, because the census's claim is "it refuses", not "it refuses
  with this spelling".

Usage:  python3 compare.py --vectors vectors_integer.json
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")


def canon(value):
    """Return a comparable form: a float for finite numbers, else the text."""
    v = value.strip()
    low = v.lower()
    if low in ("inf", "-inf", "nan", "true", "false"):
        return low
    if low.startswith("<"):
        return low
    try:
        return float(v)
    except ValueError:
        return v


def same(actual, expected):
    if expected == "<any>":
        return True
    a_raw = actual.strip()
    if expected == "<raise:*>":
        return a_raw.startswith("<raise:")
    a, e = canon(actual), canon(expected)
    if isinstance(a, float) and isinstance(e, float):
        return a == e
    return a == e


def read_results(path):
    if not os.path.exists(path):
        return None
    lines = {}
    with open(path) as fh:
        for raw in fh:
            if "|" not in raw:
                continue
            pid, _, val = raw.strip().partition("|")
            if pid.startswith("__"):
                return None if "ABSENT" in pid else lines
            lines.setdefault(pid, val)  # first line for an id wins
    return lines


def base_of(lang, template_of):
    return template_of.get(lang, lang)


def applicable(p, lang, base):
    only = p.get("only")
    if only and base not in only and lang not in only:
        return False
    skip = p.get("skip")
    if skip and (base in skip or lang in skip):
        return False
    e = p["expr"]
    if isinstance(e, dict):
        if not any(k in e for k in (lang, base, "default")):
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vectors", default="vectors_boolean_float.json")
    args = ap.parse_args()

    path = args.vectors
    if not os.path.isabs(path):
        path = os.path.join(HERE, path)
    with open(path) as fh:
        vectors = json.load(fh)

    prefix = vectors.get("run_prefix", "bf")
    obj = vectors.get("object_key", "boolean_float")
    template_of = vectors.get("template_of", {"rust-release": "rust", "dart-web": "dart"})

    languages = vectors["languages"]
    status = vectors["language_status"]
    out = {
        "schema": "dominant_intentions/harness/verified v2",
        "source_page": vectors["source_page"],
        "vectors": os.path.basename(path),
        "languages": languages,
        "language_status": status,
        "facts": {},
        "totals": {"CONFIRMED": 0, "REFUTED": 0, "SKIPPED": 0},
    }

    results = {lang: read_results(os.path.join(RESULTS, "%s_%s.txt" % (prefix, lang)))
               for lang in languages}

    for fact in vectors["facts"]:
        fid = fact["fact_id"]
        cells = {}
        for lang in languages:
            base = base_of(lang, template_of)
            res = results.get(lang)
            if res is None:
                cells[lang] = {"verdict": "SKIPPED",
                               "reason": status.get(lang, "no results file")}
                out["totals"]["SKIPPED"] += 1
                continue
            exp_default = fact["expected"]["default"]
            # EXACT language key only -- never fall back to the base language.
            # A mode column (rust-release, dart-web) exists precisely because it
            # may answer differently from the mode it shares source text with;
            # inheriting the base's expectation would erase the finding.
            exp_lang = fact["expected"].get("by_language", {}).get(lang, {})
            mismatches, checked, evidence = [], 0, {}
            for p in fact["probes"]:
                pid = p["probe_id"]
                if not applicable(p, lang, base):
                    continue
                expected = exp_lang.get(pid, exp_default.get(pid))
                if expected is None:
                    continue
                actual = res.get(fid + "." + pid, "<missing>")
                checked += 1
                evidence[pid] = actual
                if not same(actual, expected):
                    mismatches.append({"probe": pid, "expected": expected,
                                       "actual": actual})
            if checked == 0:
                cells[lang] = {"verdict": "SKIPPED",
                               "reason": "no applicable probes for this language"}
                out["totals"]["SKIPPED"] += 1
            elif mismatches:
                cells[lang] = {"verdict": "REFUTED", "probes_checked": checked,
                               "mismatches": mismatches, "evidence": evidence}
                out["totals"]["REFUTED"] += 1
            else:
                cells[lang] = {"verdict": "CONFIRMED", "probes_checked": checked,
                               "evidence": evidence}
                out["totals"]["CONFIRMED"] += 1
        out["facts"][fid] = {
            "object": fact["object"],
            "owner": fact["owner"],
            "kind": fact["kind"],
            "description": fact["description"],
            "cells": cells,
        }

    dest = [os.path.join(HERE, "verified_%s.json" % obj),
            os.path.join(os.path.dirname(HERE), "verified",
                         "verified_%s.json" % obj)]
    for d in dest:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        with open(d, "w") as fh:
            json.dump(out, fh, indent=2)
            fh.write("\n")

    short = {"CONFIRMED": "OK", "REFUTED": "XX", "SKIPPED": "--"}
    print("fact".ljust(12) + "".join(l[:7].rjust(9) for l in languages))
    for fid, f in out["facts"].items():
        print(fid.ljust(12) + "".join(
            short[f["cells"][l]["verdict"]].rjust(9) for l in languages))
    print()
    print("totals: %s" % out["totals"])
    for fid, f in out["facts"].items():
        for lang, c in f["cells"].items():
            if c["verdict"] == "REFUTED":
                for m in c["mismatches"]:
                    print("REFUTED %s/%s probe %s: expected %s, got %s"
                          % (fid, lang, m["probe"], m["expected"], m["actual"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
