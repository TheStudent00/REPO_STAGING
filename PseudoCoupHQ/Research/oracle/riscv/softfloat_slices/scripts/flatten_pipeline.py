#!/usr/bin/env python3
"""One (operation, rounding mode, variant, target) through the whole chain.

  slice (context pinned, -Oz)  ->  localise the globals  ->  sroa/instcombine/
  simplifycfg  ->  instnamer  ->  flatten the DAG to one block  ->  llc

The riscv64 arm is the artefact; the host arm is the same IR lowered for
x86-64 so the two can be executed side by side.  Both arms use `-nostdlibinc`
and the SAME SoftFloat build headers, so uint_fast8/16/32_t have the same
widths in both and the IR is comparable line by line.
"""
import json
import os
import re
import subprocess
import sys

SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad")
REPO = (HOME + "/Programming/PRIVATE/PseudoCoupHQ/Research/oracle/riscv/"
        "softfloat_slices")
sys.path.insert(0, os.path.join(SCRATCH, "lib"))
sys.path.insert(0, os.path.join(SCRATCH, "fl"))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import sfmeasure as M                                          # noqa: E402
import flatten_dag as F                                        # noqa: E402
from localise import localise                                  # noqa: E402

HOME = os.path.expanduser("~")   # no machine path is written into this file

SF = (HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/"
      "berkeley-softfloat-3")
B = "/usr/lib/llvm-21/bin"
ROOT = os.path.join(SCRATCH, "fl")

DEFINES = ["-DSOFTFLOAT_FAST_INT64", "-DSOFTFLOAT_ROUND_ODD",
           "-DINLINE_LEVEL=5", "-DSOFTFLOAT_FAST_DIV32TO16",
           "-DSOFTFLOAT_FAST_DIV64TO32"]
INCLUDES = ["-I" + SF + "/build/Linux-RISCV64-GCC", "-I" + SF + "/source/RISCV",
            "-I" + SF + "/source/include", "-idirafter", SCRATCH + "/shim"]
COMMON = ["-nostdlibinc", "-ffreestanding", "-Oz",
          "-Werror-implicit-function-declaration"]
TARGETS = {
    "rv": ["--target=riscv64-unknown-elf", "-march=rv64im", "-mabi=lp64"],
    "host": ["--target=x86_64-unknown-elf"],
}
PASSES = ("internalize,globalopt,ipsccp,always-inline,inline,globaldce,"
          "instcombine,simplifycfg,dce,globalopt,globaldce")


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, p.stdout, (p.stderr or "").strip()


# ---------------------------------------------------------------- sources ---
def pinned_state(mode, outdir):
    p = os.path.join(outdir, "softfloat_state_rm%d.c" % mode)
    if not os.path.exists(p):
        src = open(os.path.join(SF, "source", "softfloat_state.c")).read()
        new, n = re.subn(
            r"softfloat_roundingMode\s*=\s*softfloat_round_near_even\s*;",
            "softfloat_roundingMode = %d;" % mode, src)
        assert n == 1, "could not pin roundingMode"
        atomic_write(p, new)
    return p


def atomic_write(path, text):
    tmp = "%s.%d.tmp" % (path, os.getpid())
    open(tmp, "w").write(text)
    os.replace(tmp, path)


PROTOS = json.load(open(os.path.join(ROOT, "protos.json"))) \
    if os.path.exists(os.path.join(ROOT, "protos.json")) else None


def takes_mode_parameter(op):
    ra = PROTOS.get(op)
    return bool(ra and any("uint_fast8_t" in a for a in ra[1]))


def wrapper_source(op, mode, variant, outdir):
    """The public entry.  The rounding mode arrives exactly as the emulator
    sends it - the global is pinned by the linked state file, and for the
    twelve float-to-integer conversions plus roundToInt it is ALSO a literal
    argument; `exact` is pinned true for the conversions, as
    c_emulator/riscv_softfloat.cpp does.

    variant `value` returns the operation's own result; variant `flags`
    returns { flags, value }, which is the shape of Sail's own declaration
    (bits_fflags, bits_D) - the flags RETURNED, not stored."""
    ret, args = PROTOS[op]
    name = "%s_rm%d_%s" % (op, mode, variant)
    is_rti = op.endswith("roundToInt")
    params, actuals, n = [], [], 0
    for a in args:
        if a == "uint_fast8_t":
            actuals.append(str(mode))
            continue
        if a == "bool" and not is_rti and takes_mode_parameter(op):
            actuals.append("true")
            continue
        params.append("%s a%d" % (a, n))
        actuals.append("a%d" % n)
        n += 1
    sig = ", ".join(params) if params else "void"
    if variant == "value":
        body = ("%s %s( %s )\n{\n    return %s( %s );\n}\n"
                % (ret, name, sig, op, ", ".join(actuals)))
    else:
        body = ("typedef struct { uint8_t flags; %s v; } %s_res;\n"
                "%s_res %s( %s )\n{\n"
                "    softfloat_exceptionFlags = 0;\n"
                "    %s r = %s( %s );\n"
                "    %s_res out;\n    out.flags = softfloat_exceptionFlags;\n"
                "    out.v = r;\n    return out;\n}\n"
                % (ret, name, name, name, sig, ret, op,
                   ", ".join(actuals), name))
    txt = ('#include <stdint.h>\n#include <stdbool.h>\n'
           '#include "platform.h"\n#include "softfloat_types.h"\n'
           '#include "softfloat.h"\n' + body)
    p = os.path.join(outdir, name + ".c")
    atomic_write(p, txt)
    return p, name


# --------------------------------------------------------------- compiling --
def compile_bc(cfile, tgt, bcdir):
    base = os.path.basename(cfile)[:-2]
    tag = ("RISCV_" + base) if "/RISCV/" in cfile else base
    out = os.path.join(bcdir, tag + "." + tgt + ".bc")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(cfile):
        return out
    tmp = "%s.%d.tmp" % (out, os.getpid())
    rc, _, err = run(["clang"] + TARGETS[tgt] + COMMON + DEFINES + INCLUDES
                     + ["-emit-llvm", "-c", cfile, "-o", tmp])
    if rc:
        raise RuntimeError("compile %s (%s): %s" % (cfile, tgt, err[:400]))
    os.replace(tmp, out)
    return out


def build(op, mode, variant, tgt, files, wdir, gendir, bcdir):
    """-> dict of stage artefacts and counts."""
    wrap, entry = wrapper_source(op, mode, variant, gendir)
    srcs = [wrap, pinned_state(mode, gendir)] + \
           [f for f in files if os.path.basename(f) != "softfloat_state.c"]
    bcs = [compile_bc(f, tgt, bcdir) for f in srcs]

    pfx = os.path.join(wdir, "%s.rm%d.%s.%s" % (op, mode, variant, tgt))
    linked, sbc = pfx + ".linked.bc", pfx + ".sliced.bc"
    rc, _, err = run([B + "/llvm-link"] + bcs + ["-o", linked])
    if rc:
        raise RuntimeError("llvm-link: " + err[:300])
    # Everything but the entry is marked alwaysinline.  At -Oz the inliner
    # leaves softfloat_roundPackToF<n> out of line for the six add/sub
    # operations, and one call is one call too many: a slice with a call is
    # not a single block of arithmetic, and the flag global could not be
    # localised while a second function still reads it.
    _, nmout, _ = run([B + "/llvm-nm", "--defined-only", linked])
    others = sorted({l.split()[-1] for l in nmout.splitlines()
                     if len(l.split()) >= 2 and l.split()[-2] in "TtWwDdBbRrVv"}
                    - {entry})
    passes = PASSES.replace("internalize,", "internalize,forceattrs,")
    cmd = [B + "/opt", "-passes=" + passes,
           "-internalize-public-api-list=" + entry] \
        + ["-force-attribute=%s:alwaysinline" % s for s in others] \
        + [linked, "-o", sbc]
    rc, _, err = run(cmd)
    if rc and "did not reach a fixpoint" in err:
        passes = passes.replace("instcombine,",
                                "instcombine<no-verify-fixpoint>,")
        cmd[1] = "-passes=" + passes
        rc, _, err = run(cmd)
    if rc:
        raise RuntimeError("opt slice: " + err[:300])
    sliced = pfx + ".sliced.ll"
    rc, _, err = run([B + "/llvm-dis", sbc, "-o", sliced])
    if rc:
        raise RuntimeError("llvm-dis: " + err[:300])

    # ---- localise the state globals, then let sroa erase the memory ----
    try:
        loc_text, done = localise(open(sliced).read())
    except SystemExit as ex:
        return {"entry": entry, "sliced_ll": sliced,
                "refused": "localise: %s" % ex}
    loc = pfx + ".loc.ll"
    atomic_write(loc, loc_text)
    clean = pfx + ".clean.ll"
    rc, _, err = run([B + "/opt", "-passes=function(sroa,instcombine,simplifycfg)",
                      "-S", loc, "-o", clean])
    if rc and "fixpoint" in err:
        rc, _, err = run([B + "/opt",
                          "-passes=function(sroa,instcombine<no-verify-fixpoint>,"
                          "simplifycfg)", "-S", loc, "-o", clean])
    if rc:
        raise RuntimeError("opt clean: " + err[:300])
    named = pfx + ".named.ll"
    rc, _, err = run([B + "/opt", "-passes=function(instnamer)", "-S",
                      clean, "-o", named])
    if rc:
        raise RuntimeError("opt instnamer: " + err[:300])

    # ---- flatten ----
    flat = pfx + ".flat.ll"
    res = {"entry": entry, "sliced_ll": sliced, "clean_ll": clean,
           "flat_ll": flat, "localised": [d[0] for d in done],
           "passes": passes}
    try:
        text, em = F.flatten(open(named).read(), new_name=entry + "_flat")
    except F.Refuse as ex:
        res["refused"] = str(ex)
        return res
    atomic_write(flat, text)
    rc, _, err = run([B + "/opt", "-passes=verify", "-S", flat, "-o", "/dev/null"])
    if rc:
        res["refused"] = "flattened IR fails the verifier: " + err[:300]
        return res
    # Only passes that cannot invent control flow.  early-cse shares the
    # duplicates flattening creates; instsimplify replaces, never builds.
    # instcombine is NOT here: it would turn the masks straight back into
    # selects and the backend would put the branches back.
    rc, _, err = run([B + "/opt",
                      "-passes=function(early-cse,instsimplify,dce),globaldce",
                      "-S", flat, "-o", flat + ".tmp"])
    if rc == 0:
        chk, _, _ = run([B + "/opt", "-passes=verify", "-S", flat + ".tmp",
                         "-o", "/dev/null"])
        if chk == 0:
            os.replace(flat + ".tmp", flat)
    res["guarded"] = em.guarded
    res["tables_lowered"] = em.tables
    res["blocks_after"] = count_blocks(flat)
    res["ir_instructions"] = len([l for l in open(flat)
                                  if l.startswith("  ")])
    return res


def lower_and_measure(llfile, entry, objfile, tgt):
    if tgt == "rv":
        # Without the last flag the backend parks a wide literal in .rodata and
        # loads it, which would put memory back into a function that has none:
        # the packed seed-table words are exactly such literals.
        cmd = [B + "/llc", "-march=riscv64", "-mattr=+m", "-O2",
               "--riscv-disable-using-constant-pool-for-large-ints",
               "-filetype=obj", llfile, "-o", objfile]
    else:
        cmd = ["clang", "--target=x86_64-unknown-elf", "-O2", "-c",
               llfile, "-o", objfile]
    rc, _, err = run(cmd)
    if rc:
        raise RuntimeError("llc: " + err[:300])
    dis = M.disasm(objfile)
    r, _ = M.measure(objfile, entry, dis)
    if r is None:
        raise RuntimeError("entry %s absent from %s" % (entry, objfile))
    return r, dis


def count_blocks(llfile):
    n, indef = 0, False
    for l in open(llfile):
        if l.startswith("define "):
            indef, n = True, n + 1
            continue
        if indef and l.rstrip() == "}":
            indef = False
        elif indef and re.match(r"^[-a-zA-Z$._0-9]+:", l):
            n += 1
    return n
