#!/usr/bin/env python3
"""bb2_run.py -- THE BIT-BLAST ROUTE OVER EVERY ATTESTED x86 CELL: task
t4's x86 pass with ONE thing swapped, the render; and the same circuit
rendered in the seven interpreted languages and run beside the
definition at points.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly, and the
x86_64 architecture node beside it.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_bb2_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.

WHAT THIS FILE IS, one sentence, in relation: `general.py` -- task t4's
x86 pass, with its population, its arrival contract, its bank delta and
its readings -- with `general.one_attempt` replaced by one that asks
`bitblast.blast` for the circuit and `bitblast.render_gates` for the
source, exactly as `bb1_run.py` replaced `rv_general.one_attempt` on
RISC-V.  Nothing of the pass is copied: the driver, the native route,
the compile at ship flags, the carve, the walk through the reference,
the gate, the store and the bank registration are `general.py`'s and
`autopoly.py`'s own and are CALLED.

WHAT IS THE SAME AS TASK t4, and this is what lets the counts stand
side by side: the population is `autopoly5_cells.json`'s 253 attested
cells, every written place of each -- the term's own places and the
flags places the bank tracks -- the five compiled targets are c, cpp,
rust, go and swift, the gate is `handful.check_one_place` at the
pipeline's own 3,000 ms with task t4's 5-second bound on how many
solver calls one place may ask, and the gate is offered 4,000 carved
instructions and no more.

WHAT IS DIFFERENT, and there are four things.
  1. There is ONE route rather than two, so `POLICIES` is the single
     name `bit_blast`; the source is a circuit of gates and not a term
     printed in the language's own operators.
  2. THE TIER IS OFFERED EVERY PLACE, including the places the native
     route proved.  Task t4's tier declined those ("the native route
     proved this place, so there is nothing the general tier can add"),
     which is right for a tier that exists to catch what the route
     misses and wrong for a THIRD ROUTE whose own count over the whole
     population is the measurement.  It is done by handing
     `general.general_tier` a native record with no places, which is
     `general.one_place`'s own rule read at an empty record -- not by
     copying that function.
  3. THE POPULATION IS THE WHOLE OUTER SET, not the bank's delta, for
     the same reason: a route is measured over every cell or its column
     is not comparable with the other two.  The bank's OWN delta is
     still computed and printed beside it, and because this pass
     re-derives every certified key by an independent route, the pass
     is also a 100% audit of the bank on this architecture -- every
     place where the bank says proved and this route says DISPROVED is
     an ALARM and is reported.
  4. The store carries, per attempt, the gate count, the source line
     count, the compile seconds, the carved body's instruction count
     and the check's outcome and seconds -- the brief's own section 4.

THE INTERPRETED SEVEN.  No machine body exists for an interpreted
target, so there is no carve and no gate and the route is AGREEMENT:
the same circuit is written as source in the target's own value model
and run beside the definition at the sample `interp_check.SAMPLE_RULE`
states (edge values first, at most 20,000 points), and the outcome is
`agreed`, never `proved`.  The loop is `interp_check.one_run`, CALLED,
with `interp_render.InterpRenderer` replaced by `GateRenderer` below --
the same swap, at the same seam.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.  One
process, no pool.

Coding discipline: no compound one-liner statements.

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

HOW THIS FILE OBEYS IT.  The population is the cells file's own list,
each a (`mnem`, operand shape, `key_width`) triple; every row of every
table below is keyed on that triple and on the target, and the mnemonic
rides in the field `mnem`, which the ruling of 2026-09-08 states is
machine form.  What a node becomes is z3's declaration kind on the
blasted boolean and nothing else.  Nothing here reads a source token.

usage:
  bb2_run.py sizes                  the gates of every place, nothing
                                    compiled and nothing gated
  bb2_run.py sample <n>             the n largest circuits taken all the
                                    way through on every target, with
                                    the sizes and the seconds
  bb2_run.py cell <mnem> <shape> <width> [<lang> ...]
                                    one cell through this route, printed
  bb2_run.py preflight              what the pass would attempt
  bb2_run.py run [<limit>]          the pass
  bb2_run.py table                  the three routes, and this route's
                                    own outcomes and causes
  bb2_run.py largest [<n>]          the n largest cells' own rows
  bb2_run.py rows                   one line per attempt
  bb2_run.py bank                   the bank rebuilt with this pass in
  bb2_run.py readings               the three readings with this pass in
  bb2_run.py bank_before            the bank rebuilt without this pass
  bb2_run.py readings_before        the three readings without it
  bb2_run.py alarms                 every place the bank certifies and
                                    this route disproves
  bb2_run.py interp [<limit>]       the interpreted seven by agreement
  bb2_run.py interp_sizes            the work every interpreted run
                                    would ask for, nothing written
  bb2_run.py interp_one <mnem> <shape> <width> <lang>
                                    one interpreted run, printed
  bb2_run.py interp_retry [<limit>] every interpreted timeout once more
  bb2_run.py interp_table           the interpreted counts, of 253
  bb2_run.py swift_riscv            the probe for a swift riscv64 SDK
"""

import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import general as GEN                                            # noqa: E402
import bitblast as BB                                            # noqa: E402
import build as B                                                # noqa: E402

EMULATION = GEN.EMULATION
AUTOPOLY = GEN.AUTOPOLY
INTERP = os.path.join(EMULATION, "interp")
sys.path.insert(0, INTERP)

PASS_LABEL = "bb2_bit_blast"
INTERP_PASS_LABEL = "bb2_interp"
ABORT_NAME = "ABORT_MEMORY_BB2"

SIZES = os.path.join(HERE, "bb2_sizes.json")
AGGREGATE = os.path.join(HERE, "bb2.json")
REPORT = os.path.join(HERE, "bb2.md")

INTERP_RUNS = os.path.join(AUTOPOLY, "%s_runs.jsonl" % INTERP_PASS_LABEL)
INTERP_RETRY_RUNS = os.path.join(AUTOPOLY,
                                 "%s_runs_retry600.jsonl"
                                 % INTERP_PASS_LABEL)
INTERP_SRC = os.path.join(INTERP, "src_bb2")
INTERP_AGGREGATE = os.path.join(HERE, "bb2_interp.json")

SOURCE_KEPT_LINES = 2000
"""how long a rendered source may be and still be written beside the
store.  The reason is task bb1's, measured there and unchanged: a
blasted divide is about fourteen thousand gates, so its source is about
fourteen thousand lines, and this pass writes about six thousand of
them.  The CARVED BODY's instruction count is on every row at every
size, and its TEXT under the ceiling below."""

BODY_TEXT_CEILING = 20000
"""how many instructions of a carved body are kept AS TEXT on the store
line.  THE COUNT IS ALWAYS EXACT AND IS NEVER BOUNDED; this bounds the
transcript and nothing else.  The number is task bb1's and for its own
reason: it is five times the 4,000 instructions the gate is offered, so
every body that was gated is kept whole with a margin of four times
over, and a body above it was NOT_GATED by definition."""

INTERP_WORK_CEILING = 200000000
"""how many GATE EVALUATIONS one interpreted run may ask for: the
circuit's gate count times the sample's point count.

IT IS A BOUND ON WHAT IS RUN AND NEVER ON WHAT IS MEASURED.  The sample
is `interp_check`'s own, unchanged, edge values first; a circuit whose
work is above this ceiling is recorded with its gate count and its
point count on the row, exactly as a carved body above 4,000
instructions is recorded NOT_GATED with its size.

THE NUMBER IS MEASURED, in lane `bb2_l5`: `sbb gpr_same 64` is 695
gates over 19,683 sample points -- 13,679,685 gate evaluations -- and
the whole run, the interpreter's start-up included, took 2.4 s on
cpython, 2.3 s on php and 2.3 s on ruby.  That is about six million
gate evaluations a second on the three unbounded dialects, so two
hundred million is about thirty-three seconds, inside the sixty
`interp_check` is handed on the first pass and far inside the six
hundred of the retry.  Lane `bb2_l4` counts the population against it:
of the 176 cells whose destination place blasts, 174 are under it and
2 are over -- `idiv gpr_one 32` at 1,466,442,549 and `div gpr_one 32`
at 1,093,390,650."""

INTERP_TIMEOUT_FIRST = 60
INTERP_TIMEOUT_RETRY = 600
"""task ex2's own two bounds, unchanged, so the counts stand beside
its."""

THE_STATEMENT_SHAPE = {"installed": False, "assemble": None}
"""THE ONE THING THIS TASK HAD TO WORK AROUND, and it is named here
rather than hidden.

`bitblast.render_gates` hands `render_general.assemble` a list of
`(name, line)` pairs, which is what that function took when task bb1
wrote the route.  Task rd1, running beside this task, has changed
`assemble`'s own contract: its `statements` are now `(depth, line)`,
the depth being how many conditionals written as control flow the line
sits inside, and the first element is USED.  A `(name, line)` pair
therefore reaches `"    " * (depth + 1)` with a string where an integer
belongs, and lane `bb2_l2` recorded `the gate render refused` on all
sixty of its attempts, at every size and on every target, including a
place whose circuit is zero gates.  The literal is in lane `bb2_l3`.

`render_general.py` is task rd1's file and this task does not touch it.
The adapter below is installed on THIS side of the call and rewrites
every statement to `(0, line)` -- a circuit is flat and sits inside no
conditional, so its depth is zero.  IT IS CORRECT UNDER BOTH
CONTRACTS: the old `assemble` binds the first element to a name it
ignores, and the new one binds it to the depth, which is what 0 is.
Nothing of `bitblast.py`'s own behaviour changes."""

THE_LAST_BLAST = {"key": None, "circuit": None, "refusal": None}
"""the circuit of the (cell, place) the driver is on, kept for the five
targets that follow it.  THE BLAST DOES NOT DEPEND ON THE LANGUAGE --
the gates are z3's, over the term's bits -- and the driver's own loop
runs the five targets of one place one after another, so one entry is
the whole saving and nothing accumulates."""


def install_the_statement_shape():
    """`render_general.assemble` wrapped so the statements reaching it
    carry the depth its current contract asks for.  See
    `THE_STATEMENT_SHAPE` above for what was measured and why."""
    import render_general as RG
    if THE_STATEMENT_SHAPE["installed"]:
        return
    THE_STATEMENT_SHAPE["assemble"] = RG.assemble
    original = RG.assemble

    def assemble(lang, renderer, label, return_type, statements,
                 answer_lines, body, text):
        flat = []
        for entry in statements:
            flat.append((0, entry[1]))
            continue
        return original(lang, renderer, label, return_type, flat,
                        answer_lines, body, text)

    RG.assemble = assemble
    THE_STATEMENT_SHAPE["installed"] = True
    return


install_the_statement_shape()


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def quantiles(values):
    """(count, smallest, median, mean, largest) of a list of numbers."""
    kept = []
    for value in values:
        if value is None:
            continue
        kept.append(value)
        continue
    if not kept:
        return (0, None, None, None, None)
    kept.sort()
    middle = kept[len(kept) // 2]
    mean = sum(kept) / float(len(kept))
    return (len(kept), kept[0], middle, round(mean, 3), kept[-1])


def read_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        rows.append(json.loads(text))
        continue
    handle.close()
    return rows


# ==================================================================
# section 1: the swap -- one place, one target, by the bit-blast route
# ==================================================================

def the_circuit(ordered):
    """(the circuit, the refusal text) for one place's term, blasted
    once and kept for the targets that follow.

    THE KEY IS THE z3 NODE's OWN IDENTITY, which is machine form and is
    not a reading of any name: z3 hash-conses its abstract syntax, so
    two structurally identical terms are one node with one id."""
    key = ordered.get_id()
    if THE_LAST_BLAST["key"] == key:
        return THE_LAST_BLAST["circuit"], THE_LAST_BLAST["refusal"]
    circuit = None
    refusal = None
    try:
        circuit = BB.blast(ordered)
    except B.Refused as problem:
        refusal = "%s: %s" % (problem.cause, problem.detail)
    except Exception as problem:                              # noqa: BLE001
        refusal = "%s: %s" % (type(problem).__name__,
                              ("%s" % problem)[:300])
    THE_LAST_BLAST["key"] = key
    THE_LAST_BLAST["circuit"] = circuit
    THE_LAST_BLAST["refusal"] = refusal
    return circuit, refusal


def the_body_text(body):
    """the carved body as the store keeps it: the whole text under this
    file's stated ceiling, and above it the first and last two hundred
    instructions with ONE LINE BETWEEN THEM saying, in the list itself,
    what is not there and how to get it.  The row's `instructions`
    count is always the whole body's."""
    if len(body) <= BODY_TEXT_CEILING:
        return "; ".join(body)
    elided = len(body) - 400
    middle = ("... %d instructions of this body are not kept as text: "
              "the store's own ceiling is %d instructions and this body "
              "is %d, which is above the %d the gate is offered and so "
              "was never posed.  Re-derive the whole body by running "
              "bb2_run.py over this one cell."
              % (elided, BODY_TEXT_CEILING, len(body),
                 GEN.GATE_INSTRUCTION_CEILING))
    kept = list(body[:200]) + [middle] + list(body[-200:])
    return "; ".join(kept)


def keep_source(label, lang, source):
    """the rendered source written beside the store, under the line
    bound this file states.  Returns the path the store records, or
    None where the source was above the bound."""
    import handful as H
    folder = GEN.SRC_DIR
    if folder is None:
        return None
    if source.count("\n") + 1 > SOURCE_KEPT_LINES:
        return None
    if not os.path.isdir(folder):
        os.makedirs(folder)
    name = label + H.suffix_of(lang)
    handle = open(os.path.join(folder, name), "w")
    handle.write(source)
    handle.close()
    return os.path.join(os.path.basename(folder), name)


def one_attempt(shared, held, lang, working, place, word, policy,
                index):
    """`general.one_attempt` with the render swapped.  Everything after
    the source -- the compile at ship flags, the carve, the walk
    through the reference, the arrival contract, the solver budget and
    the instruction ceiling -- is `general.py`'s and `handful.py`'s own
    and is called.

    THERE IS ONE OBLIGATION HERE AND NOT TWO.  Task t4's tier renders a
    term of its own and must then prove that term is the CELL's; this
    route poses the gate on the CELL's OWN TERM -- the circuit is z3's
    blast of it and the carved body is compared to the cell's term
    itself -- so the equality is discharged by the question asked, and
    the row says so in those words rather than claiming a second
    proof."""
    import emulate as E
    import handful as H
    out = {"policy": policy}
    writes = place["writes"].replace(".", "_").replace("-", "_")
    label = E.sanitize("%s_%s_%d__%s__%s__%s"
                       % (held["mnem"], held["shape"], held["key_width"],
                          writes, lang, policy))
    out["label"] = label
    term = working["term"]
    ordered = H.renderer_input(term)
    home = working["home"]
    if E.is_an_x87_arrival(home.get("family")):
        if lang not in H.TARGETS_WITH_AN_80_BIT_HOLDER:
            out["rendered"] = False
            out["refusal_cause"] = GEN.CAUSE_NO_80_BIT_HOLDER % lang
            return out
        ordered = H.the_x87_value(ordered)

    circuit, refusal = the_circuit(ordered)
    if circuit is None:
        out["blasted"] = False
        out["rendered"] = False
        out["refusal_cause"] = "the blast refused"
        out["refusal_detail"] = refusal
        return out
    out["blasted"] = True
    out["gates"] = len(circuit.gates)
    out["input_bits"] = len(circuit.inputs)
    out["blast_seconds"] = circuit.seconds
    out["blast_shape"] = circuit.shape

    started = time.time()
    try:
        made = BB.render_gates(circuit, lang, working["families"],
                               home["family"], working["bits"], label,
                               working.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        import traceback
        out["rendered"] = False
        out["refusal_cause"] = "the gate render refused"
        out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                            ("%s" % problem)[:300])
        frames = traceback.extract_tb(sys.exc_info()[2])
        if frames:
            last = frames[-1]
            out["refusal_frame"] = ("%s:%d in %s: %s"
                                    % (os.path.basename(last.filename),
                                       last.lineno, last.name,
                                       last.line))
            out["refusal_detail"] = ("%s   [%s]"
                                     % (out["refusal_detail"],
                                        out["refusal_frame"]))
        return out
    out["rendered"] = True
    out["render_seconds"] = round(time.time() - started, 3)
    out["symbol"] = made["symbol"]
    out["statements"] = made["statements"]
    out["source_lines"] = made["source_lines"]
    out["source_path"] = keep_source(label, lang, made["source"])

    started = time.time()
    try:
        got, compile_refusal = H.compile_one_place(made["source"],
                                                   made["symbol"], lang)
    except Exception as problem:                              # noqa: BLE001
        # THE COMPILE ITSELF CAN RUN OUT, and on this route it does:
        # every target's own compile route bounds its build (swift at
        # 600 s, go at 600 s, c and cpp at 180 s) and raises where the
        # bound fires, and a gate source of seventy thousand lines is
        # exactly the size that reaches it.  The bound firing is a ROW
        # WITH A CAUSE -- the source, its line count and the seconds
        # are all on it -- and never a run this pass loses.
        got = None
        compile_refusal = "%s: %s" % (type(problem).__name__,
                                      ("%s" % problem)[:300])
    out["compile_seconds"] = round(time.time() - started, 3)
    if got is None:
        out["compiled"] = False
        out["compile_refusal"] = the_diagnostic(compile_refusal)
        out["refusal_cause"] = "the compiler refused"
        out["refusal_detail"] = out["compile_refusal"]
        return out
    out["compiled"] = True
    raw_bytes, mnem = got
    out["instructions"] = len(mnem)
    out["body_bytes"] = None
    out["body_text"] = the_body_text(mnem)
    out["landing"] = H.landing_of(mnem, held["mnem"])
    out["gate_instruction_ceiling"] = GEN.GATE_INSTRUCTION_CEILING
    if len(mnem) > GEN.GATE_INSTRUCTION_CEILING:
        out["refusal_cause"] = GEN.CAUSE_GATE_TOO_LARGE
        out["refusal_detail"] = ("%d instructions, above the %d this "
                                 "task's gate is offered"
                                 % (len(mnem),
                                    GEN.GATE_INSTRUCTION_CEILING))
        out["not_gated"] = GEN.not_gated(
            GEN.CAUSE_GATE_TOO_LARGE, instructions=len(mnem),
            ceiling=GEN.GATE_INSTRUCTION_CEILING)
        return out
    if len(mnem) <= BODY_TEXT_CEILING:
        out["body_bytes"] = " ".join(raw_bytes)

    check, ran_long, seconds = gate_in_its_own_process(
        shared, working, made["params"], raw_bytes, mnem, label, lang,
        held.get("key_width"), H.attested_of(held, None),
        GATE_WALL_SECONDS)
    out["gate_seconds"] = seconds
    out["check_seconds"] = seconds
    if ran_long:
        out["gate_seconds_allowed"] = GATE_WALL_SECONDS
        out["gate_was_aborted"] = True
        out["refusal_cause"] = CAUSE_GATE_WALL
        out["refusal_detail"] = ("%d instructions, %d s allowed, and "
                                 "the gate's own process was ABORTED"
                                 % (len(mnem), GATE_WALL_SECONDS))
        out["not_gated"] = GEN.not_gated(
            CAUSE_GATE_WALL, instructions=len(mnem),
            seconds_allowed=GATE_WALL_SECONDS)
        return out
    out["check"] = check
    out["equality"] = {
        "proof": "the gate was posed on the cell's own term",
        "outcome": "PROVED",
        "reason": ("the circuit is z3's bit-blast of the CELL's term "
                   "and the carved body is compared to that term "
                   "itself, so there is one obligation and not two"),
    }
    out["proof"] = "the gate was posed on the cell's own term"
    return out


GATE_WALL_SECONDS = 10
"""how long the WHOLE gate call may run, on a wall clock that actually
stops it.

WHY THIS TASK NEEDS ONE WHERE TASK t4 DID NOT.  t4's bound is
`signal.setitimer` calling `z3.main_ctx().interrupt()`, which stops a
SOLVER and nothing else, and t4 measured that the solver is what runs
long on its own route.  On THIS route it is not: lane `bb2_l5` took
more than eight minutes on `add gpr_gpr 32` on c -- a 461-gate circuit
carving to a few hundred instructions -- at 100% processor and 82 MB
resident, with the interrupt firing every five seconds and reaching
nothing, because the time is spent in the LIFT (the carved body put on
the canonical form and walked through the reference, one term per
instruction) and not inside any solver call.  An interrupt is a no-op
there.

WHY TEN SECONDS, and it is the same shape task t4 measured for its own
bound: the calls that run long do not run a little long.  On this task's
own two ends, `xor gpr_gpr 8` on c -- 24 gates, a body the compiler
collapsed to six instructions -- was gated in 0.007 s, and
`add gpr_gpr 32` on c -- 461 gates, a body the compiler did not collapse
-- had not answered after 1,800 s (lane `bb2_l5`, exit 124).  Ten
seconds is a thousand times the answered end and costs nothing that was
going to be answered; the distribution of gate seconds over the whole
pass is reported so the claim is measured rather than asserted.

SO THE GATE IS ASKED IN A PROCESS OF ITS OWN.  The forked process runs
`handful.check_one_place` -- the gate of record, called and not copied,
with its own arrival contract, its own 3,000 ms solver ceiling and its
own re-poses -- and writes its answer; the process that forked it waits
on a real clock and, where the clock fires, ABORTS it (`SIGKILL`, the
operating system's own spelling) and records the place as NOT GATED
with the seconds and the instruction count on the row.  That is a row
with a named cause, which is what this line asks for, and it is also
why nothing this route does can take the pass down with it."""

CAUSE_GATE_WALL = ("the gate did not come back inside the seconds this "
                   "task allows one gate call on a wall clock that "
                   "stops it: the carved body is on the canonical form "
                   "and the lift had not finished")


def gate_in_its_own_process(shared, working, params, raw_bytes, mnem,
                            label, lang, answer_bits, attested,
                            seconds):
    """(the gate's answer, whether the clock fired, the seconds).

    `handful.check_one_place` is CALLED, in a process of its own, for
    the reason `GATE_WALL_SECONDS` states."""
    import signal
    import tempfile
    import handful as H
    handle, path = tempfile.mkstemp(prefix="bb2_gate_", suffix=".json",
                                    dir=os.environ.get("TMPDIR") or "/tmp")
    os.close(handle)
    started = time.time()
    sys.stdout.flush()
    sys.stderr.flush()
    forked = os.fork()
    if forked == 0:
        answer = None
        try:
            answer = H.check_one_place(shared, working, params,
                                       raw_bytes, mnem, label, lang,
                                       answer_bits=answer_bits,
                                       attested=attested)
        except Exception as problem:                          # noqa: BLE001
            answer = {"outcome": "UNDECIDED",
                      "reason": "the gate raised: %s: %s"
                                % (type(problem).__name__,
                                   ("%s" % problem)[:300])}
        try:
            written = open(path, "w")
            json.dump(answer, written, default=str)
            written.close()
        except Exception:                                     # noqa: BLE001
            pass
        os._exit(0)
    fired = False
    deadline = started + seconds
    while True:
        got, _status = os.waitpid(forked, os.WNOHANG)
        if got == forked:
            break
        if time.time() > deadline:
            fired = True
            os.kill(forked, signal.SIGKILL)
            os.waitpid(forked, 0)
            break
        time.sleep(0.02)
        continue
    elapsed = round(time.time() - started, 3)
    answer = None
    if not fired:
        try:
            read = open(path)
            answer = json.load(read)
            read.close()
        except Exception:                                     # noqa: BLE001
            answer = None
    if os.path.exists(path):
        os.remove(path)
    if answer is None and not fired:
        answer = {"outcome": "UNDECIDED",
                  "reason": ("the gate's own process ended with no "
                             "answer written: the operating system "
                             "stopped it with no language-level error")}
    return answer, fired, elapsed


def the_diagnostic(diagnostic):
    """what the build said, and where it said NOTHING, a sentence saying
    that rather than an empty string.  Task bb1's own finding, and its
    reason: a compiler route that answers with `(stderr or stdout)`
    gives an empty answer exactly where the process was stopped with no
    language-level error."""
    text = ("%s" % (diagnostic or "")).strip()
    if text:
        return text[:600]
    return ("the build refused and the compiler wrote no diagnostic at "
            "all, on neither stream: the case where the process is "
            "stopped with no language-level error")


# ==================================================================
# section 2: the pass -- `general.py` with the render swapped
# ==================================================================

THE_GENERAL_TIER = GEN.general_tier
THE_SPLIT = GEN.split
THE_DELTA = None


def general_tier(shared, held, lang, record):
    """`general.general_tier`, CALLED, with a native record that has no
    places, so no place is declined for having been proved by the
    native route.  See the header, difference 2."""
    made = THE_GENERAL_TIER(shared, held, lang, {"places": []})
    if made is not None:
        made["route"] = "bit_blast"
    return made


def split(record):
    """`general.split`, CALLED, with this route's name on the second
    line."""
    out = THE_SPLIT(record)
    for line in out:
        if line.get("route") == "general":
            line["route"] = "bit_blast"
            continue
        continue
    return out


def every_pair():
    """the population: every attested cell of `autopoly5_cells.json` on
    every one of the five compiled targets, in the cells file's own
    order (attested ledger rows descending) with the targets in
    `autopoly.TARGETS`'s own order inside each cell.  No operator token
    enters this ordering."""
    import autopoly as AP
    cells = AP.read_json(AP.CELLS)
    out = []
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for lang in AP.TARGETS:
            out.append((asked, lang, record["attested_ledger_rows"]))
            continue
        continue
    return out


def the_whole_population():
    """`autopoly.the_delta`, CALLED, with the run list replaced by the
    whole population.  The delta's own counts are kept on the plan under
    their own names and printed by `preflight`, so the bank's delta is
    reported and is simply not what decides which runs happen.  See the
    header, difference 3."""
    plan = THE_DELTA()
    plan["the_bank_delta_runs"] = plan["runs_to_execute"]
    plan["the_bank_delta_triples"] = plan["attempt_triples"]
    order = every_pair()
    plan["runs_list"] = order
    plan["runs_to_execute"] = len(order)
    return plan


def configure():
    """every swap this task makes, in one place, so the diff against
    task t4's pass is one function long."""
    global THE_DELTA
    GEN.PASS_LABEL = PASS_LABEL
    GEN.ABORT_NAME = ABORT_NAME
    GEN.AGGREGATE = AGGREGATE
    GEN.REPORT = REPORT
    GEN.POLICIES = ("bit_blast",)
    GEN.THE_TIER_SOURCES = ("bb2_run.py", "bitblast.py")
    GEN.one_attempt = one_attempt
    GEN.general_tier = general_tier
    GEN.split = split
    AP = GEN.configure_pass()
    if THE_DELTA is None:
        THE_DELTA = AP.the_delta
        AP.the_delta = the_whole_population
    AP.ABORT_NAME = ABORT_NAME
    return AP


def preflight_command():
    AP = configure()
    plan = AP.the_delta()
    say("the bank: %s" % __import__("bank").BANK)
    say("the outer set: %s" % AP.CELLS)
    say("the targets: %s" % ", ".join(AP.TARGETS))
    say("")
    say("| what | count |")
    say("|---|---|")
    say("| (cell, target, written place, setter) keys the bank "
        "certifies | %d |" % plan["certified_before"])
    say("| keys with no such certificate | %d |"
        % plan["the_bank_delta_triples"])
    say("| of them, held back because the machinery has not moved | %d |"
        % plan["held_by_version"])
    say("| the (cell, target) runs the BANK'S DELTA would execute | %d |"
        % plan["the_bank_delta_runs"])
    say("| the (cell, target) runs THIS PASS executes, the whole "
        "population | %d |" % plan["runs_to_execute"])
    say("")
    say("| target | the word, off its own renderer table |")
    say("|---|---|")
    for lang in AP.TARGETS:
        say("| %s | %s |" % (lang, GEN.word_of(lang)))
        continue
    say("")
    say("the store: %s" % GEN.store_paths()[0])
    say("the sources: %s" % GEN.store_paths()[1])
    say("peak resident: %d kB" % GEN.check_memory("preflight"))
    return 0


def run_command(limit):
    configure()
    return GEN.run_command(limit)


def bank_command():
    configure()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r and %r"
        % (PASS_LABEL, INTERP_PASS_LABEL))
    return BK.main(["build"])


def readings_command():
    configure()
    BK = register_with_the_bank()
    say("this pass registered with the bank as %r and %r"
        % (PASS_LABEL, INTERP_PASS_LABEL))
    return BK.main(["readings"])


def bank_before_command():
    """the bank rebuilt with every pass registered EXCEPT this task's
    two: the `before` bank, so `before -> after` is two rebuilds of the
    same machinery and not one rebuild and one recollection."""
    configure()
    BK = register_with_the_bank(mine=False)
    names = []
    for step in BK.PASSES:
        names.append(step["pass"])
        continue
    say("the passes registered for this build: %s" % ", ".join(names))
    return BK.main(["build"])


def readings_before_command():
    """the three readings over the bank AS IT STOOD BEFORE this task:
    every pass registered EXCEPT this task's two.

    IT IS THE `before` OF `before -> after`, and it is derived rather
    than pasted from task t4's log, because `bank.py readings` on its
    own registers neither task t2's pass nor task t4's and so answers
    with a bank two passes short."""
    configure()
    BK = register_with_the_bank(mine=False)
    names = []
    for step in BK.PASSES:
        names.append(step["pass"])
        continue
    say("the passes registered for this reading: %s" % ", ".join(names))
    return BK.main(["readings"])


def register_with_the_bank(mine=True):
    """task t2's pass, task t4's pass, and (where `mine`) this task's
    two, added to the bank's pass table.

    WHY THE OTHERS TOO.  `bank.PASSES` is the file's own list and
    neither the construct tier's pass, nor task t4's, nor these two is
    in it -- each registers itself from outside, which is what task t2's
    own registration says and why.  A rebuild run from HERE with only
    these registered would write a bank with task t4's and task t2's
    proofs missing, which is not a delta but a loss.

    AND TASK t4's IS REGISTERED BY NAME HERE, not through
    `general.register_with_the_bank`.  That function reads
    `general.PASS_LABEL`, which THIS task has already set to its own
    label, so calling it would register this task's store under this
    task's name and leave task t4's 1,926 certificates out of the bank
    entirely -- which lane `bb2_l8` did, and its own Table B3 shows the
    hole (`t4_general` absent, and the backstop column 0 on c, cpp and
    rust).  The entry below is task t4's own, spelled out."""
    import construct as CONS
    CONS.register_with_the_bank()
    import bank as BK
    held = set()
    for step in BK.PASSES:
        held.add(step["pass"])
        continue
    if "t4_general" not in held:
        BK.PASSES.append({
            "pass": "t4_general",
            "store": "t4_general_runs.jsonl",
            "reader": "compiled",
            "src": os.path.join(AUTOPOLY, "src_t4_general"),
            "task": "t4",
            "log": "log_262",
            "targets": list(BK.COMPILED),
            "optional": True,
        })
        held.add("t4_general")
    if not mine:
        return BK
    runs, src = GEN.store_paths()
    if PASS_LABEL not in held:
        BK.PASSES.append({
            "pass": PASS_LABEL,
            "store": os.path.basename(runs),
            "reader": "compiled",
            "src": src,
            "task": "bb2",
            "log": "this task",
            "targets": list(BK.COMPILED),
            "optional": True,
        })
    if INTERP_PASS_LABEL not in held:
        BK.PASSES.append({
            "pass": INTERP_PASS_LABEL,
            "store": os.path.basename(INTERP_RUNS),
            "reader": "interpreted",
            "src": INTERP_SRC,
            "task": "bb2",
            "log": "this task",
            "targets": list(BK.INTERPRETED),
            "optional": True,
        })
    return BK


# ==================================================================
# section 3: the circuit size of every place, before anything is
# compiled
# ==================================================================

def every_place(shared, cells, asked):
    """(held cell, place, working place) for every written place of one
    asked cell, by `general.one_place`'s own two steps and no others."""
    import handful as H
    out = []
    for held in H.cell_inputs(cells, asked):
        for place in held.get("places") or []:
            working = place
            note = None
            if place.get("not_rendered") is not None:
                out.append((held, place, None, place["not_rendered"]))
                continue
            if place.get("halved") is None:
                projected = H.projected_lane(shared, place,
                                             held["key_width"])
                if projected is not None:
                    if projected.get("refusal_cause") is not None:
                        out.append((held, place, None,
                                    projected["refusal_cause"]))
                        continue
                    working = projected["place"]
            if working.get("term") is None:
                note = "the place carries no term"
                out.append((held, place, None, note))
                continue
            out.append((held, place, working, None))
            continue
        continue
    return out


def sizes_command():
    """how many gates z3's blast gives every written place of every
    attested x86 cell, with nothing compiled and nothing gated.  This is
    the cheap half of the task and it is run first, because it is what
    says where the expensive end is."""
    AP = configure()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    rows = []
    started = time.time()
    number = 0
    total = len(cells["asked"])
    for record in cells["asked"]:
        number = number + 1
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for held, place, working, note in every_place(shared, cells,
                                                      asked):
            # THE SETTER IS A RECORD AND NEVER A BARE TUPLE.  A bare
            # (mnem, shape, width) tuple puts the mnemonic in a LIST
            # element, and the guard refuses that by name: lane
            # `bb2_l9` step [7/8] read
            # `$.rows[40].setter[0] -- list element is the bare
            # operator token 'or'` sixty times over.  The ruling of
            # 2026-09-08 is that the mnemonic is machine form when it
            # sits in the field `mnem`, and `autopoly.setter_record`
            # is that record.
            row = {"mnem": asked[0], "shape": asked[1],
                   "key_width": asked[2], "place": place["writes"],
                   "setter": AP.setter_record(
                       AP.setter_key(held.get("setter")))}
            if working is None:
                row["refusal"] = note
                rows.append(row)
                continue
            row["bits"] = working.get("bits")
            ordered = H.renderer_input(working["term"])
            try:
                circuit = BB.blast(ordered)
            except B.Refused as problem:
                row["refusal"] = "%s: %s" % (problem.cause,
                                             problem.detail)
                rows.append(row)
                continue
            except Exception as problem:                      # noqa: BLE001
                row["refusal"] = "%s: %s" % (type(problem).__name__,
                                             ("%s" % problem)[:300])
                rows.append(row)
                continue
            row["gates"] = len(circuit.gates)
            row["input_bits"] = len(circuit.inputs)
            row["blast_seconds"] = circuit.seconds
            row["blast_shape"] = circuit.shape
            rows.append(row)
            continue
        if number % 25 == 0:
            say("   [%d/%d] cells blasted, %.0f s; peak resident %d kB"
                % (number, total, time.time() - started,
                   GEN.check_memory("sizes")))
        continue
    document = {
        "meta": {
            "task": "bb2",
            "what": "how many gates z3's own bit-blast tactic gives "
                    "every written place of every attested x86 cell "
                    "of autopoly5_cells.json, with nothing compiled "
                    "and nothing gated",
            "seconds": round(time.time() - started, 1),
            "cells": total,
            "places": len(rows),
        },
        "rows": rows,
    }
    handle = open(SIZES, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("")
    say("wrote %s: %d places of %d cells in %.0f s"
        % (SIZES, len(rows), total, time.time() - started))
    sizes_tables(rows)
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


def sizes_tables(rows):
    gates = []
    seconds = []
    refused = []
    for row in rows:
        if row.get("gates") is None:
            refused.append(row)
            continue
        gates.append(row["gates"])
        seconds.append(row.get("blast_seconds"))
        continue
    say("")
    say("| what | places | smallest | median | mean | largest |")
    say("|---|---|---|---|---|---|")
    count, low, middle, mean, high = quantiles(gates)
    say("| gates per definition | %d | %s | %s | %s | %s |"
        % (count, low, middle, mean, high))
    count, low, middle, mean, high = quantiles(seconds)
    say("| blast seconds | %d | %s | %s | %s | %s |"
        % (count, low, middle, mean, high))
    say("")
    bands = [(0, 100), (100, 1000), (1000, 4000), (4000, 10000),
             (10000, 50000), (50000, 10 ** 9)]
    say("| gates | places |")
    say("|---|---|")
    for low, high in bands:
        many = 0
        for value in gates:
            if value >= low and value < high:
                many = many + 1
            continue
        say("| %d to %d | %d |" % (low, high, many))
        continue
    say("")
    say("THE TWENTY LARGEST CIRCUITS")
    say("| mnem | shape | width | place | gates | input bits | blast s |")
    say("|---|---|---|---|---|---|---|")
    ranked = sorted([r for r in rows if r.get("gates") is not None],
                    key=lambda r: -r["gates"])
    for row in ranked[:20]:
        say("| `%s` | `%s` | %s | %s | %d | %d | %s |"
            % (row["mnem"], row["shape"], row["key_width"],
               row["place"], row["gates"], row["input_bits"],
               row.get("blast_seconds")))
        continue
    say("")
    say("THE PLACES THE BLAST REFUSED OR THE DRIVER DID NOT REACH: %d"
        % len(refused))
    held = {}
    for row in refused:
        cause = " ".join(("%s" % (row.get("refusal") or "")).split())[:150]
        held[cause] = held.get(cause, 0) + 1
        continue
    say("| cause, LITERAL | places |")
    say("|---|---|")
    for cause in sorted(held, key=lambda one: -held[one]):
        say("| %s | %d |" % (cause.replace("|", "/"), held[cause]))
        continue
    say("")
    return


def largest_cells(many):
    """the `many` cells whose largest place has the most gates, read off
    this task's own sizes file.  The ordering key is the number of
    GATES -- machine-form evidence, measured -- and not a reading of any
    name."""
    document = json.load(open(SIZES))
    biggest = {}
    for row in document["rows"]:
        key = (row["mnem"], row["shape"], row["key_width"])
        gates = row.get("gates")
        if gates is None:
            continue
        if gates > biggest.get(key, -1):
            biggest[key] = gates
        continue
    ranked = sorted(biggest, key=lambda k: -biggest[k])
    return [(key, biggest[key]) for key in ranked[:many]]


def cell_command(mnem, shape, width, langs):
    """ONE (cell) through this route on the targets named, printed: the
    walkthrough command, and the one that MEASURES a compile's cost at a
    stated circuit size.  It writes no store line."""
    AP = configure()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    asked = (mnem, shape, int(width))
    wanted = langs or AP.TARGETS
    say("| mnem | shape | width | place | language | gates | source "
        "lines | render s | compile s | body instructions | outcome | "
        "check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    number = 0
    for held, place, working, note in every_place(shared, cells, asked):
        if working is None:
            say("| `%s` | `%s` | %s | %s | -- | -- | -- | -- | -- | -- "
                "| %s | -- |"
                % (mnem, shape, width, place["writes"],
                   " ".join(("%s" % note).split())[:80]))
            continue
        for lang in wanted:
            number = number + 1
            attempt = one_attempt(shared, held, lang, working, place,
                                  GEN.word_of(lang), "bit_blast",
                                  number)
            check = attempt.get("check") or {}
            outcome = check.get("outcome")
            if outcome is None:
                outcome = attempt.get("refusal_cause") or "no verdict"
            say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s "
                "| %s | %s |"
                % (mnem, shape, width, place["writes"], lang,
                   attempt.get("gates"), attempt.get("source_lines"),
                   attempt.get("render_seconds"),
                   attempt.get("compile_seconds"),
                   attempt.get("instructions"),
                   " ".join(("%s" % outcome).split())[:80],
                   attempt.get("check_seconds")))
            if attempt.get("refusal_detail"):
                say("      detail, LITERAL: %s"
                    % ("%s" % attempt["refusal_detail"])[:400])
            if attempt.get("compile_refusal"):
                say("      the compile refused, LITERAL: %s"
                    % ("%s" % attempt["compile_refusal"])[:400])
            continue
        continue
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


def sample_command(many):
    """the `many` largest circuits of the population taken all the way
    through on every one of the five compiled targets: the sizes, the
    seconds and the outcome, with nothing written to the pass's own
    store."""
    AP = configure()
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    shared = H.build_shared()
    cells = AP.read_json(AP.CELLS)
    chosen = largest_cells(many)
    say("the sample: the %d cells with the largest circuits, off %s"
        % (len(chosen), os.path.basename(SIZES)))
    for key, gates in chosen:
        say("   `%s` `%s` %s -- largest place %d gates"
            % (key[0], key[1], key[2], gates))
        continue
    say("")
    say("| mnem | shape | width | place | language | gates | source "
        "lines | render s | compile s | body instructions | outcome | "
        "check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    number = 0
    started = time.time()
    for key, _gates in chosen:
        asked = (key[0], key[1], key[2])
        for held, place, working, note in every_place(shared, cells,
                                                      asked):
            if working is None:
                say("| `%s` | `%s` | %s | %s | -- | -- | -- | -- | -- "
                    "| -- | %s | -- |"
                    % (key[0], key[1], key[2], place["writes"],
                       " ".join(("%s" % note).split())[:80]))
                continue
            for lang in AP.TARGETS:
                number = number + 1
                attempt = one_attempt(shared, held, lang, working,
                                      place, GEN.word_of(lang),
                                      "bit_blast", number)
                check = attempt.get("check") or {}
                outcome = check.get("outcome")
                if outcome is None:
                    outcome = attempt.get("refusal_cause") or "no verdict"
                say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s "
                    "| %s | %s | %s |"
                    % (key[0], key[1], key[2], place["writes"], lang,
                       attempt.get("gates"), attempt.get("source_lines"),
                       attempt.get("render_seconds"),
                       attempt.get("compile_seconds"),
                       attempt.get("instructions"),
                       " ".join(("%s" % outcome).split())[:80],
                       attempt.get("check_seconds")))
                if attempt.get("refusal_detail"):
                    say("      detail, LITERAL: %s"
                        % ("%s" % attempt["refusal_detail"])[:500])
                if attempt.get("compile_refusal"):
                    say("      the compile refused, LITERAL: %s"
                        % ("%s" % attempt["compile_refusal"])[:500])
                continue
            continue
        say("   -- %d attempts, %.0f s, peak resident %d kB"
            % (number, time.time() - started,
               GEN.check_memory("sample")))
        continue
    say("")
    say("the sample: %d attempts in %.0f s" % (number,
                                               time.time() - started))
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


# ==================================================================
# section 4: the three routes in one table
# ==================================================================

LANGUAGE_NAME = {"c": "c", "cpp": "c++", "go": "go", "rust": "rust",
                 "swift": "swift"}
ORDER = ["c", "cpp", "rust", "go", "swift"]


def key_of(row):
    return (row["mnem"], row["shape"], row["key_width"])


THE_NATIVE_ROUTE = ("term", "primitive", "primitive+setup", None)
"""the route names the DRIVER's own route wrote, read off the bank
rather than recalled: a term printed in the language's own operators, a
primitive body matched out of the corpus, that with a setup, and the
rows an early pass wrote before the field existed."""

THE_BACKSTOP = ("general", "constructed")
"""the CONSTRUCTION route's own two names: task t4's general tier
(`general`) and task t2's eight schemas (`constructed`) before it."""

THE_BIT_BLAST = ("bit_blast",)
"""this task's, and task bb1's on the other architecture."""


def bank_reading(route_names, reading):
    """{target: cells} under one reading, over certificates whose
    `route` is in `route_names`.

    THE TWO READINGS THE BRIEF ASKS FOR.  `strict`: every written place
    of the cell is proved, flags included.  `destination_only`: the
    destination place's value is proved and the flags places are not
    required.  Both are `bank.py`'s own definitions, read here off the
    certificates so the three routes can stand in one table."""
    import bank as BK
    places = {}
    for cert in BK.stream(BK.BANK):
        if cert["target"] not in ORDER:
            continue
        if route_names is not None:
            if cert.get("route") not in route_names:
                continue
        if cert["place"] is None:
            continue
        key = (cert["target"], (cert["cell"]["mnem"],
                                cert["cell"]["shape"],
                                cert["cell"]["key_width"]))
        held = places.setdefault(key, {})
        was = held.get(cert["place"])
        now = cert["kind"] in ("proved", "proved_under_caller_extension")
        if was is None:
            held[cert["place"]] = now
            continue
        held[cert["place"]] = was or now
        continue
    out = {}
    for target in ORDER:
        out[target] = set()
        continue
    for (target, cell) in places:
        held = places[(target, cell)]
        if reading == "strict":
            every = True
            for name in held:
                if not held[name]:
                    every = False
                continue
            if every and held:
                out[target].add(cell)
            continue
        wanted = destination_names(held)
        every = True
        for name in wanted:
            if not held[name]:
                every = False
            continue
        if every and wanted:
            out[target].add(cell)
        continue
    return out


def destination_names(held):
    """the destination places of one cell's place set: every place that
    is not the flags, or the flags place when that is all there is.
    `handful.destination_place`'s own rule, read over a set of names."""
    out = []
    for name in held:
        base = ("%s" % name).split(".")[0]
        if base == "flags":
            continue
        out.append(name)
        continue
    if out:
        return out
    return list(held)


def route_sets(reading):
    """the three routes' cell sets under one reading, plus any route at
    all, each read off the bank's own certificates and not re-derived."""
    native = bank_reading(THE_NATIVE_ROUTE, reading)
    backstop = bank_reading(THE_BACKSTOP, reading)
    blasted = bank_reading(THE_BIT_BLAST, reading)
    whatever = bank_reading(None, reading)
    return native, backstop, blasted, whatever


def table_command():
    configure()
    import autopoly as AP
    cells = AP.read_json(AP.CELLS)
    whole = len(cells["asked"])
    for reading in ("destination_only", "strict"):
        native, backstop, blasted, whatever = route_sets(reading)
        say("")
        say("THE THREE ROUTES, PROVED, %s reading, of %d on every row"
            % (reading, whole))
        say("| language | native route | backstop (t4, t2) | bit-blast "
            "(bb2) | any route | of |")
        say("|---|---|---|---|---|---|")
        union_native = set()
        union_backstop = set()
        union_blast = set()
        union_any = set()
        every = None
        for target in ORDER:
            one = native.get(target, set())
            two = backstop.get(target, set())
            three = blasted.get(target, set())
            four = whatever.get(target, set())
            union_native |= one
            union_backstop |= two
            union_blast |= three
            union_any |= four
            if every is None:
                every = set(four)
            else:
                every = every & four
            say("| %s | %d | %d | %d | %d | %d |"
                % (LANGUAGE_NAME[target], len(one), len(two), len(three),
                   len(four), whole))
            continue
        say("| **proved on at least one language** | **%d** | **%d** | "
            "**%d** | **%d** | **%d** |"
            % (len(union_native), len(union_backstop), len(union_blast),
               len(union_any), whole))
        say("| **proved on all five languages** | | | | **%d** | **%d** |"
            % (len(every or set()), whole))
        say("")
        continue

    rows = read_rows(GEN.store_paths()[0])
    outcomes(rows, whole)
    distributions(rows)
    causes(rows)
    return 0


def kind_of_place(place):
    import bank as BK
    return BK.kind_of_place(place)


def outcomes(rows, whole):
    """this route's own outcomes, per language, over the store."""
    held = {}
    for row in rows:
        if row.get("route") != "bit_blast":
            continue
        key = (row["lang"], key_of(row))
        counts = held.setdefault(key, {"proved": 0, "sat": 0,
                                       "undecided": 0, "refused": 0})
        for place in row.get("places") or []:
            kind = kind_of_place(place)
            if kind == "proved_under_caller_extension":
                kind = "proved"
            counts[kind] = counts.get(kind, 0) + 1
            continue
        continue
    say("THE BIT-BLAST ROUTE'S OWN OUTCOMES OVER WRITTEN PLACES, "
        "of %d cells on every row" % whole)
    say("| language | cells run | places | proved | disproved | "
        "undecided | refused |")
    say("|---|---|---|---|---|---|---|")
    for target in ORDER:
        cells = set()
        totals = {"proved": 0, "sat": 0, "undecided": 0, "refused": 0}
        for (lang, cell) in held:
            if lang != target:
                continue
            cells.add(cell)
            for name in totals:
                totals[name] = totals[name] + held[(lang, cell)][name]
                continue
            continue
        say("| %s | %d | %d | %d | %d | %d | %d |"
            % (LANGUAGE_NAME[target], len(cells), sum(totals.values()),
               totals["proved"], totals["sat"], totals["undecided"],
               totals["refused"]))
        continue
    say("")
    return


def attempts_of(rows):
    out = []
    for row in rows:
        if row.get("route") != "bit_blast":
            continue
        for place in row.get("places") or []:
            for attempt in place.get("attempts") or []:
                out.append((row, place, attempt))
                continue
            continue
        continue
    return out


def distributions(rows):
    gates = []
    blasts = []
    lines = []
    renders = []
    compiles = []
    instructions = []
    checks = []
    not_gated = []
    per_target = {}
    for row, place, attempt in attempts_of(rows):
        target = row["lang"]
        held = per_target.setdefault(target, {"gates": [],
                                              "instructions": [],
                                              "compile": [],
                                              "check": []})
        if attempt.get("gates") is not None:
            gates.append(attempt["gates"])
            held["gates"].append(attempt["gates"])
        if attempt.get("blast_seconds") is not None:
            blasts.append(attempt["blast_seconds"])
        if attempt.get("source_lines") is not None:
            lines.append(attempt["source_lines"])
        if attempt.get("render_seconds") is not None:
            renders.append(attempt["render_seconds"])
        if attempt.get("compile_seconds") is not None:
            compiles.append(attempt["compile_seconds"])
            held["compile"].append(attempt["compile_seconds"])
        if attempt.get("instructions") is not None:
            instructions.append(attempt["instructions"])
            held["instructions"].append(attempt["instructions"])
        if attempt.get("check_seconds") is not None:
            checks.append(attempt["check_seconds"])
            held["check"].append(attempt["check_seconds"])
        made = attempt.get("not_gated") or {}
        if made.get("the_gate_was_not_asked") is not None:
            not_gated.append((row["lang"], key_of(row),
                              place.get("writes"),
                              made.get("instructions"),
                              made["the_gate_was_not_asked"]))
        continue
    say("THE SIZES AND THE SECONDS")
    say("| what | attempts | smallest | median | mean | largest |")
    say("|---|---|---|---|---|---|")
    for name, values in (("gates per definition", gates),
                         ("blast seconds", blasts),
                         ("source lines", lines),
                         ("render seconds", renders),
                         ("compile seconds", compiles),
                         ("carved body instructions", instructions),
                         ("check seconds", checks)):
        count, low, middle, mean, high = quantiles(values)
        say("| %s | %d | %s | %s | %s | %s |"
            % (name, count, low, middle, mean, high))
        continue
    say("")
    say("PER LANGUAGE")
    say("| language | attempts | gates, median | body, median | "
        "body, largest | compile s, median | compile s, summed |")
    say("|---|---|---|---|---|---|---|")
    for target in ORDER:
        held = per_target.get(target)
        if held is None:
            continue
        gate_stats = quantiles(held["gates"])
        body_stats = quantiles(held["instructions"])
        compile_stats = quantiles(held["compile"])
        say("| %s | %d | %s | %s | %s | %s | %.0f |"
            % (LANGUAGE_NAME[target], gate_stats[0], gate_stats[2],
               body_stats[2], body_stats[4], compile_stats[2],
               sum(held["compile"])))
        continue
    say("")
    say("NOT GATED -- the gate was never asked, by cause: %d attempts "
        "(the ceilings are %d carved instructions and %d seconds on a "
        "wall clock that stops it)"
        % (len(not_gated), GEN.GATE_INSTRUCTION_CEILING,
           GATE_WALL_SECONDS))
    counted = {}
    for row in not_gated:
        cause = " ".join(("%s" % row[4]).split())[:150]
        counted[cause] = counted.get(cause, 0) + 1
        continue
    say("| the cause, LITERAL | attempts |")
    say("|---|---|")
    for cause in sorted(counted, key=lambda one: -counted[one]):
        say("| %s | %d |" % (cause.replace("|", "/"), counted[cause]))
        continue
    say("")
    say("| language | mnem | shape | width | place | instructions |")
    say("|---|---|---|---|---|---|")
    for target, key, writes, size, _cause in sorted(
            not_gated, key=lambda r: -(r[3] or 0))[:40]:
        say("| %s | `%s` | `%s` | %s | %s | %s |"
            % (LANGUAGE_NAME.get(target, target), key[0], key[1],
               key[2], writes, size))
        continue
    say("")
    return


def causes(rows):
    held = {}
    for row, _place, attempt in attempts_of(rows):
        check = attempt.get("check") or {}
        outcome = check.get("outcome")
        if outcome is None:
            outcome = attempt.get("refusal_cause") or "no verdict"
        if outcome == "PROVED_ON_SHIP":
            continue
        detail = attempt.get("refusal_detail") or check.get("reason") or ""
        key = (row["lang"], " ".join(("%s" % outcome).split())[:110],
               " ".join(("%s" % detail).split())[:140])
        held[key] = held.get(key, 0) + 1
        continue
    say("EVERY OUTCOME THAT IS NOT A PROOF, with its cause, LITERAL")
    say("| language | outcome | cause | attempts |")
    say("|---|---|---|---|")
    for key in sorted(held, key=lambda k: (-held[k], k)):
        say("| %s | %s | %s | %d |"
            % (LANGUAGE_NAME.get(key[0], key[0]),
               key[1].replace("|", "/"), key[2].replace("|", "/"),
               held[key]))
        continue
    say("")
    return


def largest_command(many):
    """the `many` cells with the largest circuits, as THE PASS ITSELF
    measured them, read off the store.

    WHY IT IS READ OFF THE STORE.  Lane `bb2_l4` ran the six-cell
    sample as its own command and was cut inside it: `swiftc` did not
    come back from a 74,674-line source and its own 600-second bound
    raised `subprocess.TimeoutExpired` out of the run.  The bound firing
    is now a row with a cause, and the pass then ran every one of these
    cells on every target, so the rows below are the same measurement
    finished rather than a second one."""
    configure()
    chosen = largest_cells(many)
    wanted = set()
    for key, _gates in chosen:
        wanted.add(key)
        continue
    say("the sample: the %d cells with the largest circuits, off %s"
        % (len(chosen), os.path.basename(SIZES)))
    for key, gates in chosen:
        say("   `%s` `%s` %s -- largest place %d gates"
            % (key[0], key[1], key[2], gates))
        continue
    say("")
    rows = read_rows(GEN.store_paths()[0])
    say("| mnem | shape | width | place | language | gates | source "
        "lines | render s | compile s | body instructions | outcome | "
        "check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row, place, attempt in attempts_of(rows):
        key = key_of(row)
        if key not in wanted:
            continue
        check = attempt.get("check") or {}
        outcome = check.get("outcome")
        if outcome is None:
            outcome = attempt.get("refusal_cause") or "no verdict"
        say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | "
            "%s | %s |"
            % (key[0], key[1], key[2], place.get("writes"), row["lang"],
               attempt.get("gates"), attempt.get("source_lines"),
               attempt.get("render_seconds"),
               attempt.get("compile_seconds"),
               attempt.get("instructions"),
               " ".join(("%s" % outcome).split())[:80],
               attempt.get("check_seconds")))
        if attempt.get("compile_refusal"):
            say("      the compile refused, LITERAL: %s"
                % " ".join(("%s" % attempt["compile_refusal"]).split())[:300])
        continue
    return 0


def rows_command():
    configure()
    rows = read_rows(GEN.store_paths()[0])
    say("| mnem | shape | width | language | place | gates | source "
        "lines | compile s | body instructions | outcome | check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|")
    for row, place, attempt in attempts_of(rows):
        key = key_of(row)
        check = attempt.get("check") or {}
        outcome = check.get("outcome")
        if outcome is None:
            outcome = attempt.get("refusal_cause") or "no verdict"
        say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (key[0], key[1], key[2],
               LANGUAGE_NAME.get(row["lang"], row["lang"]),
               place.get("writes"), attempt.get("gates"),
               attempt.get("source_lines"),
               attempt.get("compile_seconds"),
               attempt.get("instructions"),
               " ".join(("%s" % outcome).split())[:90],
               attempt.get("check_seconds")))
        continue
    return 0


def alarms_command():
    """every written place ANOTHER pass certifies PROVED and this route
    DISPROVES, keyed the way the bank keys a certificate.

    THE KEY CARRIES THE SETTER, which is the bank's own rule and not a
    refinement of it: a flag consumer's mapping is a function of the
    flag state a setter wrote, so the same consumer over another setter
    is another artifact with its own proof.  Lane `bb2_l9` read 726
    "alarms" with the setter left out of the key and this task's own
    pass left in the certified set -- every one of them this route's
    own verdict on one setter set against this route's own verdict on
    another.  Neither is an alarm; the key was wrong.

    A disproof of a circuit z3 itself wrote, against a term z3 itself
    holds, on a place another pass proved, is an alarm about the
    machinery and not a result about a language, and it is reported as
    one."""
    configure()
    import autopoly as AP
    import bank as BK
    mine = (PASS_LABEL, INTERP_PASS_LABEL)
    certified = {}
    for cert in BK.stream(BK.BANK):
        if cert["place"] is None:
            continue
        if cert["produced_by"]["pass"] in mine:
            continue
        if cert["kind"] not in ("proved",
                                "proved_under_caller_extension"):
            continue
        key = (cert["target"], cert["cell"]["mnem"],
               cert["cell"]["shape"], cert["cell"]["key_width"],
               cert["place"], BK.setter_tuple(cert))
        certified[key] = cert["produced_by"]["pass"]
        continue
    rows = read_rows(GEN.store_paths()[0])
    found = []
    for row in rows:
        if row.get("route") != "bit_blast":
            continue
        setter = AP.setter_key(row.get("setter"))
        for place in row.get("places") or []:
            # THE BANK'S OWN READING OF THE PLACE, not the gate's raw
            # outcome.  A gate that answers DISPROVED and whose
            # caller-extension re-pose then proves is banked
            # `proved_under_caller_extension` -- it is a proof on the
            # region the caller guarantees, which is task o7's rule and
            # every pass's -- and reading the raw outcome counted 294
            # such places as alarms in lane `bb2_l10`.  An alarm is a
            # place the bank would record `sat`.
            if BK.kind_of_place(place) != "sat":
                continue
            check = place.get("check") or {}
            key = (row["lang"], row["mnem"], row["shape"],
                   row["key_width"], place.get("writes"), setter)
            if key not in certified:
                continue
            found.append((key, certified[key],
                          check.get("counterexample")))
            continue
        continue
    say("THE 100%% RE-DERIVATION: every place another pass certifies "
        "and this route disproves")
    say("| language | mnem | shape | width | place | setter | the "
        "bank's pass | counterexample, LITERAL |")
    say("|---|---|---|---|---|---|---|---|")
    for key, which, counter in sorted(found, key=lambda r: "%s" % (r[0],)):
        setter = key[5]
        if setter is None:
            setter = "--"
        else:
            setter = "`%s` `%s` %s" % (setter[0], setter[1], setter[2])
        say("| %s | `%s` | `%s` | %s | %s | %s | %s | %s |"
            % (key[0], key[1], key[2], key[3], key[4], setter, which,
               " ".join(("%s" % counter).split())[:160]))
        continue
    if not found:
        say("| none | | | | | | | |")
    say("")
    say("certified places another pass holds, on the five compiled "
        "targets: %d" % len(certified))
    say("alarms: %d" % len(found))
    return 0


# ==================================================================
# section 5: the interpreted seven, by agreement
# ==================================================================

GATE_TEXT = BB.GATE_TEXT
"""the four operator texts, task bb1's own, read from `bitblast.py` so
the compiled route and the interpreted route write the same gate.  They
are OUTPUT SPELLINGS in the rendered source and are never a key, a
grouping or a comparison scope."""

THE_INTERP_RENDERER = None


def install_the_gate_renderer():
    """`interp_render.InterpRenderer` replaced by `GateRenderer`, which
    is the same swap `bb1_run.py` made at `rv_general.one_attempt`:
    `interp_check.one_run` looks the class up on the module at call
    time, so the loop is CALLED and nothing of it is copied."""
    global THE_INTERP_RENDERER
    import interp_render as IR
    if THE_INTERP_RENDERER is None:
        THE_INTERP_RENDERER = IR.InterpRenderer
        IR.InterpRenderer = GateRenderer
    return IR


class GateRenderer(object):
    """the circuit written as one named local per gate, in one
    interpreted language.

    IT IS NOT A SECOND RENDERER.  Every part that is about the target --
    the parameter plan, the holder widths, the answer home, the
    prelude, the runner's own main, the literal spelling -- is
    `interp_render.InterpRenderer`'s and is held on `self.inner` and
    called.  What this class writes is the four gate texts and the
    bindings around them.

    THE VALUES ARE SINGLE BITS.  Every local holds 0 or 1, so the gate
    texts are the same four in all seven languages and no width
    question arises inside the circuit at all; the arrival bits are
    read with the dialect's own `ext` helper and the answer is packed
    with the dialect's own `cat`, both from that dialect's prelude,
    which is where every width question in this line already lives."""

    def __init__(self, lang, families, result_family, result_width,
                 label):
        self.lang = lang
        self.inner = THE_INTERP_RENDERER(lang, families, result_family,
                                         result_width, label)
        self.dialect = self.inner.dialect
        self.label = label
        self.params = []
        self.gates = None
        self.points = None
        self.not_run = None

    def __getattr__(self, name):
        if name == "inner":
            raise AttributeError(name)
        return getattr(self.inner, name)

    def render(self, term, text):
        import emulate as E
        inner = self.inner
        inner.plan_parameters(term)
        inner.check_symbols(term)
        inner.dialect.check_width(inner.result_width)
        self.params = inner.params
        try:
            circuit = BB.blast(term)
        except B.Refused as problem:
            raise E.Refused(problem.cause, problem.detail)
        self.gates = len(circuit.gates)
        work = len(circuit.gates) * points_of(inner.params)
        self.points = points_of(inner.params)
        if work > INTERP_WORK_CEILING:
            self.not_run = ("%d gates times %d sample points is %d gate "
                            "evaluations, above the %d this task's "
                            "interpreted runner is offered"
                            % (len(circuit.gates), self.points, work,
                               INTERP_WORK_CEILING))
            raise E.Refused("the circuit is larger than the work this "
                            "task's interpreted runner is offered",
                            self.not_run)
        return self.assemble(circuit, text)

    def name(self, text):
        """one local's name in this dialect's own spelling: php's carry
        a `$` and no other language's do, which is the dialect's own
        `param`."""
        return self.dialect.param(text)

    def assemble(self, circuit, text):
        import emulate as E
        inner = self.inner
        statements = []
        for local, symbol_index, bit in circuit.inputs:
            symbol_name = circuit.symbols[symbol_index]
            position = inner.seed_names.get(symbol_name)
            if position is None:
                raise E.Refused(BB.CAUSE_BIT_MISSING,
                                "%s is not a planned arrival"
                                % symbol_name)
            param = inner.params[position]
            if bit >= param["bits"]:
                raise E.Refused(BB.CAUSE_BIT_MISSING,
                                "bit %d of %s, whose holder is %d bits"
                                % (bit, symbol_name, param["bits"]))
            read = inner.helper("ext", [self.name(param["name"]), bit,
                                        bit])
            statements.append((self.name(local), read))
            continue
        one = self.dialect.lit(1, 1)
        for local, kind, arguments in circuit.gates:
            if kind == BB.CONST:
                body = self.dialect.lit(int(arguments[0]), 1)
            elif kind == BB.NOT:
                body = "(%s ^ %s)" % (self.name(arguments[0]), one)
            else:
                body = GATE_TEXT[kind] % (self.name(arguments[0]),
                                          self.name(arguments[1]))
            statements.append((self.name(local), body))
            continue
        packed = None
        counter = 0
        for index in range(circuit.width - 1, -1, -1):
            driver = self.name(circuit.outputs[index])
            local = self.name("w%d" % counter)
            counter = counter + 1
            if packed is None:
                statements.append((local, driver))
            else:
                statements.append((local,
                                   inner.helper("cat", [packed, driver,
                                                        1])))
            packed = local
            continue
        if packed is None:
            packed = self.name("w0")
            statements.append((packed, self.dialect.lit(0, 1)))
        body = inner.answer(packed, "bv", inner.result_width)
        symbol = "emu_%s" % self.label
        names = []
        for param in inner.params:
            names.append(self.dialect.param(param["name"]))
            continue
        pieces = []
        pieces.append(self.dialect.prelude)
        pieces.append("\n")
        pieces.append(self.comment_lines(text))
        pieces.append(gate_function(self.lang, symbol, names,
                                    statements, body))
        call = "%s(%s)" % (symbol, inner.argument_text(len(names)))
        pieces.append(self.dialect.main % {"symbol": symbol,
                                           "call": call})
        return "".join(pieces), symbol

    def comment_lines(self, text):
        marks = {"cpython": "#", "ruby": "#", "javascript": "//",
                 "php": "//", "java": "    //", "dart": "//",
                 "csharp": "    //"}
        mark = marks[self.lang]
        lines = []
        lines.append("%s task bb2 emulation -- the BIT-BLAST route: "
                     "z3's own circuit," % mark)
        lines.append("%s one named local per gate, over the term of %s."
                     % (mark, self.label))
        lines.append("%s The term's layer-5 text, LITERAL:" % mark)
        lines.append("%s   %s" % (mark, " ".join(("%s" % text).split())))
        return "\n".join(lines) + "\n"


BINDING = {
    "cpython": ("    %s = %s", "    return %s", None),
    "ruby": ("  %s = %s", "  %s", "end"),
    "javascript": ("    const %s = %s;", "    return %s;", "}"),
    "php": ("    %s = %s;", "    return %s;", "}"),
    "java": ("        long %s = %s;", "        return %s;", "    }"),
    "dart": ("  int %s = %s;", "  return %s;", "}"),
    "csharp": ("        long %s = %s;", "        return %s;", "    }"),
}
"""how each of the seven binds a local and answers.  Every text is that
language's own syntax, read off `interp_render`'s own dialect for the
same language; the fixed-width four bind at the dialect's own answer
holder and the three unbounded ones bind without one."""


def gate_head(lang, symbol, names):
    if lang == "cpython":
        return "def %s(%s):" % (symbol, ", ".join(names))
    if lang == "ruby":
        return "def %s(%s)" % (symbol, ", ".join(names))
    if lang == "javascript":
        return "function %s(%s) {" % (symbol, ", ".join(names))
    if lang == "php":
        return "function %s(%s) {" % (symbol, ", ".join(names))
    if lang == "dart":
        typed = []
        for one in names:
            typed.append("int %s" % one)
            continue
        return "int %s(%s) {" % (symbol, ", ".join(typed))
    typed = []
    for one in names:
        typed.append("long %s" % one)
        continue
    if lang == "java":
        return "    static long %s(%s) {" % (symbol, ", ".join(typed))
    return "    public static long %s(%s) {" % (symbol,
                                                ", ".join(typed))


def gate_function(lang, symbol, names, statements, body):
    """one function with a statement per gate, in one language's own
    syntax.  `interp_render`'s own `Dialect.function` takes ONE
    expression as the body, which a circuit is not; this writes the
    same signature with a body of bindings."""
    bind, answer, close = BINDING[lang]
    lines = [gate_head(lang, symbol, names)]
    for local, text in statements:
        lines.append(bind % (local, text))
        continue
    lines.append(answer % body)
    if close is not None:
        lines.append(close)
    lines.append("")
    return "\n".join(lines) + "\n"


def points_of(params):
    """how many sample points `interp_check`'s own rule gives this
    parameter plan, computed by that file's own two functions."""
    import interp_check as IC
    lists = IC.points_for(params)
    many = 1
    for one in lists:
        many = many * len(one)
        continue
    return many


def use_task_bb2():
    import interp_check as IC
    IC.ABORT_KB = 6 * 1024 * 1024
    IC.ABORT_NAME = ABORT_NAME
    IC.SRC_DIR = INTERP_SRC
    GEN.ABORT_NAME = ABORT_NAME
    if not os.path.isdir(INTERP_SRC):
        os.makedirs(INTERP_SRC)
    install_the_gate_renderer()
    return IC


def interp_pairs():
    """every (cell, interpreted target) pair: the 253 attested cells in
    the cells file's own order and the seven targets in
    `interp_render.LANGUAGES`'s own order inside each cell."""
    import autopoly as AP
    import interp_render as IR
    cells = AP.read_json(AP.CELLS)
    out = []
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for lang in IR.LANGUAGES:
            out.append((asked, lang, record["attested_ledger_rows"]))
            continue
        continue
    return out


def interp_key(asked, lang):
    return "%s|%s|%s|%s" % (asked[0], asked[1], asked[2], lang)


def interp_command(limit, path=None, timeout=None):
    """the interpreted loop: one line on the store per finished run."""
    import autopoly as AP
    import interp_check as IC
    import interp_render as IR
    use_task_bb2()
    if path is None:
        path = INTERP_RUNS
    if timeout is None:
        timeout = INTERP_TIMEOUT_FIRST
    cells = AP.read_json(AP.CELLS)
    shared = IC.build_shared()
    say("the runners, as this machine answers them:")
    for lang in IR.LANGUAGES:
        say("   %-12s %s" % (lang, IR.runner_answer(lang)))
    say("")
    done = set()
    for run in read_rows(path):
        done.add(interp_key((run["mnem"], run["shape"],
                             run["key_width"]), run["lang"]))
        continue
    pairs = interp_pairs()
    say("pairs to run: %d; already recorded: %d" % (len(pairs),
                                                    len(done)))
    ran = 0
    index = 0
    started = time.time()
    for asked, lang, ledger in pairs:
        index = index + 1
        if interp_key(asked, lang) in done:
            continue
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, len(pairs), asked[0], asked[1], asked[2], lang,
               ledger))
        record = IC.one_run(shared, cells, asked, lang, timeout=timeout)
        record["attested_ledger_rows"] = ledger
        record["route"] = "bit_blast"
        handle = open(path, "a")
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.close()
        ran = ran + 1
        say("   %s | %d s | peak resident: %d kB"
            % (interp_line(record), round(record.get("seconds") or 0),
               GEN.check_memory("interp %d" % index)))
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d run(s) performed" % ran)
            break
        continue
    say("")
    say("runs performed this lane: %d in %d s"
        % (ran, round(time.time() - started)))
    say("lines on %s: %d" % (path, len(read_rows(path))))
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


INTERP_SIZES = os.path.join(HERE, "bb2_interp_sizes.json")


def interp_sizes_command():
    """the WORK every interpreted run would ask for, before anything is
    written or run: the destination place's circuit blasted, the sample
    counted by `interp_check`'s own rule, and the two multiplied.  This
    is what `INTERP_WORK_CEILING` is read off, so the ceiling is a
    number measured over the population and not a preference."""
    import autopoly as AP
    import interp_check as IC
    import interp_render as IR
    import emulate as E
    use_task_bb2()
    cells = AP.read_json(AP.CELLS)
    shared = IC.build_shared()
    driver = shared["driver"]
    rows = []
    started = time.time()
    number = 0
    for record in cells["asked"]:
        number = number + 1
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        row = {"mnem": asked[0], "shape": asked[1],
               "key_width": asked[2]}
        rows.append(row)
        try:
            held = driver.cell_input(cells, asked)
        except Exception as problem:                          # noqa: BLE001
            row["refusal"] = "%s: %s" % (type(problem).__name__,
                                         problem)
            continue
        if held.get("refusal_cause") is not None:
            row["refusal"] = held["refusal_cause"]
            continue
        place = driver.destination_place({"places": held["places"]})
        if place is None:
            row["refusal"] = "the cell writes no place"
            continue
        if driver.fixes_are_on() and place.get("halved") is None:
            projected = driver.projected_lane(shared["pipeline"], place,
                                              held["key_width"])
            if projected is not None:
                if projected.get("refusal_cause") is not None:
                    row["refusal"] = projected["refusal_cause"]
                    continue
                place = projected["place"]
        if place.get("families") is None:
            row["refusal"] = place.get("not_rendered")
            continue
        row["place"] = place["writes"]
        row["bits"] = place["bits"]
        term = driver.renderer_input(place["term"], driver.TASK)
        renderer = THE_INTERP_RENDERER("cpython", place["families"],
                                       place["home"]["family"],
                                       place["bits"], "probe")
        try:
            renderer.plan_parameters(term)
        except E.Refused as refusal:
            row["refusal"] = "%s: %s" % (refusal.cause, refusal.detail)
            continue
        row["arrivals"] = len(renderer.params)
        row["sample_points"] = points_of(renderer.params)
        try:
            circuit = BB.blast(term)
        except B.Refused as problem:
            row["refusal"] = "%s: %s" % (problem.cause, problem.detail)
            continue
        except Exception as problem:                          # noqa: BLE001
            row["refusal"] = "%s: %s" % (type(problem).__name__,
                                         ("%s" % problem)[:200])
            continue
        row["gates"] = len(circuit.gates)
        row["work"] = row["gates"] * row["sample_points"]
        if number % 50 == 0:
            say("   [%d/%d] cells, %.0f s" % (number, len(cells["asked"]),
                                              time.time() - started))
        continue
    handle = open(INTERP_SIZES, "w")
    json.dump({"meta": {"task": "bb2",
                        "what": "the gate count times the sample point "
                                "count for every attested x86 cell's "
                                "destination place, before anything is "
                                "written or run",
                        "seconds": round(time.time() - started, 1)},
               "rows": rows}, handle, indent=1, sort_keys=True)
    handle.close()
    say("")
    say("wrote %s" % INTERP_SIZES)
    work = []
    for row in rows:
        if row.get("work") is None:
            continue
        work.append(row["work"])
        continue
    count, low, middle, mean, high = quantiles(work)
    say("| what | cells | smallest | median | mean | largest |")
    say("|---|---|---|---|---|---|")
    say("| gate evaluations per run | %d | %s | %s | %s | %s |"
        % (count, low, middle, mean, high))
    say("")
    bands = [(0, 10 ** 5), (10 ** 5, 10 ** 6), (10 ** 6, 10 ** 7),
             (10 ** 7, 10 ** 8), (10 ** 8, 10 ** 9), (10 ** 9, 10 ** 18)]
    say("| gate evaluations | cells |")
    say("|---|---|")
    for low, high in bands:
        many = 0
        for value in work:
            if value >= low and value < high:
                many = many + 1
            continue
        say("| %d to %d | %d |" % (low, high, many))
        continue
    say("")
    say("THE FIFTEEN LARGEST")
    say("| mnem | shape | width | place | arrivals | points | gates | "
        "gate evaluations |")
    say("|---|---|---|---|---|---|---|---|")
    ranked = sorted([r for r in rows if r.get("work") is not None],
                    key=lambda r: -r["work"])
    for row in ranked[:15]:
        say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s |"
            % (row["mnem"], row["shape"], row["key_width"],
               row.get("place"), row.get("arrivals"),
               row.get("sample_points"), row.get("gates"), row["work"]))
        continue
    say("")
    say("peak resident: %d kB" % GEN.peak_kb())
    return 0


def interp_one_command(mnem, shape, width, lang, ceiling=None):
    """ONE (cell, interpreted target), printed: the walkthrough command,
    and the one that MEASURES what an interpreted gate run costs, so
    `INTERP_WORK_CEILING` is a number read off a run and not a
    preference.  It writes no store line.

    `ceiling` raises this task's own work ceiling FOR THIS ONE RUN, so
    the rate can be measured above the ceiling the pass then states.
    The pass itself never takes it."""
    global INTERP_WORK_CEILING
    import autopoly as AP
    import interp_check as IC
    use_task_bb2()
    held_ceiling = INTERP_WORK_CEILING
    if ceiling is not None:
        INTERP_WORK_CEILING = int(ceiling)
    cells = AP.read_json(AP.CELLS)
    shared = IC.build_shared()
    asked = (mnem, shape, int(width))
    started = time.time()
    record = IC.one_run(shared, cells, asked, lang,
                        timeout=INTERP_TIMEOUT_RETRY)
    seconds = time.time() - started
    say("%s %s %s -> %s" % (mnem, shape, width, lang))
    say("   place: %s, %s bits" % (record.get("writes"),
                                   record.get("bits")))
    say("   %s" % interp_line(record))
    say("   seconds: %.1f" % seconds)
    say("   source: %s" % record.get("source_path"))
    if record.get("refusal_detail"):
        say("   refusal detail, LITERAL: %s"
            % ("%s" % record["refusal_detail"])[:400])
    say("   gloss, LITERAL: %s" % ("%s" % record.get("gloss"))[:300])
    say("peak resident: %d kB" % GEN.peak_kb())
    INTERP_WORK_CEILING = held_ceiling
    return 0


def interp_line(record):
    if record.get("outcome") == "TIMEOUT":
        return ("TIMEOUT at %s s, %s point(s) reached"
                % (record.get("timeout_seconds"),
                   record.get("points_reached")))
    if record.get("refusal_cause") is not None:
        return "REFUSED: %s" % ("%s" % record["refusal_cause"])[:80]
    return ("%s points, %s agree, %s disagree, %s declined"
            % (record.get("sample_points"), record.get("agreements"),
               record.get("disagreements"),
               record.get("declined_points")))


def interp_retry_command(limit):
    """every interpreted run whose first pass TIMED OUT, once more at
    the longer bound.  Task ex2's own two-pass shape, unchanged."""
    import autopoly as AP
    import interp_check as IC
    use_task_bb2()
    cells = AP.read_json(AP.CELLS)
    shared = IC.build_shared()
    wanted = []
    for run in read_rows(INTERP_RUNS):
        if run.get("outcome") != "TIMEOUT":
            continue
        wanted.append(((run["mnem"], run["shape"], run["key_width"]),
                       run["lang"],
                       run.get("attested_ledger_rows")))
        continue
    done = set()
    for run in read_rows(INTERP_RETRY_RUNS):
        done.add(interp_key((run["mnem"], run["shape"],
                             run["key_width"]), run["lang"]))
        continue
    say("timed out on the first pass: %d; already retried: %d"
        % (len(wanted), len(done)))
    ran = 0
    for asked, lang, ledger in wanted:
        if interp_key(asked, lang) in done:
            continue
        say("retry %s %s %s -> %s" % (asked[0], asked[1], asked[2],
                                      lang))
        record = IC.one_run(shared, cells, asked, lang,
                            timeout=INTERP_TIMEOUT_RETRY)
        record["attested_ledger_rows"] = ledger
        record["route"] = "bit_blast"
        handle = open(INTERP_RETRY_RUNS, "a")
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.close()
        ran = ran + 1
        say("   %s" % interp_line(record))
        if limit is not None and ran >= limit:
            break
        continue
    say("retries performed: %d" % ran)
    return 0


def interp_effective():
    """one record per (cell, target): the first pass's, replaced by the
    retry's where the first pass timed out and the retry answered."""
    out = {}
    for run in read_rows(INTERP_RUNS):
        out[interp_key((run["mnem"], run["shape"], run["key_width"]),
                       run["lang"])] = run
        continue
    for run in read_rows(INTERP_RETRY_RUNS):
        out[interp_key((run["mnem"], run["shape"], run["key_width"]),
                       run["lang"])] = run
        continue
    return out


def interp_table_command():
    import autopoly as AP
    import interp_render as IR
    configure()
    cells = AP.read_json(AP.CELLS)
    whole = len(cells["asked"])
    held = interp_effective()
    say("THE INTERPRETED SEVEN, THE BIT-BLAST CIRCUIT RUN BESIDE THE "
        "DEFINITION, of %d on every row" % whole)
    say("| language | agreed | disagreed | refused | timed out | of |")
    say("|---|---|---|---|---|---|")
    agree_sets = {}
    for lang in IR.LANGUAGES:
        agreed = set()
        disagreed = set()
        refused = set()
        timed = set()
        for key in held:
            run = held[key]
            if run["lang"] != lang:
                continue
            cell = (run["mnem"], run["shape"], run["key_width"])
            if run.get("outcome") == "TIMEOUT":
                timed.add(cell)
                continue
            if run.get("refusal_cause") is not None:
                refused.add(cell)
                continue
            if run.get("disagreements"):
                disagreed.add(cell)
                continue
            if not run.get("agreements"):
                refused.add(cell)
                continue
            agreed.add(cell)
            continue
        agree_sets[lang] = agreed
        say("| %s | %d | %d | %d | %d | %d |"
            % (lang, len(agreed), len(disagreed), len(refused),
               len(timed), whole))
        continue
    every = None
    for lang in IR.LANGUAGES:
        if every is None:
            every = set(agree_sets[lang])
            continue
        every = every & agree_sets[lang]
        continue
    say("| **agreeing on all seven** | **%d** | | | | **%d** |"
        % (len(every or set()), whole))
    say("")
    say("EVERY DISAGREEMENT, LITERAL")
    say("| language | mnem | shape | width | place | the point | the "
        "reference | the interpreter |")
    say("|---|---|---|---|---|---|---|---|")
    many = 0
    for key in sorted(held):
        run = held[key]
        first = run.get("first_disagreement")
        if not first:
            continue
        many = many + 1
        say("| %s | `%s` | `%s` | %s | %s | %s | %s | %s |"
            % (run["lang"], run["mnem"], run["shape"],
               run["key_width"], run.get("writes"),
               first.get("point"), first.get("the reference's answer"),
               first.get("the interpreter's answer")))
        continue
    if not many:
        say("| none | | | | | | | |")
    say("")
    say("EVERY REFUSAL, BY CAUSE, LITERAL")
    reasons = {}
    for key in held:
        run = held[key]
        if run.get("refusal_cause") is None:
            continue
        cause = " ".join(("%s" % run["refusal_cause"]).split())[:150]
        reasons[(run["lang"], cause)] = \
            reasons.get((run["lang"], cause), 0) + 1
        continue
    say("| language | cause | cells |")
    say("|---|---|---|")
    for key in sorted(reasons, key=lambda k: (-reasons[k], k)):
        say("| %s | %s | %d |" % (key[0], key[1].replace("|", "/"),
                                  reasons[key]))
        continue
    say("")
    document = {
        "meta": {
            "task": "bb2",
            "what": "the bit-blast circuit of every attested x86 cell "
                    "rendered in the seven interpreted languages and "
                    "run beside the definition at points; an agreement "
                    "is `agreed` and never `proved`",
            "cells": whole,
            "work_ceiling": INTERP_WORK_CEILING,
            "timeout_first": INTERP_TIMEOUT_FIRST,
            "timeout_retry": INTERP_TIMEOUT_RETRY,
            "memory_abort": ABORT_NAME,
        },
        "agreed": {},
    }
    for lang in IR.LANGUAGES:
        document["agreed"][lang] = len(agree_sets[lang])
        continue
    handle = open(INTERP_AGGREGATE, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("wrote %s" % INTERP_AGGREGATE)
    return 0


# ==================================================================
# section 6: the probe -- is there a Swift SDK for riscv64 linux
# ==================================================================

SWIFT_ROOT = "/persist/swift"


def probe(command):
    say("")
    say("$ %s" % " ".join(command))
    try:
        done = subprocess.run(command, capture_output=True, text=True,
                              timeout=300)
    except OSError as problem:
        say("  OSError: %s" % problem.strerror)
        return
    except Exception as problem:                              # noqa: BLE001
        say("  %s: %s" % (type(problem).__name__, problem))
        return
    say("  exit %d" % done.returncode)
    for line in (done.stdout or "").splitlines():
        say("  out: %s" % line)
        continue
    for line in (done.stderr or "").splitlines():
        say("  err: %s" % line)
        continue
    return


def swift_riscv_command():
    """THE PROBE, LITERAL: whether a Swift SDK for riscv64 linux exists
    to install, asked of the toolchain that is in this image and of the
    machine this runs on.  Nothing here is a guess and nothing here
    reaches the network -- the instance is configured `proxy = no`, so
    an answer about what could be DOWNLOADED is a flag for the
    coordinator and not a measurement this lane can make."""
    say("THE SWIFT TOOLCHAIN IN THIS IMAGE")
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swiftc"), "--version"])
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swift"), "--version"])
    say("")
    say("WHAT TARGETS THIS swiftc WILL WRITE FOR: the riscv64 triple, "
        "asked directly")
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swiftc"), "-target",
           "riscv64-unknown-linux-gnu", "-print-target-info"])
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swiftc"), "-target",
           "x86_64-unknown-linux-gnu", "-print-target-info"])
    say("")
    say("THE SDKs THIS TOOLCHAIN HAS INSTALLED, in its own words")
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swift"), "sdk", "list"])
    say("")
    say("THE RUNTIME LIBRARIES ON DISK, one directory per architecture")
    probe(["ls", "-1", os.path.join(SWIFT_ROOT, "usr/lib/swift/linux")])
    probe(["ls", "-1", os.path.join(SWIFT_ROOT, "usr/lib/swift")])
    say("")
    say("WHETHER A COMPILE FOR riscv64 IS ACCEPTED AT ALL: one source, "
        "the ship flags, the riscv64 triple")
    work = os.environ.get("TMPDIR") or "/tmp"
    folder = os.path.join(work, "bb2_swift_riscv")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    source = os.path.join(folder, "probe.swift")
    handle = open(source, "w")
    handle.write("@_cdecl(\"emu_probe\")\n"
                 "public func emu_probe(_ a: UInt64) -> UInt64\n"
                 "{\n"
                 "    let g0: UInt64 = (a >> 0) & 1\n"
                 "    return g0\n"
                 "}\n")
    handle.close()
    probe([os.path.join(SWIFT_ROOT, "usr/bin/swiftc"), "-O", "-c",
           "-target", "riscv64-unknown-linux-gnu", source, "-o",
           os.path.join(folder, "probe.o")])
    say("")
    say("THE NETWORK THIS INSTANCE HAS, so an answer about what could "
        "be fetched is not invented")
    probe(["cat", "/etc/resolv.conf"])
    return 0


# ==================================================================
# section 7: the commands
# ==================================================================

def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    what = argv[1]
    if what == "sizes":
        return sizes_command()
    if what == "sample":
        many = 6
        if len(argv) > 2:
            many = int(argv[2])
        return sample_command(many)
    if what == "cell":
        return cell_command(argv[2], argv[3], argv[4], argv[5:])
    if what == "preflight":
        return preflight_command()
    if what == "run":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return run_command(limit)
    if what == "table":
        return table_command()
    if what == "largest":
        many = 6
        if len(argv) > 2:
            many = int(argv[2])
        return largest_command(many)
    if what == "rows":
        return rows_command()
    if what == "alarms":
        return alarms_command()
    if what == "bank":
        return bank_command()
    if what == "readings":
        return readings_command()
    if what == "readings_before":
        return readings_before_command()
    if what == "bank_before":
        return bank_before_command()
    if what == "interp":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return interp_command(limit)
    if what == "interp_sizes":
        return interp_sizes_command()
    if what == "interp_one":
        ceiling = None
        if len(argv) > 6:
            ceiling = argv[6]
        return interp_one_command(argv[2], argv[3], argv[4], argv[5],
                                  ceiling)
    if what == "interp_retry":
        limit = None
        if len(argv) > 2:
            limit = int(argv[2])
        return interp_retry_command(limit)
    if what == "interp_table":
        return interp_table_command()
    if what == "swift_riscv":
        return swift_riscv_command()
    say("unknown command %r" % what)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
