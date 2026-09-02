#!/usr/bin/env python3
"""canon12_render.py -- STAGE 2's codegen half: renders the z3 wide-
divide/-remainder shape canon12_normalize.py's model produces back
into real x86-64 `idiv`/`div` with %rax/%rdx pinning. Mul64/Mul32
need NO new codegen at all -- z3's bitvector multiply (`kids[0] *
kids[1]`, decl `bvmul`) already truncates to the operand width by
construction, and gen7/gen11's EXISTING `bvmul` -> `imul` ALU_OP
entry renders it (see canon12_normalize.py's header for the measured
proof that this corpus's own Mul64/Mul32 units are all the plain
truncating 2-operand `imul` form, never the 1-operand widening one).

THE PATTERN, empirically confirmed on all 6 signed/unsigned x
quotient/remainder combinations in this corpus (c/op_211, 212, 217,
218, 247, 248 -- see this lap's report): after
canon12_normalize.normalize_v2()'s model runs and z3 simplifies, the
unit's WHOLE expression collapses to exactly

    Extract(63, 0, bvXdiv_i(DIVIDEND128, DIVISOR128))    -- quotient
    Extract(63, 0, bvXrem_i(DIVIDEND128, DIVISOR128))    -- remainder

(X is 's' or 'u'). Real x86-64 for a 64-bit dividend has no way to
avoid touching both %rax and %rdx (`cqto`/`idiv` and `xor %edx,%edx`/
`div` are hard-wired to that pair), so this is rendered as a NEW,
NARROW dispatch case in gen12() (checked BEFORE gen11's generic
"extract" handling, which has no rule for a bvXdiv_i/bvXrem_i child
and would otherwise refuse honestly) -- not a generalization of any
existing rule, because no existing rule reasons about a hardware-
pinned REGISTER PAIR at all.

gen12() otherwise DELEGATES to canon11_render.gen11 UNCHANGED (a
function reference, not a copy) for every other z3 op -- Stage 1's
two fixes stay exactly as they are, reused, not re-implemented.

MONKEYPATCH, same technique and same reasoning as canon11_render.py's
own (see that file's header): canon7_render.gen7 and canon7_render.
to_z3_with_prov are reassigned so canon7_render.render_unit7's own
self-consistency re-derivation (which the ground-truth gate depends
on running cleanly) picks up the wide-arithmetic model. Neither
canon7_render.py nor canon11_render.py's own source is edited.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon7_render as R7                                     # noqa: E402
import canon11_render as R11                                   # noqa: E402
import canon12_normalize as C12N                                # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
round_up_width = R7.round_up_width

WIDE_DIVMOD_DECL = set([
    "bvsdiv_i", "bvsdiv",
    "bvudiv_i", "bvudiv",
    "bvsrem_i", "bvsrem",
    "bvurem_i", "bvurem",
])


def _gen_wide_divmod(decl_name, kids, ctx, lines, prov):
    dividend128, divisor128 = kids
    signed = decl_name.startswith("bvs")
    want_quotient = "div" in decl_name

    dividend_lo = z3.simplify(z3.Extract(63, 0, dividend128))
    divisor64 = z3.simplify(z3.Extract(63, 0, divisor128))

    # dividend into %rax (== "ans") FIRST -- cqto/xor-%edx reads it.
    # (R7.gen7, not the literal name gen12 -- see canon11_render.py's
    # "DEEP-DISPATCH FIX" note; same late-binding reasoning applies
    # here so a later stage's rule can see a node nested under a
    # wide-divmod dividend/divisor, should one ever occur.)
    R7.gen7(dividend_lo, "ans", ctx, lines, prov)
    ctx.pins.add("rax")
    if signed:
        lines.append("cqto")
    else:
        lines.append("xor %edx,%edx")
    ctx.pins.add("rdx")

    t = ctx.alloc()
    R7.gen7(divisor64, t, ctx, lines, prov)
    mnem = "idiv" if signed else "div"
    lines.append("%s %s" % (mnem, reg_text(t, 64)))
    ctx.release(t)

    if not want_quotient:
        # quotient landed in %rax ("ans") for free; remainder is in
        # %rdx -- move it into the designated answer register.
        lines.append("mov %rdx,%rax")
    return 64


def gen12(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() != z3.Z3_OP_UNINTERPRETED and \
            node.decl().name() == "extract":
        hi, lo = node.params()
        if hi == 63 and lo == 0 and dest_base == "ans":
            args = node.children()
            if len(args) == 1:
                inner = args[0]
                if not z3.is_bv_value(inner) and \
                        inner.decl().kind() != z3.Z3_OP_UNINTERPRETED:
                    inner_name = inner.decl().name()
                    if inner_name in WIDE_DIVMOD_DECL and \
                            len(inner.children()) == 2:
                        return _gen_wide_divmod(
                            inner_name, inner.children(), ctx, lines,
                            prov)
    return R11.gen11(node, dest_base, ctx, lines, prov)


R7.gen7 = gen12
R7.to_z3_with_prov = C12N.to_z3_with_prov_v2

render_unit12 = R7.render_unit7
