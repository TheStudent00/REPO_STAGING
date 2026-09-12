#!/bin/bash
# bb2_l6_the_pass.sh -- task bb2, lane 6: WHERE THE GATE'S TIME GOES,
# named stage by stage, and then THE MEASUREMENT ITSELF -- the
# bit-blast route over every attested x86 cell on all five compiled
# targets, 1,265 (cell, target) runs, one process and no pool.
#
# WHAT LANES 1 TO 5 SETTLED BEFORE THIS ONE RAN.  1,199 written places
# over 253 cells, of which 618 blast (the other 581 are the arrived
# flag state of a preseeded row, a term that is not over bit-vectors,
# or a circuit above 200,000 gates -- lane 1 counts each).  The largest
# circuit is `idiv gpr_one 32` at 74,786 gates; at that size clang
# takes 35 s, rustc 38 s, go 8 s and swiftc does not come back inside
# its own 600-second bound (lane 4).  AND THE GATE IS WHAT RUNS OUT:
# `xor gpr_gpr 8` on c (24 gates, a body the compiler collapsed to six
# instructions) is gated in 0.007 s, and `add gpr_gpr 32` on c (461
# gates, a body the compiler did not collapse) had not come back after
# 1,800 s (lane 5, exit 124).  Step 1 asks WHICH PART of the gate that
# is, each part in a process of its own under a real clock, so the
# cause on the row is the one that was measured.
#
#   [1/4] the gate's stages on one place, each bounded, each timed
#   [2/4] the route on one cell, printed, before the pass
#   [3/4] the pass, repeated until an attempt adds no store line
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
STORE="$HQ/Research/oracle/cross_construction/emulation/autopoly/bb2_bit_blast_runs.jsonl"
total=4

i=1
echo "[$i/$total] where the gate's time goes, stage by stage"
timeout 1200 python3 - <<'PY'
import os, signal, sys, time
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
sys.path.insert(0, G)
import bb2_run as BB2
import bitblast as BB
AP = BB2.configure()
import handful as H
import emulate as E
import model_table as MTAB
MTAB._install_gpr_widths()
shared = H.build_shared()
cells = AP.read_json(AP.CELLS)

BOUND = 60

def bounded(name, call):
    """one stage in a process of its own, under a real clock."""
    started = time.time()
    sys.stdout.flush()
    forked = os.fork()
    if forked == 0:
        code = 0
        try:
            got = call()
            sys.stdout.write("      %s: answered, %s\n" % (name, got))
        except Exception as problem:
            sys.stdout.write("      %s: RAISED %s: %s\n"
                             % (name, type(problem).__name__,
                                ("%s" % problem)[:200]))
            code = 2
        sys.stdout.flush()
        os._exit(code)
    fired = False
    while True:
        done, _st = os.waitpid(forked, os.WNOHANG)
        if done == forked:
            break
        if time.time() - started > BOUND:
            fired = True
            os.kill(forked, signal.SIGKILL)
            os.waitpid(forked, 0)
            break
        time.sleep(0.02)
    if fired:
        print("    %-28s ABORTED at %d s (the clock fired)" % (name, BOUND))
    else:
        print("    %-28s %.2f s" % (name, time.time() - started))

for asked in [("xor", "gpr_gpr", 8), ("add", "gpr_gpr", 32)]:
    for held, place, working, note in BB2.every_place(shared, cells, asked):
        if working is None:
            continue
        ordered = H.renderer_input(working["term"])
        circuit = BB.blast(ordered)
        lang = "c"
        label = E.sanitize("%s_%s_%d__%s__%s__probe"
                           % (asked[0], asked[1], asked[2],
                              place["writes"].replace(".", "_"), lang))
        made = BB.render_gates(circuit, lang, working["families"],
                               working["home"]["family"],
                               working["bits"], label,
                               working.get("text") or "")
        got, refusal = H.compile_one_place(made["source"],
                                           made["symbol"], lang)
        if got is None:
            print("  %s %s %s / %s: the compile refused: %s"
                  % (asked + (place["writes"], refusal)))
            continue
        raw_bytes, mnem = got
        print("  %s %s %s / %s on c: %d gates, %d carved instructions"
              % (asked[0], asked[1], asked[2], place["writes"],
                 len(circuit.gates), len(mnem)))

        def the_recorded():
            return E.recorded_facts("c/%s" % label, label, raw_bytes,
                                    mnem)

        def the_wrap():
            import canonical_form as CF
            recorded = the_recorded()
            fields = shared["form"].wrap(
                recorded["body_text"], recorded["arrival_families"],
                recorded.get("result_family"),
                recorded.get("result_width"),
                body_bytes=recorded.get("body_bytes"), label=label,
                toolchain=CF.TOOLCHAIN_OF_LANGUAGE.get("c"))
            return "%d characters of wrapped text" % len(
                fields["wrapped_text"])

        def the_canon():
            canon = H.wrapped_body(shared, raw_bytes, mnem, label, "c")
            return "canon40 %s" % canon.get("outcome")

        def the_body_answer():
            canon = H.wrapped_body(shared, raw_bytes, mnem, label, "c")
            term, cause = E.body_answer(shared["reference"], canon)
            if term is None:
                return "no term: %s" % cause
            return "a term of %d bits" % term.size()

        def the_whole_gate():
            check = H.check_one_place(shared, working, made["params"],
                                      raw_bytes, mnem, label, "c",
                                      answer_bits=held.get("key_width"),
                                      attested=H.attested_of(held, None))
            return check.get("outcome")

        bounded("form.wrap alone", the_wrap)
        bounded("wrapped_body (wrap+canon40)", the_canon)
        bounded("body_answer (the lift)", the_body_answer)
        bounded("check_one_place, whole", the_whole_gate)
PY
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the route on xor gpr_gpr 8, every target, printed"
timeout 900 python3 "$G/bb2_run.py" cell xor gpr_gpr 8
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the pass, repeated until an attempt adds no store line"
before=0
if [ -f "$STORE" ]; then before=$(wc -l < "$STORE"); fi
for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do
  echo ""
  echo "  ---- attempt $attempt, store lines before: $before ----"
  timeout 3600 python3 "$G/bb2_run.py" run
  echo "  exit: $?"
  after=0
  if [ -f "$STORE" ]; then after=$(wc -l < "$STORE"); fi
  echo "  store lines after: $after"
  if [ "$after" = "$before" ]; then
    echo "  the attempt added no store line: the pass is done"
    break
  fi
  before=$after
done

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
