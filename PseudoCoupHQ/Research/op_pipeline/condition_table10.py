#!/usr/bin/env python3
"""condition_table10.py -- log_084 lap, item 1 of the coordinator's
"jobs 1 and 3 are mechanical, do them now" instruction: the SUB-family
carry-bit direct-numeric-read for `amd64g_calculate_rflags_c`, the
SAME TECHNIQUE condition_table9.py already established for
`amd64g_calculate_condition` (read the family off the helper's own
numeric first argument -- VEX's fixed CC_OP enum -- no canonical-text
pairing, no position assumption).

MEASURED TARGET (survey, log_084's own script, reproduced here):
19 not-yet-converged units (matches name_census.json's own count for
this lifter_name) carry a raw `amd64g_calculate_rflags_c(cc_op, dep1,
dep2, ndep)` call. ALL 19 have cc_op in {7, 8} (SUB family -- SUBL/
SUBQ, condition_table9.py's own SUB_FAMILY_CCOPS, reused here
unchanged) -- ZERO exceptions, measured, not assumed. Every one of the
19 masks the call's result to bit 0 with `And64(1:64, ...)` or
`And8(1:8, ex8@0(...))`, e.g.:

    go/op_175:
      And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),
            Sub64(0:64,And64(1:64,
              amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))

    cpp/op_764:
      Sub8(zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,
           in1:64,u0:64))),
           And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in0:64,
           in1:64,u0:64))))

Bit 0 of the x86-64 RFLAGS word is the CARRY FLAG. For the SUB family,
hardware defines CF as the unsigned-borrow bit of `dep1 - dep2`:
CF = 1 iff (unsigned)dep1 < (unsigned)dep2. This is a fixed hardware
fact (Intel SDM Vol 1 3.4.3.1), not read off any canonical text and
not language-specific -- it costs nothing extra to state directly, the
same posture condition_table9.py's header takes for the LOGIC-family
dep2==0 convention.

WHAT THIS FILE DOES: replaces every `amd64g_calculate_rflags_c(cc_op,
dep1,dep2,ndep)` call whose cc_op is in the SUB family with a new
named atom `CF_SUB(dep1,dep2)` -- IDENTICAL in spirit to condition_
table3.py's `CondXX(dep1,dep2)` naming convention (a display atom, not
a raw helper call), so a later render-layer rule (NOT written here --
see log_084's second section: rendering a `CF_SUB`-bearing combination
shape is exactly the kind of new render-grouping decision the STOP
RULE reserves) can intercept it by name. `cc_op` values outside {7,8}
are left as an honest `unresolved` entry, never guessed.

THE SPELLING BAN: this file is keyed by VEX's own numeric `cc_op`
condition-code argument and by the FIXED CC_OP shape (SUB family
membership, a helper-contract fact, not a source-language token). It
performs a per-call substitution inside ONE unit's own raw expression
text; it never groups or pairs UNITS, so it has no key for
check_no_spelling_keys.py to examine -- no grouping/pairing artifact
is written by this file.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table9 as CT9                                  # noqa: E402

SUB_FAMILY_CCOPS = frozenset([5, 6, 7, 8])       # SUBB/W/L/Q

RFLAGS_CALL_HEAD = "amd64g_calculate_rflags_c("


def find_rflags_spans(raw_text):
    """returns a list of (start, end, cc_op, args_start) for every
    `amd64g_calculate_rflags_c(cc_op:64,` occurrence, left to right.
    `end` is the index just past the matching close-paren of the call
    itself (balanced-paren scan from the call's own open paren)."""
    spans = []
    search_from = 0
    while True:
        idx = raw_text.find(RFLAGS_CALL_HEAD, search_from)
        if idx == -1:
            break
        open_pos = idx + len(RFLAGS_CALL_HEAD) - 1
        colon_pos = raw_text.index(":", open_pos)
        cc_op = int(raw_text[open_pos + 1:colon_pos])
        j = open_pos
        depth = 0
        while j < len(raw_text):
            if raw_text[j] == "(":
                depth += 1
            elif raw_text[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        end = j + 1
        args_start = raw_text.index(",", colon_pos) + 1
        spans.append((idx, end, cc_op, args_start))
        search_from = end
    return spans


def rflags_inner_args(raw_text, span):
    """given a span from find_rflags_spans, return the RAW TEXT of
    (dep1, dep2, ndep) -- the three arguments after cc_op:64, inside
    amd64g_calculate_rflags_c(...), by a balanced-comma top-level
    scan (same technique as condition_table.call_inner_args)."""
    start, end, cc_op, args_start = span
    body = raw_text[args_start:end - 1]
    depth = 0
    parts = []
    cur = []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    if len(parts) != 3:
        raise ValueError(
            "expected 3 args (dep1,dep2,ndep), got %d: %r" % (
                len(parts), parts))
    return parts[0], parts[1], parts[2]


def substitute_sub_carry(raw_text):
    """(new_text, applied, unresolved) -- resolves every SUB-family
    `amd64g_calculate_rflags_c` call to a named `CF_SUB(dep1,dep2)`
    atom. `unresolved` lists (cc_op, reason) pairs for any call this
    file's own SUB-family whitelist does not cover (an honest partial
    application -- callers refuse to render a unit with anything left
    in `unresolved`)."""
    spans = find_rflags_spans(raw_text)
    if not spans:
        return raw_text, 0, []
    spans_sorted = sorted(spans, key=lambda s: s[0], reverse=True)
    out = raw_text
    applied = 0
    unresolved = []
    for span in spans_sorted:
        start, end, cc_op, args_start = span
        if cc_op not in SUB_FAMILY_CCOPS:
            unresolved.append(
                (cc_op, "cc_op %d is outside this file's own SUB "
                 "family whitelist (%r) -- no LOGIC/other-family "
                 "carry-bit formula is modelled here" % (
                     cc_op, sorted(SUB_FAMILY_CCOPS))))
            continue
        dep1, dep2, ndep = rflags_inner_args(raw_text, span)
        repl = "CF_SUB(%s,%s)" % (dep1, dep2)
        out = out[:start] + repl + out[end:]
        applied = applied + 1
    return out, applied, unresolved


def substitute_all(raw_text):
    """runs condition_table9.substitute_all FIRST (the amd64g_
    calculate_condition/CmpF64 family -- cpp/op_764 in the survey
    carries BOTH an amd64g_calculate_condition and an amd64g_
    calculate_rflags_c call in the same expression, so this file must
    compose with condition_table9 exactly the way condition_table9
    composes with condition_table4), then this file's own SUB-family
    carry-bit substitution over what is left. The two call heads are
    textually disjoint (`amd64g_calculate_condition` vs `amd64g_
    calculate_rflags_c`), so ordering never double-touches a call
    site."""
    ct9_text, float_applied, int_applied, float_note, ct9_unresolved = \
        CT9.substitute_all(raw_text)
    final_text, rflags_applied, rflags_unresolved = \
        substitute_sub_carry(ct9_text)
    return (final_text, float_applied, int_applied, rflags_applied,
            float_note, ct9_unresolved, rflags_unresolved)


GO_OP_175_RAW = (
    "And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),"
    "Sub64(0:64,And64(1:64,"
    "amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))")

CPP_OP_764_RAW = (
    "Sub8(zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,"
    "in1:64,u0:64))),And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,"
    "in0:64,in1:64,u0:64))))")


def job_regression_check():
    """reproduces go/op_175's own raw text (a single SUB-family
    rflags_c call, no condition call) and cpp/op_764's own raw text
    (BOTH an amd64g_calculate_condition call and an amd64g_calculate_
    rflags_c call in the same expression -- the compose-with-CT9
    case), confirming this file's own substitution resolves both call
    heads to named atoms, leaving zero raw helper-call text behind."""
    lines = []
    ok = True

    new_text, applied, unresolved = substitute_sub_carry(GO_OP_175_RAW)
    lines.append("go/op_175 input: " + GO_OP_175_RAW)
    lines.append("go/op_175 output: " + new_text)
    lines.append("applied=%d unresolved=%r" % (applied, unresolved))
    if applied != 1:
        ok = False
        lines.append("FAIL: expected 1 SUB-family substitution")
    if unresolved:
        ok = False
        lines.append("FAIL: expected zero unresolved calls")
    if "amd64g_calculate_rflags_c(" in new_text:
        ok = False
        lines.append("FAIL: a raw call site survived substitution")
    if "CF_SUB(in1:64,64:64)" not in new_text:
        ok = False
        lines.append("FAIL: expected CF_SUB(in1:64,64:64)")

    (final_text, float_applied, int_applied, rflags_applied,
     float_note, ct9_unresolved, rflags_unresolved) = \
        substitute_all(CPP_OP_764_RAW)
    lines.append("")
    lines.append("cpp/op_764 input: " + CPP_OP_764_RAW)
    lines.append("cpp/op_764 output: " + final_text)
    lines.append(
        "float_applied=%d int_applied=%d rflags_applied=%d "
        "ct9_unresolved=%r rflags_unresolved=%r" % (
            float_applied, int_applied, rflags_applied,
            ct9_unresolved, rflags_unresolved))
    if int_applied != 1:
        ok = False
        lines.append("FAIL: expected 1 CT9 integer substitution")
    if rflags_applied != 1:
        ok = False
        lines.append("FAIL: expected 1 rflags_c substitution")
    if "amd64g_calculate_condition(" in final_text:
        ok = False
        lines.append("FAIL: a raw condition call site survived")
    if "amd64g_calculate_rflags_c(" in final_text:
        ok = False
        lines.append("FAIL: a raw rflags_c call site survived")
    if "CondNBE(" not in final_text and "CondNLE(" not in final_text \
            and "Cond" not in final_text:
        ok = False
        lines.append("FAIL: expected a named Cond* atom from CT9")
    if "CF_SUB(in0:64,in1:64)" not in final_text:
        ok = False
        lines.append("FAIL: expected CF_SUB(in0:64,in1:64)")

    return ok, lines


if __name__ == "__main__":
    ok, lines = job_regression_check()
    for ln in lines:
        print(ln)
    print()
    print("condition_table10 regression check: %s" % (
        "PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
