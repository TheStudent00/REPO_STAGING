#!/usr/bin/env python3
"""canon22_render.py -- RENDER THE CONVERSION-EXTENDED UCOMISD/UCOMISS
FLAGS FAMILY (condition_table8.py/canon22_float.py's conversion-aware
fcond payloads) BACK TO INSTRUCTIONS. Re-ports canon17_render.py's own
walk (same reason every renderer in this lineage re-ports -- see
canon19_render.py's own header), with ONE real addition: an fcond
payload's own p_tag/q_tag may now be a `("conv", tag, kind)` tuple
instead of a bare "a"/"b"/"zero" string, and resolving it emits the
ACTUAL conversion instruction (`cvtsi2sd`/`cvtsi2ss`) real ship code
itself emits -- canon20_arith.py's own CONV_MNEM/CONV_GP_WIDTH tables,
reused unchanged, exactly the way canon21_render.py already reused
them for the packed-mask compare family's own conversion operands.

TEMP POOL: canon17_render.py's own single guarded slot (`ctx.
fcmp_zero_reg`, ONE literal-zero temp -- that file's own target set
never needed more) is not enough here: a unit may need a temp for a
"zero" operand AND a separate temp for a converted operand, or two
DIFFERENT conversions of two different arguments in the SAME
comparison (measured directly, this file's own survey: cases A/B/C
in condition_table8.py's own header). This file switches to canon16_
xmm.XMM_TEMP_POOL_ORDER's own ordered allocator (`_next_temp`,
identical in shape to canon21_render.py's own), and caches a
CONVERTED operand's own resolved register by its `(tag, kind)`
identity (`ctx.fcmp_conv_regs`) so the SAME conversion, read by TWO
different fcond atoms in one unit (e.g. `a==b || a<b`, both against
the SAME converted `a`), is computed once, not twice -- real
hardware's own register-reuse discipline, mirrored, not invented.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                           # noqa: E402
import canon7_render as R7                                     # noqa: E402
import canon14_render as R14                                   # noqa: E402
import canon16_xmm as X16                                       # noqa: E402
import canon17_render as R17                                    # noqa: E402
import canon20_arith as A20                                     # noqa: E402
import canon22_float as CF22                                    # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
Unsupported = R7.Unsupported

TEMP_POOL = X16.XMM_TEMP_POOL_ORDER

CONV_MNEM = A20.CONV_MNEM
CONV_GP_WIDTH = A20.CONV_GP_WIDTH
gp_reg = A20.gp_reg

CURRENT_A_IS_VECTOR = R17.CURRENT_A_IS_VECTOR
set_render_context = R17.set_render_context

FCOND_TO_SUFFIX = R17.FCOND_TO_SUFFIX


def _next_temp(ctx):
    idx = getattr(ctx, "fcmpc_temp_idx", 0)
    if idx >= len(TEMP_POOL):
        raise Unsupported(
            "conversion-extended float comparison needs more XMM "
            "temps than this file's own ordered pool has (%d) -- "
            "never measured in this corpus" % len(TEMP_POOL))
    ctx.fcmpc_temp_idx = idx + 1
    return TEMP_POOL[idx]


def _operand_xmm(tag, width, ctx, lines):
    """the physical %xmmN register holding this operand -- extends
    canon17_render._operand_xmm with the `("conv", tag, kind)` case
    (see file header). `tag` here is the WHOLE p_tag/q_tag value from
    the fcond payload, not yet unpacked."""
    if isinstance(tag, tuple):
        _, src_tag, kind = tag
        cache = getattr(ctx, "fcmp_conv_regs", None)
        if cache is None:
            cache = {}
            ctx.fcmp_conv_regs = cache
        key = (src_tag, kind)
        if key in cache:
            return cache[key]
        temp = _next_temp(ctx)
        if kind == "f32_to_f64":
            home = CANON.designated(src_tag, "xmm0",
                                     CURRENT_A_IS_VECTOR[0])
            lines.append("cvtss2sd %%%s,%%%s" % (home, temp))
            cache[key] = temp
            return temp
        mnem = CONV_MNEM.get(kind)
        gp_width = CONV_GP_WIDTH.get(kind)
        if mnem is None:
            raise Unsupported(
                "unknown float-compare conversion kind %r -- no "
                "return path" % (kind,))
        home = CANON.designated(src_tag, "rdi", CURRENT_A_IS_VECTOR[0])
        gp = gp_reg(home, gp_width)
        lines.append("%s %%%s,%%%s" % (mnem, gp, temp))
        cache[key] = temp
        return temp

    if tag in ("a", "b"):
        return CANON.designated(tag, "xmm0", CURRENT_A_IS_VECTOR[0])
    if tag == "zero":
        already = getattr(ctx, "fcmp_zero_reg", None)
        if already is not None:
            return already
        temp = _next_temp(ctx)
        mnem = "xorps" if width == 32 else "xorpd"
        lines.append("%s %%%s,%%%s" % (mnem, temp, temp))
        ctx.fcmp_zero_reg = temp
        return temp
    raise Unsupported(
        "float comparison operand tag %r is outside this file's own "
        "whitelist -- no return path" % (tag,))


def _emit_ucomis(p_tag, p_w, q_tag, q_w, ctx, lines):
    """identical shape to canon17_render._emit_ucomis -- the cache key
    now includes the FULL tag (a conv tuple is hashable), so a
    converted operand is only ever compared once against a given
    other operand."""
    if p_w != q_w:
        raise Unsupported(
            "float comparison operand width mismatch (%d vs %d) -- "
            "never measured in this corpus, refusing rather than "
            "guessing which width to compare at" % (p_w, q_w))
    cache = getattr(ctx, "fcmp_done", None)
    if cache is None:
        cache = {}
        ctx.fcmp_done = cache
    key = (p_tag, q_tag, p_w)
    if key in cache:
        return
    p_reg = _operand_xmm(p_tag, p_w, ctx, lines)
    q_reg = _operand_xmm(q_tag, q_w, ctx, lines)
    mnem = "ucomisd" if p_w == 64 else "ucomiss"
    lines.append("%s %%%s,%%%s" % (mnem, q_reg, p_reg))
    cache[key] = True


def _render_fcond(payload, dest_base, ctx, lines):
    fcond = payload["fcond"]
    p_tag, p_w = payload["p_tag"], payload["p_width"]
    q_tag, q_w = payload["q_tag"], payload["q_width"]
    if p_tag is None or q_tag is None:
        raise Unsupported(
            "float comparison operand(s) outside this file's own "
            "whitelist (p=%r q=%r) -- no return path; see condition_"
            "table8.py's own classify_float_operand8" % (
                payload.get("p_text"), payload.get("q_text")))
    if p_tag == q_tag:
        raise Unsupported(
            "float comparison between two operands sharing the same "
            "resolved identity (%r) is not modeled -- never measured "
            "in this corpus" % (p_tag,))
    suf = FCOND_TO_SUFFIX.get(fcond)
    if suf is None:
        raise Unsupported(
            "synthetic float condition %r has no known setcc suffix"
            % fcond)
    _emit_ucomis(p_tag, p_w, q_tag, q_w, ctx, lines)
    lines.append("mov $0,%s" % reg_text(dest_base, 32))
    lines.append("set%s %s" % (suf, reg_text(dest_base, 8)))
    return 1


def gen22(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, payload = prov[name]
        if kind == "fcond":
            return _render_fcond(payload, dest_base, ctx, lines)
    return R14.gen14(node, dest_base, ctx, lines, prov)


R7.gen7 = gen22
R7.to_z3_with_prov = CF22.to_z3_with_prov_v2e

render_unit22 = R7.render_unit7
