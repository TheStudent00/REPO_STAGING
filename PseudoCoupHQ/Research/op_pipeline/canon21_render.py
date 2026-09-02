#!/usr/bin/env python3
"""canon21_render.py -- RENDER THE CONVERSION-EXTENDED PACKED-MASK
FLOAT COMPARE FAMILY (condition_table7.py/canon21_float.py's
FPACKMASK32C/FPACKMASK8C) BACK TO INSTRUCTIONS. Re-ports canon19_
render.py's own walk (same reason every renderer in this lineage
re-ports -- see canon19_render.py's own header), with ONE real
addition: a leaf operand may now be `("conv", tag, kind)` instead of a
bare "a"/"b"/"zero" tag, and rendering it emits the ACTUAL conversion
instruction (`cvtsi2sd`/`cvtsi2ss`/`cvtss2sd`) real ship code itself
emits -- canon20_arith.py's own CONV_MNEM/CONV_GP_WIDTH tables, reused
unchanged (the SAME five conversion kinds, the SAME instruction
choices, already measured correct by canon20_behaviour_check.py's own
z3-FPA gate for the packed ARITHMETIC family; this file applies them
to a COMPARE's operand instead of an arithmetic operand -- the
conversion itself does not care what consumes its result).

THE RENDER, per leaf `("cmp", precision, is_ne, p_operand, q_operand)`:
resolve P into a register (P's own designated home, if `direct`/
"a"/"b"/"zero"; a FRESH temp, converted via cvtsi2sd/cvtsi2ss/cvtss2sd,
if `("conv", tag, kind)` -- canon20_arith._resolve_operand's own
shape, re-implemented here since that function is entangled with
arithmetic's own P<op>Q return convention, not a compare's copy-then-
cmpXXss/sd convention); COPY (never convert twice) P's resolved
register into a fresh temp; compare Q (resolved the same way) against
it in place. AndV128/OrV128 combinators are unchanged from canon19_
render.py (they never touch a leaf's own resolution).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                           # noqa: E402
import canon7_render as R7                                     # noqa: E402
import canon19_render as R19                                   # noqa: E402
import canon16_xmm as X16                                       # noqa: E402
import canon20_arith as A20                                     # noqa: E402
import canon21_float as CF21                                    # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
Unsupported = R7.Unsupported

CURRENT_A_IS_VECTOR = R19.CURRENT_A_IS_VECTOR
set_render_context = R19.set_render_context

TEMP_POOL = X16.XMM_TEMP_POOL_ORDER

CONV_MNEM = A20.CONV_MNEM
CONV_GP_WIDTH = A20.CONV_GP_WIDTH
gp_reg = A20.gp_reg


def _next_temp(ctx):
    idx = getattr(ctx, "packmaskc_temp_idx", 0)
    if idx >= len(TEMP_POOL):
        raise Unsupported(
            "conversion-extended packed-mask compare needs more XMM "
            "temps than this file's own ordered pool has (%d) -- "
            "never measured in this corpus" % len(TEMP_POOL))
    ctx.packmaskc_temp_idx = idx + 1
    return TEMP_POOL[idx]


def _resolve_operand(operand, precision, ctx, lines):
    """the physical %xmmN register HOLDING this operand's value --
    returns the register name, WITHOUT the leading '%'. A `direct`
    ("a"/"b") operand's own designated home is returned directly
    (read-only reference, never clobbered); `zero` materializes a
    self-xor temp (cached per unit, same as canon19_render.py);
    `("conv", tag, kind)` materializes a FRESH temp via the real
    conversion instruction real ship code itself would use."""
    if isinstance(operand, tuple):
        _, tag, kind = operand
        temp = _next_temp(ctx)
        if kind == "f32_to_f64":
            home = CANON.designated(tag, "xmm0", CURRENT_A_IS_VECTOR[0])
            lines.append("cvtss2sd %%%s,%%%s" % (home, temp))
            return temp
        mnem = CONV_MNEM.get(kind)
        gp_width = CONV_GP_WIDTH.get(kind)
        if mnem is None:
            raise Unsupported(
                "unknown conversion kind %r -- no return path" % kind)
        home = CANON.designated(tag, "rdi", CURRENT_A_IS_VECTOR[0])
        gp = gp_reg(home, gp_width)
        lines.append("%s %%%s,%%%s" % (mnem, gp, temp))
        return temp

    tag = operand
    if tag in ("a", "b"):
        return CANON.designated(tag, "xmm0", CURRENT_A_IS_VECTOR[0])
    if tag == "zero":
        already = getattr(ctx, "packmaskc_zero_reg", None)
        if already is not None:
            return already
        temp = _next_temp(ctx)
        mnem = "xorps" if precision == 32 else "xorpd"
        lines.append("%s %%%s,%%%s" % (mnem, temp, temp))
        ctx.packmaskc_zero_reg = temp
        return temp
    raise Unsupported(
        "conversion-extended packed-mask compare operand %r is "
        "outside this file's own whitelist -- no return path" % (tag,))


def _operand_tag_pair(operand):
    """a hashable identity for the p_operand==q_operand same-tag
    refusal check -- a bare string for direct/zero, the FULL tuple for
    conv (two DIFFERENT conversions of the SAME source register are
    never the same value, e.g. i32_to_f64 of a vs i32_to_f32 of a)."""
    return operand


def _render_leaf_cmp(precision, is_ne, p_operand, q_operand, ctx,
                      lines):
    if _operand_tag_pair(p_operand) == _operand_tag_pair(q_operand):
        raise Unsupported(
            "conversion-extended packed-mask compare between two "
            "operands sharing the same resolved identity (%r) is not "
            "modeled -- never measured in this corpus"
            % (p_operand,))
    dest = _next_temp(ctx)
    p_reg = _resolve_operand(p_operand, precision, ctx, lines)
    q_reg = _resolve_operand(q_operand, precision, ctx, lines)
    copy_mnem = "movaps" if precision == 32 else "movapd"
    lines.append("%s %%%s,%%%s" % (copy_mnem, p_reg, dest))
    suffix = "ss" if precision == 32 else "sd"
    cmp_mnem = ("cmpneq" if is_ne else "cmpeq") + suffix
    lines.append("%s %%%s,%%%s" % (cmp_mnem, q_reg, dest))
    return dest


def _render_maskexpr(node, ctx, lines):
    kind = node[0]
    if kind == "cmp":
        _, precision, is_ne, p_operand, q_operand = node
        return _render_leaf_cmp(precision, is_ne, p_operand, q_operand,
                                 ctx, lines)
    if kind in ("and", "or"):
        _, left, right = node
        left_reg = _render_maskexpr(left, ctx, lines)
        right_reg = _render_maskexpr(right, ctx, lines)
        mnem = "andps" if kind == "and" else "orps"
        lines.append("%s %%%s,%%%s" % (mnem, right_reg, left_reg))
        return left_reg
    raise Unsupported(
        "conversion-extended packed-mask compare AST node kind %r is "
        "not one of this file's own cmp/and/or shapes -- no return "
        "path" % (kind,))


def _render_packmask(payload, dest_base, ctx, lines):
    maskexpr = payload["maskexpr"]
    if maskexpr is None:
        raise Unsupported(
            "conversion-extended packed-mask compare text %r did not "
            "parse under condition_table7.parse_maskexpr7 -- no "
            "return path" % payload.get("text"))
    result_reg = _render_maskexpr(maskexpr, ctx, lines)
    lines.append("movd %%%s,%s" % (result_reg, reg_text(dest_base, 32)))
    return 1


def gen21(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, payload = prov[name]
        if kind == "packmaskconv":
            return _render_packmask(payload, dest_base, ctx, lines)
    return R19.gen19(node, dest_base, ctx, lines, prov)


R7.gen7 = gen21
R7.to_z3_with_prov = CF21.to_z3_with_prov_v2d

render_unit21 = R7.render_unit7
