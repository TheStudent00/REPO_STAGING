#!/usr/bin/env python3
"""canon38_gate.py -- THE GATE for the repaired form (ledger48).

canon37_gate.py is NOT edited.  It is imported, and two things are
added on top of it:

 1. THE ROW TEST IS WIDENED TO EIGHT BLOCKS.  canon37_gate patched
    `canon33_gate.is_slot_text` to recognise ledger47's six block
    names.  ledger48 has eight, so the patch is re-applied with
    ledger48's own test.  STACK and X87 rows never appear in a wrapped
    text (rows are information, not stores), so this changes no proof;
    it is done so the test cannot lie about what a row name is.

 2. THE STRUCTURAL ROUTE GAINS ONE CHECK, C6, BECAUSE THE BODY IS NO
    LONGER CHARACTER-FOR-CHARACTER.  Ruling 4 rewrites transfer
    targets, so canon37_gate's structural claim ("the body is present
    character-for-character") is no longer true as written and must
    not be reused as if it were.  C6 states exactly what changed and
    checks it:

      * every line of the body as it was read is either unchanged in
        the stored body, or is a TRANSFER whose target operand was
        rewritten, and nothing else on that line moved (the mnemonic
        is the same, the trailing annotation is the same);
      * the rewrite is a FUNCTION of the target, not of the line: two
        transfers to the same target get the same label;
      * every label the stored body uses inside the unit is defined
        exactly once in the stored body;
      * the only lines added are label definitions.

    A unit whose C6 fails is not claimed by the structural route.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon33_gate as G33                                       # noqa: E402
import canon37_gate as G37                                       # noqa: E402
import ledger48 as L48                                           # noqa: E402

_BEFORE_LEDGER48 = G33.is_slot_text


def is_slot_text(text):
    if _BEFORE_LEDGER48(text):
        return True
    return L48.is_row_text(text)


G33.is_slot_text = is_slot_text

# everything else the drivers need, taken from canon37_gate unchanged
Sim47 = G37.Sim47
bind_arrival = G37.bind_arrival
compare = G37.compare
answer_home_of = G37.answer_home_of
arrival_family_list = G37.arrival_family_list
arrival_contract = G37.arrival_contract
contract_disagreement = G37.contract_disagreement
sequences_for = G37.sequences_for
DESIGNATIONS = G37.DESIGNATIONS


def label_definitions(lines):
    out = []
    for line in lines:
        if line.endswith(":"):
            out.append(line[:-1])
    return out


def check_six(fields):
    """C6 -- the branch-label rewrite, stated and checked."""
    was = fields.get("body_as_read")
    now = fields.get("body_verbatim")
    record = fields.get("branch_labels") or {}
    if was is None:
        return False, "C6 fails: the record carries no body as read"
    defined = label_definitions(now)
    if len(defined) != len(set(defined)):
        return False, ("C6 fails: a label is defined more than once: %r"
                       % defined)
    stored_without_labels = []
    for line in now:
        if line.endswith(":"):
            continue
        stored_without_labels.append(line)
    if len(stored_without_labels) != len(was):
        return False, ("C6 fails: the stored body has %d instructions "
                       "and the body as read has %d"
                       % (len(stored_without_labels), len(was)))
    rewritten_at = {}
    for entry in record.get("rewrites") or []:
        rewritten_at[entry["line_index"]] = entry
    by_target = {}
    for index, old in enumerate(was):
        new = stored_without_labels[index]
        if new == old:
            if index in rewritten_at:
                return False, ("C6 fails: line %d is recorded as "
                               "rewritten and is unchanged" % index)
            continue
        if index not in rewritten_at:
            return False, ("C6 fails: line %d changed and no rewrite "
                           "is recorded for it: %r -> %r"
                           % (index, old, new))
        old_text, old_annotation = L48.split_off_annotation(old)
        new_text, new_annotation = L48.split_off_annotation(new)
        if old_annotation != new_annotation:
            return False, ("C6 fails: line %d's trailing annotation "
                           "changed" % index)
        old_parts = old_text.split(" ", 1)
        new_parts = new_text.split(" ", 1)
        if old_parts[0] != new_parts[0]:
            return False, ("C6 fails: line %d's mnemonic changed, %r "
                           "to %r" % (index, old_parts[0],
                                      new_parts[0]))
        if not L48.is_transfer(old_parts[0]):
            return False, ("C6 fails: line %d changed and is not a "
                           "transfer: %r" % (index, old))
        target_was = old_parts[1].strip()
        target_now = new_parts[1].strip()
        if target_was in by_target:
            if by_target[target_was] != target_now:
                return False, ("C6 fails: the same target %r was "
                               "rewritten two ways" % target_was)
        by_target[target_was] = target_now
    used = set()
    for line in stored_without_labels:
        text, _annotation = L48.split_off_annotation(line)
        parts = text.split(" ", 1)
        if len(parts) != 2:
            continue
        if not L48.is_transfer(parts[0]):
            continue
        target = parts[1].strip()
        if target.startswith("L"):
            if target[1:].isdigit():
                used.add(target)
    for name in sorted(used):
        if name not in defined:
            return False, ("C6 fails: the stored body branches to %s "
                           "and defines no such label" % name)
    return True, ("C6: the only text this form changed inside the body "
                  "is the TARGET operand of %d transfer(s); every "
                  "mnemonic, every other operand and every trailing "
                  "annotation is the body's own, the rewrite is a "
                  "function of the target, and every positional label "
                  "the body branches to is defined exactly once in it"
                  % len(rewritten_at))


def structural_route(fields):
    """canon37_gate's route, with C6 added."""
    ok, note = G37.structural_route(fields)
    if not ok:
        return False, note
    ok6, note6 = check_six(fields)
    if not ok6:
        return False, note6
    checks = list(note)
    checks.append(note6)
    return True, checks
