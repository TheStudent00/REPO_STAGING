#!/usr/bin/env python3
"""t104_fix_spelling_keys.py -- the two spelling-ban violations lane
11's guard step found in this task's OWN artifacts, corrected in
place, never worked around.

FINDING 1.  `kind_census()` in `t104_walk.py` (used for the
`declaration_kind_census` field in `t104_audit.json`,
`t104_audit_unchanged_rule.json`, `t104_walk_evidence.json` and
`t104_walk_evidence_unchanged_rule.json`) keyed its dict
`"%s|%d" % (declaration.name(), declaration.kind())` -- an operator
token joined to a number, a dict-key violation by the guard's own
rule 1.  The name was always redundant with the kind: z3's numeric
declaration kind determines the name 1:1, so re-keying by the number
alone loses nothing machine-readable and drops the spelling.  This
program re-keys the four files' existing counts (`"and|261"` ->
`"261"`, summed if two spellings ever mapped to the same number,
which does not happen here) rather than re-running the walk: the
counts themselves are untouched, only the key text is.  `term.py`
carries the current name for a kind at the report layer, where a
display label is allowed.

FINDING 2.  `t104_diagnose.py`'s `commutative_report()` put
`operator_name` (a bare token, e.g. `"="`) on each
`commutative_nodes_after_order` / `commutative_nodes_after_simplify`
row -- a plain string field on a dict that is not a unit object (it
carries no `lang`/`id` of its own; those live one level up, on the
`"cpp/op_473"` key). The row already carries `kind_number`, the same
machine form with no name attached, so `operator_name` was decoration
duplicating it. This program drops the field from the six units'
already-written rows in `t104_diagnose.json` (the walk that produced
it changes nothing else).

BOTH FIXES ALSO GO INTO THE SOURCE, so a re-run does not reintroduce
either: `kind_census()` in `t104_walk.py` keys by kind number alone;
`commutative_report()` in `t104_diagnose.py` stops writing
`operator_name` into the row (its print loop names the operator by
calling `T.operator_name(current)` directly, at print time, which is
a display label on stdout and not a stored key).

WRITES: t104_audit.json, t104_audit_unchanged_rule.json,
        t104_walk_evidence.json, t104_walk_evidence_unchanged_rule.json,
        t104_diagnose.json (re-keyed / stripped, counts unchanged)
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)

CENSUS_FILES = [
    "t104_audit.json",
    "t104_audit_unchanged_rule.json",
    "t104_walk_evidence.json",
    "t104_walk_evidence_unchanged_rule.json",
]

DIAGNOSE_FILE = "t104_diagnose.json"
DIAGNOSE_LIST_FIELDS = [
    "commutative_nodes_after_order",
    "commutative_nodes_after_simplify",
]


def load(name):
    return json.load(open(os.path.join(PIPELINE, name)))


def save(name, document):
    path = os.path.join(PIPELINE, name)
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()


def rekey_census(census):
    """`{"and|261": 5000, ...}` -> `{"261": 5000, ...}`, summed on a
    numeric collision (none observed)."""
    out = {}
    for key, count in census.items():
        if "|" not in key:
            out[key] = out.get(key, 0) + count
            continue
        _name, _sep, number = key.rpartition("|")
        out[number] = out.get(number, 0) + count
    return out


def fix_census_file(name):
    document = load(name)
    if "declaration_kind_census" not in document:
        sys.stdout.write("   %s -- no declaration_kind_census field, "
                         "left alone\n" % name)
        return False
    before = document["declaration_kind_census"]
    after = rekey_census(before)
    before_total = sum(before.values())
    after_total = sum(after.values())
    if before_total != after_total:
        raise SystemExit(
            "ABORT: %s -- re-keying changed the total count (%d -> %d)"
            % (name, before_total, after_total))
    document["declaration_kind_census"] = after
    save(name, document)
    sys.stdout.write("   %s -- %d keys re-keyed to numeric kind alone, "
                     "total count %d unchanged\n"
                     % (name, len(before), before_total))
    return True


def strip_operator_name(rows):
    changed = 0
    for row in rows:
        if "operator_name" in row:
            del row["operator_name"]
            changed = changed + 1
    return changed


def fix_diagnose_file():
    document = load(DIAGNOSE_FILE)
    changed = 0
    for unit_name in sorted(document):
        record = document[unit_name]
        if not isinstance(record, dict):
            continue
        for field in DIAGNOSE_LIST_FIELDS:
            rows = record.get(field)
            if rows is None:
                continue
            changed = changed + strip_operator_name(rows)
    save(DIAGNOSE_FILE, document)
    sys.stdout.write("   %s -- operator_name dropped from %d row(s), "
                     "kind_number left in place\n"
                     % (DIAGNOSE_FILE, changed))


def main():
    sys.stdout.write("[1/2] re-key declaration_kind_census by numeric "
                     "kind alone\n")
    for name in CENSUS_FILES:
        fix_census_file(name)
    sys.stdout.write("[2/2] drop operator_name from t104_diagnose.json's "
                     "commutative-node rows\n")
    fix_diagnose_file()
    return 0


if __name__ == "__main__":
    sys.exit(main())
