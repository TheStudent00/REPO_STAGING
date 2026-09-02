#!/usr/bin/env python3
"""job1_float_worked_examples.py -- generates job1_float_worked_
examples.txt, the reading-form (SPEC_reading_form.md) rendering of a
handful of this lap's JOB 1/2/3 (condition_table4.py/canon17_float.py/
canon17_render.py/canon17_behaviour_check.py) converged units, plus
the JOB 3 counterexample (c/op_285) worked by hand.

Does NOT modify reading_form.py (an existing artifact) -- imports its
per-instruction `render_instruction`, and adds exactly one small local
adapter this pipeline's OWN canonical renderer needs that reading_
form.py's own vocabulary (built from REAL compiler AT&T text) does not
carry: canon7_render.py's `movzx`/`movsx`/`movsxd` are un-suffixed
(the pipeline's own established convention -- see canon7_render.py's
`_ensure_native_write`), where reading_form.py's own ZERO_EXTEND_MNEM/
SIGN_EXTEND_MNEM sets only recognize the AT&T size-precise spellings
(`movzbl`, `movslq`, ...) real compiler text always uses. THE SAME
INSTRUCTION, two spellings for the same widths -- this file's own
`_atnt_widen_mnem` picks the AT&T spelling from the operands' own
recorded widths (canon.WIDTH_OF, the SAME table reading_form.py itself
already uses) so the existing template still applies unchanged.

usage:
  job1_float_worked_examples.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                    # noqa: E402
import reading_form as RF                                       # noqa: E402
import condition_table4 as CT4                                  # noqa: E402

WIDTH_LETTER = {0: "q", 1: "l", 2: "w", 3: "b"}


def _atnt_widen_mnem(mnem, operands):
    """movzx/movsx/movsxd (this pipeline's own bare spelling) -> the
    AT&T size-precise spelling reading_form.py's own template table
    recognizes, e.g. `movzx %al,%eax` -> `movzbl` (8-bit source, 32-bit
    destination)."""
    if mnem not in ("movzx", "movsx", "movsxd"):
        return mnem
    src, dst = operands[0], operands[1]
    src_w = canon.WIDTH_OF.get(src[1:])
    dst_w = canon.WIDTH_OF.get(dst[1:])
    src_letter = WIDTH_LETTER[src_w]
    dst_letter = WIDTH_LETTER[dst_w]
    prefix = "movz" if mnem == "movzx" else "movs"
    return "%s%s%s" % (prefix, src_letter, dst_letter)


def reading_line(instr_text, ret_register):
    mnem, operands = canon.parse(instr_text)
    mnem = _atnt_widen_mnem(mnem, operands)
    return RF.render_instruction(mnem, operands, ret_register, True)


def two_column(instr_texts, ret_register):
    """[(instr_text, reading_line), ...], space-aligned when printed."""
    out = []
    for text in instr_texts:
        try:
            line = reading_line(text, ret_register)
        except RF.Unsupported as e:
            line = "<UNSUPPORTED: %r>" % e.mnem
        out.append((text, line))
    return out


def render_block(title, instr_texts, ret_register="%eax"):
    rows = two_column(instr_texts, ret_register)
    width = max(len(t) for t, _ in rows) + 4
    lines = [title]
    for t, r in rows:
        lines.append("    %s%s%s" % (t, " " * (width - len(t)), r))
    return "\n".join(lines)


def main():
    out = []
    out.append(
        "job1_float_worked_examples.txt -- JOB 1/2/3 (condition_"
        "table4.py's float packed-flags model, canon17_render.py's "
        "XMM rendering, the resolve_conditions bug fix), reading-form "
        "worked examples (SPEC_reading_form.md's two-column style: "
        "instruction text, then plain-language reading, space-"
        "aligned). Every example below is a REAL converged unit from "
        "this lap's own canon17_units_<lang>.json, PROVED_EQUAL "
        "against its own real ship code by canon17_behaviour_check."
        "anchored_check -- see this file's own generator for how the "
        "reading column was built.")
    out.append("=" * 100)

    out.append("")
    out.append("EXAMPLE 1 -- c/op_663, `a < b`, a:float b:float (f32).")
    out.append("A pure float-vs-float comparison: real ship code does "
                "NOT compare a against b directly with `seta`/`setb` "
                "(setb/CondULT would be wrong on NaN -- see this "
                "file's own condition_table4.py header). It SWAPS the "
                "operand order instead (`ucomiss %xmm0,%xmm1` compares "
                "b against a) and reads `seta` (CondUGT = NOT(CF or "
                "ZF) -- correctly false on any NaN), which equals "
                "`a < b` for every non-NaN pair and correctly answers "
                "false whenever either operand is NaN.")
    out.append(render_block(
        "  real ship code:",
        ["ucomiss %xmm0,%xmm1", "xor %eax,%eax", "seta %al"]))
    out.append(render_block(
        "  this lap's candidate (canon17_text):",
        ["ucomiss %xmm0,%xmm1", "mov $0,%eax", "seta %al",
         "movzx %al,%eax"]))
    out.append("  both proved equal to real ship code directly "
                "(canon17_behaviour_check.anchored_check); the "
                "xor-vs-mov difference at the top is the pre-existing "
                "canonicalization convention (mov $0 over xor for a "
                "written-not-read destination), not a float-comparison "
                "difference.")

    out.append("")
    out.append("EXAMPLE 2 -- c/op_351, `a && b`, a:bool b:float (f32) "
                "-- THE MIXED-SIGNATURE REGISTER RULE.")
    out.append("Argument a is NOT a float here, so per canon.py's own "
                "`designated()` rule (\"b takes %xmm1 only when a is "
                "ALSO a floating-point value; otherwise b takes "
                "%xmm0\") the ONLY float argument, b, lives in %xmm0, "
                "not %xmm1. Real ship code's own `ucomiss %xmm1,%xmm0` "
                "compares b (in %xmm0) against a self-zeroed %xmm1 -- "
                "this lap's first rendering attempt assumed b always "
                "lives in %xmm1 and was DISPROVED by the ground-truth "
                "gate; canon17_render.py's `CURRENT_A_IS_VECTOR` fix "
                "(driven by the unit's own recorded meta.lhs_rep) "
                "closes exactly this gap.")
    out.append(render_block(
        "  real ship code:",
        ["xorps %xmm1,%xmm1", "ucomiss %xmm1,%xmm0", "setp %al",
         "setne %cl", "or %al,%cl", "and %dil,%cl", "movzbl %cl,%eax"]))
    out.append(render_block(
        "  this lap's candidate (canon17_text):",
        ["mov %rdi,%rax", "and $-1,%al", "xorps %xmm2,%xmm2",
         "ucomiss %xmm2,%xmm0", "mov $0,%r10d", "setp %r10b",
         "mov $0,%r11d", "setne %r11b", "or %r11b,%r10b",
         "and %r10b,%al", "movzx %al,%eax"]))
    out.append("  reading b's truthiness off the flags: `setp` reads "
                "the NaN flag (unordered means \"b is truthy\" in C, "
                "since NaN != 0.0), `setne` reads \"ordered and not "
                "equal to zero\"; ORing them is exactly `is_nan OR "
                "(not is_nan AND not is_eq)` -- condition_table4.py's "
                "own FCNE-under-Or8-with-FCPAR shape, the SAME "
                "algebra AgentMemory's own worked example names for "
                "go's `==`.")

    out.append("")
    out.append("EXAMPLE 3 -- JOB 3's counterexample, c/op_285 -- "
                "stage5_float_conditions_diagnosis.txt's own reported "
                "bug, reproduced and fixed.")
    ok, ct4_lines = CT4.job3_regression_check()
    out.append("  (condition_table4.job3_regression_check(), verbatim "
                "-- PASS below means this file's own substitution "
                "correctly reads the FIRST amd64g_calculate_condition "
                "call (cc=10) as Parity, not the mislabeled CondNE "
                "the old positional-pairing machinery would have "
                "produced if naively widened to the float family.)")
    for ln in ct4_lines:
        out.append("    " + ln)
    out.append("  JOB 3 regression check: %s" %
                ("PASS" if ok else "FAIL"))

    text = "\n".join(out) + "\n"
    path = os.path.join(HERE, "job1_float_worked_examples.txt")
    open(path, "w").write(text)
    print("wrote %s (%d bytes)" % (path, len(text)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
