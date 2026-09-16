#!/usr/bin/env python3
"""
Core of the CONTEXT-SPECIALISED slicing of Berkeley SoftFloat for riscv64.

Difference from the previous (generic) run:
  * softfloat_state.c, s_approxRecipSqrt_1Ks.c and s_approxRecip_1Ks.c are
    ALWAYS linked, so nothing dangles;
  * the rounding mode Sail fixes at the call site is applied, either by
    pinning the global (a copy of softfloat_state.c with a literal
    initialiser) or, for the roundToInt family, by a per-mode wrapper that
    passes the mode as a literal;
  * globalopt + ipsccp are in the pass list so the constant propagates.

Read-only on $SF; every artefact lands under SCRATCH.
"""

import os
import re
import subprocess
import sys

SF = (HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/"
      "berkeley-softfloat-3")
SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad")
OLD = ("/tmp/claude-1000/-home-<user>-Programming/"
       "6fc7a103-e75c-45df-aff2-b85555e7a824/scratchpad")
B = "/usr/lib/llvm-21/bin"
CLANG = "clang"

sys.path.insert(0, os.path.join(SCRATCH, "lib"))
import sfmeasure as M                                    # noqa: E402

HOME = os.path.expanduser("~")   # no machine path is written into this file

DEFINES = [
    "-DSOFTFLOAT_FAST_INT64",
    "-DSOFTFLOAT_ROUND_ODD",
    "-DINLINE_LEVEL=5",
    "-DSOFTFLOAT_FAST_DIV32TO16",
    "-DSOFTFLOAT_FAST_DIV64TO32",
]
INCLUDES = [
    "-I" + SF + "/build/Linux-RISCV64-GCC",
    "-I" + SF + "/source/RISCV",
    "-I" + SF + "/source/include",
    "-idirafter", SCRATCH + "/shim",
]
TARGET = ["--target=riscv64-unknown-elf", "-march=rv64im", "-mabi=lp64", "-O1"]

SRC_DIRS = ("source", "source/RISCV")

# the three that must always be present: state (roundingMode / exceptionFlags /
# detectTininess) and the two sqrt lookup TABLES (data, not code)
ALWAYS = [
    os.path.join(SF, "source", "s_approxRecipSqrt_1Ks.c"),
    os.path.join(SF, "source", "s_approxRecip_1Ks.c"),
]
STATE_SRC = os.path.join(SF, "source", "softfloat_state.c")

PASSES = ("internalize,globalopt,ipsccp,always-inline,inline,globaldce,"
          "instcombine,simplifycfg,dce,globalopt,globaldce")
PASSES_NOFIX = PASSES.replace("instcombine,", "instcombine<no-verify-fixpoint>,")

MODES = [0, 1, 2, 3, 4, 6]          # softfloat.h: near_even, minMag, min, max,
MODE_NAMES = {0: "near_even", 1: "minMag", 2: "min", 3: "max",
              4: "near_maxMag", 6: "odd"}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, (p.stderr or "").strip()


# ------------------------------------------------------------- bitcode ------
_bc = {}


def to_bitcode(cfile, outdir):
    key = (cfile, outdir)
    if key in _bc:
        return _bc[key]
    base = os.path.basename(cfile)[:-2]
    tag = "RISCV_" + base if "/RISCV/" in cfile else base
    out = os.path.join(outdir, tag + ".bc")
    rc, _, err = run([CLANG] + TARGET + ["-Werror-implicit-function-declaration"]
                     + DEFINES + INCLUDES + ["-emit-llvm", "-c", cfile, "-o", out])
    res = (out if rc == 0 else None, err)
    _bc[key] = res
    return res


_nm = {}


def nm(bcfile):
    if bcfile in _nm:
        return _nm[bcfile]
    rc, out, _ = run([B + "/llvm-nm", bcfile])
    defined, undef = set(), set()
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        typ, name = parts[-2], parts[-1]
        if typ == "U":
            undef.add(name)
        elif typ in ("T", "t", "W", "w", "D", "d", "B", "b", "R", "r", "V", "v"):
            defined.add(name)
    _nm[bcfile] = (defined, undef)
    return defined, undef


def find_source(sym, bcdir):
    base = sym[len("softfloat_"):] if sym.startswith("softfloat_") else sym
    for cand in ("s_" + base, sym, base):
        for sub in SRC_DIRS:
            p = os.path.join(SF, sub, cand + ".c")
            if not os.path.exists(p):
                continue
            bc, _ = to_bitcode(p, bcdir)
            if bc is None:
                continue
            d, _ = nm(bc)
            if sym in d:
                return p
    return None


def link_closure(seed_files, bcdir):
    """Fixed point over undefined symbols, starting from seed_files."""
    files = list(seed_files)
    seen = set(files)
    unresolved = set()
    while True:
        bcs = []
        for f in files:
            bc, err = to_bitcode(f, bcdir)
            if bc is None:
                raise RuntimeError("compile failed %s: %s" % (f, err[:300]))
            bcs.append(bc)
        undef, defined = set(), set()
        for bc in bcs:
            d, u = nm(bc)
            undef |= u
            defined |= d
        added = False
        for sym in sorted(undef - defined - unresolved):
            if sym.startswith("__"):
                unresolved.add(sym)
                continue
            p = find_source(sym, bcdir)
            if p is None:
                unresolved.add(sym)
                continue
            if p not in seen:
                seen.add(p)
                files.append(p)
                added = True
        if not added:
            return files, bcs, sorted(unresolved)


# ------------------------------------------------------- pinned state -------
def pinned_state(mode, outdir):
    """A copy of softfloat_state.c with the roundingMode initialiser replaced
    by the literal `mode`.  Written into SCRATCH; the original is untouched."""
    src = open(STATE_SRC).read()
    new, n = re.subn(
        r"softfloat_roundingMode\s*=\s*softfloat_round_near_even\s*;",
        "softfloat_roundingMode = %d;" % mode, src)
    if n != 1:
        raise RuntimeError("could not pin roundingMode (matched %d)" % n)
    p = os.path.join(outdir, "softfloat_state_rm%d.c" % mode)
    open(p, "w").write(new)
    return p


def generic_state(outdir):
    """State file for the GENERIC slice: the rounding mode must stay an unknown
    runtime value, so it is marked volatile.  Without that, `internalize` plus
    `globalopt` would see a never-written internal global and fold its
    initialiser (near_even), silently producing the mode-0 slice and calling it
    generic."""
    src = open(STATE_SRC).read()
    new, n = re.subn(
        r"THREAD_LOCAL uint_fast8_t softfloat_roundingMode\s*=\s*"
        r"softfloat_round_near_even\s*;",
        "THREAD_LOCAL volatile uint_fast8_t softfloat_roundingMode_v = "
        "softfloat_round_near_even;\n"
        "THREAD_LOCAL uint_fast8_t softfloat_roundingMode = 0;\n"
        "__attribute__((constructor)) static void _sf_rm_unknown(void)"
        " { softfloat_roundingMode = softfloat_roundingMode_v; }",
        src)
    if n != 1:
        raise RuntimeError("could not build generic state (matched %d)" % n)
    p = os.path.join(outdir, "softfloat_state_generic.c")
    open(p, "w").write(new)
    return p


# ------------------------------------------- mode-as-parameter operations ---
# Not just the roundToInt family: every float-to-integer conversion takes the
# rounding mode as an ARGUMENT too, and c_emulator/riscv_softfloat.cpp passes
# the same literal into it —
#     softfloat_init(rm); ... res.v = f64_to_i64(a, uint8_of_rm(rm), true);
# so pinning the global alone would leave those twelve untouched and they would
# look mode-independent when they are not.  Signatures are parsed from
# softfloat.h rather than assumed.
def _parse_prototypes():
    hdr = open(os.path.join(SF, "source/include/softfloat.h")).read()
    hdr = re.sub(r"/\*.*?\*/", "", hdr, flags=re.S)
    hdr = " ".join(hdr.split())
    protos = {}
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_ ]*?)\s+([A-Za-z_][A-Za-z0-9_]*)"
                         r"\s*\(([^)]*)\)\s*;", hdr):
        protos[m.group(2)] = (m.group(1).strip(),
                              [a.strip() for a in m.group(3).split(",")])
    return protos


PROTOS = _parse_prototypes()


def takes_mode_parameter(op):
    ret_args = PROTOS.get(op)
    return bool(ret_args and any("uint_fast8_t" in a for a in ret_args[1]))


def param_wrapper(op, mode, outdir, fix_exact=None):
    """A wrapper that calls the operation with the mode as a LITERAL.  The
    wrapper is the only public symbol, so `inline` folds the operation into it
    and ipsccp kills every arm the literal cannot reach.

    fix_exact additionally pins the trailing `bool exact`, which the emulator
    also passes as a literal `true` for the twelve float-to-integer
    conversions (it stays a real argument for roundToInt, which is FROUND vs
    FROUNDNX)."""
    ret, args = PROTOS[op]
    name = "%s_rm%d%s" % (op, mode, "_exact" if fix_exact is not None else "")
    params, actuals, n = [], [], 0
    for a in args:
        if a == "uint_fast8_t":
            actuals.append(str(mode))
            continue
        if a == "bool" and fix_exact is not None:
            actuals.append("true" if fix_exact else "false")
            continue
        params.append("%s a%d" % (a, n))
        actuals.append("a%d" % n)
        n += 1
    body = ('#include <stdbool.h>\n'
            '#include <stdint.h>\n'
            '#include "platform.h"\n'
            '#include "softfloat_types.h"\n'
            '#include "softfloat.h"\n'
            '%s %s( %s )\n'
            '{\n'
            '    return %s( %s );\n'
            '}\n' % (ret, name, ", ".join(params), op, ", ".join(actuals)))
    p = os.path.join(outdir, name + ".c")
    open(p, "w").write(body)
    return p, name


# ---------------------------------------------------------------- slice -----
def opt_slice(bcs, entry, wdir, tag, force_inline_syms=None):
    linked = os.path.join(wdir, tag + ".linked.bc")
    rc, _, err = run([B + "/llvm-link"] + bcs + ["-o", linked])
    if rc:
        raise RuntimeError("llvm-link: " + err[:300])
    sbc = os.path.join(wdir, tag + ".bc")
    passes = PASSES
    if force_inline_syms is not None:
        passes = passes.replace("internalize,", "internalize,forceattrs,")
    cmd = [B + "/opt", "-passes=" + passes,
           "-internalize-public-api-list=" + entry]
    for s in (force_inline_syms or []):
        cmd.append("-force-attribute=" + s + ":alwaysinline")
    cmd += [linked, "-o", sbc]
    rc, _, err = run(cmd)
    if rc and "did not reach a fixpoint" in err:
        passes = passes.replace("instcombine,", "instcombine<no-verify-fixpoint>,")
        cmd[1] = "-passes=" + passes
        rc, _, err = run(cmd)
    if rc:
        raise RuntimeError("opt: " + err[:300])
    sobj = os.path.join(wdir, tag + ".o")
    rc, _, err = run([B + "/llc", "-march=riscv64", "-mattr=+m", "-O2",
                      "-filetype=obj", sbc, "-o", sobj])
    if rc:
        raise RuntimeError("llc: " + err[:300])
    return linked, sbc, sobj, passes


def per_symbol_counts(dis):
    counts, cur = {}, None
    for line in dis.splitlines():
        h = M.HDR_RE.match(line.strip())
        if h:
            cur = h.group(2)
            counts.setdefault(cur, 0)
            continue
        if cur and M.INSN_RE.match(line):
            counts[cur] += 1
    return counts
