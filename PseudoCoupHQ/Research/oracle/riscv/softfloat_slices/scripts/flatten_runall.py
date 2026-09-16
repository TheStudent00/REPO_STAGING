#!/usr/bin/env python3
"""Every (operation, rounding mode, variant): flatten for riscv64, flatten for
the host, and run the two side by side on the same inputs."""
import json
import os
import re
import subprocess
import sys
import traceback
from multiprocessing import Pool

ROOT = ("/tmp/claude-1000/-home-<user>-Programming/"
        "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/fl")
OUT = (HOME + "/Programming/PRIVATE/PseudoCoupHQ/Research/oracle/riscv/"
       "softfloat_slices/flattened")
sys.path.insert(0, ROOT)
import pipe as P                                                # noqa: E402
import verify as V                                              # noqa: E402

HOME = os.path.expanduser("~")   # no machine path is written into this file

CL = json.load(open(os.path.join(ROOT, "closures.json")))
PROTOS = json.load(open(os.path.join(ROOT, "protos.json")))
P.PROTOS = PROTOS
MODES = [0, 1, 2, 3, 4]
VARIANTS = ["value", "flags"]
N_RAND = int(os.environ.get("NRAND", 200000))
N_STRUCT = int(os.environ.get("NSTRUCT", 100000))
WORK = os.path.join(ROOT, "run")
B = P.B


def data_memory(dis, fn):
    """Memory instructions that are NOT stack traffic.  Everything the
    flattened code touches should be sp-relative save/restore and spill."""
    import sfmeasure as M
    cur, spill, data = None, 0, 0
    for line in dis.splitlines():
        h = M.HDR_RE.match(line.strip())
        if h:
            cur = h.group(2)
            continue
        if cur != fn:
            continue
        m = M.INSN_RE.match(line)
        if not m:
            continue
        if m.group(2) in M.MEM:
            if "(sp)" in m.group(3) or "(s0)" in m.group(3):
                spill += 1
            else:
                data += 1
    return spill, data


def body_of(llfile):
    keep, out = False, []
    for l in open(llfile):
        if l.startswith("define "):
            keep = True
        if keep:
            out.append(l.rstrip())
        if keep and l.rstrip() == "}":
            break
    return "\n".join(out)


def one(job):
    op, mode, variant = job
    tag = "%s.rm%d.%s" % (op, mode, variant)
    rec = {"operation": op, "mode": mode, "variant": variant, "tag": tag}
    wdir = os.path.join(WORK, tag)
    os.makedirs(wdir, exist_ok=True)
    gen, bc = os.path.join(ROOT, "gen"), os.path.join(ROOT, "bc")
    try:
        rv = P.build(op, mode, variant, "rv", CL["closures"][op], wdir, gen, bc)
        rec["entry"] = rv["entry"]
        if "refused" in rv:
            rec["refused"] = rv["refused"]
            return rec
        base, bdis = P.lower_and_measure(rv["sliced_ll"], rv["entry"],
                                         wdir + "/sliced.o", "rv")
        flt, fdis = P.lower_and_measure(rv["flat_ll"], rv["entry"] + "_flat",
                                        wdir + "/flat.o", "rv")
        spill, data = data_memory(fdis, rv["entry"] + "_flat")
        bspill, bdata = data_memory(bdis, rv["entry"])
        rec.update({
            "sliced_instructions": base["instructions"],
            "sliced_branches": base["branches"] + base["jumps"],
            "sliced_memory": base["memory"],
            "sliced_memory_data": bdata,
            "sliced_blocks": P.count_blocks(rv["sliced_ll"]),
            "instructions": flt["instructions"],
            "branches": flt["branches"],
            "jumps": flt["jumps"],
            "calls": flt["calls"],
            "memory": flt["memory"],
            "memory_stack_spill": spill,
            "memory_data": data,
            "blocks": rv["blocks_after"],
            "ir_instructions": rv["ir_instructions"],
            "size_bytes": flt["size_bytes"],
            "guarded": rv["guarded"],
            "tables_lowered": rv["tables_lowered"],
            "localised_globals": rv["localised"],
        })
        # ---- artefacts ----
        os.makedirs(OUT, exist_ok=True)
        import shutil
        shutil.copy(rv["flat_ll"], os.path.join(OUT, tag + ".flat.ll"))
        shutil.copy(wdir + "/flat.o", os.path.join(OUT, tag + ".flat.o"))
        with open(os.path.join(OUT, tag + ".flat.dis"), "w") as fh:
            fh.write("# %s  rounding mode %d  variant %s\n"
                     "# entry symbol: %s\n"
                     "# one basic block: %d instructions, %d branches, "
                     "%d jumps, %d calls,\n"
                     "# %d memory (%d stack spill / restore, %d data)\n"
                     "# llc -march=riscv64 -mattr=+m -O2\n\n"
                     % (op, mode, variant, rv["entry"] + "_flat",
                        flt["instructions"], flt["branches"], flt["jumps"],
                        flt["calls"], flt["memory"], spill, data))
            fh.write(fdis)

        # ---- host arm ----
        hs = P.build(op, mode, variant, "host", CL["closures"][op],
                     wdir, gen, bc)
        if "refused" in hs:
            rec["host_refused"] = hs["refused"]
            return rec
        rec["ir_identical_host_vs_riscv"] = \
            body_of(rv["flat_ll"]) == body_of(hs["flat_ll"])

        # ---- differential test ----
        ret, params = V.wrapper_params(op, PROTOS)
        drv = V.gen_driver(op, rv["entry"], params, ret, variant,
                           N_RAND, N_STRUCT)
        dpath = wdir + "/driver.c"
        open(dpath, "w").write(drv)
        objs = []
        for src, o in ((hs["sliced_ll"], wdir + "/h_orig.o"),
                       (hs["flat_ll"], wdir + "/h_flat.o")):
            rc, _, err = P.run(["clang", "-O2", "-c", src, "-o", o])
            if rc:
                rec["verify_error"] = "host compile: " + err[:300]
                return rec
            objs.append(o)
        rc, _, err = P.run(["clang", "-O2", "-o", wdir + "/test", dpath] + objs)
        if rc:
            rec["verify_error"] = "driver link: " + err[:400]
            return rec
        p = subprocess.run([wdir + "/test"], capture_output=True, text=True,
                           timeout=1800)
        m = re.search(r"TESTED (\d+) MISMATCHES (\d+)", p.stdout)
        if not m:
            rec["verify_error"] = "no verdict: " + (p.stdout + p.stderr)[:400]
            return rec
        rec["inputs_tested"] = int(m.group(1))
        rec["mismatches"] = int(m.group(2))
        if rec["mismatches"]:
            rec["mismatch_examples"] = [l for l in p.stdout.splitlines()
                                        if l.startswith("MISMATCH")][:8]
        for f in ("linked.bc", "sliced.bc"):
            for t in ("rv", "host"):
                pth = os.path.join(wdir, "%s.%s.%s" % (tag, t, f))
                if os.path.exists(pth):
                    os.unlink(pth)
    except Exception:                                           # noqa: BLE001
        rec["error"] = traceback.format_exc()[-600:]
    return rec


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    jobs = [(op, m, v) for op in CL["ops"] for m in MODES for v in VARIANTS]
    if len(sys.argv) > 1:
        jobs = [j for j in jobs if j[0] in sys.argv[1:]]
    results = []
    with Pool(int(os.environ.get("JOBS", 8))) as pool:
        for r in pool.imap_unordered(one, jobs):
            results.append(r)
            flag = ("ERROR" if "error" in r else
                    "REFUSED" if "refused" in r else
                    "VERIFY-ERR" if "verify_error" in r else
                    "MISMATCH" if r.get("mismatches") else "ok")
            print("%-28s %-10s insns %5s br %-3s mem %-4s tested %-9s"
                  % (r["tag"], flag, r.get("instructions", "-"),
                     r.get("branches", "-"), r.get("memory_data", "-"),
                     r.get("inputs_tested", "-")), flush=True)
            if flag in ("ERROR", "VERIFY-ERR"):
                print("    " + str(r.get("error") or r.get("verify_error"))[:400],
                      flush=True)
    json.dump(results, open(os.path.join(ROOT, "results.json"), "w"), indent=1)
    print("%d jobs" % len(results))
