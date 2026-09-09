#!/usr/bin/env bash
# ap4_l6_probe_the_x87_answer_and_its_arrivals.sh -- task ap4: what the
# body's answer term holds once the driver reads it off the x87 stack,
# and what its ARRIVALS are spelled as.
#
# For every distinct x87 c body task ap3's store carries: the cell, its
# own arrivals, the carved body, the wrapped text, the answer term the
# driver now reads, and every free symbol of that term with its sort --
# which is what an x87 IN row would have to be aligned on.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import reference as R
import canonical_form as CF
import autopoly3 as A

A.use_task_ap3()
runs = A.read_runs(A.RUNS)
shared = H.build_shared()

seen = set()
count = 0
for run in runs:
    if run["lang"] != "c":
        continue
    for place in (run.get("places") or []):
        home = (place.get("home") or {}).get("family")
        if not E.is_an_x87_arrival(home):
            continue
        if not place.get("compiled"):
            continue
        body = place.get("body_text")
        if body in seen:
            continue
        seen.add(body)
        count = count + 1
        print("")
        print("== [%d] `%s` %s %s -> c, place `%s`"
              % (count, run["mnem"], run["shape"], run["key_width"],
                 place["writes"]))
        print("   the cell's arrivals: %s" % place.get("families"))
        print("   the cell's term, LITERAL: %s"
              % (place.get("text") or "")[:300])
        print("   the parameter plan: %s"
              % [(p.get("name"), p.get("holder"), p.get("family"),
                  p.get("kind"), p.get("bits"))
                 for p in (place.get("params") or [])])
        print("   the carved body, LITERAL: %s" % body)
        recorded = E.recorded_facts("c/probe%d" % count, "probe%d" % count,
                                    place["body_bytes"].split(),
                                    body.split("; "))
        canon = CF.render_one(shared["form"], shared["gate"], recorded)
        print("   canonical_form outcome: %r" % canon.get("outcome"))
        print("   the wrapped text resolved, LITERAL: %s"
              % canon.get("wrapped_text_resolved"))
        term, cause = E.body_answer(shared["reference"], canon)
        if term is None:
            print("   the body's answer: REFUSED -- %s" % cause)
            continue
        print("   the body's answer, LITERAL: %s"
              % H.T.one_line(term)[:400])
        print("   its sort: %s  its size: %s"
              % (term.sort(),
                 term.size() if z3.is_bv(term) else "not a bitvector"))
        print("   its free symbols:")
        for symbol in z3.z3util.get_vars(term):
            print("      %-28s sort %s" % (symbol.decl().name(),
                                           symbol.sort()))
print("")
print("distinct x87 c bodies: %d" % count)
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "done"
