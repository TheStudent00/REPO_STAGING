#!/usr/bin/env python3
"""guard48b.py -- THE GUARDS for task 48, SECOND VERSION: NO EXEMPTION
OF ANY KIND, at file level or at field level.

WHAT CHANGED FROM guard48.py, and why the first version's claim was
wrong.  guard48.py stripped the file-level provenance role from a
scratch copy (good) and then ADDED `producer` and `blocked_by` to the
generic checker's own prose-field set at run time (not good).  That
second step is a field-level exemption invented by the very stage
being checked, and it made the guard pass a shape the guard should
reject: a bare operator-token spelling sitting in a row field.  Run
plainly, `check_no_spelling_keys.py name_census2.json` FAILED on four
places.  This version adds nothing to any field set.  The artifacts
were changed instead: every producer is a typed machine-form object
whose mnemonic sits under the ratified `mnem` field, and no artifact
declares the provenance role.

Two checks, on every artifact this lap wrote:

  CHECK ONE -- every census entry's `producer` is an arch opcode, or a
  PAIR of arch opcodes, that the blocked unit's own body actually
  spells.  This is the same check canon37_guard.py runs over the
  ledger, carried into the census: the census is KEYED ON PRODUCER
  OPCODES, and some arch opcodes are spelled exactly like operator
  tokens, so the distinction has to be proved per row rather than
  asserted.

  CHECK TWO -- the generic spelling-key guard
  (check_no_spelling_keys.py), with the generator-provenance exemption
  DELETED from a scratch copy of each file, so every artifact is walked
  in full.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.
"""

import glob
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_no_spelling_keys as CHECK                            # noqa: E402

NON_OPCODE_PRODUCERS = set([
    "arrival",
    "the body's own immediate operand",
    "the body's own stack displacement",
])


def artifacts():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(HERE, "layer4b_terms_%s.json" % lang))
    out.append(os.path.join(HERE, "layer4b_interp.json"))
    out.append(os.path.join(HERE, "name_census3.json"))
    out.append(os.path.join(HERE, "layer4b_state.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "layer4b_regen_store",
                                             "*.json"))))
    return [one for one in out if os.path.exists(one)]


def without_exemption(path, scratch):
    document = json.load(open(path))
    if isinstance(document, dict):
        meta = document.get("meta")
        if isinstance(meta, dict) and "role" in meta:
            del meta["role"]
        if "role" in document:
            del document["role"]
    target = os.path.join(scratch, os.path.basename(path))
    handle = open(target, "w")
    json.dump(document, handle)
    handle.close()
    return target


def bodies():
    """unit name -> the set of mnemonics that unit's own body spells,
    read out of task 47's own artifacts."""
    out = {}
    paths = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        paths.append(os.path.join(HERE, "canon37_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon37_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(HERE,
                                               "canon37_regen_store",
                                               "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for label, record in document.get("units", {}).items():
            found = set()
            for raw in record.get("body_verbatim") or []:
                line = raw
                if "!!" in line:
                    line = line.split("!!", 1)[0].strip()
                found.add(line.split(" ", 1)[0])
            out[label] = found
    return out


def members_of(producer):
    """the mnemonics a typed producer object names, as a list."""
    if not isinstance(producer, dict):
        return [str(producer)]
    if producer.get("kind") == "flag_pair":
        return list(producer.get("mnem") or [])
    if producer.get("kind") == "arch_opcode":
        return [producer.get("mnem")]
    return []


def check_record_producers(spelled):
    """the same CHECK ONE, carried over the per-unit layer-4 records:
    every `producer` field on a hole or a cascade must be an arch
    opcode -- or a pair of them -- that THAT unit's own body spells.
    Only when this passes may the generic checker read the field as
    machine form."""
    checked = 0
    findings = []
    for path in artifacts():
        if os.path.basename(path) in ("name_census3.json",
                                      "layer4b_state.json"):
            continue
        document = json.load(open(path))
        for label, record in document.get("units", {}).items():
            known = spelled.get(label, set())
            for group in ("holes", "cascades"):
                for entry in record.get(group, []):
                    checked += 1
                    producer = entry.get("producer") or {}
                    members = members_of(producer)
                    for member in members:
                        if member in NON_OPCODE_PRODUCERS:
                            continue
                        if member.startswith("the body's last write "
                                             "to"):
                            continue
                        if member == "None":
                            continue
                        if member in known:
                            continue
                        findings.append({
                            "unit": label, "producer": producer,
                            "why": "the producer member %r is not a "
                                   "mnemonic of this unit's own body"
                                   % member,
                        })
    return checked, findings


def check_census_producers(census, spelled):
    checked = 0
    findings = []
    for entry in census["entries"]:
        producer = entry["producer"]
        members = members_of(producer)
        for unit in entry["units_blocked"]:
            checked += 1
            known = spelled.get(unit)
            if known is None:
                findings.append({"unit": unit, "producer": producer,
                                 "why": "no body is recorded for this "
                                        "unit"})
                continue
            for member in members:
                if member in NON_OPCODE_PRODUCERS:
                    continue
                if member.startswith("the body's last write to"):
                    continue
                if member in known:
                    continue
                findings.append({
                    "unit": unit, "producer": producer,
                    "why": "the producer member %r is not a mnemonic "
                           "of this unit's own body" % member,
                })
    return checked, findings


def main():
    tokens = CHECK.inventory()
    print("operator inventory: %d tokens read from "
          "probe_manifest_*.json" % len(tokens))
    print("THE GENERATOR-PROVENANCE EXEMPTION IS REMOVED for every "
          "file below.")
    print("")
    census_path = os.path.join(HERE, "name_census3.json")
    if os.path.exists(census_path):
        census = json.load(open(census_path))
        spelled = bodies()
        checked, findings = check_census_producers(census, spelled)
        print("CHECK ONE -- every census producer is an arch opcode "
              "(or a pair of them) that the blocked unit's own body "
              "spells")
        print("  unit/producer places checked: %d" % checked)
        print("  findings:                     %d" % len(findings))
        for item in findings[:20]:
            print("    %s" % item)
        if not findings:
            print("  PASS -- every census key is a machine mnemonic of "
                  "the blocked unit's own body, so an operator-token "
                  "SPELLING in that field is a collision with a machine "
                  "mnemonic, not a spelling key.")
    print("")
    checked, findings = check_record_producers(spelled)
    print("CHECK ONE-B -- the same test on every `producer` field of "
          "every per-unit layer-4 record")
    print("  producer fields checked: %d" % checked)
    print("  findings:                %d" % len(findings))
    for item in findings[:20]:
        print("    %s" % item)
    if findings:
        sys.exit(1)
    print("  PASS -- every producer field is a machine mnemonic of "
          "that unit's own body.")
    print("")
    print("CHECK TWO -- the generic spelling-key guard, exemption "
          "removed -- and NOTHING added to any field set")
    # NOTHING is added to any of the checker's field sets.  The
    # artifacts carry machine form structurally; the checker is
    # untouched.
    scratch = tempfile.mkdtemp(prefix="guard48_")
    checked = 0
    failed = []
    for path in artifacts():
        target = without_exemption(path, scratch)
        worst = CHECK.check(target, tokens)
        checked += 1
        if worst:
            failed.append(path)
    print("  checked %d files without exemption; %d failed"
          % (checked, len(failed)))
    for path in failed:
        print("    FAIL %s" % path)
    if failed:
        sys.exit(1)
    print("  PASS")


if __name__ == "__main__":
    main()
