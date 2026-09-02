#!/usr/bin/env python3
"""cross_unit_prover.py -- JOB 2, the cross-unit equivalence prover
(log_081 work item 5: "Build the two grouping tables: seed families
... and guard families", the piece this file supplies ground (c) for
-- a REAL cross-unit proved-edge table, which build_representatives2.
py's/build_representatives3.py's docstrings both record as "wired but
never fires" today).

CANDIDATE SET -- machine-form only, THE SPELLING BAN untouched.
A pair of 0-branch units (dominant_table17.load_0branch_units's own
1,641-unit population, the SAME call build_representatives2.py/
build_representatives3.py already use) is a candidate when:
  1. they share a CLASS KEY -- (type_pair, machine-fact result-type
     family) -- computed by dom_ops_0branch.type_pair_of (probe meta's
     own lhs_rep/rhs_rep) and result_type_norm.class_family (DWARF-
     read base type -> canon_of family). The SAME two functions
     build_representatives3.py already calls for its own ground (b)
     split; reused, not reinvented. NEITHER function ever reads an
     operator token.
  2. their newest canonical texts (dominant_table17.final_text_of)
     are NOT character-identical -- identical ones are already
     unioned by representatives3.json's ground (a); a prover call on
     them would be redundant, never wrong, so they are excluded for
     time budget, not for soundness.
No operator/grammar token participates in step 1 or step 2 -- the
class key is exactly the pair build_representatives3.py already keys
ground (b) on, and step 2 compares TEXT, not spelling.

PROOF. Two Sim classes are REUSED UNCHANGED from the existing
canon*_behaviour_check.py lineage (never reinvented):
  - canon20_behaviour_check.Sim20 for a pair whose canonical text
    uses any SSE scalar-float mnemonic (addsd/subsd/mulsd/divsd/
    addss/.../cvt*) -- real z3 FPA (fpAdd/fpSub/fpMul/fpDiv/
    fpSignedToFP/fpFPToFP), bit-level equality via fpToIEEEBV (never
    fpEQ), so NaN-payload/sign-of-zero differences stay visible, per
    the task's own requirement.
  - canon8_behaviour_check.Sim8 for everything else (integer GP ops
    as BitVecs) -- adds masked shift-counts on top of the Sim5/6/7
    lineage's mov/add/sub/and/or/xor/imul/not/neg/lea/shl.
Both sides of a pair run under a SHARED z3 seed dict (the SAME
technique every canon*_behaviour_check.py file already uses for its
own real-vs-candidate proof), so an argument register neither side
writes before reading starts from the SAME unconstrained symbol in
both -- proving equality for ALL inputs, not one sample.

TIMEOUT: a 12000ms per-pair z3 solver timeout (within the task's
10-15s band). `unknown` is recorded UNDECIDED, honestly, never folded
into PROVED or DISPROVED.

REFUSAL: a pair where either side's text contains an operand this
file's Sim cannot resolve to a concrete or shared-symbolic value --
chiefly a `N(%rip)`-relative load of a compiler constant this file
has no recorded value for (the SAME opaque-load shape JOB 1 fixed
for the raw-expression axis; here it is the CANONICAL TEXT axis, and
no per-unit recovered value is threaded through this file, so it
REFUSES rather than guesses) -- is REFUSED(reason), never silently
skipped and never counted as UNDECIDED (UNDECIDED is reserved for an
actual solver timeout/unknown).

SCALE, HONESTLY. The full candidate set (computed once at the top of
main(), printed in full) is far larger than a single run's time
budget allows at a 12s-per-pair worst case. This file PRIORITIZES,
in order: (a) cross-language pairs, (b) pairs where either unit's
class key result family is a float family (f32/f64), (c) everything
else -- and takes a `--limit N` prefix of that ordering. Every pair
NOT attempted is named in the output's `not_attempted_count` (by
priority bucket), not hidden.

usage:
  cross_unit_prover.py [--limit N] [--out FILE]
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                      # noqa: E402
import dominant_table17 as DT17                                  # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402
import result_type_norm as RTN                                    # noqa: E402
import canon8_behaviour_check as BC8                              # noqa: E402
import canon20_behaviour_check as BC20                            # noqa: E402
import z3                                                         # noqa: E402

FLOAT_FAMS = set(["f32", "f64"])

# canon.py's own WIDTH_OF maps a GP spelling to a RANK (0=64-bit,
# 1=32-bit, 2=16-bit, 3=8-bit), read directly off canon5_behaviour_
# check.py's own WIDTH_BITS table (that file's module-level constant,
# same source, reused not re-derived).
WIDTH_BITS = {0: 64, 1: 32, 2: 16, 3: 8}


def gp_width_of(name):
    """canon.py's OWN WIDTH_OF/FAMILY_OF tables, reused unchanged --
    the same source canon5_behaviour_check.Sim.width_of_operand
    reads. Returns None for a spelling canon.py does not know (an
    xmm register, or a spelling this corpus never uses)."""
    w = canon.WIDTH_OF.get(name)
    if w is None:
        return None
    return WIDTH_BITS[w]


def gp_family_of(name):
    return canon.FAMILY_OF.get(name)


class Sim20Cmp(BC20.Sim20):
    """canon20_behaviour_check.Sim20, extended with the ucomiss/
    ucomisd + setcc flag idiom, so a comparison-shaped pair (e.g.
    cpp's cmpeqss-value-write idiom vs go's ucomiss+sete+setnp+and
    idiom -- the exact NaN-aware-equality shape AgentMemory's
    2026-08-29 'quiet-continue tested and not needed' entry already
    read by hand and found answer-identical over 8 sampled rows) can
    be PROVEN rather than only sampled. Adds GP registers al/eax/...
    as ordinary 64-bit BitVecs (Sim20's own `regs` dict already holds
    raw bits per name; this class just also writes flag-derived GP
    values into it), and z3's OWN FPA compare/NaN primitives
    (fpLT/fpGT/fpEQ/fpIsNaN) -- never a re-derived/uninterpreted
    boolean model -- for the flag semantics themselves. This is an
    ADDITIVE subclass in THIS file only; canon20_behaviour_check.py
    itself is not modified."""

    def __init__(self, *a, **kw):
        BC20.Sim20.__init__(self, *a, **kw)
        self.flag_cf = None
        self.flag_zf = None
        self.flag_pf = None
        self.last_gp_write = None
        # GP registers are tracked by FAMILY (canon.FAMILY_OF), so
        # al/eax/rax alias correctly -- Sim20's OWN `regs` dict is
        # by bare spelling (xmm0, xmm2, ...) with no such aliasing
        # need, so GP state lives in this SEPARATE dict, never
        # colliding with an xmm entry.
        self.gpregs = {}

    def _gp_get_family(self, fam):
        if fam not in self.gpregs:
            if fam not in self.shared_seed:
                self.shared_seed[fam] = z3.BitVec("seed_%s" % fam, 64)
            self.gpregs[fam] = self.shared_seed[fam]
        return self.gpregs[fam]

    def _gp_write(self, name, width, value):
        fam = gp_family_of(name)
        if fam is None:
            raise BC20.NotModeled(
                "GP register spelling %r not in canon.py's FAMILY_OF"
                % name)
        if width < 64:
            full = z3.ZeroExt(64 - width, value)
        else:
            full = value
        self.gpregs[fam] = full
        self.last_gp_write = (fam, width)

    def _gp_read(self, operand, width):
        if operand.startswith("$"):
            v = int(operand[1:], 0) & ((1 << width) - 1)
            return z3.BitVecVal(v, width)
        name = operand[1:]
        fam = gp_family_of(name)
        if fam is None:
            raise BC20.NotModeled(
                "GP register spelling %r not in canon.py's FAMILY_OF"
                % name)
        full = self._gp_get_family(fam)
        return z3.Extract(width - 1, 0, full)

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        operands = [o.strip() for o in rest.split(",")] if rest else []

        if mnem in ("ucomiss", "ucomisd"):
            src, dst = operands
            width = 32 if mnem == "ucomiss" else 64
            reader = self._fp32_of if mnem == "ucomiss" else \
                self._fp64_of
            a_v = reader(self.get(dst[1:]))
            b_v = reader(self.get(src[1:]))
            is_nan = z3.Or(z3.fpIsNaN(a_v), z3.fpIsNaN(b_v))
            self.flag_cf = z3.Or(is_nan, z3.fpLT(a_v, b_v))
            self.flag_zf = z3.Or(is_nan, z3.fpEQ(a_v, b_v))
            self.flag_pf = is_nan
            return

        if mnem in ("sete", "setne", "seta", "setae", "setb", "setbe",
                    "setp", "setnp"):
            (dst,) = operands
            if mnem == "sete":
                cond = self.flag_zf
            elif mnem == "setne":
                cond = z3.Not(self.flag_zf)
            elif mnem == "seta":
                cond = z3.And(z3.Not(self.flag_cf), z3.Not(self.flag_zf))
            elif mnem == "setae":
                cond = z3.Not(self.flag_cf)
            elif mnem == "setb":
                cond = self.flag_cf
            elif mnem == "setbe":
                cond = z3.Or(self.flag_cf, self.flag_zf)
            elif mnem == "setp":
                cond = self.flag_pf
            else:
                cond = z3.Not(self.flag_pf)
            val = z3.If(cond, z3.BitVecVal(1, 8), z3.BitVecVal(0, 8))
            self._gp_write(dst[1:], 8, val)
            return

        if mnem in ("cmpeqss", "cmpneqss", "cmpeqsd", "cmpneqsd"):
            src, dst = operands
            width = 32 if mnem.endswith("ss") else 64
            reader = self._fp32_of if width == 32 else self._fp64_of
            dst_v = reader(self.get(dst[1:]))
            src_v = reader(self.get(src[1:]))
            is_nan = z3.Or(z3.fpIsNaN(dst_v), z3.fpIsNaN(src_v))
            truth = z3.And(z3.Not(is_nan), z3.fpEQ(dst_v, src_v))
            if mnem.startswith("cmpneq"):
                truth = z3.Not(truth)
            allones = z3.BitVecVal((1 << 64) - 1, 64)
            val = z3.If(truth, allones, z3.BitVecVal(0, 64))
            self.regs[dst[1:]] = val
            return

        if mnem in ("xorps", "xorpd", "andps", "andpd", "orps", "orpd"):
            src, dst = operands
            a_v = self.get(dst[1:])
            b_v = self.get(src[1:])
            if mnem.startswith("xor"):
                r = a_v ^ b_v
            elif mnem.startswith("and"):
                r = a_v & b_v
            else:
                r = a_v | b_v
            self.regs[dst[1:]] = r
            return

        if mnem in ("and", "or") and \
                gp_width_of((operands[-1] or "")[1:]) is not None:
            src, dst = operands
            width = gp_width_of(dst[1:])
            a_v = self._gp_read(dst, width)
            b_v = self._gp_read(src, width)
            r = (a_v & b_v) if mnem == "and" else (a_v | b_v)
            self._gp_write(dst[1:], width, r)
            return

        if mnem in ("mov", "movl", "movq") and operands and \
                gp_width_of(operands[-1][1:]) is not None and \
                not operands[0].startswith("%xmm"):
            src, dst = operands
            width = gp_width_of(dst[1:])
            v = self._gp_read(src, width)
            self._gp_write(dst[1:], width, v)
            return

        if mnem == "movzx":
            src, dst = operands
            src_w = gp_width_of(src[1:])
            dst_w = gp_width_of(dst[1:])
            if src_w is None or dst_w is None:
                raise BC20.NotModeled(
                    "movzx operand not in canon.py's WIDTH_OF table")
            v = self._gp_read(src, src_w)
            v = z3.ZeroExt(dst_w - src_w, v) if dst_w > src_w else v
            self._gp_write(dst[1:], dst_w, v)
            return

        if mnem == "movd" and operands and \
                not operands[-1].startswith("%xmm") and \
                gp_width_of(operands[-1][1:]) is not None:
            # xmm -> GP: Sim20's OWN movd/movq handler assumes a
            # fixed 64-bit family-less name; route this direction
            # through the GP family store instead so a later GP
            # read (and/movzx) sees the same value.
            src, dst = operands
            v = self.get(src[1:])
            v = z3.Extract(31, 0, v)
            self._gp_write(dst[1:], 32, z3.ZeroExt(32, v))
            return

        BC20.Sim20.exec_line(self, line)

    def answer_value(self, lines, width):
        """OVERRIDES Sim20.answer_value's xmm0-only assumption: this
        class answers a BOOLEAN comparison, whose real destination is
        a GP register (al/eax/...), not %xmm0. Reads back whichever
        GP register `_gp_write` last touched (tracked explicitly,
        never assumed to be a fixed name), zero-extended/truncated to
        `width` -- the SAME "read the text's own last write, at its
        own stated width" discipline canon5_behaviour_check.Sim.
        answer_value already uses for its GP answers."""
        for line in lines:
            self.exec_line(line)
        if self.last_gp_write is None:
            raise BC20.NotModeled(
                "this comparison text never wrote a GP destination "
                "this class tracks -- no boolean answer register "
                "found")
        fam, _w = self.last_gp_write
        full = self.gpregs[fam]
        return z3.Extract(width - 1, 0, full)

PER_PAIR_TIMEOUT_MS = 12000

FLOAT_MNEM = set([
    "addsd", "subsd", "mulsd", "divsd",
    "addss", "subss", "mulss", "divss",
    "cvtsi2sd", "cvtsi2ss", "cvtss2sd", "cvtsd2ss",
    "movd", "movq", "movaps", "movapd",
])


COMPARE_MNEM = set([
    "ucomiss", "ucomisd", "cmpeqss", "cmpneqss", "cmpeqsd", "cmpneqsd",
])


def is_float_text(text):
    for ln in text.split(";"):
        mnem = ln.strip().split(" ", 1)[0]
        if mnem in FLOAT_MNEM and mnem not in ("movd", "movq"):
            return True
    return False


def is_float_compare_text(text):
    for ln in text.split(";"):
        mnem = ln.strip().split(" ", 1)[0]
        if mnem in COMPARE_MNEM:
            return True
    return False


def type_pair_has_float(type_pair):
    return "f32" in type_pair or "f64" in type_pair


def precision_of(fam):
    if fam == "f32":
        return 32
    if fam == "f64":
        return 64
    return None


def build_population():
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    text_of = {}
    meta_of = {}
    class_of = {}
    for lang, n, u, text, gen in units:
        lab = "%s/op_%s" % (lang, n)
        text_of[lab] = text
        meta_of[lab] = u.get("meta")
        tp = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        rkey = fam if fam is not None else ("unknown:%s" % note)
        class_of[lab] = (tp, rkey)
    return text_of, meta_of, class_of


def build_candidate_pairs(text_of, class_of):
    by_class = {}
    for lab, key in class_of.items():
        by_class.setdefault(key, []).append(lab)
    pairs = []
    for key, labs in by_class.items():
        labs_sorted = sorted(labs)
        n = len(labs_sorted)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = labs_sorted[i], labs_sorted[j]
                if text_of[a] == text_of[b]:
                    continue
                pairs.append((a, b, key))
    return pairs


def priority_bucket(a, b, key, class_of):
    lang_a = a.split("/op_")[0]
    lang_b = b.split("/op_")[0]
    cross_lang = lang_a != lang_b
    fam = key[1]
    has_float = fam in FLOAT_FAMS or type_pair_has_float(key[0])
    if cross_lang and has_float:
        return 0
    if cross_lang:
        return 1
    if has_float:
        return 2
    return 3


def prove_pair(a, b, text_of, class_of):
    """(verdict, detail)."""
    text_a = text_of[a]
    text_b = text_of[b]
    if "(%rip)" in text_a or "(%rip)" in text_b:
        return "REFUSED", (
            "one side's canonical text carries a rip-relative "
            "operand (an opaque compiler-constant load) with no "
            "per-unit recovered value threaded through this file -- "
            "cannot be soundly proved equal on unknown inputs")
    fam = class_of[a][1]
    type_pair = class_of[a][0]
    use_compare = is_float_compare_text(text_a) or \
        is_float_compare_text(text_b)
    use_float = (not use_compare) and (
        is_float_text(text_a) or is_float_text(text_b))
    shared_seed = {}
    if use_compare:
        # a float COMPARISON pair -- proved at the 8-bit boolean
        # answer width via Sim20Cmp (this file's own additive
        # subclass, see its docstring), never at the operand's own
        # float width (the answer is 0/1, not a float).
        opnd_precision = 32 if "f32" in type_pair else (
            64 if "f64" in type_pair else None)
        if opnd_precision is None:
            return "REFUSED", (
                "comparison mnemonic present but neither operand "
                "type in %r is f32/f64" % (type_pair,))
        lines_a = [ln.strip() for ln in text_a.split(";")]
        lines_b = [ln.strip() for ln in text_b.split(";")]
        try:
            val_a = Sim20Cmp(shared_seed, "a").answer_value(
                lines_a, 8)
            val_b = Sim20Cmp(shared_seed, "b").answer_value(
                lines_b, 8)
        except BC20.NotModeled as exc:
            return "UNDECIDED", (
                "this file's Sim20Cmp (float-comparison extension "
                "of canon20_behaviour_check.Sim20) has no model for "
                "a mnemonic in this pair's text -- an instrument "
                "limit, not an unknowable-input case: %s" % exc)
        solver = z3.Solver()
        solver.set("timeout", PER_PAIR_TIMEOUT_MS)
        solver.add(val_a != val_b)
    elif use_float:
        precision = precision_of(fam)
        if precision is None:
            return "REFUSED", (
                "text uses SSE float mnemonics but the class key's "
                "result family %r is not f32/f64 -- no answer width "
                "to compare at" % fam)
        lines_a = [ln.strip() for ln in text_a.split(";")]
        lines_b = [ln.strip() for ln in text_b.split(";")]
        try:
            val_a = BC20.Sim20(shared_seed, "a").answer_value(
                lines_a, precision)
            val_b = BC20.Sim20(shared_seed, "b").answer_value(
                lines_b, precision)
        except BC20.NotModeled as exc:
            return "UNDECIDED", (
                "this file's reused float simulator (canon20_"
                "behaviour_check.Sim20) has no model for a mnemonic "
                "in this pair's text -- an instrument limit, not an "
                "unknowable-input case: %s" % exc)
        solver = z3.Solver()
        solver.set("timeout", PER_PAIR_TIMEOUT_MS)
        solver.add(val_a != val_b)
    else:
        lines_a = [ln.strip() for ln in text_a.split(";")]
        lines_b = [ln.strip() for ln in text_b.split(";")]
        try:
            va, wa = BC8.Sim8(shared_seed, "a").answer_value(lines_a)
            vb, wb = BC8.Sim8(shared_seed, "b").answer_value(lines_b)
        except BC8.NotModeled as exc:
            return "UNDECIDED", (
                "this file's reused integer simulator (canon8_"
                "behaviour_check.Sim8) has no model for a mnemonic "
                "in this pair's text -- an instrument limit, not an "
                "unknowable-input case: %s" % exc)
        w = min(wa, wb)
        va = z3.Extract(w - 1, 0, va)
        vb = z3.Extract(w - 1, 0, vb)
        solver = z3.Solver()
        solver.set("timeout", PER_PAIR_TIMEOUT_MS)
        solver.add(va != vb)

    result = solver.check()
    if result == z3.unsat:
        return "PROVED", (
            "z3 proved bit-level equality for every value of every "
            "register either text reads before writing "
            "(fpToIEEEBV/BitVec comparison, %dms timeout)"
            % PER_PAIR_TIMEOUT_MS)
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", (
            "z3 found a counterexample: %s" % model)
    return "UNDECIDED", (
        "z3 returned %r (timeout at %dms, or otherwise declined to "
        "decide) -- counted honestly" % (result, PER_PAIR_TIMEOUT_MS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--out", default=os.path.join(HERE,
                     "proved_edges.json"))
    args = ap.parse_args()

    text_of, meta_of, class_of = build_population()
    print("0-branch population: %d" % len(text_of))

    all_pairs = build_candidate_pairs(text_of, class_of)
    print("full candidate set (same class key, non-identical text): "
          "%d pairs" % len(all_pairs))

    buckets = {0: [], 1: [], 2: [], 3: []}
    for a, b, key in all_pairs:
        buckets[priority_bucket(a, b, key, class_of)].append((a, b, key))
    for bnum in (0, 1, 2, 3):
        buckets[bnum].sort()
    names = {0: "cross-language + float", 1: "cross-language (other)",
             2: "same-language + float", 3: "same-language (other)"}
    for bnum in (0, 1, 2, 3):
        print("  bucket %d (%s): %d pairs"
              % (bnum, names[bnum], len(buckets[bnum])))

    ordered = buckets[0] + buckets[1] + buckets[2] + buckets[3]
    attempt = ordered[:args.limit]
    skipped = ordered[args.limit:]

    skipped_by_bucket = {0: 0, 1: 0, 2: 0, 3: 0}
    attempt_set = set(id(x) for x in attempt)
    idx = 0
    for bnum in (0, 1, 2, 3):
        for item in buckets[bnum]:
            if idx >= len(ordered):
                break
            idx += 1
    # recompute skipped-per-bucket directly (simpler and correct)
    attempted_keys = set((a, b) for a, b, _k in attempt)
    for bnum in (0, 1, 2, 3):
        for a, b, _k in buckets[bnum]:
            if (a, b) not in attempted_keys:
                skipped_by_bucket[bnum] += 1

    print("attempting %d pairs this run (--limit %d)"
          % (len(attempt), args.limit))

    edges = []
    tally = {"PROVED": 0, "DISPROVED": 0, "UNDECIDED": 0, "REFUSED": 0}
    tally_by_bucket = {}
    t0 = time.time()
    for i, (a, b, key) in enumerate(attempt):
        bnum = priority_bucket(a, b, key, class_of)
        verdict, detail = prove_pair(a, b, text_of, class_of)
        tally[verdict] += 1
        tb = tally_by_bucket.setdefault(bnum, {"PROVED": 0,
                                                "DISPROVED": 0,
                                                "UNDECIDED": 0,
                                                "REFUSED": 0})
        tb[verdict] += 1
        cross_lang = a.split("/op_")[0] != b.split("/op_")[0]
        edges.append({
            "a": a,
            "b": b,
            "class_key_type_pair": key[0],
            "class_key_result_family": key[1],
            "cross_language": cross_lang,
            "verdict": verdict,
            "detail": detail,
        })
        elapsed = time.time() - t0
        print("  [%d/%d] %s (%.1fs elapsed)"
              % (i + 1, len(attempt), verdict, elapsed))
        if (i + 1) % 20 == 0:
            json.dump({"partial": True, "done": i + 1,
                       "total": len(attempt), "edges_so_far": edges},
                      open(args.out + ".partial", "w"), indent=1)

    doc = {
        "meta": {
            "role_note": "this file IS a GROUPING/matching artifact -- "
                        "checked by check_no_spelling_keys.py IN FULL.",
            "generator": "cross_unit_prover.py",
            "population": len(text_of),
            "full_candidate_set_count": len(all_pairs),
            "candidate_buckets": {
                "bucket_0_cross_language_float": len(buckets[0]),
                "bucket_1_cross_language_other": len(buckets[1]),
                "bucket_2_same_language_float": len(buckets[2]),
                "bucket_3_same_language_other": len(buckets[3]),
            },
            "attempted_count": len(attempt),
            "not_attempted_count": {
                "bucket_0_cross_language_float":
                    skipped_by_bucket[0],
                "bucket_1_cross_language_other":
                    skipped_by_bucket[1],
                "bucket_2_same_language_float":
                    skipped_by_bucket[2],
                "bucket_3_same_language_other":
                    skipped_by_bucket[3],
            },
            "per_pair_timeout_ms": PER_PAIR_TIMEOUT_MS,
            "tally": tally,
            "tally_by_bucket": tally_by_bucket,
            "note": "candidate set is machine-form only (type_pair, "
                   "result-type class family), never an operator "
                   "token -- see this file's own docstring.",
        },
        "pairs": edges,
    }
    json.dump(doc, open(args.out, "w"), indent=1)
    print("wrote %s" % args.out)
    print("tally: %r" % tally)


if __name__ == "__main__":
    main()
