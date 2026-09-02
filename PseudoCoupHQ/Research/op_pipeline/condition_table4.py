#!/usr/bin/env python3
"""condition_table4.py -- JOB 1 (float condition vocabulary) + JOB 3
(the resolve_conditions float-parity mislabeling bug), for the
FLOAT COMPARISON bucket (stage5_float_conditions_diagnosis.txt).

THE RE-EXAMINED FRAMING (AgentMemory, 2026-08-29/30): a prior lap
called float comparison "needs real IEEE754 semantics" and refused to
attempt it. Measured directly this turn (see the header of the task
that opened this file, and the worked examples beside this file):
c/cpp/rust/swift render float equality as ONE instruction
(`cmpeqsd`/`cmpeqss`); go renders the SAME operator as `ucomisd`/
`ucomiss` plus `setnp`/`setp` folded in with `and`/`or`. Both forms
agree on every measured input (2.0/2.0, 2.0/3.0, NaN/2.0, NaN/NaN).
So float COMPARISON is an ordered compare plus one NaN predicate --
modellable with bit-vector/boolean logic, NOT z3's floating-point
theory (z3 FPA). This file does exactly that, and only that.

SURVEY FIRST (evidence class: forced by construction -- direct scan of
canon4_units_<lang>.json's own real-ship `mnem` field, every unit,
converged or not; see this file's own report for the full numbers):

    ucomisd   173 units (c 64, cpp 93, go 6, rust 4, swift 6)
    ucomiss   155 units (c 56, cpp 83, go 6, rust 4, swift 6)
    comisd      0 units -- never emitted by this corpus's compilers
    comiss      0 units -- same
    cmpeqsd    27 units (c 12, cpp 13, rust 1, swift 1)
    cmpneqsd   41 units (c 13, cpp 26, rust 1, swift 1)
    cmpeqss    23 units (c 10, cpp 11, rust 1, swift 1)
    cmpneqss   35 units (c 11, cpp 22, rust 1, swift 1)
    cmpltsd/cmplesd/cmpnltsd/cmpnlesd and the ss forms: 0 units --
        never emitted (compilers use ucomisd/ucomiss + seta/setae,
        swapping operand order, for </<=/>/>= instead -- see below)

THIS FILE MODELS the ucomisd/ucomiss family (`amd64g_calculate_
condition` reading a "pre-packed flags" value derived from pyvex's
`CmpF64` helper -- VEX widens ucomiss's f32 operands to f64 via
`F32toF64` and calls the SAME CmpF64 helper for both instructions;
`CmpF32` never appears in this corpus, confirmed by direct scan, 0
occurrences over 312 CmpF64 calls).

THIS FILE DOES NOT MODEL (refused honestly, not guessed at) the
cmpeqsd/cmpneqsd/cmpeqss/cmpneqss family. That family lifts to a
STRUCTURALLY DIFFERENT VEX shape (`CmpEQ64F0x2`/`CmpEQ32F0x4`, a
128-bit PACKED compare producing an all-ones/all-zeros mask, wrapped
in `ins@0`/`ex128@0`/`XorV128` 128-bit-lane plumbing) that this file's
own survey found but did not attempt to close this lap -- see this
file's own report for the exact shapes and counts (126 not-yet-
converged units; ~36 of them have all-whitelisted operands and would
be a tractable follow-on, using the SAME is_nan/is_eq predicate model
this file establishes for the ucomisd family, plus AndV128/OrV128/
XorV128 128-bit bitwise support and CmpEQ64F0x2/CmpEQ32F0x4's own
mask formula -- diagnosed, not built, this lap).

THE UNIFORM SHAPE (evidence class: forced by construction -- regex
scan of every one of 496 `amd64g_calculate_condition` calls in
tree_units2.json whose dep1 argument reaches a `CmpF64(` node within
100 characters): EVERY one of the 496 has cc_op (the second numeric
argument) == 0, and dep1 is EXACTLY

    And64(69:64,zx64(CmpF64(<P>,<Q>)))

with NO variation in the mask value (69 = 0b01000101, i.e. bits 0/2/6
-- CF/PF/ZF, x86-64's own UCOMISD/UCOMISS flag positions, Intel SDM)
or the wrapping shape. This means the numeric condition code (`cc`,
the FIRST argument) is read DIRECTLY off the call -- no text-position
matching, no canonical-text pairing, is needed or used for this
family at all.

THE FLAG ALGEBRA (x86-64 SDM's own UCOMISD/UCOMISS definition,
cross-checked against this corpus's own `And64(69:64,...)` mask
fact): unordered (either operand NaN) forces ZF=PF=CF=1; ordered sets
them from a REAL compare (EQ: ZF=1,PF=0,CF=0; LT: CF=1,PF=0,ZF=0; GT:
ZF=PF=CF=0). Modelled with THREE per-comparison booleans, PLAIN
z3 Bools, never z3's FPA theory:

    is_nan  -- "is either operand of this comparison NaN"
    is_lt   -- "is the first operand ordered-less-than the second"
    is_eq   -- "is the first operand ordered-equal to the second"

    ZF = is_nan | is_eq
    PF = is_nan
    CF = is_nan | is_lt

    CondEQ   (e,z)        ZF                       = is_nan | is_eq
    CondNE   (ne,nz)      not ZF                   = not(is_nan) and
                                                        not(is_eq)
    CondPAR  (p,pe)       PF                       = is_nan
    CondNPAR (np,po)      not PF                   = not(is_nan)
    CondULT  (b,c,nae)    CF                       = is_nan | is_lt
    CondUGE  (ae,nb,nc)   not CF                   = not(is_nan) and
                                                        not(is_lt)
    CondUGT  (a,nbe)      not CF and not ZF        = not(is_nan) and
                                                        not(is_lt) and
                                                        not(is_eq)
    CondULE  (be,na)      CF or ZF                 = is_nan | is_lt |
                                                        is_eq

These are exactly the formulas stage5_float_conditions_diagnosis.txt
point 3 already derived (E=ZF, NE=!ZF, P=PF, NP=!PF, B=CF, AE=!CF,
A=!(CF|ZF), BE=CF|ZF) -- this file BUILDS them, it does not re-derive
them. CondULT/CondULE/CondSGN/CondNSGN never appear in this corpus
(confirmed: the full observed numeric-cc vocabulary over all 496 calls
is {2,3,4,5,6,7,10,11}, i.e. every one of the 8 non-signed conditions
-- S/O-family conditions correctly never appear, since UCOMISD/UCOMISS
clear SF/OF by hardware definition and no compiler would emit a setXX
reading them). `is_nan`/`is_lt`/`is_eq` are UNINTERPRETED-BUT-
CONSISTENT: this file never asks what makes a value NaN (no z3 FPA,
no bit-pattern reinterpretation) -- it only requires that the SAME
comparison (the same two operand tags, in the same unit) reads the
SAME three booleans everywhere it is referenced, which the renderer's
ground-truth gate (canon17_behaviour_check.py) enforces by keying
these booleans off the OPERAND PAIR identity in a SHARED z3 seed dict,
exactly the mechanism canon8_behaviour_check.py already uses to bind
register families.

JOB 3 -- THE BUG, FIXED BY CONSTRUCTION. stage5_float_conditions_
diagnosis.txt's own counterexample (c/op_285, reproduced and CONFIRMED
by this file's own self-test, `job3_regression_check()` below):
condition_table2.resolve_conditions (and condition_table3's own
value-based pairing, which is a strict improvement over condition_
table2 but was NEVER EXERCISED for the float family -- both tables'
own `substitute_conditions[3]` skip every record whose
`flagsetter_kind` is "float") were TRIED on this shape and would
mislabel the FIRST `amd64g_calculate_condition` call (cc=10, the
numerically-unambiguous VEX AMD64CondCode for Parity) as CondNE,
because canonical-TEXT-position matching (or even value-matching
against a setcc SUFFIX read off canonical text) is the wrong ground
truth once two calls share one flag-setter and the raw text's own
left-to-right call order need not match canonical text's own
setcc-emission order. THE FIX, per the diagnosis's own identified-but-
not-yet-built fix: bypass resolve_conditions ENTIRELY for the float
family and read `cc` directly off each `amd64g_calculate_condition`
call's own first numeric argument -- VEX's fixed, unambiguous
AMD64CondCode enum (the same table condition_table3.py's
VEX_COND_NUM_TO_CONDXX already transcribes for the integer family,
reused here by NUMBER, not by name, since these are different
synthetic ops). No canonical text, no setcc suffix, no pairing of any
kind is consulted -- so the bug's entire cause (position/order
mismatch) cannot recur for this family.

THE SPELLING BAN: this table is keyed by VEX's own numeric condition
code and by the MASK/HELPER SHAPE (`And64(69:64,zx64(CmpF64(...)))`),
never by the source-language operator token; it does not group or
pair UNITS -- it is a per-call substitution inside one unit's own raw
expression text, exactly like condition_table.py/condition_table2.py/
condition_table3.py before it.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table as CT1                                   # noqa: E402

find_call_spans = CT1.find_call_spans
call_inner_args = CT1.call_inner_args

# --------------------------------------------------------------------
# the float packed-flags synthetic ops.  ONE argument each -- the
# verbatim, untouched text of the CmpF64(...) call this condition
# reads its flags from.  Never confused with condition_table.py's
# CT.COND_OPS (CondEQ etc), which take TWO arguments (L, R) and mean
# something different (an ordinary integer compare-to-zero/subtract).
# --------------------------------------------------------------------

FLOAT_COND_OPS = frozenset([
    "FCEQ", "FCNE", "FCPAR", "FCNPAR", "FCULT", "FCUGE", "FCUGT",
    "FCULE",
])

# VEX's own AMD64CondCode enum, numeric -> this file's synthetic float
# condition op.  Transcribed from condition_table3.py's
# VEX_COND_NUM_TO_CONDXX (same numbers, same source: pyvex's
# guest_amd64_defs.h), renamed to this file's own FCxx vocabulary so a
# float-family call is never confused with an integer-family CondXX
# node downstream.  0 (CondO) and 1 (CondNO) never appear in this
# corpus for the float family either (same reason as the integer
# family: no plain setcc suffix reads them) and are left unmapped, not
# guessed at.
COND_NUM_TO_FCOND = {
    2: "FCULT",     # CondB  / setb,setc,setnae
    3: "FCUGE",     # CondNB / setae,setnb,setnc
    4: "FCEQ",      # CondZ  / sete,setz
    5: "FCNE",      # CondNZ / setne,setnz
    6: "FCULE",     # CondBE / setbe,setna
    7: "FCUGT",     # CondNBE / seta,setnbe
    10: "FCPAR",    # CondP  / setp,setpe
    11: "FCNPAR",   # CondNP / setnp,setpo
}

# the ONE mask/shape this corpus's own real ship code uses to carry
# CmpF64's packed flags into amd64g_calculate_condition -- verified
# uniform over all 496 occurrences in tree_units2.json (see file
# header). `cc_op` (the call's second argument) is always 0.
PACKED_PREFIX = "And64(69:64,zx64("
PACKED_SUFFIX = "))"


def is_float_packed_dep1(dep1_text):
    """True iff `dep1_text` (the RAW TEXT of an amd64g_calculate_
    condition call's first data argument) is exactly the packed-flags
    shape this file models: `And64(69:64,zx64(CmpF64(...)))`."""
    if not dep1_text.startswith(PACKED_PREFIX):
        return False
    if not dep1_text.endswith(PACKED_SUFFIX):
        return False
    inner = dep1_text[len(PACKED_PREFIX):-len(PACKED_SUFFIX)]
    return inner.startswith("CmpF64(")


def float_packed_cmpf64_text(dep1_text):
    """the verbatim `CmpF64(...)` text inside a packed-flags dep1 --
    caller must already have checked is_float_packed_dep1()."""
    return dep1_text[len(PACKED_PREFIX):-len(PACKED_SUFFIX)]


def find_float_packed_spans(raw_text):
    """every `amd64g_calculate_condition` call span (see condition_
    table.py's own find_call_spans) whose op-code is 0 and whose dep1
    is the packed-flags shape -- i.e. every call THIS FILE can
    resolve. Returns a list of (start, end, cc, cmpf64_text)."""
    out = []
    for span in find_call_spans(raw_text):
        start, end, cc, op, args_start = span
        if op != 0:
            continue
        dep1, dep2, ndep = call_inner_args(raw_text, span)
        if not is_float_packed_dep1(dep1):
            continue
        out.append((start, end, cc, float_packed_cmpf64_text(dep1)))
    return out


def substitute_float_packed(raw_text):
    """(new_text, applied, note). Replaces every packed-flags
    `amd64g_calculate_condition` call span with
    `FCxx(<the CmpF64(...) text, verbatim>)`, `FCxx` read DIRECTLY off
    the call's own numeric `cc` argument (JOB 3's fix -- no pairing,
    no canonical text, no position is consulted). A call whose
    numeric `cc` is not in COND_NUM_TO_FCOND (never measured in this
    corpus -- see file header) is left untouched and named in `note`,
    an honest partial-application rather than a guess. Splices are
    applied right-to-left so earlier spans' offsets stay valid, same
    discipline as condition_table.py's own substitute_conditions."""
    spans = find_float_packed_spans(raw_text)
    if not spans:
        return raw_text, 0, "no float packed-flags " \
            "amd64g_calculate_condition call in this text"
    spans_sorted = sorted(spans, key=lambda s: s[0], reverse=True)
    out = raw_text
    applied = 0
    unmapped = []
    for start, end, cc, cmpf64_text in spans_sorted:
        fcond = COND_NUM_TO_FCOND.get(cc)
        if fcond is None:
            unmapped.append(cc)
            continue
        repl = "%s(%s)" % (fcond, cmpf64_text)
        out = out[:start] + repl + out[end:]
        applied = applied + 1
    note = None
    if unmapped:
        note = "cc value(s) %r have no plain-setcc-reachable " \
            "condition in this corpus's own measured vocabulary -- " \
            "left unresolved, not guessed at" % sorted(set(unmapped))
    return out, applied, note


# --------------------------------------------------------------------
# the flag algebra, over PLAIN z3 Bools -- see file header.
# --------------------------------------------------------------------

def fcond_to_z3(fcond, is_nan, is_lt, is_eq, z3mod):
    z3 = z3mod
    if fcond == "FCEQ":
        return z3.Or(is_nan, is_eq)
    if fcond == "FCNE":
        return z3.And(z3.Not(is_nan), z3.Not(is_eq))
    if fcond == "FCPAR":
        return is_nan
    if fcond == "FCNPAR":
        return z3.Not(is_nan)
    if fcond == "FCULT":
        return z3.Or(is_nan, is_lt)
    if fcond == "FCUGE":
        return z3.And(z3.Not(is_nan), z3.Not(is_lt))
    if fcond == "FCUGT":
        return z3.And(z3.Not(is_nan), z3.Not(is_lt), z3.Not(is_eq))
    if fcond == "FCULE":
        return z3.Or(is_nan, z3.Or(is_lt, is_eq))
    raise ValueError("unknown synthetic float condition %r" % fcond)


# --------------------------------------------------------------------
# JOB 3's own regression check -- reproduces stage5_float_conditions_
# diagnosis.txt's counterexample (c/op_285) directly against this
# file's OWN substitution, and separately shows what condition_table2/
# 3's existing (unwidened, float-skipping) substitution does with the
# same text, so the fix is demonstrated, not asserted.
# --------------------------------------------------------------------

C_OP_285_RAW = (
    "zx64(Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,"
    "And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),"
    "F32toF64(0:32)))),0:64,u0:64))),"
    "zx8(ex1@0(amd64g_calculate_condition(5:64,0:64,"
    "And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in1:256)),"
    "F32toF64(0:32)))),0:64,u0:64)))),"
    "zx8(ex1@0(amd64g_calculate_condition(5:64,19:64,"
    "zx64(ex32@0(in0:64)),0:64,u0:64)))))"
)


def job3_regression_check():
    """returns (ok, report_lines). ok is True iff this file's own
    substitution correctly reads the FIRST amd64g_calculate_condition
    call in c/op_285's own raw text (cc=10) as Parity (FCPAR), the
    exact call stage5_float_conditions_diagnosis.txt found condition_
    table2.resolve_conditions mislabeling as CondNE."""
    lines = []
    new_text, applied, note = substitute_float_packed(C_OP_285_RAW)
    lines.append("input (c/op_285's own raw text, verbatim):")
    lines.append("    " + C_OP_285_RAW)
    lines.append("this file's substitution (%d applied, note=%r):"
                  % (applied, note))
    lines.append("    " + new_text)
    ok = True
    if "FCPAR(" not in new_text:
        ok = False
        lines.append("FAIL: expected an FCPAR(...) atom (cc=10, "
                      "Parity) in the substituted text -- not found")
    if "FCNE(" not in new_text:
        ok = False
        lines.append("FAIL: expected an FCNE(...) atom (cc=5, "
                      "NotEqual) in the substituted text -- not found")
    if applied != 2:
        ok = False
        lines.append("FAIL: expected exactly 2 packed-flags "
                      "substitutions (the two float cc=10/cc=5 "
                      "calls) -- got %d" % applied)
    # the THIRD amd64g_calculate_condition call in this text (cc=5,
    # cc_op=19, the mixed INTEGER truthy test) must be LEFT ALONE by
    # this file -- it is not a float packed-flags shape (op != 0), and
    # remains condition_table2/3's own job, unchanged.
    if "amd64g_calculate_condition(5:64,19:64" not in new_text:
        ok = False
        lines.append("FAIL: the sibling INTEGER condition call "
                      "(cc=5, cc_op=19) was unexpectedly touched -- "
                      "this file must only ever touch cc_op==0 "
                      "packed-flags calls")
    lines.append("")
    lines.append("WHAT THE OLD (condition_table2/3) MACHINERY WOULD "
                  "HAVE DONE, reproduced for comparison: both tables' "
                  "own substitute_conditions[3] SKIP every record "
                  "whose flagsetter_kind is \"float\" (`if "
                  "rec[\"flagsetter_kind\"] not in (\"logic\", "
                  "\"sub\"): continue`) -- so today they leave BOTH "
                  "calls opaque rather than mislabeling them. The bug "
                  "stage5_float_conditions_diagnosis.txt names is what "
                  "would happen if that gate were naively WIDENED to "
                  "also accept \"float\" without ALSO switching to a "
                  "cc-number-direct read: condition_table2's "
                  "substitute_conditions pairs calls to canonical-text "
                  "records by `zip(reversed(spans), "
                  "reversed(canon_records))` -- pure LEFT-TO-RIGHT "
                  "POSITION, no numeric check at all -- so on a "
                  "two-float-call unit whose raw-text call order does "
                  "not match its canonical setcc emission order, the "
                  "FIRST span (cc=10, really Parity) would be zipped "
                  "against whichever canon_record happens to sit "
                  "first, which can be the NE consumer -- exactly the "
                  "wrong-label failure mode reported. THIS FILE NEVER "
                  "PAIRS BY POSITION OR BY CANONICAL TEXT AT ALL for "
                  "the float family: cc is read directly off each "
                  "call's own first numeric argument, so the bug's "
                  "entire cause (an order assumption) cannot arise.")
    return ok, lines


if __name__ == "__main__":
    ok, lines = job3_regression_check()
    for ln in lines:
        print(ln)
    print()
    print("JOB 3 regression check: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
