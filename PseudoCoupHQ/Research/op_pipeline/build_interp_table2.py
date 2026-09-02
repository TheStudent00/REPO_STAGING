#!/usr/bin/env python3
"""build_interp_table2.py -- TASK 34 part (b): the interpreter table,
rebuilt on THE UNIVERSAL CANONICAL FORM.

WHAT IS DIFFERENT FROM `build_interp_table1.py`, and it is the ruling.

  1.  The text in every row is the UNIVERSAL text from
      `interp_canon35.json`: designated locations for every traced
      value, standardized loads at the top, one shape for every
      arrival.  table1's texts were the register-based render and are
      superseded as the primary statement; they are carried on each
      member as `register_form_text_superseded` so nothing is lost.
  2.  ARRIVAL IS AN ANNOTATION, NOT A KEY COMPONENT.  the owner, 2026-09-01:
      "special structures like pointers and the bulk of
      register-friendly binary operators MEET IN THE MIDDLE on the same
      memory-based form, with HOW the value arrived carried as
      annotation"; and, ruled the same day, "same instructions +
      different modes = a finding to record".  So the class key is
      (type_pair, result_type, universal_text) and every class whose
      members carry more than one arrival annotation is emitted as a
      recorded finding.  Keeping the annotation in the key would have
      re-created the separate dialects the ruling dissolves.
  3.  ELEVEN units are answered for, not eight.

The key is machine facts only.  No operator token participates in the
key, in the grouping, or in the choice of what is compared.

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
  /tmp/reconnect_venv/bin/python3 build_interp_table2.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_table2.json")

INTERPRETER_LANGUAGES = ("cpython", "java", "ruby", "php")

DWARF_UNIT = {
    "cpython/long_add_fastpath": "cpython/long_add",
    "ruby/rb_fix_plus": "ruby/rb_fix_plus",
    "ruby/rb_int_plus": "ruby/rb_int_plus",
    "php/add_function": "php/add_function",
    "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER":
        "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER",
    "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER":
        "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER",
    "php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER":
        "php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER",
}


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def typed_key_rows():
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


def members_from_canon35():
    doc = load("interp_canon35.json")
    members = []
    for rec in doc["records"]:
        if rec.get("outcome") != "UNIVERSAL_TEXT_PRODUCED":
            continue
        members.append({
            "unit": rec["unit"],
            "language": rec["language"],
            "operator": rec.get("operator"),
            "universal_text": rec["universal_text"],
            "standardized_loads": rec.get("standardized_loads"),
            "core_after_substitution": rec.get("core_after_substitution"),
            "designated_location_directory":
                rec.get("designated_location_directory"),
            "seats_in_the_universal_form":
                rec.get("seats_in_the_universal_form"),
            "arrival_annotation": rec.get("arrival_annotation"),
            "register_form_text_superseded": rec.get("prior_text"),
            "register_form_source": rec.get("prior_text_source"),
            "gate_verdict": rec.get("gate_verdict"),
            "gate_detail": rec.get("gate_detail"),
            "build": rec.get("build"),
            "provenance_is_weaker": True,
        })
    return members, doc


def main():
    members, canon35 = members_from_canon35()
    keys = typed_key_rows()
    reps = representation_rows()

    for member in members:
        dwarf_unit = DWARF_UNIT.get(member["unit"])
        record = keys.get(dwarf_unit) if dwarf_unit else None
        if record is not None:
            member["type_pair"] = record.get("typed_key")
            member["result_type"] = record.get("return_type")
            member["type_key_outcome"] = record.get("outcome")
            member["type_key_refusal"] = record.get("refusal_reason")
            member["type_key_evidence_class"] = (
                "forced by construction -- the compiler's own DWARF "
                "DW_AT_type chain, dwarf_typed_key.json")
        else:
            member["type_pair"] = None
            member["result_type"] = None
            member["type_key_outcome"] = "NO DWARF"
            member["type_key_refusal"] = (
                "there is no ELF file for a JIT nmethod, so there is no "
                "DWARF to read; a null key merges with nothing, which "
                "is the intended behaviour")
            member["type_key_evidence_class"] = None
        representation = reps.get(dwarf_unit) if dwarf_unit else None
        if representation is not None:
            member["arrival_annotation_source"] = (
                "proposal_representation_dimension3.json (log_113)")
            if not member.get("arrival_annotation"):
                member["arrival_annotation"] = representation.get(
                    "representation")

    jvm = load("interp_jvm.json")
    for unit in jvm["units"]:
        label = "java/op_%s" % unit["id"][1:]
        for member in members:
            if member["unit"] != label:
                continue
            member["type_pair_testimony"] = ",".join(unit["operand_types"])
            member["result_type_testimony"] = unit["result_type"]
            member["arrival_annotation"] = "plain"
            member["arrival_annotation_evidence_class"] = (
                "the tool's own testimony -- the JVM's own printed "
                "parameter comments declare both parameters `int` in "
                "registers")

    # ---- the rows.  Three machine facts; arrival is an annotation.
    rows = []
    index = {}
    for member in sorted(members, key=lambda m: m["unit"]):
        key = (member.get("type_pair"),
               member.get("result_type"),
               member.get("universal_text"))
        if key not in index:
            class_id = "IU%04d" % (len(rows) + 1)
            row = {
                "class_id": class_id,
                "type_pair": key[0],
                "result_type": key[1],
                "universal_text": key[2],
                "arrival_annotations_present": [],
                "members": [],
            }
            rows.append(row)
            index[key] = row
        row = index[key]
        row["members"].append(member)
        annotation = member.get("arrival_annotation")
        if annotation not in row["arrival_annotations_present"]:
            row["arrival_annotations_present"].append(annotation)

    # ---- the finding the ruling asks for by name.
    findings = []
    for row in rows:
        if len(row["arrival_annotations_present"]) < 2:
            continue
        findings.append({
            "class_id": row["class_id"],
            "universal_text": row["universal_text"],
            "arrival_annotations": row["arrival_annotations_present"],
            "members": [m["unit"] for m in row["members"]],
            "why_this_is_recorded":
                "same instructions, different arrival modes.  Ruled "
                "2026-09-01: that is a finding to record, not a reason "
                "to split the class -- the arrival is an annotation on "
                "the one shared form.",
        })

    # ---- the cross-language text identities the ruling produced.
    #
    # These are OBSERVATIONS, not classes.  Two units whose universal
    # texts are character-identical but whose declared type keys differ
    # stay in separate classes -- the result-type split stands (the owner,
    # 2026-08-26).  What the ruling produced is that the TEXTS now
    # coincide at all, which the register-based render hid, so the
    # coincidence is recorded where it can be read.
    identities = []
    by_text = {}
    for row in rows:
        by_text.setdefault(row["universal_text"], []).append(row)
    for text in sorted(by_text):
        group = by_text[text]
        units = []
        languages = set()
        for row in group:
            for member in row["members"]:
                units.append(member["unit"])
                languages.add(member["language"])
        if len(languages) < 2:
            continue
        identities.append({
            "universal_text": text,
            "languages": sorted(languages),
            "members": sorted(units),
            "class_ids": [row["class_id"] for row in group],
            "type_keys_that_keep_them_separate": [
                {"class_id": row["class_id"],
                 "type_pair": row["type_pair"],
                 "result_type": row["result_type"]}
                for row in group],
            "arrival_annotations": sorted(set(
                str(m["arrival_annotation"])
                for row in group for m in row["members"])),
            "level": "level 1 -- character identity of the universal "
                     "text, no proof required.  Recorded as an "
                     "observation; the classes are NOT merged, because "
                     "the declared type keys differ and the result-type "
                     "split stands.",
        })

    unplaced = []
    for rec in canon35["records"]:
        if rec.get("outcome") == "UNIVERSAL_TEXT_PRODUCED":
            continue
        unplaced.append({
            "unit": rec["unit"],
            "language": rec["language"],
            "operator": rec.get("operator"),
            "why_no_class": rec.get("refusal"),
            "provenance_is_weaker": True,
        })
    for row in canon35["units_with_no_universal_text"]:
        unplaced.append({
            "unit": row["unit"],
            "language": row["language"],
            "why_no_class": row["why_not"],
            "ship_body_present_in_the_dump":
                row.get("ship_body_present_in_the_dump"),
            "is_this_a_register_scarcity_refusal": False,
            "what_would_change_it": row.get("what_would_change_it"),
            "provenance_is_weaker": True,
        })

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
        here["exception_family_ids"] = sorted(family_of.get(row["unit"],
                                                            set()))
        mode_rows.append(here)

    measured = []
    for rec in canon35["records"]:
        branches = rec.get("guards_passed_on_the_normal_path")
        if not branches:
            continue
        measured.append({
            "unit": rec["unit"],
            "branches": branches,
            "route": "interp_canon35.py's own lineage walk over the "
                     "unit's recorded objdump -- an independent route "
                     "from the guard record of record",
        })
        metadata = rec.get("arrival_metadata_reads")
        if metadata:
            measured[-1]["arrival_metadata_reads"] = metadata

    out = {
        "meta": {
            "generator": "build_interp_table2.py",
            "role_note": "GROUPING/matching artifact (top-level `rows`, "
                         "each with `members`) -- checked by "
                         "check_no_spelling_keys.py IN FULL, no "
                         "exemption claimed.",
            "task": "TASK 34 part (b) -- the interpreter table on the "
                    "universal canonical form",
            "ruling": "AgentMemory 2026-09-01, THE UNIVERSAL CANONICAL "
                      "FORM",
            "supersedes": "interp_table1.json (register-based texts, "
                          "arrival inside the key, 8 of 11 units)",
            "class_key": "(type_pair, result_type, universal_text) -- "
                         "three machine facts, no token; arrival is an "
                         "ANNOTATION and is deliberately not in the key",
            "type_key_source": "dwarf_typed_key.json (log_111)",
            "text_source": "interp_canon35.json (TASK 34 part a), every "
                           "text z3-gated against its own unit's prior "
                           "text",
            "guard_source": "guards5.json, filtered by each row's own "
                            "`language` field",
            "does_not_open": ["dominant_table24.json", "dom_ops22.json"],
            "provenance_is_weaker": True,
        },
        "population": {
            "interpreter_and_jit_units_on_record": 11,
            "per_language": {"cpython": 1, "java": 2, "ruby": 4,
                             "php": 4},
            "with_universal_text": len(members),
            "without_universal_text": len(unplaced),
        },
        "rows": rows,
        "units_with_no_class_and_why": unplaced,
        "same_text_different_arrival_findings": findings,
        "cross_language_text_identities": identities,
        "mode_rows": mode_rows,
        "normal_path_branches_measured_this_lap": measured,
        "summary": {
            "class_count": len(rows),
            "member_count": sum([len(r["members"]) for r in rows]),
            "mode_row_count": len(mode_rows),
            "same_text_different_arrival_count": len(findings),
            "cross_language_identity_count": len(identities),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for row in rows:
        print("%s  type_pair=%-28s result=%-16s arrivals=%s"
              % (row["class_id"], row["type_pair"], row["result_type"],
                 row["arrival_annotations_present"]))
        print("        %s" % row["universal_text"])
        for member in row["members"]:
            print("            %s" % member["unit"])
    print("no class: %s" % [u["unit"] for u in unplaced])
    print("summary: %s" % json.dumps(out["summary"]))
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
