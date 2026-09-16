#!/usr/bin/env python3
"""Verify every arch-unit emulation against the ORIGINAL compiler-operator.

For each of the 174 arch-units the reference is the source expression the
arch-unit came from -- `!a`, `a + b`, `a <= b` -- written as a native function
in the arch-unit's own language (c for the 150 c units, go for the 24 go
units), compiled for the HOST at -O2.  That native function is run over an
input stream; the same stream is then run through the integer-only emulation
in ALL FOUR languages and compared bit for bit.

Two comparisons come out of one run:

  native   each language's emulation against the native operator.  A
           difference where BOTH answers are NaN of the result type is
           counted apart as a NaN divergence, because C and go both leave the
           sign and payload of a NaN result unspecified and the two targets
           pin them differently -- see the README.
  cross    every language's emulation against c's, byte for byte, no
           tolerance at all.  This is the cross-language claim.

Inputs per arch-unit: every edge value of each operand crossed, plus NRAND
uniform random bit patterns per operand, plus NBAND with the exponent banded
around the bias.  All six programs draw the identical sequence from the same
xorshift64 seed in the same order.

Everything is built and run under EMUL_SCRATCH; nothing outside
softfloat_slices/arch_units and softfloat_slices/scripts is written.
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "arch_units")
EMUL = os.path.join(OUT, "emul_rm0")
sys.path.insert(0, HERE)
import emul_spec as S                                          # noqa: E402

SCRATCH = os.environ.get(
    "AU_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/archunits")

N_RAND = int(os.environ.get("NRAND", 200000))
N_BAND = int(os.environ.get("NBAND", 100000))
SEED = "0x9E3779B97F4A7C15"
JOBS = int(os.environ.get("JOBS", str(os.cpu_count() or 4)))
ONLY = os.environ.get("AU_ONLY", "")


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, p.stdout, p.stderr


def must(cmd, what, **kw):
    rc, o, e = run(cmd, **kw)
    if rc:
        raise SystemExit("%s failed:\n%s\n%s" % (what, o[-4000:], e[-8000:]))
    return o


def note(*a):
    print(*a, flush=True)


# ------------------------------------------------------------- input plans --
OPERAND_SPEC = {
    "float": lambda: S.flt("f32"), "float32": lambda: S.flt("f32"),
    "double": lambda: S.flt("f64"), "float64": lambda: S.flt("f64"),
    "int32_t": lambda: S.integer("i32"), "int64_t": lambda: S.integer("i64"),
    "uint64_t": lambda: S.integer("ui64"), "bool": S.boolean,
}


def plan(u):
    ops = [OPERAND_SPEC[u["lhs_type"]]()]
    if u["rhs_type"] is not None:
        ops.append(OPERAND_SPEC[u["rhs_type"]]())
    edges = [S.edges(o) for o in ops]
    n = 1
    for e in edges:
        n *= len(e)
    return ops, edges, n + N_RAND + N_BAND


# ---------------------------------------------------------- native c source --
C_DECODE = {
    "float": "    float %s; { uint32_t t_ = (uint32_t)p%d;"
             " memcpy(&%s, &t_, 4); }",
    "double": "    double %s; { uint64_t t_ = p%d; memcpy(&%s, &t_, 8); }",
    "int32_t": "    int32_t %s = (int32_t)(uint32_t)p%d;%.0s",
    "int64_t": "    int64_t %s = (int64_t)p%d;%.0s",
    "uint64_t": "    uint64_t %s = p%d;%.0s",
    "bool": "    _Bool %s = (p%d & 1u) != 0;%.0s",
}


def c_ref_fn(u):
    names = ["a"] if u["rhs_type"] is None else ["a", "b"]
    tys = [u["lhs_type"]] + ([] if u["rhs_type"] is None else [u["rhs_type"]])
    L = ["static uint64_t ref_%03d(%s)" %
         (u["index"], ", ".join("uint64_t p%d" % i for i in range(len(names)))),
         "{"]
    for i, (nm, ty) in enumerate(zip(names, tys)):
        L.append(C_DECODE[ty] % (nm, i, nm))
    kind = u["result_kind"]
    expr = u["expression"]
    if u["operator"] == "&":                       # the stated reduction
        ct = "float" if u["result_bits"] == 32 else "double"
        L.append("    %s *q_ = &a;" % ct)
        expr = "*q_"
    if kind == "int":
        L.append("    int r_ = (%s);" % expr)
        L.append("    return (uint64_t)(uint32_t)r_;")
    elif kind == "f32":
        L.append("    float r_ = (%s);" % expr)
        L.append("    uint32_t o_; memcpy(&o_, &r_, 4); return (uint64_t)o_;")
    else:
        L.append("    double r_ = (%s);" % expr)
        L.append("    uint64_t o_; memcpy(&o_, &r_, 8); return o_;")
    L.append("}")
    return "\n".join(L)


GO_DECODE = {
    "float32": "\t%s := math.Float32frombits(uint32(p%d))",
    "float64": "\t%s := math.Float64frombits(p%d)",
}


def go_ref_fn(u):
    names = ["a"] if u["rhs_type"] is None else ["a", "b"]
    tys = [u["lhs_type"]] + ([] if u["rhs_type"] is None else [u["rhs_type"]])
    L = ["func ref_%03d(%s) uint64 {" %
         (u["index"], ", ".join("p%d uint64" % i for i in range(len(names))))]
    for i, (nm, ty) in enumerate(zip(names, tys)):
        L.append(GO_DECODE[ty] % (nm, i))
    expr = u["expression"]
    if u["operator"] == "&":
        L.append("\tq_ := &a")
        expr = "*q_"
    kind = u["result_kind"]
    if kind == "int":
        L.append("\tr_ := (%s)" % expr)
        L.append("\tif r_ {\n\t\treturn 1\n\t}\n\treturn 0")
    elif kind == "f32":
        L.append("\tr_ := (%s)" % expr)
        L.append("\treturn uint64(math.Float32bits(r_))")
    else:
        L.append("\tr_ := (%s)" % expr)
        L.append("\treturn math.Float64bits(r_)")
    L.append("}")
    return "\n".join(L)


# ------------------------------------------------------- generator fragments --
def band_lines(lang, ops, indent):
    """the exponent-banded draw, identical arithmetic in all four languages."""
    L = []
    for i, p in enumerate(ops):
        if p.kind == "float":
            if lang in ("c", "cpp"):
                L.append(indent + "{ uint64_t sg = rnd() & 1ULL;"
                         " uint64_t ex = (uint64_t)(%d + (int64_t)(rnd() %%"
                         " 33) - 16) & 0x%xULL; uint64_t mn = rnd() &"
                         " 0x%xULL; c%d = (sg << %d) | (ex << %d) | mn; }"
                         % (p.bias, (1 << p.exp) - 1, (1 << p.man) - 1,
                            i, p.width - 1, p.man))
            elif lang == "rust":
                L.append(indent + "{ let sg = rnd(&mut s) & 1u64;"
                         " let ex = ((%d as i64 + ((rnd(&mut s) %% 33) as"
                         " i64) - 16) as u64) & 0x%xu64;"
                         " let mn = rnd(&mut s) & 0x%xu64;"
                         " c%d = (sg << %d) | (ex << %d) | mn; }"
                         % (p.bias, (1 << p.exp) - 1, (1 << p.man) - 1,
                            i, p.width - 1, p.man))
            else:
                L.append(indent + "{ sg := rnd() & 1;"
                         " ex := uint64(int64(%d)+int64(rnd()%%33)-16) &"
                         " 0x%x; mn := rnd() & 0x%x;"
                         " c%d = (sg << %d) | (ex << %d) | mn }"
                         % (p.bias, (1 << p.exp) - 1, (1 << p.man) - 1,
                            i, p.width - 1, p.man))
        else:
            L.append(rand_line(lang, i, p, indent))
    return L


def rand_line(lang, i, p, indent):
    if lang in ("c", "cpp"):
        return indent + "c%d = rnd() & 0x%xULL;" % (i, p.mask)
    if lang == "rust":
        return indent + "c%d = rnd(&mut s) & 0x%xu64;" % (i, p.mask)
    return indent + "c%d = rnd() & 0x%x" % (i, p.mask)


def nan_test(lang, kind, v):
    if kind == "int":
        return {"c": "false", "cpp": "false", "rust": "false",
                "go": "false"}[lang]
    if kind == "f32":
        m, e, q = "0x7f800000", "0x007fffff", "0x7f800000"
    else:
        m, e, q = ("0x7ff0000000000000", "0x000fffffffffffff",
                   "0x7ff0000000000000")
    if lang in ("c", "cpp"):
        return "((((%s) & %sULL) == %sULL) && (((%s) & %sULL) != 0))" % (
            v, m, q, v, e)
    if lang == "rust":
        return "((((%s) & %su64) == %su64) && (((%s) & %su64) != 0))" % (
            v, m, q, v, e)
    return "((((%s) & %s) == %s) && (((%s) & %s) != 0))" % (v, m, q, v, e)


# =========================================================== reference in c ==
def gen_ref_c(units):
    cu = [u for u in units if u["lang"] == "c"]
    L = ["/* generated by scripts/verify_arch_units.py */",
         "#include <stdint.h>", "#include <stdio.h>", "#include <stdlib.h>",
         "#include <string.h>", "",
         "static uint64_t S_;",
         "static void seed(void) { S_ = %sULL; }" % SEED,
         "static uint64_t rnd(void) { S_ ^= S_ << 13; S_ ^= S_ >> 7;"
         " S_ ^= S_ << 17; return S_; }",
         "static const char *DIR_;", ""]
    for u in cu:
        L.append(c_ref_fn(u))
        L.append("")
    for u in cu:
        L.append(gen_stream_c(u, "ref_%03d" % u["index"], units))
        L.append("")
    L.append("int main(int argc, char **argv)\n{\n    DIR_ = argv[1];")
    for u in cu:
        L.append("    stream_%03d();" % u["index"])
    L.append("    return 0;\n}")
    return "\n".join(L) + "\n"


def gen_stream_c(u, fname, units):
    ops, edges, total = plan(u)
    n = len(ops)
    L = []
    for i, e in enumerate(edges):
        L.append("static const unsigned long long E_%03d_%d[] = {%s};"
                 % (u["index"], i, ",".join("0x%xULL" % v for v in e)))
    L += ["static void stream_%03d(void)" % u["index"], "{",
          "    uint64_t *buf = (uint64_t *)malloc(%dULL * 8);" % total,
          "    unsigned long long k = 0;",
          "    unsigned long long %s;" % ", ".join("c%d" % i for i in range(n)),
          "    char path[512];",
          "    seed();"]
    for i in range(n):
        L.append("    %sfor (unsigned long long i%d = 0; i%d < %d; i%d++) {"
                 % ("    " * i, i, i, len(edges[i]), i))
    for i in range(n):
        L.append("    %sc%d = E_%03d_%d[i%d];"
                 % ("    " * n, i, u["index"], i, i))
    L.append("    %sbuf[k++] = %s(%s);"
             % ("    " * n, fname, ", ".join("c%d" % i for i in range(n))))
    L.append("    " + "}" * n)
    L.append("    for (unsigned long long q = 0; q < %dULL; q++) {" % N_RAND)
    for i, p in enumerate(ops):
        L.append(rand_line("c", i, p, "        "))
    L.append("        buf[k++] = %s(%s);"
             % (fname, ", ".join("c%d" % i for i in range(n))))
    L.append("    }")
    L.append("    for (unsigned long long q = 0; q < %dULL; q++) {" % N_BAND)
    L += band_lines("c", ops, "        ")
    L.append("        buf[k++] = %s(%s);"
             % (fname, ", ".join("c%d" % i for i in range(n))))
    L.append("    }")
    L += ['    snprintf(path, sizeof path, "%s/%03d.bin", DIR_, '
          + str(u["index"]) + ");",
          '    { FILE *f = fopen(path, "wb"); fwrite(buf, 8, k, f);'
          ' fclose(f); }',
          "    free(buf);",
          '    printf("REF %d %%llu\\n", k);' % u["index"],
          "}"]
    return "\n".join(L)


# ========================================================== reference in go ==
def gen_ref_go(units):
    gu = [u for u in units if u["lang"] == "go"]
    L = ["// generated by scripts/verify_arch_units.py", "package main", "",
         'import (', '\t"bufio"', '\t"encoding/binary"', '\t"fmt"',
         '\t"math"', '\t"os"', ')', "",
         "var s_ uint64", "",
         "func seed() { s_ = %s }" % SEED,
         "func rnd() uint64 { s_ ^= s_ << 13; s_ ^= s_ >> 7; s_ ^= s_ << 17;"
         " return s_ }", "",
         "var dir_ string", "",
         "func emit(idx int, buf []uint64) {",
         '\tf, err := os.Create(fmt.Sprintf("%s/%03d.bin", dir_, idx))',
         "\tif err != nil { panic(err) }",
         "\tw := bufio.NewWriterSize(f, 1<<20)",
         "\tvar tmp [8]byte",
         "\tfor _, v := range buf {",
         "\t\tbinary.LittleEndian.PutUint64(tmp[:], v)",
         "\t\tw.Write(tmp[:])",
         "\t}",
         "\tw.Flush()",
         "\tf.Close()",
         '\tfmt.Printf("REF %d %d\\n", idx, len(buf))',
         "}", "",
         "var _ = math.Float32bits", ""]
    for u in gu:
        L.append(go_ref_fn(u))
        L.append("")
    for u in gu:
        L.append(gen_stream_go(u))
        L.append("")
    L.append("func main() {\n\tdir_ = os.Args[1]")
    for u in gu:
        L.append("\tstream_%03d()" % u["index"])
    L.append("}")
    return "\n".join(L) + "\n"


def gen_stream_go(u):
    ops, edges, total = plan(u)
    n = len(ops)
    L = []
    for i, e in enumerate(edges):
        L.append("var e_%03d_%d = []uint64{%s}"
                 % (u["index"], i, ",".join("0x%x" % v for v in e)))
    L += ["func stream_%03d() {" % u["index"],
          "\tbuf := make([]uint64, 0, %d)" % total,
          "\tvar %s uint64" % ", ".join("c%d" % i for i in range(n)),
          "\t_ = c0",
          "\tseed()"]
    for i in range(n):
        L.append("\t%sfor _, x%d := range e_%03d_%d {"
                 % ("\t" * i, i, u["index"], i))
    for i in range(n):
        L.append("\t%sc%d = x%d" % ("\t" * n, i, i))
    L.append("\t%sbuf = append(buf, ref_%03d(%s))"
             % ("\t" * n, u["index"], ", ".join("c%d" % i for i in range(n))))
    L.append("\t" + "}" * n)
    L.append("\tfor q := 0; q < %d; q++ {" % N_RAND)
    for i, p in enumerate(ops):
        L.append(rand_line("go", i, p, "\t\t"))
    L.append("\t\tbuf = append(buf, ref_%03d(%s))"
             % (u["index"], ", ".join("c%d" % i for i in range(n))))
    L.append("\t}")
    L.append("\tfor q := 0; q < %d; q++ {" % N_BAND)
    L += band_lines("go", ops, "\t\t")
    L.append("\t\tbuf = append(buf, ref_%03d(%s))"
             % (u["index"], ", ".join("c%d" % i for i in range(n))))
    L.append("\t}")
    L.append("\temit(%d, buf)" % u["index"])
    L.append("}")
    return "\n".join(L)


# ================================================================ harnesses ==
def gen_harness_c(units, cpp):
    lang = "cpp" if cpp else "c"
    inc = '#include "arch_units.hpp"' if cpp else '#include "arch_units.h"'
    L = ["/* generated by scripts/verify_arch_units.py */",
         "#include <stdint.h>", "#include <stdio.h>", "#include <stdlib.h>",
         "#include <string.h>", inc, ""]
    if cpp:
        L.append("using namespace archunits;")
    L += ["static uint64_t S_;",
          "static void seed(void) { S_ = %sULL; }" % SEED,
          "static uint64_t rnd(void) { S_ ^= S_ << 13; S_ ^= S_ >> 7;"
          " S_ ^= S_ << 17; return S_; }",
          "static const char *REF_; static const char *EMU_;"
          " static int WRITE_;", "",
          "static uint64_t *slurp(const char *d, int idx,"
          " unsigned long long n)",
          "{",
          "    char path[512]; snprintf(path, sizeof path,"
          ' "%s/%03d.bin", d, idx);',
          '    FILE *f = fopen(path, "rb"); if (!f) { printf("NOFILE %d\\n",'
          " idx); return NULL; }",
          "    uint64_t *b = (uint64_t *)malloc(n * 8);",
          '    if (fread(b, 8, n, f) != n) { printf("SHORT %d\\n", idx); }',
          "    fclose(f); return b;", "}", ""]
    for u in units:
        L.append(gen_check_c(u, cpp))
        L.append("")
    L.append("int main(int argc, char **argv)\n{\n    REF_ = argv[1];"
             " EMU_ = argv[2]; WRITE_ = atoi(argv[3]);")
    for u in units:
        L.append("    check_%03d();" % u["index"])
    L.append("    return 0;\n}")
    return "\n".join(L) + "\n"


def gen_check_c(u, cpp):
    ops, edges, total = plan(u)
    n = len(ops)
    name = u["languages"]["cpp" if cpp else "c"]["entry"]
    args = ", ".join("c%d" % i for i in range(n))
    L = []
    for i, e in enumerate(edges):
        L.append("static const unsigned long long F_%03d_%d[] = {%s};"
                 % (u["index"], i, ",".join("0x%xULL" % v for v in e)))
    L += ["static void check_%03d(void)" % u["index"], "{",
          "    uint64_t *ref = slurp(REF_, %d, %dULL);" % (u["index"], total),
          "    uint64_t *xl = WRITE_ ? NULL : slurp(EMU_, %d, %dULL);"
          % (u["index"], total),
          "    uint64_t *mine = (uint64_t *)malloc(%dULL * 8);" % total,
          "    unsigned long long k = 0, mism = 0, nand = 0, xlm = 0,"
          " shown = 0, shownn = 0;",
          "    unsigned long long %s;" % ", ".join("c%d" % i for i in range(n)),
          "    seed();"]
    chk = ["        {",
           "            uint64_t got = %s(%s);" % (name, args),
           "            uint64_t want = ref[k];",
           "            mine[k] = got;",
           "            if (got != want) {",
           "                if (%s && %s) { nand++;"
           % (nan_test("c", u["result_kind"], "got"),
              nan_test("c", u["result_kind"], "want")),
           "                    if (shownn < 2) { shownn++;",
           '                        printf("EXN %d NAN-DIVERGENT");'
           % u["index"],
           "                        %s" % " ".join(
               'printf(" 0x%%llx", c%d);' % i for i in range(n)),
           '                        printf(" native 0x%llx emul 0x%llx\\n",'
           " (unsigned long long)want, (unsigned long long)got); } }",
           "                else { mism++; if (shown < 4) { shown++;",
           '                    printf("EX %d MISMATCH");' % u["index"],
           "                    %s" % " ".join(
               'printf(" 0x%%llx", c%d);' % i for i in range(n)),
           '                    printf(" want 0x%llx got 0x%llx\\n",'
           " (unsigned long long)want, (unsigned long long)got); } }",
           "            }",
           "            if (xl && got != xl[k]) xlm++;",
           "            k++;",
           "        }"]
    chk = "\n".join(chk)
    for i in range(n):
        L.append("    %sfor (unsigned long long i%d = 0; i%d < %d; i%d++) {"
                 % ("    " * i, i, i, len(edges[i]), i))
    for i in range(n):
        L.append("    %sc%d = F_%03d_%d[i%d];"
                 % ("    " * n, i, u["index"], i, i))
    L.append(chk)
    L.append("    " + "}" * n)
    L.append("    for (unsigned long long q = 0; q < %dULL; q++) {" % N_RAND)
    for i, p in enumerate(ops):
        L.append(rand_line("c", i, p, "        "))
    L.append(chk)
    L.append("    }")
    L.append("    for (unsigned long long q = 0; q < %dULL; q++) {" % N_BAND)
    L += band_lines("c", ops, "        ")
    L.append(chk)
    L.append("    }")
    L += ["    if (WRITE_) { char path[512];",
          '        snprintf(path, sizeof path, "%s/%03d.bin", EMU_, '
          + str(u["index"]) + ");",
          '        FILE *f = fopen(path, "wb"); fwrite(mine, 8, k, f);'
          " fclose(f); }",
          '    printf("RESULT %d %%llu %%llu %%llu %%llu\\n", k, mism, nand,'
          " xlm);" % u["index"],
          "    free(ref); free(mine); if (xl) free(xl);",
          "}"]
    return "\n".join(L)


def gen_harness_rust(units):
    L = ["// generated by scripts/verify_arch_units.py",
         "#![allow(unused_parens, unused_mut, non_snake_case)]",
         "use std::fs::File;", "use std::io::Read;", "",
         "#[inline(always)]",
         "fn rnd(s: &mut u64) -> u64 { *s ^= *s << 13; *s ^= *s >> 7;"
         " *s ^= *s << 17; *s }", "",
         "fn slurp(d: &str, idx: usize, n: usize) -> Vec<u64> {",
         '    let mut f = File::open(format!("{}/{:03}.bin", d, idx))'
         '.expect("ref");',
         "    let mut raw = Vec::new(); f.read_to_end(&mut raw).unwrap();",
         "    assert!(raw.len() >= n * 8);",
         "    let mut v = Vec::with_capacity(n);",
         "    for i in 0..n { let mut b = [0u8; 8];"
         " b.copy_from_slice(&raw[i*8..i*8+8]); v.push(u64::from_le_bytes(b));"
         " }",
         "    v", "}", ""]
    for u in units:
        L.append(gen_check_rust(u))
        L.append("")
    L.append("fn main() {")
    L.append("    let a: Vec<String> = std::env::args().collect();")
    L.append("    let (r, e) = (a[1].clone(), a[2].clone());")
    for u in units:
        L.append("    check_%03d(&r, &e);" % u["index"])
    L.append("}")
    return "\n".join(L) + "\n"


def gen_check_rust(u):
    ops, edges, total = plan(u)
    n = len(ops)
    name = u["languages"]["rust"]["entry"]
    call = "archunits::%s::%s(%s)" % (
        name, name, ", ".join("c%d" % i for i in range(n)))
    L = []
    for i, e in enumerate(edges):
        L.append("static F_%03d_%d: [u64; %d] = [%s];"
                 % (u["index"], i, len(e), ",".join("0x%xu64" % v for v in e)))
    L += ["fn check_%03d(refd: &str, emud: &str) {" % u["index"],
          "    let refv = slurp(refd, %d, %d);" % (u["index"], total),
          "    let xl = slurp(emud, %d, %d);" % (u["index"], total),
          "    let mut s: u64 = %s;" % SEED,
          "    let (mut k, mut mism, mut nand, mut xlm) "
          "= (0usize, 0u64, 0u64, 0u64);",
          "    let mut shown = 0;",
          "    %s" % " ".join("let mut c%d: u64 = 0;" % i for i in range(n))]
    # simpler example print: list the operands
    ex = " ".join('print!(" {:#x}", c%d);' % i for i in range(n))
    chk = ["        {",
           "            let got: u64 = %s;" % call,
           "            let want: u64 = refv[k];",
           "            if got != want {",
           "                if %s && %s { nand += 1; }"
           % (nan_test("rust", u["result_kind"], "got"),
              nan_test("rust", u["result_kind"], "want")),
           "                else { mism += 1; if shown < 4 { shown += 1;",
           '                    print!("EX %d MISMATCH"); %s'
           % (u["index"], ex),
           '                    println!(" want {:#x} got {:#x}", want,'
           " got); } }",
           "            }",
           "            if got != xl[k] { xlm += 1; }",
           "            k += 1;",
           "        }"]
    chk = "\n".join(chk)
    for i in range(n):
        L.append("    %sfor i%d in 0..%d {" % ("    " * i, i, len(edges[i])))
    for i in range(n):
        L.append("    %sc%d = F_%03d_%d[i%d];"
                 % ("    " * n, i, u["index"], i, i))
    L.append(chk)
    L.append("    " + "}" * n)
    L.append("    for _q in 0..%d {" % N_RAND)
    for i, p in enumerate(ops):
        L.append(rand_line("rust", i, p, "        "))
    L.append(chk)
    L.append("    }")
    L.append("    for _q in 0..%d {" % N_BAND)
    L += band_lines("rust", ops, "        ")
    L.append(chk)
    L.append("    }")
    L.append('    println!("RESULT %d {} {} {} {}", k, mism, nand, xlm);'
             % u["index"])
    L.append("}")
    return "\n".join(L)


def gen_harness_go(units):
    L = ["// generated by scripts/verify_arch_units.py", "package main", "",
         "import (", '\t"encoding/binary"', '\t"fmt"', '\t"os"',
         '\tarchunits "archunits"', ")", "",
         "var s_ uint64",
         "func rnd() uint64 { s_ ^= s_ << 13; s_ ^= s_ >> 7; s_ ^= s_ << 17;"
         " return s_ }", "",
         "func slurp(d string, idx int, n int) []uint64 {",
         '\traw, err := os.ReadFile(fmt.Sprintf("%s/%03d.bin", d, idx))',
         "\tif err != nil { panic(err) }",
         "\tv := make([]uint64, n)",
         "\tfor i := 0; i < n; i++ {"
         " v[i] = binary.LittleEndian.Uint64(raw[i*8:]) }",
         "\treturn v", "}", ""]
    for u in units:
        L.append(gen_check_go(u))
        L.append("")
    L.append("func main() {\n\tr, e := os.Args[1], os.Args[2]")
    for u in units:
        L.append("\tcheck_%03d(r, e)" % u["index"])
    L.append("}")
    return "\n".join(L) + "\n"


def gen_check_go(u):
    ops, edges, total = plan(u)
    n = len(ops)
    name = u["languages"]["go"]["entry"]
    call = "archunits.%s(%s)" % (name, ", ".join("c%d" % i for i in range(n)))
    L = []
    for i, e in enumerate(edges):
        L.append("var f_%03d_%d = []uint64{%s}"
                 % (u["index"], i, ",".join("0x%x" % v for v in e)))
    L += ["func check_%03d(refd, emud string) {" % u["index"],
          "\trefv := slurp(refd, %d, %d)" % (u["index"], total),
          "\txl := slurp(emud, %d, %d)" % (u["index"], total),
          "\ts_ = %s" % SEED,
          "\tk, mism, nand, xlm, shown := 0, 0, 0, 0, 0",
          "\tvar %s uint64" % ", ".join("c%d" % i for i in range(n)),
          "\t_ = c0"]
    ex = "\n\t\t\t\t\t\t".join('fmt.Printf(" %%#x", c%d)' % i
                               for i in range(n))
    chk = "\n".join([
        "\t\t{",
        "\t\t\tgot := %s" % call,
        "\t\t\twant := refv[k]",
        "\t\t\tif got != want {",
        "\t\t\t\tif %s && %s {" % (nan_test("go", u["result_kind"], "got"),
                                   nan_test("go", u["result_kind"], "want")),
        "\t\t\t\t\tnand++",
        "\t\t\t\t} else {",
        "\t\t\t\t\tmism++",
        "\t\t\t\t\tif shown < 4 { shown++",
        '\t\t\t\t\t\tfmt.Printf("EX %d MISMATCH")' % u["index"],
        "\t\t\t\t\t\t%s" % ex,
        '\t\t\t\t\t\tfmt.Printf(" want %#x got %#x\\n", want, got) }',
        "\t\t\t\t}",
        "\t\t\t}",
        "\t\t\tif got != xl[k] { xlm++ }",
        "\t\t\tk++",
        "\t\t}"])
    for i in range(n):
        L.append("\t%sfor _, x%d := range f_%03d_%d {"
                 % ("\t" * i, i, u["index"], i))
    for i in range(n):
        L.append("\t%sc%d = x%d" % ("\t" * n, i, i))
    L.append(chk)
    L.append("\t" + "}" * n)
    L.append("\tfor q := 0; q < %d; q++ {" % N_RAND)
    for i, p in enumerate(ops):
        L.append(rand_line("go", i, p, "\t\t"))
    L.append(chk)
    L.append("\t}")
    L.append("\tfor q := 0; q < %d; q++ {" % N_BAND)
    L += band_lines("go", ops, "\t\t")
    L.append(chk)
    L.append("\t}")
    L.append('\tfmt.Printf("RESULT %d %%d %%d %%d %%d\\n", k, mism, nand,'
             " xlm)" % u["index"])
    L.append("}")
    return "\n".join(L)


# ==================================================================== build ==
def parallel(cmds, what):
    import concurrent.futures as cf
    with cf.ThreadPoolExecutor(max_workers=JOBS) as ex:
        for rc, o, e in ex.map(lambda c: run(c), cmds):
            if rc:
                raise SystemExit("%s failed:\n%s\n%s" % (what, o[-3000:],
                                                         e[-6000:]))


def build_c(units, work):
    od = os.path.join(work, "obj_c")
    os.makedirs(od, exist_ok=True)
    inc = ["-I" + os.path.join(EMUL, "c"), "-I" + os.path.join(OUT, "c")]
    srcs = ([os.path.join(EMUL, "c", f)
             for f in sorted(os.listdir(os.path.join(EMUL, "c")))
             if f.endswith(".c")]
            + [os.path.join(OUT, "c", u["name"] + ".c") for u in units])
    cmds = [["clang", "-O2", "-std=c17", "-c", s, "-o",
             os.path.join(od, os.path.basename(s)[:-2] + ".o")] + inc
            for s in srcs]
    parallel(cmds, "clang -c (arch units)")
    h = os.path.join(work, "h_c.c")
    open(h, "w").write(gen_harness_c(units, False))
    objs = [os.path.join(od, f) for f in sorted(os.listdir(od))]
    must(["clang", "-O2", "-std=c17", h] + objs + inc
         + ["-o", os.path.join(work, "h_c")], "link h_c")


def build_cpp(units, work):
    od = os.path.join(work, "obj_cpp")
    os.makedirs(od, exist_ok=True)
    inc = ["-I" + os.path.join(EMUL, "cpp"), "-I" + os.path.join(OUT, "cpp")]
    srcs = ([os.path.join(EMUL, "cpp", f)
             for f in sorted(os.listdir(os.path.join(EMUL, "cpp")))
             if f.endswith(".cpp")]
            + [os.path.join(OUT, "cpp", u["name"] + ".cpp") for u in units])
    cmds = [["clang++", "-O2", "-std=c++20", "-c", s, "-o",
             os.path.join(od, os.path.basename(s)[:-4] + ".o")] + inc
            for s in srcs]
    parallel(cmds, "clang++ -c (arch units)")
    h = os.path.join(work, "h_cpp.cpp")
    open(h, "w").write(gen_harness_c(units, True))
    objs = [os.path.join(od, f) for f in sorted(os.listdir(od))]
    must(["clang++", "-O2", "-std=c++20", h] + objs + inc
         + ["-o", os.path.join(work, "h_cpp")], "link h_cpp")


def build_rust(units, work):
    rl = os.path.join(work, "rlib")
    os.makedirs(rl, exist_ok=True)
    must(["rustc", "-O", "--edition", "2021", "--crate-type=rlib",
          "--crate-name", "sfemul", os.path.join(EMUL, "rust", "lib.rs"),
          "--out-dir", rl, "-A", "warnings"], "rustc sfemul")
    must(["rustc", "-O", "--edition", "2021", "--crate-type=rlib",
          "--crate-name", "archunits", os.path.join(OUT, "rust", "lib.rs"),
          "--extern", "sfemul=" + os.path.join(rl, "libsfemul.rlib"),
          "-L", "dependency=" + rl,
          "--out-dir", rl, "-A", "warnings"], "rustc archunits")
    h = os.path.join(work, "h_rust.rs")
    open(h, "w").write(gen_harness_rust(units))
    must(["rustc", "-O", "--edition", "2021", h,
          "--extern", "archunits=" + os.path.join(rl, "libarchunits.rlib"),
          "--extern", "sfemul=" + os.path.join(rl, "libsfemul.rlib"),
          "-L", "dependency=" + rl,
          "-o", os.path.join(work, "h_rust"), "-A", "warnings"], "rustc h_rust")


GO_ENV = dict(os.environ, GOFLAGS="-mod=mod", GO111MODULE="on",
              GOPATH=os.path.join(SCRATCH, "gopath"),
              GOCACHE=os.path.join(SCRATCH, "gocache"))


def build_go(units, work):
    d = os.path.join(work, "go_h")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "main.go"), "w").write(gen_harness_go(units))
    open(os.path.join(d, "go.mod"), "w").write(
        "module harness\n\ngo 1.21\n\n"
        "require archunits v0.0.0\nrequire softfloat_emul v0.0.0\n\n"
        "replace archunits => %s\nreplace softfloat_emul => %s\n"
        % (os.path.join(OUT, "go"), os.path.join(EMUL, "go")))
    must(["go", "build", "-o", os.path.join(work, "h_go"), "."],
         "go build harness", cwd=d, env=GO_ENV)


def build_ref(units, work):
    rc = os.path.join(work, "ref_c.c")
    open(rc, "w").write(gen_ref_c(units))
    must(["clang", "-O2", "-std=c17", rc, "-o", os.path.join(work, "ref_c")],
         "clang ref_c")
    d = os.path.join(work, "go_ref")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "main.go"), "w").write(gen_ref_go(units))
    open(os.path.join(d, "go.mod"), "w").write("module refgo\n\ngo 1.21\n")
    must(["go", "build", "-o", os.path.join(work, "ref_go"), "."],
         "go build ref", cwd=d, env=GO_ENV)


# ====================================================================== run ==
def parse_out(text):
    res, ex = {}, []
    for line in text.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "RESULT":
            res[int(f[1])] = dict(zip(("tested", "mismatch", "nan_divergent",
                                       "cross_lang_mismatch"),
                                      [int(x) for x in f[2:6]]))
        elif f[0] in ("EX", "EXN"):
            ex.append(line)
    return res, ex


def main():
    units = json.load(open(os.path.join(OUT, "_units.json")))["units"]
    if ONLY:
        keep = set(int(x) for x in ONLY.split(","))
        units = [u for u in units if u["index"] in keep]
    work = SCRATCH
    os.makedirs(work, exist_ok=True)
    refd = os.path.join(work, "ref")
    emud = os.path.join(work, "emu")
    for d in (refd, emud):
        os.makedirs(d, exist_ok=True)

    note("building references (native operator, host -O2) ...")
    build_ref(units, work)
    note("building the four integer-only harnesses ...")
    build_c(units, work)
    build_cpp(units, work)
    build_rust(units, work)
    build_go(units, work)

    note("running references ...")
    must([os.path.join(work, "ref_c"), refd], "ref_c run")
    must([os.path.join(work, "ref_go"), refd], "ref_go run")

    out = {}
    note("running c   (writes the cross-language reference stream) ...")
    o = must([os.path.join(work, "h_c"), refd, emud, "1"], "h_c run")
    out["c"] = parse_out(o)
    for lang in ("cpp", "rust", "go"):
        note("running %s ..." % lang)
        o = must([os.path.join(work, "h_" + lang), refd, emud, "0"],
                 "h_%s run" % lang)
        out[lang] = parse_out(o)

    summary = {"n_rand": N_RAND, "n_band": N_BAND, "seed": SEED,
               "per_unit": {}, "examples": {l: out[l][1] for l in out}}
    tot = {l: dict(tested=0, mismatch=0, nan_divergent=0,
                   cross_lang_mismatch=0) for l in out}
    for u in units:
        i = u["index"]
        rec = {}
        for lang in out:
            r = out[lang][0].get(i)
            rec[lang] = r
            if r:
                for k in tot[lang]:
                    tot[lang][k] += r[k]
        summary["per_unit"][str(i)] = rec
    summary["totals"] = tot
    json.dump(summary, open(os.path.join(work, "verdict.json"), "w"), indent=1)
    note(json.dumps(tot, indent=1))
    for lang in out:
        for line in out[lang][1][:20]:
            note(lang, line)
    note("verdict written to", os.path.join(work, "verdict.json"))


if __name__ == "__main__":
    main()
