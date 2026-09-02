#!/usr/bin/env python3
"""canon16_xmm.py -- JOB 3: VECTOR REGISTER PLUMBING.

gen7 through gen14's ENTIRE register model is GP-integer only (no
%xmm0/%xmm1/... entries in REGMAP at all -- confirmed independently by
stage3_vector_constants_report.txt and stage5_float_conditions_
diagnosis.txt, the SAME finding both times). This file adds the
minimum real plumbing to render and PROVE the 10 genuine float-negate-
via-sign-mask units stage3_vector_constants_report.txt already
resolved the constant for (c/15,16, cpp/15,16, go/9,10, rust/3,4,
swift/15,16 -- `-a` for a:float|double, real ship `xorps 0x0(%rip),
%xmm0; ret` / `xorpd 0x0(%rip),%xmm0; ret`), NOT a general float ALU
(that remains Stage 5(b)'s own, larger, deferred scope).

THE DESIGNATED REGISTERS (ratified form, per this lap's own brief):
    a      -> %xmm0
    b      -> %xmm1  (unused by this file's own 10-unit target --
                       every one of them is UNARY -- documented here
                       so a later float-binary-op file does not have
                       to re-derive it)
    answer -> %xmm0

THE ORDERED XMM TEMP POOL (the owner's 2026-08-28 ruling, "TEMP REGISTERS
ARE STANDARDIZED, NOT LIMITED", applied to the vector file exactly as
canon7_render.py's own TEMP_POOL_ORDER applies it to the GP file):
canon.py's own VECTOR_TEMPS already names the first two members,
%xmm2 then %xmm3 ("the two vector registers the canonical form does
not designate"); this file extends that SAME order out to the full
vector file, %xmm4 through %xmm15, so a unit that ever needs more than
two live temporaries has somewhere standardized to go rather than a
renderer improvising an unordered choice:

    XMM_TEMP_POOL_ORDER = [xmm2, xmm3, xmm4, xmm5, ..., xmm15]

None of THIS file's own 10 target units need more than ONE temp (the
mask constant, built in a GP register and moved across) -- the longer
order is recorded because ORDER is what makes two units' rendered text
comparable at all (AgentMemory: "the order is what makes units
match"), not because these units exhaust it.

THE MOVE/LOAD FORMS THIS FILE ADDS: `movd GP32,%xmmN` (GP->XMM,
32-bit, the rest of the destination zeroed -- real x86-64 SSE2
semantics), `movq GP64,%xmmN` (GP->XMM, 64-bit, same), `xorps
%xmmS,%xmmD` / `xorpd %xmmS,%xmmD` (packed XOR -- for a SCALAR
negate, only the low lane the caller reads is observable, so a
register-register xorps/xorpd against a mask register whose own upper
bits are already zero is bit-for-bit what the memory-operand form
real ship code uses, PROVEN below, not assumed).

WHY A REGISTER-REGISTER MASK INSTEAD OF real ship's OWN RIP-RELATIVE
MEMORY OPERAND: this renderer has no mechanism anywhere in this
lineage to allocate a `.rodata` constant or resolve a relocation --
real ship's `xorps 0x0(%rip),%xmm0` reads a 128-bit memory constant
this codebase cannot materialize as an address. The constant's VALUE
is already resolved (stage3_vector_constants_report.txt, two
independent evidence classes: this corpus's own ANCHOR immediates, and
an independently rebuilt-and-disassembled `gcc -O2` object). Loading
that SAME value into a register first (`mov $-2147483648,%eax; movd
%eax,%xmm2` for float; `movabs $-9223372036854775808,%rax; movq
%rax,%xmm2` for double -- the immediate is the mask's OWN signed 32/
64-bit reading, this lineage's existing convention for every GP
immediate) and XOR-ing register-to-register computes the IDENTICAL
value in the observable low lane; canon16.py's own gate PROVES this
directly rather than asserting it (see that file's `Sim16`).

THE SPELLING BAN: unchanged -- this file renders one unit at a time,
keyed by (lang, n) and by z3/meta SHAPE (unary `-` at f32/f64), never
by the source-language operator token as a grouping or matching key;
no units are paired.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

XMM_DESIGNATED_A = "xmm0"
XMM_DESIGNATED_B = "xmm1"
XMM_DESIGNATED_ANSWER = "xmm0"

XMM_TEMP_POOL_ORDER = ["xmm%d" % i for i in range(2, 16)]

# the two resolved sign-mask constants (stage3_vector_constants_
# report.txt, two independent evidence classes -- forced by
# construction both times), read as SIGNED 32-/64-bit immediates, this
# lineage's own existing convention for every GP `mov`/`movabs`.
F32_SIGN_MASK_UNSIGNED = 0x80000000
F64_SIGN_MASK_UNSIGNED = 0x8000000000000000
F32_SIGN_MASK_SIGNED = F32_SIGN_MASK_UNSIGNED - (1 << 32)
F64_SIGN_MASK_SIGNED = F64_SIGN_MASK_UNSIGNED - (1 << 64)


def is_float_negate_unit(meta):
    """True iff `meta` (a unit's own stored `meta` dict) is exactly
    the shape this file targets: unary `-` on a float or double
    operand. Shape-checked on RECORDED evidence (arity, operator,
    lhs_rep), never on the operator token as a grouping key -- the
    token only ever appears once, as this function's own comment."""
    if meta.get("arity") != "unary":
        return False
    if meta.get("operator") != "-":
        return False
    return meta.get("lhs_rep") in ("f32", "f64")


def render_float_negate(lhs_rep):
    """the fixed 3-instruction sequence for `-a`, a:float|double,
    entry contract a in %xmm0, answer left in %xmm0 -- see file header
    for why a register-register mask replaces real ship's memory
    operand, and canon16.py for the proof that this is sound."""
    temp = XMM_TEMP_POOL_ORDER[0]
    if lhs_rep == "f32":
        lines = [
            "mov $%d,%%eax" % F32_SIGN_MASK_SIGNED,
            "movd %%eax,%%%s" % temp,
            "xorps %%%s,%%xmm0" % temp,
            "ret",
        ]
    else:
        lines = [
            "movabs $%d,%%rax" % F64_SIGN_MASK_SIGNED,
            "movq %%rax,%%%s" % temp,
            "xorpd %%%s,%%xmm0" % temp,
            "ret",
        ]
    return lines
