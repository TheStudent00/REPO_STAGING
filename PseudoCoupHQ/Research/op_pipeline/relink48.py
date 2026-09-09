#!/usr/bin/env python3
"""relink48.py -- TASK 48 step 0: attach each ledger row to the BODY LINE
that produced it, and CHECK the attachment against the stored ledger.

WHY THIS FILE EXISTS.  Task 47's provenance ledger (ledger47.py) records,
per row, the ARCH OPCODE that made the value and the ROWS it read.  It
does not record the operand WIDTH, and width is not a property of the
row (a row is 8 or 16 bytes; `add %esi,%eax` is a 32-bit operation
inside an 8-byte row).  Layer 4 transcribes the ledger into a z3 term,
and a term needs its width.

THE METHOD, and why it is a transcription and not a second pipeline.
This file does not re-derive the dataflow.  It RE-RUNS ledger47's own
`wrap_unit` with two seams instrumented -- `mnemonic_of`, which
ledger47 calls once per body line, records which line is being walked;
`LedgerTable.add`, which ledger47 calls once per row, stamps that line
onto the row it is creating.  The result is then CHECKED row for row
against the ledger already stored in task 47's artifact: same row
names, same producers, same operands, in the same order.  A unit whose
re-run disagrees is REFUSED BY NAME and reported; nothing is guessed.

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

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger47 as L47                                           # noqa: E402
import region36 as R36                                           # noqa: E402


class RelinkDisagreement(Exception):
    """the re-run's ledger is not the stored ledger; refused by name."""


_STATE = {"line": None}

_ORIGINAL_MNEMONIC_OF = L47.mnemonic_of
_ORIGINAL_ADD = L47.LedgerTable.add


def _mnemonic_of(line):
    _STATE["line"] = line
    return _ORIGINAL_MNEMONIC_OF(line)


def _add(self, block, size, type_name, produced_by, operands,
         note=None, resident=None):
    record = _ORIGINAL_ADD(self, block, size, type_name, produced_by,
                           operands, note=note, resident=resident)
    record["_line"] = _STATE["line"]
    return record


L47.mnemonic_of = _mnemonic_of
L47.LedgerTable.add = _add


def _key(row):
    """the three fields the check compares: name, producer, operands."""
    producer = row["produced_by"]
    if isinstance(producer, list):
        producer = tuple(producer)
    return (row["row"], producer, tuple(row["operands"]))


def relink(unit):
    """unit: one record out of a canon37 artifact.

    Returns a list, one entry per stored ledger row, in the stored
    order, each entry a dict with the row itself plus:
        line       the body line that produced it, or None
        line_index its index in `body_verbatim`, or None
    Raises RelinkDisagreement if the re-run does not reproduce the
    stored ledger exactly."""
    body_text = "; ".join(unit["body_verbatim"])
    _STATE["line"] = None
    fields = L47.wrap_unit(body_text,
                           list(unit["arrival_families"]),
                           unit["result_family"],
                           unit["result_width"])
    fresh = fields["ledger"]
    stored = unit["ledger"]
    if len(fresh) != len(stored):
        raise RelinkDisagreement(
            "the re-run made %d rows, the stored ledger has %d"
            % (len(fresh), len(stored)))
    for index, (a, b) in enumerate(zip(fresh, stored)):
        if _key(a) != _key(b):
            raise RelinkDisagreement(
                "row %d differs: re-run %r, stored %r"
                % (index, _key(a), _key(b)))
    lines = [R36.strip_annotation(one) for one in unit["body_verbatim"]]
    out = []
    for a, b in zip(fresh, stored):
        line = a.get("_line")
        line_index = None
        if line is not None and line in lines:
            line_index = lines.index(line)
        entry = dict(b)
        entry["line"] = line
        entry["line_index"] = line_index
        out.append(entry)
    return out


def self_check():
    import json
    total = 0
    bad = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "canon37_wrapped_%s.json" % lang)
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" not in unit:
                continue
            total += 1
            try:
                relink(unit)
            except Exception as problem:
                bad.append((name, str(problem)))
    print("relink self-check over the original population")
    print("  units walked: %d" % total)
    print("  disagreements: %d" % len(bad))
    for name, why in bad[:20]:
        print("    %s -- %s" % (name, why))


if __name__ == "__main__":
    self_check()
