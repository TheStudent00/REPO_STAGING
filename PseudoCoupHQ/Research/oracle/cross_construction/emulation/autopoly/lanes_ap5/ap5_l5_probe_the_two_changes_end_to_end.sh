#!/usr/bin/env bash
# ap5_l5_probe_the_two_changes_end_to_end.sh -- task ap5: the two
# changes asked end to end, on named (cell, target) pairs, BEFORE the
# loop of record is started and without writing one line of its store.
#
#  [1] THE TWO SHARED READINGS, asked directly again now that they are
#      in: `reference.answer_of` on an x87 answer home, and
#      `pool100_entry_equivalence.align_by_row` on an x87 arrival.
#      Both branches LITERAL, and the unchanged branches beside them
#      text for text.
#  [2] THREE x87 c RUNS end to end, each printed with the route, the
#      aligned IN rows, the gate's verdict in z3's own words.
#  [3] THE SIX RUNS task ap4's loop left `sat` at an `imm_*` cell,
#      each run again: the route, the parameter plan (the immediate as
#      one more parameter), and the verdict.
#  [4] THREE imm_* RUNS task ap4 PROVED, run again, so what the change
#      does to a run that was already proved is measured and not
#      assumed.
#
# Nothing here is written to `autopoly5_runs.jsonl`: `one_run` is
# called and its record printed.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import inspect
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

print("[1/4] THE TWO SHARED READINGS, now that they are in")
print("   reference.Reference.answer_of, LITERAL:")
print(inspect.getsource(R.Reference.answer_of))
state = R.MachineState()
state.x87_push(z3.FP("seed_X87_1", R.X87_SORT))
state.x87_push(z3.FP("seed_X87_0", R.X87_SORT))
got = R.REFERENCE.answer_of(state, ("X87_0", E.X87_BITS))
print("   answer_of((X87_0, 79)) gives: %s   sort %s  size %d"
      % (got, got.sort(), got.size()))
got1 = R.REFERENCE.answer_of(state, ("X87_1", E.X87_BITS))
print("   answer_of((X87_1, 79)) gives: %s" % got1)
print("")
print("   THE UNCHANGED BRANCHES, text for text:")
plain = R.MachineState()
print("      a general answer  answer_of(('rax', 32)) = %s"
      % R.REFERENCE.answer_of(plain, ("rax", 32)))
print("      a vector answer   answer_of(('xmm0', 64)) = %s"
      % R.REFERENCE.answer_of(plain, ("xmm0", 64)))
print("")
print("   pool100_entry_equivalence.align_by_row, LITERAL:")
print(inspect.getsource(P100.align_by_row))
term = z3.fpToIEEEBV(z3.FP("seed_X87_0", R.X87_SORT)
                     * z3.FP("seed_X87_1", R.X87_SORT))
rows = P100.input_rows(["X87_0", "X87_1"])
aligned = P100.align_by_row(term, rows)
print("   the x87 term, LITERAL:  %s" % term)
print("   aligned by row:         %s" % aligned)
print("   its free symbols:       %s"
      % [s.decl().name() for s in z3.z3util.get_vars(aligned)])
plain_term = z3.BitVec("seed_rdi", 64) + z3.BitVec("seed_rsi", 64)
plain_rows = P100.input_rows(["rdi", "rsi"])
print("   THE UNCHANGED BRANCH: a general term aligned by row: %s"
      % P100.align_by_row(plain_term, plain_rows))
vector_term = z3.BitVec("seed_xmm0", 128)
print("   THE UNCHANGED BRANCH: a vector term aligned by row: %s"
      % P100.align_by_row(vector_term, P100.input_rows(["xmm0"])))
guard("section 1")

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
    print("      route: %s   chosen_by: %s"
          % (run.get("route"), run.get("chosen_by")))
    print("      line: %r" % run.get("line"))
    if run.get("primitive") is not None:
        print("      primitive: row %s  cause %s"
              % ((run["primitive"].get("row") or {}).get("body_text"),
                 run["primitive"].get("cause")))
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
        if place.get("params") is not None:
            print("         the parameter plan: %s"
                  % [(p.get("name"), p.get("holder"), p.get("family"),
                      p.get("bits")) for p in place["params"]])
        if place.get("source") is not None:
            print("         the rendered source, LITERAL:")
            for line in (place["source"] or "").split("\n"):
                print("            %s" % line)
        if place.get("mnem") is not None:
            print("         the carved body, LITERAL: %s"
                  % "; ".join(place["mnem"]))
        for name in ["region", "aligned_rows", "x87_rows", "reason",
                     "counterexample"]:
            if check.get(name) is not None:
                print("         %s: %s" % (name, check[name]))
    print("      the run's verdict: %s" % A.outcome_of(run))
    return run


print("")
print("[2/4] THREE x87 c RUNS, end to end")
for asked in [("faddp", "st_st", 80), ("fmulp", "st_st", 80),
              ("fdivp", "st_st", 80)]:
    one(asked, "c")
guard("section 2")

print("")
print("[3/4] THE SIX RUNS task ap4 LEFT `sat` AT AN imm_* CELL")
for asked, lang in [(("mov", "imm_gpr", 32), "c"),
                    (("mov", "imm_gpr", 8), "c"),
                    (("xor", "imm_gpr", 8), "c"),
                    (("xor", "imm_gpr", 8), "rust"),
                    (("xor", "imm_gpr", 8), "swift"),
                    (("xor", "imm_gpr", 32), "go")]:
    one(asked, lang)
guard("section 3")

print("")
print("[4/4] THREE imm_* RUNS task ap4 PROVED, run again")
for asked, lang in [(("and", "imm_gpr", 32), "c"),
                    (("cmp", "imm_gpr", 64), "go"),
                    (("movabs", "imm_gpr", 64), "swift")]:
    one(asked, lang)
guard("section 4")
print("done")
PY
