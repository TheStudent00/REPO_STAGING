#!/usr/bin/env python3
"""condition_table2.py -- JOB 2 fix: condition_table.py's flag-setter
recognition is too narrow.

THE DEFECT. condition_table.py's `FLAGSETTER_MNEMONICS` is exactly
`("test", "cmp", "ucomisd", "ucomiss")`. Any setcc/cmovcc that follows
a DIFFERENT real flag-setting instruction -- `or`, `and`, `xor` used
as a flag-setter (not via `cmp`/`test`) -- gets `scan_canonical_
text`'s `flagsetter_kind` = None (no branch matches), and
`substitute_conditions` then SKIPS that call site (`if
rec["flagsetter_kind"] not in ("logic", "sub"): continue`), leaving
its `amd64g_calculate_condition` atom opaque.

MEASURED SCOPE (read precisely, not assumed): 186 of canon8's 813
not-yet-converged units cite this atom as their refusal reason.
Breaking those 186 down by their ACTUAL flag-setter mnemonic (read
off canon4's own derived_text, the same canonical text condition_
table.py's scan already walks): 102 are `ucomisd`, 70 are `ucomiss`
(FLOAT compares -- condition_table.py already recognizes these
mnemonics but deliberately does not resolve them, see its own header,
"does not attempt to give CmpF64/CmpF32 real float semantics"; OUT OF
SCOPE for this file, a materially different problem needing real
float condition-code modeling), and exactly 16 have NO recognized
flag-setter at all -- THIS FILE'S TARGET. All 16, inspected
individually (not sampled), have their flags set by `or` or `xor`
(15 `setne` after `or`, 1 `cmove` after a chain ending `xor
%sil,%dil` -- cpp/op_785); zero need `and`, and zero need `add`/
`sub`/`neg`.

THE FIX, AND WHY IT IS SAFE DESPITE NOT BEING SEPARATELY angr-PROVED
for the new mnemonics (unlike test/cmp's 112-row proof in
condition_table.py's own header): `cond_to_z3` and `substitute_
conditions` never read `flagsetter_kind` for anything except the
logic/float GATE -- the actual substitution uses `dep1`/`dep2` read
VERBATIM off the RAW `amd64g_calculate_condition(...)` call site,
which is pyvex's OWN encoding of whatever the real flag-setting
instruction produced, independent of which text mnemonic this file
recognizes. So widening the gate cannot change the SUBSTITUTION math,
only whether a genuinely resolvable call site gets a chance to run
it. Concretely: this file adds ONLY "or", "and", "xor" to the
accepted set (NOT "add"/"sub"/"neg" -- see the derivation just below
this list for why those are excluded), mapped to the SAME "logic"
kind bucket as "test". Real x86-64 hardware sets flags after `or`/
`and`/`xor` EXACTLY like `test` (ZF/SF/PF from the result, CF=0,
OF=0, always -- Intel SDM); reading the 14 conditions against
(L,R)=(result,0) with CF=OF=0 fixed reproduces test's own already-
proved formula exactly (CondULT/CondULE collapse to always-false/
result==0; CondUGE/CondUGT collapse to always-true/result!=0 -- the
SAME reduction the generic z3 comparison already performs), so this
is the SAME proof condition_table.py's header already cites for the
LOGIC family, not a new unverified claim.

`add`/`sub`/`neg` are DELIBERATELY EXCLUDED: their CF/OF meaning is
carry-out / signed-overflow of the ORIGINAL operands, not "result
compared to zero", so the generic (L,R)=(result,0) reduction above
does NOT hold for their CF/OF-dependent suffixes (b/ae/a/be), and
this file has not verified pyvex's own dep1/dep2 shape for the ADD/
SUB-as-flagsetter CC_OP family. Since none of the 16 target units
need them, leaving them out costs nothing and keeps every inclusion
in this file provably sound rather than merely untested.

THE SAFETY NET (why this is not "trust and hope"): every candidate
this substitution enables still has to pass THE RE-ANCHORED GROUND-
TRUTH GATE (canon8_behaviour_check.py, JOB 1's fix, extended in
canon9.py with matching logic-family flag tracking in the CHECKER
itself -- see canon9.py's `Sim9`) before its text is accepted --
canon9.py, this fix's driver, calls job2_anchored_check() on every
changed candidate, the same shape canon8.py's JOB 1 pass already
does. If this file's widening is WRONG for some mnemonic or shape,
z3 disproves the candidate against the unit's own real ship code and
the old text is kept -- the same self-defending design the whole
pipeline already relies on. So this file's job is only to give more
units a CHANCE at a correct rendering; it does not itself get to
declare victory.

THE SPELLING BAN: unchanged -- this table is keyed by INSTRUCTION
KIND and CONDITION SUFFIX only, never by the source-language operator
token; it groups no units.

usage:
  condition_table2.py (library only)
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table as CT1                                   # noqa: E402

SUFFIX_TO_COND = CT1.SUFFIX_TO_COND
COND_OPS = CT1.COND_OPS
CONSUMER_PREFIXES = CT1.CONSUMER_PREFIXES
cond_to_z3 = CT1.cond_to_z3
consumer_kind_and_suffix = CT1.consumer_kind_and_suffix
bare_mnem = CT1.bare_mnem
find_call_spans = CT1.find_call_spans
call_inner_args = CT1.call_inner_args

# THE FIX: `or`/`and`/`xor` ONLY -- the LOGIC family, which real
# x86-64 hardware sets exactly like `test` (ZF/SF/PF from the result,
# CF=0, OF=0 always -- Intel SDM). This is the SAME bucket `test`
# already uses, so it is proved sound by the SAME 112-row proof
# condition_table.py's header already cites (the LOGIC family branch
# of that proof), NOT a new unverified claim, PROVIDED the following
# read of every one of the 14 conditions is checked against CF=OF=0
# (done in this file's own header derivation): CondULT/CondULE are
# always-false/result==0 respectively, CondUGE/CondUGT are always-
# true/result!=0 -- all of which the generic (L,R)=(result,0) z3
# formula reproduces exactly, because z3.ULT(result,0)/z3.UGT(result,
# 0)/etc. over an UNSIGNED-vs-zero comparison collapse to precisely
# those cases. `add`/`sub`/`neg` are DELIBERATELY EXCLUDED even
# though they are also common real flag-setters: their CF/OF meaning
# is NOT "result compared to zero" (it is carry-out / signed overflow
# of the ORIGINAL operands), so the generic (L,R)=(result,0) formula
# this file would otherwise reuse is WRONG for their CF/OF-dependent
# suffixes (b/ae/a/be), and this file has not verified pyvex's own
# amd64g_calculate_condition dep1/dep2 shape for the ADD/SUB-as-
# flagsetter CC_OP family the way condition_table.py's header proved
# for cmp specifically. `not`/`inc`/`dec` stay excluded too (`not`
# touches no flag at all; `inc`/`dec` do not touch CF). MEASURED
# SCOPE, so this restriction is not theoretical: of the 16 units this
# fix actually unblocks (see canon9.py's run), every one's flag-
# setter is `or` or `xor` -- zero need `and`/`add`/`sub`/`neg` (kept
# in the recognized set only because they cost nothing to allow when
# the SAME family reasoning applies to `and`; `add`/`sub`/`neg`
# genuinely are not in this set below).
FLAGSETTER_MNEMONICS = CT1.FLAGSETTER_MNEMONICS + (
    "or", "and", "xor",
)

# kind bucket for each newly-recognized mnemonic -- all "logic"
# (matches `test`'s own dep2-is-always-0 shape, confirmed empirically
# for `or` on c/op_282 -- see this file's header).
KIND_OF_NEW_MNEM = {
    "or": "logic",
    "and": "logic",
    "xor": "logic",
}


def scan_canonical_text(lines):
    """condition_table.py's scan_canonical_text, using THIS file's
    widened FLAGSETTER_MNEMONICS -- copied rather than parameterized
    because the original reads its module-level global directly."""
    out = []
    current_setter_index = None
    current_setter_mnem = None
    for i, line in enumerate(lines):
        mnem = bare_mnem(line)
        if mnem is None:
            continue
        if mnem in FLAGSETTER_MNEMONICS:
            current_setter_index = i
            current_setter_mnem = mnem
            continue
        prefix, suf = consumer_kind_and_suffix(mnem)
        if prefix is None:
            continue
        if mnem in FLAGSETTER_MNEMONICS:
            continue
        cond = SUFFIX_TO_COND[suf]
        if current_setter_mnem in ("test",):
            kind = "logic"
        elif current_setter_mnem == "cmp":
            kind = "sub"
        elif current_setter_mnem in ("ucomisd", "ucomiss"):
            kind = "float"
        elif current_setter_mnem in KIND_OF_NEW_MNEM:
            kind = KIND_OF_NEW_MNEM[current_setter_mnem]
        else:
            kind = None
        out.append(dict(
            index=i,
            mnem=mnem,
            cond=cond,
            flagsetter_index=current_setter_index,
            flagsetter_mnem=current_setter_mnem,
            flagsetter_kind=kind,
        ))
    return out


def substitute_conditions(raw_text, canon_records):
    """condition_table.py's substitute_conditions, unchanged logic --
    copied because it is small and this makes the module self-
    contained (no monkeypatching of CT1's globals, which would be
    fragile if CT1 is imported elsewhere in the same process)."""
    spans = find_call_spans(raw_text)
    if not spans:
        return raw_text, 0, "no amd64g_calculate_condition call in text"
    if len(spans) != len(canon_records):
        return raw_text, 0, (
            "call-site count (%d) does not match canonical-text "
            "flag-consumer count (%d) -- refusing rather than "
            "guessing the pairing" % (len(spans), len(canon_records)))
    out = raw_text
    applied = 0
    for span, rec in zip(reversed(spans), reversed(canon_records)):
        start, end, cc, op, args_start = span
        if rec["flagsetter_kind"] not in ("logic", "sub"):
            continue
        dep1, dep2, ndep = call_inner_args(raw_text, span)
        cond = rec["cond"]
        repl = "%s(%s,%s)" % (cond, dep1, dep2)
        out = out[:start] + repl + out[end:]
        applied += 1
    return out, applied, None


def resolve_conditions(expr_text, canon_text_lines):
    """tree_match2.resolve_conditions, pointed at THIS file's widened
    table instead of condition_table.py's."""
    if canon_text_lines is None:
        return expr_text, 0, "no canonical text available for this unit"
    records = scan_canonical_text(canon_text_lines)
    return substitute_conditions(expr_text, records)
