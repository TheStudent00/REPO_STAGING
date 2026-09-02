#!/usr/bin/env python3
"""probe_gen2.py -- the REGENERATION candidate set: every operator unit
crossed with the language's full extracted scalar core, with the legality
filter's verdict recorded on each candidate.

WHAT IS DIFFERENT FROM probe_gen.py, AND NOTHING ELSE IS

  - HOLDERS.  probe_gen.py carries six hand-written holder types per
    language.  This program uses the language's EXTRACTED scalar core
    from `core_rule2.py` -- 56 c, 56 cpp, 14 go, 15 rust, 17 swift.
  - THE FILTER'S VERDICT.  Each candidate carries `filter_verdict`, one
    of `legal`, `illegal`, `no_rule`.  Only `legal` and `no_rule`
    candidates are handed to a compiler; `illegal` ones are skipped,
    which is the whole point of the filter.
  - A SEPARATE ID SPACE.  Probes are numbered from 0 in a NEW manifest
    (`probe_manifest2_<lang>.json`).  The existing corpus's `op_<n>` ids
    are untouched and no store of this run is written over one of theirs.

Everything else -- the source templates, the result-type rules, the
operator inventory, the constant ban, the acceptance-is-the-compiler's
rule -- is probe_gen.py's, imported rather than copied, so the two cannot
drift.

THE SPELLING BAN.  Candidates are enumerated from the grammar-authored
operator inventory crossed with extracted TYPE evidence, and filtered by
RULE ID.  No key, grouping, pairing or selection anywhere here is an
operator token; the token sits in each probe's `operator` display field,
exactly as probe_gen.py's manifests already carry it.

usage:
    /tmp/reconnect_venv/bin/python3 probe_gen2.py c cpp go rust swift
writes:
    probe_manifest2_<lang>.json
    probe_residue2.json          (the per-language tallies, one page)
"""

import argparse
import json
import os
import subprocess
import sys

import core_rule2
import legality_filter as v1
import probe_gen

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

# The six campaign rep names, so a candidate at one of the original
# holder types keeps the name the arch campaign used and the two runs can
# be lined up without a translation table.  A type outside the six is
# named by its own spelling.
def rep_name(lang, spelling):
    for rep, ty in probe_gen.HOLDERS[lang]:
        if ty == spelling:
            return rep
    return spelling


def unit_index(units, lang):
    """(arity, position, spelling) -> the rule-carrying unit row."""
    index = {}
    for row in units[lang]:
        index[(row["arity"], row["position"], row["spelling"])] = row
    return index


def build(lang, arity_inv, inv, by_id, units):
    core, _undecided = core_rule2.scalar_core(lang, inv)
    holders = []
    for spelling, _marking, cls in core:
        holders.append((rep_name(lang, spelling), spelling, cls))
    ops, excluded_ops = probe_gen.candidates(lang, arity_inv)
    index = unit_index(units, lang)

    probes = {}
    tally = {"legal": 0, "illegal": 0, "no_rule": 0,
             "unit_not_in_the_rule_document": 0}
    n = 0
    for op, arity, pos, bucket in ops:
        row = index.get((arity, pos, op))
        bodies = v1.unit_bodies(by_id, row) if row else []
        if row is None:
            # The rule document's unit list comes from the corpus's own
            # acceptance record; a grammar operator absent from it has no
            # rule and no unit object, so it is passed through exactly as
            # a no-rule unit is, and counted separately so the gap is
            # visible rather than silent.
            verdict_default = "no_rule"
            tally["unit_not_in_the_rule_document"] = (
                tally["unit_not_in_the_rule_document"] + 1)
        elif not bodies:
            verdict_default = "no_rule"
        else:
            verdict_default = None

        pairs = []
        if arity == "binary":
            for lrep, lty, lcls in holders:
                for rrep, rty, rcls in holders:
                    pairs.append((lrep, lty, lcls, rrep, rty, rcls))
        else:
            for lrep, lty, lcls in holders:
                pairs.append((lrep, lty, lcls, None, None, None))

        for lrep, lty, lcls, rrep, rty, rcls in pairs:
            if verdict_default is not None:
                verdict = verdict_default
            else:
                ok = v1.admits(bodies, lcls, lty, rcls, rty, arity)
                verdict = "legal" if ok else "illegal"
            tally[verdict] = tally[verdict] + 1
            if verdict == "illegal":
                # not compiled, and not written into the manifest: the
                # filter's whole job is that these never reach a compiler
                continue
            rec = probe_record(lang, n, op, arity, pos, bucket,
                               lrep, lty, rrep, rty)
            rec["filter_verdict"] = verdict
            rec["rule_ids"] = list(row["rule_ids"]) if row else []
            rec["operator_unit_id"] = row["id"] if row else None
            probes[str(n)] = rec
            n = n + 1

    meta = {}
    meta["language"] = lang
    meta["generated_by"] = "probe_gen2.py"
    # The same declaration probe_gen.py's manifests carry: a manifest is
    # the record of what was handed to a compiler, so its operator field
    # is the provenance of the probe and never a grouping key.
    meta["role"] = "generator provenance"
    meta["holders"] = [{"language": lang,
                        "id": "%s/holder_%d" % (lang, i),
                        "rep": holders[i][0],
                        "spelling": holders[i][1],
                        "normalised_class": holders[i][2]}
                       for i in range(len(holders))]
    meta["holder_rule"] = "core_rule2.py (v2 scalar core)"
    meta["buckets_read"] = list(probe_gen.BUCKETS)
    meta["excluded_buckets"] = probe_gen.EXCLUDED_BUCKETS
    meta["excluded_operators"] = excluded_ops
    meta["filter"] = ("legality_rules.json as legality_filter2.py applies "
                      "it; a candidate marked illegal is not written here "
                      "and never reaches a compiler")
    meta["acceptance"] = ("not consulted -- acceptance is discovered by the "
                          "compiler in the lane, never assumed here")
    meta["constants"] = "banned -- every operand is a parameter"
    meta["id_space"] = ("numbered from 0 in this manifest; the existing "
                        "corpus's op_<n> ids are a different space and are "
                        "not touched")
    return meta, probes, tally


def probe_record(lang, n, op, arity, pos, bucket, lrep, lty, rrep, rty):
    """One candidate, rendered by probe_gen.py's own templates."""
    rec = {}
    rec["n"] = n
    rec["operator"] = op
    rec["arity"] = arity
    rec["position"] = pos
    rec["bucket"] = bucket
    rec["lhs_rep"] = lrep
    rec["lhs_type"] = lty
    rec["rhs_rep"] = rrep
    rec["rhs_type"] = rty
    rec["expression"] = probe_gen.expression(op, arity, pos)
    symbol = "op_%d" % n
    exact = True
    result = None
    rule = None
    if lang == "c":
        source = probe_gen.emit_c(n, op, arity, pos, lty, rty)
        rule = "compiler_states_it_typeof"
    elif lang == "cpp":
        source = probe_gen.emit_cpp(n, op, arity, pos, lty, rty)
        rule = "compiler_states_it_auto"
    else:
        result, rule = probe_gen.RESULT[lang](op, arity, pos, lty, rty)
        if lang == "go":
            source = probe_gen.emit_go(n, op, arity, pos, lty, rty, result)
            symbol = "main.op_%d" % n
        elif lang == "rust":
            source = probe_gen.emit_rust(n, op, arity, pos, lty, rty, result)
        else:
            source, cdecl = probe_gen.emit_swift(n, op, arity, pos, lty, rty,
                                                 result)
            exact = cdecl
    rec["result_type"] = result
    rec["result_rule"] = rule
    rec["symbol"] = symbol
    rec["symbol_exact"] = exact
    rec["source"] = source
    return rec


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=LANGS)
    args = ap.parse_args()
    langs = args.langs or LANGS

    arity_inv = json.load(open(probe_gen.ARITY))
    _rules_doc, inv, by_id, units = v1.load()

    summary = {}
    summary["generated_by"] = "probe_gen2.py"
    summary["languages"] = []
    written = []
    grand = 0
    for lang in langs:
        meta, probes, tally = build(lang, arity_inv, inv, by_id, units)
        path = os.path.join(HERE, "probe_manifest2_%s.json" % lang)
        doc = {"meta": meta, "count": len(probes), "probes": probes}
        fh = open(path, "w")
        json.dump(doc, fh, indent=1)
        fh.write("\n")
        fh.close()
        written.append(path)
        grand = grand + len(probes)
        summary["languages"].append({
            "language": lang,
            "scalar_core_size": len(meta["holders"]),
            "candidates_naive": tally["legal"] + tally["illegal"]
                                + tally["no_rule"],
            "filter_legal": tally["legal"],
            "filter_illegal_skipped": tally["illegal"],
            "filter_no_rule_passed_through": tally["no_rule"],
            "to_compile": len(probes),
            "operators_absent_from_the_rule_document": tally[
                "unit_not_in_the_rule_document"],
        })
        print("%-6s core %2d   naive %7d   legal %7d   no-rule %6d   "
              "illegal(skipped) %7d   TO COMPILE %7d"
              % (lang, len(meta["holders"]),
                 tally["legal"] + tally["illegal"] + tally["no_rule"],
                 tally["legal"], tally["no_rule"], tally["illegal"],
                 len(probes)))
    summary["total_to_compile"] = grand
    spath = os.path.join(HERE, "probe_residue2.json")
    fh = open(spath, "w")
    json.dump(summary, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("TOTAL to compile: %d" % grand)
    print("wrote %s" % spath)
    refuse_own_output_on_spelling_failure(written + [spath])


if __name__ == "__main__":
    main()
