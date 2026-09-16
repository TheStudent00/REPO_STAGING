#!/usr/bin/env python3
"""The strong form of the differential test.

The first pass built a separate host slice, which is NOT the same IR as the
riscv64 one: the two datalayouts declare different native integer widths
(n32:64 against n8:16:32:64) and instcombine narrows differently during
slicing, so only 48 of 670 come out textually identical.

This pass removes that gap.  It takes the EXACT .ll that was handed to llc for
riscv64 - the sliced one and the flattened one - changes nothing in either
body, rewrites only the `target datalayout` and `target triple` lines and
drops the riscv-only target-feature attributes, and runs those two on the
host against each other.  What is executed here is the same instruction
sequence, operand for operand, that the published .o was lowered from.
"""
import json
import os
import re
import subprocess
import sys
import traceback
from multiprocessing import Pool

ROOT = ("/tmp/claude-1000/-home-<user>-Programming/"
        "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/fl")
sys.path.insert(0, ROOT)
import pipe as P                                                # noqa: E402
import verify as V                                              # noqa: E402

PROTOS = json.load(open(os.path.join(ROOT, "protos.json")))
HOST_DL = ("e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-"
           "n8:16:32:64-S128")
HOST_TRIPLE = "x86_64-unknown-linux-gnu"
N_RAND = int(os.environ.get("NRAND", 200000))
N_STRUCT = int(os.environ.get("NSTRUCT", 100000))


def retarget(src, dst):
    out = []
    for l in open(src):
        if l.startswith("target datalayout"):
            l = 'target datalayout = "%s"\n' % HOST_DL
        elif l.startswith("target triple"):
            l = 'target triple = "%s"\n' % HOST_TRIPLE
        elif l.startswith("attributes #"):
            l = re.sub(r'"target-(cpu|features|abi)"="[^"]*"\s*', "", l)
        elif l.startswith("!llvm.module.flags"):
            continue        # target-abi / riscv-isa / SmallDataLimit; optional
        out.append(l)
    open(dst, "w").write("".join(out))


def one(job):
    op, mode, variant = job
    tag = "%s.rm%d.%s" % (op, mode, variant)
    d = os.path.join(ROOT, "run", tag)
    rec = {"tag": tag, "operation": op, "mode": mode, "variant": variant}
    try:
        entry = "%s_rm%d_%s" % (op, mode, variant)
        pairs = []
        for kind, name in (("sliced", "orig"), ("flat", "flat")):
            src = os.path.join(d, "%s.rv.%s.ll" % (tag, kind))
            rt = os.path.join(d, "x_%s.ll" % name)
            retarget(src, rt)
            o = os.path.join(d, "x_%s.o" % name)
            rc, _, err = P.run(["clang", "-O2", "-Wno-override-module",
                                "-c", rt, "-o", o])
            if rc:
                rec["error"] = "%s: %s" % (kind, err[:300])
                return rec
            pairs.append(o)
        ret, params = V.wrapper_params(op, PROTOS)
        drv = os.path.join(d, "driver.c")
        if not os.path.exists(drv):
            open(drv, "w").write(V.gen_driver(op, entry, params, ret, variant,
                                              N_RAND, N_STRUCT))
        exe = os.path.join(d, "x_test")
        rc, _, err = P.run(["clang", "-O2", "-o", exe, drv] + pairs)
        if rc:
            rec["error"] = "link: " + err[:400]
            return rec
        p = subprocess.run([exe], capture_output=True, text=True, timeout=1800)
        m = re.search(r"TESTED (\d+) MISMATCHES (\d+)", p.stdout)
        if not m:
            rec["error"] = "no verdict: " + (p.stdout + p.stderr)[:300]
            return rec
        rec["inputs_tested"] = int(m.group(1))
        rec["mismatches"] = int(m.group(2))
        if rec["mismatches"]:
            rec["examples"] = [l for l in p.stdout.splitlines()
                               if l.startswith("MISMATCH")][:8]
        for f in ("x_orig.o", "x_flat.o", "x_test"):
            q = os.path.join(d, f)
            if os.path.exists(q):
                os.unlink(q)
    except Exception:                                           # noqa: BLE001
        rec["error"] = traceback.format_exc()[-400:]
    return rec


if __name__ == "__main__":
    res = json.load(open(os.path.join(ROOT, "results.json")))
    jobs = [(r["operation"], r["mode"], r["variant"]) for r in res]
    if len(sys.argv) > 1:
        jobs = [j for j in jobs if j[0] in sys.argv[1:]]
    out = []
    with Pool(int(os.environ.get("JOBS", 10))) as pool:
        for r in pool.imap_unordered(one, jobs):
            out.append(r)
            if "error" in r or r.get("mismatches"):
                print("%-28s %s" % (r["tag"],
                                    r.get("error") or
                                    "MISMATCHES %d" % r["mismatches"]),
                      flush=True)
    json.dump(out, open(os.path.join(ROOT, "results_exact.json"), "w"),
              indent=1)
    ok = [r for r in out if "error" not in r]
    print("exact-IR test: %d of %d jobs ran, %d inputs, %d mismatches"
          % (len(ok), len(out), sum(r["inputs_tested"] for r in ok),
             sum(r["mismatches"] for r in ok)))
