#!/usr/bin/env python3
"""expr_to_canon.py -- THE RETURN PATH.

Reads tree_units2.json (tree_match2.py's z3-simplify()-normalized
`normal_path_root` expression per unit) and, for each unit, tries to
render that expression back into canonical x86-64 AT&T instructions
in the designated registers (a -> %rdi/%edi, b -> %rsi/%esi,
answer -> %rax/%eax, temps -> %r10/%r11), one instruction per line,
then ASSEMBLES the result with the system `as` and disassembles it
with `objdump` (the same real-tool-testimony pattern canon2.py uses)
to confirm the rendering is valid.

Every unit's own canon2_units_<lang>.json record is consulted for
atom provenance ONLY for the divmod-family uninterpreted atom (the
one case in this corpus where the SAME unit's own erased_form/
derived_text already names the originating instructions -- reused
here, not re-derived). No atom is ever given invented semantics: an
uninterpreted atom this file cannot trace to real instructions is an
honest "no return path", never a guess.

Output: tree_units3.json -- tree_units2.json's own unit list, each
record with one field added, `canonical_return`: either the list of
rendered+assembled instruction lines, or a string starting with
"no return path: " naming the exact reason.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

THE SPELLING BAN: the op-to-instruction table below is keyed by the
z3 OPERATOR/OPCODE name (bvadd, bvand, extract, concat, ...) -- never
by a source-language operator token ('+', '%', ...). This file does
not group or pair units; it renders one unit at a time.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                      # noqa: E402
import tree_match2 as TM2                                     # noqa: E402
import condition_table as CT                                  # noqa: E402

import z3                                                     # noqa: E402

LANGS = TM2.LANGS

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width


# --------------------------------------------------------------------
# Section 1: re-derive z3 expr + PROVENANCE for one unit's
# `normal_path_raw` text.
#
# tree_match2.py's own `normalize()` throws its `atoms` dict away
# after simplify() -- only the printed string survives in
# tree_units2.json. To know what an atom named atom_N/op_N actually
# denotes we must rebuild the SAME z3 expression the same way
# (identical recursive walk, identical insertion order), and this
# time keep the provenance: is this atom a bare input leaf (a/b/an
# immediate), or an uninterpreted VEX call this normalizer could not
# model?
# --------------------------------------------------------------------

class CallAtom(Exception):
    def __init__(self, name, call_text):
        Exception.__init__(self, call_text)
        self.name = name
        self.call_text = call_text


def to_z3_with_prov(tree, atoms, prov, widen_cache=None):
    """kept in lockstep with tree_match2.py's to_z3_fixed -- see that
    file's CAUSE 1/2/3 comments for why each addition below exists.
    This copy also tracks PROVENANCE (leaf vs. opaque call), which
    to_z3_fixed does not need."""
    if widen_cache is None:
        widen_cache = {}
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = leaf_width(text)
        key = text
        if key not in atoms:
            name = "atom_%d" % len(atoms)
            atoms[key] = z3.BitVec(name, w)
            prov[name] = ("leaf", key)
        return atoms[key]

    name, args = tree[1], tree[2]
    kids = [to_z3_with_prov(a, atoms, prov, widen_cache) for a in args]

    if name in CT.COND_OPS:
        # CAUSE 1.
        L, R = kids[0], kids[1]
        if L.size() != R.size():
            if L.size() < R.size():
                L = z3.ZeroExt(R.size() - L.size(), L)
            else:
                R = z3.ZeroExt(L.size() - R.size(), R)
        pred = CT.cond_to_z3(name, L, R, z3)
        return z3.If(pred, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
    if name in ("And32", "And64", "And8"):
        return kids[0] & kids[1]
    if name in ("Or32", "Or64", "Or8"):
        return kids[0] | kids[1]
    if name in ("Xor32", "Xor64", "Xor8"):
        return kids[0] ^ kids[1]
    if name in ("Add32", "Add64"):
        return kids[0] + kids[1]
    if name in ("Sub32", "Sub64", "Sub8"):
        return kids[0] - kids[1]
    if name in ("Not32", "Not64", "Not8"):
        return ~kids[0]
    if name in ("Sar32", "Sar64", "Shr32", "Shr64", "Shl32", "Shl64",
                "Shl8"):
        val, amt = kids[0], kids[1]
        if amt.size() != val.size():
            if val.size() > amt.size():
                amt = z3.ZeroExt(val.size() - amt.size(), amt)
            else:
                amt = z3.Extract(val.size() - 1, 0, amt)
        if name.startswith("Sar"):
            return val >> amt
        if name.startswith("Shr"):
            return z3.LShR(val, amt)
        return val << amt
    if name.startswith("zx"):
        outw = int(name[2:])
        inw = kids[0].size()
        if outw > inw:
            return z3.ZeroExt(outw - inw, kids[0])
        return kids[0]
    if name.startswith("sx"):
        outw = int(name[2:])
        inw = kids[0].size()
        if outw > inw:
            return z3.SignExt(outw - inw, kids[0])
        return kids[0]
    if name.startswith("ex"):
        m = TM.re.match(r"ex(\d+)@(\d+)$", name)
        width, off = int(m.group(1)), int(m.group(2))
        child = kids[0]
        need = off + width
        if need > child.size():
            # CAUSE 3.
            ck = (id(child), need)
            if ck not in widen_cache:
                extra = need - child.size()
                nm = "pad_%d" % len(widen_cache)
                pad = z3.BitVec(nm, extra)
                prov[nm] = ("call", "<width-pad for %r>" % serialize(tree))
                widen_cache[ck] = z3.Concat(pad, child)
            child = widen_cache[ck]
        return z3.Extract(off + width - 1, off, child)
    if name == "32HLto64":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name == "ite":
        # CAUSE 1 (cmov).
        cond_bit = kids[0]
        return z3.If(cond_bit == z3.BitVecVal(1, cond_bit.size()),
                      kids[1], kids[2])
    if name.startswith("ins@"):
        # CAUSE 1 (partial-register write idiom; see tree_match2.py).
        m = TM.re.match(r"ins@(\d+)$", name)
        off = int(m.group(1))
        base, val = kids[0], kids[1]
        w, vw = base.size(), val.size()
        if off + vw > w:
            raise ValueError(
                "ins@%d: inserted value width %d at offset %d "
                "exceeds base width %d" % (off, vw, off, w))
        widened_val = z3.ZeroExt(w - vw, val) if w > vw else val
        if off:
            widened_val = widened_val << off
        mask = ((1 << vw) - 1) << off
        cleared = base & z3.BitVecVal((~mask) & ((1 << w) - 1), w)
        return cleared | widened_val

    text = serialize(tree)
    w = 64
    if text not in atoms:
        nm = "op_%d" % len(atoms)
        atoms[text] = z3.BitVec(nm, w)
        prov[nm] = ("call", text)
    return atoms[text]


CALL_HEAD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(")


def call_op_name(call_text):
    m = CALL_HEAD_RE.match(call_text)
    return m.group(1) if m else call_text


# --------------------------------------------------------------------
# Section 2: category names for the atoms this renderer refuses.
# Verified by direct grep of tree_units2.json's own normal_path_raw/
# normal_path_root text (see report) -- not guessed.
# --------------------------------------------------------------------

DIVMOD_SCALAR = set([
    "DivModS64to32",
    "DivModU64to32",
])

REFUSAL_CATEGORY = {
    "amd64g_calculate_condition": "condition-code helper call "
        "(flags -> boolean; not a scalar bitvector op this "
        "renderer models)",
    "amd64g_calculate_rflags_c": "condition-code helper call "
        "(carry-flag reconstruction; not modeled)",
    "CmpF64": "floating-point compare (not a scalar bitvector op)",
    "CmpEQ32F0x4": "SIMD packed-float compare (not modeled)",
    "CmpEQ64F0x2": "SIMD packed-float compare (not modeled)",
    "F32toF64": "float<->float conversion (not modeled as an "
        "integer bitvector op)",
    "F64toF32": "float<->float conversion (not modeled as an "
        "integer bitvector op)",
    "I32StoF64": "int->float conversion (not modeled as an "
        "integer bitvector op)",
    "I64StoF64": "int->float conversion (not modeled as an "
        "integer bitvector op)",
    "Add32F0x4": "SIMD packed-float add (not modeled)",
    "Add64F0x2": "SIMD packed-float add (not modeled)",
    "Sub32F0x4": "SIMD packed-float sub (not modeled)",
    "Sub64F0x2": "SIMD packed-float sub (not modeled)",
    "Sub64Fx2": "SIMD packed-float sub (not modeled)",
    "Mul32F0x4": "SIMD packed-float mul (not modeled)",
    "Mul64F0x2": "SIMD packed-float mul (not modeled)",
    "Div32F0x4": "SIMD packed-float div (not modeled)",
    "Div64F0x2": "SIMD packed-float div (not modeled)",
    "XorV128": "SIMD 128-bit xor (not modeled)",
    "OrV128": "SIMD 128-bit or (not modeled)",
    "AndV128": "SIMD 128-bit and (not modeled)",
    "HLtoV128": "SIMD 128-bit pack (not modeled)",
    "HLto128": "128-bit pack (not modeled)",
    "InterleaveLO32x4": "SIMD lane interleave (not modeled)",
    "DivModU128to64": "128-bit divmod (not modeled; distinct from "
        "the scalar 32-bit divmod this renderer does model)",
    "DivModS128to64": "128-bit divmod (not modeled; distinct from "
        "the scalar 32-bit divmod this renderer does model)",
    "Mul64": "64x64 multiply not recognized by tree_match2's "
        "normalize() (falls to opaque atom; only Add/Sub/And/Or/"
        "Xor/Not/shifts are recognized scalar ops)",
    "Mul32": "32x32 multiply not recognized by tree_match2's "
        "normalize() (falls to opaque atom)",
    "ite": "z3 if-then-else survives simplification (control-flow "
        "dependent value; not a straight-line scalar rendering)",
    "g0": "raw VEX guest-state/helper read, opaque to the "
        "normalizer",
    "MullU64": "widening multiply not recognized by tree_match2's "
        "normalize()",
    "Shl8": "8-bit shift not recognized by tree_match2's "
        "normalize() (only Shl32/Shl64 are in the recognized list)",
    "Or8": "8-bit or not recognized by tree_match2's normalize() "
        "(only Or32/Or64 are in the recognized list)",
    "And8": "8-bit and not recognized by tree_match2's normalize() "
        "(only And32/And64 are in the recognized list)",
    "Xor8": "8-bit xor not recognized by tree_match2's normalize() "
        "(only Xor32/Xor64 are in the recognized list)",
    "Sub8": "8-bit sub not recognized by tree_match2's normalize() "
        "(only Sub32/Sub64 are in the recognized list)",
    "Not8": "8-bit not not recognized by tree_match2's normalize() "
        "(only Not32/Not64 are in the recognized list)",
}


def refusal_reason_for_call(name):
    cat = REFUSAL_CATEGORY.get(name)
    if cat is None:
        cat = "uninterpreted VEX operation not modeled by " \
              "tree_match2's normalize() (falls to an opaque atom)"
    return "no return path: expression contains an uninterpreted " \
           "atom for VEX op '%s' -- %s" % (name, cat)


# --------------------------------------------------------------------
# Section 3: canon2 lookup, for the ONE atom family this renderer
# does trace to real instructions (scalar 32-bit divmod, the same
# family worked in AgentMemory's/log_074's c/op_246 example).
# --------------------------------------------------------------------

_CANON2_CACHE = {}


def load_canon2(lang):
    if lang not in _CANON2_CACHE:
        path = os.path.join(HERE, "canon2_units_%s.json" % lang)
        if os.path.exists(path):
            doc = json.load(open(path))
            _CANON2_CACHE[lang] = doc.get("units", {})
        else:
            _CANON2_CACHE[lang] = {}
    return _CANON2_CACHE[lang]


def canon2_derived_text(lang, n):
    units = load_canon2(lang)
    rec = units.get(n)
    if rec is None:
        return None, "no canon2_units_%s.json record for this unit" \
            % lang
    if rec.get("erasure") != "ok":
        return None, "this unit's own canon2 record did not erase " \
            "cleanly (%r); no runnable instructions to trace the " \
            "divmod atom to" % rec.get("erasure")
    dt = rec.get("derived_text")
    if not isinstance(dt, list):
        return None, "this unit's own canon2 record has no " \
            "derived instruction list (branching unit or refused: " \
            "%r)" % dt
    return dt, None


# --------------------------------------------------------------------
# Section 4: general scalar codegen for the pure-arithmetic case
# (no uninterpreted atom anywhere in the simplified expression).
#
# z3's simplify() rewrites the recognized vocabulary into ITS OWN
# normal form -- confirmed by direct experiment, not assumed:
# subtraction becomes bvadd with a constant bvmul; conjunction
# becomes a De Morgan bvnot/bvor chain; sign-extension becomes a
# repeated single-bit Concat. This codegen renders what z3 ACTUALLY
# emits, op by op, rather than the tidier vocabulary the input
# recognizer used.
# --------------------------------------------------------------------

class NoTemps(Exception):
    pass


class Unsupported(Exception):
    pass


REGMAP = {
    "a": {64: "%rdi", 32: "%edi", 16: "%di", 8: "%dil"},
    "b": {64: "%rsi", 32: "%esi", 16: "%si", 8: "%sil"},
    "ans": {64: "%rax", 32: "%eax", 16: "%ax", 8: "%al"},
    "r10": {64: "%r10", 32: "%r10d", 16: "%r10w", 8: "%r10b"},
    "r11": {64: "%r11", 32: "%r11d", 16: "%r11w", 8: "%r11b"},
    "cl": {8: "%cl"},
}

NATIVE_WIDTHS = (8, 16, 32, 64)


def reg_text(base, width):
    table = REGMAP[base]
    if width not in table:
        raise Unsupported("register base %r has no %d-bit form"
                           % (base, width))
    return table[width]


def round_up_width(w):
    for cand in NATIVE_WIDTHS:
        if w <= cand:
            return cand
    raise Unsupported("width %d exceeds 64 bits" % w)


class Pool(object):
    def __init__(self):
        self.free_temps = ["r10", "r11"]

    def alloc(self):
        if not self.free_temps:
            raise NoTemps("expression nesting exceeds the two "
                           "available temp registers (%r10/%r11)")
        return self.free_temps.pop()

    def release(self, base):
        if base in ("r10", "r11") and base not in self.free_temps:
            self.free_temps.append(base)


def imm_fits_32(v, width):
    if width <= 32:
        return True
    return -(2 ** 31) <= v < 2 ** 31


def mask_value(width):
    return (1 << width) - 1


def emit_move_leaf_or_imm(lines, val, dest_base, dest_width, pool):
    """val is ('leaf', base, width) or ('imm', intval, width).
    emit a mov into dest_base at dest_width; returns nothing."""
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


def emit_alu_source(lines, val, op_mnem, dest_base, dest_width, pool):
    """emit `op_mnem  src, dest` where src is val's leaf/imm/temp,
    widened/truncated to dest_width first if it is a leaf/temp of a
    different width (rare in this corpus; refuse rather than guess
    if it happens)."""
    kind = val[0]
    if kind == "imm":
        v = val[1] & mask_value(dest_width)
        if v >= 2 ** (dest_width - 1):
            signed = v - (1 << dest_width)
        else:
            signed = v
        if dest_width == 64 and not imm_fits_32(signed, 64):
            t = pool.alloc()
            lines.append("movabs $%d,%s" % (
                signed, reg_text(t, dest_width)))
            lines.append("%s %s,%s" % (
                op_mnem, reg_text(t, dest_width),
                reg_text(dest_base, dest_width)))
            pool.release(t)
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


ALU_OP = {
    "bvadd": "add",
    "bvor": "or",
    "bvxor": "xor",
    "bvand": "and",
    "bvmul": "imul",
}


CMP_OP_TO_SUFFIX = {
    "=": "e",
    "distinct": "ne",
    "bvult": "b", "bvule": "be",
    "bvugt": "a", "bvuge": "ae",
    "bvslt": "l", "bvsle": "le",
    "bvsgt": "g", "bvsge": "ge",
}

NEGATE_SUFFIX = {
    "e": "ne", "ne": "e",
    "b": "ae", "ae": "b",
    "a": "be", "be": "a",
    "l": "ge", "ge": "l",
    "g": "le", "le": "g",
}


def decode_bool_condition(bnode):
    """CAUSE 1 renderer helper: z3's own post-simplify vocabulary for
    a boolean condition (`=`, `distinct`, `bvult`/`bvule`/`bvugt`/
    `bvuge`, `bvslt`/`bvsle`/`bvsgt`/`bvsge`, or `not` of any of
    those) -> (setcc suffix, L, R). Parity conditions (CondPAR/
    CondNPAR) are not decodable this way and correctly fall through
    to Unsupported -- they are rare in this corpus (see condition_
    table.py's header) and this renderer refuses them honestly
    rather than guessing."""
    d = bnode.decl().name()
    if d == "not":
        suf, L, R = decode_bool_condition(bnode.children()[0])
        if suf not in NEGATE_SUFFIX:
            raise Unsupported(
                "no negation rule for condition suffix %r" % suf)
        return NEGATE_SUFFIX[suf], L, R
    if d in CMP_OP_TO_SUFFIX:
        L, R = bnode.children()
        return CMP_OP_TO_SUFFIX[d], L, R
    raise Unsupported(
        "no rendering rule for boolean condition shape %r" % d)


def _signed_of(v, width):
    v = v & mask_value(width)
    if v >= 2 ** (width - 1):
        return v - (1 << width)
    return v


def as_immediate(node, prov):
    """returns the constant integer this node denotes, if it is one
    -- either a concrete z3 BitVecVal, OR (this codebase's own
    convention, unchanged, see gen()'s Z3_OP_UNINTERPRETED case) an
    uninterpreted atom whose provenance is a bare numeric-immediate
    LEAF (e.g. the "0:64" in `CondEQ(x, 0:64)` -- immediate leaves
    are kept as named atoms for z3 CSE/equality reasoning, and only
    resolved back to a concrete value here, at render time, via
    provenance). Returns None if `node` is not a constant."""
    if z3.is_bv_value(node):
        return node.as_long()
    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, key = prov.get(name, (None, None))
        if kind == "leaf" and not key.startswith("in0") and \
                not key.startswith("in1"):
            m = re.match(r"^-?\d+:(\d+)$", key)
            if m:
                return int(key.split(":")[0])
    return None


def gen(node, dest_base, pool, lines, prov):
    """render `node` (a z3 BitVecRef) so its value ends up in
    dest_base at node's own bit-width. returns the width written.
    `prov` maps an atom's z3 declaration name to its provenance
    (leaf text or uninterpreted-call text) -- passed explicitly on
    every call, since z3's ExprRef objects returned by `.children()`
    are fresh wrapper objects each time and cannot carry a stashed
    Python attribute across that boundary."""
    if z3.is_bv_value(node):
        # a constant's OWN width need not be a native register width
        # (e.g. z3's De Morgan expansion of `not(zx8(x))` produces a
        # literal 7-bit `127` alongside a 1-bit `if` in one Concat --
        # found while extending this renderer for CAUSE 1's CondXX
        # predicates). A constant always fits cleanly in the next
        # native width up; round up before ever calling reg_text.
        w = round_up_width(node.size())
        emit_move_leaf_or_imm(
            lines, ("imm", node.as_long(), w), dest_base, w, pool)
        return w

    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        name = node.decl().name()
        kind, key = prov[name]
        if kind == "call":
            raise CallAtom(name, key)
        w = node.size()
        if key.startswith("in0"):
            emit_move_leaf_or_imm(
                lines, ("leaf", "a", w), dest_base, w, pool)
        elif key.startswith("in1"):
            emit_move_leaf_or_imm(
                lines, ("leaf", "b", w), dest_base, w, pool)
        else:
            m = re.match(r"^-?\d+:(\d+)$", key)
            if not m:
                raise Unsupported(
                    "leaf atom %r is neither an input (in0/in1) "
                    "nor a recognizable immediate literal" % key)
            v = int(key.split(":")[0])
            emit_move_leaf_or_imm(
                lines, ("imm", v, w), dest_base, w, pool)
        return w

    op = node.decl().name()
    args = node.children()

    if op == "bvnot":
        w = gen(args[0], dest_base, pool, lines, prov)
        lines.append("not %s" % reg_text(dest_base, round_up_width(w)))
        return w

    if op == "if":
        # CAUSE 1 (best-effort renderer extension, added while
        # verifying condition_table.py's substitution actually
        # converges units, not just normalizes them).  z3's `If`
        # shows up two ways here: predicate-as-DATA (CondXX's own
        # `If(pred, 1, 0)` -- possibly re-simplified further by z3)
        # and general SELECT (cmov's `ite(cond, then, else)`).  Both
        # render off the SAME two steps: render the compared operands,
        # `cmp`, then either `setCC` (data case) or `cmovCC` (select
        # case) reading the fresh flags.
        cond_node, then_v, else_v = args
        suf, L, R = decode_bool_condition(cond_node)
        w = node.size()
        native_w = round_up_width(w)
        is_bool_data = (
            z3.is_bv_value(then_v) and z3.is_bv_value(else_v) and
            then_v.size() == else_v.size() and
            set([then_v.as_long(), else_v.as_long()]) == set([0, 1]))
        if is_bool_data:
            tL = pool.alloc()
            gen(L, tL, pool, lines, prov)
            Lw = round_up_width(L.size())
            r_imm = as_immediate(R, prov)
            if r_imm is not None:
                lines.append("cmp $%d,%s" % (
                    _signed_of(r_imm, Lw), reg_text(tL, Lw)))
            else:
                tR = pool.alloc()
                gen(R, tR, pool, lines, prov)
                lines.append("cmp %s,%s" % (
                    reg_text(tR, Lw), reg_text(tL, Lw)))
                pool.release(tR)
            if native_w > 8:
                lines.append("mov $0,%s" % reg_text(dest_base, native_w))
            real_suf = suf if then_v.as_long() == 1 else \
                NEGATE_SUFFIX[suf]
            lines.append("set%s %s" % (real_suf, reg_text(dest_base, 8)))
            pool.release(tL)
            return w
        # general select (cmov): render both branch values FIRST
        # (either may itself contain a nested condition, which would
        # clobber the flags this level is about to set), then compare,
        # then cmov.
        gen(else_v, dest_base, pool, lines, prov)
        t2 = pool.alloc()
        gen(then_v, t2, pool, lines, prov)
        tL = pool.alloc()
        gen(L, tL, pool, lines, prov)
        Lw = round_up_width(L.size())
        r_imm = as_immediate(R, prov)
        if r_imm is not None:
            lines.append("cmp $%d,%s" % (
                _signed_of(r_imm, Lw), reg_text(tL, Lw)))
        else:
            tR = pool.alloc()
            gen(R, tR, pool, lines, prov)
            lines.append("cmp %s,%s" % (reg_text(tR, Lw), reg_text(tL, Lw)))
            pool.release(tR)
        lines.append("cmov%s %s,%s" % (
            suf, reg_text(t2, native_w), reg_text(dest_base, native_w)))
        pool.release(t2)
        pool.release(tL)
        return w

    if op == "bvmul" and len(args) == 2:
        # STEP 7 fix (found on c/op_13, `-a`): z3's own normal form
        # for unary negation is `bvmul(x, -1)` (equivalently
        # `bvadd(0, bvmul(-1,x))` when embedded in a sum -- see the
        # bvadd zero-elision fix just below).  The generic ALU_OP fold
        # rendered this as "mov 0,dest; mov -1,t1; mov x,t2;
        # imul t2,t1; add t1,dest" -- four extra instructions for
        # what a single `neg` does.  Detected here by literal value,
        # not by matching source syntax (never the operator token):
        # a concrete multiplicand equal to the all-ones bit pattern
        # (unsigned 2**w-1, i.e. -1) at this op's own width.
        for i in (0, 1):
            if z3.is_bv_value(args[i]) and \
                    args[i].as_long() == (1 << args[i].size()) - 1:
                other = args[1 - i]
                w = gen(other, dest_base, pool, lines, prov)
                lines.append("neg %s" % reg_text(dest_base,
                                                   round_up_width(w)))
                return w

    if op == "bvadd" and len(args) >= 2:
        # STEP 7 fix, same shape: drop any addend that is a literal
        # ZERO (concrete OR an immediate-leaf atom resolved via
        # provenance, e.g. the "0:64" leaf c/op_13's own Sub64(0,a)
        # lift produces) BEFORE folding -- adding zero is a no-op,
        # and the generic fold was spending a `mov $0,dest` plus a
        # trailing `add` on it. Left with exactly one addend, this
        # turns "mov 0,dest; ...; add ...,dest" into rendering that
        # ONE addend straight into dest, no add at all -- which is
        # what collapses c/op_13's `0 + (-1)*a` down to a bare
        # `mov %rdi,%rax; neg %rax`.
        keep = [a for a in args if as_immediate(a, prov) != 0]
        if keep and len(keep) < len(args):
            args = keep

    if op in ALU_OP:
        w = node.size()
        native_w = round_up_width(w)
        mnem = ALU_OP[op]
        gen(args[0], dest_base, pool, lines, prov)
        for extra in args[1:]:
            # STEP 7 fix (c/op_138, `a - b`): a NEGATED addend inside
            # a bvadd fold (`bvmul(x, -1)`, z3's own normal form for
            # subtraction, same shape as the negation fix above) was
            # rendered as its own `neg` PLUS the fold's `add` -- two
            # instructions doing exactly what one `sub` does. Detected
            # the same way, by literal multiplicand value, and only
            # when this IS a plain `bvadd` (never for bvor/bvxor/
            # bvand/bvmul, where "subtract" has no meaning).
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
                t = pool.alloc()
                gen(neg_operand, t, pool, lines, prov)
                emit_alu_source(
                    lines, ("leaf", t, native_w), "sub", dest_base,
                    native_w, pool)
                pool.release(t)
            elif z3.is_bv_value(extra):
                emit_alu_source(
                    lines, ("imm", extra.as_long(), native_w), mnem,
                    dest_base, native_w, pool)
            else:
                t = pool.alloc()
                gen(extra, t, pool, lines, prov)
                emit_alu_source(
                    lines, ("leaf", t, native_w), mnem, dest_base,
                    native_w, pool)
                pool.release(t)
        return w

    if op in ("bvshl", "bvlshr", "bvashr"):
        val_node, amt_node = args[0], args[1]
        w = val_node.size()
        native_w = round_up_width(w)
        gen(val_node, dest_base, pool, lines, prov)
        mnem = {"bvshl": "shl", "bvlshr": "shr",
                "bvashr": "sar"}[op]
        if z3.is_bv_value(amt_node):
            amt = amt_node.as_long()
            lines.append("%s $%d,%s" % (
                mnem, amt, reg_text(dest_base, native_w)))
        else:
            t = pool.alloc()
            gen(amt_node, t, pool, lines, prov)
            lines.append("mov %s,%%cl" % reg_text(t, 8))
            lines.append("%s %%cl,%s" % (
                mnem, reg_text(dest_base, native_w)))
            pool.release(t)
        return w

    if op == "extract":
        hi, lo = node.params()
        w = hi - lo + 1
        src_w = args[0].size()
        gen(args[0], dest_base, pool, lines, prov)
        cur_w = round_up_width(src_w)
        if lo > 0:
            lines.append("shr $%d,%s" % (
                lo, reg_text(dest_base, cur_w)))
        target_native = round_up_width(w)
        if target_native != cur_w or w not in NATIVE_WIDTHS:
            mask = mask_value(w)
            lines.append("and $%d,%s" % (
                mask, reg_text(dest_base, target_native)))
        return w

    if op == "concat":
        parts = list(node.children())
        total_w = node.size()
        sign_bit_re = None
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
                gen(last, dest_base, pool, lines, prov)
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
            src_w = parts[1].size()
            w = gen(parts[1], dest_base, pool, lines, prov)
            return total_w
        acc_w = parts[0].size()
        gen(parts[0], dest_base, pool, lines, prov)
        for nxt in parts[1:]:
            nxt_w = nxt.size()
            new_w = acc_w + nxt_w
            native_new = round_up_width(new_w)
            if round_up_width(acc_w) != native_new:
                lines.append("movzx %s,%s" % (
                    reg_text(dest_base, round_up_width(acc_w)),
                    reg_text(dest_base, native_new)))
            lines.append("shl $%d,%s" % (
                nxt_w, reg_text(dest_base, native_new)))
            t = pool.alloc()
            gen(nxt, t, pool, lines, prov)
            lines.append("or %s,%s" % (
                reg_text(t, round_up_width(nxt_w)),
                reg_text(dest_base, native_new)))
            pool.release(t)
            acc_w = new_w
        return total_w

    raise Unsupported("no rendering rule for z3 op %r" % op)


# --------------------------------------------------------------------
# Section 5: assemble/objdump, reusing canon2.py's own pattern
# (subprocess `as` + `objdump`, real-tool testimony).
# --------------------------------------------------------------------

import tempfile                                                # noqa: E402

ASM_PROLOGUE = ".text\n.globl op_unit\n.type op_unit,@function\n" \
    "op_unit:\n"


def assemble_and_disassemble(lines, workdir):
    src = ASM_PROLOGUE
    for line in lines:
        src = src + "\t" + line + "\n"
    src_path = os.path.join(workdir, "u.s")
    obj_path = os.path.join(workdir, "u.o")
    fh = open(src_path, "w")
    fh.write(src)
    fh.close()
    proc = subprocess.run(
        ["as", "--64", "-o", obj_path, src_path],
        capture_output=True, text=True)
    if proc.returncode != 0:
        return False, proc.stderr.strip()
    proc2 = subprocess.run(
        ["objdump", "-d", "--no-show-raw-insn", obj_path],
        capture_output=True, text=True)
    return True, proc2.stdout


# --------------------------------------------------------------------
# Section 6: per-unit driver
# --------------------------------------------------------------------

def render_unit(u, workdir):
    lang = u["lang"]
    n = u["n"]

    if u.get("sem_ok") is False:
        reason = u.get("refused") or "sem not ok"
        return "no return path: unit never reached a normal-path " \
            "root (%s)" % reason

    root_text = u.get("normal_path_root")
    if root_text is None:
        return "no return path: no return-bearing block with a " \
            "value (tree_match2's own normal_path_value found no " \
            "candidate)"

    if not u.get("normalize_ok"):
        return "no return path: z3 failed to normalize this " \
            "unit's lifted expression (%s); the raw VEX text is " \
            "retained verbatim in normal_path_root/normal_path_raw " \
            "with no bitvector normal form to render from" % \
            u.get("normalize_note", "unknown z3 failure")

    raw = u.get("normal_path_raw")
    if raw is None:
        return "no return path: normalize_ok is true but " \
            "normal_path_raw is missing from this unit's record"

    try:
        tree = parse_expr(raw)
    except Exception as exc:
        return "no return path: could not re-parse this unit's " \
            "own normal_path_raw text (%r)" % exc

    atoms = {}
    prov = {}
    try:
        expr = to_z3_with_prov(tree, atoms, prov)
        simplified = z3.simplify(expr)
    except Exception as exc:
        return "no return path: re-deriving the z3 expression from " \
            "normal_path_raw failed (%r) even though tree_match2 " \
            "recorded normalize_ok=true for it" % exc

    resim_text = str(simplified).replace("\n", " ").strip()
    stored_text = root_text
    if resim_text != stored_text:
        return "no return path: this renderer's own re-derivation " \
            "of the z3 normal form does not match tree_units2.json's " \
            "stored normal_path_root text (stored=%r, rederived=%r) " \
            "-- refusing rather than rendering a different " \
            "expression than the one on record" % (
                stored_text, resim_text)

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
                            head, call_text, err)
                ok, out = assemble_and_disassemble(dt, workdir)
                if not ok:
                    return "no return path: this unit's own " \
                        "canon2 derived_text for the divmod atom " \
                        "failed to re-assemble here (%s)" % out
                return list(dt)
            return refusal_reason_for_call(head)
        names = sorted(call_atoms.keys())
        heads = sorted(set(call_op_name(call_atoms[nm])
                            for nm in names))
        return "no return path: expression contains %d distinct " \
            "uninterpreted atoms (%s) -- this renderer only traces " \
            "a SINGLE scalar-divmod atom back to instructions, via " \
            "that unit's own canon2 record" % (len(call_atoms),
                                                ", ".join(heads))

    pool = Pool()
    lines = []
    try:
        w = gen(simplified, "ans", pool, lines, prov)
    except CallAtom as ca:
        return refusal_reason_for_call(call_op_name(ca.call_text))
    except NoTemps as exc:
        return "no return path: %s" % exc
    except Unsupported as exc:
        return "no return path: %s" % exc
    except Exception as exc:
        return "no return path: codegen raised %r rendering %r" % (
            exc, resim_text)

    native_w = round_up_width(w)
    ans_reg = reg_text("ans", native_w)
    if native_w != 32 and native_w != 64:
        return "no return path: final answer width %d bits has no " \
            "native x86-64 return register form" % native_w
    lines.append("ret")

    ok, out = assemble_and_disassemble(lines, workdir)
    if not ok:
        return "no return path: rendered instructions failed to " \
            "assemble (%s); rendered lines were: %s" % (
                out, "; ".join(lines))
    return list(lines)


def _is_trivial_wrapper_of_one_atom(node, atom_name, prov):
    """true if `node` is nothing but zero-extension/extraction of
    the ONE call atom (no combination with any other value) -- the
    shape tree_match2 actually produces for a scalar divmod result,
    e.g. `Concat(0, Extract(63, 32, op_3))`."""
    if z3.is_bv_value(node):
        return True
    if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
        return node.decl().name() == atom_name
    op = node.decl().name()
    if op not in ("concat", "extract"):
        return False
    for c in node.children():
        if not _is_trivial_wrapper_of_one_atom(c, atom_name, prov):
            return False
    return True


# --------------------------------------------------------------------
# Section 6b: CAUSE 4 -- the block-aware renderer for GUARDED
# (branching) units.  canon5's own docstring says why this did not
# exist before: render_unit() above reconstructs ONE straight-line
# scalar expression (the unit's single normal-path return value); a
# branching unit has several blocks, each potentially its OWN return
# value, plus real control flow (branches) that carry no "value" at
# all and so cannot go through a value-lift-simplify-render pipeline.
#
# THE FIX: per the owner's instruction, "emit each block's instructions
# plus its branch, using the normalized labels canon4/canon5 already
# store." canon4's own `derived_blocks` ALREADY is exactly that --
# real, register-canonicalized, positionally-labeled (L0, L1, ...)
# per-block instruction lists, already proven to assemble as a whole
# program (canon4's own roundtrip check). What canon4 does NOT do is
# run the transform-and-return step on each block's OWN return value
# the way canon5 does for straight-line units -- a branching unit's
# canon5_text was simply canon4's text, untouched, "not yet
# converged" by construction, never attempted.
#
# This renderer closes that gap per block: for every block whose OWN
# canon4 text ends in `ret` (a genuine leaf return path), find that
# SAME block's own lifted value in sem_anchored_spill (block id N
# <-> label "L%d", confirmed empirically on c/op_117: sem block 1's
# value is the smaller tree matching L1's `cvtsi2ss`+`addss` text,
# sem block 2's is the larger tree matching L2's `shr`/`and`/`or`
# text), pick that block's own largest-tree value (tree_match2's own
# per-block rule, unchanged, just scoped to one block instead of the
# whole unit), and run it through the SAME CAUSE 1/2/3-fixed lift ->
# normalize -> render pipeline render_unit() already uses for a whole
# straight-line unit.  A block that re-renders is REPLACED by its
# fresh rendering (still ending `ret`); a block that does not (any
# honest render_unit refusal) keeps canon4's OWN text for that block,
# never fabricated.  Guard/dispatch/trap/call-tail blocks (anything
# NOT ending in `ret`) are ALWAYS kept verbatim from canon4 -- there
# is no scalar value to lift on a pure branch, and this renderer does
# not invent one.
#
# The whole multi-block result -- some blocks fresh-rendered, some
# canon4-original, labels unchanged -- is then assembled+disassembled
# for real (`as`/`objdump`, this file's own assemble_and_disassemble,
# the SAME harness canon2/canon4 already use for the identical label
# format, confirmed by reading canon4.py's flatten_for_asm), never
# trusted unverified.
# --------------------------------------------------------------------

def _largest_block_value(values):
    """tree_match2's own per-block selection rule (candidate_values /
    normal_path_value in tree_match2.py), applied to ONE block's own
    `values` list: drop bare single-leaf values unless nothing else
    survives, take the largest remaining tree."""
    if not values:
        return None
    sized = [(v, TM.tree_size(TM.parse_expr(v))) for v in values]
    non_trivial = [(v, s) for v, s in sized if s > 1]
    pool = non_trivial if non_trivial else sized
    pool.sort(key=lambda vs: -vs[1])
    return pool[0][0]


def render_block_value(lang, n, raw_value_text, block_canon_lines, workdir):
    """runs ONE block's own value through the same CAUSE 1/2/3-fixed
    lift -> normalize -> render pipeline render_unit() uses for a
    whole straight-line unit.  Returns a rendered+assembled
    instruction list (ending in `ret`), or a "no return path: ..."
    string -- the SAME honest-refusal convention render_unit() uses."""
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
    return render_unit(synth, workdir)


def render_branching_unit(lang, n, canon4_rec, sem_blocks, workdir):
    """CAUSE 4 driver.  canon4_rec: this unit's own canon4_units_
    <lang>.json record (needs `derived_blocks`).  sem_blocks: this
    unit's sem_anchored_spill blocks list (`sem`, `blocks`).

    Returns (lines, per_block_report) on success (assembled), or a
    "no return path: ..." string naming why the WHOLE unit still
    refuses (this renderer never partially-emits an unassembled
    program)."""
    derived_blocks = canon4_rec.get("derived_blocks")
    if not derived_blocks:
        return "no return path: no derived_blocks on this unit's " \
            "canon4 record"
    sem_by_label = {}
    for b in sem_blocks:
        sem_by_label["L%d" % b.get("block", -1)] = b

    # canon4's OWN derived_text_flat convention (see canon4.py's
    # flatten_for_asm): label lines bare, instruction lines carry a
    # two-space indent. Matched here byte-for-byte so a block kept
    # canon4_verbatim compares EQUAL to canon4_text (this unit's own
    # "; ".join(derived_text_flat)) -- otherwise every unit would
    # misreport as "converged" by pure whitespace, even when nothing
    # about its rendering changed.
    def emit(label, steps):
        flat_lines.append("%s:" % label)
        for s in steps:
            flat_lines.append("  " + s)

    flat_lines = []
    per_block = []
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
        result = render_block_value(lang, n, value, steps, workdir)
        if isinstance(result, list):
            # BEHAVIOUR-PRESERVATION GATE, found necessary while
            # verifying this very renderer (see report): a block that
            # is only reachable AFTER an earlier block destructively
            # mutated the entry registers IN PLACE (real example:
            # swift/op_13's `-a`, where L0's `neg %rdi` overwrites the
            # argument register before falling into L1) has a
            # PRECONDITION on its registers that is not the pristine
            # entry contract -- re-rendering that block from "a is
            # whatever %rdi holds" (the ONLY convention this renderer
            # or ANY per-block rendering can assume without a full
            # cross-block dataflow analysis, out of scope here) is
            # unsound for exactly that block. Rather than emit a
            # rendering that LOOKS right and is not, every substitution
            # is proved against the block's own canon4 text first,
            # same-seed z3 equivalence (canon6_behaviour_check.py's
            # own checker, imported here so there is exactly one
            # proof routine) -- accepted only if PROVED_EQUAL, ALWAYS
            # falling back to canon4's real, already-assembled text
            # otherwise. Never a silent wrong answer.
            import canon6_behaviour_check as C6BC
            verdict, detail = C6BC.check_pair(
                "; ".join(steps), "; ".join(result))
            if verdict == "PROVED_EQUAL":
                emit(label, result)
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
                    "contract (an earlier block mutated them in "
                    "place); falling back rather than risk a wrong "
                    "answer" % (verdict, detail[:200])))
        else:
            emit(label, steps)
            per_block.append(dict(label=label, source="canon4_verbatim",
                                   reason=result))

    ok, out = assemble_and_disassemble(flat_lines, workdir)
    if not ok:
        return "no return path: block-stitched rendering failed to " \
            "assemble (%s); lines were: %s" % (out, "; ".join(flat_lines))
    return flat_lines, per_block


# --------------------------------------------------------------------
# Section 7: main
# --------------------------------------------------------------------

def main():
    src_path = os.path.join(HERE, "tree_units2.json")
    doc = json.load(open(src_path))
    units = doc["units"]

    workdir = tempfile.mkdtemp(prefix="expr_to_canon_")

    n_ok = 0
    n_refused = 0
    reasons = {}

    for u in units:
        result = render_unit(u, workdir)
        u["canonical_return"] = result
        if isinstance(result, list):
            n_ok = n_ok + 1
        else:
            n_refused = n_refused + 1
            key = result.split(" -- ")[0].split(" (")[0][:80]
            reasons[key] = reasons.get(key, 0) + 1

    out_path = os.path.join(HERE, "tree_units3.json")
    doc["canonical_return_generator"] = "expr_to_canon.py"
    doc["canonical_return_ok"] = n_ok
    doc["canonical_return_refused"] = n_refused
    json.dump(doc, open(out_path, "w"), indent=1)

    print("total units:", len(units))
    print("canonical_return rendered+assembled:", n_ok)
    print("no return path:", n_refused)
    print()
    print("refusal reasons (truncated key -> count):")
    for k in sorted(reasons, key=lambda x: -reasons[x]):
        print(" %5d  %s" % (reasons[k], k))
    return 0


if __name__ == "__main__":
    sys.exit(main())
