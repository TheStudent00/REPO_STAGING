#!/usr/bin/env python3
"""canon14_render.py -- JOB 1: THE BIT-SERIAL RECONSTRUCTION DEFECT,
ONE ROOT CAUSE, closed at its exact site (gen7/gen11/gen12/gen13's
`concat` handling and the leaf-rendering step every branch shares) --
WITHOUT editing any prior stage's own file (all of them stay kept
artifacts, same monkeypatch discipline canon11/12/13_render.py already
established).

THE DEFECT, restated from the three sightings this lap's brief names
(canon11_worked_examples.txt's own FIX (b) account; canon13_worked_
example.txt's swift/op_296 "HONEST REMAINDER"; canon11_worked_
examples.txt's STAGE 1 tally, "28 still refused ... three DIFFERENT,
UNDIAGNOSED defects"): a value that is ALREADY known, or ALREADY sits
in a register, gets bit-serially RECONSTRUCTED one narrow slice at a
time (`shr`/`and`/`shl`/`or`, repeated once per bit or per byte)
instead of being copied, masked or sign/zero-extended in one
instruction -- because the general `concat` fold (canon7_render.gen7's
own fallback loop, unchanged through canon11/12/13) only recognizes
ONE narrow syntactic shape of "this concat is really an extend": every
sign-bit-replicate part's operand must be l.eq() to the concat's OWN
LAST part, EXACTLY. Two independent things defeat that literal check:

  (i)  DEAD PADDING MATERIALIZED AS REAL INSTRUCTIONS. A leaf atom
       whose provenance resolves to a bare numeric IMMEDIATE (never
       `in0`/`in1` -- this corpus's own convention, expr_to_canon.
       as_immediate's header: "immediate leaves are kept as named
       atoms for z3 CSE/equality reasoning, and only resolved back to
       a concrete value here, AT RENDER TIME, via provenance") is
       OPAQUE to z3's own simplify() -- z3 has no numeric fact about
       an uninterpreted atom, so it cannot fold `Extract(63,8,atom_0)`
       to a literal even when atom_0's real value (0, in the measured
       case) is already on record, one dictionary lookup away. The
       renderer then faithfully walks the padding arithmetic
       (`shr $8,%rax; movabs $mask,%r10; and %r10,%rax; ...`)
       instruction by instruction, all of it PROVABLY dead (canon13_
       worked_example.txt's own annotation on c/op_551).
  (ii) NOT-DISTRIBUTION (and every OTHER z3 rewrite) DEFEATS A
       SYNTACTIC RECOGNIZER. canon11_render.py's FIX (b) already
       chased one instance of this (NOT pushed through Concat) by
       adding a SECOND syntactic special case, `_negate_of()`. That
       approach does not scale: swift/op_296's own stored shape
       (canon13_units_swift.json, `reason` field, verbatim) is
       `Concat(Extract(31,31,atom_0) x32, Extract(31,8,atom_0), 0,
       If(...)|If(...))` -- 32 copies of atom_0's own sign bit, but
       the concat's LAST part is NOT atom_0 at all; it is a totally
       different sub-expression (a fresh boolean fold) whose only
       relationship to atom_0 is that ITS OWN top bit happens to
       equal atom_0's bit 31 (because only the low BYTE of a copy of
       atom_0 was ever replaced). No amount of pattern-matching
       another syntactic shape closes this class of gap; a new one
       will recur under the next rewrite z3's simplifier happens to
       apply.

THE FIX, ONE MECHANISM per sighting instead of two:

  (i)  `_fold_known_leaves()` -- rebuilds a node bottom-up, substitutes
       every provenance-known-immediate leaf with a REAL z3 BitVecVal
       (never an `in0`/`in1` leaf -- those stay free, they are the
       unit's own real traced arguments, the one thing this fold must
       never assume), and re-simplifies with z3's OWN simplify() at
       every point a child actually changed. This puts the fact IN
       BAND for z3, which already knows how to fold Extract/Concat/
       And/Shift of a literal -- verified empirically before writing
       this file: `Concat(Extract(63,8,x), 0:7, y)` with `x` replaced
       by `BitVecVal(0,64)` re-simplifies to `Concat(0:31, y)`,
       collapsing the ENTIRE padding chain to nothing rather than
       leaving a renderer to reconstruct that reasoning instruction by
       instruction. Applied ONCE, as the first thing gen14() does to
       every node it is asked to render (so it fires at every
       recursion depth, not just the tree's root) -- this is a
       RENDERING-time transform only; the mandatory self-consistency
       check in render_unit7 (comparing the re-derived z3 normal form
       against the unit's own STORED normal_path_root) runs, unchanged,
       BEFORE gen14 ever sees a node, on the UNFOLDED tree -- so this
       fix cannot ever cause that check's own guarantee to drift.
  (ii) `_maximal_extend_fold()` -- replaces syntactic pattern-matching
       with a SEMANTIC z3 PROOF. For a concat's parts (MSB-first), it
       finds the longest uniform PREFIX run that is either "N copies
       of literal 0" or "N copies of Extract(k,k,X) for one common X,
       k == X's own top bit" (a cheap syntactic scan, no z3 needed for
       this part), builds `rest` = the concatenation of everything
       after that prefix, and asks z3 DIRECTLY: does the WHOLE concat
       equal `ZeroExt(N, rest)` / `SignExt(N, rest)`? -- a single
       decidable bitvector query that is blind to whatever syntactic
       shape z3's own rewriter left the surrounding expression in,
       because it compares VALUES, not text. On a proof, and only if
       the width gap maps onto one native x86-64 extend instruction
       (movzx/movsx/movsxd -- checked, never assumed), the whole run
       collapses to ONE instruction; SignExt is materialized through
       the SAME `_ensure_native_sign_write` this file adds (mirrors
       the existing `_ensure_native_write` for the zero case, itself
       reused unchanged). No match -> falls through to the prior
       stage's own concat logic (gen11's syntactic recognizer, then
       the general per-part bit-serial loop) exactly as before -- this
       is a STRICT ADDITION, the old paths are still there as a safety
       net, and the mandatory ground-truth gate is the only acceptance
       rule for anything either mechanism produces.

Neither fix reads or writes the operator token; both operate purely on
z3 node shape and this corpus's own provenance map. No memoization
mutable across calls is used ANYWHERE in this file -- correctness over
micro-speed, since z3 AST ids are only unique within one still-live
reference graph and this file has no way to prove two different
render_unit14() calls never let one get reused; every fold recomputes
from the node it is actually given.

MONKEYPATCH, same technique as canon11/12/13_render.py: canon7_render.
gen7 is reassigned to gen14 (falls back to canon13_render.gen13,
UNCHANGED, for every node this file's own two mechanisms do not
apply to or do not improve on). canon7_render.to_z3_with_prov is left
exactly as canon12_render.py already set it.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon7_render as R7                                     # noqa: E402
import canon13_render as R13                                   # noqa: E402
import z3                                                       # noqa: E402

reg_text = R7.reg_text
round_up_width = R7.round_up_width
NATIVE_WIDTHS = R7.NATIVE_WIDTHS
Unsupported = R7.Unsupported
emit_move_leaf_or_imm = R7.emit_move_leaf_or_imm
_ensure_native_write = R7._ensure_native_write

IMM_LEAF_RE = re.compile(r"^-?\d+:(\d+)$")


# --------------------------------------------------------------------
# FIX (i): dead-padding fold.  See file header.
# --------------------------------------------------------------------

def _fold_known_leaves(node, prov):
    """Rebuild `node` bottom-up, replacing every provenance-known-
    immediate leaf with a concrete z3 literal and re-simplifying every
    node whose children actually changed. Never touches an `in0`/`in1`
    leaf (the unit's own real traced arguments -- always left free).
    Falls back to returning `node` unchanged if reconstruction raises
    for any reason (never lets a folding attempt crash rendering)."""
    if z3.is_bv_value(node):
        return node
    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, pkey = prov.get(name, (None, None))
        if kind == "leaf" and pkey is not None and \
                not pkey.startswith("in0") and \
                not pkey.startswith("in1"):
            m = IMM_LEAF_RE.match(pkey)
            if m:
                v = int(pkey.split(":")[0])
                w = int(m.group(1))
                return z3.BitVecVal(v & ((1 << w) - 1), w)
        return node
    kids = node.children()
    if not kids:
        return node
    new_kids = [_fold_known_leaves(c, prov) for c in kids]
    changed = False
    for old_c, new_c in zip(kids, new_kids):
        if not old_c.eq(new_c):
            changed = True
            break
    if not changed:
        return node
    try:
        rebuilt = node.decl()(*new_kids)
        return z3.simplify(rebuilt)
    except Exception:
        return node


# --------------------------------------------------------------------
# FIX (ii): the semantic (proof-based) extend recognizer.
# --------------------------------------------------------------------

def _z3_proves_equal(a, b):
    if a.size() != b.size():
        return False
    solver = z3.Solver()
    solver.add(a != b)
    return solver.check() == z3.unsat


def _classify_prefix(parts):
    """(zero_len, sign_len, sign_source, sign_bit) -- the longest
    uniform "all literal 0" prefix and the longest uniform "N copies
    of Extract(k,k,X), one common X, one common k" prefix, of `parts`
    (MSB-first). Either length may be 0. `k` is NOT required to be
    X's own top bit here -- VEX's own idiom (canon11_render.py's FIX
    (b) comment: "sx64(ex32@0(in0:64))") replicates the sign bit of a
    NARROWER field living inside a wider uninterpreted leaf, so the
    bit position that actually matters is checked against the width
    of the REST of the concat, one level up in
    `_maximal_extend_fold` -- not against X's own declared size."""
    zero_len = 0
    for p in parts:
        if z3.is_bv_value(p) and p.as_long() == 0:
            zero_len = zero_len + 1
        else:
            break
    sign_len = 0
    sign_source = None
    sign_bit = None
    first = parts[0]
    if not z3.is_bv_value(first) and \
            first.decl().kind() == z3.Z3_OP_EXTRACT:
        hi0, lo0 = first.params()
        if hi0 == lo0:
            candidate_source = first.children()[0]
            for p in parts:
                if z3.is_bv_value(p) or \
                        p.decl().kind() != z3.Z3_OP_EXTRACT:
                    break
                hi, lo = p.params()
                if hi != lo or hi != hi0:
                    break
                if not p.children()[0].eq(candidate_source):
                    break
                sign_len = sign_len + 1
            sign_source = candidate_source
            sign_bit = hi0
    return zero_len, sign_len, sign_source, sign_bit


def _native_gap_ok(cur_w, target_w, run):
    return (target_w - cur_w) == run and \
        cur_w in NATIVE_WIDTHS and \
        target_w in NATIVE_WIDTHS


def _maximal_extend_fold(parts):
    """See file header. Returns (kind, rest_expr, run) for the longest
    provably-correct, natively-renderable extend found, else None.
    `kind` is "zero" or "sign"."""
    n = len(parts)
    if n < 2:
        return None
    zero_len, sign_len, sign_source, sign_bit = _classify_prefix(parts)
    whole = None
    candidates = []
    if sign_len >= 1:
        candidates.append(("sign", sign_len, sign_source))
    if zero_len >= 1:
        candidates.append(("zero", zero_len, None))
    for kind, max_len, source in candidates:
        for run in range(max_len, 0, -1):
            rest_parts = parts[run:]
            if not rest_parts:
                continue
            rest_expr = rest_parts[0] if len(rest_parts) == 1 else \
                z3.simplify(z3.Concat(*rest_parts))
            rest_w = rest_expr.size()
            cur_native = round_up_width(rest_w)
            target_native = round_up_width(run + rest_w)
            if not _native_gap_ok(cur_native, target_native, run):
                continue
            if kind == "sign" and sign_bit != rest_w - 1:
                # the replicated bit must be the TOP bit of whatever
                # `rest` reconstructs -- checked against rest's own
                # width, never the (possibly wider) uninterpreted
                # leaf's own declared size (see _classify_prefix's own
                # header for the VEX idiom this generalizes over).
                continue
            if kind == "sign":
                candidate_val = z3.SignExt(run, rest_expr)
            else:
                candidate_val = z3.ZeroExt(run, rest_expr)
            if candidate_val.size() != (run + rest_w):
                continue
            if whole is None:
                whole = z3.simplify(z3.Concat(*parts))
            if whole.size() != candidate_val.size():
                continue
            if _z3_proves_equal(whole, candidate_val):
                return kind, rest_expr, run
    return None


def _ensure_native_sign_write(reg_base, cur_w, target_w, lines):
    if cur_w == target_w:
        return target_w
    if cur_w == 32 and target_w == 64:
        lines.append("movsxd %s,%s" % (
            reg_text(reg_base, 32), reg_text(reg_base, 64)))
        return target_w
    if cur_w in NATIVE_WIDTHS and target_w in NATIVE_WIDTHS:
        lines.append("movsx %s,%s" % (
            reg_text(reg_base, cur_w), reg_text(reg_base, target_w)))
        return target_w
    raise Unsupported(
        "sign-extend from %d to %d bits has no native movsx form"
        % (cur_w, target_w))


# --------------------------------------------------------------------
# gen14(): folds every node it is given (FIX (i)), tries the semantic
# extend recognizer on `concat` nodes (FIX (ii)), and otherwise
# delegates to canon13_render.gen13 UNCHANGED.
# --------------------------------------------------------------------

def gen14(node, dest_base, ctx, lines, prov):
    node = _fold_known_leaves(node, prov)

    if z3.is_bv_value(node):
        w = round_up_width(node.size())
        emit_move_leaf_or_imm(
            lines, ("imm", node.as_long(), w), dest_base, w, ctx)
        return w

    # FIX (iii), found tracing c/op_319 (`a && b`) -- one of Stage 1's
    # OWN 28 still-refused units (canon11_units_cpp.json's own stored
    # reason: "STAGE1-ATTEMPTED ... DISPROVED", the exact 12 cpp + 4 c
    # units canon13_worked_example.txt separately calls "newly
    # REACHABLE" once the deep-dispatch fix let gen13 see them at
    # all). z3's own bvnot/bvor/bvand De Morgan normal form negates a
    # BOOLEAN 0/1 value (an `Extract`/`If`-derived 1-bit z3 node, e.g.
    # `~(If(a,1,0) | If(b,1,0))`, VERIFIED: `bvnot`'s own operand here
    # measures z3-node-width 1) the SAME way it negates a general
    # bitvector -- but the RENDERED representation of a 1-bit value
    # occupies a wider register (a byte, from `sete`/`or` of two
    # canonical 0/1 bytes, per this renderer's own established
    # convention). A literal `not` on that byte flips ALL 8 bits
    # (0x00 -> 0xFF, 255 -- not the logical negation 1), which the
    # OLD `bvnot` branch (gen7/gen11/gen12/gen13, unchanged, still
    # reached via delegation below) has always emitted, silently
    # WRONG for exactly this shape (measured counterexample against
    # real ship code: seed_rdi=4294967295, seed_rsi=
    # 18446744073709551615 -- z3's own gate). THE FIX: a z3 node of
    # TRUE WIDTH 1 can only ever be 0 or 1 by construction, so
    # "bitwise NOT of this node's one meaningful bit" and "logical
    # NOT of a canonical 0/1 byte" are THE SAME operation --
    # `xor $1,<8-bit dest>` implements it correctly (flips only the
    # bit that matters, leaves the already-clean upper 7 bits alone),
    # `not` does not. Reused, not duplicated: this is the identical
    # instruction canon13_render.gen_bool's own `not` case already
    # uses for the same reason.
    if node.decl().kind() != z3.Z3_OP_UNINTERPRETED and \
            node.decl().name() == "bvnot":
        inner = node.children()[0]
        if inner.size() == 1:
            R7.gen7(inner, dest_base, ctx, lines, prov)
            lines.append("xor $1,%s" % reg_text(dest_base, 8))
            return node.size()

    if node.decl().kind() != z3.Z3_OP_UNINTERPRETED and \
            node.decl().name() == "concat":
        parts = list(node.children())
        found = _maximal_extend_fold(parts)
        if found is not None:
            kind, rest_expr, run = found
            rest_w = rest_expr.size()
            rendered_w = R7.gen7(rest_expr, dest_base, ctx, lines, prov)
            cur_native = round_up_width(rendered_w)
            target_native = round_up_width(run + rest_w)
            if kind == "sign":
                _ensure_native_sign_write(
                    dest_base, cur_native, target_native, lines)
            else:
                _ensure_native_write(
                    dest_base, cur_native, target_native, lines)
            return run + rest_w

    return R13.gen13(node, dest_base, ctx, lines, prov)


R7.gen7 = gen14

render_unit14 = R7.render_unit7
render_block_value14 = R7.render_block_value7
render_branching_unit14 = R7.render_branching_unit7
