#!/usr/bin/env bash
# ap4_l5_probe_change2_end_to_end.sh -- task ap4: CHANGE 2 asked of the
# objects, end to end, before anything is measured at scale.
#
#  [1] THE WRAP: one x87 c body put on the canonical form with the
#      ledger's new x87 epilogue -- the wrapped text LITERAL, the OUT
#      row, and whether the form still refuses.
#  [2] THE TWO ROUTES the driver's check tries for a body's answer: the
#      reference simulator's `answer_for_unit`, and the transcribed
#      term.  Whichever answers, its term LITERAL.
#  [3] THE PRELUDE: `ledger.wrap_unit` handed an x87 ARRIVAL, so the
#      new prelude branch is exercised and its lines are LITERAL.
#  [4] THE GUARD THE CHANGE MUST NOT MOVE: the same wrap over a plain
#      general body and a vector body, before and after, compared text
#      for text against what the unchanged branch gives.
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
import ledger as L
import canonical_form as CF
import autopoly3 as A

ABORT_KB = 6 * 1024 * 1024

A.use_task_ap3()
runs = A.read_runs(A.RUNS)
shared = H.build_shared()

print("[1/4] THE WRAP of an x87 c body, with the ledger's new epilogue")
found = None
for run in runs:
    if run["lang"] != "c":
        continue
    for place in (run.get("places") or []):
        if not E.is_an_x87_arrival((place.get("home") or {}).get("family")):
            continue
        if not place.get("compiled"):
            continue
        found = (run, place)
        break
    if found is not None:
        break
run, place = found
print("   `%s` %s %s -> c, place `%s`"
      % (run["mnem"], run["shape"], run["key_width"], place["writes"]))
print("   the carved body, LITERAL: %s" % place["body_text"])
recorded = E.recorded_facts("c/probe", "probe",
                            place["body_bytes"].split(),
                            place["body_text"].split("; "))
print("   recorded_facts result_family: %r" % recorded.get("result_family"))
print("   recorded_facts result_width:  %r" % recorded.get("result_width"))
print("   recorded_facts arrival_families: %r"
      % recorded.get("arrival_families"))
canon = CF.render_one(shared["form"], shared["gate"], recorded)
print("   canonical_form outcome:       %r" % canon.get("outcome"))
print("   canonical_form refusal_cause: %r" % canon.get("refusal_cause"))
print("   the wrapped text, LITERAL:")
print("      %s" % canon.get("wrapped_text"))
print("   the wrapped text resolved, LITERAL:")
print("      %s" % canon.get("wrapped_text_resolved"))
print("   body_verbatim: %r" % canon.get("body_verbatim"))
print("   out_row: %r" % canon.get("out_row"))
for row in (canon.get("ledger") or []):
    print("      row %-8s %-6s %2d bytes  %s"
          % (row.get("row"), row.get("block"), row.get("size"),
             row.get("type")))

print("")
print("[2/4] THE TWO ROUTES FOR THE BODY'S ANSWER")
term, cause = E.body_answer(shared["reference"], canon)
if term is None:
    print("   answer_for_unit refused: %s" % cause)
else:
    print("   answer_for_unit, LITERAL: %s" % H.T.one_line(term)[:400])
    print("   its sort: %s" % term.sort())
walked = shared["maker"].transcribe(canon)
print("   transcribe refused: %r" % getattr(walked, "refused", None))
if walked.out_term is None:
    print("   the transcribed term: none")
else:
    print("   the transcribed term, LITERAL: %s"
          % H.T.one_line(walked.out_term)[:400])
    print("   its sort: %s" % walked.out_term.sort())

print("")
print("[3/4] THE PRELUDE, handed x87 ARRIVALS")
fields = L.wrap_unit("faddp %st,%st(1); ret", ["X87_0", "X87_1"],
                     "X87_0", 79)
print("   prelude, LITERAL:          %r" % fields["prelude"])
print("   prelude resolved, LITERAL: %r" % fields["prelude_resolved"])
print("   epilogue, LITERAL:         %r" % fields["epilogue"])
print("   epilogue resolved:         %r" % fields["epilogue_resolved"])
print("   the wrapped text, LITERAL: %s" % fields["wrapped_text"])
for row in fields["ledger"]:
    print("      row %-8s %-6s %2d bytes  %s"
          % (row.get("row"), row.get("block"), row.get("size"),
             row.get("type")))

print("")
print("[4/4] THE GUARD: the unchanged branches, text for text")
CASES = [
    ("a general answer", "add %rsi,%rdi; mov %rdi,%rax; ret",
     ["rdi", "rsi"], "rax", 64),
    ("a vector answer", "addsd %xmm1,%xmm0; ret", ["xmm0", "xmm1"],
     "xmm0", 64),
    ("a narrow general answer", "mov %edi,%eax; ret", ["rdi"], "rax",
     32),
]
for name, body, families, home, width in CASES:
    fields = L.wrap_unit(body, families, home, width)
    print("   -- %s" % name)
    print("      prelude resolved:  %r" % fields["prelude_resolved"])
    print("      epilogue resolved: %r" % fields["epilogue_resolved"])
    print("      wrapped text:      %s" % fields["wrapped_text"])
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "done"
