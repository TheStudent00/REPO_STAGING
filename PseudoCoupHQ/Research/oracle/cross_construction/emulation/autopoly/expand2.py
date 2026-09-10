#!/usr/bin/env python3
"""expand2.py -- task ex2: THE INTERPRETED LOOP.  Every attested cell of
the model table, on the seven interpreted targets, by the check task ex1
defined.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly; also
serves node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table, holding, per place the opcode writes, the
    z3 term the reference simulator's own builder puts there.
  * THE OUTER SET is the 253 cells the canon40 corpus attests, read off
    `autopoly5_cells.json` -- task ap5's own cells file, the driver as
    it now stands (the x87 answer read end to end, the immediate as an
    input of the mapping), copied here and its counts re-measured.
  * AN INTERPRETED RUN is task ex1's own object, unchanged: there is no
    carve, so the emulation is SOURCE in the target language and the
    check is the fuzz census's method over the sample `interp_check.py`
    states LITERAL. THIS TASK RUNS THE SAME CHECK OVER THE WHOLE OUTER
    SET INSTEAD OF THE HANDFUL'S TEN, on all seven of task ex1's
    interpreted targets -- 253 x 7 = 1,771 runs.

WHAT IS REUSED RATHER THAN COPIED, said out loud. `interp_check.one_run`,
`interp_render.py` and `interp/dialects.py` are task ex1's, imported and
called, never forked. `handful.cell_input` is called with every one of
the 253 triples, not only the ten of `handful.ASKED` -- it already reads
any triple against `cells["asked"]`, so no change to it was needed at
all.

THE ONE BOOKKEEPING CHANGE, and it is in the interpreted route only, and
this is the whole of it: `interp_check.interpreter_answers` and
`interp_check.one_run` each gained a `timeout` parameter (default None,
which keeps task ex1's own 900 s exactly). A run past the bound is
recorded `outcome: "TIMEOUT"` with the point count reached, read off
whatever the process had already printed before `subprocess` stopped it
-- TIMEOUT is not a new outcome name, it is the word the law already
uses for a lane or a solver that ran out of room. Nothing else about
`interp_check.py` moved, and nothing under `handful.py` or
`Research/op_pipeline/` was touched by this task at all.

BOOKKEEPING.  Runs ordered by attested ledger rows descending (the cells
file's own order); `expand2_runs.jsonl`, one line per run, resume by
skipping. The first pass bounds the interpreter to 60 s; every run that
hits it is re-run once, from a second cold render, at 600 s, into
`expand2_runs_retry600.jsonl`, and the report carries BOTH the first
pass's TIMEOUT record and the retry's own outcome for that pair.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers; peak resident checked after every run; named abort
ABORT_MEMORY_EX2 at 6 GB, inside the instance's 20g cap.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections, type
pairs) or from ratified intention -- never from the token.  The token
appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch campaign's
cross-language matrix (caught by the owner 2026-08-24); (2) verdicts.py's row
pairing (caught by the owner 2026-08-25 -- the fix brief itself reintroduced it
as "same-operator pairs").  MECHANICAL GUARD REQUIRED: every pipeline
stage that groups or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

The population is machine-form evidence and nothing else: the cells are
every triple the corpus attests, read off the table's own
`attestation.ledger_rows`, in that count's descending order; the targets
are `interp_render.LANGUAGES`, task ex1's own list. No operator token
enters the selection, the order or the pairing; every field carrying a
mnemonic is named `mnem`, which the guard reads as a machine form.

Coding discipline: no compound one-liner statements.

usage:
  expand2.py preflight        the outer set and the cells file, nothing run
  expand2.py run [<n>]        the loop, first pass, 60 s per run
  expand2.py retry [<n>]      every TIMEOUT of the first pass, re-run once
                              at 600 s
  expand2.py aggregate        expand2_runs.jsonl (+ retry) -> expand2.json
  expand2.py tables           deliverable 1: the per-target table
  expand2.py all_seven        deliverable 2: agree on all seven / all twelve
  expand2.py disagreements    deliverable 3: every disagreement, LITERAL
  expand2.py declines         deliverable 4: declines by target and word
  expand2.py refusals         deliverable 5: refusals by cause
  expand2.py handful_check    deliverable 6: the handful's 70 reproduced
  expand2.py report           expand2.md
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
INTERP = os.path.join(EMULATION, "interp")
sys.path.insert(0, HANDFUL)
sys.path.insert(0, INTERP)
sys.path.insert(0, HERE)

import handful as H                                             # noqa: E402
import interp_check as IC                                       # noqa: E402
import interp_render as IR                                      # noqa: E402
import autopoly4 as AP4                                         # noqa: E402

CELLS = os.path.join(HERE, "expand2_cells.json")
RUNS = os.path.join(HERE, "expand2_runs.jsonl")
RETRY_RUNS = os.path.join(HERE, "expand2_runs_retry600.jsonl")
AGGREGATE = os.path.join(HERE, "expand2.json")
REPORT = os.path.join(HERE, "expand2.md")

# TASK ap5'S OWN CELLS FILE, read and never written: the outer set as
# the driver now stands, with the 20 imm_symbolic rows.
AP5_CELLS = os.path.join(HERE, "autopoly5_cells.json")
AP5_AGGREGATE = os.path.join(HERE, "autopoly5.json")

# TASK ex1'S OWN PRODUCTS, read and never written: cpp's proved set (the
# fifth compiled target) and the handful's seventy interpreted runs this
# task's own loop must reproduce.
EX1_CPP_RUNS = os.path.join(HERE, "expand1_runs.jsonl")
EX1_INTERP_RUNS = os.path.join(HERE, "expand1_interp.jsonl")

HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/autopoly")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_EX2"

TIMEOUT_FIRST = 60
TIMEOUT_RETRY = 600

TOTAL_LEDGER_ROWS = 133044


def use_task_ex2():
    """the route is task ex1's, called and not restated: `fixes_are_on`,
    `primitive_first` and `setup_is_allowed` already answer for `ex1`
    the way this task needs, and nothing about the interpreted route is
    gated on a task name at all beyond the ABORT name and the source
    folder, both set here."""
    H.use_task_ex1()
    IC.ABORT_KB = ABORT_KB
    IC.ABORT_NAME = ABORT_NAME
    IC.SRC_DIR = os.path.join(INTERP, "src_ex2")


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


def read_runs(path):
    out = []
    if not os.path.exists(path):
        return out
    handle = open(path)
    for line in handle:
        stripped = line.strip()
        if not stripped:
            continue
        out.append(json.loads(stripped))
    handle.close()
    return out


def append_run(path, record):
    handle = open(path, "a")
    handle.write(json.dumps(record, sort_keys=True) + "\n")
    handle.close()


def cell_key(run):
    return (run["mnem"], run["shape"], run["key_width"])


def key_of(asked, lang):
    return "%s|%s|%s|%s" % (asked[0], asked[1], asked[2], lang)


def escaped(text):
    return ("%s" % text).replace("|", "/")


def rate(part, whole):
    if not whole:
        return "0.0"
    return "%s" % round(100.0 * part / whole, 2)


def ledger_index(cells):
    out = {}
    for record in cells["asked"]:
        key = (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"])
        out[key] = record["attested_ledger_rows"]
    return out


# ==================================================================
# section 1: THE OUTER SET
# ==================================================================

def preflight_command():
    """the outer set as the loop will walk it, and nothing run."""
    if not os.path.exists(CELLS):
        source = read_json(AP5_CELLS)
        write_json(CELLS, source)
        say("copied task ap5's cells file to %s" % CELLS)
    mine = read_json(CELLS)
    theirs = read_json(AP5_CELLS)
    same = json.dumps(mine, sort_keys=True) == json.dumps(theirs,
                                                          sort_keys=True)
    say("the cells file is task ap5's, object for object: %s" % same)
    cells = mine
    total = 0
    for record in cells["asked"]:
        total = total + record["attested_ledger_rows"]
    say("cells on %s: %d" % (CELLS, len(cells["asked"])))
    say("attested ledger rows over the whole outer set: %d" % total)
    say("the seven interpreted targets, `interp_render.LANGUAGES`: %s"
        % ", ".join(IR.LANGUAGES))
    say("pairs: %d" % (len(cells["asked"]) * len(IR.LANGUAGES)))
    say("the runners, as this machine answers them:")
    for lang in IR.LANGUAGES:
        say("   %-12s %s" % (lang, IR.runner_answer(lang)))
    say("")
    say("the first ten cells of the order, most attested first:")
    for record in cells["asked"][:10]:
        say("   %-10s %-14s %-6s ledger_rows %d"
            % (record["asked"]["mnem"], record["asked"]["shape"],
               record["asked"]["key_width"],
               record["attested_ledger_rows"]))
    say("")
    done = already_recorded(RUNS)
    say("runs already on %s: %d" % (RUNS, len(done)))
    say("peak resident: %d kB" % check_memory("preflight"))
    return 0


def the_pairs(cells):
    """every (cell, target) pair, in the order the loop walks them: the
    cells by attested ledger rows descending (the cells file's own
    order), and the seven interpreted targets in `interp_render.
    LANGUAGES`'s own order inside each cell. No operator token enters
    this pairing: the cells are read off `attestation.ledger_rows` and
    the targets off the renderer's own language list."""
    out = []
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        for lang in IR.LANGUAGES:
            out.append((asked, lang, record["attested_ledger_rows"]))
    return out


def already_recorded(path):
    done = {}
    for run in read_runs(path):
        done[key_of(cell_key(run), run["lang"])] = run
    return done


# ==================================================================
# section 2: THE LOOP, FIRST PASS AT 60 s
# ==================================================================

def run_command(limit):
    """the loop. One line on `expand2_runs.jsonl` per finished run."""
    cells = read_json(CELLS)
    pairs = the_pairs(cells)
    shared = IC.build_shared()
    done = already_recorded(RUNS)
    say("pairs to run: %d; already recorded: %d" % (len(pairs), len(done)))
    total = len(pairs)
    index = 0
    ran = 0
    started = time.time()
    for asked, lang, ledger in pairs:
        index = index + 1
        if key_of(asked, lang) in done:
            continue
        say("[%d/%d] %s %s %s -> %s (ledger_rows %d)"
            % (index, total, asked[0], asked[1], asked[2], lang, ledger))
        record = IC.one_run(shared, cells, asked, lang,
                            timeout=TIMEOUT_FIRST)
        record["attested_ledger_rows"] = ledger
        append_run(RUNS, record)
        ran = ran + 1
        say("   %s | %d s | peak resident: %d kB"
            % (one_line(record), round(record["seconds"]),
               check_memory("run %d" % index)))
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d run(s) performed" % ran)
            break
    say("")
    say("runs performed this lane: %d in %d s"
        % (ran, round(time.time() - started)))
    say("lines on %s: %d" % (RUNS, len(read_runs(RUNS))))
    say("peak resident: %d kB" % peak_kb())
    return 0


def one_line(record):
    if record.get("outcome") == "TIMEOUT":
        return ("TIMEOUT at %d s, %d point(s) reached"
                % (record["timeout_seconds"], record["points_reached"]))
    if record.get("refusal_cause") is not None:
        return "REFUSED: %s" % ("%s" % record["refusal_cause"])[:80]
    return ("%d points, %d agree, %d disagree, %d declined"
            % (record["sample_points"], record["agreements"],
               record["disagreements"], record["declined_points"]))


# ==================================================================
# section 3: THE RETRY, EVERY TIMEOUT ONCE AT 600 s
# ==================================================================

def timed_out_pairs():
    """every (cell, target) whose first-pass record is a TIMEOUT."""
    out = []
    for run in read_runs(RUNS):
        if run.get("outcome") != "TIMEOUT":
            continue
        out.append((cell_key(run), run["lang"],
                    run.get("attested_ledger_rows")))
    return out


def retry_command(limit):
    """the law's own rule for a time limit: re-run with more room and
    report whether the answer changed, never change what is measured to
    fit. Every TIMEOUT of the first pass, once, at 600 s, into a SEPARATE
    store -- the first pass's record is never overwritten, so the report
    can show both."""
    cells = read_json(CELLS)
    pairs = timed_out_pairs()
    shared = IC.build_shared()
    done = already_recorded(RETRY_RUNS)
    say("TIMEOUTs on the first pass: %d; already retried: %d"
        % (len(pairs), len(done)))
    ran = 0
    index = 0
    started = time.time()
    for asked, lang, ledger in pairs:
        index = index + 1
        if key_of(asked, lang) in done:
            continue
        say("[%d/%d retry] %s %s %s -> %s (ledger_rows %s)"
            % (index, len(pairs), asked[0], asked[1], asked[2], lang,
               ledger))
        record = IC.one_run(shared, cells, asked, lang,
                            timeout=TIMEOUT_RETRY)
        record["attested_ledger_rows"] = ledger
        append_run(RETRY_RUNS, record)
        ran = ran + 1
        say("   %s | %d s | peak resident: %d kB"
            % (one_line(record), round(record["seconds"]),
               check_memory("retry %d" % index)))
        if limit is not None and ran >= limit:
            say("")
            say("the sample's own stop: %d retry run(s) performed" % ran)
            break
    say("")
    say("retries performed this lane: %d in %d s"
        % (ran, round(time.time() - started)))
    say("lines on %s: %d" % (RETRY_RUNS, len(read_runs(RETRY_RUNS))))
    say("peak resident: %d kB" % peak_kb())
    return 0


def combined_runs():
    """the run of record per (cell, target): the first pass, with the
    600 s retry's own record attached under `retry_600s` when one
    exists. BOTH are kept -- the first pass's TIMEOUT is never
    overwritten by the retry's answer, exactly as the brief asks."""
    retries = {}
    for run in read_runs(RETRY_RUNS):
        retries[key_of(cell_key(run), run["lang"])] = run
    out = []
    for run in read_runs(RUNS):
        record = dict(run)
        retry = retries.get(key_of(cell_key(run), run["lang"]))
        if retry is not None:
            record["retry_600s"] = retry
        out.append(record)
    return out


# ==================================================================
# section 4: AGGREGATE
# ==================================================================

def aggregate_command():
    runs = combined_runs()
    document = {"meta": {"task": "ex2",
                         "what": "the interpreted loop: every attested "
                                 "cell of the model table, on the seven "
                                 "interpreted targets, by the check "
                                 "task ex1 defined",
                         "sample_rule": IC.SAMPLE_RULE,
                         "timeout_first_pass_seconds": TIMEOUT_FIRST,
                         "timeout_retry_seconds": TIMEOUT_RETRY,
                         "runs": len(runs),
                         "targets": IR.LANGUAGES},
                "runs": runs}
    write_json(AGGREGATE, document)
    say("runs on %s: %d" % (RUNS, len(read_runs(RUNS))))
    say("retries on %s: %d" % (RETRY_RUNS, len(read_runs(RETRY_RUNS))))
    say("wrote %s" % AGGREGATE)
    return 0


# ==================================================================
# section 5: THE EFFECTIVE OUTCOME OF A RUN, retry folded in
# ==================================================================

def effective(run):
    """the run the report counts by: the retry's own record when the
    first pass timed out and a retry exists, the first pass otherwise.
    The first pass's TIMEOUT is still on the record (`run` itself, or
    `run["retry_600s"]`'s sibling on the combined store) -- this
    function only decides which one the TALLY reads."""
    if run.get("outcome") == "TIMEOUT" and run.get("retry_600s") is not None:
        return run["retry_600s"]
    return run


# ==================================================================
# section 6: DELIVERABLE 1 -- THE TABLE PER TARGET
# ==================================================================

STEPS = ["attempted", "rendered", "whole sample agrees",
         "any disagreement", "refused", "timed out"]


def tables_command():
    """deliverable 1: cells attempted / rendered / whole sample agrees /
    any disagreement / refused / timed out -- counts and ledger-row
    shares, per target."""
    cells = read_json(CELLS)
    ledger_of = ledger_index(cells)
    total_rows = 0
    for key in ledger_of:
        total_rows = total_rows + ledger_of[key]
    runs = combined_runs()
    per_target = {}
    for lang in IR.LANGUAGES:
        per_target[lang] = {}
        for step in STEPS:
            per_target[lang][step] = {"cells": 0, "rows": 0}
    for run in runs:
        lang = run["lang"]
        key = cell_key(run)
        rows = ledger_of.get(key, 0)
        got = effective(run)
        per_target[lang]["attempted"]["cells"] += 1
        per_target[lang]["attempted"]["rows"] += rows
        # A run whose first pass timed out and whose retry ALSO timed
        # out is counted as timed out, never as rendered/refused --
        # `effective()` on a double timeout answers the retry's own
        # TIMEOUT record, so the check below still reads it off `got`.
        if got.get("outcome") == "TIMEOUT":
            per_target[lang]["timed out"]["cells"] += 1
            per_target[lang]["timed out"]["rows"] += rows
            continue
        if got.get("refusal_cause") is not None:
            per_target[lang]["refused"]["cells"] += 1
            per_target[lang]["refused"]["rows"] += rows
            continue
        per_target[lang]["rendered"]["cells"] += 1
        per_target[lang]["rendered"]["rows"] += rows
        if got.get("disagreements", 0) > 0:
            per_target[lang]["any disagreement"]["cells"] += 1
            per_target[lang]["any disagreement"]["rows"] += rows
        elif got.get("agreements", 0) > 0:
            per_target[lang]["whole sample agrees"]["cells"] += 1
            per_target[lang]["whole sample agrees"]["rows"] += rows
    say("Table 1 -- one row per target. `cells` counts runs; `rows` is "
        "the attested ledger rows those cells cover and `share` that as "
        "a percentage of %d. A run whose first pass TIMED OUT and whose "
        "600 s retry answered is counted by the retry's own outcome; a "
        "run that timed out on both passes is counted `timed out`."
        % total_rows)
    say("")
    say("| step | %s |" % " | ".join(IR.LANGUAGES))
    say("|---|%s" % ("---|" * len(IR.LANGUAGES)))
    for step in STEPS:
        parts = []
        for lang in IR.LANGUAGES:
            held = per_target[lang][step]
            parts.append("%d cells, %d rows, %s%%"
                         % (held["cells"], held["rows"],
                            rate(held["rows"], total_rows)))
        say("| `%s` | %s |" % (step, " | ".join(parts)))
    return 0


# ==================================================================
# section 7: DELIVERABLE 2 -- ALL SEVEN, ALL TWELVE
# ==================================================================

def cpp_proved_set():
    """cpp's own proved set, task ex1's store, `autopoly4.outcome_of`
    called and not restated -- the same function ex1's own report used.
    STATED AS A CAVEAT rather than hidden: this store predates task
    ap5's imm_symbolic gain, so an `imm_*` cell that gained a term-route
    proof on c/rust/go/swift under ap5 is not re-measured on cpp here;
    the awaiting-the owner list says so."""
    out = set()
    for run in read_runs(EX1_CPP_RUNS):
        if run["lang"] != "cpp":
            continue
        if AP4.outcome_of(run) in ("proved", "proved under caller "
                                              "extension"):
            out.add(cell_key(run))
    return out


def four_proved_set():
    """the four compiled targets' own proved set, task ap5's own
    aggregate, read and not recomputed."""
    theirs = read_json(AP5_AGGREGATE)
    out = set()
    for entry in theirs["across_targets"]["4"]["cell_list"]:
        out.add((entry["mnem"], entry["shape"], entry["key_width"]))
    return out


def five_proved_set():
    """the four compiled proved AND cpp proved, task ex1's own Table 2
    method, called over task ap5's four instead of task ap4's -- the
    driver as it now stands. Neither redefines the other; both are
    reported."""
    four = four_proved_set()
    cpp = cpp_proved_set()
    return four & cpp


def seven_agree_set(runs):
    """every cell that RENDERED on all seven interpreted targets with a
    whole-sample agreement (zero disagreements, at least one agreement)
    on every one of them. A cell missing a target -- refused, timed
    out on both passes, or simply not yet run -- is excluded: it is not
    established to agree on a target it never answered on."""
    by_cell = {}
    for run in runs:
        key = cell_key(run)
        by_cell.setdefault(key, {})[run["lang"]] = effective(run)
    out = set()
    for key, per_lang in by_cell.items():
        if set(per_lang) != set(IR.LANGUAGES):
            continue
        whole = True
        for lang in IR.LANGUAGES:
            got = per_lang[lang]
            if got.get("outcome") == "TIMEOUT":
                whole = False
                break
            if got.get("refusal_cause") is not None:
                whole = False
                break
            if got.get("disagreements", 0) > 0:
                whole = False
                break
            if got.get("agreements", 0) <= 0:
                whole = False
                break
        if whole:
            out.add(key)
    return out


def all_seven_command():
    """deliverable 2: the cells that agree on all seven interpreters, on
    all twelve targets (the five compiled proved + seven agreeing),
    beside the all-four/all-five line."""
    cells = read_json(CELLS)
    ledger_of = ledger_index(cells)
    total_rows = 0
    for key in ledger_of:
        total_rows = total_rows + ledger_of[key]
    runs = combined_runs()
    four = four_proved_set()
    five = five_proved_set()
    seven = seven_agree_set(runs)
    twelve = five & seven

    def rows_of(keys):
        total = 0
        for key in keys:
            total = total + ledger_of.get(key, 0)
        return total

    say("Table 2 -- the widths this line has proved or checked, side by "
        "side, neither redefining the other.")
    say("")
    say("| width | targets | cells | ledger rows | share |")
    say("|---|---|---|---|---|")
    say("| all four | c, rust, go, swift | %d | %d | %s%% |"
        % (len(four), rows_of(four), rate(rows_of(four), total_rows)))
    say("| all five | c, cpp, rust, go, swift | %d | %d | %s%% |"
        % (len(five), rows_of(five), rate(rows_of(five), total_rows)))
    say("| all seven | %s | %d | %d | %s%% |"
        % (", ".join(IR.LANGUAGES), len(seven), rows_of(seven),
           rate(rows_of(seven), total_rows)))
    say("| all twelve | the five compiled proved + the seven agreeing "
        "| %d | %d | %s%% |"
        % (len(twelve), rows_of(twelve), rate(rows_of(twelve),
                                              total_rows)))
    say("")
    say("cells agreeing on all seven interpreted targets but NOT proved "
        "on all five compiled targets: %d" % len(seven - five))
    say("cells proved on all five compiled targets but not agreeing on "
        "all seven interpreted targets: %d" % len(five - seven))
    return 0


# ==================================================================
# section 8: DELIVERABLE 3 -- EVERY DISAGREEMENT
# ==================================================================

def disagreements_command():
    """deliverable 3: every disagreement, with its point LITERAL."""
    runs = combined_runs()
    found = []
    for run in runs:
        got = effective(run)
        if got.get("disagreements", 0) <= 0:
            continue
        found.append((run, got))
    say("disagreements found: %d of %d runs" % (len(found), len(runs)))
    say("")
    if not found:
        say("(none: a disagreement is where an interpreter's value "
            "model differs from the opcode's, and none of the 1,771 "
            "runs found one)")
        return 0
    say("| cell | target | the point, the reference's answer, the "
        "interpreter's answer, LITERAL |")
    say("|---|---|---|")
    for run, got in found:
        cell = "`%s` %s %s" % (run["mnem"], run["shape"], run["key_width"])
        say("| %s | %s | %s |"
            % (cell, run["lang"],
               escaped(json.dumps(got.get("first_disagreement"),
                                  sort_keys=True))))
    return 0


# ==================================================================
# section 9: DELIVERABLE 4 -- DECLINES BY TARGET AND WORD
# ==================================================================

def declines_command():
    """deliverable 4: declines by target and word, never scored, this
    line's own standing rule."""
    runs = combined_runs()
    by_target = {}
    for run in runs:
        got = effective(run)
        for word in (got.get("declines") or {}):
            held = by_target.setdefault(run["lang"], {})
            held[word] = held.get(word, 0) + got["declines"][word]
    say("| target | cause | points |")
    say("|---|---|---|")
    for lang in IR.LANGUAGES:
        held = by_target.get(lang) or {}
        for word in sorted(held, key=lambda one: -held[one]):
            say("| %s | %s | %d |" % (lang, escaped(word), held[word]))
    total = 0
    for lang in by_target:
        for word in by_target[lang]:
            total = total + by_target[lang][word]
    say("")
    say("declined points over every run: %d" % total)
    return 0


# ==================================================================
# section 10: DELIVERABLE 5 -- REFUSALS BY CAUSE
# ==================================================================

def refusals_command():
    """deliverable 5: refusals by cause, per target, with the ledger
    rows those cells cover."""
    cells = read_json(CELLS)
    ledger_of = ledger_index(cells)
    runs = combined_runs()
    by_target = {}
    for run in runs:
        got = effective(run)
        if got.get("refusal_cause") is None:
            continue
        held = by_target.setdefault(run["lang"], {})
        key = "%s" % got["refusal_cause"]
        entry = held.setdefault(key, {"runs": 0, "ledger_rows": 0})
        entry["runs"] += 1
        entry["ledger_rows"] += ledger_of.get(cell_key(run), 0)
    say("| target | cause | runs | ledger rows |")
    say("|---|---|---|---|")
    total = 0
    for lang in IR.LANGUAGES:
        held = by_target.get(lang) or {}
        for key in sorted(held, key=lambda one: -held[one]["runs"]):
            say("| %s | %s | %d | %d |"
                % (lang, escaped(key), held[key]["runs"],
                   held[key]["ledger_rows"]))
            total = total + held[key]["runs"]
    say("")
    say("refused runs over the whole loop: %d of %d" % (total, len(runs)))
    return 0


# ==================================================================
# section 11: DELIVERABLE 6 -- THE HANDFUL'S SEVENTY, REPRODUCED
# ==================================================================

def handful_check_command():
    """deliverable 6: the handful's ten cells on the seven interpreted
    targets, as they came out of THIS loop, beside task ex1's own
    seventy -- the check that a bigger population did not move the ten
    already-tested cells' outcomes."""
    mine = {}
    for run in combined_runs():
        mine[key_of(cell_key(run), run["lang"])] = effective(run)
    theirs = {}
    for run in read_runs(EX1_INTERP_RUNS):
        theirs[key_of(cell_key(run), run["lang"])] = run
    say("| cell | target | this loop | task ex1's handful | agree |")
    say("|---|---|---|---|---|")
    agree = 0
    compared = 0
    for asked in AP4.HANDFUL_CELLS:
        for lang in IR.LANGUAGES:
            key = key_of(asked, lang)
            here = mine.get(key)
            there = theirs.get(key)
            if here is None or there is None:
                say("| `%s` %s %s | %s | %s | %s | -- |"
                    % (asked[0], asked[1], asked[2], lang,
                       "not run" if here is None else one_line(here),
                       "not run" if there is None else one_line(there)))
                continue
            compared = compared + 1
            same = one_line(here) == one_line(there)
            if same:
                agree = agree + 1
            say("| `%s` %s %s | %s | %s | %s | %s |"
                % (asked[0], asked[1], asked[2], lang, one_line(here),
                   one_line(there), same))
    say("")
    say("of the seventy, this loop's own outcome matches task ex1's "
        "handful: %d of %d compared" % (agree, compared))
    return 0


# ==================================================================
# section 12: THE REPORT
# ==================================================================

def captured(function, *arguments):
    import io
    held = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        function(*arguments)
    finally:
        sys.stdout = held
    return buffer.getvalue().rstrip("\n")


def report_command():
    """expand2.md, the six deliverables the brief names."""
    lines = []
    lines.append("# expand2 -- task ex2: the interpreted loop")
    lines.append("")
    lines.append("Node: hq.research.arch_unit_oracle.cross_construction"
                 ".autopoly; also serves node_0_3_1_12_remaining_languages.")
    lines.append("")
    lines.append("Written by `expand2.py report`. Every table is the "
                 "output of a command of this program, captured: "
                 "`tables`, `all_seven`, `disagreements`, `declines`, "
                 "`refusals`, `handful_check`.")
    lines.append("")
    lines.append("Nothing new in method: the emulation is task ex1's "
                 "own -- the cell's mapping rendered in the target's own "
                 "operators over its own value model -- and the check is "
                 "task ex1's own sample rule, pasted below LITERAL, "
                 "exactly as it ran.")
    lines.append("")
    lines.append("## 1. the per-target table")
    lines.append("")
    lines.append(captured(tables_command))
    lines.append("")
    lines.append("## 2. all seven, all twelve")
    lines.append("")
    lines.append(captured(all_seven_command))
    lines.append("")
    lines.append("## 3. every disagreement")
    lines.append("")
    lines.append(captured(disagreements_command))
    lines.append("")
    lines.append("## 4. declines by target and word")
    lines.append("")
    lines.append(captured(declines_command))
    lines.append("")
    lines.append("## 5. refusals by cause")
    lines.append("")
    lines.append(captured(refusals_command))
    lines.append("")
    lines.append("## 6. the handful's seventy, reproduced inside the "
                 "loop")
    lines.append("")
    lines.append(captured(handful_check_command))
    lines.append("")
    lines.append("## 7. the sample rule, LITERAL, as it was run (task "
                 "ex1's own, unchanged)")
    lines.append("")
    lines.append("```")
    for line in IC.SAMPLE_RULE.splitlines():
        lines.append(line)
    lines.append("```")
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("wrote %s (%d lines)" % (REPORT, len(lines)))
    return 0


def main(argv):
    use_task_ex2()
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
    if argv[0] == "retry":
        limit = None
        if len(argv) > 1:
            limit = int(argv[1])
        return retry_command(limit)
    if argv[0] == "aggregate":
        return aggregate_command()
    if argv[0] == "tables":
        return tables_command()
    if argv[0] == "all_seven":
        return all_seven_command()
    if argv[0] == "disagreements":
        return disagreements_command()
    if argv[0] == "declines":
        return declines_command()
    if argv[0] == "refusals":
        return refusals_command()
    if argv[0] == "handful_check":
        return handful_check_command()
    if argv[0] == "report":
        return report_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
