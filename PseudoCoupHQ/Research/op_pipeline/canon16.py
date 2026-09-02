#!/usr/bin/env python3
"""canon16.py -- JOB 3 driver: renders and PROVES the 10 genuine
float-negate-via-sign-mask units (canon16_xmm.py's own target,
stage3_vector_constants_report.txt's own resolved-but-unrendered
bucket) -- c/15,16, cpp/15,16, go/9,10, rust/3,4, swift/15,16.

`Sim16` is a SMALL, SELF-CONTAINED register simulator, not a subclass
of the Sim7/8/9/10 lineage (those model GP registers only, at widths
canon.WIDTH_OF knows -- extending that hierarchy for two mnemonics
this narrow target needs would mean teaching every ancestor about
%xmm's own width table for no benefit outside this file). It tracks
each %xmmN as a 64-BIT symbolic family -- sufficient for a SCALAR
float (32-bit, in the low lane) or double (64-bit) answer, since
`answer_value` only ever reads the low 32 or 64 bits real ship code's
own return convention exposes; the mnemonics real ship code AND this
file's candidates actually use are exactly: `mov`/`movabs` (GP,
immediate only -- these units need no register-to-register GP move),
`movd`/`movq` (GP -> XMM), `xorps`/`xorpd` (XMM, register-register
form for candidates, RIP-relative MEMORY form for real ship text).

THE ONE MODELING DECISION THAT NEEDS ITS OWN JUSTIFICATION: real ship
code's `xorps 0x0(%rip),%xmm0` / `xorpd 0x0(%rip),%xmm0` reads a
128-bit `.rodata` constant this codebase has no mechanism to resolve
an address for. Sim16 special-cases exactly this source-operand SHAPE
(a bare `N(%rip)` operand on `xorps`/`xorpd`) and substitutes the
ALREADY-RESOLVED sign-mask constant (stage3_vector_constants_
report.txt, two independent evidence classes) -- 0x80000000 for
xorps, 0x8000000000000000 for xorpd, zero-extended into the tracked
64-bit family exactly as `movd`/`movq` would establish it from a
register. This is not a guess: it is the SAME literal value this
lap's own report already proved by two independent routes, applied at
the one place real ship code's own text needs it read.

GATE: `xmm_check(lang, n, canon4_docs, candidate)` -- z3-proves the
candidate's final %xmm0 value equal to real ship code's, at the
answer's own stated width (32 for float, 64 for double -- the SAME
"project onto the narrower/stated width" discipline every other gate
in this lineage already uses).

BASELINE: canon15_units_<lang>.json (JOB 2's own output, the newest
generation). A unit not in this file's own 10-unit target list is
copied through BYTE-IDENTICAL.

usage:
  canon16.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import expr_to_canon as EC0                                     # noqa: E402
import canon16_xmm as X16                                        # noqa: E402
import z3                                                        # noqa: E402

assemble_and_disassemble = EC0.assemble_and_disassemble

LANGS = ["c", "cpp", "go", "rust", "swift"]

TARGET_UNITS = {
    "c": ["15", "16"],
    "cpp": ["15", "16"],
    "go": ["9", "10"],
    "rust": ["3", "4"],
    "swift": ["15", "16"],
}


class NotModeled(Exception):
    pass


class Sim16(object):
    """see file header. `regs` maps a bare register/family name
    ('eax', 'rax', 'xmm0', 'xmm2', ...) to a 64-bit z3 BitVec value;
    GP register ALIASES (eax vs rax) are not modeled -- this file's
    own candidates and the real ship texts it compares against never
    read a GP register back after writing it, they only ever write
    once and immediately move it into an XMM register, so no
    width-mixing GP alias ever needs resolving here."""

    def __init__(self, shared_seed, tag, mask_width):
        self.shared_seed = shared_seed
        self.tag = tag
        self.regs = {}
        # the unit's OWN known answer width (32 for float, 64 for
        # double) -- NOT read from the mnemonic spelling. Measured
        # directly (canon4_units_c.json's own `mnem` for c/op_16, a
        # DOUBLE negate): real ship code uses `xorps` (the
        # single-precision-NAMED instruction) for the DOUBLE case too
        # -- xorps/xorpd/pxor are bitwise IDENTICAL 128-bit XORs, gcc
        # picks the shorter encoding regardless of the operand's true
        # type, so which sign-mask CONSTANT a `(%rip)` operand resolves
        # to cannot be read off the mnemonic at all; it is this unit's
        # own recorded float/double shape, passed in by the caller who
        # already knows it.
        self.mask_width = mask_width

    def get(self, name):
        if name not in self.regs:
            if name not in self.shared_seed:
                self.shared_seed[name] = z3.BitVec(
                    "seed_%s" % name, 64)
            self.regs[name] = self.shared_seed[name]
        return self.regs[name]

    def exec_line(self, line):
        line = line.strip()
        reloc_at = line.find("!!reloc")
        if reloc_at != -1:
            # real ship code's own objdump annotation -- not part of
            # the instruction, strip it before parsing operands (see
            # file header: this is what real ship's rip-relative
            # constant load looks like verbatim in canon4's mnem).
            line = line[:reloc_at].strip()
        if line == "ret" or line == "":
            return
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        operands = [o.strip() for o in rest.split(",")]

        if mnem == "mov":
            src, dst = operands
            if not src.startswith("$"):
                raise NotModeled(
                    "mov with a non-immediate source is not "
                    "modeled by Sim16 -- %r" % line)
            v = int(src[1:], 0) & 0xFFFFFFFFFFFFFFFF
            self.regs[dst[1:]] = z3.BitVecVal(v, 64)
            return

        if mnem == "movabs":
            src, dst = operands
            v = int(src[1:], 0) & 0xFFFFFFFFFFFFFFFF
            self.regs[dst[1:]] = z3.BitVecVal(v, 64)
            return

        if mnem in ("movd", "movq"):
            src, dst = operands
            src_name = src[1:]
            dst_name = dst[1:]
            width = 32 if mnem == "movd" else 64
            v = self.get(src_name)
            v = z3.Extract(width - 1, 0, v)
            v = z3.ZeroExt(64 - width, v)
            self.regs[dst_name] = v
            return

        if mnem in ("xorps", "xorpd", "pxor"):
            src, dst = operands
            dst_name = dst[1:]
            # pxor (packed INTEGER xor) is bitwise identical to
            # xorps/xorpd for every bit position -- real x86-64
            # hardware defines all three as a plain 128-bit XOR, they
            # differ only in which execution-port/latency class the
            # CPU dispatches them to, never in the bits produced. Go's
            # own compiler uses pxor for exactly this idiom (measured,
            # go/op_9's own real ship mnem). Width here is only used
            # to decide how much of `dst`'s ORIGINAL upper bits survive
            # unmodified below (64-bit family boundary, this file's
            # own tracking limit, not an x86 width). Real ship code's
            # own choice of xorps/xorpd/pxor does NOT reliably say
            # which width is meant (measured: c/op_16, a DOUBLE
            # negate, uses `xorps` -- the single-precision-NAMED
            # mnemonic -- because xorps/xorpd/pxor are bitwise
            # IDENTICAL 128-bit XORs and gcc picks the shortest
            # encoding regardless of true operand type). The unit's
            # own known width (passed in as `mask_width`) is
            # authoritative; the mnemonic only selects DISPATCH here.
            width = self.mask_width
            if src.endswith("(%rip)"):
                # real ship code's own rip-relative constant --
                # substitute the ALREADY-RESOLVED sign mask (see file
                # header and __init__'s own comment on mask_width:
                # the MNEMONIC does not reliably say which constant is
                # meant, the unit's own known width does).
                mask = X16.F64_SIGN_MASK_UNSIGNED if \
                    self.mask_width == 64 else \
                    X16.F32_SIGN_MASK_UNSIGNED
                src_v = z3.BitVecVal(mask, 64)
            else:
                src_v = self.get(src[1:])
            dst_v = self.get(dst_name)
            lo = z3.Extract(width - 1, 0, dst_v) ^ \
                z3.Extract(width - 1, 0, src_v)
            if width == 64:
                self.regs[dst_name] = lo
            else:
                hi = z3.Extract(63, width, dst_v)
                self.regs[dst_name] = z3.Concat(hi, lo)
            return

        if mnem in ("movss", "movsd"):
            src, dst = operands
            dst_name = dst[1:]
            width = 32 if mnem == "movss" else 64
            if src.endswith("(%rip)"):
                # the SAME idiom as xorps/xorpd's own memory operand,
                # just loaded into a temp register first (go's own
                # compiler shape, measured go/op_9) instead of used
                # directly as an ALU source -- real x86-64 MOVSS/MOVSD
                # from memory to an XMM register zeroes bits 32-127 /
                # 64-127 (Intel SDM), matching this file's own
                # zero-extend-into-the-64-bit-family tracking exactly.
                # Mask choice is the unit's own known width, same
                # reasoning as the xorps/xorpd/pxor branch above.
                mask = X16.F64_SIGN_MASK_UNSIGNED if \
                    self.mask_width == 64 else \
                    X16.F32_SIGN_MASK_UNSIGNED
                self.regs[dst_name] = z3.BitVecVal(mask, 64)
                return
            v = self.get(src[1:])
            self.regs[dst_name] = z3.Extract(width - 1, 0, v) if \
                width == 64 else z3.ZeroExt(
                    32, z3.Extract(31, 0, v))
            return

        raise NotModeled(
            "mnemonic %r has no symbolic model in Sim16" % mnem)

    def answer_value(self, lines, width):
        for line in lines:
            self.exec_line(line)
        full = self.get("xmm0")
        return z3.Extract(width - 1, 0, full)


def width_of(lhs_rep):
    return 32 if lhs_rep == "f32" else 64


def xmm_check(real_text, candidate_text, width):
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    shared_seed = {}
    try:
        val_real = Sim16(shared_seed, "real", width).answer_value(
            lines_real, width)
        val_cand = Sim16(shared_seed, "cand", width).answer_value(
            lines_cand, width)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved this text's final %%xmm0 " \
            "equal to the unit's own real ship code's, at the " \
            "answer's own %d-bit stated width (Sim16 -- GP-immediate " \
            "/ movd / movq / xorps / xorpd model, rip-relative " \
            "operand substituted with the already-resolved sign-mask "\
            "constant)" % width
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample: %s" % model
    return "UNDECIDED", "z3 returned %r" % result


def convert_one(lang, n, canon4_rec, workdir):
    meta = canon4_rec.get("meta") or {}
    if not X16.is_float_negate_unit(meta):
        return None
    real_mnem = canon4_rec.get("mnem")
    if not real_mnem:
        return None
    real_text = "; ".join(real_mnem)
    lines = X16.render_float_negate(meta["lhs_rep"])
    ok, out = assemble_and_disassemble(lines, workdir)
    if not ok:
        return {
            "job3_xmm_candidate_text": None,
            "job3_xmm_refusal_reason":
                "rendered instructions failed to assemble (%s)" % out,
        }
    candidate = "; ".join(lines)
    width = width_of(meta["lhs_rep"])
    verdict, detail = xmm_check(real_text, candidate, width)
    update = {
        "job3_xmm_candidate_text": candidate,
        "job3_xmm_ground_truth_verdict": verdict,
        "job3_xmm_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon16_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 3 (canon16_xmm.py's float-negate-" \
            "via-sign-mask rendering, XMM register plumbing): " \
            "candidate proved equal to the unit's own real ship " \
            "code directly"
    else:
        update["job3_xmm_decision"] = "KEEP_OLD -- %s: %s" % (
            verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, workdir):
    canon15_path = os.path.join(indir, "canon15_units_%s.json" % lang)
    canon4_path = os.path.join(indir, "canon4_units_%s.json" % lang)
    doc = json.load(open(canon15_path))
    units = doc["units"]
    canon4_units = json.load(open(canon4_path))["units"]

    attempted = 0
    accepted = 0
    still_refused = 0

    for n in TARGET_UNITS.get(lang, []):
        u = units.get(n)
        if u is None:
            continue
        if u["status"] == "converged":
            # already converged by an earlier generation -- never
            # reopen a converged unit outside a named gated promotion,
            # and this file's own target list is diagnostic evidence
            # that these 10 were NOT converged as of canon15, so this
            # branch should not fire; kept as a hard safety check.
            continue
        update = convert_one(lang, n, canon4_units[n], workdir)
        if update is None:
            continue
        attempted = attempted + 1
        u.update(update)
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job3_xmm_tally"] = {
        "target_units_this_lang": len(TARGET_UNITS.get(lang, [])),
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon16.py (JOB 3: vector register " \
        "plumbing) over canon15_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon16_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused)"
          % (name, attempted, accepted, still_refused))
    return doc


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2

    started = time.time()
    print("canon16.py -- JOB 3: vector register plumbing")
    workdir = tempfile.mkdtemp(prefix="canon16_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, workdir)
        for k in totals:
            totals[k] += doc["job3_xmm_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
