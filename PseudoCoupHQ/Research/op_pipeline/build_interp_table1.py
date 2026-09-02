#!/usr/bin/env python3
"""build_interp_table1.py -- TASK 32 part (b): THE INTERPRETER TABLE.

WHAT THIS IS.  the owner's ruling of 2026-09-01 (log_115): "INTERPRETER
TABLE: THREE VIEWS.  Compiled table, interpreter table, union --
joined by proved relations, nothing merged, nothing destroyed.
Membership is not a pending ontology question; it is construction."
This file builds the SECOND of the three views.  It does not open
`dominant_table24.json` or `dom_ops22.json` and it changes nothing in
them.

THE ROW SHAPE is `dominant_table24.json`'s own row shape, plus one
column.  A compiled row is

    {class_id, type_pair, result_type, canonical_text,
     members:[{unit, own_text_before_representative_substitution}]}

and an interpreter row is the same with `representation` added --
the representation column the owner ruled onto this line (the recorded
arrival representation of the operands: typed-pointer(T), tagged,
plain, or the unit's own recorded scheme where none of the three
fits).

THE CLASS KEY IS MACHINE FACT ONLY, four fields:

  * `type_pair`     -- the DWARF-read declared operand types, from
                       `dwarf_typed_key.json` (log_111).  Not a
                       width, not a guess: the compiler's own
                       DW_AT_type chain.  `null` where the read
                       refused, and a null key does not merge with
                       anything.
  * `result_type`   -- the DWARF-read return type, same source.
  * `representation`-- the recorded arrival representation.
  * `canonical_text`-- the unit's canonical runnable text.

No operator token participates in the key, in the grouping, or in the
choice of which units are compared.  A token appears exactly once per
unit, as the display label on that unit's own member record.

THE MODE ROWS are read from `guards5.json` -- the guard record of
record -- filtered to the interpreter/JIT languages by the row's own
`language` field, and cross-referenced to `exception_families3.json`
by family membership.  Nothing is invented here: this file reports
which recorded guard rows belong to the units in this table, and it
reports the branches `interp_canon34.py` measured on java unit 2's
normal path beside them, so the two routes can be compared.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Run:
  /tmp/reconnect_venv/bin/python3 build_interp_table1.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_table1.json")

INTERPRETER_LANGUAGES = ["cpython", "ruby", "php", "java"]


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def typed_key_rows():
    """unit id -> the DWARF record, from dwarf_typed_key.json."""
    doc = load("dwarf_typed_key.json")
    out = {}
    for rec in doc["records"]:
        out["%s/%s" % (rec["lang"], rec["handler"])] = rec
    return out


def representation_rows():
    doc = load("proposal_representation_dimension3.json")
    out = {}
    for rec in doc["handlers"]:
        out[rec["unit"]] = rec
    for rec in doc["additional_route_symbols_sliced_this_session"]:
        out[rec["unit"]] = rec
    return out


def arrival_mode_rows():
    """the recorded arrival mode measured by task 30."""
    doc = load("canon33_arrival_modes.json")
    out = {}
    for block in doc.values():
        if not isinstance(block, list):
            continue
        for rec in block:
            if not isinstance(rec, dict):
                continue
            if "unit" not in rec:
                continue
            if "arrival_mode" in rec or "recorded_representation" in rec:
                out[rec["unit"]] = rec
    return out


def collect_members():
    """every interpreter/JIT unit, with whatever canonical text is on
    record for it.  Four sources, all read-only."""
    members = []

    cpython = load("canon_interp_units_cpython.json")
    unit = cpython["unit"]
    members.append({
        "unit": "cpython/long_add_fastpath",
        "language": "cpython",
        "dwarf_unit": "cpython/long_add",
        "operator": unit["operator"],
        "canonical_text": cpython.get("canonical_text"),
        "own_text_before_representative_substitution":
            cpython["gate"]["real_text_checked"],
        "canonical_text_source":
            "canon_interp_units_cpython.json (TASK 21) -- the "
            "representative rule: the class's canonical text is the "
            "text this unit was PROVED_EQUAL to",
        "verdict_on_record": cpython["verdict"],
        "provenance_is_weaker": True,
    })

    java = load("canon_interp_units_java.json")
    one = java["unit_1"]
    members.append({
        "unit": "java/op_1",
        "language": "java",
        "dwarf_unit": None,
        "operator": one["operator"],
        "canonical_text": one.get("canonical_text"),
        "own_text_before_representative_substitution":
            one["real_text_checked"],
        "canonical_text_source":
            "canon_interp_units_java.json (TASK 21) -- the "
            "representative rule, as above",
        "verdict_on_record": one["verdict"],
        "provenance_is_weaker": True,
    })

    canon34 = load("interp_canon34.json")
    for rec in canon34["records"]:
        if not rec.get("canonical_text"):
            continue
        own = rec.get("computation_core")
        if own is None and rec.get("boundary"):
            own = [rec["boundary"]["instruction"]]
        members.append({
            "unit": rec["unit"],
            "language": rec["language"],
            "dwarf_unit": ("%s/%s" % (rec["language"], rec["symbol"])
                           if rec["language"] != "java" else None),
            "operator": rec.get("operator"),
            "canonical_text": rec["canonical_text"],
            "own_text_before_representative_substitution":
                "; ".join(own) if own else None,
            "canonical_text_source":
                "interp_canon34.json (TASK 32 part a) -- this unit's "
                "OWN computation core, rendered in the canonical form "
                "with task 30's designated locations",
            "verdict_on_record": rec["outcome"],
            "build": rec.get("build"),
            "designated_location_directory":
                rec.get("designated_location_directory"),
            "seats": rec.get("seats"),
            "provenance_is_weaker": True,
        })
    return members, canon34


def main():
    members, canon34 = collect_members()
    keys = typed_key_rows()
    reps = representation_rows()
    modes = arrival_mode_rows()

    for member in members:
        dwarf_unit = member.get("dwarf_unit")
        key_record = keys.get(dwarf_unit) if dwarf_unit else None
        if key_record is not None:
            member["type_pair"] = key_record.get("typed_key")
            member["result_type"] = key_record.get("return_type")
            member["type_key_outcome"] = key_record.get("outcome")
            member["type_key_refusal"] = key_record.get("refusal_reason")
            member["type_key_evidence_class"] = (
                "forced by construction -- the compiler's own DWARF "
                "DW_AT_type chain, dwarf_typed_key.json")
        else:
            member["type_pair"] = None
            member["result_type"] = None
            member["type_key_outcome"] = "NO DWARF"
            member["type_key_refusal"] = (
                "there is no ELF file for a JIT nmethod, so there is no "
                "DWARF to read; interp_jvm.json's recorded operand and "
                "result types are the JVM's own printed testimony, a "
                "weaker evidence class, and are carried on the member "
                "under type_pair_testimony rather than in the key")
            member["type_key_evidence_class"] = None
        rep = reps.get(dwarf_unit) if dwarf_unit else None
        if rep is not None:
            member["representation"] = rep.get("representation")
        else:
            member["representation"] = None
        mode = modes.get(member["unit"]) or (
            modes.get(dwarf_unit) if dwarf_unit else None)
        if mode is not None:
            member["arrival_mode_measured"] = (
                mode.get("arrival_mode")
                or mode.get("recorded_representation"))

    # java's two units carry testimony types, not DWARF types.
    jvm = load("interp_jvm.json")
    for unit in jvm["units"]:
        label = "java/op_%s" % unit["id"][1:]
        for member in members:
            if member["unit"] != label:
                continue
            member["type_pair_testimony"] = ",".join(unit["operand_types"])
            member["result_type_testimony"] = unit["result_type"]
            member["representation"] = "plain"
            member["representation_evidence_class"] = (
                "the tool's own testimony -- the JVM's own printed "
                "parameter comments declare both parameters `int` in "
                "registers, so neither operand arrives as an address "
                "or as a tagged word")

    # ---- the rows.  The key is four machine facts; no token.
    rows = []
    index = {}
    for member in sorted(members, key=lambda m: m["unit"]):
        key = (member.get("type_pair"),
               member.get("result_type"),
               member.get("representation"),
               member.get("canonical_text"))
        if key not in index:
            class_id = "IC%04d" % (len(rows) + 1)
            row = {
                "class_id": class_id,
                "type_pair": key[0],
                "result_type": key[1],
                "representation": key[2],
                "canonical_text": key[3],
                "members": [],
            }
            rows.append(row)
            index[key] = row
        row = index[key]
        carried = {}
        for field in ("unit", "language", "operator",
                      "own_text_before_representative_substitution",
                      "canonical_text_source", "verdict_on_record",
                      "build", "type_key_outcome", "type_key_refusal",
                      "type_key_evidence_class", "type_pair_testimony",
                      "result_type_testimony",
                      "representation_evidence_class",
                      "arrival_mode_measured",
                      "designated_location_directory", "seats",
                      "provenance_is_weaker"):
            if field in member:
                carried[field] = member[field]
        row["members"].append(carried)

    # ---- the units with no row, each with its reason.
    unplaced = []
    for rec in canon34["records"]:
        if rec.get("canonical_text"):
            continue
        unplaced.append({
            "unit": rec["unit"],
            "language": rec["language"],
            "operator": rec.get("operator"),
            "why_no_class": rec.get("refusal"),
            "carve_outcomes_per_build": rec.get("carve_outcomes_per_build"),
            "provenance_is_weaker": True,
        })

    # ---- the mode rows, read from the guard record of record.
    guards = load("guards5.json")
    families = load("exception_families3.json")
    family_of = {}
    for family in families["families"]:
        for entry in family["members"]:
            family_of.setdefault(entry["unit"], set()).add(
                family["family_id"])
    mode_rows = []
    for row in guards["rows"]:
        if row.get("language") not in INTERPRETER_LANGUAGES:
            continue
        here = dict(row)
        here["exception_family_ids"] = sorted(
            family_of.get(row["unit"], set()))
        mode_rows.append(here)

    # ---- the branches this lap MEASURED on java unit 2's normal path,
    # beside the recorded rows, so the two routes can be compared.
    measured = []
    for rec in canon34["records"]:
        if not rec.get("guards_passed_on_the_normal_path"):
            continue
        # NO display label is carried here.  The guard
        # (check_no_spelling_keys.py) refused this file's first output
        # because this entry is a measurement ROW, not a unit record --
        # and it was right.  The unit id names the member; its label
        # lives on that unit's own member record in `rows` above.
        measured.append({
            "unit": rec["unit"],
            "label_deliberately_absent":
                "see this file's note on the guard refusal",
            "branches": rec["guards_passed_on_the_normal_path"],
            "route": "interp_canon34.py's own lineage walk over the "
                     "unit's recorded objdump -- an independent route "
                     "from the guard record of record",
        })

    out = {
        "meta": {
            "generator": "build_interp_table1.py",
            "role_note": "GROUPING/matching artifact (top-level `rows`, "
                         "each with `members`) -- checked by "
                         "check_no_spelling_keys.py IN FULL, no "
                         "exemption claimed.",
            "task": "TASK 32 part (b) -- the interpreter table, the "
                    "second of the owner's three views",
            "row_shape": "dominant_table24.json's own row shape plus "
                         "the representation column",
            "class_key": "(type_pair, result_type, representation, "
                         "canonical_text) -- four machine facts, no "
                         "token",
            "type_key_source": "dwarf_typed_key.json (log_111): the "
                               "compiler's own DW_AT_type chain",
            "representation_source":
                "proposal_representation_dimension3.json (log_113)",
            "canonical_text_sources": [
                "canon_interp_units_cpython.json (TASK 21)",
                "canon_interp_units_java.json (TASK 21)",
                "interp_canon34.json (TASK 32 part a)"],
            "guard_source": "guards5.json, filtered to the "
                            "interpreter/JIT languages by each row's "
                            "own `language` field",
            "does_not_open": ["dominant_table24.json", "dom_ops22.json"],
            "provenance_is_weaker": True,
        },
        "population": {
            "interpreter_and_jit_units_considered": len(members) + len(unplaced),
            "with_canonical_text": len(members),
            "without_canonical_text": len(unplaced),
        },
        "rows": rows,
        "units_with_no_class_and_why": unplaced,
        "mode_rows": mode_rows,
        "normal_path_branches_measured_this_lap": measured,
        "summary": {
            "class_count": len(rows),
            "member_count": sum([len(r["members"]) for r in rows]),
            "mode_row_count": len(mode_rows),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for row in rows:
        print("%s  type_pair=%-30s result=%-18s rep=%-40s  %s"
              % (row["class_id"], row["type_pair"], row["result_type"],
                 row["representation"], row["canonical_text"]))
        for member in row["members"]:
            print("        %s" % member["unit"])
    print("no class: %s" % [u["unit"] for u in unplaced])
    print("summary: %s" % out["summary"])
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
         OUT], capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % OUT)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
