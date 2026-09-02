#!/usr/bin/env python3
"""canon17_render.py -- JOB 2: RENDER THE FLOAT PACKED-FLAGS FAMILY
BACK TO INSTRUCTIONS, using canon16_xmm.py's own designated registers
(a -> %xmm0, b -> %xmm1) and its ordered XMM temp pool.

THE ONE NEW CASE: an uninterpreted z3 atom whose provenance kind is
"fcond" (canon17_float.py's own tag -- never confused with "call",
which still means refuse). Everything else -- how two fcond atoms
COMBINE (Or8/And8, De Morgan NOT-of-OR/AND, an outer Concat/Extract
wrapping a computed byte into a wider "answer" register) -- needs NO
new code at all: once a fcond atom renders into a canonical 0/1 BYTE
in a register (exactly gen7's own existing "if"-node is_bool_data
convention: `mov $0,<32-bit dest>; set<suf> <8-bit dest>`), the
EXISTING `_gen_alu` fold (canon7_render.py, unchanged, reached via
this file's own delegation to canon14_render.gen14) already renders
`Or8(X, Y)` as "render X into dest; render Y into a temp; `or
temp,dest`" -- real `or`/`and` INSTRUCTIONS combining two canonical
0/1 bytes, which is exactly the shape AgentMemory's own worked example
names for go's `==` (`setnp %al; setne %cl; ... and %ecx,%eax`, up to
naming). gen14's own De Morgan fold (already present, unchanged)
handles the `~(~(A|B)|~(C|D))` = `(A|B)&(C|D)` shape the same way.
So THIS file's own job is exactly one thing: turn ONE fcond atom into
one `ucomisd`/`ucomiss` (emitted ONCE per operand pair per unit,
flags read by however many setcc's reference it -- real hardware's
own "flags persist" rule, mirrored via `ctx.fcmp_done`, a per-render
cache keyed by the operand-pair identity) plus one `set<suf>`.

ENTRY CONTRACT (matches canon16_xmm.py exactly, restated here so this
file does not have to be read beside that one to be trusted): a in
%xmm0, b in %xmm1, a "zero" operand loaded via the corpus's own
self-XOR idiom (`xorps %xmmT,%xmmT` / `xorpd %xmmT,%xmmT`) into the
FIRST member of canon16_xmm.XMM_TEMP_POOL_ORDER (%xmm2) -- this file's
own target units never need more than one XMM temp (at most one of
the two compared operands is ever the literal zero), so no further
pool bookkeeping is needed; the single slot is guarded (`ctx.
fcmp_zero_reg`) so a unit that reads the SAME zero temp from two
different fcond atoms (rare -- would require comparing zero against
itself, never measured) does not re-zero it redundantly.

WIDTH: `ucomisd` (both operands f64 -- either genuinely double, or an
f32 value VEX widened via F32toF64 for the compare) vs `ucomiss` (both
operands f32, no widening) is chosen from the OPERANDS' OWN recorded
width (canon17_float.classify_float_operand's own `p_width`/`q_width`
-- NEVER guessed from a mnemonic spelling, matching canon16.py's own
established rule for the sign-mask width in the vector-negate file).
A width MISMATCH between the two operands (never measured in this
corpus -- see canon17_float.py's own survey) is refused, not guessed.

REFUSAL, HONEST: an fcond atom whose P or Q tag is None (an operand
outside the six-shape whitelist -- an int-to-float conversion, or a
comparison between two differently-derived values) is refused by name
(`Unsupported`), the same shape every other renderer in this lineage
uses for "this specific shape is not yet in scope", never a silent
wrong rendering.

MONKEYPATCH, same technique as canon11/12/13/14_render.py:
canon7_render.gen7 is reassigned to gen17 (falls back to canon14_
render.gen14, UNCHANGED, for every node this file's own new case does
not apply to); canon7_render.to_z3_with_prov is reassigned to
canon17_float.to_z3_with_prov_v2b (the float-aware normalizer,
mirroring canon12_render.py's own precedent of repointing that name).

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
import canon17_float as CF                                      # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
round_up_width = R7.round_up_width
Unsupported = R7.Unsupported

XMM_ZERO_TEMP = X16.XMM_TEMP_POOL_ORDER[0]

# THE MIXED-SIGNATURE REGISTER RULE (canon.py's own `designated()`,
# its header quoted verbatim: "b takes %xmm1 only when a is also a
# floating-point value; otherwise b takes %xmm0" -- the C calling
# rule, register files counted SEPARATELY per type). This file's own
# target set is NOT float-vs-float only -- it also covers `a && b`/
# `a || b` where ONE side is bool/int and the OTHER is the float being
# compared (e.g. c/op_351, `a && b`, a:bool b:float32 -- real ship
# code's own `ucomiss %xmm1,%xmm0` puts b (the ONLY float argument) in
# %xmm0, not %xmm1, exactly this rule). CURRENT_A_IS_VECTOR is set by
# canon17.py, the driver, once per unit (a simple "current render
# context" cell -- rendering is one unit at a time, never concurrent,
# so this is safe and avoids threading a new field through canon7_
# render.Context, which this file does not own) from that unit's OWN
# recorded `meta.lhs_rep`.
CURRENT_A_IS_VECTOR = [True]


def set_render_context(a_is_vector):
    CURRENT_A_IS_VECTOR[0] = a_is_vector

# fcond name -> setcc suffix, the SAME suffix vocabulary condition_
# table.py's own SUFFIX_TO_COND already names for these eight
# conditions (e/ne/p/np/b/ae/a/be -- the canonical spelling this
# lineage's own renderer already emits everywhere else, e.g. gen7's
# `if`-node `real_suf`).
FCOND_TO_SUFFIX = {
    "FCEQ": "e",
    "FCNE": "ne",
    "FCPAR": "p",
    "FCNPAR": "np",
    "FCULT": "b",
    "FCUGE": "ae",
    "FCUGT": "a",
    "FCULE": "be",
}

def _operand_xmm(tag, width, ctx, lines):
    """the physical %xmmN register holding this operand, emitting the
    self-XOR zero idiom the first time a "zero" operand is needed."""
    if tag in ("a", "b"):
        return CANON.designated(tag, "xmm0", CURRENT_A_IS_VECTOR[0])
    if tag == "zero":
        already = getattr(ctx, "fcmp_zero_reg", None)
        if already is not None:
            return already
        mnem = "xorps" if width == 32 else "xorpd"
        lines.append("%s %%%s,%%%s" % (
            mnem, XMM_ZERO_TEMP, XMM_ZERO_TEMP))
        ctx.fcmp_zero_reg = XMM_ZERO_TEMP
        return XMM_ZERO_TEMP
    raise Unsupported(
        "float comparison operand tag %r is outside this file's own "
        "whitelist (a/b/zero) -- no return path" % tag)


def _emit_ucomis(p_tag, p_w, q_tag, q_w, ctx, lines):
    """emits ucomisd/ucomiss ONCE for this operand pair (real
    hardware's own flags-persist rule -- a second fcond atom reading
    the SAME pair reuses the already-set flags, exactly like
    condition_table.py's own "most recent flag setter" rule for the
    integer family). Returns nothing; the cache lives on `ctx`."""
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
            "whitelist (p=%r q=%r) -- no return path; see canon17_"
            "float.py's own classify_float_operand" % (
                payload.get("p_text"), payload.get("q_text")))
    suf = FCOND_TO_SUFFIX.get(fcond)
    if suf is None:
        raise Unsupported(
            "synthetic float condition %r has no known setcc suffix"
            % fcond)
    _emit_ucomis(p_tag, p_w, q_tag, q_w, ctx, lines)
    lines.append("mov $0,%s" % reg_text(dest_base, 32))
    lines.append("set%s %s" % (suf, reg_text(dest_base, 8)))
    return 1


def gen17(node, dest_base, ctx, lines, prov):
    if not z3.is_bv_value(node) and \
            node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, payload = prov[name]
        if kind == "fcond":
            return _render_fcond(payload, dest_base, ctx, lines)
    return R14.gen14(node, dest_base, ctx, lines, prov)


R7.gen7 = gen17
R7.to_z3_with_prov = CF.to_z3_with_prov_v2b

render_unit17 = R7.render_unit7
