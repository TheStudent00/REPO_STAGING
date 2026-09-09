#!/usr/bin/env python3
"""regen_validate1.py -- the corrected inventory re-validated against what
the regeneration's compilers ACTUALLY did.

THE POPULATION, STATED
----------------------
The 129,553 probes the regeneration compiled in the trickle container on
2026-09-02 (log 131): 29,288 accepted with full extraction, 100,265
refused.  This program reads those stores and nothing else; it compiles
nothing and re-runs nothing.  The re-capture stores
(`op_units_recapture_*`) are a DIFFERENT population (the original
corpus's probes, re-captured for verbatim testimony) and are excluded by
filename; the exclusion is counted and printed.

THE TWO QUESTIONS
-----------------
1. THE HOLDER QUESTION (the new witness).  Every probe's holder types
   are looked up in `type_inventory3.json`.  A probe at least one of
   whose holders is NOT declarable on this target would never have been
   generated under the corrected inventory.  How many refusals does that
   account for, and -- the check that can refute the witness -- how many
   probes with a non-declarable holder were nonetheless ACCEPTED?  A
   single such acceptance would mean the declaration lane demoted a type
   the probe lane can actually use.

2. THE OPERATOR QUESTION.  Inside the probes whose holders are all
   declarable, the operator-legality oracle's own recorded verdict
   (`meta.filter_verdict`, written at generation time) is scored against
   accept/refuse.  `no_rule` is out of oracle scope by construction --
   the filter passes those to the compiler rather than judging them.

EVERY REMAINING MISS BY CAUSE
-----------------------------
A miss is a probe the oracle called legal, with all holders declarable,
that the compiler refused.  Misses are grouped by MESSAGE SHAPE: the
compiler's own words with the file:line:col prefix removed, every
quoted or backticked span replaced by a placeholder, and every run of
digits replaced by N.  That normalisation is uniform -- it masks type
spellings and operator tokens alike -- so the grouping key is the
compiler's own diagnostic shape, machine-form evidence, never a token.

THE SPELLING BAN
----------------
Groups are keyed by opaque shape ids and by operator UNIT ids.  No key,
grouping, pairing or row structure is an operator token.  Verbatim
compiler words live in `refusal` / `text` fields.  The output is walked
by the guard and this program deletes its own output on failure.

usage:  /tmp/reconnect_venv/bin/python3 regen_validate1.py
writes: regen_witness_validation1.json
"""

import collections
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

PREFIX = re.compile(r"^[^\s]*?:\d+(:\d+)?:\s*")
QUOTED = re.compile(r"'[^']*'|`[^`']*'|`[^`]*`|\"[^\"]*\"")
DIGITS = re.compile(r"\d+")


def shape_of(text):
    if not text:
        return "(no diagnostic)"
    line = text.strip().split("\n")[0].strip()
    line = PREFIX.sub("", line)
    line = QUOTED.sub("<Q>", line)
    line = DIGITS.sub("N", line)
    return line[:200]


def declarable_sets():
    inv3 = json.load(open(os.path.join(HERE, "type_inventory3.json")))
    out = {}
    for lang in LANGS:
        out[lang] = set(e["spelling"] for e in inv3["languages"][lang]["types"])
    return out


def main():
    ok_types = declarable_sets()
    files = sorted(glob.glob(os.path.join(HERE, "trickle_store",
                                          "op_units2_*.json")))
    excluded = sorted(glob.glob(os.path.join(HERE, "trickle_store",
                                             "op_units_recapture_*.json")))
    cells = collections.defaultdict(int)
    per_lang = collections.defaultdict(lambda: collections.defaultdict(int))
    quirk_doc = json.load(open(os.path.join(HERE, "legality_quirks.json")))
    quirk_ids = set()
    for row in quirk_doc["annotations"]:
        quirk_ids.add((row["language"], row["rule_id"]))
    quirk_agreements = []
    misses = []
    accepted_but_demoted = []
    shape_counts = collections.defaultdict(
        lambda: collections.defaultdict(int))
    shape_example = {}
    shape_holders = collections.defaultdict(
        lambda: collections.defaultdict(int))
    shape_units = collections.defaultdict(set)
    for path in files:
        doc = json.load(open(path))
        lang = doc["language"]
        for key in doc["probes"]:
            probe = doc["probes"][key]
            meta = probe["meta"]
            accepted = ("ship" in probe) and (
                probe.get("refused") in (None, "", False))
            holders = [meta["lhs_type"]]
            if meta.get("rhs_type"):
                holders.append(meta["rhs_type"])
            all_decl = all(h in ok_types[lang] for h in holders)
            verdict = meta.get("filter_verdict")
            per_lang[lang]["probes"] += 1
            per_lang[lang]["accepted" if accepted else "refused"] += 1
            cells[("all_declarable" if all_decl else "holder_demoted",
                   "accepted" if accepted else "refused")] += 1
            per_lang[lang][("declarable" if all_decl else "demoted")
                           + "_" + ("accepted" if accepted else "refused")] += 1
            if not all_decl:
                if accepted:
                    accepted_but_demoted.append({
                        "language": lang, "id": "%s/probe_%s" % (lang, key),
                        "lhs_type": meta["lhs_type"],
                        "rhs_type": meta.get("rhs_type"),
                        "operator_unit_id": meta.get("operator_unit_id"),
                    })
                continue
            if verdict != "legal":
                per_lang[lang]["out_of_oracle_scope"] += 1
                per_lang[lang][("out_of_scope_accepted" if accepted
                                else "out_of_scope_refused")] += 1
                continue
            per_lang[lang]["in_oracle_scope"] += 1
            if accepted:
                per_lang[lang]["hit_accepted"] += 1
                continue
            text = probe.get("refused") or ""
            hits_q = [r for r in (meta.get("rule_ids") or [])
                      if (lang, r) in quirk_ids]
            if hits_q:
                per_lang[lang]["agreement_by_ratified_quirk"] += 1
                quirk_agreements.append({
                    "language": lang, "id": "%s/probe_%s" % (lang, key),
                    "lhs_type": meta["lhs_type"],
                    "rhs_type": meta.get("rhs_type"),
                    "operator_unit_id": meta.get("operator_unit_id"),
                    "ratified_quirk_rule_ids": hits_q,
                    "refusal": text,
                })
                continue
            per_lang[lang]["miss_predicted_legal_but_refused"] += 1
            sh = shape_of(text)
            shape_counts[sh][lang] += 1
            shape_units[sh].add(meta.get("operator_unit_id"))
            holders = meta["lhs_type"]
            if meta.get("rhs_type"):
                holders = holders + " with " + meta["rhs_type"]
            shape_holders[sh][holders] += 1
            if sh not in shape_example:
                shape_example[sh] = {
                    "language": lang, "id": "%s/probe_%s" % (lang, key),
                    "lhs_type": meta["lhs_type"],
                    "rhs_type": meta.get("rhs_type"),
                    "operator_unit_id": meta.get("operator_unit_id"),
                    "refusal": text,
                }
    doc = {}
    doc["generated_by"] = "regen_validate1.py"
    doc["population"] = (
        "the regeneration's 129,553 compiled probes as the trickle stores "
        "hold them (326 files, op_units2_*), banked 2026-09-02 per log 131. "
        "Nothing is compiled or re-run here.")
    doc["excluded_files"] = {
        "how_many": len(excluded),
        "why": "op_units_recapture_* is the ORIGINAL corpus re-captured for "
               "verbatim testimony -- a different population from the "
               "regeneration, so it is not scored here",
        "names": [os.path.basename(p) for p in excluded],
    }
    doc["files_read"] = len(files)
    doc["spelling_ban"] = (
        "groups are keyed by opaque message-shape ids and by operator UNIT "
        "ids; no key, grouping, pairing or row structure is an operator "
        "token")
    total = sum(cells.values())
    doc["totals"] = {
        "probes": total,
        "accepted": cells[("all_declarable", "accepted")]
                    + cells[("holder_demoted", "accepted")],
        "refused": cells[("all_declarable", "refused")]
                   + cells[("holder_demoted", "refused")],
        "holders_all_declarable_accepted":
            cells[("all_declarable", "accepted")],
        "holders_all_declarable_refused":
            cells[("all_declarable", "refused")],
        "holder_demoted_accepted": cells[("holder_demoted", "accepted")],
        "holder_demoted_refused": cells[("holder_demoted", "refused")],
    }
    doc["the_witness_refutation_check"] = {
        "claim": "no probe carrying a type the declaration lane demoted was "
                 "accepted by the probe lane",
        "count_that_would_refute_it": len(accepted_but_demoted),
        "rows": accepted_but_demoted[:50],
    }
    langs = []
    for lang in LANGS:
        row = {"language": lang}
        row.update(dict(per_lang[lang]))
        scope = row.get("in_oracle_scope", 0)
        hits = row.get("hit_accepted", 0) + row.get(
            "agreement_by_ratified_quirk", 0)
        row["agreement_in_oracle_scope"] = (
            round(100.0 * hits / scope, 1) if scope else None)
        langs.append(row)
    doc["languages"] = langs
    scope = sum(r.get("in_oracle_scope", 0) for r in langs)
    hits = sum(r.get("hit_accepted", 0) for r in langs)
    quirks = sum(r.get("agreement_by_ratified_quirk", 0) for r in langs)
    doc["oracle_scope_totals"] = {
        "in_oracle_scope": scope,
        "hit_accepted": hits,
        "agreement_by_ratified_quirk": quirks,
        "miss_predicted_legal_but_refused": scope - hits - quirks,
        "agreement": round(100.0 * (hits + quirks) / scope, 1)
                     if scope else None,
        "agreement_without_the_ruling": round(100.0 * hits / scope, 1)
                                        if scope else None,
    }
    doc["quirk_agreements"] = quirk_agreements
    doc["quirk_annotations_applied"] = quirk_doc["annotations"]
    shapes = []
    i = 0
    for sh in sorted(shape_counts, key=lambda s: -sum(shape_counts[s].values())):
        i += 1
        shapes.append({
            "shape_id": "shape_%04d" % i,
            "text": sh,
            "count": sum(shape_counts[sh].values()),
            "by_language": dict(shape_counts[sh]),
            "operator_unit_ids": sorted(x for x in shape_units[sh] if x),
            "holder_tally": [{"holders": h, "count": n}
                             for h, n in sorted(shape_holders[sh].items(),
                                                key=lambda kv: -kv[1])],
            "example": shape_example[sh],
        })
    doc["miss_shapes"] = shapes
    path = os.path.join(HERE, "regen_witness_validation1.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()

    t = doc["totals"]
    print("probes %d  accepted %d  refused %d"
          % (t["probes"], t["accepted"], t["refused"]))
    print("  holders all declarable : accepted %d  refused %d"
          % (t["holders_all_declarable_accepted"],
             t["holders_all_declarable_refused"]))
    print("  a holder demoted       : accepted %d  refused %d"
          % (t["holder_demoted_accepted"], t["holder_demoted_refused"]))
    print("oracle scope %d  hits %d  misses %d  agreement %s%%"
          % (doc["oracle_scope_totals"]["in_oracle_scope"],
             doc["oracle_scope_totals"]["hit_accepted"],
             doc["oracle_scope_totals"]["miss_predicted_legal_but_refused"],
             doc["oracle_scope_totals"]["agreement"]))
    for r in langs:
        print("  %-6s scope %6d hits %6d agree %5s%%  out-of-scope %d"
              % (r["language"], r.get("in_oracle_scope", 0),
                 r.get("hit_accepted", 0), r["agreement_in_oracle_scope"],
                 r.get("out_of_oracle_scope", 0)))
    print("miss shapes: %d" % len(shapes))
    for s in shapes[:15]:
        print("  %-11s %6d  %s" % (s["shape_id"], s["count"], s["text"][:95]))
    print("wrote %s" % path)
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
           path]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


if __name__ == "__main__":
    main()
