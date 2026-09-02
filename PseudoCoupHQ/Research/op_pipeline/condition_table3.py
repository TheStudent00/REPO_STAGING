#!/usr/bin/env python3
"""condition_table3.py -- JOB 2: THE CALL-SITE PAIRING DEFECT.

condition_table.py's own header names its own assumption plainly:
call sites are "matched to canonical text POSITIONALLY (the call
sites appear left-to-right in normal_path_raw in the same program
order as the setcc/cmov/branch instructions that read them --
verified on every worked example in the report; a unit where the
COUNTS disagree is refused, not guessed at)." That is a real
assumption, stated as one, and it is FALSE for at least two measured
shapes this lap traced to ground: `a <=> b` (cpp/750,751,756,757 --
two setcc's, `setl` then `setg`) and swift's Int32-vs-UInt64 mixed-
signedness compares (16 units -- `sets` then `setb`). Both are
TWO-call units where the raw VEX text's own left-to-right call order
is the OPPOSITE of the real assembly's setcc emission order, so
`condition_table2.substitute_conditions`'s `zip(reversed(spans),
reversed(canon_records))` pairs each call with the WRONG canon_record
-- measured directly: cpp/op_757 (evidence class: forced by
construction, VEX's own numeric argument, an unambiguous fixed enum,
independent of any text-position assumption) --

    raw text order:  amd64g_calculate_condition(2:64, 8:64, ...)
                      amd64g_calculate_condition(8:64, 19:64, ...)
    -> cond=2 is VEX's CondB  (== CondULT, matches real `setb`/cmp/sub)
    -> cond=8 is VEX's CondS  (== CondSGN, matches real `sets`/test/logic)

    real asm order (canon4's own mnem): `sets %cl` (index 0, CondSGN,
    test/logic) THEN `setg %al`... (for op_757 specifically the two
    setcc's are setl-then-setg, a different pair, but the SAME
    call-order-vs-asm-order mismatch shape) -- the positional zip
    assigns the FIRST raw-text call to the FIRST asm-order record,
    which is backwards whenever (as here) VEX's own left-to-right call
    order does not match the compiler's own setcc emission order.

THE FIX: `substitute_conditions3` still uses the OLD positional zip as
its DEFAULT (unchanged behaviour for every unit where it already
works -- this file never runs on any unit outside its own re-attempt
driver's target list, so it cannot regress anything already converged
regardless), but FIRST tries a VALUE-based pairing: each call span's
own numeric `cc` argument names an UNAMBIGUOUS VEX AMD64CondCode
(0-15, the fixed enum VEX's own lifter uses -- transcribed here from
pyvex's own AMD64CondCode, cross-checked against condition_table.py's
SUFFIX_TO_COND codomain, see the table below), which is compared
against each canon_record's OWN already-resolved `cond` name (from the
REAL asm's own setcc suffix). A span is paired with the UNIQUE
canon_record sharing its cond name (greedy, first-unassigned-match,
program order for genuine ties); any span/record that cannot be
matched this way falls back to the OLD positional pairing for that
slot alone -- a safe degradation, not a refusal. THE SAFETY NET is
unchanged from every other stage in this line: every candidate this
produces still has to pass the ground-truth gate before its text is
accepted.

THE SPELLING BAN: unchanged -- keyed by VEX's own numeric condition
code and by instruction MNEMONIC, never by the source-language
operator token; no units are grouped or paired.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table2 as CT2                                  # noqa: E402

scan_canonical_text = CT2.scan_canonical_text
find_call_spans = CT2.find_call_spans
call_inner_args = CT2.call_inner_args

# VEX's own AMD64CondCode enum (pyvex guest_amd64_defs.h), transcribed
# once here and cross-checked against condition_table.py's
# SUFFIX_TO_COND codomain for every entry that table also names (O/NO
# have no setcc-suffix entry in that table -- amd64g_calculate_
# condition's overflow-only conditions are never a plain setcc suffix
# this corpus's own real ship code emits, so they are left unmatched
# by design, not guessed at).
VEX_COND_NUM_TO_CONDXX = {
    0: None,               # CondO  -- no plain setcc suffix; unmatched
    1: None,               # CondNO -- same
    2: "CondULT",           # CondB
    3: "CondUGE",             # CondNB
    4: "CondEQ",                # CondZ
    5: "CondNE",                   # CondNZ
    6: "CondULE",                     # CondBE
    7: "CondUGT",                       # CondNBE
    8: "CondSGN",                          # CondS
    9: "CondNSGN",                            # CondNS
    10: "CondPAR",                               # CondP
    11: "CondNPAR",                                 # CondNP
    12: "CondSLT",                                     # CondL
    13: "CondSGE",                                        # CondNL
    14: "CondSLE",                                           # CondLE
    15: "CondSGT",                                              # CondNLE
}


def _pair_by_value(spans, canon_records):
    """returns a list, same length as canon_records, of the span
    (or None) each record is paired with -- value-matched by cond
    name where possible, else None (caller falls back to positional
    pairing for that slot)."""
    used_span_idx = set()
    pairing = [None] * len(canon_records)
    for ri, rec in enumerate(canon_records):
        want = rec["cond"]
        for si, span in enumerate(spans):
            if si in used_span_idx:
                continue
            cc = span[2]
            if VEX_COND_NUM_TO_CONDXX.get(cc) == want:
                pairing[ri] = span
                used_span_idx.add(si)
                break
    return pairing


def substitute_conditions3(raw_text, canon_records):
    """condition_table2.substitute_conditions, with THE FIX (see file
    header): value-based pairing tried first, positional pairing kept
    as the per-slot fallback. Same refusal shape as the original for
    a genuine count mismatch."""
    spans = find_call_spans(raw_text)
    if not spans:
        return raw_text, 0, "no amd64g_calculate_condition call in text"
    if len(spans) != len(canon_records):
        return raw_text, 0, (
            "call-site count (%d) does not match canonical-text "
            "flag-consumer count (%d) -- refusing rather than "
            "guessing the pairing" % (len(spans), len(canon_records)))

    value_pairing = _pair_by_value(spans, canon_records)
    positional_pairing = list(reversed(spans))
    used_by_value = set(
        id(s) for s in value_pairing if s is not None)

    # Collect (span, cond, how, mnem) triples FIRST, THEN apply the
    # text splices in DESCENDING span-start order -- the pairing
    # (record <-> span) is no longer guaranteed to walk spans
    # right-to-left as record-index walks in reverse (value-pairing
    # can assign a LATER record to an EARLIER span), so the splice
    # order must be re-derived from the spans' own text positions,
    # never assumed from record order. Splicing right-to-left is what
    # keeps every earlier (leftmost) span's start/end offsets valid as
    # the string's length changes -- the same reason the ORIGINAL
    # substitute_conditions iterates `reversed(spans)` at all.
    todo = []
    for i in range(len(canon_records)):
        rec = canon_records[i]
        if rec["flagsetter_kind"] not in ("logic", "sub"):
            continue
        span = value_pairing[i]
        how = "value"
        if span is None:
            span = positional_pairing[len(canon_records) - 1 - i]
            how = "positional"
            if id(span) in used_by_value:
                # the positionally-implied span was already claimed
                # by a DIFFERENT record's value match -- ambiguous,
                # refuse this call site rather than double-assign.
                continue
        todo.append((span, rec["cond"], how, rec["mnem"]))
    todo.sort(key=lambda t: t[0][0], reverse=True)

    out = raw_text
    applied = 0
    pairing_note_parts = []
    for span, cond, how, mnem in todo:
        start, end, cc, op, args_start = span
        dep1, dep2, ndep = call_inner_args(raw_text, span)
        repl = "%s(%s,%s)" % (cond, dep1, dep2)
        out = out[:start] + repl + out[end:]
        applied += 1
        pairing_note_parts.append("%s:%s" % (mnem, how))
    note = None
    if pairing_note_parts:
        note = "pairing: " + ", ".join(pairing_note_parts)
    return out, applied, note


def resolve_conditions3(expr_text, canon_text_lines):
    """condition_table2.resolve_conditions, pointed at THIS file's
    value-based-first pairing instead of the pure positional one."""
    if canon_text_lines is None:
        return expr_text, 0, "no canonical text available for this unit"
    records = scan_canonical_text(canon_text_lines)
    if not records:
        return expr_text, 0, "no flag-consuming instruction found in " \
            "canonical text"
    return substitute_conditions3(expr_text, records)
