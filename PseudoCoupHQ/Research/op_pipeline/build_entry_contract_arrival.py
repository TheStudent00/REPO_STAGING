#!/usr/bin/env python3
"""build_entry_contract_arrival.py -- TASK 19 step 1.

Extends canon7's entry-contract record (each unit's `context_record`:
operand_widths, hardware_pins, temp_pool_order, callee_saved_used,
answer -- the precedent this task extends) with an ARRIVAL section per
unit: representation and the unpacking prefix, carved by the lineage-
confluence rule (AgentMemory, 2026-08-31).

Compiled-language units (all of canon7_units_c/cpp/go/rust/swift.json)
receive representation="plain" and unpacking_prefix=[] EXPLICITLY --
stated on every unit, never omitted, per the brief. The reasoning: a
compiled unit's arguments arrive as plain fixed-width register values
(canon7's own context_record.operand_widths already records this),
so there is no pointer/tag to unpack before the two lineages (a's
derivatives and b's derivatives) can meet -- the lineage-confluence
boundary is the unit's very first instruction that reads both inputs,
which for a plain register value IS the entry, so the unpacking
prefix is empty by construction, not by omission.

THIS SCRIPT DOES NOT MODIFY canon7_units_*.json. It reads them and
writes ONE new file per language plus a combined index, all new.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the
member. MECHANICAL GUARD REQUIRED: every pipeline stage that groups
or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.
"""
import json

LANGS = ["c", "cpp", "go", "rust", "swift"]

combined = {}
per_lang_counts = {}

for lang in LANGS:
    src = json.load(open("canon7_units_%s.json" % lang))
    units = src["units"]
    out_units = {}
    for key, u in units.items():
        cr = u.get("context_record", {})
        arrival = {
            "representation": "plain",
            "unpacking_prefix": [],
            "unpacking_prefix_instruction_count": 0,
            "boundary": "unit entry -- both operands are already "
                        "plain fixed-width register values at entry "
                        "(context_record.operand_widths), so the "
                        "lineage-confluence boundary (the first "
                        "instruction whose ancestors include BOTH "
                        "a's and b's derivatives) is the unit's own "
                        "first instruction; there is no prefix before "
                        "it.",
            "stated_explicitly": True,
        }
        out_units[key] = {
            "lang": u.get("lang"),
            "n": u.get("n"),
            "unit": u.get("unit"),
            "operator": u.get("operator"),
            "context_record": cr,
            "arrival": arrival,
        }
    per_lang_counts[lang] = len(out_units)
    out = {
        "meta": {
            "generator": "build_entry_contract_arrival.py",
            "role_note": "extends canon7's entry-contract record "
                         "(context_record) with an ARRIVAL section "
                         "per unit, per TASK 19 step 1. Does not "
                         "modify canon7_units_%s.json." % lang,
            "source": "canon7_units_%s.json" % lang,
            "unit_count": len(out_units),
            "spelling": "the operator token appears once per unit as "
                        "a display label on a unit-identifying object "
                        "(carries 'lang' and 'n'/'unit').",
        },
        "units": out_units,
    }
    fname = "entry_contract_arrival_%s.json" % lang
    with open(fname, "w") as f:
        json.dump(out, f, indent=1)
    combined[lang] = fname

index = {
    "meta": {
        "generator": "build_entry_contract_arrival.py",
        "role_note": "index of the per-language entry-contract "
                     "ARRIVAL extension files (TASK 19 step 1). "
                     "Compiled units all carry representation='plain' "
                     "and an empty unpacking_prefix, stated explicitly "
                     "per unit, never omitted.",
        "per_lang_files": combined,
        "per_lang_unit_counts": per_lang_counts,
        "total_units": sum(per_lang_counts.values()),
    },
}
with open("entry_contract_arrival_index.json", "w") as f:
    json.dump(index, f, indent=1)

print(json.dumps(per_lang_counts, indent=2))
print("total:", sum(per_lang_counts.values()))
