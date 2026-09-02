#!/usr/bin/env python3
"""l3_swiftexec.py -- log 034 JOB A, second half: re-execute swift's
accepted set, where "accepted" now means what the REAL compiler
accepted.

`l3_exec_lanes.emit` already takes a rows override, so this file is the
one line that matters: the accepted set comes from
`swiftfull_accepts.json` (written by `l3_swiftfull_read.py` off the
full-`swiftc` matrix) instead of from `raw/vm_swift_*.txt` (the
`-typecheck` matrix).

THE CHECK THIS RUN CARRIES.  The exec driver has a repair loop for a
compiler that refuses a chunk: it maps the error line back through the
`// __PROBE__` markers, drops those probes as CODEGEN_REFUSE and
rebuilds.  Under the old accepted set that loop fired 1,066 times for
swift and never for anything else.  Under the new one it should fire
ZERO times, because the accepted set was itself taken with the compiler
that would do the refusing.  **A non-zero codegen-refuse count here
means the matrix redo did not do its job**, and that is a stronger
check on the redo than any count the redo prints about itself.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import l3_exec as E
import l3_exec_lanes as L


def main():
    p = os.path.join(HERE, "swiftfull_accepts.json")
    ids = json.load(open(p))
    rows = sorted(tuple(int(z) for z in s[1:].split("_")) for s in ids)
    old = len(E.accepted("swift"))
    nch = (len(rows) + E.CHUNK["swift"] - 1) // E.CHUNK["swift"]
    print("| set | probes | chunks |")
    print("|---|---|---|")
    print("| -typecheck accepts (superseded) | %d | %d |"
          % (old, (old + E.CHUNK["swift"] - 1) // E.CHUNK["swift"]))
    print("| full swiftc accepts | %d | %d |" % (len(rows), nch))
    L.emit("swift", 0, nch, name="xr_swift_00", rows=rows)
    json.dump(dict(language="swift", lane="xr_swift_00",
                   probes=len(rows), chunks=nch,
                   accepted_from="swiftfull_accepts.json",
                   superseded_probes=old,
                   expect_codegen_refuse=0),
              open(os.path.join(HERE, "swiftexec_plan.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
