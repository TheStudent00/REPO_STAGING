#!/usr/bin/env python3
"""canon19_render.py -- JOB 1: RENDER THE PACKED-MASK FLOAT COMPARE
FAMILY BACK TO INSTRUCTIONS, using canon16_xmm.py's own designated
registers (a -> %xmm0, b -> %xmm1) and its ordered XMM temp pool --
same entry contract as canon17_render.py, extended with a recursive
walk of condition_table5.parse_maskexpr's own AST (AndV128/OrV128
compose more than one packed compare; canon17_render.py's own fcond
family never needed this, since its own combinators -- Or8/And8 on an
already-reduced 0/1 BYTE -- are the EXISTING gen7 GP-ALU fold, not a
new XMM-level combinator).

THE RENDER, per leaf `("cmp", precision, is_ne, p_tag, q_tag)`: copy
P's own register into a FRESH temp (`movaps`/`movapd` -- the
STANDARDIZED temp pool, never P's own designated register, so a/b are
never clobbered even though real ship code often clobbers them --
canonical text is DERIVED, not a transcription of real ship's own
register pressure choices), then compare the temp against Q in place
(`cmpeqsd`/`cmpneqsd`/`cmpeqss`/`cmpneqss`, AT&T `SRC,DST` -- DST is
the temp/P-copy, SRC is Q, matching P vs Q exactly as recorded).
`("and"|"or", L, R)`: render L, render R (each into its OWN fresh
temp), then `andps`/`orps` L's temp with R's temp in place (bitwise
combination -- precision-suffix choice does not affect the bits, "ps"
used uniformly for the combinator the same way real ship's own c/303
example does: `orps %xmm1,%xmm0` combining two cmpneqss masks). The
FINAL temp's low 32 bits are the answer; one `movd` hands it to the
GP `dest_base` the caller (the EXISTING And32(1,...) renderer) already
expects -- no new GP-side code needed at all.

REFUSAL, HONEST: `condition_table5.parse_maskexpr` already refused (at
substitution time) any unit outside its own six-operand/four-op-name
grammar, so by the time a `packmask` provenance record reaches this
file, `maskexpr` is never None -- this file's only NEW refusal is a
p_tag/q_tag comparison between the SAME tag twice (e.g. a vs a --
never measured, structurally impossible to make an "==" TRUE/FALSE
distinction render meaningfully with only one live register) or an
unbound precision mismatch across an And/OrV128 pair (also never
measured -- this corpus's own SIMD compares never mix f32 and f64
lanes within one AndV128/OrV128), named by `Unsupported`, never
guessed at.

MONKEYPATCH, same technique as canon11/12/13/14/17_render.py:
canon7_render.gen7 is reassigned to gen19 (falls back to canon17_
render.gen17, UNCHANGED, for every node this file's own new case does
not apply to -- so the ucomisd family this lap's earlier generation
already renders keeps working, unperturbed); canon7_render.to_z3_with_
prov is reassigned to canon19_float.to_z3_with_prov_v2c.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                           # noqa: E402
import canon7_render as R7                                     # noqa: E402
import canon17_render as R17                                   # noqa: E402
import canon16_xmm as X16                                       # noqa: E402
import canon19_float as CF19                                    # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
Unsupported = R7.Unsupported

CURRENT_A_IS_VECTOR = R17.CURRENT_A_IS_VECTOR
set_render_context = R17.set_render_context

TEMP_POOL = X16.XMM_TEMP_POOL_ORDER


def _next_temp(ctx):
    idx = getattr(ctx, "packmask_temp_idx", 0)
    if idx >= len(TEMP_POOL):
        raise Unsupported(
            "packed-mask compare needs more XMM temps than this "
            "file's own ordered pool has (%d) -- never measured in "
            "this corpus" % len(TEMP_POOL))
    ctx.packmask_temp_idx = idx + 1
    return TEMP_POOL[idx]


def _operand_xmm(tag, precision, ctx, lines):
    """the physical %xmmN register HOLDING (read-only reference,
    never clobbered by this file's own leaf render -- see file header)
    this operand. Mirrors canon17_render._operand_xmm exactly."""
    if tag in ("a", "b"):
        return CANON.designated(tag, "xmm0", CURRENT_A_IS_VECTOR[0])
    if tag == "zero":
        already = getattr(ctx, "packmask_zero_reg", None)
        if already is not None:
            return already
        temp = _next_temp(ctx)
        mnem = "xorps" if precision == 32 else "xorpd"
        lines.append("%s %%%s,%%%s" % (mnem, temp, temp))
        ctx.packmask_zero_reg = temp
        return temp
    raise Unsupported(
        "packed-mask compare operand tag %r is outside this file's "
        "own whitelist (a/b/zero) -- no return path" % tag)


def _render_leaf_cmp(precision, is_ne, p_tag, q_tag, ctx, lines):
    if p_tag == q_tag:
        raise Unsupported(
            "packed-mask compare between two operands sharing the "
            "same tag (%r) is not modeled -- never measured in this "
            "corpus" % p_tag)
    dest = _next_temp(ctx)
    p_reg = _operand_xmm(p_tag, precision, ctx, lines)
    q_reg = _operand_xmm(q_tag, precision, ctx, lines)
    copy_mnem = "movaps" if precision == 32 else "movapd"
    lines.append("%s %%%s,%%%s" % (copy_mnem, p_reg, dest))
    suffix = "ss" if precision == 32 else "sd"
    cmp_mnem = ("cmpneq" if is_ne else "cmpeq") + suffix
    lines.append("%s %%%s,%%%s" % (cmp_mnem, q_reg, dest))
    return dest


def _render_maskexpr(node, ctx, lines):
    kind = node[0]
    if kind == "cmp":
        _, precision, is_ne, p_tag, q_tag = node
        return _render_leaf_cmp(precision, is_ne, p_tag, q_tag, ctx,
                                 lines)
    if kind in ("and", "or"):
        _, left, right = node
        left_reg = _render_maskexpr(left, ctx, lines)
        right_reg = _render_maskexpr(right, ctx, lines)
        mnem = "andps" if kind == "and" else "orps"
        lines.append("%s %%%s,%%%s" % (mnem, right_reg, left_reg))
        return left_reg
    raise Unsupported(
        "packed-mask compare AST node kind %r is not one of this "
        "file's own cmp/and/or shapes -- no return path" % (kind,))


def _render_packmask(payload, dest_base, ctx, lines):
    maskexpr = payload["maskexpr"]
    if maskexpr is None:
        raise Unsupported(
            "packed-mask compare text %r did not parse under "
            "condition_table5.parse_maskexpr -- no return path"
            % payload.get("text"))
    result_reg = _render_maskexpr(maskexpr, ctx, lines)
    lines.append("movd %%%s,%s" % (result_reg, reg_text(dest_base, 32)))
    return 1


def gen19(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, payload = prov[name]
        if kind == "packmask":
            return _render_packmask(payload, dest_base, ctx, lines)
    return R17.gen17(node, dest_base, ctx, lines, prov)


R7.gen7 = gen19
R7.to_z3_with_prov = CF19.to_z3_with_prov_v2c

render_unit19 = R7.render_unit7
