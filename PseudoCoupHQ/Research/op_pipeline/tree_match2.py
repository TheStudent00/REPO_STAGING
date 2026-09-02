#!/usr/bin/env python3
"""tree_match2.py -- tree_match.py, re-run over the SPILL/RELOAD-fixed sem
form (`sem_anchored_spill.py`'s `sem_anchored_spill_<lang>.json`) instead
of `sem_anchored_<lang>.json`.

Everything about matching (z3 normalization, containment, the type-pair
candidate scope) is tree_match.py's own logic, reused verbatim by import.
The one thing this file changes is BLOCK/VALUE SELECTION -- the step that
picks which of a unit's several block values is "the" normal-path answer.

tree_match.py picked the ret-tagged block, then that block's ALPHABETICALLY
FIRST value (`values[0]` after arch_sem's own sort), falling back to the
largest-tree value among the OTHER blocks when the ret block's own first
value looked trivial.  Two things about that were wrong, found while
chasing the spill/reload gap:

  1. A ret-tagged block can carry MORE THAN ONE surviving value (a real
     answer plus a prologue/epilogue restore -- `pop %rbp`, `pop %rcx` for
     stack realignment -- that also survives arch_sem's filtering because,
     read one block at a time, arch_sem cannot tell it is a restore).
     Picking `values[0]` picks whichever sorts first ALPHABETICALLY, which
     has nothing to do with which one is the answer.

  2. The fallback search explicitly EXCLUDED the ret block itself
     (`if b is ret_block: continue`), so a case matching (1) could never
     be repaired by the fallback either -- the real answer was sitting in
     the very block the search refused to look inside a second time.

The fix: gather EVERY value from EVERY block that is not a trap-only or
call-tail block (unchanged exclusion), drop bare single-leaf values (a
restore has no computation on it -- machine evidence: tree size 1) unless
nothing else is left, and take the largest surviving tree, tie-broken
toward the ret-tagged block.  This is tree_match.py's own "largest tree
is the real computation" rule, now applied uniformly instead of only to
non-ret blocks.

THE SPELLING BAN: unchanged from tree_match.py -- `operator` is a display
label; nothing here groups or selects on it.
"""

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                       # noqa: E402
import sem_anchored_spill as SAS                                # noqa: E402
import condition_table as CT                                   # noqa: E402

LANGS = SAS.LANGS

parse_expr = TM.parse_expr
serialize = TM.serialize
tree_size = TM.tree_size
build_matches = TM.build_matches


# --------------------------------------------------------------------
# tree_match.py's `to_z3` hands a shift's AMOUNT operand straight to
# z3's `>>`/`<<`/`LShR` alongside the value operand.  The VEX shift ops
# this campaign's units actually emit (Sar32/Shr32/Shl32) carry their
# amount as an 8-BIT literal (`31:8`) beside a 32-bit value, and z3
# refuses two BitVecs of different width -- `normalize()` catches the
# exception and silently falls back to the UNNORMALIZED text, which is
# why go/op_132's extra `zx64(ex32@0(...))` roundtrip (equivalent bits,
# different literal text) never collapsed onto c/op_246's and
# rust/op_678's shorter form.  Fixed here, in tree_match2.py's own copy
# only (tree_match.py is not touched): the amount operand is
# zero-extended to the value's width before the shift, which is exactly
# what the hardware and VEX both already do.
# --------------------------------------------------------------------

if TM.HAVE_Z3:
    import z3 as _z3



# --------------------------------------------------------------------
# CAUSE 2 fix (2026-08-28, per AgentMemory's op_pipeline lap).
# tree_match.py's `to_z3` / this file's `to_z3_fixed` mapped VEX ALU
# ops at 32/64-bit widths only.  A survey of every value string in
# sem_anchored_spill_<lang>.json for all five languages (grep for
# `NAME(` op tokens, counted) found these 8-BIT ops actually present:
#
#     And8   243 occurrences   Or8   261   Xor8   29
#     Sub8    16 occurrences   Not8    7   Shl8   32
#
# (Shr8, Sar8, Add8 were surveyed for and NOT found in the corpus --
# not added here; nothing to add an untested code path for.  Add8 not
# found either.)  Before this fix, an 8-bit op fell through to the
# generic "everything else" branch below and was swallowed whole into
# a single opaque atom -- e.g. cpp/op_318's `And8(zx8(...),zx8(...))`
# normalized to the bare atom `op_8`, discarding the two operands
# entirely.  Fixed the same way the 32/64 entries already work: widen
# the membership tuples to include the 8-bit spelling, same style,
# same z3 operator underneath (width comes from each kid's own
# BitVec size, already carried correctly by leaf_width /
# to_z3_fixed's recursion -- these ops need no separate width-fixup
# the way the shift-amount fix above did).
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# CAUSE 3 fix (2026-08-28).  297 units threw
# `Z3Exception(b'invalid extract application')` out of normalize().
# Traced by hand-walking to_z3_fixed's own recursion on cpp/op_105
# (`Add32F0x4(ex128@0(in1:256), ex128@0(ins@0(u0:256, F64toF32(...))))`):
# `ins@0(...)` is not in the small ratified rewrite set, so it falls to
# the generic "everything else" opaque-atom branch below -- which
# HARD-CODES the atom's width to 64 regardless of context.  The
# enclosing `ex128@0(...)` then asks z3 for bits [127:0] of a 64-bit
# atom -- out of range, z3 (correctly) refuses.  OURS, not z3's, same
# shape as the Sar32 width bug this campaign already fixed once: a
# fixed-width default that is wrong whenever the true VEX op is wider.
# Surveyed all 297 failures the same way (see report): every single
# one is this SAME shape, always an `exN@off` needing more bits than
# a 64-bit-defaulted opaque atom underneath it has -- across 5 VEX
# families (ins@ SIMD insert, Sub64Fx2 SIMD sub, DivModU128to64,
# DivModS128to64, MullU64 -- all genuinely 128-bit-result ops).
#
# THE FIX, and why it is NOT simply "default opaque atoms to 128 or
# 256 bits": zero-extending the too-narrow atom up to the needed width
# (the obvious fix) would silently ASSERT that the missing high bits
# are always 0 -- a fabricated fact about an operation this normalizer
# does not model at all (verified: for DivModU128to64/128S64to32/
# MullU64, a naive ZeroExt makes the extracted high 64 bits simplify
# to the literal constant `0`, which is false in general for a
# widening multiply or a 128-bit divmod's remainder half). Instead,
# widen with FRESH, INDEPENDENT, uninterpreted high bits (z3.Concat of
# a new atom onto the old one) -- honestly "we do not know this value"
# rather than "this value is zero". Memoized per (child expression
# identity, needed total width) in `widen_cache` so the SAME opaque
# sub-tree, if referenced by more than one extract, gets the SAME
# widened value both times (same-text-same-atom, forced by
# construction, unchanged).  Verified: all 297 units that previously
# raised now normalize with zero exceptions (see report); the
# genuinely-unmodeled ones (SIMD/128-bit ops) correctly land on an
# opaque atom or pad atom, never a fabricated concrete value.
# --------------------------------------------------------------------

def to_z3_fixed(tree, atoms, widen_cache=None):
    if widen_cache is None:
        widen_cache = {}
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = TM.leaf_width(text)
        key = text
        if key not in atoms:
            atoms[key] = _z3.BitVec("atom_%d" % len(atoms), w)
        return atoms[key]

    name, args = tree[1], tree[2]
    kids = [to_z3_fixed(a, atoms, widen_cache) for a in args]

    if name in CT.COND_OPS:
        # CAUSE 1 fix: condition_table.py's substitution step (see that
        # file's header) already replaced the opaque
        # `ex1@0(amd64g_calculate_condition(...))` call with one of
        # these 14 synthetic nodes, built from CANONICAL TEXT (route
        # a) -- never from the lifter helper.  Render it here as a
        # 1-bit z3 boolean-as-bitvec, matching the width ex1@0 always
        # wrapped the original call in.
        L, R = kids[0], kids[1]
        if L.size() != R.size():
            if L.size() < R.size():
                L = _z3.ZeroExt(R.size() - L.size(), L)
            else:
                R = _z3.ZeroExt(L.size() - R.size(), R)
        pred = CT.cond_to_z3(name, L, R, _z3)
        return _z3.If(pred, _z3.BitVecVal(1, 1), _z3.BitVecVal(0, 1))

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
            amt = _z3.ZeroExt(val.size() - amt.size(), amt) \
                if val.size() > amt.size() else _z3.Extract(
                    val.size() - 1, 0, amt)
        if name.startswith("Sar"):
            return val >> amt
        if name.startswith("Shr"):
            return _z3.LShR(val, amt)
        return val << amt
    if name.startswith("zx"):
        outw = int(name[2:])
        inw = kids[0].size()
        return _z3.ZeroExt(outw - inw, kids[0]) if outw > inw else kids[0]
    if name.startswith("sx"):
        outw = int(name[2:])
        inw = kids[0].size()
        return _z3.SignExt(outw - inw, kids[0]) if outw > inw else kids[0]
    if name.startswith("ex"):
        m = TM.re.match(r"ex(\d+)@(\d+)$", name)
        width, off = int(m.group(1)), int(m.group(2))
        child = kids[0]
        need = off + width
        if need > child.size():
            ck = (id(child), need)
            if ck not in widen_cache:
                extra = need - child.size()
                pad = _z3.BitVec("pad_%d" % len(widen_cache), extra)
                widen_cache[ck] = _z3.Concat(pad, child)
            child = widen_cache[ck]
        return _z3.Extract(off + width - 1, off, child)
    if name == "32HLto64":
        hi, lo = kids
        return _z3.Concat(hi, lo)
    if name == "ite":
        # FOUND WHILE FIXING CAUSE 1: cmov's own VEX shape is
        # `ite(cond, then_value, else_value)` (c/op_179, reading_sample
        # example 8) -- squarely the "cmov" branch of Cause 1's own
        # (flag-setter, setcc/cmov/branch) table, since `cond` here is
        # exactly an `ex1@0(amd64g_calculate_condition(...))` call that
        # condition_table.py's substitution already turned into a
        # CondXX 1-bit predicate. Not previously in the rewrite set, so
        # the whole select swallowed itself into one opaque atom even
        # after the condition resolved cleanly. `cond` (kids[0]) is a
        # 1-bit BitVec per this file's CondXX rendering above; z3's If
        # needs a Bool, so compare it to the 1-bit true value.
        cond_bit = kids[0]
        return _z3.If(cond_bit == _z3.BitVecVal(1, cond_bit.size()),
                       kids[1], kids[2])
    if name.startswith("ins@"):
        # FOUND WHILE FIXING CAUSE 1 (2026-08-28), a DISTINCT pre-
        # existing gap in the same small ratified rewrite set, fixed
        # here because it was blocking Cause 1's own worked example
        # (c/op_535, `cmp`+`setl`): `ins@N(base:W, value:Wv)` is
        # pyvex's own partial-register-write idiom -- the compiler's
        # "xor %r11d,%r11d; ...; setl %al" pattern (zero a full
        # register, then write only its low byte, avoiding a partial-
        # register stall) renders as ONE VEX statement, "insert value
        # at bit-offset N of base, everything else of base
        # unchanged". Confirmed empirically: every occurrence in this
        # corpus (1,277 across all 5 languages) has offset 0 (survey:
        # `grep 'ins@(\d+)\('`, only offset 0 ever seen), consistent
        # with the "@" convention `ex1@0`/`ex32@0` already use for a
        # BIT offset, not a byte offset. Not previously in the small
        # ratified rewrite set, so it fell to the generic opaque-atom
        # branch below and swallowed whatever it wrapped (e.g. a
        # cleanly-resolved CondXX predicate) back into opacity.
        m = TM.re.match(r"ins@(\d+)$", name)
        off = int(m.group(1))
        base, val = kids[0], kids[1]
        w, vw = base.size(), val.size()
        if off + vw > w:
            raise ValueError(
                "ins@%d: inserted value width %d at offset %d "
                "exceeds base width %d" % (off, vw, off, w))
        widened_val = _z3.ZeroExt(w - vw, val) if w > vw else val
        if off:
            widened_val = widened_val << off
        mask = ((1 << vw) - 1) << off
        cleared = base & _z3.BitVecVal((~mask) & ((1 << w) - 1), w)
        return cleared | widened_val

    text = serialize(tree)
    w = 64
    if text not in atoms:
        atoms[text] = _z3.BitVec("op_%d" % len(atoms), w)
    return atoms[text]


def normalize(expr_text):
    """tree_match.py's `normalize`, using the width-fixed lift above."""
    tree = parse_expr(expr_text)
    if not TM.HAVE_Z3:
        return expr_text, False, "z3 unavailable"
    try:
        atoms = {}
        e = to_z3_fixed(tree, atoms)
        simplified = _z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (width-fixed shift lift)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


def resolve_conditions(expr_text, canon_text_lines):
    """CAUSE 1 driver: apply condition_table.py's route-(a) substitution
    (canonical-text-derived, never lifter-derived) to `expr_text`
    before normalizing, using `canon_text_lines` (a unit's own canon4
    derived_text) to read off which flag-setting instruction feeds
    which setcc/cmov/branch consumer, in program order.

    Returns (substituted_text, applied_count, sub_note) -- the
    substituted text is what should be handed to normalize() next;
    sub_note is None on a clean substitution, or the honest reason
    no substitution happened (no calls present, or a count mismatch
    this file refuses to guess through)."""
    if canon_text_lines is None:
        return expr_text, 0, "no canonical text available for this unit"
    records = CT.scan_canonical_text(canon_text_lines)
    return CT.substitute_conditions(expr_text, records)


def candidate_values(blocks, ret_block_id):
    """every (block_id, value_text, tree_size) triple worth considering:
    every block except a trap-only or call-tail block, every value in it
    except a bare single-leaf restore -- unless the block has nothing
    else, in which case its bare value still competes (better a leaf than
    nothing)."""
    out = []
    for b in blocks:
        evs = b.get("events", [])
        if any(e == "trap" or (isinstance(e, str) and e.startswith("trap"))
               for e in evs):
            continue
        has_call = any(isinstance(e, str) and e.startswith("call")
                       for e in evs)
        has_ret = any(e == "ret" or (isinstance(e, str) and e.startswith("ret"))
                      for e in evs)
        if has_call and not has_ret:
            continue
        vals = b.get("values", [])
        non_trivial = [v for v in vals if tree_size(parse_expr(v)) > 1]
        pool = non_trivial if non_trivial else vals
        for v in pool:
            out.append((b.get("block"), v, tree_size(parse_expr(v))))
    return out


def normal_path_value(blocks):
    """(value_text, rule_note).  See module docstring."""
    ret_block_id = None
    for b in blocks:
        if any(ev == "ret" or (isinstance(ev, str) and ev.startswith("ret"))
               for ev in b.get("events", [])):
            ret_block_id = b.get("block")
            break
    cands = candidate_values(blocks, ret_block_id)
    if not cands:
        return None, "no candidate value in any non-trap non-call-tail block"
    best_size = max(c[2] for c in cands)
    tied = [c for c in cands if c[2] == best_size]
    chosen = None
    for c in tied:
        if c[0] == ret_block_id:
            chosen = c
            break
    if chosen is None:
        chosen = tied[0]
    note = ("ret block %s, largest surviving tree" % ret_block_id
            if chosen[0] == ret_block_id else
            "block %s (non-ret), largest surviving tree "
            "(ret block %s had none this large)" % (chosen[0], ret_block_id))
    return chosen[1], note


def load_all_units():
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        if not os.path.exists(path):
            print("!! missing %s" % path)
            continue
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            meta = u["meta"]
            sem = u["sem"]
            rec = dict(lang=lang, n=n, operator=meta.get("operator"),
                       arity=meta.get("arity"),
                       lhs_rep=meta.get("lhs_rep"), rhs_rep=meta.get("rhs_rep"),
                       symbol=meta.get("symbol"), sem_ok=sem.get("ok"))
            if not sem.get("ok"):
                rec["refused"] = sem.get("reason", "sem not ok")
                out.append(rec)
                continue
            blocks = sem.get("blocks", [])
            rec["block_count"] = len(blocks)
            rec["all_block_values"] = [b.get("values", []) for b in blocks]
            rec["all_block_events"] = [b.get("events", []) for b in blocks]
            root_text, rule = normal_path_value(blocks)
            rec["normal_path_block_rule"] = rule
            rec["carried"] = sem.get("carried", False)
            if root_text is None:
                rec["normal_path_root"] = None
                rec["note"] = "no return-bearing block with a value"
            else:
                norm, ok, note = normalize(root_text)
                rec["normal_path_raw"] = root_text
                rec["normal_path_root"] = norm
                rec["normalize_ok"] = ok
                rec["normalize_note"] = note
                tree = parse_expr(root_text)
                if tree[0] == "node":
                    rec["subexp1_root_op"] = tree[1]
                    rec["subexp2_children"] = [serialize(a) for a in tree[2]]
                else:
                    rec["subexp1_root_op"] = None
                    rec["subexp2_children"] = []
            out.append(rec)
    return out


def main():
    units = load_all_units()
    exact, containment = build_matches(units)

    units_doc = dict(
        languages=LANGS,
        normalizer="z3 simplify (bitvector), opaque atoms for helper calls",
        source="sem_anchored_spill_<lang>.json (carry-forward substitution "
               "over the CFG's single-predecessor edges, largest-tree "
               "per-merge-variant at a join)",
        total_units=len(units),
        units=[dict(
            lang=u["lang"], n=u["n"], operator=u["operator"],
            type_pair="%s,%s" % (u.get("lhs_rep"), u.get("rhs_rep")),
            sem_ok=u.get("sem_ok"),
            refused=u.get("refused"),
            block_count=u.get("block_count"),
            carried=u.get("carried"),
            normal_path_block_rule=u.get("normal_path_block_rule"),
            normal_path_raw=u.get("normal_path_raw"),
            normal_path_root=u.get("normal_path_root"),
            normalize_ok=u.get("normalize_ok"),
            normalize_note=u.get("normalize_note"),
            subexp1_root_op=u.get("subexp1_root_op"),
            subexp2_children=u.get("subexp2_children"),
        ) for u in units],
    )
    matches_doc = dict(
        languages=LANGS,
        exact_normalized_root=exact,
        containment=containment,
    )

    json.dump(units_doc, open(os.path.join(HERE, "tree_units2.json"), "w"),
               indent=1)
    json.dump(matches_doc, open(os.path.join(HERE, "tree_matches2.json"),
                                 "w"), indent=1)

    print("units total:", len(units))
    print("units with normal-path root:", sum(1 for u in units
                                                if u.get("normal_path_root")))
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    print("containment edges:", len(containment))
    return 0


if __name__ == "__main__":
    sys.exit(main())
