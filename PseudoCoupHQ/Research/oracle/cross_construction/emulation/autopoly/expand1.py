#!/usr/bin/env python3
"""expand1.py -- task ex1: BEYOND THE FOUR.  cpp as a fifth compiled
target, and the interpreted languages with a check of their own, each
on the handful first.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08); the
interpreted half also serves
`node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages`.

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of the
    arch-opcode model table, holding, per place the opcode writes, the
    z3 term the reference simulator's own builder puts there.
  * THE OUTER SET is the 253 cells the canon40 corpus attests -- task
    ap4's `autopoly4_cells.json`, copied here and its counts
    re-measured.
  * A COMPILED RUN is `find_emulation(cell, lang)` as tasks g1 to ap4
    left it: the target's own operator where its whole lowered body IS
    the cell, the cell's term written in the target's operators where
    it is not, compiled at the corpus's ship flags, carved, and put
    back to z3 against the cell's own term.  This task adds ONE target
    to that route, cpp, and changes nothing else about it.
  * AN INTERPRETED RUN is a different thing and this task defines it:
    there is no carve, so the emulation is SOURCE in the target
    language and the check is a FUZZ CENSUS over a stated sample --
    `interp/interp_check.py` holds it and its own header states the
    sample rule LITERAL.

WHAT IS REUSED RATHER THAN COPIED, said out loud.  The compiled loop is
task ap4's, imported and REPOINTED, never forked: `autopoly4.one_run`,
`autopoly4.run_command`, `autopoly4.aggregate_command` and
`autopoly4.report_command` are the same functions task ap4 ran, with
this task's paths and this task's target list written into the module
before they are called.  `handful.py` gains cpp in four places
(`renderer_for`, `suffix_of`, `compile_one_place`, `wrapped_body`) and
one task-scoped list (`targets`), and nothing else about it moves.

WHAT IS REPORTED AT BOTH WIDTHS, and the brief is explicit about it:
the polyfill-complete set is reported over the FOUR targets tasks ap1
to ap4 counted AND over the FIVE this task runs, until the owner says which
counts.  Neither re-defines the other.

MEMORY BOUND, stated as the law requires: one collecting process, no
forked workers; peak resident checked after every run; named abort
ABORT_MEMORY_EX1 at 6 GB, inside the instance's 20g cap.

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

The population is machine-form evidence and nothing else: the cells are
every triple the corpus attests, read off the table's own
`attestation.ledger_rows`, in that count's descending order.  No
operator token enters the selection, the order or the pairing; every
field carrying a mnemonic is named `mnem`, which the guard reads as a
machine form.

Coding discipline: no compound one-liner statements.

usage:
  expand1.py preflight        the outer set and the cells file, nothing run
  expand1.py run [<n>]        the cpp loop, one line per finished run
  expand1.py aggregate        expand1_runs.jsonl -> expand1.json
  expand1.py tally            the counts, printed
  expand1.py tables           the per-target table with cpp's column, and
                              the all-four / all-five lines
  expand1.py handful          the handful's ten cells on cpp beside c
  expand1.py causes           what did not work on cpp, by cause
  expand1.py sources          the cpp source beside the c source, per cell
  expand1.py interp_run [<n>] the interpreted handful, one line per run
  expand1.py interp_table     the interpreted table the brief asks for
  expand1.py interp_sample    the sample rule LITERAL, and nothing run
  expand1.py jit              what the corpus's JIT output actually is
  expand1.py report           expand1.md
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
INTERP = os.path.join(EMULATION, "interp")
CPP = os.path.join(EMULATION, "cpp")
sys.path.insert(0, HANDFUL)
sys.path.insert(0, INTERP)
sys.path.insert(0, CPP)

# THE FROZEN DRIVER (task ap6, 2026-09-10).  This closed pass's driver
# reads `handful_frozen.py`, which is `handful.py` copied byte for byte
# on 2026-09-10, before the nine task-name gates were stripped out of
# it, so this pass answers exactly as its own log records.  The ONE
# driver is `handful.py`, which carries no task gate and is entered
# through `autopoly.py`.
import handful_frozen as H                                      # noqa: E402
import autopoly4 as AP4                                         # noqa: E402
import cpp_render as CPR                                        # noqa: E402

CELLS = os.path.join(HERE, "expand1_cells.json")
RUNS = os.path.join(HERE, "expand1_runs.jsonl")
AGGREGATE = os.path.join(HERE, "expand1.json")
REPORT = os.path.join(HERE, "expand1.md")
SRC_DIR = os.path.join(HERE, "src_expand1")
PRIMITIVE = os.path.join(HERE, "expand1_primitive.json")
SPELLINGS = os.path.join(HERE, "expand1_spellings.json")
INTERP_RUNS = os.path.join(HERE, "expand1_interp.jsonl")
INTERP_AGGREGATE = os.path.join(HERE, "expand1_interp.json")

# TASK ap4'S OWN PRODUCTS, read and never written: they are the four
# targets this task puts a fifth beside.
AP4_RUNS = os.path.join(HERE, "autopoly4_runs.jsonl")
AP4_AGGREGATE = os.path.join(HERE, "autopoly4.json")
AP4_CELLS = os.path.join(HERE, "autopoly4_cells.json")

HOST_FOLDER = ("PseudoCoupHQ/Research/oracle/"
               "cross_construction/emulation/autopoly")

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_EX1"

# THE ONE COMPILED TARGET THIS LOOP RUNS.  The other four are on task
# ap4's store and are read from there; running them again would spend
# an hour to reproduce an answer that is already recorded, and the
# change table of a task that changed nothing about them would be
# empty by construction.
TARGETS = ["cpp"]

# The five, in the order the report's columns take.  `handful.targets()`
# answers with this list for this task and it is asked rather than
# restated.
FIVE = None


def use_task_ex1():
    """the imported driver and the imported loop pointed at THIS task's
    paths, this task's target list and this task's memory bound.

    `handful.use_task_ex1` answers `fixes_are_on`, `primitive_first`
    and `setup_is_allowed` exactly as `ap4` answers them, so the ROUTE
    a cpp run is put through is the route the four were put through.
    Every path `handful.py` or `autopoly4.py` writes through is
    repointed to an `expand1_*` name, so no lane of this task can write
    task ap1's, ap2's, ap3's or ap4's products."""
    global FIVE
    H.use_task_ex1()
    H.RESULTS = AGGREGATE
    H.REPORT = REPORT
    H.SRC_DIR = SRC_DIR
    H.PRIMITIVE = PRIMITIVE
    H.SPELLINGS = SPELLINGS
    H.CELLS = CELLS
    H.HOST_FOLDER = HOST_FOLDER
    H.ABORT_KB = ABORT_KB
    H.ABORT_NAME = ABORT_NAME
    AP4.CELLS = CELLS
    AP4.RUNS = RUNS
    AP4.AGGREGATE = AGGREGATE
    AP4.REPORT = REPORT
    AP4.SRC_DIR = SRC_DIR
    AP4.PRIMITIVE = PRIMITIVE
    AP4.SPELLINGS = SPELLINGS
    AP4.TARGETS = TARGETS
    AP4.ABORT_KB = ABORT_KB
    AP4.ABORT_NAME = ABORT_NAME
    AP4.BEFORE_RUNS = AP4_RUNS
    AP4.HOST_FOLDER = HOST_FOLDER
    FIVE = H.targets()


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


def cell_key(run):
    return (run["mnem"], run["shape"], run["key_width"])


def escaped(text):
    return ("%s" % text).replace("|", "/")


# ==================================================================
# section 1: THE cpp HALF -- task ap4's loop with one more target
# ==================================================================

def preflight_command():
    """the outer set as the loop will walk it, and the cells file this
    task uses: task ap4's, copied here and its counts re-measured, so
    the two loops walk the same 253 cells and nothing of task ap4's is
    written."""
    if not os.path.exists(CELLS):
        source = read_json(AP4_CELLS)
        write_json(CELLS, source)
        say("copied task ap4's cells file to %s" % CELLS)
    mine = read_json(CELLS)
    theirs = read_json(AP4_CELLS)
    same = json.dumps(mine, sort_keys=True) == json.dumps(theirs,
                                                          sort_keys=True)
    say("the cells file is task ap4's, object for object: %s" % same)
    say("cpp, as this machine answers it: %s" % CPR.clangxx_answer())
    say("cpp ship flags, LITERAL: %s"
        % " ".join([CPR.CLANGXX] + CPR.SHIP_FLAGS))
    say("their source: %s" % CPR.SHIP_FLAGS_SOURCE)
    say("the five targets `handful.targets()` answers with: %s"
        % ", ".join(FIVE))
    say("")
    return AP4.preflight_command()


def run_command(limit):
    """task ap4's own loop, over this task's one target."""
    return AP4.run_command(limit)


def aggregate_command():
    return AP4.aggregate_command()


def tally_command():
    return AP4.tally_command()


def causes_command():
    """what did not work on cpp, by cause.  `autopoly4.causes_command`
    sums over `document["meta"]["targets"]`, which for this task's
    aggregate is cpp alone, and its own header sentence says "the four
    targets summed" -- true of the task that wrote it and not of this
    one, so the header is said here and the counting is still that
    function's."""
    document = read_json(AGGREGATE)
    say("Table -- what did not work on cpp, by cause.  One target, so "
        "`runs` is cells and `rows` is their attested ledger rows.")
    say("")
    say("| cause | runs | ledger rows |")
    say("|---|---|---|")
    held = document["causes"]["cpp"]
    ordered = sorted(held, key=lambda name: (-held[name]["runs"], name))
    total = 0
    for name in ordered:
        say("| %s | %d | %d |"
            % (escaped(name), held[name]["runs"],
               held[name]["ledger_rows"]))
        total = total + held[name]["runs"]
    say("")
    say("runs carrying a cause: %d of %d" % (total,
                                             document["meta"]["runs"]))
    return 0


# ------------------------------------------------------------------
# the two tables the brief asks for by name
# ------------------------------------------------------------------

def proved_on(run):
    """whether this run's cell is proved on this target.

    THE RULE IS TASK ap4'S OWN AND IS CALLED, NOT RESTATED:
    `autopoly4.outcome_of` reads every place of the run's destination
    REGISTER (two, where task ap2's fix 3 split a 128-bit place into
    halves) and takes the weakest of their gate answers.  Re-deriving
    it here from `destination_place` alone gave a different all-four
    count -- 142 against task ap4's own 162 -- which is exactly the
    kind of quiet drift a report at two widths must not carry."""
    return AP4.outcome_of(run) in ("proved",
                                   "proved under caller extension")


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


STEPS = ["attempted", "rendered", "compiled", "LANDED",
         "LANDED_ELSEWHERE", "NOT_COLLAPSED", "proved",
         "proved under caller extension", "sat", "undecided", "refused"]


def tables_command():
    """THE cpp COLUMN, in the per-target table's own shape, and the
    all-four and all-five lines side by side.

    Every figure in Table 1 is read off an AGGREGATE, never re-counted
    here: cpp's from this task's `expand1.json`, the other four from
    task ap4's `autopoly4.json`, both written by the same function
    (`autopoly4.aggregate_command`) over their own stores."""
    cells = read_json(CELLS)
    ledger_of = ledger_index(cells)
    total_rows = 0
    for key in ledger_of:
        total_rows = total_rows + ledger_of[key]
    mine = read_json(AGGREGATE)
    theirs = read_json(AP4_AGGREGATE)
    columns = {"cpp": mine["per_language"]["cpp"]}
    for lang in theirs["per_language"]:
        columns[lang] = theirs["per_language"][lang]
    order = []
    for lang in FIVE:
        if lang in columns:
            order.append(lang)
    say("Table 1 -- one row per target. `cells` counts runs; `rows` is "
        "the attested ledger rows those cells cover and `share` that as "
        "a percentage of %d.  cpp's column is this task's own aggregate; "
        "the other four are task ap4's, read off `autopoly4.json` and "
        "not re-run." % total_rows)
    say("")
    say("| step or verdict | %s |" % " | ".join(order))
    say("|---|%s" % ("---|" * len(order)))
    for name in STEPS:
        parts = []
        for lang in order:
            held = columns[lang].get(name)
            if held is None:
                parts.append("--")
                continue
            parts.append("%d cells, %d rows, %s%%"
                         % (held["runs"], held["ledger_rows"],
                            held["share_percent"]))
        say("| `%s` | %s |" % (name, " | ".join(parts)))
    say("")

    # THE TWO WIDTHS, side by side and neither re-defining the other.
    proved_cpp = set()
    for run in read_runs(RUNS):
        if proved_on(run):
            proved_cpp.add(cell_key(run))
    four = []
    for entry in theirs["across_targets"]["4"]["cell_list"]:
        four.append((entry["mnem"], entry["shape"], entry["key_width"]))
    five = []
    for key in four:
        if key in proved_cpp:
            five.append(key)
    say("Table 2 -- the polyfill-complete set at BOTH widths, which is "
        "what the brief asks for until the owner says which counts.  A cell "
        "counts as proved on a target when the gate answered `unsat` at "
        "that target's destination place, at the 3,000 ms ceiling of "
        "record or under the caller-extension re-pose.")
    say("")
    say("| width | targets | cells | ledger rows | share |")
    say("|---|---|---|---|---|")
    rows_four = 0
    for key in four:
        rows_four = rows_four + ledger_of.get(key, 0)
    rows_five = 0
    for key in five:
        rows_five = rows_five + ledger_of.get(key, 0)
    say("| all four | c, rust, go, swift | %d | %d | %s%% |"
        % (len(four), rows_four, rate(rows_four, total_rows)))
    say("| all five | c, cpp, rust, go, swift | %d | %d | %s%% |"
        % (len(five), rows_five, rate(rows_five, total_rows)))
    say("")
    say("cells proved on all four and NOT on cpp: %d"
        % (len(four) - len(five)))
    for key in four:
        if key in proved_cpp:
            continue
        say("   `%s` %s %s   ledger rows %d"
            % (key[0], key[1], key[2], ledger_of.get(key, 0)))
    say("")
    say("cpp's own proved set: %d cells" % len(proved_cpp))
    only_cpp = []
    for key in sorted(proved_cpp):
        if key in four:
            continue
        only_cpp.append(key)
    say("cells proved on cpp that are not in the all-four set: %d"
        % len(only_cpp))
    say("")
    say("Table 3 -- how many of the five each cell is proved on, from "
        "task ap4's own per-cell list plus cpp's.")
    say("")
    say("| proved on | cells | ledger rows | share |")
    say("|---|---|---|---|")
    counted = {}
    for many in ("4", "3", "2", "1", "0"):
        for entry in theirs["across_targets"][many]["cell_list"]:
            key = (entry["mnem"], entry["shape"], entry["key_width"])
            total = int(many)
            if key in proved_cpp:
                total = total + 1
            counted.setdefault(total, []).append(key)
    for total in sorted(counted, reverse=True):
        rows = 0
        for key in counted[total]:
            rows = rows + ledger_of.get(key, 0)
        say("| %d of 5 | %d | %d | %s%% |"
            % (total, len(counted[total]), rows,
               rate(rows, total_rows)))
    return 0


def handful_command():
    """THE HANDFUL'S TEN CELLS ON cpp BESIDE c's VERDICTS, which is the
    brief's own first deliverable: the ten cells run through the same
    loop, and c's answer for each read off task ap4's store."""
    mine = {}
    for run in read_runs(RUNS):
        mine[cell_key(run)] = run
    theirs = {}
    for run in read_runs(AP4_RUNS):
        if run["lang"] != "c":
            continue
        theirs[cell_key(run)] = run
    say("| cell | route on cpp | landed on cpp | cpp's verdict | c's "
        "verdict | the two sources |")
    say("|---|---|---|---|---|---|")
    agree = 0
    same_source = 0
    for asked in AP4.HANDFUL_CELLS:
        run = mine.get(asked)
        other = theirs.get(asked)
        if run is None:
            say("| `%s` %s %s | -- | -- | not run | %s | -- |"
                % (asked[0], asked[1], asked[2],
                   AP4.one_line_verdict(other) if other else "--"))
            continue
        place = H.destination_place(run)
        landing = "--"
        if place is not None:
            landing = (place.get("landing") or {}).get("verdict") or "--"
        verdict = AP4.one_line_verdict(run)
        their_verdict = "--"
        if other is not None:
            their_verdict = AP4.one_line_verdict(other)
        if verdict == their_verdict:
            agree = agree + 1
        note = "not compared"
        if other is not None:
            note = source_note(run, other)
            if note == "the same text but for the header and the linkage":
                same_source = same_source + 1
        say("| `%s` %s %s | %s | %s | %s | %s | %s |"
            % (asked[0], asked[1], asked[2], run.get("route") or "--",
               landing, escaped(verdict), escaped(their_verdict), note))
    say("")
    say("`sub` imm_gpr 64 is one of the handful's ten and is NOT in the "
        "253-cell outer set this loop walks, so no run of it exists on "
        "either store; task ap4's own reproduction line says the same "
        "of it, LITERAL: `the handful's forty pairs: 32 agree character "
        "for character, 35 agree on the verdict, 4 not in this outer "
        "set`.")
    say("")
    say("of the ten, cpp's verdict is c's: %d" % agree)
    say("of the ten, cpp's source is c's but for the header and the "
        "linkage: %d" % same_source)
    return 0


def strip_the_two(text):
    """the rendered source with the two things cpp spells differently
    removed -- the linkage and the header names -- and the leading
    comment block with them, so what is left is the DECLARATION and the
    EXPRESSION and those can be compared character for character.

    The comment is dropped because it names the file that rendered it
    (`emulate.py Renderer` against `cpp_render.py CppRenderer`), which
    is a true difference about the printer and not about the source it
    printed."""
    out = []
    inside = False
    started = False
    for line in (text or "").splitlines():
        stripped = line.strip()
        if not started and stripped.startswith("/*"):
            inside = True
        if inside:
            if "*/" in stripped:
                inside = False
                started = True
            continue
        started = True
        if stripped == 'extern "C"':
            continue
        if stripped in ("#include <cstdint>", "#include <stdint.h>"):
            continue
        if stripped in ("#include <cstring>", "#include <string.h>"):
            continue
        out.append(line)
    joined = "\n".join(out)
    # THE LABEL CARRIES THE TARGET'S OWN NAME, which is what makes the
    # symbol unique per run and is not a difference in what the source
    # COMPUTES.  Both are folded to one word before the comparison.
    import re
    return re.sub(r"__(?:cpp|c)\b", "__LANG", joined)


def source_note(run, other):
    mine = H.destination_place(run) or {}
    theirs = H.destination_place(other) or {}
    left = strip_the_two(mine.get("source"))
    right = strip_the_two(theirs.get("source"))
    if not left or not right:
        return "one side rendered nothing"
    if left == right:
        return "the same text but for the header and the linkage"
    return "different text"


def sources_command():
    """the cpp source beside the c source, per handful cell, LITERAL."""
    mine = {}
    for run in read_runs(RUNS):
        mine[cell_key(run)] = run
    theirs = {}
    for run in read_runs(AP4_RUNS):
        if run["lang"] != "c":
            continue
        theirs[cell_key(run)] = run
    for asked in AP4.HANDFUL_CELLS:
        run = mine.get(asked)
        if run is None:
            continue
        place = H.destination_place(run)
        if place is None or not place.get("rendered"):
            continue
        say("")
        say("== `%s` %s %s   place %r   route %s"
            % (asked[0], asked[1], asked[2], place["writes"],
               run.get("route")))
        say("   the cpp source, LITERAL:")
        for line in (place.get("source") or "").splitlines():
            say("      %s" % line)
        other = theirs.get(asked)
        if other is None:
            continue
        say("   beside c's: %s" % source_note(run, other))
    return 0


# ==================================================================
# section 2: THE INTERPRETED HALF
# ==================================================================

JIT_FOLDERS = ("javascript", "dart", "csharp")


def jit_command():
    """WHAT THE CORPUS'S JIT OUTPUT ACTUALLY IS, measured rather than
    assumed, because the brief's instruction is conditional on it:
    "where the language has a JIT whose output the corpus already
    carves, ALSO carve and gate that output the compiled way"."""
    op = os.path.normpath(os.path.join(EMULATION, "..", "..", "..",
                                       "op_pipeline"))
    say("| folder | files | the first line of its dump, LITERAL |")
    say("|---|---|---|")
    for lang in JIT_FOLDERS:
        folder = os.path.join(op, "jit_out_%s" % lang)
        if not os.path.isdir(folder):
            say("| jit_out_%s | absent | -- |" % lang)
            continue
        names = sorted(os.listdir(folder))
        first = "--"
        for name in names:
            if not name.endswith("_opt.txt") and name != "all_opt.txt":
                continue
            handle = open(os.path.join(folder, name))
            for line in handle:
                if line.strip():
                    first = line.strip()
                    break
            handle.close()
            break
        say("| jit_out_%s | %d | `%s` |"
            % (lang, len(names), escaped(first)))
    say("")
    say("what the corpus holds as ARCH-UNITS, per language "
        "(`oracle/arch_opcodes/single_opcode_units.json`):")
    say("")
    document = read_json(os.path.join(EMULATION, "..", "..",
                                      "arch_opcodes",
                                      "single_opcode_units.json"))
    groups = document["single_opcode_groups"]
    say("| language | in the file | narrow single-opcode groups |")
    say("|---|---|---|")
    for lang in ("c", "cpp", "rust", "go", "swift", "java", "cpython",
                 "php", "ruby", "javascript", "dart", "csharp"):
        held = groups.get(lang)
        if held is None:
            say("| %s | no | -- |" % lang)
            continue
        say("| %s | yes | %d |" % (lang, len(held.get("narrow", {}))))
    return 0


def interp_sample_command():
    import interp_check as IC
    return IC.sample_command()


HANDFUL_CELLS_FILE = os.path.join(HANDFUL, "handful_cells.json")
"""THE CELLS THE INTERPRETED HALF READS, and it is the handful's own
file rather than the 253-cell outer set.  `sub` imm_gpr 64 is one of
the handful's ten and is NOT in the outer set -- task ap4's own
reproduction line says so, LITERAL: "the handful's forty pairs: 32
agree character for character, 35 agree on the verdict, 4 not in this
outer set" -- so reading the ten out of the outer set would refuse that
cell for a reason that is about the outer set and not about any
interpreted language."""


def interp_run_command(limit):
    import interp_check as IC
    return IC.run_command(INTERP_RUNS, HANDFUL_CELLS_FILE, limit)


def interp_table_command():
    import interp_check as IC
    return IC.table_command(INTERP_RUNS)


def interp_aggregate_command():
    import interp_check as IC
    return IC.aggregate_command(INTERP_RUNS, INTERP_AGGREGATE)


# ==================================================================
# section 3: THE REPORT
# ==================================================================

def captured(function, *arguments):
    """one command's own printed output, captured so the report and the
    lane log carry the same characters."""
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
    """expand1.md: the cpp column, the all-four and all-five lines, the
    interpreted handful table, the sample rule LITERAL, and by cause
    what did not run.  Every table below is also a command of this
    program, and the text here is that command's own output."""
    import interp_check as IC
    lines = []
    lines.append("# expand1 -- task ex1: beyond the four")
    lines.append("")
    lines.append("Node: hq.research.arch_unit_oracle.cross_construction"
                 ".autopoly; the interpreted half also serves "
                 "node_0_3_1_12_remaining_languages.")
    lines.append("")
    lines.append("Written by `expand1.py report`. Every table is the "
                 "output of a command of this program, captured: "
                 "`tables`, `handful`, `causes`, `interp_table` and "
                 "`interp_sample`.")
    lines.append("")
    lines.append("## 1. cpp, the fifth compiled target")
    lines.append("")
    lines.append("The route is task ap4's, unchanged: the primitive "
                 "lookup first, the cell's term in the target's own "
                 "operators where there is no primitive, compiled at "
                 "the corpus's own cpp ship flags "
                 "(`%s`), carved by `lane_gen.DRIVER`'s own `extract`, "
                 "and put back to z3 against the cell's own term."
                 % " ".join([CPR.CLANGXX] + CPR.SHIP_FLAGS))
    lines.append("")
    lines.append(captured(tables_command))
    lines.append("")
    lines.append("## 2. the handful's ten cells on cpp, beside c")
    lines.append("")
    lines.append(captured(handful_command))
    lines.append("")
    lines.append("## 3. what did not work on cpp, by cause")
    lines.append("")
    lines.append(captured(causes_command))
    lines.append("")
    lines.append("## 4. the interpreted handful")
    lines.append("")
    lines.append("There is no carve for an interpreted target, so the "
                 "emulation is SOURCE in that language and the check is "
                 "the fuzz census's method over a stated sample. An "
                 "agreement is not a proof and no interpreted run "
                 "carries a gate verdict.")
    lines.append("")
    lines.append(captured(interp_table_command))
    lines.append("")
    lines.append("## 5. the JIT output the corpus holds")
    lines.append("")
    lines.append("The brief's instruction is conditional -- ALSO carve "
                 "and gate the JIT output where the corpus already "
                 "carves it -- and the condition does not hold. What "
                 "`jit_out_*` holds is each JIT's OWN dump text, in "
                 "three different formats, none of them objdump's; the "
                 "carve this line uses is `lane_gen.DRIVER`'s `extract` "
                 "over objdump, and the corpus holds no arch-unit for "
                 "javascript, dart or csharp at all. Building a reader "
                 "for three new instruction-text formats is a new "
                 "instrument, which is a flag for the coordinator and "
                 "not something this task works around.")
    lines.append("")
    lines.append(captured(jit_command))
    lines.append("")
    lines.append("## 6. the sample rule, LITERAL, as it was run")
    lines.append("")
    lines.append("```")
    for line in IC.SAMPLE_RULE.splitlines():
        lines.append(line)
    lines.append("```")
    lines.append("")
    lines.append(captured(interp_sample_command))
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("wrote %s (%d lines)" % (REPORT, len(lines)))
    return 0


def main(argv):
    use_task_ex1()
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
    if argv[0] == "tally":
        return tally_command()
    if argv[0] == "tables":
        return tables_command()
    if argv[0] == "handful":
        return handful_command()
    if argv[0] == "sources":
        return sources_command()
    if argv[0] == "causes":
        return causes_command()
    if argv[0] == "jit":
        return jit_command()
    if argv[0] == "interp_sample":
        return interp_sample_command()
    if argv[0] == "interp_run":
        limit = None
        if len(argv) > 1:
            limit = int(argv[1])
        return interp_run_command(limit)
    if argv[0] == "interp_table":
        return interp_table_command()
    if argv[0] == "interp_aggregate":
        return interp_aggregate_command()
    if argv[0] == "report":
        return report_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
