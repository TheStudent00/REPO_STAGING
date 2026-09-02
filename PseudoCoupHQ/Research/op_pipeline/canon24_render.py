#!/usr/bin/env python3
"""canon24_render.py -- RENDER vex_names.py's fcmpmask/farith/vbitwise
provenance atoms (see that file's own header) BACK TO INSTRUCTIONS.

WHY THIS IS AN EXTRACT-LEVEL HOOK, NOT A BARE-ATOM HOOK. Every atom
this file renders is 128 bits wide (vex_names.REG_WIDTH -- the real
xmm register the op lives in), but the value a caller ever actually
NEEDS is the narrow low slice a real `movd`/`movq` reads (32 or 64
bits) -- canon24.py's own driver wraps every target unit's raw text in
an outer `ex32@0(...)` before normalizing specifically so z3's own
simplifier collapses the surrounding ins@0 dead-write bookkeeping down
to exactly `Extract(31, 0, <atom>)` (measured directly, canon24.py's
own report: the dead upper-lane bits disappear entirely, verified
mechanically by z3, not assumed). This file therefore intercepts the
Extract-of-atom SHAPE, not the atom alone -- a bare (un-extracted)
atom reaching this file is refused honestly (no return path measured
for it in this corpus).

Falls through to canon22_render.gen22 for everything else, the SAME
"check my own new cases, else delegate one generation down" shape
every renderer in this lineage uses (gen22 -> gen17 -> gen14 -> ...).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                           # noqa: E402
import canon7_render as R7                                      # noqa: E402
import canon16_xmm as X16                                        # noqa: E402
import canon17_render as R17                                     # noqa: E402
import canon20_arith as A20                                      # noqa: E402
import canon22_render as R22                                     # noqa: E402
import vex_names as VN                                           # noqa: E402
import z3                                                        # noqa: E402

Unsupported = R7.Unsupported
reg_text = R7.reg_text

TEMP_POOL = X16.XMM_TEMP_POOL_ORDER

ATOM_KINDS = ("farith", "fcmpmask", "vbitwise")


def _next_temp(ctx):
    idx = getattr(ctx, "vexnames_xmm_temp_idx", 0)
    if idx >= len(TEMP_POOL):
        raise Unsupported(
            "this family needs more XMM temps than the ordered pool "
            "has (%d) -- never measured in this corpus" % len(TEMP_POOL))
    ctx.vexnames_xmm_temp_idx = idx + 1
    return TEMP_POOL[idx]


def _resolve_xmm_operand(operand, ctx, lines):
    """P/Q operand tuple (condition_table6.classify_operand /
    vex_names.classify_operand_ext's own shape: ('direct',tag) |
    ('conv',tag,kind) | ('const',None) | None) -> a physical %xmmN
    register holding that operand's value, emitting any needed
    cvtsi2sd/cvtsi2ss/cvtss2sd conversion first. 'const' and an
    unrecognized shape are honest refusals -- never measured for this
    file's own target set (see canon24.py's own report)."""
    if operand is None:
        raise Unsupported(
            "compare/arithmetic operand is outside this file's own "
            "operand grammar (condition_table6.classify_operand / "
            "vex_names.classify_operand_ext) -- no return path")
    kind = operand[0]
    a_is_vector = R17.CURRENT_A_IS_VECTOR[0]
    if kind == "direct":
        tag = operand[1]
        return CANON.designated(tag, "xmm0", a_is_vector)
    if kind == "conv":
        _, tag, convkind = operand
        temp = _next_temp(ctx)
        if convkind == "f32_to_f64":
            home = CANON.designated(tag, "xmm0", a_is_vector)
            lines.append("cvtss2sd %%%s,%%%s" % (home, temp))
            return temp
        mnem = A20.CONV_MNEM.get(convkind)
        gp_width = A20.CONV_GP_WIDTH.get(convkind)
        if mnem is None:
            raise Unsupported(
                "unknown conversion kind %r -- no return path"
                % (convkind,))
        home = CANON.designated(tag, "rdi", a_is_vector)
        gp = A20.gp_reg(home, gp_width)
        lines.append("%s %%%s,%%%s" % (mnem, gp, temp))
        return temp
    raise Unsupported(
        "compare/arithmetic operand kind %r -- no return path"
        % (kind,))


def _render_fcmpmask(payload, width, dest_base, ctx, lines):
    precision = payload["precision"]
    if width > precision:
        raise Unsupported(
            "fcmpmask atom read at %d bits, wider than its own %d-"
            "bit compare precision -- no return path" %
            (width, precision))
    p_reg = _resolve_xmm_operand(payload["p_operand"], ctx, lines)
    q_reg = _resolve_xmm_operand(payload["q_operand"], ctx, lines)
    cond = payload["cond"]
    suffix = "ss" if precision == 32 else "sd"
    mnem = ("cmpeq" if cond == "eq" else "cmpneq") + suffix
    lines.append("%s %%%s,%%%s" % (mnem, q_reg, p_reg))
    gp_mnem = "movd" if precision == 32 else "movq"
    lines.append("%s %%%s,%s" % (
        gp_mnem, p_reg, reg_text(dest_base, precision)))
    # THE BOOLEAN-MATERIALIZATION IDIOM real ship code itself always
    # follows a mask-into-GP movd/movq with (measured on every one of
    # this family's own worked examples, c/op_501 and its siblings):
    # the packed mask is all-ones/all-zero, never itself the C boolean
    # 0/1 -- narrowing to bit 0 is done HERE, explicitly, rather than
    # trusting the generic AND-fold in canon7_render.gen7's own bvand/
    # De Morgan path, which was measured to mis-render a literal-1 AND
    # of a genuinely all-ones/all-zero operand as `movzx %al,%eax`
    # (keeps a whole byte, 0xff/0x00 -- wrong for a mask that is not
    # already a tagged 0/1 boolean; that fold was only ever exercised
    # before on setcc's own already-0/1 output). Emitting the `and`
    # ourselves, unconditionally, keeps this family's own correctness
    # independent of that shared fold.
    lines.append("and $0x1,%s" % reg_text(dest_base, 32))
    return width


def _render_farith(payload, width, dest_base, ctx, lines):
    precision = payload["precision"]
    if width != precision:
        raise Unsupported(
            "farith atom read at %d bits, not its own %d-bit "
            "precision -- no return path, never measured in this "
            "corpus" % (width, precision))
    p_reg = _resolve_xmm_operand(payload["p_operand"], ctx, lines)
    q_reg = _resolve_xmm_operand(payload["q_operand"], ctx, lines)
    op_mnem = {"Add": "add", "Sub": "sub", "Mul": "mul",
               "Div": "div"}[payload["op"]]
    suffix = "ss" if precision == 32 else "sd"
    lines.append("%s %%%s,%%%s" % (op_mnem + suffix, q_reg, p_reg))
    gp_mnem = "movd" if precision == 32 else "movq"
    lines.append("%s %%%s,%s" % (
        gp_mnem, p_reg, reg_text(dest_base, precision)))
    return width


def _render_vbitwise(payload, width, dest_base, ctx, lines):
    raise Unsupported(
        "whole-register bitwise (%s) read through a narrowing "
        "extract has no rendering rule in this file -- never "
        "measured in this corpus" % payload.get("op"))


def _render_atom_extract(kind, payload, hi, lo, dest_base, ctx, lines):
    if lo != 0:
        raise Unsupported(
            "%s atom extracted at a non-zero low bit (%d) -- no "
            "return path, never measured in this corpus" % (kind, lo))
    width = hi - lo + 1
    if kind == "fcmpmask":
        return _render_fcmpmask(payload, width, dest_base, ctx, lines)
    if kind == "farith":
        return _render_farith(payload, width, dest_base, ctx, lines)
    return _render_vbitwise(payload, width, dest_base, ctx, lines)


def gen24(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_EXTRACT:
        child = node.children()[0]
        if not z3.is_bv_value(child) and \
                child.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            entry = prov.get(child.decl().name())
            if entry is not None and entry[0] in ATOM_KINDS:
                hi, lo = node.params()
                kind, payload = entry
                return _render_atom_extract(
                    kind, payload, hi, lo, dest_base, ctx, lines)

    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        entry = prov.get(node.decl().name())
        if entry is not None and entry[0] in ATOM_KINDS:
            raise Unsupported(
                "a %s atom is read directly, not through the "
                "narrowing extract real ship code itself always "
                "reads it through -- no return path measured for "
                "this shape in this corpus" % entry[0])

    return R22.gen22(node, dest_base, ctx, lines, prov)


R7.gen7 = gen24
R7.to_z3_with_prov = VN.to_z3_atoms_v3

render_unit24 = R7.render_unit7
