#!/usr/bin/env python3
"""Differential test: the four emulations against Berkeley SoftFloat itself.

SoftFloat is built HERE, from the copy vendored in the Sail model's own tree,
with the model's own defines and the RISCV specialisation, and wrapped so that
every operation becomes one `uint64_t sfref_<op>(uint64_t, ...)` with the
rounding mode pinned to the mode under test and `exact` pinned to `true` for
the twelve float-to-integer conversions, exactly as
`c_emulator/riscv_softfloat.cpp` does it.

c and c++ call that wrapper directly, rust through `extern "C"`, go through
cgo; all four are in-process, so what is compared is the returned bits, not a
transcript.

Inputs per operation, identical in all four languages because all four run the
same xorshift64 from the same seed in the same order:

  * every edge case per operand - +/-0, +/-inf, quiet and signalling NaN,
    largest and smallest normal, largest and smallest subnormal, +/-1, +/-2,
    +/-0.5, and one ulp either side of each - crossed with itself over all
    operands;
  * 200,000 uniform random bit patterns per operand;
  * 100,000 with the exponent banded around the bias, so subnormals, the
    rounding path and overflow are actually reached rather than drowned in
    the NaNs a uniform pattern produces.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import emul_spec as S                                           # noqa: E402

HOME = os.path.expanduser("~")   # no machine path is written into this file

BASE = os.path.dirname(HERE)
EMU = os.path.join(BASE, "emulations")
SF = (HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/"
      "berkeley-softfloat-3")
SCRATCH = os.environ.get(
    "EMUL_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/emul")

DEFINES = ["-DSOFTFLOAT_FAST_INT64", "-DSOFTFLOAT_ROUND_ODD",
           "-DINLINE_LEVEL=5", "-DSOFTFLOAT_FAST_DIV32TO16",
           "-DSOFTFLOAT_FAST_DIV64TO32"]
INCLUDES = ["-I" + os.path.join(SCRATCH, "sfbuild"),
            "-I" + SF + "/source/RISCV",
            "-I" + SF + "/source/include"]

C_DIR = os.environ.get("EMUL_C_DIR")            # alt-pin probe override
ONLY = [x for x in os.environ.get("EMUL_ONLY", "").split(",") if x]

N_RAND = int(os.environ.get("NRAND", 200000))
N_BAND = int(os.environ.get("NBAND", 100000))
SEED = "0x9E3779B97F4A7C15"


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, p.stdout, p.stderr


def note(*a):
    print(*a, flush=True)


# ------------------------------------------------------- softfloat, host ---
def softfloat_objects():
    """The object list the model's own Makefile builds, read from it."""
    mk = open(os.path.join(SF, "build", "Linux-RISCV64-GCC", "Makefile")).read()
    names = []
    for block in re.findall(r"^OBJS_\w+ = \\\n((?:.*\\\n)*)", mk, re.M):
        for line in block.splitlines():
            m = re.match(r"\s*(\S+)\$\(OBJ\)", line)
            if m:
                names.append(m.group(1))
    out = []
    for n in names:
        for d in ("RISCV", ""):
            p = os.path.join(SF, "source", d, n + ".c")
            if os.path.exists(p):
                out.append(p)
                break
        else:
            raise SystemExit("missing softfloat source " + n)
    return out


def build_softfloat():
    bd = os.path.join(SCRATCH, "sfbuild")
    os.makedirs(bd, exist_ok=True)
    # platform.h: the host build directory's, because the riscv one spells
    # INLINE as bare `inline`, which under C17 needs an external definition.
    # Everything that decides SEMANTICS - the RISCV specialisation and the
    # five defines - is the model's own.
    src = open(os.path.join(SF, "build", "Linux-x86_64-GCC",
                            "platform.h")).read()
    open(os.path.join(bd, "platform.h"), "w").write(src)
    objs = []
    srcs = softfloat_objects()
    for c in srcs:
        o = os.path.join(bd, os.path.basename(c)[:-2] + ".o")
        if not os.path.exists(o) or os.path.getmtime(o) < os.path.getmtime(c):
            rc, _, err = run(["clang", "-O2", "-fPIC",
                              "-Werror-implicit-function-declaration"]
                             + DEFINES + INCLUDES + ["-c", c, "-o", o])
            if rc:
                raise SystemExit("softfloat build failed on %s\n%s" % (c, err))
        objs.append(o)
    lib = os.path.join(SCRATCH, "libsfhost.a")
    rc, _, err = run(["ar", "crs", lib] + objs)
    if rc:
        raise SystemExit("ar failed: " + err)
    note("softfloat: %d objects -> %s" % (len(objs), lib))
    return lib


# ------------------------------------------------------------ the oracle ---
def sf_ret_expr(ret, call):
    if ret.kind == "float":
        return "(uint64_t)(%s).v" % call
    if ret.kind == "bool":
        return "(uint64_t)((%s) ? 1 : 0)" % call
    if ret.width == 32:
        return "(uint64_t)(uint32_t)(%s)" % call
    return "(uint64_t)(%s)" % call


def gen_oracle(mode):
    h = ["/* generated by scripts/verify_emulations.py */",
         "#ifndef ORACLE_H", "#define ORACLE_H", "#include <stdint.h>",
         '#ifdef __cplusplus', 'extern "C" {', "#endif", ""]
    c = ["/* generated by scripts/verify_emulations.py */",
         "#include <stdint.h>", "#include <stdbool.h>",
         '#include "softfloat.h"', '#include "oracle.h"', "",
         "#define RM ((uint_fast8_t)%d)" % mode, ""]
    for op in S.OPS:
        params, ret, kind = S.spec(op)
        args = ", ".join("uint64_t a%d" % i for i in range(len(params)))
        h.append("uint64_t sfref_%s(%s);" % (op, args))
        c.append("uint64_t sfref_%s(%s)" % (op, args))
        c.append("{")
        c.append("    softfloat_exceptionFlags = 0;")
        c.append("    softfloat_roundingMode = RM;")
        names = []
        for i, p in enumerate(params):
            if p.kind == "float":
                t = S.SF_FLOAT_T[p.tag]
                ut = {16: "uint16_t", 32: "uint32_t", 64: "uint64_t"}[p.width]
                c.append("    %s x%d; x%d.v = (%s)a%d;" % (t, i, i, ut, i))
            elif p.kind == "bool":
                c.append("    bool x%d = (a%d & 1) != 0;" % (i, i))
            else:
                t = {(32, True): "int32_t", (32, False): "uint32_t",
                     (64, True): "int64_t", (64, False): "uint64_t"}[
                         (p.width, p.signed)]
                c.append("    %s x%d = (%s)a%d;" % (t, i, t, i))
            names.append("x%d" % i)
        if kind == "rm_exact":
            call = "%s(%s, RM, true)" % (op, names[0])
        elif kind == "rm_exactarg":
            call = "%s(%s, RM, %s)" % (op, names[0], names[1])
        else:
            call = "%s(%s)" % (op, ", ".join(names))
        c.append("    return %s;" % sf_ret_expr(ret, call))
        c.append("}")
        c.append("")
    h += ["", "#ifdef __cplusplus", "}", "#endif", "#endif"]
    d = os.path.join(SCRATCH, "oracle")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "oracle.h"), "w").write("\n".join(h) + "\n")
    open(os.path.join(d, "oracle.c"), "w").write("\n".join(c) + "\n")
    o = os.path.join(d, "oracle.o")
    rc, _, err = run(["clang", "-O2", "-fPIC"] + DEFINES + INCLUDES
                     + ["-I" + d, "-c", os.path.join(d, "oracle.c"), "-o", o])
    if rc:
        raise SystemExit("oracle build failed:\n" + err)
    return d, o


# ----------------------------------------------------------- case vectors --
def case_plan(op):
    """(edges per operand, mask per operand, banded recipe per operand)."""
    params, ret, _ = S.spec(op)
    return params, [S.edges(p) for p in params]


# --------------------------------------------------------------- harnesses -
def _loop_bounds(edges):
    return [len(e) for e in edges]


class Emit(object):
    """Shared shape of the four harnesses; each backend fills the holes."""

    def __init__(self, entries, sigs):
        self.entries = entries          # op -> entry symbol for this language
        self.sigs = sigs                # op -> {'params': [w], 'ret': w}


C_HEAD = r"""/* generated by scripts/verify_emulations.py */
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include "sfemul.h"
#include "oracle.h"

static uint64_t S_;
static void seed(void) { S_ = %sULL; }
static uint64_t rnd(void) {
    S_ ^= S_ << 13; S_ ^= S_ >> 7; S_ ^= S_ << 17; return S_;
}
""" % SEED

CPP_HEAD = r"""// generated by scripts/verify_emulations.py
#include <cstdint>
#include <cstdio>
#include "sfemul.hpp"
#include "oracle.h"

using namespace sfemul;

static uint64_t S_;
static void seed() { S_ = %sULL; }
static uint64_t rnd() {
    S_ ^= S_ << 13; S_ ^= S_ >> 7; S_ ^= S_ << 17; return S_;
}
""" % SEED


def c_argexpr(w, i):
    if w == 64:
        return "(uint64_t)c%d" % i
    if w == 32:
        return "(uint32_t)c%d" % i
    if w == 1:
        return "((c%d & 1) != 0)" % i
    raise ValueError(w)


def c_retexpr(w, call):
    if w == 1:
        return "(uint64_t)((%s) ? 1 : 0)" % call
    if w == 32:
        return "(uint64_t)(uint32_t)(%s)" % call
    return "(uint64_t)(%s)" % call


def gen_c_like(cpp=False):
    L = [CPP_HEAD if cpp else C_HEAD]
    idx = json.load(open(os.path.join(EMU, "_index.json")))["entries"]
    lang = "cpp" if cpp else "c"
    sigs = json.load(open(os.path.join(EMU, "_emitted.json")))
    for op in S.OPS:
        params, edges = case_plan(op)
        entry = idx[op][lang]
        sig = sigs[op]["signature"]
        n = len(params)
        for i, e in enumerate(edges):
            L.append("static const unsigned long long E_%s_%d[] = {%s};"
                     % (op, i, ",".join("0x%xULL" % v for v in e)))
        call = "%s(%s)" % (entry,
                           ", ".join(c_argexpr(sig["params"][i], i)
                                     for i in range(n)))
        chk = ["    {",
               "        unsigned long long want = sfref_%s(%s);"
               % (op, ", ".join("c%d" % i for i in range(n))),
               "        unsigned long long got = %s;"
               % c_retexpr(sig["ret"], call),
               "        tested++;",
               "        if (want != got) {",
               "            mism++;",
               "            if (shown < 8) { shown++;",
               '                printf("MISMATCH %s in");' % op,
               "                %s" % " ".join(
                   'printf(" 0x%%llx", c%d);' % i for i in range(n)),
               '                printf(" want 0x%llx got 0x%llx\\n",'
               " want, got);",
               "            }",
               "        }",
               "    }"]
        chk = "\n".join(chk)
        body = ["static void run_%s(void)" % op if not cpp
                else "static void run_%s()" % op, "{",
                "    unsigned long long tested = 0, mism = 0, shown = 0;",
                "    unsigned long long %s;"
                % ", ".join("c%d" % i for i in range(n)),
                "    seed();"]
        for i in range(n):
            body.append("    %sfor (unsigned long long i%d = 0; i%d < %d;"
                        " i%d++) {" % ("    " * i, i, i, len(edges[i]), i))
        for i in range(n):
            body.append("    %sc%d = E_%s_%d[i%d];" % ("    " * n, i, op, i, i))
        body.append(chk)
        body.append("    " + "}" * n)
        body.append("    for (unsigned long long q = 0; q < %dULL; q++) {"
                    % N_RAND)
        for i, p in enumerate(params):
            body.append("        c%d = rnd() & 0x%xULL;" % (i, p.mask))
        body.append(chk)
        body.append("    }")
        body.append("    for (unsigned long long q = 0; q < %dULL; q++) {"
                    % N_BAND)
        for i, p in enumerate(params):
            if p.kind == "float":
                body.append(
                    "        { unsigned long long sg = rnd() & 1ULL;\n"
                    "          unsigned long long ex = (unsigned long long)"
                    "(%d + (long long)(rnd() %% 33) - 16) & 0x%xULL;\n"
                    "          unsigned long long mn = rnd() & 0x%xULL;\n"
                    "          c%d = (sg << %d) | (ex << %d) | mn; }"
                    % (p.bias, (1 << p.exp) - 1, (1 << p.man) - 1,
                       i, p.width - 1, p.man))
            else:
                body.append("        c%d = rnd() & 0x%xULL;" % (i, p.mask))
        body.append(chk)
        body.append("    }")
        body.append('    printf("OP %s TESTED %%llu MISMATCHES %%llu\\n",'
                    " tested, mism);" % op)
        body.append("}")
        L.append("\n".join(body))
    L.append("int main(void)\n{")
    for op in S.OPS:
        L.append("    run_%s();" % op)
    L.append("    return 0;\n}")
    return "\n\n".join(L) + "\n"


RUST_HEAD = r"""// generated by scripts/verify_emulations.py
#![allow(non_snake_case, unused_parens)]
use std::process::ExitCode;

#[inline(always)]
fn rnd(s: &mut u64) -> u64 {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17; *s
}
"""


def r_argexpr(w, i):
    if w == 64:
        return "c%d as u64" % i
    if w == 32:
        return "c%d as u32" % i
    if w == 1:
        return "((c%d & 1) != 0)" % i
    raise ValueError(w)


def r_retexpr(w, call):
    if w == 1:
        return "(if %s { 1u64 } else { 0u64 })" % call
    return "((%s) as u64)" % call


def gen_rust():
    idx = json.load(open(os.path.join(EMU, "_index.json")))["entries"]
    sigs = json.load(open(os.path.join(EMU, "_emitted.json")))
    L = [RUST_HEAD, 'extern "C" {']
    for op in S.OPS:
        n = len(S.spec(op)[0])
        L.append("    fn sfref_%s(%s) -> u64;"
                 % (op, ", ".join("a%d: u64" % i for i in range(n))))
    L.append("}")
    for op in S.OPS:
        params, edges = case_plan(op)
        sig = sigs[op]["signature"]
        entry = idx[op]["rust"]
        n = len(params)
        for i, e in enumerate(edges):
            L.append("static E_%s_%d: [u64; %d] = [%s];"
                     % (op, i, len(e), ",".join("0x%x" % v for v in e)))
        call = "sfemul::%s::%s(%s)" % (op, entry,
                                       ", ".join(r_argexpr(sig["params"][i], i)
                                                 for i in range(n)))
        chk = ["        let want: u64 = unsafe { sfref_%s(%s) };"
               % (op, ", ".join("c%d" % i for i in range(n))),
               "        let got: u64 = %s;" % r_retexpr(sig["ret"], call),
               "        tested += 1;",
               "        if want != got {",
               "            mism += 1;",
               "            if shown < 8 { shown += 1;",
               '                println!("MISMATCH %s in %s want 0x{:x}'
               ' got 0x{:x}", %s want, got);'
               % (op, " ".join("0x{:x}" for _ in range(n)),
                  "".join("c%d, " % i for i in range(n))),
               "            }",
               "        }"]
        chk = "\n".join(chk)
        body = ["fn run_%s() -> u64 {" % op,
                "    let mut s: u64 = %s;" % SEED,
                "    let (mut tested, mut mism, mut shown): (u64, u64, u64)"
                " = (0, 0, 0);"]
        for i in range(n):
            body.append("    for i%d in 0..%d {" % (i, len(edges[i])))
        body.append("    {")
        for i in range(n):
            body.append("        let c%d: u64 = E_%s_%d[i%d];" % (i, op, i, i))
        body.append(chk)
        body.append("    }")
        body.append("    " + "}" * n)
        body.append("    for _ in 0..%d {" % N_RAND)
        body.append("    {")
        for i, p in enumerate(params):
            body.append("        let c%d: u64 = rnd(&mut s) & 0x%x;"
                        % (i, p.mask))
        body.append(chk)
        body.append("    } }")
        body.append("    for _ in 0..%d {" % N_BAND)
        body.append("    {")
        for i, p in enumerate(params):
            if p.kind == "float":
                body.append(
                    "        let c{i}: u64 = {{\n"
                    "            let sg = rnd(&mut s) & 1;\n"
                    "            let ex = (({bias}i64 + (rnd(&mut s) % 33)"
                    " as i64 - 16) as u64) & 0x{em:x};\n"
                    "            let mn = rnd(&mut s) & 0x{mm:x};\n"
                    "            (sg << {sh}) | (ex << {ms}) | mn }};".format(
                        i=i, bias=p.bias, em=(1 << p.exp) - 1,
                        mm=(1 << p.man) - 1, sh=p.width - 1, ms=p.man))
            else:
                body.append("        let c%d: u64 = rnd(&mut s) & 0x%x;"
                            % (i, p.mask))
        body.append(chk)
        body.append("    } }")
        body.append('    println!("OP %s TESTED {} MISMATCHES {}",'
                    " tested, mism);" % op)
        body.append("    mism")
        body.append("}")
        L.append("\n".join(body))
    L.append("fn main() -> ExitCode {")
    L.append("    let mut bad: u64 = 0;")
    for op in S.OPS:
        L.append("    bad += run_%s();" % op)
    L.append("    if bad == 0 { ExitCode::SUCCESS } else"
             " { ExitCode::FAILURE }\n}")
    return "\n\n".join(L) + "\n"


def g_argexpr(w, i):
    if w == 64:
        return "uint64(c%d)" % i
    if w == 32:
        return "uint32(c%d)" % i
    if w == 1:
        return "((c%d & 1) != 0)" % i
    raise ValueError(w)


def g_retexpr(w, call):
    if w == 1:
        return "b2u(%s)" % call
    return "uint64(%s)" % call


def gen_go(oracle_dir, lib):
    idx = json.load(open(os.path.join(EMU, "_index.json")))["entries"]
    sigs = json.load(open(os.path.join(EMU, "_emitted.json")))
    head = "\n".join([
        "// generated by scripts/verify_emulations.py",
        "package main",
        "",
        "/*",
        "#cgo CFLAGS: -I%s" % oracle_dir,
        "#cgo LDFLAGS: %s %s" % (os.path.join(oracle_dir, "oracle.o"), lib),
        '#include "oracle.h"',
        "*/",
        'import "C"',
        "",
        "import (", '\t"fmt"', '\t"os"', '\temul "softfloat_emul"', ")",
        "",
        "func rnd(s *uint64) uint64 {",
        "\t*s ^= *s << 13", "\t*s ^= *s >> 7", "\t*s ^= *s << 17",
        "\treturn *s", "}",
        "",
        "func b2u(b bool) uint64 {", "\tif b {", "\t\treturn 1", "\t}",
        "\treturn 0", "}"])
    L = [head]
    for op in S.OPS:
        params, edges = case_plan(op)
        sig = sigs[op]["signature"]
        entry = idx[op]["go"]
        n = len(params)
        for i, e in enumerate(edges):
            L.append("var E_%s_%d = [...]uint64{%s}"
                     % (op, i, ",".join("0x%x" % v for v in e)))
        call = "emul.%s(%s)" % (entry,
                                ", ".join(g_argexpr(sig["params"][i], i)
                                          for i in range(n)))
        cargs = ", ".join("C.uint64_t(c%d)" % i for i in range(n))
        chk = ["\t\twant := uint64(C.sfref_%s(%s))" % (op, cargs),
               "\t\tgot := %s" % g_retexpr(sig["ret"], call),
               "\t\ttested++",
               "\t\tif want != got {",
               "\t\t\tmism++",
               "\t\t\tif shown < 8 {",
               "\t\t\t\tshown++",
               '\t\t\t\tfmt.Printf("MISMATCH %s in %s want 0x%%x got 0x%%x'
               '\\n", %s want, got)'
               % (op, " ".join("0x%x" for _ in range(n)),
                  "".join("c%d, " % i for i in range(n))),
               "\t\t\t}",
               "\t\t}"]
        chk = "\n".join(chk)
        body = ["func run_%s() uint64 {" % op,
                "\ts := uint64(%s)" % SEED,
                "\tvar tested, mism, shown uint64"]
        for i in range(n):
            body.append("\tfor i%d := 0; i%d < %d; i%d++ {"
                        % (i, i, len(edges[i]), i))
        body.append("\t{")
        for i in range(n):
            body.append("\t\tc%d := E_%s_%d[i%d]" % (i, op, i, i))
        body.append(chk)
        body.append("\t}")
        body.append("\t" + "}" * n)
        body.append("\tfor q := 0; q < %d; q++ {" % N_RAND)
        body.append("\t{")
        for i, p in enumerate(params):
            body.append("\t\tc%d := rnd(&s) & 0x%x" % (i, p.mask))
        body.append(chk)
        body.append("\t} }")
        body.append("\tfor q := 0; q < %d; q++ {" % N_BAND)
        body.append("\t{")
        for i, p in enumerate(params):
            if p.kind == "float":
                body.append(
                    "\t\tsg%d := rnd(&s) & 1" % i)
                body.append(
                    "\t\tex%d := uint64(int64(%d)+int64(rnd(&s)%%33)-16)"
                    " & 0x%x" % (i, p.bias, (1 << p.exp) - 1))
                body.append("\t\tmn%d := rnd(&s) & 0x%x"
                            % (i, (1 << p.man) - 1))
                body.append("\t\tc%d := (sg%d << %d) | (ex%d << %d) | mn%d"
                            % (i, i, p.width - 1, i, p.man, i))
            else:
                body.append("\t\tc%d := rnd(&s) & 0x%x" % (i, p.mask))
        body.append(chk)
        body.append("\t} }")
        body.append('\tfmt.Printf("OP %s TESTED %%d MISMATCHES %%d\\n",'
                    " tested, mism)" % op)
        body.append("\treturn mism")
        body.append("}")
        L.append("\n".join(body))
    L.append("func main() {")
    L.append("\tvar bad uint64")
    for op in S.OPS:
        L.append("\tbad += run_%s()" % op)
    L.append("\tif bad != 0 {\n\t\tos.Exit(1)\n\t}\n}")
    return "\n\n".join(L) + "\n"


# ------------------------------------------------------------------ build --
def parse_report(out):
    per = {}
    ex = {}
    for line in out.splitlines():
        m = re.match(r"OP (\S+) TESTED (\d+) MISMATCHES (\d+)", line)
        if m:
            per[m.group(1)] = (int(m.group(2)), int(m.group(3)))
        elif line.startswith("MISMATCH "):
            op = line.split()[1]
            ex.setdefault(op, []).append(line)
    return per, ex


def _run_only(results, only):
    for lang in only:
        p = subprocess.run([results[lang]], capture_output=True, text=True,
                           timeout=7200)
        per, ex = parse_report(p.stdout)
        tot = sum(v[0] for v in per.values())
        bad = sum(v[1] for v in per.values())
        note("  %s: %d operations, %d inputs, %d mismatches"
             % (lang, len(per), tot, bad))
        for op in sorted(ex):
            for line in ex[op][:2]:
                note("    " + line)
    return 0


def main():
    mode = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    os.makedirs(SCRATCH, exist_ok=True)
    lib = build_softfloat()
    odir, oobj = gen_oracle(mode)
    note("oracle: %s" % oobj)

    results = {}

    # -------- c
    cdir = C_DIR or os.path.join(EMU, "c")
    csrc = [os.path.join(cdir, op + ".c") for op in S.OPS]
    hc = os.path.join(SCRATCH, "harness.c")
    open(hc, "w").write(gen_c_like(False))
    exe = os.path.join(SCRATCH, "run_c")
    rc, _, err = run(["clang", "-O2", "-std=c17", "-Wall", "-Wextra",
                      "-Wno-unused-parameter",
                      "-I", cdir, "-I", odir, "-o", exe, hc]
                     + csrc + [oobj, lib])
    if rc:
        raise SystemExit("c harness build failed:\n" + err[:4000])
    results["c"] = exe

    # -------- c++
    if ONLY and "cpp" not in ONLY:
        raise SystemExit(_run_only(results, ONLY))
    psrc = [os.path.join(EMU, "cpp", op + ".cpp") for op in S.OPS]
    hp = os.path.join(SCRATCH, "harness.cpp")
    open(hp, "w").write(gen_c_like(True))
    exe = os.path.join(SCRATCH, "run_cpp")
    rc, _, err = run(["clang++", "-O2", "-std=c++20", "-Wall", "-Wextra",
                      "-Wno-unused-parameter", "-I",
                      os.path.join(EMU, "cpp"), "-I", odir, "-o", exe, hp]
                     + psrc + [oobj, lib])
    if rc:
        raise SystemExit("c++ harness build failed:\n" + err[:4000])
    results["cpp"] = exe

    # -------- rust
    rd = os.path.join(SCRATCH, "rust")
    os.makedirs(rd, exist_ok=True)
    rlib = os.path.join(rd, "libsfemul.rlib")
    rc, _, err = run(["rustc", "--edition", "2021", "-O", "--crate-type=lib",
                      "--crate-name", "sfemul", "lib.rs", "-o", rlib],
                     cwd=os.path.join(EMU, "rust"))
    if rc:
        raise SystemExit("rust crate failed:\n" + err[:4000])
    hm = os.path.join(rd, "main.rs")
    open(hm, "w").write(gen_rust())
    exe = os.path.join(SCRATCH, "run_rust")
    rc, _, err = run(["rustc", "--edition", "2021", "-O", hm, "-o", exe,
                      "--extern", "sfemul=" + rlib,
                      "-L", "native=" + SCRATCH,
                      "-C", "link-arg=" + oobj,
                      "-C", "link-arg=" + lib])
    if rc:
        raise SystemExit("rust harness failed:\n" + err[:6000])
    results["rust"] = exe

    # -------- go
    gd = os.path.join(SCRATCH, "goharness")
    os.makedirs(gd, exist_ok=True)
    open(os.path.join(gd, "go.mod"), "w").write(
        "module harness\n\ngo 1.21\n\nrequire softfloat_emul v0.0.0\n\n"
        "replace softfloat_emul => %s\n" % os.path.join(EMU, "go"))
    open(os.path.join(gd, "go.sum"), "w").write("")
    open(os.path.join(gd, "main.go"), "w").write(gen_go(odir, lib))
    exe = os.path.join(SCRATCH, "run_go")
    env = dict(os.environ, GOFLAGS="-mod=mod", GOCACHE=os.path.join(
        SCRATCH, "gocache"), CGO_ENABLED="1")
    p = subprocess.run(["go", "build", "-o", exe, "."], cwd=gd, env=env,
                       capture_output=True, text=True)
    if p.returncode:
        raise SystemExit("go harness failed:\n" + p.stderr[:6000])
    results["go"] = exe

    note("built: " + ", ".join(sorted(results)))

    report = {}
    for lang in ("c", "cpp", "rust", "go"):
        note("running %s ..." % lang)
        p = subprocess.run([results[lang]], capture_output=True, text=True,
                           timeout=7200)
        per, ex = parse_report(p.stdout)
        report[lang] = {"per_op": per, "examples": ex,
                        "exit": p.returncode,
                        "stderr": p.stderr[-2000:]}
        tot = sum(v[0] for v in per.values())
        bad = sum(v[1] for v in per.values())
        note("  %s: %d operations, %d inputs, %d mismatches"
             % (lang, len(per), tot, bad))
    json.dump(report, open(os.path.join(SCRATCH, "report.json"), "w"),
              indent=1)
    note("report -> " + os.path.join(SCRATCH, "report.json"))


if __name__ == "__main__":
    main()
