#!/usr/bin/env python3
"""canon11_render.py -- STAGE 1 of this lap's remedy list: the two
DIAGNOSED renderer defects (72 units total), fixed at their exact
site in canon7_render.py's gen7() -- WITHOUT editing that file (a
kept artifact). This module MONKEYPATCHES canon7_render.gen7 to a
corrected version (gen11) at import time, so canon7_render.py's own
driver functions (render_unit7, render_block_value7, _gen_alu --
none of them touched, none of their SOURCE edited) pick up the fix
automatically: Python resolves the bare name `gen7` inside those
functions from canon7_render's OWN module globals at call time, and
this file only reassigns that one name in that dict. `gen11`'s body
is otherwise a byte-for-byte copy of canon7_render.gen7 -- every
other branch (ALU fold, shifts, extract, general concat, bvmul) is
UNCHANGED, ported verbatim.

TWO FIXES, both "fix a cause at first observation" (AgentMemory):

FIX (a) -- THE STALE-WIDTH COMPARISON BUG, 60 units (measured: the
"renderer produced a wrong candidate, gate correctly refused"
bucket -- canon10's `job2_decision` starting "KEEP_OLD -- DISPROVED"
with `and $-1,%rXd` in the rejected candidate text, verified by
direct count against canon10_units_<lang>.json). ROOT CAUSE, found
by tracing a worked example (c/op_534, `a > b`, a:int32_t b:int32_t
-- see this lap's own report for the full trace): gen7()'s `if` node
handler renders one comparison operand via `gen7(L, tL, ...)`, which
for an operand shaped `Concat(0, Extract(31,0,X))` (a 32-bit field
zero-extended to a 64-bit-sized z3 node -- THE CONCAT BUG FIX
upstream already makes gen7 return the width it ACTUALLY established
clean, 32, not the node's own claimed size, 64) -- but the `if`
handler THROWS AWAY that return value and instead re-derives the
comparison width from `L.size()`, the z3 node's STATIC size (64,
unrelated to what got written). The emitted `and $-1,%r11d` truncate
is not itself wrong (it is exactly what makes the 32-bit value clean
in the parent register) -- what is wrong is comparing the two
operands at 64 BITS instead of the 32 bits gen7 actually established,
because the comparison suffix decode_bool_condition() picked is
SIGNED (bvsgt/bvslt/... -> g/l/...), and a signed 64-bit compare of a
ZERO-extended (not sign-extended) 32-bit field is a different
relation than a signed 32-bit compare of the original field whenever
the field's top bit is a genuine sign bit (measured counterexample:
seed_rdi=0, seed_rsi=4294967294 -- real "0 > -2" is true; the 64-bit-
zero-extended-then-signed-compared candidate says false). THE FIX:
capture gen7()'s own return value for L (and R) and use THAT actual
established width for the cmp/set, not `L.size()`/`R.size()`.

FIX (b) -- THE NEGATION-DISTRIBUTED-THROUGH-CONCAT BUG, 12 units
(measured: c/427,428,432,438 and cpp/427,428,432,438,931,932,936,942
-- `(int64_t)(int32_t)a & b`-shaped units, all `&`/`bitand` with one
operand int32_t promoted to int64_t). ROOT CAUSE: z3's own simplify()
normal form does not only push NOT through AND/OR (De Morgan, already
handled by `_demorgan_operands`) -- it ALSO pushes NOT through CONCAT
(`~Concat(A,B) == Concat(~A,~B)`, a bit-exact identity: concatenation
only places bits side by side, so bitwise NOT commutes with it). For
these 12 units the sign-extension of `a` (VEX's own idiom: 33 copies
of bit 31 concatenated with `a` itself) sits INSIDE a De Morgan'd `|`
operand, and z3 already distributed the NOT of that operand through
the Concat, so `_demorgan_operands`'s check ("each operand of this
bvor is bvnot(X)") fails on that operand -- it is a `concat` node
whose CHILDREN are each `bvnot`-wrapped, not a `bvnot` node itself.
The old renderer falls through to the plain `bvnot` branch, which
recurses into the raw OR/concat tree and bit-serially reconstructs
the sign bit 33 times with `shr`/`and`/`not`/`shl`/`or` -- a giant,
correct-looking-but-DISPROVED mess (60+ instructions; the concat's
own "all_sign_extend" recognizer, which would have rendered one clean
`movslq`, never gets a chance to see the pattern because it is buried
under per-part negations). THE FIX: `_negate_of()`, a small helper
that recognizes TWO shapes as "the un-negated value of this node is
materializable": a bare `bvnot(X)` (return X, the old behaviour), OR
a `concat` node whose every child is `bvnot`-wrapped (return the
freshly-built `Concat` of the un-negated children -- the identity
above, run in reverse). `_demorgan_operands` is generalized to call
`_negate_of` on each operand instead of its old inline `bvnot`-only
check; once the sign-extend concat is recognized as "the un-negated
side" of the OR, the existing De Morgan fold fires.

A SECOND, closely related gap surfaced once (b) got this far: the
existing all-sign-extend concat recognizer (unchanged in shape,
carried into gen11 verbatim) still did not fire on the reconstructed
concat, because its trailing part here is `Extract(31,0,atom_1)` (a
low-half extract of the WIDER 64-bit leaf VEX records for this input,
`sx64(ex32@0(in0:64))` -- "sign-extend the low 32 bits of a 64-bit-
recorded input", not "sign-extend a native 32-bit leaf"), while every
sign-bit-replicate part names `atom_1` (the leaf) directly, not that
Extract node -- the OLD check compared each sign-bit part's operand
to `last` AS A WHOLE NODE, which only matches the bare-leaf case. THE
FIX: when `last` is itself a from-bit-0 Extract, compare against
`last`'s own base (`last.children()[0]`) instead of `last`. With both
halves of (b) in place the whole expression renders as one `movslq`:
`movslq %edi,%rax; and %rsi,%rax; ret` -- literally the unit's own
real ship code (canon4's `mnem`), verified for all 12 target units.

Both fixes are LOCAL to gen7()'s `if` and `bvnot` branches; nothing
about the ALU fold, shift, extract, or general concat logic changes,
and the mandatory ground-truth gate (canon8_behaviour_check's
anchored_check via canon9's flag-aware Sim9) is still the sole
acceptance rule for every candidate this file produces -- a wrong
candidate is refused, never shipped, exactly as before.

DEEP-DISPATCH FIX (added when Stage 4 (canon13_render.py) needed it,
diagnosed live): `gen11`'s own recursive calls originally read
literally as `gen11(child, ...)` -- fine for THIS file alone, but it
means a later layer (canon12_render.gen12, canon13_render.gen13),
reached only by falling through gen11's OWN dispatch for a node type
gen11 itself handles (concat, shift, extract, the general ALU fold),
would never get a chance to see a node NESTED inside one of those --
observed concretely on c/op_551 (Stage 4's own compound-and/or-
condition shape wrapped in an outer `Concat`; canon13's gen13 never
saw the inner `If(And(...),...)` node at all, because gen11's concat
fold recursed into it via the literal name `gen11`, not the current
monkeypatch). THE FIX: every one of gen11's own internal recursive
call sites now reads `R7.gen7(child, ...)` instead of `gen11(child,
...)` -- the SAME late-binding trick `_gen_alu` (canon7_render.py's
own function, reused unmodified here) already relies on, just applied
one level deeper. `R7.gen7` always names whichever stage is CURRENTLY
the topmost monkeypatch, so a node buried inside a concat/shift/ALU
fold now reaches Stage 4's (or a future Stage 5's) own rule exactly as
if it were the tree's own root. Semantically inert for every node type
that has no deeper stage rule (`R7.gen7` bottoms out at gen11 itself
again once no more specific layer wants the node) -- this is ordinary
structural recursion on strictly smaller subtrees, not a cycle.

THE SPELLING BAN: unchanged -- this file renders one unit at a time,
keyed by nothing but (lang, n); no grouping, no pairing, no operator-
token key anywhere in its output.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon7_render as R7                                     # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
Context = R7.Context
NoTemps = R7.NoTemps
Unsupported = R7.Unsupported
CallAtom = R7.CallAtom
round_up_width = R7.round_up_width
mask_value = R7.mask_value
NATIVE_WIDTHS = R7.NATIVE_WIDTHS
decode_bool_condition = R7.decode_bool_condition
as_immediate = R7.as_immediate
_signed_of = R7._signed_of
NEGATE_SUFFIX = R7.NEGATE_SUFFIX
ALU_OP = R7.ALU_OP
emit_move_leaf_or_imm = R7.emit_move_leaf_or_imm
emit_alu_source = R7.emit_alu_source
_ensure_native_write = R7._ensure_native_write
_gen_alu = R7._gen_alu


# --------------------------------------------------------------------
# FIX (b)'s helper.  See file header for the identity this relies on.
# --------------------------------------------------------------------

def _negate_of(node):
    """If `node` denotes bvnot(X) for some X this can materialize,
    return that X (a fresh z3 node); else None. Two recognized
    shapes: `node` is literally `bvnot(X)` (the old, only, case --
    return X unchanged); `node` is `concat(bvnot(A), bvnot(B), ...)`
    -- z3's own normal form distributing NOT through concat, bit-
    exactly reversible because concatenation only places bits, so
    NOT of the whole equals concat of NOT of each part -- return the
    reconstructed `Concat(A, B, ...)`."""
    name = node.decl().name()
    if name == "bvnot":
        return node.children()[0]
    if name == "concat":
        parts = node.children()
        unnegated = []
        for p in parts:
            if p.decl().name() != "bvnot":
                return None
            unnegated.append(p.children()[0])
        if len(unnegated) == 1:
            return unnegated[0]
        # z3.Concat()'s own CONSTRUCTOR nests binary
        # (concat(concat(concat(...),X),Y) -- 2 children at the top,
        # not the FLAT n-ary form z3's simplify() normal form always
        # hands gen11's "concat" branch elsewhere (measured: 33 flat
        # children vs 2 nested, for this exact 12-unit shape) --
        # simplify() immediately after construction re-flattens it
        # (a no-op semantically, `simplify(Concat(a,b,c))` denotes the
        # identical value either way; verified: 33 flat children,
        # same order, after this call) so the all-sign-extend
        # recognizer below sees the shape it already knows how to
        # read, instead of a spuriously-nested non-sign-extend-
        # looking one.
        return z3.simplify(z3.Concat(*unnegated))
    return None


def _demorgan_operands(node, outer_name):
    """canon7_render._demorgan_operands, generalized (FIX (b)): each
    operand of this `outer_name` (bvor/bvand) node must denote a
    negation we can materialize -- via `_negate_of`, not a bare
    bvnot-only check -- for the fold to apply."""
    if node.decl().name() != outer_name:
        return None
    kids = node.children()
    operands = []
    for k in kids:
        u = _negate_of(k)
        if u is None:
            return None
        operands.append(u)
    return operands


# --------------------------------------------------------------------
# gen11(): canon7_render.gen7, byte-for-byte, except the two marked
# sites (FIX (a) in the `if` branch, FIX (b) via the local
# _demorgan_operands above already wired into the `bvnot` branch).
# --------------------------------------------------------------------

def gen11(node, dest_base, ctx, lines, prov):
    if z3.is_bv_value(node):
        w = round_up_width(node.size())
        emit_move_leaf_or_imm(
            lines, ("imm", node.as_long(), w), dest_base, w, ctx)
        return w

    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, key = prov[name]
        if kind == "call":
            raise CallAtom(name, key)
        w = node.size()
        if key.startswith("in0"):
            ctx.note_operand("a", w)
            emit_move_leaf_or_imm(
                lines, ("leaf", "a", w), dest_base, w, ctx)
        elif key.startswith("in1"):
            ctx.note_operand("b", w)
            emit_move_leaf_or_imm(
                lines, ("leaf", "b", w), dest_base, w, ctx)
        else:
            import re
            m = re.match(r"^-?\d+:(\d+)$", key)
            if not m:
                raise Unsupported(
                    "leaf atom %r is neither an input (in0/in1) "
                    "nor a recognizable immediate literal" % key)
            v = int(key.split(":")[0])
            emit_move_leaf_or_imm(
                lines, ("imm", v, w), dest_base, w, ctx)
        return w

    op = node.decl().name()
    args = node.children()

    if op == "bvnot":
        inner = args[0]
        # FIX (b): _demorgan_operands (this module's generalized
        # version) now also recognizes a concat-of-all-bvnot operand,
        # so the sign-extend-under-negation shape folds correctly.
        and_operands = _demorgan_operands(inner, "bvor")
        if and_operands is not None and len(and_operands) >= 2:
            return _gen_alu(
                "bvand", and_operands, dest_base, ctx, lines, prov)
        or_operands = _demorgan_operands(inner, "bvand")
        if or_operands is not None and len(or_operands) >= 2:
            return _gen_alu(
                "bvor", or_operands, dest_base, ctx, lines, prov)
        w = R7.gen7(args[0], dest_base, ctx, lines, prov)
        lines.append("not %s" % reg_text(dest_base, round_up_width(w)))
        return w

    if op == "if":
        cond_node, then_v, else_v = args
        suf, L, R = decode_bool_condition(cond_node)
        w = node.size()
        native_w = round_up_width(w)
        is_bool_data = (
            z3.is_bv_value(then_v) and z3.is_bv_value(else_v) and
            then_v.size() == else_v.size() and
            set([then_v.as_long(), else_v.as_long()]) == set([0, 1]))
        if is_bool_data:
            tL = ctx.alloc()
            # FIX (a): use the width gen11() ACTUALLY established for
            # L, not L.size() (the z3 node's own static/padded size
            # -- stale whenever L is a zero-extend-by-concat wrapper
            # around a narrower field, THE CONCAT BUG FIX's own
            # return-width contract, ignored here before this fix).
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
            if native_w > 8:
                lines.append("mov $0,%s" % reg_text(dest_base, native_w))
            real_suf = suf if then_v.as_long() == 1 else \
                NEGATE_SUFFIX[suf]
            lines.append("set%s %s" % (real_suf, reg_text(dest_base, 8)))
            ctx.release(tL)
            return w
        R7.gen7(else_v, dest_base, ctx, lines, prov)
        t2 = ctx.alloc()
        R7.gen7(then_v, t2, ctx, lines, prov)
        tL = ctx.alloc()
        # FIX (a), same shape, applied to the cmov (non-boolean-data)
        # branch too -- same stale-width cause, same fix.
        Lw_actual = R7.gen7(L, tL, ctx, lines, prov)
        Lw = round_up_width(Lw_actual)
        r_imm = as_immediate(R, prov)
        if r_imm is not None:
            lines.append("cmp $%d,%s" % (
                _signed_of(r_imm, Lw), reg_text(tL, Lw)))
        else:
            tR = ctx.alloc()
            R7.gen7(R, tR, ctx, lines, prov)
            lines.append("cmp %s,%s" % (reg_text(tR, Lw), reg_text(tL, Lw)))
            ctx.release(tR)
        lines.append("cmov%s %s,%s" % (
            suf, reg_text(t2, native_w), reg_text(dest_base, native_w)))
        ctx.release(t2)
        ctx.release(tL)
        return w

    if op == "bvmul" and len(args) == 2:
        for i in (0, 1):
            if z3.is_bv_value(args[i]) and \
                    args[i].as_long() == (1 << args[i].size()) - 1:
                other = args[1 - i]
                w = R7.gen7(other, dest_base, ctx, lines, prov)
                lines.append("neg %s" % reg_text(dest_base,
                                                   round_up_width(w)))
                return w

    if op in ALU_OP:
        return _gen_alu(op, list(args), dest_base, ctx, lines, prov)

    if op in ("bvshl", "bvlshr", "bvashr"):
        val_node, amt_node = args[0], args[1]
        w = val_node.size()
        native_w = round_up_width(w)
        R7.gen7(val_node, dest_base, ctx, lines, prov)
        mnem = {"bvshl": "shl", "bvlshr": "shr",
                "bvashr": "sar"}[op]
        if z3.is_bv_value(amt_node):
            amt = amt_node.as_long()
            lines.append("%s $%d,%s" % (
                mnem, amt, reg_text(dest_base, native_w)))
        else:
            t = ctx.alloc()
            R7.gen7(amt_node, t, ctx, lines, prov)
            lines.append("mov %s,%%cl" % reg_text(t, 8))
            ctx.pins.add("rcx")
            lines.append("%s %%cl,%s" % (
                mnem, reg_text(dest_base, native_w)))
            ctx.release(t)
        return w

    if op == "extract":
        hi, lo = node.params()
        w = hi - lo + 1
        src_w = args[0].size()
        R7.gen7(args[0], dest_base, ctx, lines, prov)
        cur_w = round_up_width(src_w)
        if lo > 0:
            lines.append("shr $%d,%s" % (
                lo, reg_text(dest_base, cur_w)))
        target_native = round_up_width(w)
        if target_native != cur_w or w not in NATIVE_WIDTHS:
            # unchanged from canon7_render.gen7 -- see that file's own
            # "THE EXTRACT MASK" comment for the full account of why
            # this condition is exactly right and was already proven
            # so (c/op_138 vs c/op_113) before this file existed.
            mask = mask_value(w)
            emit_alu_source(
                lines, ("imm", mask, target_native), "and",
                dest_base, target_native, ctx)
        return w

    if op == "concat":
        parts = list(node.children())
        total_w = node.size()
        last = parts[-1]
        if len(parts) >= 2:
            all_sign_extend = True
            # FIX (b), second half: the sign-bit-replicate parts name
            # their SOURCE register directly (e.g. `Extract(31,31,
            # atom_1)`, atom_1 the raw 64-bit leaf) even when `last`
            # itself is `Extract(31,0,atom_1)` (a low-half extract of
            # that SAME wider leaf, not the bare leaf) -- VEX's own
            # "sign-extend the low 32 bits of a 64-bit-recorded input"
            # idiom (measured: c/427, sx64(ex32@0(in0:64))). The OLD
            # check compared each sign-bit extract's operand to `last`
            # AS A WHOLE NODE, which only matches when `last` IS the
            # bare leaf -- failing here because `last` is itself an
            # Extract wrapping that leaf, not the leaf. Generalized:
            # compare against `last`'s OWN base (`last.children()[0]`)
            # whenever `last` is itself a from-bit-0 Extract; otherwise
            # unchanged (`last` itself, the old, only, case).
            if last.decl().kind() == z3.Z3_OP_EXTRACT:
                last_hi, last_lo = last.params()
                sign_source = last.children()[0] if last_lo == 0 \
                    else None
            else:
                sign_source = last
            if sign_source is None:
                all_sign_extend = False
            for p in (parts[:-1] if all_sign_extend else []):
                if not (p.decl().kind() == z3.Z3_OP_EXTRACT):
                    all_sign_extend = False
                    break
                hip, lop = p.params()
                if hip != lop:
                    all_sign_extend = False
                    break
                if not p.children()[0].eq(sign_source):
                    all_sign_extend = False
                    break
                if hip != last.size() - 1:
                    all_sign_extend = False
                    break
            if all_sign_extend:
                src_w = last.size()
                R7.gen7(last, dest_base, ctx, lines, prov)
                if src_w == 32 and total_w == 64:
                    lines.append(
                        "movsxd %s,%s" % (
                            reg_text(dest_base, 32),
                            reg_text(dest_base, 64)))
                elif total_w in NATIVE_WIDTHS and \
                        src_w in NATIVE_WIDTHS:
                    lines.append("movsx %s,%s" % (
                        reg_text(dest_base, src_w),
                        reg_text(dest_base, round_up_width(total_w))))
                else:
                    raise Unsupported(
                        "sign-extend concat from %d to %d bits "
                        "has no native movsx form" % (src_w, total_w))
                return total_w
        if len(parts) == 2 and z3.is_bv_value(parts[0]) and \
                parts[0].as_long() == 0:
            w = R7.gen7(parts[1], dest_base, ctx, lines, prov)
            return w
        acc_w = R7.gen7(parts[0], dest_base, ctx, lines, prov)
        for nxt in parts[1:]:
            nxt_w = nxt.size()
            new_w = acc_w + nxt_w
            native_new = round_up_width(new_w)
            _ensure_native_write(
                dest_base, round_up_width(acc_w), native_new, lines)
            lines.append("shl $%d,%s" % (
                nxt_w, reg_text(dest_base, native_new)))
            t = ctx.alloc()
            t_w = R7.gen7(nxt, t, ctx, lines, prov)
            _ensure_native_write(t, round_up_width(t_w), native_new, lines)
            lines.append("or %s,%s" % (
                reg_text(t, native_new),
                reg_text(dest_base, native_new)))
            ctx.release(t)
            acc_w = new_w
        return total_w

    raise Unsupported("no rendering rule for z3 op %r" % op)


# --------------------------------------------------------------------
# THE MONKEYPATCH.  canon7_render.py's own file is never edited; this
# one assignment makes every caller inside that module (render_unit7,
# render_block_value7, render_branching_unit7, and gen7's own helper
# _gen_alu) resolve their bare `gen7(...)` calls to gen11 instead,
# because Python looks up a function's free variables in its
# `__globals__` dict (the DEFINING module's namespace) AT CALL TIME,
# not at definition time -- reassigning canon7_render.gen7 mutates
# that same dict every one of those functions already reads from.
# --------------------------------------------------------------------

R7.gen7 = gen11

render_unit11 = R7.render_unit7
render_block_value11 = R7.render_block_value7
render_branching_unit11 = R7.render_branching_unit7
