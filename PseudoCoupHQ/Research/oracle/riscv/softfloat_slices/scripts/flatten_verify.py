#!/usr/bin/env python3
"""Differential test: the ORIGINAL slice against the FLATTENED one.

Both are built from the same C sources through the same slicer, targeting the
HOST, and linked into one binary with a generated driver, so every input goes
to both and the returned bits are compared directly.

Inputs per operand
  * every edge case: +/-0, +/-inf, quiet and signalling NaN, largest and
    smallest normal, largest and smallest subnormal, +/-1 and +/-2, and one
    ulp either side of each of those (the encodings are sign-magnitude, so
    p-1 and p+1 are the neighbouring values in magnitude);
  * the full cross product of those over all operands;
  * 200,000 uniform random bit patterns per operand;
  * 100,000 more with the exponent drawn from a narrow band around the bias,
    because a uniform random float64 pattern is a NaN or an overflow almost
    every time and would never exercise the rounding path.

The comparison is bit-exact on the returned value, and on the exception flags
too for the `flags` variant.
"""
import json
import os
import subprocess
import sys

ROOT = ("/tmp/claude-1000/-home-<user>-Programming/"
        "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/fl")
sys.path.insert(0, ROOT)

CTYPE = {
    "float16_t": ("f16_t", 16, "float"), "bfloat16_t": ("bf16_t", 16, "float"),
    "float32_t": ("f32_t", 32, "float"), "float64_t": ("f64_t", 64, "float"),
    "bool": ("bool", 1, "bool"),
    "uint_fast8_t": ("uint8_t", 8, "int"), "int_fast8_t": ("int8_t", 8, "int"),
    "uint_fast16_t": ("uint16_t", 16, "int"),
    "int_fast16_t": ("int16_t", 16, "int"),
    "uint_fast32_t": ("uint32_t", 32, "int"),
    "int_fast32_t": ("int32_t", 32, "int"),
    "uint_fast64_t": ("uint64_t", 64, "int"),
    "int_fast64_t": ("int64_t", 64, "int"),
    "uint32_t": ("uint32_t", 32, "int"), "int32_t": ("int32_t", 32, "int"),
    "uint64_t": ("uint64_t", 64, "int"), "int64_t": ("int64_t", 64, "int"),
}
FMT = {16: (5, 10), 32: (8, 23), 64: (11, 52)}
BF = (8, 7)

PREAMBLE = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
typedef struct { uint16_t v; } f16_t;
typedef struct { uint16_t v; } bf16_t;
typedef struct { uint32_t v; } f32_t;
typedef struct { uint64_t v; } f64_t;
static uint64_t S = 0x9E3779B97F4A7C15ULL;
static uint64_t rnd(void) {
    S ^= S << 13; S ^= S >> 7; S ^= S << 17; return S;
}
"""


def float_edges(w, exp_bits, man_bits):
    top = (1 << w) - 1
    bias = (1 << (exp_bits - 1)) - 1
    expall = (1 << exp_bits) - 1
    man = (1 << man_bits) - 1
    named = [
        0,                                              # +0
        expall << man_bits,                             # +inf
        (expall << man_bits) | (1 << (man_bits - 1)),   # quiet NaN
        (expall << man_bits) | 1,                       # signalling NaN
        ((expall - 1) << man_bits) | man,               # largest normal
        1 << man_bits,                                  # smallest normal
        man,                                            # largest subnormal
        1,                                              # smallest subnormal
        bias << man_bits,                               # 1.0
        (bias + 1) << man_bits,                         # 2.0
        (bias - 1) << man_bits,                         # 0.5
    ]
    out = set()
    for p in named:
        for q in (p, p | (1 << (w - 1))):               # both signs
            for d in (-1, 0, 1):                        # one ulp either side
                out.add((q + d) & top)
    return sorted(out)


def int_edges(w, signed):
    top = (1 << w) - 1
    vals = {0, 1, top, top - 1, 1 << (w - 1), (1 << (w - 1)) - 1,
            (1 << (w - 1)) + 1}
    for k in (1, 7, 8, 15, 16, 23, 24, 31, 32, 52, 53, 62, 63):
        if k < w:
            for d in (-1, 0, 1):
                vals.add(((1 << k) + d) & top)
    return sorted(v & top for v in vals)


def operand_spec(ctype):
    cty, w, kind = CTYPE[ctype]
    if kind == "float":
        e, m = FMT[w] if ctype != "bfloat16_t" else BF
        return cty, w, kind, float_edges(w, e, m)
    if kind == "bool":
        return cty, 1, kind, [0, 1]
    return cty, w, kind, int_edges(w, ctype.startswith("int"))


def make_value(cty, kind, expr):
    if kind == "float":
        bits = {"f16_t": "uint16_t", "bf16_t": "uint16_t",
                "f32_t": "uint32_t", "f64_t": "uint64_t"}[cty]
        return "({ %s _t; _t.v = (%s)(%s); _t; })" % (cty, bits, expr)
    if kind == "bool":
        return "(bool)((%s) & 1)" % expr
    return "(%s)(%s)" % (cty, expr)


def gen_driver(op, entry, params, ret_ctype, variant, n_rand, n_struct):
    """params = list of SoftFloat type names for the wrapper's arguments."""
    specs = [operand_spec(p) for p in params]
    rty, rw, rkind = CTYPE[ret_ctype]
    if variant == "value":
        rdecl = rty
        cmp_ = ("A.v != B.v" if rkind == "float" else "A != B")
        enc = ("(unsigned long long)A.v" if rkind == "float"
               else "(unsigned long long)A")
        encb = enc.replace("A", "B")
    else:
        rdecl = "res_t"
        cmp_ = ("A.flags != B.flags || A.v.v != B.v.v" if rkind == "float"
                else "A.flags != B.flags || A.v != B.v")
        enc = ("(unsigned long long)A.v.v" if rkind == "float"
               else "(unsigned long long)A.v")
        encb = enc.replace("A", "B")

    L = [PREAMBLE]
    if variant == "flags":
        L.append("typedef struct { uint8_t flags; %s v; } res_t;" % rty)
    argdecl = ", ".join("%s a%d" % (s[0], i) for i, s in enumerate(specs)) \
        or "void"
    L.append("extern %s %s(%s);" % (rdecl, entry, argdecl))
    L.append("extern %s %s_flat(%s);" % (rdecl, entry, argdecl))
    for i, (cty, w, kind, edges) in enumerate(specs):
        L.append("static const unsigned long long E%d[] = {%s};"
                 % (i, ",".join("0x%xULL" % e for e in edges)))
        L.append("#define N%d (sizeof(E%d)/sizeof(E%d[0]))" % (i, i, i))
    L.append("""
static unsigned long long tested = 0, mismatches = 0, shown = 0;
static unsigned long long cur[%d];
""" % max(1, len(specs)))
    call_args = ", ".join(
        make_value(s[0], s[2], "cur[%d]" % i) for i, s in enumerate(specs))
    L.append("""
static void check(void) {
    %s A = %s(%s);
    %s B = %s_flat(%s);
    tested++;
    if (%s) {
        mismatches++;
        if (shown < 8) {
            shown++;
            printf("MISMATCH in:");
            for (int k = 0; k < %d; k++) printf(" 0x%%016llx", cur[k]);
            printf("  orig=0x%%llx flat=0x%%llx", %s, %s);
""" % (rdecl, entry, call_args, rdecl, entry, call_args, cmp_,
       max(1, len(specs)), enc, encb))
    if variant == "flags":
        L.append('            printf("  origflags=0x%x flatflags=0x%x",'
                 ' A.flags, B.flags);')
    L.append("""            printf("\\n");
        }
    }
}
""")
    # exhaustive cross product over the edge cases
    loops = "".join("    for (unsigned long long i%d = 0; i%d < N%d; i%d++) {\n"
                    % (i, i, i, i) for i in range(len(specs)))
    setc = "".join("        cur[%d] = E%d[i%d];\n" % (i, i, i)
                   for i in range(len(specs)))
    close = "    }" * len(specs)
    masks = [((1 << s[1]) - 1) if s[1] < 64 else 0xFFFFFFFFFFFFFFFF
             for s in specs]
    rnd_set = "".join("        cur[%d] = rnd() & 0x%xULL;\n" % (i, masks[i])
                      for i in range(len(specs)))
    st = []
    for i, (cty, w, kind, edges) in enumerate(specs):
        if kind == "float":
            e, m = FMT[w] if cty not in ("bf16_t",) else BF
            bias = (1 << (e - 1)) - 1
            st.append("        { unsigned long long sgn = rnd() & 1ULL;\n"
                      "          unsigned long long ex = (unsigned long long)"
                      "(%d + (long long)(rnd() %% 33) - 16) & 0x%xULL;\n"
                      "          unsigned long long mn = rnd() & 0x%xULL;\n"
                      "          cur[%d] = (sgn << %d) | (ex << %d) | mn; }\n"
                      % (bias, (1 << e) - 1, (1 << m) - 1, i, w - 1, m))
        else:
            st.append("        cur[%d] = rnd() & 0x%xULL;\n" % (i, masks[i]))
    L.append("""
int main(void) {
%s%s        check();
%s
    for (unsigned long long n = 0; n < %dULL; n++) {
%s        check();
    }
    for (unsigned long long n = 0; n < %dULL; n++) {
%s        check();
    }
    printf("TESTED %%llu MISMATCHES %%llu\\n", tested, mismatches);
    return mismatches != 0;
}
""" % (loops, setc, close, n_rand, rnd_set, n_struct, "".join(st)))
    return "\n".join(L)


def wrapper_params(op, protos):
    """The wrapper's argument list: the operation's, minus the rounding mode
    and minus `exact` for the twelve conversions (both pinned literals)."""
    ret, args = protos[op]
    is_rti = op.endswith("roundToInt")
    takes_mode = any("uint_fast8_t" in a for a in args)
    out = []
    for a in args:
        if a == "uint_fast8_t":
            continue
        if a == "bool" and not is_rti and takes_mode:
            continue
        out.append(a)
    return ret, out
