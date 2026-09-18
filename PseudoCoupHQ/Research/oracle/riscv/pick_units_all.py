#!/usr/bin/env python3
"""pick_units_all.py -- EVERY arch-unit that has BOTH lowerings on record,
written as `units_all.json` and `carved_all.json` for `claim_check.py`.

`pick_units.py` chose ELEVEN units, one per cell of the arch-opcode model
table, because task rv1 was a handful. Nothing about `claim_check.py` is
limited to eleven: it walks a unit's x86-64 ship body with
`op_pipeline/reference.py`, walks its riscv64 body with the RISC-V reference,
and asks z3 whether the two agree at the unit's own answer width. This file
hands it every unit for which both bodies exist.

They all do. `attest_rv.json` carries a riscv64 body for 507 units and marks
`x86_ship_body_in_the_store` on every one of them.

WHERE EACH FIELD COMES FROM, so no field is invented:

  riscv64 body, lang, operator, operand types, expression, symbol
                                      `attest_rv.json`
  x86-64 ship body                    `op_pipeline/op_units_<lang>.json`,
                                      the probe's own `ship.mnem`
  the x86 ANSWER HOME and arrivals    `op_pipeline/term66_store`, the term
                                      store's `result_family`,
                                      `result_width`, `arrival_families`
  the x86 term as text                the same record's
                                      `layer5_normalized_text`, carried so
                                      `claim_check` can show its
                                      re-derivation IS the stored term

A unit whose term store record is missing is NOT guessed at -- the answer
home is what the comparison reads out of, and inventing one would invent the
verdict. Such a unit is written with outcome `NO_TERM_STORE_RECORD` and
`claim_check` skips it, exactly as it skips `NO_CORPUS_UNIT`.

THE SPELLING BAN: no operator token is used for any key, grouping, pairing or
selection here. The pairing key is the unit name, which is machine-formed
(`<lang>/op_<n>`), and the operator token is carried as a display label only.

    python3 pick_units_all.py <op_pipeline dir> <attest_rv.json> <out dir>
"""

import json
import os
import sys


def read_json(path):
    fh = open(path)
    try:
        return json.load(fh)
    finally:
        fh.close()


def ship_bodies(op_dir, lang):
    """probe number (str) -> its x86-64 ship body, from the probe's own store."""
    path = os.path.join(op_dir, "op_units_%s.json" % lang)
    out = {}
    for number, unit in (read_json(path).get("probes") or {}).items():
        body = list((unit.get("ship") or {}).get("mnem") or [])
        if body:
            out[str(number)] = body
    return out


def term_records(op_dir, wanted):
    """unit name -> its term store record, for the wanted names. One pass."""
    store = os.path.join(op_dir, "term66_store")
    out = {}
    for name in sorted(os.listdir(store)):
        if not name.endswith(".json"):
            continue
        doc = read_json(os.path.join(store, name))
        for key, rec in (doc.get("units") or {}).items():
            if key in wanted and key not in out:
                copy = dict(rec)
                copy["term_store_shard"] = name
                out[key] = copy
    return out


def main():
    op_dir, attest_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    attest = read_json(attest_path)["rows"]
    units = [r for r in attest if r.get("body")]
    wanted = set(r["unit"] for r in units)
    print("arch-units with a riscv64 body: %d" % len(units))

    ships = {}
    for lang in sorted(set(r["lang"] for r in units)):
        ships[lang] = ship_bodies(op_dir, lang)
        print("  %-4s probes with an x86-64 ship body: %d" % (lang,
                                                              len(ships[lang])))
    terms = term_records(op_dir, wanted)
    print("  term store records found: %d of %d" % (len(terms), len(wanted)))

    rows, carved, skipped = [], [], {}
    for r in units:
        lang = r["lang"]
        number = r["unit"].split("/")[1].split("_")[1]
        body = (ships.get(lang) or {}).get(number)
        rec = terms.get(r["unit"])
        row = {
            "unit": r["unit"], "lang": lang,
            "mnem": (r["body"][0].split() or [""])[0],
            "shape": "", "key_width": r.get("answer_bits"),
            "operator": r.get("operator"), "expression": r.get("expression"),
            "lhs_type": r.get("lhs_type"), "rhs_type": r.get("rhs_type"),
            "symbol": r.get("symbol"), "probe_number": int(number),
            "attest_outcome": r.get("outcome"),
        }
        if not body:
            row["outcome"] = "NO_X86_SHIP_BODY"
            row["why"] = "the probe store holds no shipped x86-64 body"
        elif rec is None:
            row["outcome"] = "NO_TERM_STORE_RECORD"
            row["why"] = ("no term store record, so the x86 answer home is "
                          "unknown and is NOT guessed")
        elif rec.get("result_family") is None or rec.get("result_width") is None:
            row["outcome"] = "NO_ANSWER_HOME"
            row["why"] = "the term store record names no answer home"
        else:
            row["outcome"] = "PICKED"
            row["why"] = "both lowerings on record"
            row["x86_ship_body"] = body
            row["x86_result_family"] = rec["result_family"]
            row["x86_result_width"] = rec["result_width"]
            row["x86_arrival_families"] = rec.get("arrival_families") or []
            row["x86_term"] = rec.get("layer5_normalized_text")
            row["x86_term_outcome"] = rec.get("outcome")
            row["term_store_shard"] = rec.get("term_store_shard")
            carved.append({"unit": r["unit"], "lang": lang,
                           "body": r["body"], "mnem": row["mnem"],
                           "shape": "", "key_width": row["key_width"],
                           "outcome": "CARVED",
                           "instruction_count": r.get("instruction_count")})
        skipped[row["outcome"]] = skipped.get(row["outcome"], 0) + 1
        rows.append(row)

    os.makedirs(out_dir, exist_ok=True)
    u = {"meta": {"what": "every arch-unit with both a riscv64 body and an "
                          "x86-64 ship body, for claim_check.py",
                  "source_attest": os.path.basename(attest_path),
                  "counts": skipped},
         "rows": rows}
    json.dump(u, open(os.path.join(out_dir, "units_all.json"), "w"),
              indent=1, sort_keys=True)
    json.dump({"meta": {"what": "the riscv64 bodies, from attest_rv.json"},
               "rows": carved},
              open(os.path.join(out_dir, "carved_all.json"), "w"),
              indent=1, sort_keys=True)
    print()
    for k in sorted(skipped):
        print("  %-24s %d" % (k, skipped[k]))
    print("wrote %s/units_all.json and carved_all.json" % out_dir)


if __name__ == "__main__":
    main()
