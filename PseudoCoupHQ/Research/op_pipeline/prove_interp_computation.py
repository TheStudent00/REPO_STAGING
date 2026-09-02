#!/usr/bin/env python3
"""prove_interp_computation.py -- TASK 27, part 3: the COMPUTATION-PART
proofs, against the compiled classes, through the cross-unit prover.

WHAT IS PROVED.  `lineage_carve.json` carves each interpreter handler
into ARRIVAL (the maximal prefix of each lineage that touches one
lineage only) and COMPUTATION (from the first confluence to the
answer).  This program takes the COMPUTATION CORE of each carved unit,
renders it in the canonical runnable form (traced values in their
designated registers: a in %rdi, b in %rsi, the answer in %rax, with
the entry contract's adapter move on its own line), and asks
`cross_unit_prover.prove_pair` -- imported unmodified -- whether it is
equal, for every value of every register either text reads before
writing, to each compiled unit in the comparable class.

HOW THE CANDIDATE SET IS CHOSEN -- machine-form only.  A candidate is a
compiled 0-branch unit whose CLASS KEY (type pair, machine-fact result
family; both computed by the functions cross_unit_prover already uses)
carries two 64-bit integer operands and a 64-bit integer result.  The
interpreter side qualifies for that key from its own DWARF typed key,
read out of the same binary the slice came from: ruby's handlers
declare `VALUE, VALUE`, and `VALUE` resolves through DWARF to
`long unsigned int`, DW_ATE_unsigned, 8 bytes (measured, not assumed).
No operator token takes part in the candidate choice at any step.

WHERE IT REFUSES, and does not force a proof:
  * a unit whose typed key was REFUSED at the DWARF read (php's three
    specialized handlers: zero formal parameters, so no declared
    operand type exists to compare with a compiled class key);
  * a unit whose typed key is a POINTER pair (php's generic routine,
    `zval*,zval*`): a pointer pair is not comparable with a compiled
    integer class key, and forcing it would be inventing a type;
  * a computation core this program cannot render in the canonical
    form by a rename alone -- chiefly a core that reads an operand out
    of MEMORY (php's handlers read the VM stack slot directly), where
    a "rename" into a designated register would be re-plumbing, not
    canonicalization.

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
  /tmp/reconnect_venv/bin/python3 prove_interp_computation.py
"""

import json
import os
import re
import sys

import canon
import cross_unit_prover as CUP

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prove_interp_computation.json")

DESIGNATED = {
    "argument_lineage_1": "%rdi",
    "argument_lineage_2": "%rsi",
}

INTEGER_64_KEYS = [("u64,u64", "u64"), ("i64,i64", "i64")]


def typed_key_for(lang, symbol, build):
    doc = json.load(open(os.path.join(HERE, "dwarf_typed_key_t27.json")))
    for rec in doc["records"]:
        if rec["lang"] != lang:
            continue
        if rec["handler"] != symbol:
            continue
        binary = rec["dwarf_source_binary"]
        if build == "anchor" and "anchor" not in binary:
            continue
        if build == "ship" and "ship" not in binary:
            continue
        return rec
    return None


def canonical_core_text(record):
    """-> (text, note) or (None, refusal).

    The rename is only attempted for the shape this task's carves
    actually produced: ONE core instruction, both operands registers,
    the destination the second operand.  Anything else is refused by
    name rather than approximated."""
    core = record["computation_core"]["instructions"]
    if len(core) != 1:
        return None, ("the computation core is %d instructions; this "
                      "program renders a single-instruction core only"
                      % len(core))
    line = core[0]["mnem"]
    mnem, operands = canon.parse(line)
    if len(operands) != 2:
        return None, "the core instruction does not have two operands"
    src, dst = operands[0].strip(), operands[1].strip()
    if "(" in src or "(" in dst:
        return None, ("the core reads or writes MEMORY (%r): placing that "
                      "value in a designated register would be re-plumbing "
                      "the unit, not renaming it, so no canonical text is "
                      "produced and no proof is attempted" % line)
    place_lineages = record["boundary"]["place_lineages"]
    src_reg = src.lstrip("%")
    dst_reg = dst.lstrip("%")
    src_lin = place_lineages.get(_fold(src_reg), [])
    dst_lin = place_lineages.get(_fold(dst_reg), [])
    if len(src_lin) != 1 or len(dst_lin) != 1:
        return None, ("an operand of the core carries %r / %r lineages; a "
                      "designated-register rename needs exactly one traced "
                      "value per operand" % (src_lin, dst_lin))
    src_des = DESIGNATED[src_lin[0]]
    dst_des = DESIGNATED[dst_lin[0]]
    text = "mov %s,%%rax; %s %s,%%rax; ret" % (dst_des, mnem, src_des)
    note = ("traced values renamed to the designated registers (%s -> %s, "
            "%s -> %s), the answer to %%rax, with the entry contract's "
            "adapter move on its own line"
            % (src, src_des, dst, dst_des))
    return text, note


def _fold(name):
    import lineage_carve
    return lineage_carve.fold(name)


def refuse_own_output_on_spelling_keys(path):
    """THE MECHANICAL GUARD.  Every pipeline stage that groups or pairs
    units must run the spelling-key check and REFUSE ITS OWN OUTPUT on
    failure.  This function is that refusal: it runs
    check_no_spelling_keys.py over the file just written and returns a
    nonzero exit code if the guard fails."""
    import subprocess
    proc = subprocess.run(
        [sys.executable,
         os.path.join(HERE, "check_no_spelling_keys.py"), path],
        capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % path)
    return proc.returncode


def main():
    carves = json.load(open(os.path.join(HERE, "lineage_carve.json")))
    text_of, meta_of, class_of = CUP.build_population()
    candidates = []
    for lab, key in class_of.items():
        if key in INTEGER_64_KEYS:
            candidates.append(lab)
    candidates.sort()

    records = []
    for rec in carves["records"]:
        if rec["outcome"] != "CARVED":
            continue
        here = {
            "unit": rec["unit"],
            "build": rec["build"],
            "language": rec["language"],
            "symbol": rec["symbol"],
            "boundary": rec["boundary"]["instruction"],
            "boundary_address": rec["boundary"]["address"],
            "computation_core": [x["mnem"]
                                 for x in rec["computation_core"]["instructions"]],
            "provenance_is_weaker": True,
        }
        key = typed_key_for(rec["language"], rec["symbol"], rec["build"])
        here["dwarf_typed_key"] = key.get("typed_key") if key else None
        here["dwarf_read_outcome"] = key.get("outcome") if key else "NO RECORD"
        if key is None or key.get("outcome") != "READ":
            here["verdict"] = "TYPE_INCOMPARABLE"
            here["why"] = (
                "no typed key could be read for this unit at this build, so "
                "there is no measured operand type to match against a "
                "compiled class key.  The DWARF refusal, verbatim: %s"
                % (key.get("refusal") if key else "no record at all"))
            records.append(here)
            continue
        sizes = [p.get("byte_size") for p in key.get("formal_parameters", [])]
        here["dwarf_byte_sizes"] = sizes[:2]
        if "*" in (key.get("typed_key") or ""):
            here["verdict"] = "TYPE_INCOMPARABLE"
            here["why"] = (
                "the declared operand type is a POINTER pair (%s).  The "
                "compiled classes in the comparable set carry integer "
                "operands; matching a pointer pair to them would be "
                "inventing a type, so no proof is attempted."
                % key["typed_key"])
            records.append(here)
            continue
        text, note = canonical_core_text(rec)
        if text is None:
            here["verdict"] = "NOT_RENDERABLE_IN_CANONICAL_FORM"
            here["why"] = note
            records.append(here)
            continue
        here["canonical_text"] = text
        here["canonicalization_note"] = note
        proved = []
        disproved = 0
        undecided = 0
        refused = 0
        lab_self = "%s::%s" % (rec["unit"], rec["build"])
        text_of[lab_self] = text
        class_of[lab_self] = INTEGER_64_KEYS[0]
        for other in candidates:
            verdict, detail = CUP.prove_pair(lab_self, other, text_of, class_of)
            if verdict == "PROVED":
                proved.append({
                    "compiled_unit": other,
                    "compiled_text": text_of[other],
                    "detail": detail,
                    # NO display label is carried here.  The guard
                    # (check_no_spelling_keys.py) refused this file's
                    # first output because a token on a proof ROW is a
                    # row structure, not a per-unit label -- and it was
                    # right.  The compiled unit's id names the member;
                    # its label lives on that unit's own record, in the
                    # artifact that owns it.
                    "label_deliberately_absent": "see this file's note on the guard refusal",
                })
            elif verdict == "DISPROVED":
                disproved += 1
            elif verdict == "UNDECIDED":
                undecided += 1
            else:
                refused += 1
        here["candidates_considered"] = len(candidates)
        here["proved_equal_to"] = proved
        here["counts"] = {
            "proved": len(proved),
            "disproved": disproved,
            "undecided": undecided,
            "refused": refused,
        }
        if proved:
            here["verdict"] = "PROVED"
        elif undecided or refused:
            here["verdict"] = "UNDECIDED"
        else:
            here["verdict"] = "NO_MATCH_IN_THE_COMPARABLE_CLASS"
        records.append(here)

    out = {
        "meta": {
            "generator": "prove_interp_computation.py",
            "task": "TASK 27 -- computation-part proofs for the ruby and php carves",
            "prover": "cross_unit_prover.prove_pair, imported unmodified (z3 over the canon8/canon20 simulators)",
            "candidate_rule": "every compiled 0-branch unit whose class key (type pair, machine-fact result family) is a 64-bit integer pair with a 64-bit integer result: %s.  No token participates." % (INTEGER_64_KEYS,),
            "candidates_in_that_class": len(candidates),
            "typed_keys": "dwarf_typed_key_t27.json -- read from the same binary each slice came from",
            "value_type_resolution": "ruby's VALUE resolves through DWARF to base type 'long unsigned int', DW_ATE_unsigned (encoding 7), byte size 8 -- measured in both ruby binaries this session, not assumed",
            "provenance_is_weaker": True,
        },
        "records": records,
        "summary": {
            "carved_units_considered": len(records),
            "proved": len([r for r in records if r["verdict"] == "PROVED"]),
            "type_incomparable": len([r for r in records
                                      if r["verdict"] == "TYPE_INCOMPARABLE"]),
            "not_renderable": len([r for r in records
                                   if r["verdict"] == "NOT_RENDERABLE_IN_CANONICAL_FORM"]),
            "undecided": len([r for r in records if r["verdict"] == "UNDECIDED"]),
            "no_match": len([r for r in records
                             if r["verdict"] == "NO_MATCH_IN_THE_COMPARABLE_CLASS"]),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    guard_code = refuse_own_output_on_spelling_keys(OUT)
    for r in records:
        line = "%-6s %-56s %-34s" % (r["build"], r["symbol"], r["verdict"])
        if r["verdict"] == "PROVED":
            line += " proved against %d of %d candidates" % (
                r["counts"]["proved"], r["candidates_considered"])
        print(line)
    print("summary: %s" % out["summary"])
    return guard_code


if __name__ == "__main__":
    sys.exit(main())
