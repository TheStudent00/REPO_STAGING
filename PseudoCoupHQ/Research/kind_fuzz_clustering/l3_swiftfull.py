#!/usr/bin/env python3
"""l3_swiftfull.py -- log 034 JOB A: swift's acceptance matrix retaken
with the REAL compiler.

Log 032 measured that `swiftc -typecheck` ACCEPTS 1,066 of the 2,618
probes that full `swiftc` then refuses -- 40.7 percent -- almost all of
them overflowing integer literals, which swift diagnoses in SILGen and
not in the type checker.  Every swift verdict in the node was taken
with `-typecheck`, so every swift verdict is suspect.

This file re-emits swift's FULL value matrix -- the same 76,614 probes,
the same rows, the same sources, byte for byte -- with the verdict
instrument changed from `swiftc -typecheck` to `swiftc -c`, which runs
SILGen and IRGen and is the instrument the execution pass used.

MEASURED 2026-08-19 in the container: `swiftc -typecheck` 154 ms/probe,
`swiftc -c` 155 ms/probe, effective 34 ms/probe at -P 8 on 6 cores.
Full compilation is therefore NOT more expensive than type checking
here, and the whole matrix is retaken rather than only its accepts.
That matters: an accepts-only redo would have rested on the assumption
that full swiftc refuses everything -typecheck refuses, which is
plausible and was never measured.

Lanes are named vs_swift_NN so they cannot collide with the superseded
vm_swift_NN products.
"""
import io, gzip, base64, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import l3_matrix as M

OLD = '"swift": lambda f: ["/persist/swift/usr/bin/swiftc", "-typecheck", f],'
NEW = ('"swift": lambda f: ["/persist/swift/usr/bin/swiftc", "-c", f,\n'
       '                          "-o", f + ".o"],')

MS_FULL = 34.0          # measured, -P 8, 6 cores
SHARD_SECONDS = 1500.0  # 25 min against the daemon's 3600 s kill


def main():
    hs, ops_, tpl, rows = M.matrix("swift")
    tbl = M.table("swift", hs, ops_, tpl)
    secs = len(rows) * MS_FULL / 1000.0
    n = max(2, int(secs / SHARD_SECONDS) + (1 if secs % SHARD_SECONDS else 0))
    per = (len(rows) + n - 1) // n
    print("| language | holders | ops | probes | ms/probe | projected | "
          "shards |")
    print("|---|---|---|---|---|---|---|")
    print("| swift | %d | %d | %d | %.1f | %.1f min | %d |"
          % (len(hs), len(ops_), len(rows), MS_FULL, secs / 60.0, n))
    import tempfile
    tmp = tempfile.mkdtemp(prefix="swiftfull_")
    real, M.LANES = M.LANES, tmp
    names = []
    for s in range(n):
        chunk = rows[s * per:(s + 1) * per]
        if not chunk:
            continue
        name, p = M.emit("swift", s, n, chunk, tbl, len(rows))
        # rename vm_ -> vs_ and swap the verdict instrument
        txt = open(p).read()
        assert OLD in txt, "swift command line moved"
        txt = txt.replace(OLD, NEW)
        txt = txt.replace("/work/vm_swift", "/work/vs_swift")
        txt = txt.replace("/out/vm_swift", "/out/vs_swift")
        txt = txt.replace("A2 swiftc -typecheck", "A2r swiftc -c (FULL)")
        txt = txt.replace("value matrix, route A",
                          "value matrix REDO, route A2r full swiftc")
        np = os.path.join(real, name.replace("vm_", "vs_") + ".sh")
        open(np, "w").write(txt)
        os.chmod(np, 0o755)
        names.append(name.replace("vm_", "vs_"))
        print("  emitted %s  (%d probes)" % (names[-1], len(chunk)))
    M.LANES = real
    import shutil; shutil.rmtree(tmp, ignore_errors=True)
    json.dump(dict(language="swift", instrument="swiftc -c",
                   superseded="valuematrix_swift.json (swiftc -typecheck)",
                   probes=len(rows), shards=len(names), lanes=names,
                   ms_per_probe_measured=MS_FULL, projected_seconds=secs),
              open(os.path.join(HERE, "swiftfull_plan.json"), "w"), indent=1)
    print("\nprojected TOTAL %.1f min (derived from a measured per-probe "
          "cost)" % (secs / 60.0))


if __name__ == "__main__":
    main()
