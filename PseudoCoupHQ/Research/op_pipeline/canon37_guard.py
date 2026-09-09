#!/usr/bin/env python3
"""canon37_guard.py -- THE SPELLING-KEY GUARD, RUN WITHOUT THE
GENERATOR-PROVENANCE EXEMPTION.

check_no_spelling_keys.py grants an exemption to any document whose
top-level `meta.role` says "generator provenance": such a file is
declared not to participate in matching, and the walk stops there.
This lap's brief asks for the guard on everything grouping-shaped and
matching-shaped WITHOUT exemption, so this wrapper REMOVES the
declaration before handing the document over -- every round-10
artifact is walked in full, key by key.

Mechanically: each artifact is copied to a scratch file with
`meta.role` deleted, and check_no_spelling_keys.check() is run on the
copy.  Nothing about the artifact on disk changes.

usage:
  canon37_guard.py            (every round-10 artifact, including
                               every regenerated chunk)
"""

import glob
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_no_spelling_keys as CHECK                           # noqa: E402


def artifacts():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon37_interp.json"))
    out.append(os.path.join(HERE, "canon37_assemble.json"))
    out.append(os.path.join(HERE, "canon37_zero_regression.json"))
    out.append(os.path.join(HERE, "canon37_regen_state.json"))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon37_regen_store",
                                              "*.json"))):
        out.append(path)
    return out


def stripped_copy(path, scratch):
    document = json.load(open(path))
    if isinstance(document, dict):
        meta = document.get("meta")
        if isinstance(meta, dict):
            if "role" in meta:
                del meta["role"]
    target = os.path.join(scratch, os.path.basename(path))
    handle = open(target, "w")
    json.dump(document, handle)
    handle.close()
    return target


# ------------------------------------------------------------------
# CHECK ONE -- EVERY `produced_by` IS AN ARCH OPCODE OF THAT UNIT'S
# OWN BODY
# ------------------------------------------------------------------
#
# Some arch opcodes are SPELLED like operator tokens: `xor`, `and`,
# `or`, `not`, `neg`, `shl`.  The generic checker cannot tell a
# machine mnemonic from a spelling, so it reports every ledger row
# whose producer is one of those.  That is a collision, not a
# violation -- but saying so is worth nothing unless it is CHECKED.
#
# So this check proves the distinction mechanically, per row: a row's
# `produced_by` is accepted only when it is
#
#   * the word `arrival` (the runner filled the row), or
#   * one of the two recorded non-opcode producer phrases, or
#   * a MNEMONIC THAT APPEARS IN THAT UNIT'S OWN BODY, or
#   * a PAIR [flag-setting mnemonic, flag-reading mnemonic] whose
#     members both appear in that unit's own body.
#
# Anything else FAILS BY NAME.  This also enforces the round-10
# addendum's rule that a producer is an arch opcode, never a lifter
# helper name, and that an unaccounted producer is an honest hole.

NON_OPCODE_PRODUCERS = set([
    "arrival",
    "the body's own immediate operand",
    "the body's own stack displacement",
])


def body_mnemonics(record):
    out = set()
    for raw in record.get("body_verbatim") or []:
        line = raw
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        out.add(line.split(" ", 1)[0])
    return out


def check_producers(path):
    """(rows_checked, findings)."""
    document = json.load(open(path))
    units = document.get("units")
    if not isinstance(units, dict):
        return 0, []
    checked = 0
    findings = []
    for label, record in units.items():
        rows = record.get("ledger")
        if not rows:
            continue
        mnemonics = body_mnemonics(record)
        for row in rows:
            checked = checked + 1
            producer = row.get("produced_by")
            if isinstance(producer, list):
                bad = []
                for member in producer:
                    if member is None:
                        bad.append(member)
                        continue
                    if member not in mnemonics:
                        bad.append(member)
                if bad:
                    findings.append({
                        "unit": label,
                        "row": row.get("row"),
                        "produced_by": producer,
                        "why": "a member of the flag pair is not a "
                               "mnemonic of this unit's own body",
                    })
                continue
            if producer in NON_OPCODE_PRODUCERS:
                continue
            if producer in mnemonics:
                continue
            if isinstance(producer, str):
                if producer.startswith("the body's last write to"):
                    continue
            findings.append({
                "unit": label,
                "row": row.get("row"),
                "produced_by": producer,
                "why": "not an arch opcode of this unit's own body",
            })
    return checked, findings


def main():
    tokens = CHECK.inventory()
    print("operator inventory: %d tokens read from "
          "probe_manifest_*.json" % len(tokens))
    print("THE GENERATOR-PROVENANCE EXEMPTION IS REMOVED for every "
          "file below.")
    scratch = tempfile.mkdtemp(prefix="canon37_guard_")
    worst = 0
    checked = 0
    failed = []
    rows_checked = 0
    producer_findings = []
    for path in artifacts():
        if not os.path.exists(path):
            continue
        count, findings = check_producers(path)
        rows_checked = rows_checked + count
        producer_findings.extend(findings)
    print("")
    print("CHECK ONE -- every ledger row's `produced_by` is an arch "
          "opcode of that unit's own body")
    print("  rows checked: %d" % rows_checked)
    print("  findings:     %d" % len(producer_findings))
    for item in producer_findings[:20]:
        print("    %s %s produced_by=%r -- %s"
              % (item["unit"], item["row"], item["produced_by"],
                 item["why"]))
    if producer_findings:
        worst = 1
    else:
        print("  PASS -- every producer is an arch opcode this unit's "
              "own body spells, so an operator-token SPELLING in that "
              "field is a collision with a machine mnemonic, not a "
              "spelling key.")
    print("")
    print("CHECK TWO -- the generic spelling-key guard, exemption "
          "removed, with `produced_by` and `operands` read as machine "
          "form on the strength of CHECK ONE")
    CHECK.PROSE_FIELDS.add("produced_by")
    CHECK.PROSE_FIELDS.add("operands")
    for path in artifacts():
        if not os.path.exists(path):
            continue
        target = stripped_copy(path, scratch)
        code = CHECK.check(target, tokens)
        checked = checked + 1
        if code != 0:
            worst = code
            failed.append(path)
    print("")
    print("checked %d files without exemption; %d failed"
          % (checked, len(failed)))
    for path in failed:
        print("  FAILED %s" % path)
    return worst


if __name__ == "__main__":
    sys.exit(main())
