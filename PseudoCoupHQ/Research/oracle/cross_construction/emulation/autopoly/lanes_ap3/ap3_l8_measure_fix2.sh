#!/usr/bin/env bash
# ap3_l8_measure_fix2.sh -- task ap3: FIX 2, MEASURED ON THE 128 PAIRS
# IT TARGETS, before the loop.
#
# `autopoly3.py measure <a substring of the cause>` reads task ap2's own
# store, takes exactly the (cell, target) pairs whose cause holds that
# substring, runs each again through the driver as this task leaves it,
# and prints the cause before and after.  It writes nothing to the
# loop's store.
#
# The 128 pairs are the 32 x87 cells at `key_width` 80 on the four
# targets, which task ap2 recorded as `no setter row to compose the flag
# pair from: None at width 8` -- a cause lane `ap3_l2` measured to be
# wrong in the objects: 0 of the 32 rows reads the arriving flag state.
#
# WHAT THIS MEASUREMENT CAN AND CANNOT SHOW.  c is the only target of
# the four with an 80-bit holder, so at most a quarter of these pairs
# can render at all; rust, go and swift refuse BY NATURE and that
# refusal is the fix's own answer for them, not a defect.  Whether a
# rendered c row then PROVES is a separate question and the arrival
# contract is expected to stop it -- said here before the numbers, so
# the numbers are not read as a disappointment.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly3.py measure 'no setter row to compose'
echo ""
echo "the c rows in full: the rendered source and the carved body of one"
python3 - <<'PY'
import os
import sys

HERE = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly3 as A
import handful as H
import gate as G
import model_table as MTAB

A.use_task_ap3()
cells = A.read_json(A.CELLS)
shared = H.build_shared()
reposer = G.Gate(reference=shared["reference"],
                 solver_timeout_ms=A.REPOSE_MS)
MTAB._install_gpr_widths()
in_table = H.load_in_table()
for asked in (("faddl", "mem_one", 80), ("fdivp", "st_st", 80)):
    for lang in ("c", "rust"):
        record = A.one_run(shared, reposer, cells, asked, lang, 0,
                           in_table)
        print("")
        print("== %s %s %s -> %s" % (asked + (lang,)))
        for place in record.get("places") or []:
            print("   place `%s`, %s bits, home %s, families %s"
                  % (place["writes"], place["bits"],
                     (place.get("home") or {}).get("family"),
                     place.get("families")))
            print("   rendered: %s" % place.get("rendered"))
            if not place.get("rendered"):
                print("   refusal: %s: %s"
                      % (place.get("refusal_cause"),
                         place.get("refusal_detail")))
                continue
            print("   THE RENDERED SOURCE, LITERAL:")
            for line in place["source"].rstrip("\n").split("\n"):
                print("      %s" % line)
            print("   compiled: %s" % place.get("compiled"))
            print("   the carved body, LITERAL: %s"
                  % place.get("body_text"))
            print("   landing: %s"
                  % (place.get("landing") or {}).get("verdict"))
            check = place.get("check") or {}
            print("   the gate: %s -- %s"
                  % (check.get("outcome"), check.get("reason")))
PY
echo "done"
