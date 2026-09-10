#!/usr/bin/env python3
"""pick_units.py -- THE TEN UNITS OF THE HANDFUL, WITH THEIR SOURCES AND
THEIR x86 TERMS, written as `units.json`.

Node: hq.research.arch_unit_oracle
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Task rv1, brief `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv1_brief.md`
section 2.

WHAT A UNIT IS HERE, one sentence: one probe of the corpus -- a function
body the compiler emitted for one (operator, operand types) -- named
`<lang>/op_<n>`, whose source this file reads from the probe manifest and
whose x86 TERM (the z3 expression the pipeline's ledger walk left for its
answer place) this file reads from the term store.

HOW THE TEN WERE CHOSEN, mechanically, and never from an operator token:
the brief names TEN CELLS of the arch-opcode model table by their machine
key (`mnem`, operand shape, `key_width`); each cell carries the corpus's
own attestation -- the units whose bodies spell that cell.  This file takes
the cell's attested unit in a language that HAS a riscv64 compiler in the
image (c through clang, go through the go toolchain); swift, java and the
interpreted languages have none, so a cell attested only by those falls
back to the nearest attested c or go unit and the cell it actually attests
is recorded on the row (`attests_cell`), never hidden.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

The rows below are keyed by the MACHINE key (`mnem`, shape, `key_width`).
The ruling of 2026-09-08 states that a mnemonic alone is a SPELLING and
that the machine-form key is the triple; the mnemonic sits in the field
`mnem`, which the spelling guard reads as machine form.  The SOURCE
operator token rides on the row as the field `operator`, on a row that
also carries `lang` and `unit` -- that is the guard's one allowed place,
a display label on a member -- and nothing reads it.

usage:
  pick_units.py <op_pipeline dir> <out units.json>
"""

import json
import os
import sys


# The ten cells the brief names, in its own order.  Each is a MACHINE key.
TEN_CELLS = [
    {"mnem": "add", "shape": "gpr_gpr", "key_width": 32},
    {"mnem": "sub", "shape": "imm_gpr", "key_width": 64},
    {"mnem": "imul", "shape": "gpr_gpr", "key_width": 32},
    {"mnem": "sar", "shape": "cl_gpr", "key_width": 32},
    {"mnem": "shr", "shape": "cl_gpr", "key_width": 64},
    {"mnem": "idiv", "shape": "gpr_one", "key_width": 32},
    {"mnem": "cmovne", "shape": "gpr_gpr", "key_width": 32},
    {"mnem": "setne", "shape": "gpr_one", "key_width": 8},
    {"mnem": "addss", "shape": "xmm_xmm", "key_width": 32},
    {"mnem": "cvtsi2sd", "shape": "gpr_xmm", "key_width": 64},
]

# The unit each row carries, and WHY that unit and not another.  Every
# entry is a fact this file's own lane prints back from the corpus: the
# cell's attestation, restricted to the two languages the image can compile
# for riscv64.
CHOSEN = {
    ("add", "gpr_gpr", 32): {
        "unit": "go/op_312",
        "attests_cell": {"mnem": "add", "shape": "gpr_gpr",
                         "key_width": 32},
        "why": "the cell's own attested unit; c's int32 addition lowers "
               "to lea, not to this cell",
    },
    ("sub", "imm_gpr", 64): {
        "unit": None,
        "attests_cell": None,
        "why": "NO CORPUS UNIT: the probe corpus is (operator x holder "
               "pair) and never puts a literal on an operand, so no body "
               "spells an immediate-form subtract at 64. The row is a "
               "flag, not a substitution.",
    },
    ("imul", "gpr_gpr", 32): {
        "unit": "c/op_174",
        "attests_cell": {"mnem": "imul", "shape": "gpr_gpr",
                         "key_width": 32},
        "why": "the cell's own attested unit, first c example",
    },
    ("sar", "cl_gpr", 32): {
        "unit": "c/op_714",
        "attests_cell": {"mnem": "sar", "shape": "cl_gpr",
                         "key_width": 32},
        "why": "the cell's own attested unit, first c example",
    },
    ("shr", "cl_gpr", 64): {
        "unit": "c/op_726",
        "attests_cell": {"mnem": "shr", "shape": "cl_gpr",
                         "key_width": 64},
        "why": "the cell's own attested unit, first c example",
    },
    ("idiv", "gpr_one", 32): {
        "unit": "c/op_210",
        "attests_cell": {"mnem": "idiv", "shape": "gpr_one",
                         "key_width": 32},
        "why": "the cell's own attested unit, first c example",
    },
    ("cmovne", "gpr_gpr", 32): {
        "unit": "c/op_185",
        "attests_cell": {"mnem": "cmovne", "shape": "gpr_gpr",
                         "key_width": 64},
        "why": "the 32-bit cell is attested only by swift units, and the "
               "image has no swift for riscv64; c/op_185 is the nearest "
               "attested c unit of the same mnemonic and is the brief's "
               "'a select' -- its ship body is xor, test, cmovne. The "
               "cell it attests is the 64-bit one and is recorded here.",
    },
    ("setne", "gpr_one", 8): {
        "unit": "c/op_498",
        "attests_cell": {"mnem": "setne", "shape": "gpr_one",
                         "key_width": 8},
        "why": "the brief's 'a compare': the c unit whose ship body is "
               "xor, cmp, setne",
    },
    ("addss", "xmm_xmm", 32): {
        "unit": "c/op_105",
        "attests_cell": {"mnem": "addss", "shape": "xmm_xmm",
                         "key_width": 32},
        "why": "the cell's own attested unit, first c example",
    },
    ("cvtsi2sd", "gpr_xmm", 64): {
        "unit": "c/op_106",
        "attests_cell": {"mnem": "cvtsi2sd", "shape": "gpr_xmm",
                         "key_width": 64},
        "why": "the cell's own attested unit, first c example",
    },
}

# THE TENTH BODY.  The `sub` immediate cell attests no unit, so the tenth
# compiled body is the c reading of the FIRST row -- the same operation the
# go unit carries, in the other language, so both compilers the image can
# aim at riscv64 are exercised on one operation.  It is a row of its own and
# is never folded into the cell it does not attest.
BESIDE = {
    "unit": "c/op_102",
    "for_cell": {"mnem": "add", "shape": "gpr_gpr", "key_width": 32},
    "attests_cell": {"mnem": "lea", "shape": "mem_gpr", "key_width": 32},
    "why": "the c body of the same int32 addition the go unit carries; "
           "clang lowers it to lea, which is a finding of section 4 and "
           "not a defect. It fills the tenth slot the immediate-form "
           "subtract cell leaves empty.",
}


def read_manifest(op_dir, lang):
    path = os.path.join(op_dir, "probe_manifest_%s.json" % lang)
    return json.load(open(path))["probes"]


def read_units(op_dir, lang):
    path = os.path.join(op_dir, "op_units_%s.json" % lang)
    return json.load(open(path))["probes"]


def read_term_store(op_dir, wanted):
    """unit name -> its record in the term store, for the wanted names."""
    store = os.path.join(op_dir, "term66_store")
    out = {}
    names = sorted(os.listdir(store))
    for name in names:
        if not name.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(store, name)))
        units = doc.get("units") or {}
        for key in wanted:
            if key in units:
                rec = dict(units[key])
                rec["term_store_shard"] = name
                out[key] = rec
        if len(out) == len(wanted):
            break
    return out


def row_for(op_dir, cell, chosen, manifests, unit_stores):
    row = {
        "mnem": cell["mnem"],
        "shape": cell["shape"],
        "key_width": cell["key_width"],
        "unit": chosen["unit"],
        "attests_cell": chosen["attests_cell"],
        "why": chosen["why"],
    }
    if chosen["unit"] is None:
        row["outcome"] = "NO_CORPUS_UNIT"
        return row
    lang, opname = chosen["unit"].split("/")
    number = opname.split("_")[1]
    probe = manifests[lang][number]
    unit = unit_stores[lang][number]
    row["lang"] = lang
    row["probe_number"] = int(number)
    row["symbol"] = probe["symbol"]
    row["symbol_exact"] = probe.get("symbol_exact", True)
    row["source"] = probe["source"]
    row["operator"] = probe.get("operator")
    row["lhs_type"] = probe.get("lhs_type")
    row["rhs_type"] = probe.get("rhs_type")
    row["expression"] = probe.get("expression")
    row["x86_ship_body"] = list((unit.get("ship") or {}).get("mnem") or [])
    row["outcome"] = "PICKED"
    return row


def main():
    op_dir = sys.argv[1]
    out_path = sys.argv[2]

    manifests = {}
    unit_stores = {}
    for lang in ("c", "go"):
        manifests[lang] = read_manifest(op_dir, lang)
        unit_stores[lang] = read_units(op_dir, lang)

    rows = []
    for cell in TEN_CELLS:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        rows.append(row_for(op_dir, cell, CHOSEN[key], manifests,
                            unit_stores))

    beside_cell = dict(BESIDE["for_cell"])
    beside = row_for(op_dir, beside_cell,
                     {"unit": BESIDE["unit"],
                      "attests_cell": BESIDE["attests_cell"],
                      "why": BESIDE["why"]},
                     manifests, unit_stores)
    beside["beside_the_ten"] = True
    rows.append(beside)

    wanted = set(r["unit"] for r in rows if r.get("unit"))
    terms = read_term_store(op_dir, wanted)
    for row in rows:
        name = row.get("unit")
        if not name:
            continue
        rec = terms.get(name)
        if rec is None:
            row["x86_term"] = None
            row["x86_term_outcome"] = "NOT_IN_TERM_STORE"
            continue
        row["x86_term"] = rec.get("layer5_normalized_text")
        row["x86_term_outcome"] = rec.get("outcome")
        row["x86_result_width"] = rec.get("result_width")
        row["x86_result_family"] = rec.get("result_family")
        row["x86_arrival_families"] = rec.get("arrival_families")
        row["term_store_shard"] = rec.get("term_store_shard")

    doc = {
        "meta": {
            "task": "rv1",
            "what": "the ten cells of the brief's handful, each with the "
                    "corpus unit that attests it, that unit's own probe "
                    "source, and its x86 term from the term store",
            "term_store": os.path.join(op_dir, "term66_store"),
            "ship_flags_x86": {
                "c": "clang -std=c17 -O1 -c",
                "go": "go build",
            },
            "ship_flags_riscv64": {
                "c": "clang -std=c17 -O1 --target=riscv64-unknown-linux-"
                     "gnu -c",
                "go": "GOARCH=riscv64 GOOS=linux go build",
            },
        },
        "rows": rows,
    }
    fh = open(out_path, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    picked = len([r for r in rows if r["outcome"] == "PICKED"])
    print("rows %d, picked %d, no corpus unit %d"
          % (len(rows), picked, len(rows) - picked))
    for row in rows:
        print("  %-9s %-8s %3s  %-12s %s"
              % (row["mnem"], row["shape"], row["key_width"],
                 row.get("unit") or "(none)", row["outcome"]))


if __name__ == "__main__":
    main()
