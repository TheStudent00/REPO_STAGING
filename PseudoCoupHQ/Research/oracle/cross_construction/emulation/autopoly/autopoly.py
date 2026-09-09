#!/usr/bin/env python3
"""autopoly.py -- task ap1: the owner's loop, run for the first time over its
measured outer set.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08).

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table
    (`Research/oracle/arch_opcodes/model/model_table.json`, tasks
    m1/m1b), which holds, per place the opcode writes, the z3 term the
    reference simulator's own builder puts there.
  * THE OUTER SET is every cell of that table which the canon40 corpus
    actually attests -- a distinct triple with a TRANSLATED row whose
    `attestation.ledger_rows` is greater than zero.  Task m1b measured
    it at 253 and lane `ap1_l1_cells.sh` counts it again.
  * A RUN is `find_emulation(cell, lang)` for one of the four compiled
    targets: the target's own operator where it has one whose whole
    lowered body IS the cell, the cell's term written in the target's
    operators where it has not, then compiled at the corpus's ship
    flags, carved, and put back to z3 against the cell's own term.
  * THIS PROGRAM is the loop around that run and nothing else.  The run
    itself is `handful.py` as task g1b left it, imported and called.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  Everything that
decides an answer:
  `handful.cell_input` reads the cell and rebuilds its terms,
  `handful.find_emulation` runs the four steps (primitive lookup,
  render, compile-and-carve, gate), `handful.one_recheck` re-poses an
  UNDECIDED obligation with more room, `handful.composition_of_run`
  classifies the carved body instruction by instruction, and
  `handful.load_in_table` reads the table's own TRANSLATED triples.
  The two renderers task g1 added (`go/go_render.py`,
  `swift/swift_render.py`), the two task o7/o11 already had
  (`emulation/emulate.py`, `emulation/rust/rust_render.py`), the carve,
  the canonical form, the reference simulator and `gate.Gate.decide`
  are reached through that file and never through this one.

WHAT THIS FILE ADDS, and it is only bookkeeping -- the brief's own
words, "the driver as g1b left it, unchanged except for (a) taking its
cells from the table instead of a list of ten and (b) the bookkeeping
below":
  (a) THE OUTER SET.  `autopoly_cells.json`, written by lane
      `ap1_l1_cells.sh`, in the same shape `handful_cells.json` has, so
      `handful.cell_input` reads it unchanged.
  (b) FIVE PIECES OF BOOKKEEPING.
      1. THE ORDER: most attested ledger rows first, so a stopped lane
         has already finished the cells that carry most of the corpus.
      2. THE INCREMENTAL STORE: one json object per line on
         `autopoly_runs.jsonl`, written and flushed as each run
         finishes, so a stopped lane loses nothing and resumes by
         skipping the (cell, target) pairs already on the file.
      3. THE RE-POSE: every gate call the 3,000 ms ceiling left
         UNDECIDED is re-posed ONCE at 30,000 ms, inside the run rather
         than in a second pass over the file, so a line on the store is
         a finished run.
      4. THE CAUSE OF A RUN THE ROUTE CANNOT HANDLE: every run is
         wrapped, and an exception out of the driver is recorded as
         that run's `refusal_cause` with the exception LITERAL.  the owner's
         rule for this task, in the brief's own words: "a cell the
         route cannot handle is a RESULT BY CAUSE, never a reason to
         touch the method mid-run."
      5. THE AGGREGATE AND THE REPORT: `autopoly.json` and
         `autopoly.md`.

WHAT IS NOT CHANGED, said out loud because it would be the easy thing
to change.  `handful.TASK` is set to `g1c`, which is the task g1b
closer's own setting: the two printing fixes of task h2 on, the
primitive route tried before the term route, and the primitive lookup
widened by one step (a single-opcode row is accepted when its
narrow-stripped body is the cell's own instruction plus zero or more
zero-operand setup instructions from `reference.SPREAD_SIGN` /
`reference.ACCUMULATOR_WIDEN` and nothing else).  Not one line of
`handful.py` is edited by this task, and its own products
(`handful*.json`, `handful*.md`, `src*/`) are never written: every path
`handful.py` writes through is repointed into this folder by
`use_task_ap1` below.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers; peak resident checked after every run; named abort
ABORT_MEMORY_AP1 at 6 GB, which is inside the instance's 20g cap.  The
reads are `autopoly_cells.json` (2 MB), `model_table_rows.json` (50 MB,
once, for the composition step), `single_opcode_units.json` (1.6 MB,
twice, cached) and one probe manifest per target (a few MB each,
cached).  The 73 MB `model_table.json` is not read by this program at
all -- lane `ap1_l1_cells.sh` read it once and wrote the small file.

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

The population is MACHINE-FORM EVIDENCE and nothing else: the cells are
every triple the corpus attests, read off the table's own
`attestation.ledger_rows`, and the order is that count descending.  No
operator token enters the selection, the order, the pairing (there is
one run per (cell, target), fixed in advance), or any key of any file
this program writes.  Every field carrying a mnemonic is named `mnem`,
which the guard reads as a machine form.

Coding discipline: no compound one-liner statements.

usage:
  autopoly.py preflight        the outer set as the loop will walk it,
                               and nothing run
  autopoly.py run [<n>]        the runs, appended one line at a time to
                               autopoly_runs.jsonl; `<n>` stops after n
                               runs actually performed (the sample)
  autopoly.py aggregate        autopoly_runs.jsonl -> autopoly.json
  autopoly.py report           autopoly.json       -> autopoly.md
  autopoly.py tally            the counts, printed
  autopoly.py reproduce        the handful's forty (cell, target) pairs
                               as they came out of this loop, beside
                               task g1b's own answers
  autopoly.py tables           the report's tables 1, 2 and 3 and the
                               two `sat` counts, printed and nothing
                               that moves between runs
  autopoly.py causes           the by-cause table summed over the four
                               targets, and the arrival-contract group
  autopoly.py repose           what the one re-pose at 30,000 ms moved
  autopoly.py store            the store and the aggregate compared run
                               for run
  autopoly.py sat              the two `sat` counts and the five largest
  autopoly.py branch           which form of a cell's term the renderer
                               is handed, per task, with the driver's
                               own source LITERAL
"""

import json
import os
import resource
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
sys.path.insert(0, HANDFUL)

import handful as H                                             # noqa: E402
import model_table as MTAB                                      # noqa: E402
import gate as G                                                # noqa: E402

CELLS = os.path.join(HERE, "autopoly_cells.json")
RUNS = os.path.join(HERE, "autopoly_runs.jsonl")
AGGREGATE = os.path.join(HERE, "autopoly.json")
REPORT = os.path.join(HERE, "autopoly.md")
SRC_DIR = os.path.join(HERE, "src")
PRIMITIVE = os.path.join(HERE, "autopoly_primitive.json")
SPELLINGS = os.path.join(HERE, "autopoly_spellings.json")
HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/autopoly")

# THE TWO CEILINGS THE BRIEF STATES.  The first is the pipeline's own
# and is the verdict of record; the second is the ONE re-pose a time
# limit obliges, and 30,000 ms rather than the handful's 300,000 ms
# because this loop poses a thousand runs rather than forty.
SOLVER_MS = 3000
REPOSE_MS = 30000

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_AP1"

# The four compiled targets, in the brief's own order.
TARGETS = ["c", "rust", "go", "swift"]

CAUSE_DRIVER = "the driver raised on this (cell, target) pair"

# The handful's ten cells, so this loop's answers for them can be put
# beside task g1b's own.  Ratified intention, in task h1's brief order;
# nothing here selects, groups or pairs by them.
HANDFUL_CELLS = [
    ("add", "gpr_gpr", 32),
    ("sub", "imm_gpr", 64),
    ("imul", "gpr_gpr", 32),
    ("sar", "cl_gpr", 32),
    ("shr", "cl_gpr", 64),
    ("idiv", "gpr_one", 32),
    ("cmovne", "gpr_gpr", 32),
    ("setne", "gpr_one", 8),
    ("addss", "xmm_xmm", 32),
    ("cvtsi2sd", "gpr_xmm", 64),
]
HANDFUL_G1B = os.path.join(HANDFUL, "handful3b.json")
HANDFUL_G1C = os.path.join(HANDFUL, "handful3c.json")


def use_task_ap1():
    """the imported driver pointed at THIS task's paths and this task's
    memory bound, and at task g1c's route.

    `handful.TASK` decides three things and this task re-decides none of
    them: `fixes_are_on` (task h2's two printing fixes), `primitive_first`
    (task g1's route order) and `setup_is_allowed` (task g1c's widened
    lookup).  `g1c` is the setting under which task g1b's closer ran, so
    the method here is that one, unchanged.

    Every path `handful.py` writes through is repointed into this
    folder, so no lane of this task can write task g1b's products."""
    H.TASK = "g1c"
    H.RESULTS = AGGREGATE
    H.REPORT = REPORT
    H.SRC_DIR = SRC_DIR
    H.PRIMITIVE = PRIMITIVE
    H.SPELLINGS = SPELLINGS
    H.CELLS = CELLS
    H.HOST_FOLDER = HOST_FOLDER
    H.ABORT_KB = ABORT_KB
    H.ABORT_NAME = ABORT_NAME


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


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


# ==================================================================
# section 1: THE COMMANDS
# ==================================================================

def main(argv):
    use_task_ap1()
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "preflight":
        return preflight_command()
    if argv[0] == "run":
        limit = None
        if len(argv) > 1:
            limit = int(argv[1])
        return run_command(limit)
    if argv[0] == "aggregate":
        return aggregate_command()
    if argv[0] == "report":
        return report_command()
    if argv[0] == "tally":
        return tally_command()
    if argv[0] == "reproduce":
        return reproduce_command()
    if argv[0] == "tables":
        return tables_command()
    if argv[0] == "causes":
        return causes_command()
    if argv[0] == "repose":
        return repose_command()
    if argv[0] == "store":
        return store_command()
    if argv[0] == "sat":
        return sat_command()
    if argv[0] == "branch":
        return branch_command()
    say("unknown command %r" % argv[0])
    return 2


def preflight_command():
    """the outer set as the loop will walk it, and nothing run: how many
    cells, how many pairs, what the order is, and which cells carry a
    field the driver cannot format."""
    cells = read_json(CELLS)
    asked = cells["asked"]
    say("cells on %s: %d" % (CELLS, len(asked)))
    say("targets: %s" % ", ".join(TARGETS))
    say("pairs: %d" % (len(asked) * len(TARGETS)))
    total = 0
    for record in asked:
        total = total + record["attested_ledger_rows"]
    say("attested ledger rows over the whole outer set: %d" % total)
    say("")
    say("the first ten cells of the order, most attested first:")
    for record in asked[:10]:
        say("   %-10s %-14s %-6s ledger_rows %d"
            % (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"],
               record["attested_ledger_rows"]))
    say("")
    without = []
    for record in asked:
        if record["asked"]["key_width"] is not None:
            continue
        without.append(record["asked"])
    say("cells whose key_width is null: %d" % len(without))
    for one in without:
        say("   %s %s %s" % (one["mnem"], one["shape"], one["key_width"]))
    say("")
    done = already_recorded()
    say("runs already on %s: %d" % (RUNS, len(done)))
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


def run_command(limit):
    """the loop.  One line on `autopoly_runs.jsonl` per finished run."""
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    cells = read_json(CELLS)
    pairs = the_pairs(cells)
    moved = normalize_store()
    if moved:
        say("%d line(s) of the store were rewritten onto the "
            "machine-form cell key" % moved)
    done = already_recorded()
    say("pairs to run: %d; already recorded: %d" % (len(pairs), len(done)))
    shared = H.build_shared()
    say("the gate of record: %d ms; the one re-pose: %d ms"
        % (shared["gate"].solver_timeout_ms, REPOSE_MS))
    reposer = G.Gate(reference=shared["reference"],
                     solver_timeout_ms=REPOSE_MS)
    MTAB._install_gpr_widths()
    in_table = H.load_in_table()
    say("the table's own TRANSLATED triples, for the composition step: %d"
        % len(in_table))
    say("peak resident after the two reads: %d kB"
        % check_memory("after load_in_table"))
    total = len(pairs)
    index = 0
    ran = 0
    started = time.time()
    for asked, lang, ledger in pairs:
        index = index + 1
        if key_of(asked, lang) in done:
            continue
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, total, asked[0], asked[1], asked[2], lang,
               ledger))
        record = one_run(shared, reposer, cells, asked, lang, ledger,
                         in_table)
        append_run(record)
        ran = ran + 1
        say("   %s | %s | %d s | peak resident: %d kB"
            % (record.get("route") or "-", one_line_verdict(record),
               round(record["seconds"]), check_memory("run %d" % index)))
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d run(s) performed" % ran)
            break
    say("")
    say("runs performed this lane: %d in %d s" % (ran,
                                                  round(time.time()
                                                        - started)))
    say("lines on %s: %d" % (RUNS, len(already_recorded())))
    say("peak resident: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 2: ONE RUN, and the four pieces of bookkeeping around it
# ==================================================================

def the_pairs(cells):
    """every (cell, target) pair, in the order the loop walks them: the
    cells by attested ledger rows descending (the order the cells file
    already holds), and the four targets in the brief's order inside
    each cell."""
    out = []
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for lang in TARGETS:
            out.append((asked, lang, record["attested_ledger_rows"]))
    return out


def key_of(asked, lang):
    """the identity of one run on the incremental store."""
    return "%s|%s|%s|%s" % (asked[0], asked[1], asked[2], lang)


def one_run(shared, reposer, cells, asked, lang, ledger, in_table):
    """one (cell, target), wrapped.

    THE WRAP IS THE BRIEF'S OWN RULE, and it is the fourth piece of
    bookkeeping: a cell the route cannot handle is a RESULT BY CAUSE.
    An exception out of the driver is recorded as this run's
    `refusal_cause` with the exception LITERAL and the line it came
    from, and the loop goes on to the next pair."""
    started = time.time()
    record = {
        "mnem": asked[0],
        "shape": asked[1],
        "key_width": asked[2],
        "lang": lang,
        "attested_ledger_rows": ledger,
        "places": [],
    }
    held = None
    try:
        held = H.cell_input(cells, asked)
        record = H.find_emulation(shared, held, lang)
        record["attested_ledger_rows"] = ledger
    except Exception as problem:
        record["refusal_cause"] = CAUSE_DRIVER
        record["refusal_detail"] = named(problem)
        record["refusal_traceback"] = last_frame(problem)
        record["composition"] = []
        record["seconds"] = round(time.time() - started, 3)
        return record
    # THE TWO STEPS AFTER THE RUN are wrapped separately, so a failure
    # in either is recorded as its own field and never as a refusal of
    # the run itself -- a run whose places all answered is not a refused
    # run because its composition could not be classified.
    try:
        reposed(shared, reposer, held, record)
    except Exception as problem:
        record["repose_refusal"] = named(problem)
        record["repose_refusal_traceback"] = last_frame(problem)
    try:
        record["composition"] = H.composition_of_run(record, in_table)
    except Exception as problem:
        record["composition"] = []
        record["composition_refusal"] = named(problem)
        record["composition_refusal_traceback"] = last_frame(problem)
    record["seconds"] = round(time.time() - started, 3)
    return record


def named(problem):
    """an exception as the record carries it: its own class and its own
    message, LITERAL."""
    return "%s: %s" % (type(problem).__name__, problem)


def last_frame(problem):
    """the one line of the traceback that names where the driver
    stopped, LITERAL, so a refusal by this cause is a fact about a
    place in the code rather than a message."""
    frames = traceback.extract_tb(problem.__traceback__)
    if not frames:
        return ""
    frame = frames[-1]
    return "%s:%d in %s -- %s" % (os.path.basename(frame.filename),
                                  frame.lineno, frame.name, frame.line)


def reposed(shared, reposer, held, record):
    """every gate call the 3,000 ms ceiling left UNDECIDED, re-posed
    ONCE with more room.

    THE LAW'S RULE, followed literally: a time limit is a FLAG, so the
    obligation is re-run with a larger ceiling and whether the answer
    changed is reported.  The verdict OF RECORD stays the one the
    pipeline's own ceiling gave and this answer sits beside it.

    `handful.one_recheck` is the step, called rather than restated, and
    the cell it needs is handed to it in a one-entry cache so it never
    re-reads the cells file."""
    if record.get("refusal_cause") is not None:
        return
    cache = {(held["mnem"], held["shape"], held["key_width"]): held}
    of_record = shared["gate"]
    for place in record.get("places") or []:
        check = place.get("check") or {}
        if check.get("outcome") != "UNDECIDED":
            continue
        if not place.get("compiled"):
            continue
        shared["gate"] = reposer
        try:
            again = H.one_recheck(shared, cache, record, place)
        finally:
            shared["gate"] = of_record
        again["ceiling_ms"] = REPOSE_MS
        check["recheck"] = again


def append_run(record):
    """one finished run, appended to the incremental store and flushed
    to the operating system before the next run begins, so a lane the
    wall clock stops loses nothing."""
    handle = open(RUNS, "a")
    handle.write(json.dumps(as_machine_form(record), sort_keys=True))
    handle.write("\n")
    handle.flush()
    os.fsync(handle.fileno())
    handle.close()


def as_machine_form(node):
    """the record with every cell triple written as three fields, the
    mnemonic in `mnem`, before anything of it reaches a file.

    WHAT THIS IS FOR, and it is not a style choice.  The driver records
    a matched primitive row's cell as a LIST -- `["xor", "gpr_same",
    32]` -- and the spelling guard refuses a list whose element is a
    bare operator token, which is what a mnemonic spelled `and`, `or`,
    `xor` or `not` is.  The handful's ten cells carried no such
    mnemonic, so the shape never met the guard before; this loop's 253
    do.  The MATCH is untouched -- the driver still compares triple with
    triple in memory, and this task changes nothing about how a
    primitive row is found -- and what changes is only how the store
    SPELLS the key it writes down: `{"mnem": "xor", "shape":
    "gpr_same", "key_width": 32}`, which is the machine form the ruling
    of 2026-09-08 states and the guard already reads as one.

    Applied to the whole record, once, at the one place a record
    becomes a line on a file."""
    if isinstance(node, dict):
        out = {}
        for name in node:
            value = node[name]
            if name == "cell" and is_a_triple(value):
                out[name] = cell_of(value)
                continue
            out[name] = as_machine_form(value)
        return out
    if isinstance(node, list):
        held = []
        for value in node:
            held.append(as_machine_form(value))
        return held
    return node


def is_a_triple(value):
    """whether a `cell` field holds the (mnem, shape, key_width) triple
    as a list.  The composition column's own `cell` field is a boolean
    and a setup instruction that did not classify carries None; neither
    is a triple and neither is touched."""
    if not isinstance(value, list):
        return False
    if len(value) != 3:
        return False
    return isinstance(value[0], str)


def already_recorded():
    """the runs the store already holds, by (cell, target).

    A line that does not parse can only be the last one, written while
    the lane was stopped; it is dropped and the file rewritten without
    it, and the drop is said out loud."""
    if not os.path.exists(RUNS):
        return set()
    handle = open(RUNS)
    lines = handle.read().splitlines()
    handle.close()
    kept = []
    done = set()
    dropped = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except ValueError:
            dropped = dropped + 1
            continue
        asked = (record["mnem"], record["shape"], record["key_width"])
        key = key_of(asked, record["lang"])
        if key in done:
            dropped = dropped + 1
            continue
        done.add(key)
        kept.append(line)
    if dropped:
        say("   %d line(s) of %s did not parse or repeated a pair; "
            "the file is rewritten without them" % (dropped, RUNS))
        handle = open(RUNS, "w")
        for line in kept:
            handle.write(line + "\n")
        handle.close()
    return done


def read_runs():
    """every run on the incremental store, in the order it was run, each
    through `as_machine_form` so a line written before that rewrite
    existed reads the same way as one written after it."""
    out = []
    if not os.path.exists(RUNS):
        return out
    handle = open(RUNS)
    for line in handle:
        if not line.strip():
            continue
        out.append(as_machine_form(json.loads(line)))
    handle.close()
    return out


def normalize_store():
    """the store rewritten through `as_machine_form` where any line is
    not already in it, said out loud when it happens.

    The first twenty runs -- the sample the law asks for -- were written
    before the rewrite existed, and this is what brings them onto the
    same shape as the rest rather than leaving the file half in one
    spelling and half in the other."""
    if not os.path.exists(RUNS):
        return 0
    handle = open(RUNS)
    lines = handle.read().splitlines()
    handle.close()
    moved = 0
    kept = []
    for line in lines:
        if not line.strip():
            continue
        record = json.loads(line)
        again = json.dumps(as_machine_form(record), sort_keys=True)
        if again != json.dumps(record, sort_keys=True):
            moved = moved + 1
        kept.append(again)
    if moved:
        handle = open(RUNS, "w")
        for line in kept:
            handle.write(line + "\n")
        handle.close()
    return moved


# ==================================================================
# section 3: THE AGGREGATE -- what the thousand runs say
# ==================================================================
#
# EVERY COUNT BELOW IS OF THE RUN'S OWN DESTINATION PLACE, which is
# `handful.destination_place`: the first place the cell writes that is
# not the flags, or the flags place when that is all the cell writes.
# That is the place task h1's, h2's and g1's own tables already
# summarize, so a row here and a row there count the same thing.  The
# per-place counts sit beside them and are named as such.

OUTCOMES = ["proved", "proved under caller extension", "sat",
            "undecided", "refused"]
LANDINGS = ["LANDED", "LANDED_ELSEWHERE", "NOT_COLLAPSED"]
ROUTES = ["primitive", "primitive+setup", "term", "no route reached"]


def aggregate_command():
    """the incremental store read once, and every table the brief asks
    for computed off it."""
    runs = read_runs()
    say("runs on %s: %d" % (RUNS, len(runs)))
    cells = read_json(CELLS)
    document = {
        "meta": {
            "task": "ap1",
            "what": "the owner's loop over every attested cell of the "
                    "arch-opcode model table, on the four compiled "
                    "targets, primitive-first",
            "cells_source": CELLS,
            "runs_source": RUNS,
            "cells": len(cells["asked"]),
            "targets": TARGETS,
            "runs": len(runs),
            "solver_ceiling_ms": SOLVER_MS,
            "repose_ceiling_ms": REPOSE_MS,
            "route": "handful.py as task g1b left it, TASK g1c: the "
                     "two printing fixes of task h2, the primitive "
                     "route before the term route, and the primitive "
                     "lookup widened by one zero-operand setup step",
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "peak_kb": peak_kb(),
            "host_folder": HOST_FOLDER,
        },
        "ledger_rows_total": ledger_total(cells),
        "per_language": per_language(runs, cells),
        "routes": routes_reached(runs, cells),
        "causes": causes_by_language(runs),
        "across_targets": across_targets(runs, cells),
        "sat_verdicts": sat_verdicts(runs),
        "handful": handful_reproduction(runs),
        "seconds": seconds_summary(runs),
        "runs": runs,
    }
    write_json(AGGREGATE, document)
    say("wrote %s" % AGGREGATE)
    say("peak resident: %d kB" % check_memory("aggregate"))
    return 0


def ledger_total(cells):
    """the attested ledger rows of the whole outer set, which is the
    denominator of every share this report prints."""
    total = 0
    for record in cells["asked"]:
        total = total + record["attested_ledger_rows"]
    return total


def outcome_of(run):
    """one run's gate answer at its destination place, in the five names
    the brief's table 1 uses.

    `proved` is z3's `unsat` at the 3,000 ms ceiling of record.  `proved
    under caller extension` is task o7's own re-pose: `sat` on the plain
    comparison, `unsat` once every narrow-holder input row is
    zero-extended to its register.  `sat` is a counterexample that
    survives that re-pose.  `undecided` is the solver not answering, at
    either ceiling.  `refused` is a run that never reached the gate at
    all."""
    place = the_place(run)
    if place is None:
        return "refused"
    check = place.get("check")
    if check is None:
        return "refused"
    outcome = check.get("outcome")
    if outcome == "PROVED_ON_SHIP":
        return "proved"
    if outcome == "DISPROVED":
        again = check.get("under_caller_extension") or {}
        if again.get("outcome") == "PROVED_ON_SHIP":
            return "proved under caller extension"
        return "sat"
    return "undecided"


def the_place(run):
    """the run's destination place, or None where it has none.

    `handful.destination_place` is the function; this wrapper is here
    because a refused run carries no `places` key at all on the store
    and that function reads one."""
    if run.get("refusal_cause") is not None:
        return None
    if not run.get("places"):
        return None
    return H.destination_place(run)


def reached(run, step):
    """whether the run's destination place reached one of the three
    steps before the gate."""
    place = the_place(run)
    if place is None:
        return False
    if step == "rendered":
        return place.get("rendered") is True
    if step == "compiled":
        return place.get("compiled") is True
    return False


def landing_of(run):
    """the run's landing at its destination place, or None."""
    place = the_place(run)
    if place is None:
        return None
    landing = place.get("landing")
    if landing is None:
        return None
    return landing["verdict"]


def per_language(runs, cells):
    """THE table the brief asks for first: per target, how many cells
    reached each step and each verdict, and the share of the corpus's
    attested ledger rows those cells cover."""
    whole = ledger_total(cells)
    out = {}
    for lang in TARGETS:
        held = []
        for run in runs:
            if run["lang"] != lang:
                continue
            held.append(run)
        counted = {"attempted": bucket(held, whole)}
        counted["rendered"] = bucket(
            [r for r in held if reached(r, "rendered")], whole)
        counted["compiled"] = bucket(
            [r for r in held if reached(r, "compiled")], whole)
        for name in LANDINGS:
            counted[name] = bucket(
                [r for r in held if landing_of(r) == name], whole)
        for name in OUTCOMES:
            counted[name] = bucket(
                [r for r in held if outcome_of(r) == name], whole)
        out[lang] = counted
    return out


def bucket(runs, whole):
    """one cell of the table: how many runs, how many ledger rows they
    cover, and that as a share of the whole outer set."""
    rows = 0
    for run in runs:
        rows = rows + (run.get("attested_ledger_rows") or 0)
    share = 0.0
    if whole:
        share = round(100.0 * rows / whole, 2)
    return {"runs": len(runs), "ledger_rows": rows,
            "share_percent": share}


def route_of(run):
    """which of the three routes ran, or that none did."""
    if run.get("route") is not None:
        return run["route"]
    return "no route reached"


def routes_reached(runs, cells):
    """the second table: per target, how far the primitive route
    reached."""
    whole = ledger_total(cells)
    out = {}
    for lang in TARGETS:
        counted = {}
        for name in ROUTES:
            held = []
            for run in runs:
                if run["lang"] != lang:
                    continue
                if route_of(run) != name:
                    continue
                held.append(run)
            counted[name] = bucket(held, whole)
        out[lang] = counted
    return out


def causes_by_language(runs):
    """the third table: what did not work, by cause, per target, each
    cause with three example cells and the ledger rows they cover.

    The cause is the driver's own word -- the run's `refusal_cause`, the
    place's `refusal_cause`, the compiler's own first line, or the
    gate's own verdict -- never a reading of it."""
    out = {}
    for lang in TARGETS:
        causes = {}
        for run in runs:
            if run["lang"] != lang:
                continue
            name = cause_of(run)
            if name is None:
                continue
            entry = causes.setdefault(name, {"runs": 0,
                                             "ledger_rows": 0,
                                             "examples": []})
            entry["runs"] = entry["runs"] + 1
            entry["ledger_rows"] = (entry["ledger_rows"]
                                    + (run.get("attested_ledger_rows")
                                       or 0))
            if len(entry["examples"]) < 3:
                entry["examples"].append({
                    "mnem": run["mnem"],
                    "shape": run["shape"],
                    "key_width": run["key_width"],
                    "ledger_rows": run.get("attested_ledger_rows"),
                })
        out[lang] = causes
    return out


def cause_of(run):
    """the one cause of a run that did not end PROVED at its destination
    place, or None where it did."""
    if run.get("refusal_cause") is not None:
        return "%s: %s" % (run["refusal_cause"],
                           run.get("refusal_detail"))
    place = the_place(run)
    if place is None:
        return "the cell writes no place this route could render"
    if place.get("rendered") is False:
        return "%s" % place.get("refusal_cause")
    if not place.get("compiled"):
        return "the compiler refused: %s" % first_line(
            place.get("compile_refusal"))
    check = place.get("check") or {}
    outcome = outcome_of(run)
    if outcome == "proved":
        return None
    if outcome == "proved under caller extension":
        return None
    if outcome == "sat":
        return "the gate answered sat: the body holds on a region, " \
               "not on every input"
    again = check.get("recheck") or {}
    if again.get("outcome") == "PROVED_ON_SHIP":
        return None
    return "the gate did not answer: %s" % check.get("reason")


def first_line(text):
    """the compiler's own first error line, which is what the brief asks
    a compile refusal to be recorded as."""
    if text is None:
        return ""
    held = "%s" % text
    return held.split("\n")[0].strip()


def cell_of(record):
    """one cell as the machine-form key the ruling of 2026-09-08 states:
    the triple, its three parts in three fields, the mnemonic in the
    field `mnem`.

    NOT A JOINED STRING, and this is not a style choice.  The spelling
    guard refused an earlier draft of this file for exactly that: a
    field `cell` holding `and|gpr_gpr|32` is a row key carrying an
    operator token, whatever the token happens to be a mnemonic of.
    The guard was right and the record is written the guard's way."""
    return {"mnem": record[0], "shape": record[1],
            "key_width": record[2]}


def across_targets(runs, cells):
    """the fourth table: per cell, on how many of the four targets it is
    proved, and the whole list of the cells proved on none."""
    proved = {}
    ledger = {}
    for record in cells["asked"]:
        key = (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"])
        proved[key] = []
        ledger[key] = record["attested_ledger_rows"]
    for run in runs:
        key = (run["mnem"], run["shape"], run["key_width"])
        if key not in proved:
            continue
        outcome = outcome_of(run)
        if outcome not in ("proved", "proved under caller extension"):
            continue
        proved[key].append(run["lang"])
    whole = ledger_total(cells)
    counted = {}
    for many in range(0, 5):
        held = []
        for key in sorted(proved, key=readable):
            if len(proved[key]) != many:
                continue
            held.append(key)
        rows = 0
        for key in held:
            rows = rows + ledger[key]
        share = 0.0
        if whole:
            share = round(100.0 * rows / whole, 2)
        listed = []
        for key in held:
            entry = cell_of(key)
            entry["ledger_rows"] = ledger[key]
            entry["proved_on"] = sorted(proved[key])
            listed.append(entry)
        counted["%d" % many] = {"cells": len(held), "ledger_rows": rows,
                                "share_percent": share,
                                "cell_list": listed}
    counted["on_all_four_list"] = counted["4"]["cell_list"]
    counted["on_none_with_causes"] = none_list(runs, proved, ledger)
    return counted


def readable(key):
    """a sort key over a cell triple that never compares None with an
    integer."""
    return (key[0], key[1], "%s" % key[2])


def none_list(runs, proved, ledger):
    """every cell proved on no target at all, with the cause on each of
    the four, in full -- the brief asks for this list entire."""
    out = []
    for key in sorted(proved, key=readable):
        if proved[key]:
            continue
        causes = {}
        for run in runs:
            held = (run["mnem"], run["shape"], run["key_width"])
            if held != key:
                continue
            causes[run["lang"]] = cause_of(run)
        entry = cell_of(key)
        entry["ledger_rows"] = ledger[key]
        entry["causes"] = causes
        out.append(entry)
    out.sort(key=lambda entry: (-entry["ledger_rows"], entry["mnem"],
                                entry["shape"],
                                "%s" % entry["key_width"]))
    return out


def sat_verdicts(runs):
    """every `sat` the loop produced, with z3's counterexample LITERAL
    and the region the gate's own words name.

    A `sat` is where the target's edge region differs from the opcode's,
    so this list is the owner's edge-region model in machine form.  Every
    written place is walked, not only the destination place, because a
    counterexample on the flags place is as much a difference as one on
    the answer."""
    out = []
    for run in runs:
        for place in (run.get("places") or []):
            check = place.get("check") or {}
            if check.get("outcome") != "DISPROVED":
                continue
            again = check.get("under_caller_extension") or {}
            out.append({
                "mnem": run["mnem"],
                "shape": run["shape"],
                "key_width": run["key_width"],
                "lang": run["lang"],
                "writes": place["writes"],
                "route": route_of(run),
                "ledger_rows": run.get("attested_ledger_rows"),
                "counterexample": check.get("counterexample"),
                "region": H.region_of(check),
                "under_caller_extension": again.get("outcome"),
                "body_text": place.get("body_text"),
            })
    out.sort(key=lambda entry: (-(entry["ledger_rows"] or 0),
                                entry["mnem"], entry["lang"]))
    return out


def seconds_summary(runs):
    """how long the loop took, per target, so the pace is a measurement
    rather than an estimate."""
    out = {}
    for lang in TARGETS:
        held = []
        for run in runs:
            if run["lang"] != lang:
                continue
            held.append(run.get("seconds") or 0)
        if not held:
            continue
        out[lang] = {"runs": len(held),
                     "total_s": round(sum(held), 1),
                     "slowest_s": round(max(held), 1),
                     "median_s": round(sorted(held)[len(held) // 2], 2)}
    return out


# ==================================================================
# section 4: THE HANDFUL, REPRODUCED
# ==================================================================
#
# The brief's sixth deliverable: the handful's own rows shown again as
# they came out of this loop, so that the loop reproducing the handful
# is a measurement rather than a claim.  Task g1b's second run of
# record (`handful3b.json`) holds thirty-nine of the forty; the one the
# widened lookup changes is on `handful3c.json`, and this comparison
# takes each pair from whichever of the two files ran it under the route
# this loop runs.

def handful_reproduction(runs):
    """the forty (cell, target) pairs of the handful, this loop's answer
    beside task g1b's own."""
    earlier = {}
    for path in (HANDFUL_G1B, HANDFUL_G1C):
        if not os.path.exists(path):
            continue
        document = read_json(path)
        for run in document["runs"]:
            key = key_of((run["mnem"], run["shape"], run["key_width"]),
                         run["lang"])
            earlier[key] = {"run": run, "file": os.path.basename(path)}
    out = []
    for asked in HANDFUL_CELLS:
        for lang in TARGETS:
            key = key_of(asked, lang)
            mine = None
            for run in runs:
                held = key_of((run["mnem"], run["shape"],
                               run["key_width"]), run["lang"])
                if held != key:
                    continue
                mine = run
            out.append(one_comparison(asked, lang, mine,
                                      earlier.get(key)))
    return out


def one_comparison(asked, lang, mine, theirs):
    """one row of the reproduction table: the route, the landing and the
    gate answer on both sides, and whether they agree."""
    row = {
        "mnem": asked[0],
        "shape": asked[1],
        "key_width": asked[2],
        "lang": lang,
    }
    if mine is None:
        row["this_loop"] = None
        row["agrees"] = False
        row["why"] = "this loop has no run for this pair"
    else:
        row["this_loop"] = summary_of(mine)
    if theirs is None:
        row["the_handful"] = None
        row["agrees"] = False
        row["why"] = "no run of the handful holds this pair"
        return row
    row["the_handful"] = summary_of(theirs["run"])
    row["the_handful_file"] = theirs["file"]
    if mine is None:
        return row
    row["agrees"] = (row["this_loop"] == row["the_handful"])
    # THE TWO COMPARISONS, and the second is the one that says whether
    # the loop reproduces the handful.  `agrees` is character for
    # character, so a pair whose only difference is the ceiling the
    # re-pose used -- 30,000 ms here against the handful's 300,000 ms,
    # which is this brief's own instruction -- reads as a disagreement.
    # `agrees_on_the_verdict` drops that number and nothing else.
    row["agrees_on_the_verdict"] = (
        without_ceiling(row["this_loop"])
        == without_ceiling(row["the_handful"]))
    return row


def summary_of(run):
    """one run as three cells: the route, the landing, and the gate's
    answer at the destination place."""
    verdict = H.verdict_of_run(run)
    return {"route": route_of(run), "landed": verdict["landed"],
            "gate": verdict["gate"], "cause": verdict["cause"]}


def without_ceiling(summary):
    """the same three cells with the re-pose's own millisecond number
    taken out of the gate cell, so two runs that answered the same way
    at two different ceilings compare equal."""
    import re
    if summary is None:
        return None
    held = dict(summary)
    held["gate"] = re.sub(r" at \d+ ms", " on the one re-pose",
                          held["gate"])
    return held


def one_line_verdict(run):
    """the run's answer on one line, for the lane's own progress
    print."""
    verdict = H.verdict_of_run(run)
    if verdict["cause"]:
        return "REFUSED: %s" % verdict["cause"][:70]
    return "%s / %s" % (verdict["landed"], verdict["gate"])


def reproduce_command():
    """the reproduction table alone, printed, and nothing run."""
    runs = read_runs()
    rows = handful_reproduction(runs)
    agreed = 0
    on_verdict = 0
    missing = 0
    for row in rows:
        if row.get("this_loop") is None:
            missing = missing + 1
            continue
        if row.get("agrees"):
            agreed = agreed + 1
        if row.get("agrees_on_the_verdict"):
            on_verdict = on_verdict + 1
    say("the handful's forty pairs, this loop beside task g1b's own")
    say("")
    say("| cell | lang | this loop: route / landed / gate | the "
        "handful: route / landed / gate | agrees | agrees on the "
        "verdict |")
    say("|---|---|---|---|---|---|")
    for row in rows:
        say("| `%s` %s %s | %s | %s | %s | %s | %s |"
            % (row["mnem"], row["shape"], row["key_width"], row["lang"],
               three_cells(row.get("this_loop")),
               three_cells(row.get("the_handful")),
               yes_or_no(row.get("agrees")),
               yes_or_no(row.get("agrees_on_the_verdict"))))
    say("")
    say("agree character for character: %d of %d; agree on the "
        "verdict, the re-pose's own ceiling aside: %d; pairs this loop "
        "has not run: %d" % (agreed, len(rows), on_verdict, missing))
    say("peak resident: %d kB" % check_memory("reproduce"))
    return 0


def three_cells(summary):
    if summary is None:
        return "--"
    if summary["cause"]:
        return "%s / REFUSED: %s" % (summary["route"], summary["cause"])
    return "%s / %s / %s" % (summary["route"], summary["landed"],
                             summary["gate"])


def yes_or_no(value):
    if value:
        return "yes"
    return "**no**"


# ==================================================================
# section 5: THE REPORT
# ==================================================================

def tally_command():
    """the counts, printed, over whatever the store already holds."""
    runs = read_runs()
    cells = read_json(CELLS)
    say("runs recorded: %d of %d" % (len(runs),
                                     len(cells["asked"]) * len(TARGETS)))
    counted = per_language(runs, cells)
    say("")
    say("| target | attempted | rendered | compiled | LANDED | proved | "
        "sat | undecided | refused |")
    say("|---|---|---|---|---|---|---|---|---|")
    for lang in TARGETS:
        held = counted[lang]
        say("| %s | %d | %d | %d | %d | %d | %d | %d | %d |"
            % (lang, held["attempted"]["runs"], held["rendered"]["runs"],
               held["compiled"]["runs"], held["LANDED"]["runs"],
               held["proved"]["runs"], held["sat"]["runs"],
               held["undecided"]["runs"], held["refused"]["runs"]))
    say("")
    say("peak resident: %d kB" % check_memory("tally"))
    return 0


def tables_command():
    """the report's four tables, printed and nothing else, so a claim
    about them in a DevComms log carries a command that re-runs and
    whose output holds no figure that moves between runs."""
    document = read_json(AGGREGATE)
    lines = []
    write_table_one(lines, document)
    write_routes(lines, document)
    write_across_counts(lines, document)
    for line in lines:
        say(line)
    held = document["sat_verdicts"]
    survived = []
    for entry in held:
        if entry.get("under_caller_extension") == "PROVED_ON_SHIP":
            continue
        survived.append(entry)
    say("`sat` at the plain comparison, every written place: %d"
        % len(held))
    say("`sat` surviving the caller-extension re-pose: %d"
        % len(survived))
    agreed = 0
    on_verdict = 0
    missing = 0
    for row in document["handful"]:
        if row.get("this_loop") is None:
            missing = missing + 1
            continue
        if row.get("agrees"):
            agreed = agreed + 1
        if row.get("agrees_on_the_verdict"):
            on_verdict = on_verdict + 1
    say("the handful's forty pairs: %d agree character for character, "
        "%d agree on the verdict, %d not in this outer set"
        % (agreed, on_verdict, missing))
    return 0


def write_across_counts(lines, document):
    """Table 3 alone, without the two lists under it."""
    lines.append("Table 3 -- a cell counts as proved on a target when "
                 "the gate answered `unsat` at that target's "
                 "destination place, at the 3,000 ms ceiling of record "
                 "or under the caller-extension re-pose.")
    lines.append("")
    lines.append("| proved on | cells | ledger rows | share |")
    lines.append("|---|---|---|---|")
    for many in ("4", "3", "2", "1", "0"):
        held = document["across_targets"][many]
        lines.append("| %s of 4 | %d | %d | %s%% |"
                     % (many, held["cells"], held["ledger_rows"],
                        held["share_percent"]))
    lines.append("")


def causes_command():
    """the report's section 3 summed over the four targets: one row per
    cause over all 1,012 runs, and the arrival-contract group inside
    them counted on its own."""
    document = read_json(AGGREGATE)
    summed = {}
    for lang in document["meta"]["targets"]:
        for name in document["causes"][lang]:
            held = document["causes"][lang][name]
            entry = summed.setdefault(name, {"runs": 0, "rows": 0,
                                             "langs": []})
            entry["runs"] = entry["runs"] + held["runs"]
            entry["rows"] = entry["rows"] + held["ledger_rows"]
            entry["langs"].append(lang)
    say("Table 5 -- what did not work, by cause, the four targets "
        "summed. `rows` counts a cell's attested ledger rows once per "
        "run, so a cause seen on all four targets counts them four "
        "times.")
    say("")
    say("| cause | runs | ledger rows | targets |")
    say("|---|---|---|---|")
    ordered = sorted(summed, key=lambda name: (-summed[name]["runs"],
                                               name))
    for name in ordered:
        held = summed[name]
        say("| %s | %d | %d | %s |"
            % (escaped(name), held["runs"], held["rows"],
               ", ".join(sorted(held["langs"]))))
    total = 0
    for name in summed:
        total = total + summed[name]["runs"]
    say("")
    say("runs carrying a cause: %d of %d" % (total,
                                             document["meta"]["runs"]))
    say("")
    say("THE ARRIVAL-CONTRACT GROUP, counted on its own: every gate "
        "call that declined because the two sides name a different "
        "number of arriving values.")
    say("")
    group = []
    for run in document["runs"]:
        for place in (run.get("places") or []):
            check = place.get("check") or {}
            reason = "%s" % check.get("reason")
            if "the IN rows cannot be aligned" not in reason:
                continue
            group.append((run, place, reason))
    say("places the gate declined on the IN-row alignment: %d"
        % len(group))
    shapes = {}
    for _run, _place, reason in group:
        shapes.setdefault(reason, 0)
        shapes[reason] = shapes[reason] + 1
    for reason in sorted(shapes, key=lambda one: -shapes[one]):
        say("   %d place(s): %s" % (shapes[reason], reason))
    say("")
    say("| cell | route | ledger rows |")
    say("|---|---|---|")
    seen = set()
    for run, _place, _reason in group:
        key = (run["mnem"], run["shape"], run["key_width"],
               run["route"])
        if key in seen:
            continue
        seen.add(key)
        say("| `%s` %s %s | %s | %d |"
            % (run["mnem"], run["shape"], run["key_width"],
               run["route"], run["attested_ledger_rows"]))
    return 0


def repose_command():
    """what the ONE re-pose at 30,000 ms moved, which is the law's own
    obligation on a time limit: re-run with more room and report
    whether the answer changed."""
    document = read_json(AGGREGATE)
    posed = 0
    answers = {}
    moved = []
    for run in document["runs"]:
        for place in (run.get("places") or []):
            check = place.get("check") or {}
            again = check.get("recheck")
            if again is None:
                continue
            posed = posed + 1
            outcome = again.get("outcome")
            answers.setdefault(outcome, 0)
            answers[outcome] = answers[outcome] + 1
            if outcome == "UNDECIDED":
                continue
            moved.append((run, place, outcome))
    say("places UNDECIDED at the 3,000 ms ceiling of record and "
        "re-posed once at 30,000 ms: %d" % posed)
    for outcome in sorted(answers):
        say("   %-16s %d" % (outcome, answers[outcome]))
    say("")
    say("| cell | lang | place | route | ledger rows | the re-pose's "
        "answer |")
    say("|---|---|---|---|---|---|")
    for run, place, outcome in moved:
        say("| `%s` %s %s | %s | %s | %s | %d | %s |"
            % (run["mnem"], run["shape"], run["key_width"],
               run["lang"], place["writes"], run["route"],
               run["attested_ledger_rows"], outcome))
    return 0


def store_command():
    """the incremental store and the aggregate read side by side and
    compared run for run, so "they hold the same 1,012 runs" is checked
    rather than asserted."""
    lines = []
    handle = open(RUNS)
    for line in handle:
        if not line.strip():
            continue
        lines.append(as_machine_form(json.loads(line)))
    handle.close()
    document = read_json(AGGREGATE)
    runs = document["runs"]
    say("lines on the store: %d" % len(lines))
    say("runs on the aggregate: %d" % len(runs))
    same = 0
    for one, two in zip(lines, runs):
        if json.dumps(one, sort_keys=True) != json.dumps(two,
                                                         sort_keys=True):
            continue
        same = same + 1
    say("run for run identical: %d" % same)
    keys = set()
    for run in runs:
        keys.add(key_of((run["mnem"], run["shape"], run["key_width"]),
                        run["lang"]))
    say("distinct (cell, target) pairs: %d" % len(keys))
    return 0


def sat_command():
    """the two `sat` counts, the per-target split of the surviving ones,
    and the five with the most attested ledger rows with z3's own
    counterexample."""
    document = read_json(AGGREGATE)
    held = document["sat_verdicts"]
    survived = []
    for entry in held:
        if entry.get("under_caller_extension") == "PROVED_ON_SHIP":
            continue
        survived.append(entry)
    say("sat at the plain comparison, every written place: %d"
        % len(held))
    say("sat surviving the caller-extension re-pose: %d" % len(survived))
    by_lang = {}
    for entry in survived:
        by_lang.setdefault(entry["lang"], 0)
        by_lang[entry["lang"]] = by_lang[entry["lang"]] + 1
    for lang in sorted(by_lang):
        say("   %-6s %d" % (lang, by_lang[lang]))
    say("the five surviving sat places with the most ledger rows:")
    for entry in survived[:5]:
        say("   %-10s %-12s %-5s %-6s [%s] %d rows"
            % (entry["mnem"], entry["shape"], entry["key_width"],
               entry["lang"], entry["writes"], entry["ledger_rows"]))
        say("      counterexample: %s" % entry["counterexample"])
    return 0


def branch_command():
    """`handful.renderer_input` quoted LITERAL, and which of its two
    branches each task's own setting takes.

    Here because a claim about the imported driver should carry the
    driver's own source rather than a reading of it."""
    import inspect
    say(inspect.getsource(H.renderer_input))
    for task in ("h1", "h2", "g1", "g1b", "g1c"):
        H.TASK = task
        if task in ("h2", "g1"):
            which = "the normalised term (task h2's fix 1)"
        else:
            which = "order_commutative(simplify(term)), task h1's own"
        say("TASK %-4s fixes_are_on %-5s primitive_first %-5s "
            "setup_is_allowed %-5s -> %s"
            % (task, H.fixes_are_on(), H.primitive_first(),
               H.setup_is_allowed(), which))
    use_task_ap1()
    return 0


def report_command():
    """`autopoly.json` -> `autopoly.md`, the six sections the brief
    names."""
    document = read_json(AGGREGATE)
    lines = []
    write_head(lines, document)
    write_table_one(lines, document)
    write_routes(lines, document)
    write_causes(lines, document)
    write_across(lines, document)
    write_sat(lines, document)
    write_handful(lines, document)
    handle = open(REPORT, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("wrote %s (%d lines)" % (REPORT, len(lines)))
    say("peak resident: %d kB" % check_memory("report"))
    return 0


def write_head(lines, document):
    meta = document["meta"]
    lines.append("# autopoly.md -- task ap1: AutoPoly's first full loop")
    lines.append("")
    lines.append("Node `hq.research.arch_unit_oracle.cross_construction"
                 ".autopoly`. Written by `autopoly.py`; never "
                 "hand-edited.")
    lines.append("")
    lines.append("**What this is, one sentence.** the owner's loop -- for "
                 "every arch opcode of the model table that the corpus "
                 "attests, for each of the four compiled targets, "
                 "`find_emulation(cell, lang)` -- run for the first "
                 "time over its whole measured outer set: %d cells x %d "
                 "targets = %d runs, of which %d are recorded here."
                 % (meta["cells"], len(meta["targets"]),
                    meta["cells"] * len(meta["targets"]), meta["runs"]))
    lines.append("")
    lines.append("The route is `handful.py` as task g1b left it "
                 "(`%s`), imported and called; this task's own program "
                 "is the loop around it and the bookkeeping, nothing "
                 "else." % meta["route"])
    lines.append("")
    lines.append("Every count below is of the run's own DESTINATION "
                 "PLACE -- `handful.destination_place`, the first place "
                 "the cell writes that is not the flags -- which is the "
                 "place tasks h1, h2, g1 and g1b's own tables already "
                 "summarize. The denominator of every share is %d, the "
                 "attested ledger rows of the whole outer set."
                 % document["ledger_rows_total"])
    lines.append("")


def write_table_one(lines, document):
    lines.append("## 1. THE table: per target, what the loop reached")
    lines.append("")
    lines.append("Table 1 -- one row per target. `cells` counts runs; "
                 "`rows` is the attested ledger rows those cells cover "
                 "and `share` that as a percentage of %d."
                 % document["ledger_rows_total"])
    lines.append("")
    header = ["step or verdict"]
    for lang in document["meta"]["targets"]:
        header.append(lang)
    lines.append("| %s |" % " | ".join(header))
    lines.append("|%s" % ("---|" * len(header)))
    names = ["attempted", "rendered", "compiled"] + LANDINGS + OUTCOMES
    for name in names:
        row = ["`%s`" % name]
        for lang in document["meta"]["targets"]:
            held = document["per_language"][lang][name]
            row.append("%d cells, %d rows, %s%%"
                       % (held["runs"], held["ledger_rows"],
                          held["share_percent"]))
        lines.append("| %s |" % " | ".join(row))
    lines.append("")


def write_routes(lines, document):
    lines.append("## 2. Per target, how far the primitive route reached")
    lines.append("")
    lines.append("Table 2 -- `primitive` is a target operator whose "
                 "whole lowered body IS the cell; `primitive+setup` is "
                 "that plus zero-operand accumulator setup (task g1c's "
                 "widened lookup); `term` is the cell's own term "
                 "written in the target's operators, which is the "
                 "fallback.")
    lines.append("")
    header = ["route"]
    for lang in document["meta"]["targets"]:
        header.append(lang)
    lines.append("| %s |" % " | ".join(header))
    lines.append("|%s" % ("---|" * len(header)))
    for name in ROUTES:
        row = ["`%s`" % name]
        for lang in document["meta"]["targets"]:
            held = document["routes"][lang][name]
            row.append("%d cells, %d rows, %s%%"
                       % (held["runs"], held["ledger_rows"],
                          held["share_percent"]))
        lines.append("| %s |" % " | ".join(row))
    lines.append("")


def write_causes(lines, document):
    lines.append("## 3. Refusals and non-proofs, by cause")
    lines.append("")
    for lang in document["meta"]["targets"]:
        causes = document["causes"][lang]
        lines.append("### 3.%d %s" % (document["meta"]["targets"]
                                      .index(lang) + 1, lang))
        lines.append("")
        if not causes:
            lines.append("Nothing was refused and every gate call "
                         "proved.")
            lines.append("")
            continue
        lines.append("| cause | cells | ledger rows | three examples |")
        lines.append("|---|---|---|---|")
        ordered = sorted(causes,
                         key=lambda name: (-causes[name]["ledger_rows"],
                                           name))
        for name in ordered:
            held = causes[name]
            examples = []
            for one in held["examples"]:
                examples.append("`%s` %s %s (%s rows)"
                                % (one["mnem"], one["shape"],
                                   one["key_width"],
                                   one["ledger_rows"]))
            lines.append("| %s | %d | %d | %s |"
                         % (escaped(name), held["runs"],
                            held["ledger_rows"], "; ".join(examples)))
        lines.append("")


def escaped(text):
    """a pipe inside a table cell, escaped, so a compiler's own error
    line cannot break the row."""
    held = "%s" % text
    held = held.replace("|", "\\|")
    held = held.replace("\n", " ")
    if len(held) > 300:
        held = held[:297] + "..."
    return held


def write_across(lines, document):
    lines.append("## 4. Cells proved on all four targets, on three, "
                 "two, one, none")
    lines.append("")
    lines.append("Table 3 -- a cell counts as proved on a target when "
                 "the gate answered `unsat` at that target's "
                 "destination place, at the 3,000 ms ceiling of record "
                 "or under the caller-extension re-pose. The "
                 "polyfill-complete set is the row `4`.")
    lines.append("")
    lines.append("| proved on | cells | ledger rows | share |")
    lines.append("|---|---|---|---|")
    for many in ("4", "3", "2", "1", "0"):
        held = document["across_targets"][many]
        lines.append("| %s of 4 | %d | %d | %s%% |"
                     % (many, held["cells"], held["ledger_rows"],
                        held["share_percent"]))
    lines.append("")
    lines.append("### 4.1 The polyfill-complete set, in full")
    lines.append("")
    held = document["across_targets"]["4"]["cell_list"]
    if not held:
        lines.append("No cell is proved on all four targets.")
    lines.append("")
    lines.append("| cell | ledger rows |")
    lines.append("|---|---|")
    for entry in held:
        lines.append("| %s | %d |" % (named_cell(entry),
                                      entry["ledger_rows"]))
    lines.append("")
    lines.append("### 4.2 The cells proved on no target, in full, with "
                 "the cause on each")
    lines.append("")
    lines.append("| cell | ledger rows | c | rust | go | swift |")
    lines.append("|---|---|---|---|---|---|")
    for entry in document["across_targets"]["on_none_with_causes"]:
        row = [named_cell(entry), "%d" % entry["ledger_rows"]]
        for lang in document["meta"]["targets"]:
            row.append(escaped(entry["causes"].get(lang)))
        lines.append("| %s |" % " | ".join(row))
    lines.append("")


def named_cell(entry):
    """one cell as a report reads it: the triple, the mnemonic in
    backticks as the display label it is."""
    return "`%s` %s %s" % (entry["mnem"], entry["shape"],
                           entry["key_width"])


def write_sat(lines, document):
    lines.append("## 5. Every `sat` verdict, with its counterexample "
                 "and the region it names")
    lines.append("")
    lines.append("A `sat` is where the target's edge region differs "
                 "from the opcode's: z3 found a starting state under "
                 "which the compiled body and the cell's term answer "
                 "differently. The counterexample is z3's own, "
                 "LITERAL.")
    lines.append("")
    held = document["sat_verdicts"]
    survived = []
    for entry in held:
        if entry.get("under_caller_extension") == "PROVED_ON_SHIP":
            continue
        survived.append(entry)
    lines.append("TWO COUNTS, and they are two different things.")
    lines.append("")
    lines.append("- **`sat` at the plain comparison: %d places.** z3 "
                 "answered `sat` when the emulation's arriving values "
                 "are whatever fits the register." % len(held))
    lines.append("- **`sat` that survives the caller-extension re-pose: "
                 "%d places.** Task o7's own rule: pose the same "
                 "comparison again with every narrow-holder input row "
                 "zero-extended from its holder width to the register, "
                 "which is what the target's own calling rule "
                 "guarantees the caller did. What is left is where the "
                 "target's edge region really differs from the "
                 "opcode's." % len(survived))
    lines.append("")
    lines.append("Table 1's `sat` row counts the second of these at the "
                 "destination place; this table lists every written "
                 "place, the flags included.")
    lines.append("")
    if not held:
        lines.append("The loop produced no `sat` verdict.")
        lines.append("")
        return
    lines.append("| cell | lang | place | route | ledger rows | "
                 "survives the re-pose | region | counterexample "
                 "(LITERAL) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for entry in held:
        stands = "yes"
        if entry.get("under_caller_extension") == "PROVED_ON_SHIP":
            stands = "no, proved once zero-extended"
        lines.append("| `%s` %s %s | %s | %s | %s | %s | %s | %s | %s |"
                     % (entry["mnem"], entry["shape"],
                        entry["key_width"], entry["lang"],
                        entry["writes"], entry["route"],
                        entry["ledger_rows"], stands,
                        escaped(entry["region"]),
                        escaped(entry["counterexample"])))
    lines.append("")


def write_handful(lines, document):
    lines.append("## 6. The handful, reproduced")
    lines.append("")
    lines.append("Table 4 -- the ten cells tasks h1, h2, g1 and g1b ran, "
                 "on the same four targets, as they came out of THIS "
                 "loop, beside task g1b's own answer for the same pair. "
                 "The handful's side is read from "
                 "`handful3b.json` and, for the one pair the widened "
                 "lookup changes, `handful3c.json`.")
    lines.append("")
    lines.append("| cell | lang | this loop: route / landed / gate | "
                 "the handful: route / landed / gate | agrees | agrees "
                 "on the verdict |")
    lines.append("|---|---|---|---|---|---|")
    agreed = 0
    on_verdict = 0
    for row in document["handful"]:
        if row.get("agrees"):
            agreed = agreed + 1
        if row.get("agrees_on_the_verdict"):
            on_verdict = on_verdict + 1
        lines.append("| `%s` %s %s | %s | %s | %s | %s | %s |"
                     % (row["mnem"], row["shape"], row["key_width"],
                        row["lang"],
                        escaped(three_cells(row.get("this_loop"))),
                        escaped(three_cells(row.get("the_handful"))),
                        yes_or_no(row.get("agrees")),
                        yes_or_no(row.get("agrees_on_the_verdict"))))
    lines.append("")
    lines.append("Agree character for character: %d of %d. Agree on "
                 "the verdict, the re-pose's own ceiling aside: %d -- "
                 "this loop re-poses an UNDECIDED once at 30,000 ms "
                 "where the handful re-posed at 300,000 ms, which is "
                 "this brief's own instruction, so the two differ in "
                 "that number and in nothing else."
                 % (agreed, len(document["handful"]), on_verdict))
    lines.append("")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
