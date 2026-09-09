#!/usr/bin/env python3
"""unique_opcodes.py -- task o2 deliverable 2.

Per language: the set of distinct mnemonics across ALL its units'
body_verbatim (chaff included -- this is the raw vocabulary), with
occurrence count and unit count each, sorted by unit count. Then a
cross-language table: mnemonic down, language across, cell = unit
count, plus "languages using it".

Cross-check: every ledger row's produced_by.mnem (where
produced_by.kind == "arch_opcode") must be a subset of this
per-language mnemonic set. Reports any mismatch by name.

Streams shards; never holds the whole store at once.

Run:
    /usr/bin/time -v python3 unique_opcodes.py
"""
import json
import glob
import os
import resource
import re

LABEL_LINE_RE = re.compile(r'^[A-Za-z_.$][\w.$]*:$')

OP_PIPELINE = "PseudoCoupHQ/Research/op_pipeline"
OUT_DIR = "PseudoCoupHQ/Research/oracle/arch_opcodes"


def parse_mnem(insn):
    insn = insn.strip()
    if not insn:
        return None
    if LABEL_LINE_RE.match(insn):
        # a branch-target label definition (e.g. 'L0:') -- not an
        # instruction, so not an arch opcode.
        return None
    return insn.split(None, 1)[0]


def iter_all_units():
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(OP_PIPELINE, f"canon40_wrapped_{lang}.json")
        with open(path) as f:
            d = json.load(f)
        for uid, rec in d["units"].items():
            yield lang, uid, rec

    shard_paths = sorted(glob.glob(os.path.join(OP_PIPELINE, "canon40_regen_store", "*.json")))
    for path in shard_paths:
        with open(path) as f:
            d = json.load(f)
        for uid, rec in d["units"].items():
            lang = rec.get("lang")
            if lang is None:
                base = os.path.basename(path)
                lang = base.split("op_units2_")[1].split("_")[0]
            yield lang, uid, rec
        del d

    path = os.path.join(OP_PIPELINE, "canon40_interp.json")
    with open(path) as f:
        d = json.load(f)
    for uid, rec in d["units"].items():
        lang = rec.get("lang")
        yield lang, uid, rec


def main():
    # per lang -> mnem -> {"occurrences": N, "units": set(uid)}
    tally = {}
    ledger_mnems = {}  # per lang -> set of mnems seen in produced_by.kind==arch_opcode
    mismatches = []  # (lang, mnem, "in_ledger_not_body" / "in_body_not_ledger") -- reported, not expected

    for lang, uid, rec in iter_all_units():
        t = tally.setdefault(lang, {})
        bv = rec.get("body_verbatim") or []
        seen_this_unit = set()
        for insn in bv:
            m = parse_mnem(insn)
            if m is None:
                continue
            entry = t.setdefault(m, {"occurrences": 0, "units": set()})
            entry["occurrences"] += 1
            if m not in seen_this_unit:
                entry["units"].add(uid)
                seen_this_unit.add(m)

        lm = ledger_mnems.setdefault(lang, set())
        for row in rec.get("ledger", []) or []:
            pb = row.get("produced_by") or {}
            if pb.get("kind") == "arch_opcode":
                mnem = pb.get("mnem")
                if mnem:
                    lm.add(mnem)

    # Cross-check.
    for lang in sorted(set(tally) | set(ledger_mnems)):
        body_set = set(tally.get(lang, {}).keys())
        ledger_set = ledger_mnems.get(lang, set())
        only_ledger = sorted(ledger_set - body_set)
        only_body_not_ledger = sorted(body_set - ledger_set)
        for m in only_ledger:
            mismatches.append({"lang": lang, "mnem": m, "where": "in ledger produced_by, not in body_verbatim vocabulary"})
        # only_body_not_ledger is EXPECTED for chaff mnemonics (mov/ret/etc
        # that never directly produce a ledger row) -- report count only,
        # not as a mismatch, since the brief's cross-check direction is
        # "ledger mnemonics subset of body vocabulary".

    out = {"per_language": {}, "cross_language_rows": [], "cross_check_mismatches": mismatches,
           "note": "cross_check_mismatches lists any mnemonic named by a ledger row's "
                   "produced_by.kind=='arch_opcode' that is absent from that language's "
                   "body_verbatim vocabulary (the required subset direction). Mnemonics "
                   "present in body_verbatim but never a ledger producer (pure chaff, e.g. "
                   "mov/ret) are expected and not reported as mismatches."}

    for lang in sorted(tally):
        rows = []
        for mnem, entry in tally[lang].items():
            rows.append({"mnem": mnem, "occurrences": entry["occurrences"], "unit_count": len(entry["units"])})
        rows.sort(key=lambda r: (-r["unit_count"], r["mnem"]))
        out["per_language"][lang] = rows

    # Cross-language table.
    all_mnems = set()
    for lang in tally:
        all_mnems |= set(tally[lang].keys())
    langs_sorted = sorted(tally.keys())
    cross_rows = []
    for mnem in sorted(all_mnems):
        row = {"mnem": mnem}
        langs_using = []
        for lang in langs_sorted:
            cnt = len(tally.get(lang, {}).get(mnem, {}).get("units", set()))
            row[lang] = cnt
            if cnt > 0:
                langs_using.append(lang)
        row["languages_using_it"] = langs_using
        cross_rows.append(row)
    cross_rows.sort(key=lambda r: r["mnem"])
    out["cross_language_rows"] = cross_rows
    out["languages"] = langs_sorted

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "unique_opcodes.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    lines = []
    lines.append("# unique_opcodes -- task o2 deliverable 2")
    lines.append("")
    for lang in langs_sorted:
        rows = out["per_language"][lang]
        lines.append(f"## {lang} -- {len(rows)} unique arch opcodes")
        lines.append("")
        lines.append("| mnemonic | occurrences | unit count |")
        lines.append("|---|---|---|")
        for r in rows:
            lines.append(f"| {r['mnem']} | {r['occurrences']} | {r['unit_count']} |")
        lines.append("")

    lines.append("## cross-language table")
    lines.append("")
    header = "| mnemonic | " + " | ".join(langs_sorted) + " | languages using it |"
    sep = "|---|" + "---|" * len(langs_sorted) + "---|"
    lines.append(header)
    lines.append(sep)
    for row in cross_rows:
        cells = " | ".join(str(row[l]) for l in langs_sorted)
        lines.append(f"| {row['mnem']} | {cells} | {', '.join(row['languages_using_it'])} |")
    lines.append("")

    lines.append("## cross-check")
    lines.append("")
    if mismatches:
        lines.append(f"{len(mismatches)} mismatch(es):")
        for m in mismatches:
            lines.append(f"- {m['lang']}: `{m['mnem']}` -- {m['where']}")
    else:
        lines.append("0 mismatches: every ledger-row producing mnemonic is present in that "
                      "language's body_verbatim vocabulary.")
    lines.append("")

    with open(os.path.join(OUT_DIR, "unique_opcodes.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    for lang in langs_sorted:
        print(f"[{lang}] unique opcodes: {len(out['per_language'][lang])}")
    print(f"cross-language rows: {len(cross_rows)}")
    print(f"cross-check mismatches: {len(mismatches)}")
    print("wrote", os.path.join(OUT_DIR, "unique_opcodes.json"))
    print("wrote", os.path.join(OUT_DIR, "unique_opcodes.md"))


if __name__ == "__main__":
    main()
    peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"PEAK_RSS_KB={peak_kb} PEAK_RSS_MB={peak_kb/1024:.1f}")

