#!/usr/bin/env python3
"""canon13_render.py -- STAGE 4's codegen addition: the compound
boolean branch shapes gen7/gen11/gen12 have no rule for at all
("no rendering rule for boolean condition shape 'and'/'or'" -- the
literal refusal text, 16 units, canon12_units_<lang>.json's own
not_yet_converged reasons).

THE SHAPE, measured (c/op_551, `a > b`, a:uint64_t, b:bool -- real
ship `xor %r10d,%r10d; cmp %rsi,%rdi; mov %r10d,%eax; seta %al; ret`;
this lap's report has the full trace): condition_table2.py's own
CondXX substitution, for the specific (cc_op, cond) pair this unit's
flag computation carries, resolves to a COMPOUND z3 boolean --

    If(And(Extract(63,32,X) == 0, ULE(Extract(31,0,X), Extract(31,0,Y))),
       0, 1)                                                   -- c/551
    If(Or(Not(Extract(63,32,X) == 0), ULE(Extract(31,0,X), Extract(31,0,Y))),
       1, 0)                                                   -- cpp/587

-- an `if` node whose CONDITION is `And`/`Or` of two (or more)
DECODABLE comparisons, not one bare comparison the way `decode_bool_
condition` (unchanged since expr_to_canon.py) has always assumed.
Swift's 4 units (e.g. swift/op_296) hit the SAME gap one level
deeper: `If(And(...), 0, 1) | If(<plain comparison>, 0, 1)` -- the
OUTER `|` is a normal `bvor` the existing ALU fold already renders
fine (it calls gen13 on each `If` operand independently), but the
FIRST inner `If`'s own condition is the SAME `And(...)` shape, so
fixing the ONE gap fixes both measured forms.

THE FIX: `gen_bool()`, a small recursive renderer for a z3 BOOLEAN
node (as opposed to gen7/gen11/gen12's bitvector-valued `gen*()`) --
`and`/`or` fold their operands the same way `_gen_alu` folds a
bitvector ALU chain (render the first operand into the destination
byte, then AND/OR each further operand's rendering, via a temp, into
it -- sound because every operand is already a canonical 0/1 byte, so
bitwise and/or IS logical and/or); `not` renders its operand then
flips it (`xor $1,...`); the base case (a real comparison) is
`decode_bool_condition` + `cmp`/`set%s`, UNCHANGED, factored out of
gen7's own `if`-node body rather than duplicated. The `if` node
dispatch, when its own `decode_bool_condition(cond_node)` would have
raised (shape is `and`/`or`, checked by decl name BEFORE calling it,
never by catching the exception and guessing), now clears the
destination register (the boolean answer needs the SAME "mov $0,dest"
prelude a plain comparison already gets) and calls `gen_bool` on the
whole condition, negating the byte afterward if the `If`'s own
then/else pair was `(0, 1)` instead of `(1, 0)` -- the SAME then/else-
swap rule the single-comparison path already applies (`real_suf` in
gen7/gen11/gen12's own code), just implemented as a post-hoc negate
since a compound condition has no single setcc suffix to flip.

MONKEYPATCH, same technique as canon11_render.py/canon12_render.py:
canon7_render.gen7 is reassigned to gen13 (falls back to canon12_
render.gen12, UNCHANGED, for every other z3 op -- Stage 1/2's fixes
stay exactly as they are). canon7_render.to_z3_with_prov is left
exactly as canon12_render.py already set it (no normalizer change is
needed for this stage -- condition_table2.py's own substitution and
the existing COND_OPS handling in to_z3_with_prov already produce the
And/Or shape; the gap was purely on the RENDERING side).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon7_render as R7                                     # noqa: E402
import canon12_render as R12                                   # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
round_up_width = R7.round_up_width
decode_bool_condition = R7.decode_bool_condition
as_immediate = R7.as_immediate
_signed_of = R7._signed_of


def gen_bool(node, dest_base, ctx, lines, prov):
    """renders the z3 BOOLEAN `node` into `dest_base`'s low byte as a
    canonical 0/1 value. See file header for the and/or/not fold and
    why bitwise and/or of two 0/1 bytes is sound as logical and/or."""
    name = node.decl().name()
    if name in ("and", "or"):
        kids = node.children()
        gen_bool(kids[0], dest_base, ctx, lines, prov)
        mnem = "and" if name == "and" else "or"
        for k in kids[1:]:
            t = ctx.alloc()
            gen_bool(k, t, ctx, lines, prov)
            lines.append("%s %s,%s" % (
                mnem, reg_text(t, 8), reg_text(dest_base, 8)))
            ctx.release(t)
        return
    if name == "not":
        gen_bool(node.children()[0], dest_base, ctx, lines, prov)
        lines.append("xor $1,%s" % reg_text(dest_base, 8))
        return
    # base case: one decodable comparison -- gen7's own single-
    # comparison shape, factored out rather than duplicated.
    # (R7.gen7, not the literal name gen13 -- see canon11_render.py's
    # "DEEP-DISPATCH FIX" note; keeps this comparison's own operands
    # reachable by whatever stage is currently topmost, same as every
    # other layer in this chain.)
    suf, L, R = decode_bool_condition(node)
    tL = ctx.alloc()
    Lw_actual = R7.gen7(L, tL, ctx, lines, prov)
    Lw = round_up_width(Lw_actual)
    r_imm = as_immediate(R, prov)
    if r_imm is not None:
        lines.append("cmp $%d,%s" % (
            _signed_of(r_imm, Lw), reg_text(tL, Lw)))
    else:
        tR = ctx.alloc()
        R7.gen7(R, tR, ctx, lines, prov)
        lines.append("cmp %s,%s" % (
            reg_text(tR, Lw), reg_text(tL, Lw)))
        ctx.release(tR)
    lines.append("set%s %s" % (suf, reg_text(dest_base, 8)))
    ctx.release(tL)


def _is_compound_bool_if(node):
    if z3.is_bv_value(node):
        return False
    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        return False
    if node.decl().name() != "if":
        return False
    args = node.children()
    if len(args) != 3:
        return False
    cond_node, then_v, else_v = args
    is_bool_data = (
        z3.is_bv_value(then_v) and z3.is_bv_value(else_v) and
        then_v.size() == else_v.size() and
        set([then_v.as_long(), else_v.as_long()]) == set([0, 1]))
    if not is_bool_data:
        return False
    return cond_node.decl().name() in ("and", "or")


def gen13(node, dest_base, ctx, lines, prov):
    if _is_compound_bool_if(node):
        cond_node, then_v, else_v = node.children()
        w = node.size()
        native_w = round_up_width(w)
        if native_w > 8:
            lines.append("mov $0,%s" % reg_text(dest_base, native_w))
        gen_bool(cond_node, dest_base, ctx, lines, prov)
        if then_v.as_long() != 1:
            lines.append("xor $1,%s" % reg_text(dest_base, 8))
        return w
    return R12.gen12(node, dest_base, ctx, lines, prov)


R7.gen7 = gen13

render_unit13 = R7.render_unit7
