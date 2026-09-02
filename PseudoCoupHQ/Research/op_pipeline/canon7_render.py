#!/usr/bin/env python3
"""canon7_render.py -- THE RETURN PATH, WITH ITS CONTEXT.

Companion to canon7.py.  This file is expr_to_canon.py's renderer
(imported here as `EC0`, REUSED for every piece that does not touch a
register table or a width decision), with the context-record fix
the owner's diagnosis names: THE EXPRESSION TRAVELS WITHOUT ITS CONTEXT, so
the return path guesses. Every measured canon5/canon6 renderer defect
this lap found is the same root cause wearing a different mnemonic:

  * an operand's real width (64 bits) silently dropped to 32 -- a
    stale canon6 snapshot (fixed already upstream, see canon7.py's
    own header; not reproduced by the current expr_to_canon.py, kept
    here as a live regression test via the behaviour gate) --
  * an 8/16-bit ANSWER treated as if it were already a clean 32/64-bit
    register value, when only a 32-bit x86-64 write actually
    auto-zero-extends (an 8/16-bit write does not) -- THE CONCAT BUG
    below,
  * "the two available temp registers" -- an invented cap AgentMemory
    has already struck; the pool must be ORDERED, not SIZED,
  * hardware-pinned registers (%cl for a variable shift count) not
    recorded anywhere for a report to point at.

THE CONTEXT RECORD (this file's fix, `Context`, formerly `Pool`):
travels through every gen7() call for one unit and is read back, not
re-derived, at the point the answer is finished:

    operand_widths   {'a': int|None, 'b': int|None} -- the NATIVE
                     width this unit's own leaf atoms declared for
                     each traced operand (leaf_width() of the raw VEX
                     leaf text, e.g. "in0:64" -> 64), recorded the
                     first time gen7() renders that operand, never
                     re-guessed afterward.
    pins             set of hardware-pinned register bases this
                     unit's own shape required (e.g. "rcx" -- a
                     variable-count shift's %cl).
    pool_order       ["r10","r11","r9","r8","rbx","r12","r13","r14",
                     "r15"] -- the owner's 2026-08-28 ruling ("TEMP
                     REGISTERS ARE STANDARDIZED, NOT LIMITED"): a
                     FIXED ORDER, not a fixed SIZE.  alloc() always
                     hands out the LOWEST-ORDER currently-free member;
                     release() returns it to the pool and re-sorts by
                     that same order -- so the SAME nesting shape
                     always assigns the SAME registers across units,
                     which is what makes two units' rendered text
                     comparable at all ("the order is what makes
                     units match").  callee_saved_used records, in
                     first-use order, which of %rbx/%r12../%r15 this
                     unit actually needed, so the driver can wrap the
                     unit in exactly the push/pop pairs required.
    answer           filled once gen7() finishes the top-level value:
                     {'value_width': <bits gen7() actually wrote>,
                      'native_register_width': <32 or 64 -- the width
                          the FINISHED answer is clean at>,
                      'convention': 'native-32'|'native-64'|
                          'zero-extended-from-8'|'zero-extended-
                          from-16'}. THE RULE THIS RECORD ENFORCES:
                      only a 32-bit x86-64 write auto-zero-extends to
                      fill the upper 32 bits of the 64-bit register;
                      an 8- or 16-bit write does not touch them at
                      all.  So an 8/16-bit answer is ALWAYS finished
                      with one explicit movzx into the 32-bit answer
                      register before `ret` -- the exact shape the
                      corpus's own real compiler output already uses
                      (c/op_5: `xor $0x1,%dil; movzbl %dil,%eax;
                      ret`) -- rather than either refusing (canon5/
                      canon6: "final answer width 8 bits has no
                      native x86-64 return register form") or, worse,
                      silently trusting the upper bits were already
                      clean when they were not (see THE CONCAT BUG).

THE CONCAT BUG (found here, fixed here, "fix a cause at first
observation"). expr_to_canon.py's own "zero-extend-by-one-part"
concat case -- the shape z3 uses to wrap an 8/16/32-bit computed value
up to VEX's 64-bit temp convention, `Concat(0-literal, X)` -- rendered
X into the destination register at X's own width, then `return
total_w` (64), CLAIMING the full 64 bits were now clean.  That claim
is true only when X's width is 32 (the one case x86-64 auto-extends
for free); for an 8- or 16-bit X it is false -- the upper bits are
whatever garbage was already in the register.  The old code's own
comment even said so in general ("the narrower write already
zero-extends on x86-64"), overgeneralizing the 32-bit case to all
cases.  Measured effect: c/op_5 (`!a`, a bool `Xor8`-then-Concat-with-
zero) rendered as a correct-answer-but-unproven-clean-upper-bits
8-bit computation with no finishing instruction, then render_unit's
own tail check saw a claimed-64-bit answer and shipped it as-is.  THE
FIX is one line: return the width gen7() ACTUALLY wrote (`w`), not
the concat's own total width.  Combined with the answer-record fix
above, the SAME single finishing step (movzx into the 32-bit answer
register) now fires correctly wherever it is needed -- nested or
top-level -- instead of a special case per call site.

THE EXTRACT MASK -- TRIED AS A VERBOSITY FIX, REVERTED, recorded
honestly per the evidence doctrine ("refuse honestly rather than
fabricate").  An early version of this file dropped `extract`'s
`and $mask,...` instruction whenever the extracted field's width was
already a native register width, reasoning that %eax always IS the
low 32 bits of %rax so no instruction should be needed.  That is true
for the ONE call site that reads the result back at that SAME narrow
alias (verified: c/op_138, `a - b` at i32, 6 lines -> 4, PROVED_EQUAL)
-- but it is not the only call site.  `_gen_alu`'s ALU-fold loop reads
a nested operand's rendered temp at the ENCLOSING operation's own
native width, not at the width the nested render actually returned.
Measured counterexample found by this lap's own mandatory zero-
regression sweep: c/op_113 (`a + (int64_t)(int32_t)b`) -- the extract
is 32-bit but the enclosing add is 64-bit; dropping the mask left the
temp's upper 32 bits as live garbage from the preceding 64-bit `mov`,
and the 64-bit `add` read all of it. DISPROVED by the behaviour gate;
ground truth confirmed canon5's old text was right. THE ACTUAL JOB
this mask does, once seen: on real x86-64 a 32-bit WRITE (which
`and $mask,%r11d` is) for-free clears bits 32-63 of the parent 64-bit
register -- an invariant every OTHER gen7() branch maintains by
construction, that this one broke by skipping its own write.
REVERTED to expr_to_canon.py's original condition exactly
(`target_native != cur_w or w not in NATIVE_WIDTHS`); see gen7()'s
own comment at the `extract` case for the full account. Reported here
because the owner's evidence doctrine requires an agent to show a wrong
turn it caught and undid, not just the turns that worked.

THE DE MORGAN FOLD (verbosity survey, item 4).  z3's own simplify()
normal form for AND/OR is a De Morgan bvnot/bvor (resp. bvnot/bvand)
chain (expr_to_canon.py's own header already names this fact for
subtraction/negation; the same rewrite hits conjunction/disjunction).
Un-fixed, `b & 31` (c/op_678's shift count) rendered as three `not`s
and an `or` instead of one `and`.  THE FIX: `_demorgan_operands()`
recognizes `bvnot(bvor(bvnot(X),bvnot(Y),...))` as `X & Y & ...` and
`bvnot(bvand(bvnot(X),bvnot(Y),...))` as `X | Y | ...` -- a bit-exact
identity (De Morgan's law), so this changes only which instruction
gen7() picks, never what is proved equal.  Before/after, c/op_678
(`a << (b & 31)`, the AND-count sub-expression only): old
`mov $31,%r11b; not %r11b; mov %rsi,%r10; and $255,%r10b; not %r10b;
or %r10b,%r11b; not %r11b` (7 lines) -> new `mov $31,%r11b;
mov %rsi,%r10; and $255,%r10b; and %r10b,%r11b` (4 lines, verified
PROVED_EQUAL).

NEGATION (task's own headline example, c/op_13, `-a`): ALREADY FIXED
upstream in expr_to_canon.py (the "STEP 7" comments in gen()'s
bvmul/bvadd handling) -- verified empirically before writing this
file: the CURRENT expr_to_canon.py already renders c/op_13 as
`mov %rdi,%rax; neg %rax; ret`, never the four-instruction
multiply-by-minus-one form the task quotes.  Carried forward
unchanged (this file reuses EC0's bvmul/bvadd STEP 7 logic via the
shared `_gen_alu` fold, itself a straight port of EC0's ALU_OP body).

THE SPELLING BAN: unchanged from expr_to_canon.py -- keyed by z3
operator/opcode name, never a source-language token; renders one unit
at a time, no grouping or pairing.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import expr_to_canon as EC0                                   # noqa: E402
import z3                                                      # noqa: E402

parse_expr = EC0.parse_expr
serialize = EC0.serialize
leaf_width = EC0.leaf_width
to_z3_with_prov = EC0.to_z3_with_prov
CallAtom = EC0.CallAtom
call_op_name = EC0.call_op_name
DIVMOD_SCALAR = EC0.DIVMOD_SCALAR
refusal_reason_for_call = EC0.refusal_reason_for_call
canon2_derived_text = EC0.canon2_derived_text
_is_trivial_wrapper_of_one_atom = EC0._is_trivial_wrapper_of_one_atom
assemble_and_disassemble = EC0.assemble_and_disassemble
round_up_width = EC0.round_up_width
mask_value = EC0.mask_value
imm_fits_32 = EC0.imm_fits_32
NATIVE_WIDTHS = EC0.NATIVE_WIDTHS
decode_bool_condition = EC0.decode_bool_condition
as_immediate = EC0.as_immediate
_signed_of = EC0._signed_of
NEGATE_SUFFIX = EC0.NEGATE_SUFFIX
ALU_OP = EC0.ALU_OP


class NoTemps(Exception):
    pass


class Unsupported(Exception):
    pass


# --------------------------------------------------------------------
# THE EXTENDED REGISTER TABLE (context record's entry-contract/pool
# fields draw from this).  a/b/ans/cl unchanged from EC0.REGMAP; r10/
# r11 unchanged; r9/r8 added (caller-saved, no save/restore needed --
# real x86-64 SysV scratch registers, same as r10/r11); rbx/r12/r13/
# r14/r15 added as the CALLEE-SAVED overflow tier (the owner's ruling:
# "as many as the unit needs; standardized stack slots only after the
# pool is exhausted" -- callee-saved-with-save/restore is exhausted
# BEFORE stack slots, and this corpus's measured nesting never needed
# stack slots -- see canon7.py's report).
# --------------------------------------------------------------------

REGMAP = dict(EC0.REGMAP)
REGMAP["r9"] = {64: "%r9", 32: "%r9d", 16: "%r9w", 8: "%r9b"}
REGMAP["r8"] = {64: "%r8", 32: "%r8d", 16: "%r8w", 8: "%r8b"}
REGMAP["rbx"] = {64: "%rbx", 32: "%ebx", 16: "%bx", 8: "%bl"}
REGMAP["r12"] = {64: "%r12", 32: "%r12d", 16: "%r12w", 8: "%r12b"}
REGMAP["r13"] = {64: "%r13", 32: "%r13d", 16: "%r13w", 8: "%r13b"}
REGMAP["r14"] = {64: "%r14", 32: "%r14d", 16: "%r14w", 8: "%r14b"}
REGMAP["r15"] = {64: "%r15", 32: "%r15d", 16: "%r15w", 8: "%r15b"}

TEMP_POOL_ORDER = ["r10", "r11", "r9", "r8",
                    "rbx", "r12", "r13", "r14", "r15"]
CALLEE_SAVED = set(["rbx", "r12", "r13", "r14", "r15"])


def reg_text(base, width):
    table = REGMAP[base]
    if width not in table:
        raise Unsupported("register base %r has no %d-bit form"
                           % (base, width))
    return table[width]


# --------------------------------------------------------------------
# THE CONTEXT RECORD.  See file header.  Exposes the same alloc()/
# release() interface EC0's Pool did (gen7() below is otherwise a
# straight port of EC0.gen()), plus the bookkeeping fields that let
# canon7.py's driver report what travelled.
# --------------------------------------------------------------------

class Context(object):
    def __init__(self):
        self.order = list(TEMP_POOL_ORDER)
        self.free = list(TEMP_POOL_ORDER)
        self.callee_saved_used = []
        self.operand_widths = {}
        self.pins = set()
        self.answer = {}

    def alloc(self):
        if not self.free:
            raise NoTemps(
                "temp pool exhausted -- every register in the "
                "standardized ordered pool (%s) is already live in "
                "this unit's own expression nesting; stack-slot "
                "overflow is not yet implemented"
                % ",".join(self.order))
        base = self.free.pop(0)
        if base in CALLEE_SAVED and base not in self.callee_saved_used:
            self.callee_saved_used.append(base)
        return base

    def release(self, base):
        if base in self.order and base not in self.free:
            self.free.append(base)
            self.free.sort(key=self.order.index)

    def note_operand(self, which, width):
        if self.operand_widths.get(which) is None:
            self.operand_widths[which] = width

    def to_dict(self):
        return {
            "operand_widths": dict(self.operand_widths),
            "hardware_pins": sorted(self.pins),
            "temp_pool_order": list(self.order),
            "callee_saved_used": list(self.callee_saved_used),
            "answer": dict(self.answer),
        }


# --------------------------------------------------------------------
# local ports of EC0's width-aware emitters, register-table-extended.
# --------------------------------------------------------------------

def emit_move_leaf_or_imm(lines, val, dest_base, dest_width, ctx):
    kind = val[0]
    if kind == "leaf":
        src_base, src_w = val[1], val[2]
        if src_w == dest_width:
            lines.append("mov %s,%s" % (reg_text(src_base, src_w),
                                         reg_text(dest_base,
                                                   dest_width)))
        elif src_w < dest_width:
            lines.append("movzx %s,%s" % (
                reg_text(src_base, src_w),
                reg_text(dest_base, dest_width)))
        else:
            lines.append("mov %s,%s" % (
                reg_text(src_base, dest_width),
                reg_text(dest_base, dest_width)))
    else:
        v = val[1] & mask_value(dest_width)
        if v >= 2 ** (dest_width - 1):
            signed = v - (1 << dest_width)
        else:
            signed = v
        if dest_width == 64 and not imm_fits_32(signed, 64):
            lines.append("movabs $%d,%s" % (
                signed, reg_text(dest_base, dest_width)))
        else:
            lines.append("mov $%d,%s" % (
                signed, reg_text(dest_base, dest_width)))


def emit_alu_source(lines, val, op_mnem, dest_base, dest_width, ctx):
    kind = val[0]
    if kind == "imm":
        v = val[1] & mask_value(dest_width)
        if v >= 2 ** (dest_width - 1):
            signed = v - (1 << dest_width)
        else:
            signed = v
        if dest_width == 64 and not imm_fits_32(signed, 64):
            t = ctx.alloc()
            lines.append("movabs $%d,%s" % (
                signed, reg_text(t, dest_width)))
            lines.append("%s %s,%s" % (
                op_mnem, reg_text(t, dest_width),
                reg_text(dest_base, dest_width)))
            ctx.release(t)
        else:
            lines.append("%s $%d,%s" % (
                op_mnem, signed, reg_text(dest_base, dest_width)))
        return
    src_base, src_w = val[1], val[2]
    if src_w != dest_width:
        raise Unsupported("operand width %d does not match "
                           "destination width %d for op %s"
                           % (src_w, dest_width, op_mnem))
    lines.append("%s %s,%s" % (op_mnem, reg_text(src_base, src_w),
                                reg_text(dest_base, dest_width)))


# --------------------------------------------------------------------
# De Morgan recognizer (RENDERING ONLY -- see file header).
# --------------------------------------------------------------------

def _demorgan_operands(node, outer_name):
    if node.decl().name() != outer_name:
        return None
    kids = node.children()
    operands = []
    for k in kids:
        if k.decl().name() != "bvnot":
            return None
        operands.append(k.children()[0])
    return operands


# --------------------------------------------------------------------
# THE WIDTH-CONSUMER FIX (found alongside the reverted extract change,
# same root cause, general form): ANY call site that renders a value
# into a temp via gen7() and then reads that temp back at a WIDER
# native width than gen7() actually returned must explicitly widen it
# first -- gen7()'s contract ("the value is established clean up to
# round_up_width(returned width)") does not extend itself to a wider
# width for free, except x86-64's own one real exception (a 32-bit
# write auto zero-extends its parent 64-bit register). Factored once,
# used at every consumption point (`_gen_alu`'s fold loop, the general
# multi-part concat loop) instead of re-deriving the same rule ad hoc
# per call site -- the ad hoc version is exactly what the extract
# mask's earlier, reverted "fix" got wrong.
# --------------------------------------------------------------------

def _ensure_native_write(reg_base, cur_native_w, target_native_w, lines):
    if cur_native_w == target_native_w:
        return target_native_w
    if cur_native_w == 32 and target_native_w == 64:
        # x86-64's own free case: a 32-bit write already zero-extends
        # the parent 64-bit register; GAS's movzx has no 32->64 form
        # to even ask for (it would be redundant), so emitting nothing
        # here is correct, not an optimization risk.
        return target_native_w
    lines.append("movzx %s,%s" % (
        reg_text(reg_base, cur_native_w),
        reg_text(reg_base, target_native_w)))
    return target_native_w


# --------------------------------------------------------------------
# shared ALU fold -- ports EC0.gen()'s `if op in ALU_OP:` body
# (including its STEP 7 zero-elision/neg-detection fixes, unchanged),
# factored so the De Morgan un-expansion can reuse it on a synthesized
# operand list instead of a real z3 node.
# --------------------------------------------------------------------

def _gen_alu(op, args, dest_base, ctx, lines, prov):
    w = args[0].size()
    native_w = round_up_width(w)
    mnem = ALU_OP[op]
    if op == "bvadd" and len(args) >= 2:
        keep = [a for a in args if as_immediate(a, prov) != 0]
        if keep and len(keep) < len(args):
            args = keep
    w0 = gen7(args[0], dest_base, ctx, lines, prov)
    _ensure_native_write(dest_base, round_up_width(w0), native_w, lines)
    for extra in args[1:]:
        neg_operand = None
        if op == "bvadd" and extra.decl().name() == "bvmul" and \
                len(extra.children()) == 2:
            m0, m1 = extra.children()
            if z3.is_bv_value(m0) and \
                    m0.as_long() == (1 << m0.size()) - 1:
                neg_operand = m1
            elif z3.is_bv_value(m1) and \
                    m1.as_long() == (1 << m1.size()) - 1:
                neg_operand = m0
        if neg_operand is not None:
            t = ctx.alloc()
            t_w = gen7(neg_operand, t, ctx, lines, prov)
            _ensure_native_write(t, round_up_width(t_w), native_w, lines)
            emit_alu_source(
                lines, ("leaf", t, native_w), "sub", dest_base,
                native_w, ctx)
            ctx.release(t)
        elif z3.is_bv_value(extra):
            emit_alu_source(
                lines, ("imm", extra.as_long(), native_w), mnem,
                dest_base, native_w, ctx)
        else:
            t = ctx.alloc()
            t_w = gen7(extra, t, ctx, lines, prov)
            _ensure_native_write(t, round_up_width(t_w), native_w, lines)
            emit_alu_source(
                lines, ("leaf", t, native_w), mnem, dest_base,
                native_w, ctx)
            ctx.release(t)
    return w


# --------------------------------------------------------------------
# gen7(): EC0.gen(), ported to the Context/reg_text/emit_* above, plus
# the three fixes (De Morgan fold, extract mask, concat honest width).
# Every OTHER branch (if/select CAUSE1, shifts, sign-extend concat,
# general concat) is EC0.gen()'s own logic, unchanged in shape.
# --------------------------------------------------------------------

def gen7(node, dest_base, ctx, lines, prov):
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
        and_operands = _demorgan_operands(inner, "bvor")
        if and_operands is not None and len(and_operands) >= 2:
            return _gen_alu(
                "bvand", and_operands, dest_base, ctx, lines, prov)
        or_operands = _demorgan_operands(inner, "bvand")
        if or_operands is not None and len(or_operands) >= 2:
            return _gen_alu(
                "bvor", or_operands, dest_base, ctx, lines, prov)
        w = gen7(args[0], dest_base, ctx, lines, prov)
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
            gen7(L, tL, ctx, lines, prov)
            Lw = round_up_width(L.size())
            r_imm = as_immediate(R, prov)
            if r_imm is not None:
                lines.append("cmp $%d,%s" % (
                    _signed_of(r_imm, Lw), reg_text(tL, Lw)))
            else:
                tR = ctx.alloc()
                gen7(R, tR, ctx, lines, prov)
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
        gen7(else_v, dest_base, ctx, lines, prov)
        t2 = ctx.alloc()
        gen7(then_v, t2, ctx, lines, prov)
        tL = ctx.alloc()
        gen7(L, tL, ctx, lines, prov)
        Lw = round_up_width(L.size())
        r_imm = as_immediate(R, prov)
        if r_imm is not None:
            lines.append("cmp $%d,%s" % (
                _signed_of(r_imm, Lw), reg_text(tL, Lw)))
        else:
            tR = ctx.alloc()
            gen7(R, tR, ctx, lines, prov)
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
                w = gen7(other, dest_base, ctx, lines, prov)
                lines.append("neg %s" % reg_text(dest_base,
                                                   round_up_width(w)))
                return w

    if op in ALU_OP:
        return _gen_alu(op, list(args), dest_base, ctx, lines, prov)

    if op in ("bvshl", "bvlshr", "bvashr"):
        val_node, amt_node = args[0], args[1]
        w = val_node.size()
        native_w = round_up_width(w)
        gen7(val_node, dest_base, ctx, lines, prov)
        mnem = {"bvshl": "shl", "bvlshr": "shr",
                "bvashr": "sar"}[op]
        if z3.is_bv_value(amt_node):
            amt = amt_node.as_long()
            lines.append("%s $%d,%s" % (
                mnem, amt, reg_text(dest_base, native_w)))
        else:
            t = ctx.alloc()
            gen7(amt_node, t, ctx, lines, prov)
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
        gen7(args[0], dest_base, ctx, lines, prov)
        cur_w = round_up_width(src_w)
        if lo > 0:
            lines.append("shr $%d,%s" % (
                lo, reg_text(dest_base, cur_w)))
        target_native = round_up_width(w)
        if target_native != cur_w or w not in NATIVE_WIDTHS:
            # NOTE (found and reverted during this lap's own
            # zero-regression sweep -- "fix a cause at first
            # observation"): an EARLIER version of this file dropped
            # this mask whenever `w` was already a native width,
            # reasoning that a narrower register-name alias already
            # reads the correct low bits with no instruction needed.
            # That reasoning is true for the ONE call site that reads
            # dest_base back at exactly this narrower alias -- but the
            # ALU-fold loop (`_gen_alu`) that consumes a nested
            # extract's rendered temp does NOT reliably do that: it
            # reads the temp at the OUTER operation's own native
            # width, whatever that is (measured counterexample:
            # c/op_113, `a + (i64)(i32)b` -- the extract's own width
            # is 32, but the enclosing bvadd is 64-bit, so dropping
            # this mask left %r10's upper 32 bits as live garbage
            # from the `mov %rsi,%r10` that preceded it, and the
            # 64-bit `add %r10,%rax` read all of it -- DISPROVED by
            # the behaviour gate, ground-truth-confirmed the OLD
            # (canon5) text was right). THE INVARIANT this mask
            # actually maintains, once you see it: gen7()'s contract
            # is "the value is established CLEAN up to
            # round_up_width(returned width)" -- and on real x86-64,
            # a 32-bit WRITE (which `and $mask,%r11d` is, even though
            # its own visible job is masking the low field) is the
            # thing that for-free clears bits 32-63 of the parent
            # 64-bit register. Skipping the write because "w is
            # already native" broke that invariant whenever the
            # source register's own prior width (cur_w) was WIDER
            # than the extracted field -- restored here, matching
            # expr_to_canon.py's original (proven-good, canon5)
            # condition exactly.
            # THE MASK-IMMEDIATE-WIDTH FIX (item 3, an assembler
            # failure found and fixed here): x86-64's `and` has no
            # register-with-64-bit-immediate encoding at all -- only
            # a 32-bit sign-extended immediate. A wide, non-native
            # extract (e.g. a 56-bit field) produces a mask like
            # 0x00ffffffffffffff, which does not fit; `as` refused it
            # ("operand type mismatch for `and'") every time this
            # branch was reached with such a field, ALWAYS -- this
            # was a real bug in the plain immediate form, not
            # something a diagnostic reads as need-more-evidence.
            # `emit_alu_source` already has the correct fallback
            # (movabs into a temp, then AND register-to-register) for
            # exactly this situation; reused here instead of a second
            # ad hoc immediate-fits check.
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
            for p in parts[:-1]:
                if not (p.decl().kind() == z3.Z3_OP_EXTRACT):
                    all_sign_extend = False
                    break
                hip, lop = p.params()
                if hip != lop:
                    all_sign_extend = False
                    break
                if not p.children()[0].eq(last):
                    all_sign_extend = False
                    break
                if hip != last.size() - 1:
                    all_sign_extend = False
                    break
            if all_sign_extend:
                src_w = last.size()
                gen7(last, dest_base, ctx, lines, prov)
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
            # THE CONCAT BUG FIX -- see file header. Return the width
            # gen7() ACTUALLY wrote, never the concat's own claimed
            # total width: only a 32-bit write auto zero-extends on
            # real x86-64, so claiming total_w here for an 8/16-bit
            # part would hide an unproven-clean upper half from every
            # caller, including render_unit7's own answer-finishing
            # step.
            w = gen7(parts[1], dest_base, ctx, lines, prov)
            return w
        acc_w = gen7(parts[0], dest_base, ctx, lines, prov)
        for nxt in parts[1:]:
            nxt_w = nxt.size()
            new_w = acc_w + nxt_w
            native_new = round_up_width(new_w)
            # THE WIDTH-CONSUMER FIX applied here too (same shape as
            # `_gen_alu`'s, see that helper's own comment): both the
            # running accumulator and the freshly-rendered next part
            # must be established clean at `native_new` -- via
            # `_ensure_native_write`, never a hand-written movzx
            # condition that silently mis-handles the free 32->64
            # case (GAS's movzx has no 32-bit-source form at all).
            _ensure_native_write(
                dest_base, round_up_width(acc_w), native_new, lines)
            lines.append("shl $%d,%s" % (
                nxt_w, reg_text(dest_base, native_new)))
            t = ctx.alloc()
            t_w = gen7(nxt, t, ctx, lines, prov)
            _ensure_native_write(t, round_up_width(t_w), native_new, lines)
            lines.append("or %s,%s" % (
                reg_text(t, native_new),
                reg_text(dest_base, native_new)))
            ctx.release(t)
            acc_w = new_w
        return total_w

    raise Unsupported("no rendering rule for z3 op %r" % op)


# --------------------------------------------------------------------
# render_unit7(): EC0.render_unit()'s driver, with the context record
# built and consulted, callee-saved push/pop wrapping, and the 8/16-
# bit answer FIX (item 2) replacing the old refusal.
# --------------------------------------------------------------------

def render_unit7(u, workdir):
    lang = u["lang"]
    n = u["n"]

    if u.get("sem_ok") is False:
        reason = u.get("refused") or "sem not ok"
        return "no return path: unit never reached a normal-path " \
            "root (%s)" % reason, None

    root_text = u.get("normal_path_root")
    if root_text is None:
        return "no return path: no return-bearing block with a " \
            "value (tree_match2's own normal_path_value found no " \
            "candidate)", None

    if not u.get("normalize_ok"):
        return "no return path: z3 failed to normalize this " \
            "unit's lifted expression (%s); the raw VEX text is " \
            "retained verbatim in normal_path_root/normal_path_raw " \
            "with no bitvector normal form to render from" % \
            u.get("normalize_note", "unknown z3 failure"), None

    raw = u.get("normal_path_raw")
    if raw is None:
        return "no return path: normalize_ok is true but " \
            "normal_path_raw is missing from this unit's record", None

    try:
        tree = parse_expr(raw)
    except Exception as exc:
        return "no return path: could not re-parse this unit's " \
            "own normal_path_raw text (%r)" % exc, None

    atoms = {}
    prov = {}
    try:
        expr = to_z3_with_prov(tree, atoms, prov)
        simplified = z3.simplify(expr)
    except Exception as exc:
        return "no return path: re-deriving the z3 expression from " \
            "normal_path_raw failed (%r) even though normalize_ok " \
            "was recorded true for it" % exc, None

    resim_text = str(simplified).replace("\n", " ").strip()
    stored_text = root_text
    if resim_text != stored_text:
        return "no return path: this renderer's own re-derivation " \
            "of the z3 normal form does not match the unit's own " \
            "stored normal_path_root text (stored=%r, rederived=%r) " \
            "-- refusing rather than rendering a different " \
            "expression than the one on record" % (
                stored_text, resim_text), None

    call_atoms = {}

    def find_calls(node, seen):
        if id(node) in seen:
            return
        seen.add(id(node))
        if z3.is_bv_value(node):
            return
        if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            name = node.decl().name()
            kind, key = prov[name]
            if kind == "call":
                call_atoms[name] = key
            return
        for c in node.children():
            find_calls(c, seen)

    find_calls(simplified, set())

    if call_atoms:
        if len(call_atoms) == 1:
            only_name = list(call_atoms.keys())[0]
            call_text = call_atoms[only_name]
            head = call_op_name(call_text)
            is_trivial_wrapper = _is_trivial_wrapper_of_one_atom(
                simplified, only_name, prov)
            if head in DIVMOD_SCALAR and is_trivial_wrapper:
                dt, err = canon2_derived_text(lang, n)
                if dt is None:
                    return "no return path: expression is the " \
                        "scalar divmod atom '%s' (%s) but %s" % (
                            head, call_text, err), None
                ok, out = assemble_and_disassemble(dt, workdir)
                if not ok:
                    return "no return path: this unit's own " \
                        "canon2 derived_text for the divmod atom " \
                        "failed to re-assemble here (%s)" % out, None
                return list(dt), None
            return refusal_reason_for_call(head), None
        names = sorted(call_atoms.keys())
        heads = sorted(set(call_op_name(call_atoms[nm])
                            for nm in names))
        return "no return path: expression contains %d distinct " \
            "uninterpreted atoms (%s) -- this renderer only traces " \
            "a SINGLE scalar-divmod atom back to instructions, via " \
            "that unit's own canon2 record" % (len(call_atoms),
                                                ", ".join(heads)), None

    ctx = Context()
    lines = []
    try:
        w = gen7(simplified, "ans", ctx, lines, prov)
    except CallAtom as ca:
        return refusal_reason_for_call(call_op_name(ca.call_text)), None
    except NoTemps as exc:
        return "no return path: %s" % exc, None
    except Unsupported as exc:
        return "no return path: %s" % exc, None
    except Exception as exc:
        return "no return path: codegen raised %r rendering %r" % (
            exc, resim_text), None

    native_w = round_up_width(w)
    if native_w in (8, 16):
        # THE 8/16-BIT ANSWER FIX (item 2) -- see file header and
        # Context.answer.  Finish with the corpus's own real
        # convention: zero-extend into the 32-bit answer register.
        lines.append("movzx %s,%s" % (
            reg_text("ans", native_w), reg_text("ans", 32)))
        ctx.answer = {
            "value_width": native_w,
            "native_register_width": 32,
            "convention": "zero-extended from %d-bit into the "
                          "32-bit answer register" % native_w,
        }
        native_w = 32
    else:
        ctx.answer = {
            "value_width": w,
            "native_register_width": native_w,
            "convention": "native-32 (auto-clears upper 32 bits of "
                          "the 64-bit answer register)" if native_w == 32
                          else "native-64",
        }

    prelude = []
    for base in ctx.callee_saved_used:
        prelude.append("push %s" % reg_text(base, 64))
    postlude = []
    for base in reversed(ctx.callee_saved_used):
        postlude.append("pop %s" % reg_text(base, 64))
    lines = prelude + lines + postlude
    lines.append("ret")

    ok, out = assemble_and_disassemble(lines, workdir)
    if not ok:
        return "no return path: rendered instructions failed to " \
            "assemble (%s); rendered lines were: %s" % (
                out, "; ".join(lines)), ctx.to_dict()
    return list(lines), ctx.to_dict()


def _largest_block_value(values):
    return EC0._largest_block_value(values)


def render_block_value7(lang, n, raw_value_text, block_canon_lines,
                         workdir):
    TM2 = EC0.TM2
    sub_text, applied, note = TM2.resolve_conditions(
        raw_value_text, block_canon_lines)
    norm, ok, nnote = TM2.normalize(sub_text)
    synth = dict(
        lang=lang, n=n, sem_ok=True,
        normal_path_raw=sub_text,
        normal_path_root=norm,
        normalize_ok=ok,
        normalize_note=nnote,
    )
    return render_unit7(synth, workdir)


def render_branching_unit7(lang, n, canon4_rec, sem_blocks, workdir,
                            check_pair):
    """EC0.render_branching_unit, ported to render_unit7/gen7.
    `check_pair` is canon7_behaviour_check.check_pair (passed in to
    avoid a circular import -- canon7_behaviour_check imports this
    module's render_unit7 for nothing, but keeping the dependency
    one-directional is simpler to reason about)."""
    derived_blocks = canon4_rec.get("derived_blocks")
    if not derived_blocks:
        return "no return path: no derived_blocks on this unit's " \
            "canon4 record", None
    sem_by_label = {}
    for b in sem_blocks:
        sem_by_label["L%d" % b.get("block", -1)] = b

    def emit(label, steps):
        flat_lines.append("%s:" % label)
        for s in steps:
            flat_lines.append("  " + s)

    flat_lines = []
    per_block = []
    contexts = {}
    for rec in derived_blocks:
        label = rec["label"]
        steps = rec.get("steps") or []
        last = steps[-1].split()[0] if steps else None
        if last != "ret":
            emit(label, steps)
            per_block.append(dict(label=label, source="canon4_verbatim",
                                   reason="block does not end in ret "
                                   "-- no scalar value to lift"))
            continue
        sem_block = sem_by_label.get(label)
        value = _largest_block_value(sem_block.get("values", [])) \
            if sem_block else None
        if value is None:
            emit(label, steps)
            per_block.append(dict(label=label, source="canon4_verbatim",
                                   reason="no sem_anchored_spill value "
                                   "found for this block (label %r)"
                                   % label))
            continue
        result, ctxd = render_block_value7(lang, n, value, steps, workdir)
        if isinstance(result, list):
            verdict, detail = check_pair(
                "; ".join(steps), "; ".join(result))
            if verdict == "PROVED_EQUAL":
                emit(label, result)
                contexts[label] = ctxd
                per_block.append(dict(label=label, source="rerendered",
                                       changed=(result != steps),
                                       behaviour_check=verdict))
            else:
                emit(label, steps)
                per_block.append(dict(
                    label=label, source="canon4_verbatim",
                    reason="rendered a candidate but the behaviour-"
                    "preservation gate did not prove it equal to "
                    "canon4's own block text (%s: %s) -- likely this "
                    "block's registers are not the pristine entry "
                    "contract; falling back rather than risk a wrong "
                    "answer" % (verdict, detail[:200])))
        else:
            emit(label, steps)
            per_block.append(dict(label=label, source="canon4_verbatim",
                                   reason=result))

    ok, out = assemble_and_disassemble(flat_lines, workdir)
    if not ok:
        return "no return path: block-stitched rendering failed to " \
            "assemble (%s); lines were: %s" % (
                out, "; ".join(flat_lines)), None
    return (flat_lines, per_block), contexts
