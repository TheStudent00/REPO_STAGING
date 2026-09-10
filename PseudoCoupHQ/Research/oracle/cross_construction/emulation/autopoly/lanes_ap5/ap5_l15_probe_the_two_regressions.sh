#!/usr/bin/env bash
# ap5_l15_probe_the_two_regressions.sh -- task ap5: the loop's own
# measurement found 31 runs task ap4 proved that the first pass of
# this loop did not, which is the brief's STOP condition.  This lane
# asks both populations before anything is re-run.
#
#  [1] THE THIRTY: `mem_one` 80 cells on c.  The counterexamples name
#      `seed_x87__rsi_` as a free symbol beside `IN_0` and `IN_1`, so
#      the cell's SECOND arrival was not put on a row.  An x87 arrival
#      reaches a row under two names -- `X87_<k>`, a stack position
#      the model table preseeded, and `x87_<mangled operand>`, a
#      literal memory operand read at the x87 sort -- and
#      `emulate.X87_ARRIVAL` holds both; the first draft of
#      `align_by_row`'s new branch tested only the first.  The branch
#      now tests both, and this section runs four of the thirty to see
#      whether that is the whole of it.
#  [2] THE ONE: `sbb` imm_gpr 8 on swift, whose cause is `this unit
#      record carries no body`.  The carved body is printed LITERAL
#      beside the source, and beside the same cell on c, so what swift
#      did with the rendered text is read rather than guessed.
#
# Nothing here is written to `autopoly5_runs.jsonl`.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
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
import pool100_entry_equivalence as P100
import model_table as MTAB
import gate as G
import autopoly5 as A

ABORT_KB = 6 * 1024 * 1024


def guard(where):
    got = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


A.use_task_ap5()
MTAB._install_gpr_widths()
print("emulate.X87_ARRIVAL, LITERAL: %s" % (E.X87_ARRIVAL,))
print("align_by_row over the two spellings:")
for family in ["X87_0", "x87__rsi_"]:
    term = z3.fpToIEEEBV(z3.Const("seed_%s" % family, R.X87_SORT))
    rows = P100.input_rows([family])
    print("   %-12s %s   ->   %s"
          % (family, term, P100.align_by_row(term, rows)))
guard("the two spellings")

if not os.path.isdir(A.SRC_DIR):
    os.makedirs(A.SRC_DIR)
cells = A.read_json(A.CELLS)
shared = H.build_shared()
reposer = G.Gate(reference=shared["reference"],
                 solver_timeout_ms=A.REPOSE_MS)
in_table = H.load_in_table()
guard("the driver's own reads")


def one(asked, lang):
    ledger = 0
    for record in cells["asked"]:
        key = (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"])
        if key == asked:
            ledger = record["attested_ledger_rows"]
    run = A.one_run(shared, reposer, cells, asked, lang, ledger,
                    in_table)
    print("   == `%s` %s %s -> %s" % (asked[0], asked[1], asked[2],
                                      lang))
    print("      route: %s   line: %r" % (run.get("route"),
                                          run.get("line")))
    if run.get("refusal_cause") is not None:
        print("      REFUSED: %s: %s"
              % (run["refusal_cause"], run.get("refusal_detail")))
        return run
    for place in run.get("places") or []:
        check = place.get("check") or {}
        print("      place %-14s rendered %s  outcome %s"
              % (place.get("writes"), place.get("rendered", True),
                 check.get("outcome")))
        if place.get("rendered") is False:
            print("         refusal: %s -- %s"
                  % (place.get("refusal_cause"),
                     place.get("refusal_detail")))
            continue
        if place.get("families") is not None:
            print("         the cell's families: %s" % place["families"])
        if place.get("params") is not None:
            print("         the parameter plan: %s"
                  % [(p.get("name"), p.get("holder"), p.get("family"),
                      p.get("bits")) for p in place["params"]])
        if place.get("mnem") is not None:
            print("         the carved body, LITERAL: %s"
                  % "; ".join(place["mnem"]))
        else:
            print("         the carved body: none")
        if place.get("compile_refusal") is not None:
            print("         the compiler: %s"
                  % A.first_line(place["compile_refusal"]))
        for name in ["aligned_rows", "reason", "counterexample"]:
            if check.get(name) is not None:
                print("         %s: %s" % (name, check[name]))
    print("      the run's verdict: %s" % A.outcome_of(run))
    return run


print("")
print("[1/2] FOUR OF THE THIRTY, with the branch testing both spellings")
for asked in [("faddl", "mem_one", 80), ("fldt", "mem_one", 80),
              ("fildl", "mem_one", 80), ("fsubrl", "mem_one", 80)]:
    one(asked, "c")
guard("section 1")

print("")
print("[2/2] `sbb` imm_gpr 8, on swift and on c")
for lang in ["swift", "c"]:
    run = one(("sbb", "imm_gpr", 8), lang)
    for place in run.get("places") or []:
        if place.get("source"):
            print("      the rendered source on %s, LITERAL:" % lang)
            for line in place["source"].split("\n"):
                print("         %s" % line)
            break
guard("section 2")
print("done")
PY
