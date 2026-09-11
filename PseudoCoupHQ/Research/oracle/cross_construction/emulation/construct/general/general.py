#!/usr/bin/env python3
"""general.py -- THE GENERAL TIER: every place the native route did not
prove, rendered again by `render_general` -- one named intermediate per
node, the language's own operator where it has one and the construction
where it does not -- then compiled, carved, gated, and the construction's
own equality discharged per OPERATION KIND.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * THE NATIVE ROUTE is `handful.the_native_route`, the driver as task
    ap6 left it, unchanged and called and never copied.
  * THE GENERAL TIER is `general_tier` below: per place, the term
    rendered by `render_general.render` under a POLICY, compiled at the
    corpus's ship flags, carved, and gated.
  * THE TWO POLICIES are `native_first` -- the brief's own rule, the
    language's own operator wherever it has one -- and
    `all_constructed`, where the construction answers every node whose
    kind has one.  The second is the GUARANTEE's own measurement and
    the first is the route of record; both are attempted per place and
    whichever proves is the one banked, which is task t2's section 3
    rule ("whoever gets there first") read at the run.
  * TWO OBLIGATIONS, not one, exactly as task t2 states them.  THE GATE
    answers whether the carved body equals the term the render actually
    wrote; THE EQUALITY answers whether that term is the CELL's own.
  * THE EQUALITY IS DISCHARGED PER OPERATION KIND.  Where the render
    constructed nothing the two terms are the same object and the
    canonical form fires with no solver.  Where it constructed
    something, every constructed node is one application of a
    construction whose correctness at that (kind, width, word) is
    proved ONCE -- by a Lean lemma where one closes, else by z3 on the
    construction alone -- and the composition is equal by structural
    induction on the term.  z3 on the whole miter is the last resort
    and is bounded at the brief's hard 30 seconds.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4, checked after
every store line.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

HOW THIS FILE OBEYS IT.  Which places the tier acts on is the bank's own
keys; which route a node takes is whether the target's renderer raises;
a cell is addressed by (`mnem`, operand shape, `key_width`), and the
mnemonic sits in `mnem`, which the ruling of 2026-09-08 states is
machine form.

usage:
  general.py preflight            what the pass would attempt
  general.py run [<n>]            the pass; `<n>` stops after n runs
  general.py bank                 the bank rebuilt with this pass in it
  general.py readings             the three readings with this pass in
  general.py report               `general.md`
  general.py tier <mnem> <shape> <width> <lang>
                                  one (cell, target), printed
  general.py probe <mnem> <shape> <width> <lang> <stage>
                                  one (cell, target) stopped after
                                  `render`, `compile` or `gate`, with
                                  the size and the resident reading
                                  after each stage

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
EMULATION = os.path.normpath(os.path.join(CONSTRUCT, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
AUTOPOLY = os.path.join(EMULATION, "autopoly")
sys.path.insert(0, HERE)
sys.path.insert(0, CONSTRUCT)
sys.path.insert(0, HANDFUL)
sys.path.insert(0, AUTOPOLY)
sys.path.insert(0, EMULATION)
sys.path.insert(0, os.path.join(EMULATION, "rust"))
sys.path.insert(0, os.path.join(EMULATION, "go"))
sys.path.insert(0, os.path.join(EMULATION, "swift"))

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import render_general as RG                                      # noqa: E402

PASS_LABEL = "t4_general"

REPORT = os.path.join(HERE, "general.md")
AGGREGATE = os.path.join(HERE, "general.json")
PROOFS = os.path.join(HERE, "construction_proofs.json")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"

EQUALITY_CEILING_MS = 30000
"""the brief's HARD ceiling on the last resort; never raised."""

Z3_MEMORY_MB = 4096
"""the solver's OWN memory bound, under this task's 6 GB, so a solver
that grows past it answers `unknown` with reason `memout` -- an
UNDECIDED row with a cause -- instead of being stopped by the operating
system with no row at all."""

z3.set_param("memory_max_size", Z3_MEMORY_MB)

CANONICAL_CEILING = 200000
"""how large the term the render wrote may be WRITTEN OUT before the
canonical form is not attempted on it.

The canonical form compares two PRINTED texts, and a printed term names
no intermediate: a step read three times is written three times.  Every
constructed term is made of such steps.  So the size is measured the way
printing counts it (`build.unfolded_size`) and the form is offered where
it can finish, declined by name where it cannot, and the kind lemma --
which is about the construction and not about its text -- answers
instead.

THE NUMBER IS TASK t2's OWN (`construct.UNFOLDED_CEILING`,
`run_lemmas_t2.STATEMENT_CEILING`) and for its own reason, so the two
tiers refuse a statement at the same size."""

GATE_INSTRUCTION_CEILING = 4000
"""how many carved instructions the gate is offered.

MEASURED, in this task's lane `t4_l9`: the render and the compile of a
construction are cheap and fast -- `div gpr_one 64` on c under
`all_constructed` renders 19,592 statements in 2.1 s at 88 MB resident
and compiles and carves 20,109 instructions in 6.1 s at 90 MB -- and it
is the GATE that runs out: lifting a body of that size through the
reference and posing it builds a term per instruction and was stopped by
the operating system at the instance's 20 GB with the task's own 6 GB
bound never reached.  A body above this ceiling is recorded as
CONSTRUCTED, COMPILED and CARVED with its instruction count and its
landing, and NOT GATED, with the count on the row: that is the gate's
cost, which is what the brief's section 2 item 4 asks for, and it is a
row with a named cause rather than an ABORT with nothing in it."""

CAUSE_GATE_TOO_LARGE = ("the carved body is larger than the number of "
                        "instructions this task's gate is offered: the "
                        "lift builds one term per instruction and a "
                        "body of this size is not posed at all")

GATE_SECONDS = 5
"""how long ONE gate call may run before this task stops asking.

MEASURED: `adc gpr_gpr 64` on go -- a 65-bit adder constructed into 185
statements and about 250 carved instructions -- did not come back from
the gate inside 600 s in lanes `t4_l10` step [1/6] and `t4_l16` step
[1/3], with the process holding under 120 MB and burning processor.  The
gate of record is `handful.check_one_place`, which puts the carved body
on the pipeline's canonical form and then asks z3 at the gate's own
3,000 ms; the 3,000 ms bounds ONE solver call and not the number of
them.  A place whose gate runs past this bound is recorded as
CONSTRUCTED, COMPILED and CARVED with its instruction count and its
landing, and NOT GATED, with the seconds on the row.

HOW IT IS ENFORCED, and why that is the right tool: `signal.alarm`
raises in the PYTHON frame, so it takes effect between calls into the
solver and not inside one.  That is exactly the bound wanted -- one
solver call is already bounded at 3,000 ms by the gate itself, and what
this bounds is how many of them are asked.

WHY FIVE SECONDS, measured on this pass's own store: of the 443 gate
calls that ANSWERED in the first 93 runs of lane `t4_l20`, the slowest
took 0.099 s and the median 0.011 s.  The calls that run long do not run
a little long -- they run past any bound this task could state -- so
five seconds is fifty times the slowest answer on record and costs
nothing that was going to be answered.

WHY IT WAS LOWERED TWICE, and what the number buys, because a bound
that moves must say what moved it.  At 120 s, one flag consumer cost
2,046 s (`setl gpr_one 8` on c, lane `t4_l20`): a flag consumer carries
one written place per setter cell -- seventeen of them -- and each place
pays the whole bound.  At 30 s the same cell still held lane `t4_l22`
for more than 44 minutes and its lane's own attempt budget was about to
cut it, which would have left the pass unable to pass that one cell at
all.  At 5 s that cell costs about three minutes.  Nothing that answers
is lost at any of the three, and what is bought is that the pass
FINISHES."""

CAUSE_GATE_RAN_LONG = ("the gate did not answer inside the seconds this "
                       "task allows one gate call: the carved body is "
                       "on the canonical form and the solver was asked, "
                       "and the asking had not finished")


RUN_SECONDS = 900
"""how long ONE (cell, target) run may take before this pass leaves it
and goes on.

WHY IT EXISTS: the pass is run inside a lane that repeats it, and the
repeat stops when an attempt adds no store line.  A single run that
takes longer than one attempt's own wall clock therefore stops the pass
DEAD -- every attempt starts it again, every attempt is cut in the
middle of it, and nothing after it is ever reached.  Lane `t4_l22` was
44 minutes into one such run with its attempt budget nearly spent.  A
run past this bound is left with its cause on the record and the pass
goes on, which is a row and a finished pass rather than a pass that
stops."""


# THE TWO BOUNDS ARE ENFORCED BY INTERRUPTING THE SOLVER, never by
# raising: `under_the_clock` below says why, and the two exception
# classes that did raise are gone with the lane that measured them.


def not_gated(reason, **extra):
    """the record for a place that rendered, compiled and carved and
    whose GATE WAS NEVER ASKED.

    IT CARRIES NO `check`, deliberately, and that is the bank's own
    reading: `bank.kind_of_place` answers `refused` for a place with no
    check -- "never reached the gate at all", in its own words -- and
    `bank.cause_of_place` then takes the sentence off `refusal_cause`.
    A place banked `undecided` would say the gate ran and could not
    decide, which is not what happened.

    The one thing that must not happen is the progress line raising on
    it: `handful.verdict_of_run` reads `place["check"]` unconditionally
    and task t4's lane `t4_l16` step [2/3] ended on `KeyError: 'check'`
    at run 62 of 665, so `the_verdict_line` below answers for it."""
    out = {"the_gate_was_not_asked": reason}
    out.update(extra)
    return out


def the_verdict_line(line):
    """`autopoly.one_line_verdict`, which cannot read a place whose gate
    was never asked, with that case answered here instead."""
    import autopoly as AP
    try:
        return AP.one_line_verdict(line)
    except KeyError:
        for place in line.get("places") or []:
            if place.get("refusal_cause"):
                return "NOT GATED: %s" % place["refusal_cause"][:70]
            continue
        return "NOT GATED"


def under_the_clock(seconds, function, *arguments, **named):
    """one call under a wall clock that stops THE SOLVER rather than the
    interpreter.

    WHY IT INTERRUPTS AND DOES NOT RAISE, and it is measured twice.  A
    signal handler that raises lands in whatever Python frame is
    running, and on this pass that is constantly z3's own
    `AstRef.__del__`: Python IGNORES an exception raised in a `__del__`,
    so the bound fires and is thrown away (lane `t4_l23` printed
    "Exception ignored in: AstRef.__del__ ... TheGateRanLong: 5 s"), and
    raising through the solver's C frames ended attempt 1 of that lane
    with a `Segmentation fault`, exit 139, at run 109 of 654.

    `Context.interrupt` is z3's own way to stop a solver: the running
    `check` returns `unknown` and every later one returns quickly too,
    so the call comes back by itself and nothing is raised anywhere.
    The timer REPEATS so a call that starts a second solver is stopped
    again.

    Returns (the answer, whether the clock fired, the seconds taken)."""
    import signal
    state = {"fired": False}

    def fired(_number, _frame):
        state["fired"] = True
        try:
            z3.main_ctx().interrupt()
        except Exception:                                     # noqa: BLE001
            pass
        return

    previous = signal.signal(signal.SIGALRM, fired)
    pending = signal.getitimer(signal.ITIMER_REAL)
    signal.setitimer(signal.ITIMER_REAL, 0, 0)
    started = time.time()
    signal.setitimer(signal.ITIMER_REAL, float(seconds), float(seconds))
    try:
        answer = function(*arguments, **named)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        signal.signal(signal.SIGALRM, previous)
        if pending[0]:
            left = pending[0] - (time.time() - started)
            if left < 0.5:
                left = 0.5
            signal.setitimer(signal.ITIMER_REAL, left, pending[1])
    return answer, state["fired"], round(time.time() - started, 3)

POLICIES = ("native_first", "all_constructed")

CAUSE_ALREADY_PROVED = ("the native route proved this place, so there "
                        "is nothing the general tier can add")
CAUSE_NOT_RENDERED_UPSTREAM = ("the native route did not reach this "
                               "place's term at all, so the tier has "
                               "nothing to render")
CAUSE_EQUALITY = ("the carved body is proved equal to the term the "
                  "render wrote, and that term's equality with the "
                  "CELL's own is not discharged by any of the three "
                  "forms")
CAUSE_NO_80_BIT_HOLDER = ("an arrival or answer home on the x87 stack: "
                          "%s has no 80-bit holder, so the value cannot "
                          "be received or answered with at all")


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def word_of(lang):
    import construct as CONS
    return CONS.word_of(lang)


# ==================================================================
# section 1: the proof table, one row per (kind, width, word)
# ==================================================================

PROOF_CACHE = None


def proof_table():
    """{(kind, width, word): the row} -- the construction's own proof at
    that instance, off `construction_proofs.json`, which
    `collect_proofs.py` writes from the Lean lemmas and from
    `check_constructions.py`'s z3 rows.

    A row's `form` is `lemma` (a Lean theorem closed), `sat` (z3 proved
    the construction equal to the operation at that instance) or absent
    (neither)."""
    global PROOF_CACHE
    if PROOF_CACHE is not None:
        return PROOF_CACHE
    PROOF_CACHE = {}
    if not os.path.exists(PROOFS):
        return PROOF_CACHE
    handle = open(PROOFS)
    document = json.load(handle)
    handle.close()
    for row in document.get("rows") or []:
        key = (row["kind"], int(row["width"]), int(row["word"]))
        PROOF_CACHE[key] = row
        continue
    return PROOF_CACHE


def the_equality(cell_term, built_term, constructed_widths, word):
    """whether the term the render WROTE is the cell's own mapping, in
    the three forms the brief names, in the brief's order."""
    import handful as H
    import term as T
    out = {"forms": []}
    started = time.time()
    if built_term.get_id() == cell_term.get_id():
        out["forms"].append({"form": "canonical", "answer": True})
        out["proof"] = "canonical"
        out["outcome"] = "PROVED"
        out["reason"] = ("the render wrote the cell's own term: every "
                         "node of it is the target's own operator, so "
                         "there is nothing constructed to discharge")
        out["seconds"] = round(time.time() - started, 3)
        return out
    holder = T.Term()
    anything_constructed = False
    for kind in constructed_widths:
        if constructed_widths[kind]:
            anything_constructed = True
            break
        continue
    built_nodes = B.node_count(built_term, CANONICAL_CEILING)
    written_out = CANONICAL_CEILING
    if not anything_constructed:
        written_out = B.unfolded_size(built_term, CANONICAL_CEILING)
    if written_out >= CANONICAL_CEILING:
        # NOT NORMALISED EITHER.  `the_normalised_term` runs
        # `z3.simplify` and the ordering step over the whole term; on a
        # construction those are a cost with nothing bought, because the
        # form that would use the result is the one being declined.  The
        # miter below is posed on the terms as they are, which is the
        # same question.
        cell_posed = cell_term
        built_posed = built_term
    else:
        cell_posed = H.the_normalised_term(cell_term)
        built_posed = H.the_normalised_term(built_term)
    # THE CANONICAL FORM IS A COMPARISON OF TWO PRINTED TEXTS, and
    # `term.one_line` -- which `Term.normalize` ends with -- writes a
    # step that reads its own previous step ONCE PER READ.  A
    # constructed term is nothing but such steps: the adder at 65 bits
    # over a word of 64 is a few hundred DISTINCT nodes and an
    # unbounded number of written ones.  So the size is measured first,
    # on the distinct nodes, and the printed form is only attempted
    # where it can finish.  Measured: task t4's lane `t4_l8` step [1/4]
    # (`adc gpr_gpr 64` on go) spent more than 700 s here and the lane's
    # own ceiling stopped it.
    out["built_nodes"] = built_nodes
    out["built_nodes_written_out"] = written_out
    out["canonical_ceiling"] = CANONICAL_CEILING
    if written_out >= CANONICAL_CEILING:
        why = ("the term the render wrote is %d or more nodes WRITTEN "
               "OUT (%d distinct), and the canonical form is its text "
               "written out, which names no intermediate; the ceiling "
               "this task states is %d"
               % (written_out, built_nodes, CANONICAL_CEILING))
        if anything_constructed:
            why = ("the render CONSTRUCTED at least one node, so the "
                   "question is whether each construction is the "
                   "operation it replaced -- which the kind lemma "
                   "answers -- and not whether the two terms print the "
                   "same text, which a construction and an operation "
                   "never do; the printed form is not attempted (%d "
                   "distinct nodes)" % built_nodes)
        out["forms"].append({"form": "canonical", "answer": None,
                             "why": why})
    else:
        cell_text = holder.normalize(cell_posed)
        built_text = holder.normalize(built_posed)
        same = (cell_text == built_text)
        out["forms"].append({"form": "canonical", "answer": same})
        if same:
            out["proof"] = "canonical"
            out["outcome"] = "PROVED"
            out["reason"] = ("the cell's mapping and the term the "
                             "render wrote print the same text under "
                             "the pipeline's own normaliser")
            out["seconds"] = round(time.time() - started, 3)
            return out
    table = proof_table()
    held = []
    missing = []
    for kind in sorted(constructed_widths):
        for width in sorted(constructed_widths[kind]):
            key = (kind, int(width), word)
            entry = {"kind": kind, "width": int(width), "word": word,
                     "nodes": constructed_widths[kind][width]}
            found = table.get(key)
            if found is None:
                entry["why"] = ("no proof is recorded for this "
                                "construction at this width over this "
                                "word")
                missing.append(entry)
                continue
            if found.get("form") is None:
                entry["why"] = ("the construction's own proof at this "
                                "instance is %s" % found.get("outcome"))
                missing.append(entry)
                continue
            entry["form"] = found["form"]
            entry["proof_of_record"] = found.get("theorem") \
                or found.get("outcome")
            held.append(entry)
            continue
        continue
    answered = bool(held) and not missing
    out["forms"].append({"form": "kind lemma", "answer": answered,
                         "proofs_held": held,
                         "proofs_missing": missing})
    if answered:
        out["proof"] = "kind"
        out["outcome"] = "PROVED"
        out["reason"] = ("every node the render CONSTRUCTED is one "
                         "application of a construction proved equal "
                         "to the operation it replaced at that width "
                         "over that word; the render is one such "
                         "replacement per node, so the two terms are "
                         "equal by structural induction on the term")
        out["seconds"] = round(time.time() - started, 3)
        return out
    solver = z3.Solver()
    solver.set("timeout", EQUALITY_CEILING_MS)
    try:
        solver.add(cell_posed != built_posed)
        answer = solver.check()
    except Exception as problem:                              # noqa: BLE001
        # THE SOLVER'S OWN MEMORY BOUND, ANSWERED rather than allowed to
        # stop the pass: z3 raises at `memory_max_size` and its C++ side
        # calls `terminate` if nothing catches it (lane `t4_l15` part 1,
        # exit 134).
        out["forms"].append({"form": "sat",
                             "answer": "the solver stopped: %s"
                                       % problem})
        out["solver_timeout_ms"] = EQUALITY_CEILING_MS
        out["solver_memory_bound_mb"] = Z3_MEMORY_MB
        out["seconds"] = round(time.time() - started, 3)
        out["proof"] = None
        out["outcome"] = "UNDECIDED"
        out["reason"] = ("z3 stopped before answering either way: %s"
                         % problem)
        return out
    out["forms"].append({"form": "sat", "answer": str(answer)})
    out["solver_timeout_ms"] = EQUALITY_CEILING_MS
    out["seconds"] = round(time.time() - started, 3)
    if answer == z3.unsat:
        out["proof"] = "sat"
        out["outcome"] = "PROVED"
        out["reason"] = ("z3 found no input at which the cell's mapping "
                         "and the term the render wrote differ")
        return out
    out["proof"] = None
    if answer == z3.sat:
        out["outcome"] = "DISPROVED"
        out["reason"] = ("z3 found an input at which the cell's mapping "
                         "and the term the render wrote differ")
        out["counterexample"] = str(solver.model())[:400]
        return out
    out["outcome"] = "UNDECIDED"
    out["reason"] = ("z3 answered neither way inside the brief's hard "
                     "30-second ceiling; the ceiling is the brief's own "
                     "and is not raised")
    return out


# ==================================================================
# section 2: one place, one policy
# ==================================================================

def general_tier(shared, held, lang, record):
    """the driver's ONE call: every place of this run rendered again by
    the general render, under both policies.

    Returns None where the tier rendered nothing for any place."""
    word = word_of(lang)
    if word is None:
        return None
    inputs = held.get("places")
    if not inputs:
        return None
    natives = record.get("places") or []
    out = []
    reached = False
    started = time.time()
    for index, place in enumerate(inputs):
        native = None
        if index < len(natives):
            native = natives[index]
        made = one_place(shared, held, lang, place, native, word, index)
        out.append(made)
        if made.get("check") is not None:
            reached = True
        continue
    return {
        "route": "general",
        "word_bits": word,
        "places": out,
        "reached_the_gate": reached,
        "rendered_any_place": any_rendered(out),
        "seconds": round(time.time() - started, 3),
    }


def any_rendered(places):
    for place in places:
        if place.get("rendered"):
            return True
        continue
    return False


def one_place(shared, held, lang, place, native, word, index):
    """one written place through the general tier: both policies, the
    better answer kept."""
    import handful as H
    out = {
        "writes": place["writes"],
        "text": place.get("text"),
        "sexpr": place.get("sexpr"),
        "bits": place.get("bits"),
        "families": place.get("families"),
        "home": place.get("home"),
    }
    if place.get("halved") is not None:
        out["halved"] = place["halved"]
    if native is not None:
        check = (native.get("check") or {})
        if check.get("outcome") == "PROVED_ON_SHIP":
            out["rendered"] = False
            out["refusal_cause"] = CAUSE_ALREADY_PROVED
            return out
    if place.get("not_rendered") is not None:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
        out["refusal_detail"] = place["not_rendered"]
        return out
    working = place
    if place.get("halved") is None:
        projected = H.projected_lane(shared, place, held["key_width"])
        if projected is not None:
            out["lane"] = projected["lane"]
            if projected.get("refusal_cause") is not None:
                out["rendered"] = False
                out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
                out["refusal_detail"] = projected["refusal_cause"]
                return out
            working = projected["place"]
    if working.get("term") is None:
        out["rendered"] = False
        out["refusal_cause"] = CAUSE_NOT_RENDERED_UPSTREAM
        out["refusal_detail"] = "the place carries no term"
        return out
    attempts = []
    for policy in POLICIES:
        attempt = one_attempt(shared, held, lang, working, place, word,
                              policy, index)
        attempts.append(attempt)
        if the_attempt_proved(attempt):
            # WHOEVER GETS THERE FIRST, which is the brief's own rule
            # read at the run: `native_first` is the route of record and
            # where it PROVES the place there is nothing left for the
            # second policy to settle.  `all_constructed` is still
            # attempted at every place the first policy does not prove,
            # which is where the GUARANTEE is the question.
            #
            # MEASURED, and this is why the rule is applied rather than
            # both policies always run: a flag consumer carries one
            # place per setter cell -- `setl gpr_one 8` has seventeen --
            # and a gate that runs long costs its whole bound on each,
            # so that one (cell, target) took 2,046 s of lane `t4_l20`'s
            # first attempt with both policies run at every place.
            break
        continue
    out["attempts"] = attempts
    chosen = the_better(attempts)
    if chosen is None:
        out["rendered"] = False
        out["refusal_cause"] = attempts[0].get("refusal_cause") \
            or attempts[1].get("refusal_cause") or "no attempt rendered"
        out["refusal_detail"] = attempts[0].get("refusal_detail")
        return out
    for field in ("rendered", "source", "source_path", "symbol",
                  "compiled", "compile_refusal", "body_bytes",
                  "body_text", "landing", "label", "policy",
                  "statements", "constructed_kinds",
                  "constructed_widths", "native_nodes",
                  "constructed_nodes", "check", "instructions",
                  "not_gated", "gate_seconds",
                  "gate_instruction_ceiling",
                  "gate_on_the_written_term", "equality",
                  "refusal_cause", "refusal_detail", "proof"):
        if field in chosen:
            out[field] = chosen[field]
            continue
    return out


def the_attempt_proved(attempt):
    """whether this attempt settled the place: the gate proved the
    carved body equals the term the render wrote, AND the equality
    proved that term is the cell's own.  Both, never one."""
    check = attempt.get("check") or {}
    if check.get("outcome") != "PROVED_ON_SHIP":
        return False
    equality = attempt.get("equality") or {}
    return equality.get("outcome") == "PROVED"


def the_better(attempts):
    """whoever gets there first: the attempt that PROVED, and the
    smaller carved body where both did; else the one that reached the
    gate; else the first that rendered."""
    proved = []
    for attempt in attempts:
        check = attempt.get("check") or {}
        if check.get("outcome") == "PROVED_ON_SHIP":
            proved.append(attempt)
            continue
        continue
    if proved:
        proved.sort(key=lambda one: one.get("instructions") or 10 ** 6)
        return proved[0]
    for attempt in attempts:
        if attempt.get("gate_on_the_written_term") is not None:
            return attempt
        continue
    for attempt in attempts:
        if attempt.get("rendered"):
            return attempt
        continue
    return None


def one_attempt(shared, held, lang, working, place, word, policy,
                index):
    """one policy: render, compile, carve, gate, discharge."""
    import emulate as E
    import handful as H
    out = {"policy": policy}
    label = E.sanitize("%s_%s_%d__%s__%s__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          place["writes"].replace(".", "_"), lang,
                          policy))
    out["label"] = label
    term = working["term"]
    ordered = H.renderer_input(term)
    home = working["home"]
    if E.is_an_x87_arrival(home.get("family")):
        if lang not in H.TARGETS_WITH_AN_80_BIT_HOLDER:
            out["rendered"] = False
            out["refusal_cause"] = CAUSE_NO_80_BIT_HOLDER % lang
            return out
        ordered = H.the_x87_value(ordered)
    try:
        made = RG.render(ordered, lang, working["families"],
                         home["family"], working["bits"], label, word,
                         policy, working.get("text") or "")
    except Exception as problem:
        if not RG.is_a_refusal(problem):
            out["rendered"] = False
            out["refusal_cause"] = "the render raised"
            out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                                problem)
            return out
        out["rendered"] = False
        out["refusal_cause"] = getattr(problem, "cause", "%s" % problem)
        out["refusal_detail"] = getattr(problem, "detail", "")
        return out
    out["rendered"] = True
    out["source"] = made["source"]
    out["symbol"] = made["symbol"]
    out["statements"] = made["statements"]
    out["native_nodes"] = made["native_nodes"]
    out["constructed_nodes"] = made["constructed_nodes"]
    out["constructed_kinds"] = made["constructed_kinds"]
    out["constructed_widths"] = made["constructed_widths"]
    out["source_path"] = write_source(label, lang, made["source"])
    got, refusal = H.compile_one_place(made["source"], made["symbol"],
                                       lang)
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = refusal
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["body_bytes"] = " ".join(raw_bytes)
    out["body_text"] = "; ".join(mnem)
    out["instructions"] = len(mnem)
    out["landing"] = H.landing_of(mnem, held["mnem"])
    out["gate_instruction_ceiling"] = GATE_INSTRUCTION_CEILING
    if len(mnem) > GATE_INSTRUCTION_CEILING:
        # CONSTRUCTED, COMPILED AND CARVED, AND NOT GATED.  The row keeps
        # its statement count, its instruction count and its landing, so
        # the collapse column and the source-size table still carry it;
        # what it does not carry is a verdict, and the cause says why.
        out["refusal_cause"] = CAUSE_GATE_TOO_LARGE
        out["refusal_detail"] = ("%d instructions, above the %d this "
                                 "task's gate is offered"
                                 % (len(mnem), GATE_INSTRUCTION_CEILING))
        out["not_gated"] = not_gated(CAUSE_GATE_TOO_LARGE,
                                     instructions=len(mnem),
                                     ceiling=GATE_INSTRUCTION_CEILING)
        return out
    written = made.get("written_term")
    posed = dict(working)
    if written is not None:
        posed["term"] = written
    check, ran_long, seconds = under_the_clock(
        GATE_SECONDS, H.check_one_place, shared, posed, made["params"],
        raw_bytes, mnem, label, lang,
        answer_bits=held.get("key_width"),
        attested=H.attested_of(held, None))
    out["gate_seconds"] = seconds
    if ran_long:
        out["gate_seconds_allowed"] = GATE_SECONDS
        out["gate_was_interrupted"] = True
        out["refusal_cause"] = CAUSE_GATE_RAN_LONG
        out["refusal_detail"] = ("%d instructions, %d s allowed, and "
                                 "the solver was interrupted"
                                 % (len(mnem), GATE_SECONDS))
        out["not_gated"] = not_gated(CAUSE_GATE_RAN_LONG,
                                     instructions=len(mnem),
                                     seconds_allowed=GATE_SECONDS,
                                     the_gate_answered=check.get(
                                         "outcome"))
        out["gate_after_the_interrupt"] = check
        return out
    if written is None or written.get_id() == term.get_id():
        out["check"] = check
        out["equality"] = {"proof": "canonical", "outcome": "PROVED",
                           "reason": ("the render wrote the cell's own "
                                      "term")}
        out["proof"] = "canonical"
        return out
    equality = the_equality(term, written, made["constructed_widths"],
                            word)
    out["equality"] = equality
    out["proof"] = equality.get("proof")
    if equality.get("outcome") != "PROVED":
        out["gate_on_the_written_term"] = check
        out["refusal_cause"] = CAUSE_EQUALITY
        out["refusal_detail"] = "%s: %s" % (equality.get("outcome"),
                                            equality.get("reason"))
        out["not_gated"] = not_gated(
            CAUSE_EQUALITY,
            the_gate_on_the_written_term=check.get("outcome"),
            the_equality=equality.get("outcome"))
        return out
    out["check"] = check
    return out


SRC_DIR = None


def write_source(label, lang, source):
    import handful as H
    if SRC_DIR is None:
        return None
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    name = label + H.suffix_of(lang)
    handle = open(os.path.join(SRC_DIR, name), "w")
    handle.write(source)
    handle.close()
    return os.path.join(os.path.basename(SRC_DIR), name)


# ==================================================================
# section 3: the driver's dispatch, and the pass
# ==================================================================

def find_emulation(shared, held, lang):
    """the driver's run with THIS tier in place of task t2's eight
    schemas: the native route, then the general tier, unconditionally."""
    import handful as H
    record = H.the_native_route(shared, held, lang)
    record["general"] = general_tier(shared, held, lang, record)
    return record


THE_TIER_SOURCES = ("general.py", "render_general.py", "build.py",
                    "softfloat.py", "lean_general.py")
"""the files THIS TIER is; their bytes are the version it runs at."""


def tier_version():
    """the sha256 of this tier's own sources, joined.

    WHY IT IS SET AS THE LOOP'S VERSION.  A certificate carries
    `code_version` -- the sha256 of the driver, the loop and the
    renderer that wrote the target -- and the bank's re-attempt rule
    holds back any key whose recorded version equals the version running
    now.  This tier changes none of those three files: it is new
    machinery beside them, and a key answered by the driver alone is a
    key this tier has not been asked about.  So the tier's own bytes are
    the loop's version for this pass, set from OUTSIDE the driver the
    way `autopoly.configure` sets its paths, and every uncertified key
    is attempted because the machinery HAS moved."""
    import hashlib
    digest = hashlib.sha256()
    for name in THE_TIER_SOURCES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        handle = open(path, "rb")
        digest.update(handle.read())
        handle.close()
        continue
    return digest.hexdigest()


def configure_pass():
    import autopoly as AP
    global SRC_DIR
    runs, src = store_paths()
    SRC_DIR = src
    AP.LOOP_VERSION = tier_version()
    AP.PASS_LABEL = PASS_LABEL
    AP.HELD = {
        "runs": runs,
        "aggregate": AGGREGATE,
        "src": src,
        "primitive": os.path.join(HERE, "%s_primitive.json" % PASS_LABEL),
        "spellings": os.path.join(HERE, "%s_spellings.json" % PASS_LABEL),
        "report": REPORT,
    }
    AP.RUNS = AP.HELD["runs"]
    AP.AGGREGATE = AP.HELD["aggregate"]
    AP.SRC_DIR = AP.HELD["src"]
    AP.PRIMITIVE = AP.HELD["primitive"]
    AP.SPELLINGS = AP.HELD["spellings"]
    AP.REPORT = AP.HELD["report"]
    if not os.path.isdir(src):
        os.makedirs(src)
    AP.AUDIT_SHARE = 0.0
    AP.ATTEMPTS_ARE_ON = True
    AP.ABORT_NAME = ABORT_NAME
    AP.configure(AP.RUNS, AP.SRC_DIR)
    import handful as H
    H.find_emulation = find_emulation
    return AP


def store_paths():
    """THE STORE LIVES WHERE EVERY PASS'S STORE LIVES, in the autopoly
    folder, for task t2's own reason: `bank.store_path` writes a
    certificate's `produced_by.store` relative to that folder, and a
    store reached with `..` puts an operator token on a structure field,
    which the guard refuses."""
    return (os.path.join(AUTOPOLY, "%s_runs.jsonl" % PASS_LABEL),
            os.path.join(AUTOPOLY, "src_%s" % PASS_LABEL))


def register_with_the_bank():
    """this pass added to the bank's pass table, and TASK t2's BESIDE IT.

    WHY BOTH.  `bank.PASSES` is the file's own list and neither the
    construct tier's pass nor this one is in it -- each registers itself
    from outside, which is what task t2's `construct.register_with_the_
    bank` says and why.  A rebuild run from HERE with only this pass
    registered would write a bank with task t2's fourteen proved places
    missing, which is not a delta but a loss; so t2's own registration
    is called, from t2's own file, before this one."""
    import construct as CONS
    CONS.register_with_the_bank()
    import bank as BK
    for step in BK.PASSES:
        if step["pass"] == PASS_LABEL:
            return BK
        continue
    runs, src = store_paths()
    BK.PASSES.append({
        "pass": PASS_LABEL,
        "store": os.path.basename(runs),
        "reader": "compiled",
        "src": src,
        "task": "t4",
        "log": "this task",
        "targets": list(BK.COMPILED),
        "optional": True,
    })
    return BK


def split(record):
    """one finished run as the two runs it is: the native route's, and
    the general tier's where the tier rendered anything."""
    import autopoly5 as LOOP
    made = record.pop("general", None)
    out = [record]
    if made is None:
        return out
    if not made.get("places"):
        return out
    if not made.get("rendered_any_place"):
        return out
    second = {}
    for field in ("mnem", "shape", "key_width", "lang", "row_id",
                  "line", "chosen_by", "attestation", "setter",
                  "code_version", "attested_ledger_rows", "seconds"):
        if field in record:
            second[field] = record[field]
            continue
    second["route"] = "general"
    second["word_bits"] = made["word_bits"]
    second["places"] = trimmed(made["places"])
    second["seconds"] = made.get("seconds")
    second["composition"] = []
    out.append(LOOP.as_machine_form(second))
    return out


def trimmed(places):
    """the places with the two attempts' full sources dropped: the
    CHOSEN attempt's source is already on the place and is written to
    the source folder, and a store line carrying both is the store
    filled with text nobody reads."""
    out = []
    for place in places:
        made = dict(place)
        attempts = made.pop("attempts", None)
        if attempts is not None:
            short = []
            for attempt in attempts:
                row = dict(attempt)
                row.pop("source", None)
                short.append(row)
                continue
            made["attempts"] = short
        out.append(made)
        continue
    return out


def walk(order, runs, done, limit):
    import autopoly as AP
    import gate as G
    import handful as H
    import model_table as MTAB
    shared = H.build_shared()
    reposer = G.Gate(reference=shared["reference"],
                     solver_timeout_ms=AP.REPOSE_MS)
    MTAB._install_gpr_widths()
    in_table = H.load_in_table()
    cells = AP.read_json(AP.CELLS)
    say("the gate of record: %d ms; the one re-pose: %d ms; the "
        "equality's ceiling: %d ms"
        % (shared["gate"].solver_timeout_ms, AP.REPOSE_MS,
           EQUALITY_CEILING_MS))
    say("the construction proofs on record: %d (kind, width, word) rows"
        % len(proof_table()))
    total = len(order)
    index = 0
    ran = 0
    tiers = 0
    declines = {}
    started = time.time()
    behind = the_left_behind()
    say("left behind by an earlier attempt, and gone past here: %d"
        % len(behind))
    for row in sorted(behind):
        say("   %s %s %s -> %s" % row)
        continue
    say("")
    for asked, lang, ledger in order:
        index = index + 1
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, total, asked[0], asked[1], asked[2], lang,
               ledger))
        if (asked[0], asked[1], asked[2], lang) in behind:
            cause = ("the run was left behind: an earlier attempt of "
                     "this pass entered it and did not come out inside "
                     "that attempt's own wall clock")
            declines[cause] = declines.get(cause, 0) + 1
            say("   LEFT BEHIND: %s" % cause)
            continue
        mark_in_flight(asked, lang)
        ran, tiers = one_numbered_run(AP, shared, reposer, cells,
                                      asked, lang, ledger, in_table,
                                      done, runs, declines, ran, tiers,
                                      index)
        clear_in_flight()
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d store line(s) written" % ran)
            break
        continue
    seconds = round(time.time() - started)
    say("")
    say("store lines written this lane: %d in %d s" % (ran, seconds))
    say("of them, general-tier runs: %d" % tiers)
    say("lines on %s: %d" % (runs, AP.count_lines(runs)))
    say("")
    say("| where the tier declined, LITERAL | places |")
    say("|---|---|")
    for cause in sorted(declines, key=lambda one: -declines[one]):
        say("| %s | %d |" % (cause.replace("|", "/")[:180],
                             declines[cause]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    write_declines(declines, ran, tiers, seconds)
    return 0


IN_FLIGHT = None
LEFT_BEHIND = None


def in_flight_paths():
    return (os.path.join(AUTOPOLY, "%s_in_flight.json" % PASS_LABEL),
            os.path.join(AUTOPOLY, "%s_left_behind.json" % PASS_LABEL))


def the_left_behind():
    """every (cell, target) an EARLIER attempt of this pass entered and
    never came out of, so this attempt goes past it.

    WHY IT EXISTS, measured: the pass is run in a lane that repeats it
    and stops when an attempt adds no store line.  One (cell, target)
    that does not return inside an attempt's own wall clock therefore
    stops the pass dead -- every attempt starts it again, every attempt
    is cut inside it, and nothing after it is ever reached.  Lane
    `t4_l23` and lane `t4_l24` both ended on the same one.  A run is
    written down BEFORE it starts and rubbed out after it finishes, so
    what is left written down when an attempt is cut is exactly the run
    that was in flight; the next attempt records it with its cause and
    goes on."""
    global IN_FLIGHT, LEFT_BEHIND
    flight, behind = in_flight_paths()
    LEFT_BEHIND = []
    if os.path.exists(behind):
        handle = open(behind)
        LEFT_BEHIND = json.load(handle)
        handle.close()
    if os.path.exists(flight):
        handle = open(flight)
        held = json.load(handle)
        handle.close()
        if held and held not in LEFT_BEHIND:
            LEFT_BEHIND.append(held)
        handle = open(behind, "w")
        json.dump(LEFT_BEHIND, handle, indent=1, sort_keys=True)
        handle.close()
        os.remove(flight)
    IN_FLIGHT = flight
    out = set()
    for row in LEFT_BEHIND:
        out.add((row[0], row[1], int(row[2]), row[3]))
        continue
    return out


def mark_in_flight(asked, lang):
    handle = open(IN_FLIGHT, "w")
    json.dump([asked[0], asked[1], asked[2], lang], handle)
    handle.close()
    return


def clear_in_flight():
    if os.path.exists(IN_FLIGHT):
        os.remove(IN_FLIGHT)
    return


def one_numbered_run(AP, shared, reposer, cells, asked, lang, ledger,
                     in_table, done, runs, declines, ran, tiers, index):
    """one (cell, target) run, UNDER THE RUN'S OWN WALL CLOCK.

    Every record the run yielded before the bound fired is already on
    the store -- `autopoly.append_run` flushes each -- so what a bound
    costs is the rest of that one run and nothing else."""
    counted = [ran, tiers]

    def walk_the_pair():
        for record in AP.one_pair(shared, reposer, cells, asked, lang,
                                  ledger, in_table, done):
            if record is None:
                continue
            tally_the_declines(record, declines)
            for line in split(record):
                AP.append_run(runs, line)
                counted[0] = counted[0] + 1
                if line.get("route") == "general":
                    counted[1] = counted[1] + 1
                say("   %s | %s | %s | peak resident: %d kB"
                    % (line.get("route") or "-",
                       AP.setter_label(line),
                       the_verdict_line(line),
                       check_memory("run %d" % index)))
                continue
            continue
        return

    _answer, ran_long, seconds = under_the_clock(RUN_SECONDS,
                                                 walk_the_pair)
    if ran_long:
        say("   THE RUN RAN LONG: %s %s %s -> %s took %.0f s, the bound "
            "this pass states being %d s; every solver in it was "
            "interrupted from there on and %d store line(s) of it are "
            "on the store"
            % (asked[0], asked[1], asked[2], lang, seconds,
               RUN_SECONDS, counted[0] - ran))
        cause = ("the run passed the seconds this pass allows one "
                 "(cell, target) and its solvers were interrupted")
        declines[cause] = declines.get(cause, 0) + 1
    return counted[0], counted[1]


def tally_the_declines(record, declines):
    made = record.get("general")
    if not made:
        return declines
    for place in made.get("places") or []:
        if place.get("rendered"):
            continue
        cause = place.get("refusal_cause") or "no cause"
        declines[cause] = declines.get(cause, 0) + 1
        continue
    return declines


def write_declines(declines, ran, tiers, seconds):
    document = {
        "meta": {
            "what": "task t4's pass: every (cell, target) the bank "
                    "certifies no proof for, through the native route "
                    "and the general tier under both policies",
            "store_lines": ran,
            "general_tier_runs": tiers,
            "seconds": seconds,
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "equality_ceiling_ms": EQUALITY_CEILING_MS,
            "statement_ceiling": RG.STATEMENT_CEILING,
            "policies": list(POLICIES),
        },
        "declined_by_cause": declines,
    }
    handle = open(AGGREGATE, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


# ==================================================================
# section 4: the commands
# ==================================================================

def preflight_command():
    AP = configure_pass()
    plan = AP.the_delta()
    say("the bank: %s" % __import__("bank").BANK)
    say("the outer set: %s" % AP.CELLS)
    say("the targets: %s" % ", ".join(AP.TARGETS))
    say("")
    say("| what | count |")
    say("|---|---|")
    say("| (cell, target, written place, setter) keys the bank "
        "certifies | %d |" % plan["certified_before"])
    say("| keys with no such certificate, which this pass attempts | "
        "%d |" % plan["attempt_triples"])
    say("| of them, held back because the machinery has not moved | %d |"
        % plan["held_by_version"])
    say("| the (cell, target) runs this pass executes | %d |"
        % plan["runs_to_execute"])
    say("")
    say("| target | the word, off its own renderer table |")
    say("|---|---|")
    for lang in AP.TARGETS:
        say("| %s | %d |" % (lang, word_of(lang)))
        continue
    say("")
    say("the construction proofs on record: %d rows" % len(proof_table()))
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


STOP_FILE = os.path.join(HERE, "STOP_THE_PASS")
"""a file whose PRESENCE makes `run` do nothing and say so.

WHY IT EXISTS.  A lane already running cannot be told anything except
through the files it reads, and this task's pass lane runs the pass in a
loop that stops when an attempt adds no store line.  When a bound is
re-stated from the pass's own measurements -- as the gate's was, from
120 s to 30 s -- the lane running under the old bound has to be able to
stop without being ABORTED and without its store being touched.  The
file is this task's own artifact; it is written and removed by a lane,
never by hand on the tower."""


def run_command(limit):
    if os.path.exists(STOP_FILE):
        say("the pass is stopped by %s" % STOP_FILE)
        handle = open(STOP_FILE)
        say(handle.read().strip())
        handle.close()
        return 0
    AP = configure_pass()
    runs, _src = store_paths()
    plan = AP.the_delta()
    say("keys with no proof: %d over %d run(s)"
        % (plan["attempt_triples"], plan["attempt_pairs"]))
    say("runs to execute: %d" % plan["runs_to_execute"])
    done = AP.already_recorded(runs)
    say("runs already on %s: %d" % (runs, len(done)))
    say("")
    return walk(plan["runs_list"], runs, done, limit)


def bank_command():
    configure_pass()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r" % PASS_LABEL)
    return BK.main(["build"])


def readings_command():
    configure_pass()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r" % PASS_LABEL)
    return BK.main(["readings"])


def tier_command(mnem, shape, width, lang):
    """ONE (cell, target) through the native route and the general tier,
    printed.  The walkthrough command; it writes no store line."""
    AP = configure_pass()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    asked = (mnem, shape, int(width))
    say("the word for %s: %d bits" % (lang, word_of(lang)))
    for held in H.cell_inputs(cells, asked):
        # THE TWO ROUTES ARE RUN AND REPORTED SEPARATELY HERE, with the
        # resident reading between them, so a run the operating system
        # stops says WHICH route it was in.  `find_emulation` is the
        # same two calls in the same order.
        say("resident before the native route: %d kB" % RG.resident_kb())
        record = H.the_native_route(shared, held, lang)
        say("resident after the native route: %d kB" % RG.resident_kb())
        made = general_tier(shared, held, lang, record)
        record["general"] = made
        say("resident after the general tier: %d kB" % RG.resident_kb())
        say("")
        say("setter: %s" % AP.setter_label(record))
        say("| route | place | rendered | compiled | gate | statements "
            "| constructed | landing | instructions |")
        say("|---|---|---|---|---|---|---|---|---|")
        for place in record.get("places") or []:
            check = place.get("check") or {}
            say("| native | %s | %s | %s | %s | -- | -- | %s | %d |"
                % (place.get("writes"), place.get("rendered"),
                   place.get("compiled"),
                   check.get("outcome") or place.get("refusal_cause"),
                   (place.get("landing") or {}).get("verdict"),
                   len((place.get("body_text") or "").split(";"))))
            continue
        if made is None:
            say("the general tier: declined for every place")
            continue
        for place in made.get("places") or []:
            for attempt in place.get("attempts") or []:
                check = attempt.get("check") or {}
                gate = attempt.get("gate_on_the_written_term") or {}
                kinds = attempt.get("constructed_kinds") or {}
                say("| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                    % (attempt.get("policy"), place.get("writes"),
                       attempt.get("rendered"), attempt.get("compiled"),
                       check.get("outcome") or gate.get("outcome")
                       or (attempt.get("refusal_cause") or "")[:70],
                       attempt.get("statements"),
                       ", ".join(sorted(kinds)) or "--",
                       (attempt.get("landing") or {}).get("verdict"),
                       attempt.get("instructions")))
                continue
            continue
        say("")
        say("the carved bodies, LITERAL:")
        for place in made.get("places") or []:
            for attempt in place.get("attempts") or []:
                if attempt.get("body_text") is None:
                    say("   %s / %s: %s"
                        % (place.get("writes"), attempt.get("policy"),
                           (attempt.get("refusal_cause") or "-")[:150]))
                    if attempt.get("compiled") is False:
                        say("      THE COMPILE REFUSED, LITERAL: %s"
                            % (attempt.get("compile_refusal") or "-"))
                        say("      the source written: %s"
                            % attempt.get("source_path"))
                        continue
                    continue
                say("   %s / %s: %s"
                    % (place.get("writes"), attempt.get("policy"),
                       attempt.get("body_text")))
                equality = attempt.get("equality") or {}
                say("      statements %s; native nodes %s; constructed "
                    "nodes %s; equality %s by %s"
                    % (attempt.get("statements"),
                       attempt.get("native_nodes"),
                       attempt.get("constructed_nodes"),
                       equality.get("outcome"), equality.get("proof")))
                continue
            continue
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def probe_command(mnem, shape, width, lang, stage):
    """ONE (cell, target) taken through the tier's stages ONE AT A TIME,
    with the resident reading and the size after each.

    THE WALKTHROUGH THAT LOCATES A COST.  `tier` runs render, compile,
    carve and gate as one call and a run the operating system stops
    says nothing about which of the four it was in; this command stops
    where it is told to and prints what it built."""
    AP = configure_pass()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    asked = (mnem, shape, int(width))
    word = word_of(lang)
    say("the word for %s: %d bits; the stage: %s" % (lang, word, stage))
    for held in H.cell_inputs(cells, asked):
        for place in held.get("places") or []:
            working = place
            if place.get("halved") is None:
                projected = H.projected_lane(shared, place,
                                             held["key_width"])
                if projected is not None:
                    if projected.get("refusal_cause") is not None:
                        say("  %s: not rendered upstream: %s"
                            % (place.get("writes"),
                               projected["refusal_cause"]))
                        continue
                    working = projected["place"]
            if working.get("term") is None:
                say("  %s: the place carries no term"
                    % place.get("writes"))
                continue
            say("")
            say("  place %s, %s bits" % (place.get("writes"),
                                         working.get("bits")))
            say("    the cell's term: %d distinct nodes"
                % B.node_count(working["term"]))
            for policy in POLICIES:
                one_probe(held, lang, working, place, word, policy,
                          stage)
                continue
            continue
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def one_probe(held, lang, working, place, word, policy, stage):
    import emulate as E
    import handful as H
    label = E.sanitize("%s_%s_%d__%s__%s__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          place["writes"].replace(".", "_"), lang,
                          policy))
    ordered = H.renderer_input(working["term"])
    home = working["home"]
    if E.is_an_x87_arrival(home.get("family")):
        if lang not in H.TARGETS_WITH_AN_80_BIT_HOLDER:
            say("    %s: %s" % (policy, CAUSE_NO_80_BIT_HOLDER % lang))
            return
        ordered = H.the_x87_value(ordered)
    started = time.time()
    try:
        made = RG.render(ordered, lang, working["families"],
                         home["family"], working["bits"], label, word,
                         policy, working.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        say("    %s: the render refused: %s: %s"
            % (policy, type(problem).__name__,
               ("%s" % problem)[:200]))
        return
    say("    %s: rendered %d statements (%d before the dead were "
        "dropped), %d native nodes, %d constructed nodes, in %.1f s; "
        "resident %d kB"
        % (policy, made["statements"],
           made["statements_before_the_dead_were_dropped"],
           made["native_nodes"], made["constructed_nodes"],
           time.time() - started, RG.resident_kb()))
    say("      the term the render wrote: %d distinct nodes"
        % B.node_count(made["written_term"]))
    say("      the source: %d bytes, %d lines"
        % (len(made["source"]), made["source"].count("\n") + 1))
    if stage == "render":
        return
    started = time.time()
    got, refusal = H.compile_one_place(made["source"], made["symbol"],
                                       lang)
    if got is None:
        say("      the compile refused, LITERAL: %s"
            % ("%s" % refusal)[:400])
        return
    raw_bytes, mnemonics = got
    say("      compiled and carved: %d instructions in %.1f s; "
        "resident %d kB"
        % (len(mnemonics), time.time() - started, RG.resident_kb()))
    if stage == "compile":
        return
    started = time.time()
    posed = dict(working)
    written = made.get("written_term")
    if written is not None:
        posed["term"] = written
    check = H.check_one_place(shared_holder(), posed, made["params"],
                              raw_bytes, mnemonics, label, lang,
                              answer_bits=held.get("key_width"),
                              attested=H.attested_of(held, None))
    say("      the gate: %s in %.1f s; resident %d kB"
        % (check.get("outcome"), time.time() - started,
           RG.resident_kb()))
    return


SHARED = None


def shared_holder():
    global SHARED
    if SHARED is None:
        import handful as H
        SHARED = H.build_shared()
    return SHARED


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    what = argv[1]
    if what == "preflight":
        return preflight_command()
    if what == "run":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return run_command(limit)
    if what == "bank":
        return bank_command()
    if what == "readings":
        return readings_command()
    if what == "report":
        import general_report as GRP
        return GRP.main(argv[1:])
    if what == "tier":
        return tier_command(argv[2], argv[3], argv[4], argv[5])
    if what == "probe":
        stage = argv[6] if len(argv) > 6 else "render"
        return probe_command(argv[2], argv[3], argv[4], argv[5], stage)
    say("unknown command %r" % what)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
