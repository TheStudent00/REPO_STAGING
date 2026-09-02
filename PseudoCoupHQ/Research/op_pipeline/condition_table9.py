#!/usr/bin/env python3
"""condition_table9.py -- log_081 work item 2, THE FAN-OUT TRACER: per-
atom condition resolution for units whose normal_path_raw carries MORE
THAN ONE amd64g_calculate_condition/CmpF64 atom family in the SAME
expression, joined by the boolean structure (And/Or/Not) the
normalized expression already records (SEEDED GROUPING UNDER
CONDITIONS -- AgentMemory 2026-08-29 -- "trace follows transformations
indefinitely"; a tracer that only ever resolves a SINGLE atom kind per
unit is exactly the "implementation depth limit" that ruling names as
a defect, not a policy).

MEASURED TARGET (survey, this lap, over canon22_units_<lang>.json's
own `reason` field, matched against tree_units3.json -- the ADOPTED
tree_match3.py baseline): 78 not-yet-converged units refused with "no
return path: expression contains N distinct uninterpreted atoms
(...)" where the atom heads are exactly {amd64g_calculate_condition}
(42 units, 2 atoms) or {CmpF64, amd64g_calculate_condition} (36 units,
3 atoms). EVERY ONE of the 78 units' own amd64g_calculate_condition
calls has cc_op (the helper's own second numeric argument) in
{0, 19, 20} ONLY (survey script output, this lap) -- 0 is
condition_table4.py's own float packed-flags shape
(`And64(69:64,zx64(CmpF64(...)))`), already modelled by that file's
`substitute_float_packed`; 19/20 are LOGICL/LOGICQ (verdicts.py's own
independently-transcribed CC_OP table, cross-checked against
condition_table.py's own SUB/LOGIC dep1/dep2 convention -- two
independent sources agreeing, the evidence doctrine's standing
pattern). No SUB-family (cmp) call appears anywhere in this target
population (measured, not assumed).

THE MISSING PIECE, closed here: condition_table4.py's own JOB 3 fix
(read `cc` directly off the call's own numeric first argument -- VEX's
fixed AMD64CondCode enum, no canonical-text pairing, no position
assumption) is proved for the FLOAT family only. THIS FILE extends the
exact same direct-numeric-read insight to the plain INTEGER LOGIC
family: `dep2` for a LOGIC-family call is uniformly the literal
`0:64` (condition_table.py's own header states this convention; this
lap's own survey confirms it holds for all 72 LOGIC-family calls in
the 78-unit target population, zero exceptions), so a LOGIC-family
call can be resolved to `CondXX(dep1,dep2)` -- IDENTICAL output shape
to condition_table.py/condition_table3.py's own canonical-text-paired
substitution -- WITHOUT ever reading canonical text at all. The SUB
family (cc_op in {5,6,7,8}) is included too, using condition_table.py's
own header convention (dep1=L=AT&T DST, dep2=R=AT&T SRC) directly off
the call's own two data arguments, for completeness (never measured in
THIS population, but the same construction condition_table.py's own
header already documents, so it costs nothing to include and leaves no
family half-built).

WHY THIS IS SAFE TO COMBINE WITH THE FLOAT SUBSTITUTION IN ONE PASS:
condition_table4.find_float_packed_spans only ever matches calls whose
op-code is 0 AND whose dep1 is the packed-flags shape; this file's own
`substitute_direct_integer` only ever matches calls whose op-code is
in the SUB/LOGIC family ranges. The two span sets are DISJOINT BY
CONSTRUCTION (a call cannot have both op==0 and op in {5..8,17..20}),
so running the float substitution first and this file's integer
substitution second (each finding spans afresh in the OTHER'S already-
substituted text) never double-touches a call site and never depends
on ordering for correctness.

THE SPELLING BAN: this file is keyed by VEX's own numeric cc/cc_op
condition-code arguments and by the FIXED CC_OP shape (SUB/LOGIC
family membership, a helper-contract fact, not a source-language
token); it performs a per-call substitution inside ONE unit's own raw
expression text, never groups or pairs UNITS. check_no_spelling_keys.py
is run over every artifact this file's own driver (canon23.py) writes.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table as CT1                                   # noqa: E402
import condition_table3 as CT3                                  # noqa: E402
import condition_table4 as CT4                                  # noqa: E402

find_call_spans = CT1.find_call_spans
call_inner_args = CT1.call_inner_args

VEX_COND_NUM_TO_CONDXX = CT3.VEX_COND_NUM_TO_CONDXX

# verdicts.py's own independently-transcribed CC_OP table (guest_
# amd64_defs.h): base index, family name, per (8,16,32,64)-bit width.
# Reproduced here NUMERICALLY ONLY (the family membership fact, not
# verdicts.py's own word-rendering machinery) -- cross-checked against
# condition_table.py's own SUB/LOGIC dep1/dep2 convention, which is
# where the family names originate.
SUB_FAMILY_CCOPS = frozenset([5, 6, 7, 8])       # SUBB/W/L/Q
LOGIC_FAMILY_CCOPS = frozenset([17, 18, 19, 20])  # LOGICB/W/L/Q


def substitute_direct_integer(raw_text):
    """(new_text, applied, unresolved) -- resolves every remaining
    (non-float-packed) `amd64g_calculate_condition` call directly off
    its own numeric cc/cc_op arguments -- see file header. `unresolved`
    lists (cc, cc_op, reason) triples for any call this file's own
    whitelist does not cover (an honest partial application, not a
    guess -- callers refuse to render a unit with anything left in
    `unresolved` AND left uninterpreted)."""
    spans = find_call_spans(raw_text)
    if not spans:
        return raw_text, 0, []
    spans_sorted = sorted(spans, key=lambda s: s[0], reverse=True)
    out = raw_text
    applied = 0
    unresolved = []
    for span in spans_sorted:
        start, end, cc, op, args_start = span
        if op in LOGIC_FAMILY_CCOPS:
            family = "logic"
        elif op in SUB_FAMILY_CCOPS:
            family = "sub"
        else:
            family = None
        if family is None:
            unresolved.append(
                (cc, op, "cc_op %d is outside this file's own SUB/"
                 "LOGIC family whitelist (%r)" % (
                     op, sorted(SUB_FAMILY_CCOPS | LOGIC_FAMILY_CCOPS))))
            continue
        cond = VEX_COND_NUM_TO_CONDXX.get(cc)
        if cond is None:
            unresolved.append(
                (cc, op, "cc %d has no plain setcc-suffix condition "
                 "(condition_table3.VEX_COND_NUM_TO_CONDXX)" % cc))
            continue
        dep1, dep2, ndep = call_inner_args(raw_text, span)
        repl = "%s(%s,%s)" % (cond, dep1, dep2)
        out = out[:start] + repl + out[end:]
        applied = applied + 1
    return out, applied, unresolved


def substitute_all(raw_text):
    """(new_text, float_applied, int_applied, float_note, unresolved)
    -- runs condition_table4.substitute_float_packed FIRST (float
    packed-flags family, cc_op==0), then this file's own direct-
    numeric integer substitution over what is left (SUB/LOGIC family).
    See file header for why the two spans never overlap."""
    float_text, float_applied, float_note = \
        CT4.substitute_float_packed(raw_text)
    int_text, int_applied, unresolved = \
        substitute_direct_integer(float_text)
    return int_text, float_applied, int_applied, float_note, unresolved


def job_regression_check():
    """reproduces c/op_285's own raw text (the worked example, log_081
    item 2) and confirms this file's own combined substitution resolves
    ALL THREE atoms -- the two float packed-flags calls (FCPAR, FCNE)
    AND the sibling plain-integer LOGIC call (CondNE), leaving ZERO
    amd64g_calculate_condition/CmpF64 text behind."""
    raw = CT4.C_OP_285_RAW
    new_text, float_applied, int_applied, float_note, unresolved = \
        substitute_all(raw)
    lines = []
    lines.append("input: " + raw)
    lines.append("output: " + new_text)
    lines.append("float_applied=%d int_applied=%d unresolved=%r" % (
        float_applied, int_applied, unresolved))
    ok = True
    if float_applied != 2:
        ok = False
        lines.append("FAIL: expected 2 float substitutions")
    if int_applied != 1:
        ok = False
        lines.append("FAIL: expected 1 integer substitution")
    if unresolved:
        ok = False
        lines.append("FAIL: expected zero unresolved calls")
    if "amd64g_calculate_condition(" in new_text:
        ok = False
        lines.append("FAIL: a raw call site survived substitution")
    if "FCPAR(" not in new_text or "FCNE(" not in new_text:
        ok = False
        lines.append("FAIL: expected both FCPAR(...) and FCNE(...)")
    if "CondNE(" not in new_text:
        ok = False
        lines.append("FAIL: expected the sibling integer CondNE(...)")
    return ok, lines


if __name__ == "__main__":
    ok, lines = job_regression_check()
    for ln in lines:
        print(ln)
    print()
    print("condition_table9 regression check: %s" % (
        "PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
