#!/usr/bin/env python3
"""interp_check.py -- task ex1: THE CHECK FOR AN INTERPRETED TARGET,
defined here and stated LITERAL before it runs.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly, with
`node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages`.

WHY THERE HAS TO BE A DIFFERENT CHECK, in one sentence: for a compiled
target the emulation's machine code IS the object, so it can be carved,
put on the canonical form and PROVED equal to the cell's term over
every input by z3; an interpreted target hands us no such object -- the
machine code that runs is the interpreter's own handler, a different
unit under a different node -- so the emulation is SOURCE and the only
evidence available is what the interpreter ANSWERS.

THE CHECK, and it is the fuzz census's method
(`node_0_3_0_2_kind_fuzz_clustering`, "the method, as designed
2026-08-14": generate a minimal program per thing, RUN it, record what
came back, compare by relation):

  1. the cell's mapping is rendered as source in the target's own
     operators over the target's own value model (`interp_render.py`);
  2. a SAMPLE of input points is built by the rule below, which is
     stated in full before anything runs and includes the cell's own
     edge regions;
  3. the REFERENCE's answer at each point is the cell's own z3 term
     with the point substituted and `z3.simplify` applied -- the
     reference simulator's own mapping, evaluated, and not a second
     model of it;
  4. the INTERPRETER's answer at each point is what the rendered source
     prints when the runner is handed every point on standard input,
     one process for the whole sample;
  5. the two are compared point by point.  An AGREEMENT is two integers
     that are equal.  A DISAGREEMENT is two integers that are not, and
     it is reported with the point LITERAL -- it is what a `sat` is on
     the compiled route: a witness that the two mappings differ.  A
     DECLINE is a point where one side has no value: the interpreter
     raised (division by zero raises in every one of these languages --
     lane ex1_l2 measured `ZeroDivisionError`, `DivisionByZeroError`,
     `ArithmeticException`, `RangeError`,
     `IntegerDivisionByZeroException`, `DivideByZeroException`), or the
     reference's own term does not evaluate to a numeral there.
     DECLINES ARE NOT SCORED, which is this line's own standing rule
     (`CLAUDE.md`, "Declines are never scored"): they are dropped from
     the numerator and the denominator and counted separately by cause.

WHAT AN AGREEMENT IS AND IS NOT.  It is not a proof.  A cell whose
whole sample agrees is EVIDENCE that the rendering computes the cell's
mapping, at the strength the fuzz line's own evidence doctrine gives an
executed measurement, and nothing more; a single disagreement is
conclusive the other way, which is the asymmetry that makes the check
worth running at all.  The report never writes `PROVED_ON_SHIP` for an
interpreted run.

THE SAMPLE RULE, LITERAL -- this is the object the brief asks to be
stated before it runs, and `SAMPLE_RULE` below is the same text the
program itself prints and the report carries:

%(rule)s

THE PLACE THAT IS CHECKED.  One per (cell, target): the run's
DESTINATION place, which is `handful.destination_place`'s own rule --
the first place that is not the flags, or the flags place when that is
all there is.  It is the same place the compiled route's verdict is
read from, so the two columns of the report are about the same object.

MEMORY: one collecting process; every runner is a separate short-lived
process handed the whole sample at once, so no per-point process is
ever started.  Bound 6 GB, named abort ABORT_MEMORY_EX1.

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

The pairing here is fixed in advance and carries no token: one run per
(cell, target) over the handful's ten cells, which are ratified
intention, and the seven targets whose runners this task found.  The
sample is built from WIDTHS, never from a mnemonic.

Coding discipline: no compound one-liner statements.

usage:
  interp_check.py sample     the sample rule LITERAL, and the point
                             counts it gives for the handful's places
"""

import json
import os
import random
import resource
import struct
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EMULATION = os.path.normpath(os.path.join(HERE, ".."))
HANDFUL = os.path.join(EMULATION, "handful")
CROSS = os.path.normpath(os.path.join(HERE, "..", ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, HANDFUL)
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402
import interp_render as IR                                       # noqa: E402

SRC_DIR = os.path.join(HERE, "src_ex1")
WORK_DIR = os.environ.get("TMPDIR") or "/tmp"

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_EX1"

SEED = 20260909
BUDGET_CEILING = 20000
RUNNER_TIMEOUT = 900

SAMPLE_RULE = """THE SAMPLE, for a place whose emulation takes k arrivals of widths
w_1 .. w_k.

  the per-arrival budget b = max(4, int(20000 ** (1.0 / k)))

  P(an INTEGER arrival of width w) is this list, in this order,
  deduplicated, every value taken modulo nothing and dropped when it
  is not less than 2^w, then cut to its first b entries:
      0, 1, 2, 3, 7, 100,
      2^(w-1) - 1, 2^(w-1), 2^(w-1) + 1,          the sign boundary
      2^w - 2, 2^w - 1,                           the top, and -1
      w - 1, w, w + 1,                            this width's shift counts
      7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, the other widths'
      then 8 values from random.Random(20260909).randrange(2^w)

  P(a FLOAT arrival of width w, which reaches the emulation as its
  IEEE bit pattern) is this list, in this order, deduplicated, cut to
  its first b entries:
      +0, -0, 1.0, -1.0, 2.0, 0.5, -0.5,
      the smallest subnormal, the largest subnormal,
      the smallest normal, the largest finite,
      +inf, -inf, a quiet NaN, a signalling NaN,
      then 8 values from random.Random(20260909).randrange(2^w)

  THE SAMPLE is the ordered cross product P(a_1) x ... x P(a_k), in
  that order.  Its size is at most 20,000 by the budget above, and the
  run record carries the exact count.

  WHY b IS A CEILING AND NOT A CHOICE OF POINTS: the edge values come
  FIRST in every list, so cutting to b drops ordinary values before it
  drops an edge.  A place with one or two arrivals is never cut at all
  (b is 20000 and 141), so the handful's edges are all present; a
  place with four is cut to 11 per arrival, and the run record says
  which values those were."""

__doc__ = __doc__ % {"rule": SAMPLE_RULE}


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


# ==================================================================
# section 1: THE SAMPLE
# ==================================================================

def budget(count):
    if count < 1:
        return 1
    return max(4, int(BUDGET_CEILING ** (1.0 / count)))


def integer_points(width, cut):
    """P(an integer arrival of width w), exactly as SAMPLE_RULE states
    it."""
    ordered = [0, 1, 2, 3, 7, 100]
    if width >= 2:
        ordered.append((1 << (width - 1)) - 1)
        ordered.append(1 << (width - 1))
        ordered.append((1 << (width - 1)) + 1)
    ordered.append((1 << width) - 2)
    ordered.append((1 << width) - 1)
    ordered.append(width - 1)
    ordered.append(width)
    ordered.append(width + 1)
    for one in (7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65):
        ordered.append(one)
    source = random.Random(SEED)
    for _index in range(8):
        ordered.append(source.randrange(1 << width))
    out = []
    for one in ordered:
        if one < 0:
            continue
        if one >= (1 << width):
            continue
        if one in out:
            continue
        out.append(one)
    return out[:cut]


def float_points(width, cut):
    """P(a float arrival of width w), as its bit patterns."""
    if width == 32:
        pack = "<f"
        unpack = "<I"
        quiet = 0x7fc00000
        loud = 0x7f800001
        smallest_sub = 0x00000001
        largest_sub = 0x007fffff
        smallest_norm = 0x00800000
        largest = 0x7f7fffff
        plus_inf = 0x7f800000
        minus_inf = 0xff800000
    else:
        pack = "<d"
        unpack = "<Q"
        quiet = 0x7ff8000000000000
        loud = 0x7ff0000000000001
        smallest_sub = 0x0000000000000001
        largest_sub = 0x000fffffffffffff
        smallest_norm = 0x0010000000000000
        largest = 0x7fefffffffffffff
        plus_inf = 0x7ff0000000000000
        minus_inf = 0xfff0000000000000

    def bits_of(value):
        return struct.unpack(unpack, struct.pack(pack, value))[0]

    ordered = [bits_of(0.0), bits_of(-0.0), bits_of(1.0), bits_of(-1.0),
               bits_of(2.0), bits_of(0.5), bits_of(-0.5),
               smallest_sub, largest_sub, smallest_norm, largest,
               plus_inf, minus_inf, quiet, loud]
    source = random.Random(SEED)
    for _index in range(8):
        ordered.append(source.randrange(1 << width))
    out = []
    for one in ordered:
        if one in out:
            continue
        out.append(one)
    return out[:cut]


def points_for(params):
    """the per-arrival point lists, in arrival order."""
    cut = budget(len(params))
    out = []
    for param in params:
        if param["kind"] == "fp":
            out.append(float_points(param["bits"], cut))
            continue
        out.append(integer_points(param["bits"], cut))
    return out


def sample_of(lists):
    """the ordered cross product, built without holding an intermediate
    list of every prefix: one tuple at a time."""
    if not lists:
        return [()]
    out = [()]
    for one in lists:
        grown = []
        for prefix in out:
            for value in one:
                grown.append(prefix + (value,))
        out = grown
    return out


# ==================================================================
# section 2: THE REFERENCE'S ANSWER AT A POINT
# ==================================================================

def symbols_of(term):
    """every free symbol of the term, by name, with its own sort."""
    out = {}
    seen = set()

    def walk(node):
        key = node.get_id()
        if key in seen:
            return
        seen.add(key)
        if z3.is_const(node) and \
                node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            out[node.decl().name()] = node
            return
        for index in range(node.num_args()):
            walk(node.arg(index))

    walk(term)
    return out


def reference_answers(term, params, points):
    """the cell's own term at each point: substituted and simplified.

    A point is a tuple of arrival values in the parameter plan's order,
    each less than 2^(that arrival's planned width); it is substituted
    into the symbol at the SYMBOL's own width, zero-extended, which is
    exactly what a c emulation receives when the renderer plans a
    narrow holder for a 64-bit register."""
    held = symbols_of(term)
    order = []
    for param in params:
        name = "seed_%s" % param["family"]
        symbol = held.get(name)
        order.append(symbol)
    out = []
    for point in points:
        pairs = []
        for index, symbol in enumerate(order):
            if symbol is None:
                continue
            pairs.append((symbol,
                          z3.BitVecVal(point[index], symbol.size())))
        answer = z3.simplify(z3.substitute(term, *pairs))
        if z3.is_bv_value(answer):
            out.append(answer.as_long())
            continue
        out.append(None)
    return out


# ==================================================================
# section 3: THE INTERPRETER'S ANSWER AT EVERY POINT
# ==================================================================

CSHARP_PROJECT = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>disable</Nullable>
    <AssemblyName>emu</AssemblyName>
    <StartupObject>Emu</StartupObject>
  </PropertyGroup>
</Project>
'''


def run_folder(lang):
    folder = os.path.join(WORK_DIR, "ex1_interp_%s" % lang)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def write_for_running(lang, label, source):
    """the source where the runner needs it.  Two languages dictate the
    file name: java's single-file launcher wants the public class's own
    name, and c#'s `dotnet run` wants a project directory -- which is
    also why the c# folder is reused across runs, so its restore is
    done once."""
    folder = run_folder(lang)
    if lang == "java":
        path = os.path.join(folder, "Emu.java")
    elif lang == "csharp":
        path = os.path.join(folder, "Program.cs")
        project = os.path.join(folder, "emu.csproj")
        if not os.path.exists(project):
            handle = open(project, "w")
            handle.write(CSHARP_PROJECT)
            handle.close()
    else:
        path = os.path.join(folder, "emu%s"
                            % IR.DIALECTS[lang].suffix)
    handle = open(path, "w")
    handle.write(source)
    handle.close()
    return folder, path


def interpreter_answers(lang, label, source, points, timeout=None):
    """one process for the whole sample.  Returns (answers, problem):
    `answers` is one entry per point -- an integer, or the runner's own
    `RAISE:<kind>` token -- or None with the problem stated when the
    runner itself did not run.

    TASK ex2's ONE ADDITION: `timeout` overrides `RUNNER_TIMEOUT` for
    this call (None keeps ex1's own 900 s, unchanged); a timeout is no
    longer just a string -- it is a dict `{"kind": "TIMEOUT", "seconds":
    ..., "points_reached": ...}`, the point count read off whatever the
    process had already printed before it was stopped (`subprocess`'s
    own `TimeoutExpired.stdout`, captured because `capture_output` is
    already on). TIMEOUT is not a new outcome name -- it is the word the
    law already uses for a lane or a solver that ran out of room."""
    run_timeout = timeout if timeout is not None else RUNNER_TIMEOUT
    folder, path = write_for_running(lang, label, source)
    lines = []
    for point in points:
        parts = []
        for value in point:
            parts.append("%d" % value)
        lines.append(" ".join(parts))
    fed = "\n".join(lines) + "\n"
    environment = dict(os.environ)
    environment["HOME"] = folder
    environment["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
    environment["DOTNET_NOLOGO"] = "1"
    try:
        command, problem = IR.DIALECTS[lang].prepare(folder, path, label,
                                                     environment)
    except subprocess.TimeoutExpired:
        return None, "the runner's own build did not finish in time"
    except OSError as problem:
        return None, "%s" % problem
    if command is None:
        return None, problem
    try:
        done = subprocess.run(command, input=fed, capture_output=True,
                              text=True, timeout=run_timeout,
                              cwd=folder, env=environment)
    except OSError as problem:
        return None, "%s: %s" % (command[0], problem.strerror)
    except subprocess.TimeoutExpired as expired:
        reached = 0
        for line in (expired.stdout or "").splitlines():
            if line.strip():
                reached = reached + 1
        return None, {"kind": "TIMEOUT", "seconds": run_timeout,
                      "points_reached": reached}
    text = done.stdout
    got = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        got.append(stripped)
    if len(got) != len(points):
        first = "(no diagnostic)"
        problem_text = (done.stderr or done.stdout).strip()
        if problem_text:
            first = problem_text.splitlines()[0][:300]
        return None, ("the runner answered %d lines for %d points, "
                      "exit %d: %s"
                      % (len(got), len(points), done.returncode, first))
    out = []
    for one in got:
        if one.startswith("RAISE:"):
            out.append(one)
            continue
        try:
            out.append(int(one))
        except ValueError:
            out.append("RAISE:unreadable answer %r" % one[:40])
    return out, None


# ==================================================================
# section 4: ONE RUN
# ==================================================================

def gloss_of(source, symbol):
    """the EMULATION's own body on one line: a GLOSS.  The LITERAL
    source is kept under `interp/src_ex1/` and the run record names it.

    The body is found by the emulation's own symbol, never by the first
    `return` in the file -- the prelude above it is full of them, and
    reading one of those is what the first pass of lane ex1_l7 printed
    in this column."""
    lines = (source or "").splitlines()
    for index, line in enumerate(lines):
        if symbol not in line:
            continue
        if "(" not in line:
            continue
        for after in lines[index:index + 4]:
            stripped = after.strip()
            if stripped.startswith("return "):
                return stripped[len("return "):].rstrip(";")
            if stripped.startswith("=> "):
                return stripped[len("=> "):].rstrip(";")
        # ruby: the body is the line under the `def`
        if index + 1 < len(lines):
            return lines[index + 1].strip()
    return ""


def one_run(shared, cells, asked, lang, timeout=None):
    """one (cell, interpreted target): the input, the render, the
    sample, the two answers, the comparison.

    TASK ex2's ONE ADDITION: `timeout`, threaded to
    `interpreter_answers` unchanged (None keeps ex1's own bound). A
    TIMEOUT is recorded as `record["outcome"] = "TIMEOUT"` with the
    point count reached, never as a `refusal_cause` -- it is a result
    by cause, not a refusal of the cell."""
    started = time.time()
    record = {"mnem": asked[0], "shape": asked[1],
              "key_width": asked[2], "lang": lang,
              "route": "source", "check": "the fuzz census's method"}
    held = None
    try:
        held = shared["driver"].cell_input(cells, asked)
    except Exception as problem:                             # noqa: BLE001
        record["refusal_cause"] = "the driver raised on this cell"
        record["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                               problem)
        record["seconds"] = time.time() - started
        return record
    record["row_id"] = held.get("row_id")
    record["line"] = held.get("line")
    record["attested_ledger_rows"] = (held.get("attestation")
                                      or {}).get("ledger_rows")
    if held.get("refusal_cause") is not None:
        record["refusal_cause"] = held["refusal_cause"]
        record["refusal_detail"] = held.get("refusal_detail")
        record["seconds"] = time.time() - started
        return record
    place = shared["driver"].destination_place({"places": held["places"]})
    if place is None:
        record["refusal_cause"] = "the cell writes no place"
        record["seconds"] = time.time() - started
        return record
    record["writes"] = place["writes"]
    record["bits"] = place["bits"]
    record["term_text"] = place["text"]
    # FIX 2 (task h2), IN THE DRIVER, and the interpreted route runs it
    # exactly where the compiled route runs it (`handful.py` around the
    # `working = place` line): a vector cell's place carries the whole
    # 128-bit register, so the lane the operation writes is projected
    # out of it and it is that lane which is rendered and checked.  A
    # place already split into halves is not asked again, which is task
    # ap2's fix 3.
    driver = shared["driver"]
    if driver.fixes_are_on() and place.get("halved") is None:
        projected = driver.projected_lane(shared["pipeline"], place,
                                          held["key_width"])
        if projected is not None:
            record["lane"] = projected["lane"]
            if projected.get("refusal_cause") is not None:
                record["refusal_cause"] = projected["refusal_cause"]
                record["refusal_detail"] = projected.get(
                    "refusal_detail")
                record["seconds"] = time.time() - started
                return record
            place = projected["place"]
            record["writes"] = place["writes"]
            record["bits"] = place["bits"]
            record["term_text"] = place["text"]
    if place.get("families") is None:
        record["refusal_cause"] = place.get("not_rendered")
        record["refusal_detail"] = place.get("not_rendered_detail")
        record["seconds"] = time.time() - started
        return record
    term = shared["driver"].renderer_input(place["term"],
                                           shared["driver"].TASK)
    # TASK ex2'S SECOND BOOKKEEPING FIX, found by the loop's own runs
    # over the full outer set (the handful's ten cells never hit it): a
    # PLACE NAME can carry a character invalid in an identifier, and the
    # label becomes the rendered FUNCTION NAME. Two are attested over
    # the whole 253-cell outer set, measured rather than assumed (every
    # `writes` string this loop ever saw was scanned character by
    # character): the dot task ap2's fix 3 puts on a halved place
    # (`flags.low`) or task h2's fix 2 puts on a projected vector lane
    # (`reg_xmm0.low`), and the hyphen a negative stack offset carries
    # (`stack_-8`, `push`'s own destination). `handful.one_place` (the
    # compiled route) sanitises the dot the same way
    # (`place["writes"].replace(".", "_")`) but NOT the hyphen -- it
    # has the identical gap, dormant only because every compiled cell
    # this loop met with a hyphenated `writes` was already refused
    # earlier, for an unrelated reason (`CAUSE_STATE`, "no answer
    # home"), before its label is ever built. That dormant gap is out
    # of this task's scope (the interpreted route only) and is on the
    # awaiting-the owner list. Both characters are sanitised here, and
    # nowhere else.
    safe_writes = place["writes"].replace(".", "_").replace("-", "_")
    label = "%s_%s_%s__%s__%s" % (asked[0], asked[1], asked[2],
                                  safe_writes, lang)
    renderer = IR.InterpRenderer(lang, place["families"],
                                 place["home"]["family"], place["bits"],
                                 label)
    try:
        source, symbol = renderer.render(term, place["text"])
    except E.Refused as refusal:
        record["refusal_cause"] = refusal.cause
        record["refusal_detail"] = refusal.detail
        record["seconds"] = time.time() - started
        return record
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    kept = os.path.join(SRC_DIR, label + IR.DIALECTS[lang].suffix)
    handle = open(kept, "w")
    handle.write(source)
    handle.close()
    record["source_path"] = os.path.join("interp/src_ex1",
                                         os.path.basename(kept))
    record["symbol"] = symbol
    record["rendered"] = True
    record["gloss"] = gloss_of(source, symbol)
    record["params"] = []
    for param in renderer.params:
        record["params"].append({"name": param["name"],
                                 "family": param["family"],
                                 "kind": param["kind"],
                                 "bits": param["bits"],
                                 "holder": param["holder"]})
    lists = points_for(renderer.params)
    points = sample_of(lists)
    record["sample_points"] = len(points)
    record["sample_per_arrival"] = []
    for one in lists:
        record["sample_per_arrival"].append(len(one))
    reference = reference_answers(term, renderer.params, points)
    answers, problem = interpreter_answers(lang, label, source, points,
                                           timeout=timeout)
    if answers is None:
        if isinstance(problem, dict) and problem.get("kind") == "TIMEOUT":
            record["outcome"] = "TIMEOUT"
            record["timeout_seconds"] = problem["seconds"]
            record["points_reached"] = problem["points_reached"]
            record["seconds"] = time.time() - started
            return record
        record["refusal_cause"] = "the runner did not answer"
        record["refusal_detail"] = problem
        record["seconds"] = time.time() - started
        return record
    agreements = 0
    disagreements = 0
    declines = {}
    first = None
    for index, point in enumerate(points):
        theirs = answers[index]
        ours = reference[index]
        if ours is None:
            key = ("the reference's own term does not evaluate to a "
                   "numeral at this point")
            declines[key] = declines.get(key, 0) + 1
            continue
        if not isinstance(theirs, int):
            key = "the interpreter %s" % theirs
            declines[key] = declines.get(key, 0) + 1
            continue
        if theirs == ours:
            agreements = agreements + 1
            continue
        disagreements = disagreements + 1
        if first is None:
            first = {"point": list(point),
                     "the reference's answer": ours,
                     "the interpreter's answer": theirs}
    record["agreements"] = agreements
    record["disagreements"] = disagreements
    record["declines"] = declines
    record["declined_points"] = len(points) - agreements - disagreements
    record["first_disagreement"] = first
    record["seconds"] = time.time() - started
    return record


# ==================================================================
# section 5: THE COMMANDS
# ==================================================================

def build_shared():
    """the driver, and the pipeline's own walk beside it.

    The walk is needed because task h2's FIX 2 -- the vector-lane
    projection -- asks the GATE whether the bits above the lane are the
    arrival's own bits passed through, and the interpreted route runs
    that fix for the same reason the compiled route does: a vector
    cell's place carries the whole 128-bit register and the lane the
    operation writes is what an emulation computes."""
    # THE FROZEN DRIVER (task ap6, 2026-09-10): task ex1/ex2's route
    # reads the copy of `handful.py` made before its task gates were
    # stripped, so a closed pass answers as its log records.
    import handful_frozen as H
    H.use_task_ex1()
    return {"driver": H, "pipeline": H.build_shared()}


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


def key_of(asked, lang):
    return "%s|%s|%s|%s" % (asked[0], asked[1], asked[2], lang)


def run_command(runs_path, cells_path, limit):
    """the interpreted handful: the ten cells on each target whose
    runner this machine has, one line on the store per finished run."""
    shared = build_shared()
    cells = shared["driver"].read_json(cells_path)
    say("the runners, as this machine answers them:")
    for lang in IR.LANGUAGES:
        say("   %-12s %s" % (lang, IR.runner_answer(lang)))
    say("")
    done = set()
    for run in read_runs(runs_path):
        done.add(key_of((run["mnem"], run["shape"], run["key_width"]),
                        run["lang"]))
    pairs = []
    for asked in shared["driver"].ASKED:
        for lang in IR.LANGUAGES:
            pairs.append((asked, lang))
    say("pairs to run: %d; already recorded: %d" % (len(pairs),
                                                    len(done)))
    ran = 0
    index = 0
    started = time.time()
    for asked, lang in pairs:
        index = index + 1
        if key_of(asked, lang) in done:
            continue
        say("[%d/%d] %s %s %s -> %s"
            % (index, len(pairs), asked[0], asked[1], asked[2], lang))
        record = one_run(shared, cells, asked, lang)
        append_run(runs_path, record)
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
    say("lines on %s: %d" % (runs_path, len(read_runs(runs_path))))
    say("peak resident: %d kB" % peak_kb())
    return 0


def one_line(record):
    if record.get("refusal_cause") is not None:
        return "REFUSED: %s" % ("%s" % record["refusal_cause"])[:80]
    return ("%d points, %d agree, %d disagree, %d declined"
            % (record["sample_points"], record["agreements"],
               record["disagreements"], record["declined_points"]))


def sample_command():
    say(SAMPLE_RULE)
    say("")
    say("the point counts the rule gives, per arrival width:")
    say("")
    say("| arrivals | budget | an 8-bit list | a 32-bit list | a "
        "64-bit list |")
    say("|---|---|---|---|---|")
    for count in (1, 2, 3, 4):
        cut = budget(count)
        say("| %d | %d | %d | %d | %d |"
            % (count, cut, len(integer_points(8, cut)),
               len(integer_points(32, cut)),
               len(integer_points(64, cut))))
    say("")
    say("a 32-bit integer list in full, LITERAL: %s"
        % integer_points(32, budget(2)))
    say("")
    say("a 32-bit float list in full, as bit patterns, LITERAL: %s"
        % [hex(one) for one in float_points(32, budget(2))])
    return 0


def table_command(runs_path):
    """THE TABLE THE BRIEF ASKS FOR, one row per (cell, target)."""
    runs = read_runs(runs_path)
    say("| cell | target | route | rendered (GLOSS) | sample points | "
        "agreements / disagreements | the first disagreement LITERAL | "
        "JIT carve verdict |")
    say("|---|---|---|---|---|---|---|---|")
    for run in runs:
        cell = "`%s` %s %s" % (run["mnem"], run["shape"],
                               run["key_width"])
        if run.get("refusal_cause") is not None:
            say("| %s | %s | source | REFUSED: %s | -- | -- | -- | %s |"
                % (cell, run["lang"],
                   escaped("%s: %s" % (run["refusal_cause"],
                                       run.get("refusal_detail"))),
                   jit_note(run["lang"])))
            continue
        first = "--"
        if run.get("first_disagreement") is not None:
            first = escaped(json.dumps(run["first_disagreement"],
                                       sort_keys=True))
        gloss = escaped(run.get("gloss") or "")
        if len(gloss) > 90:
            gloss = gloss[:87] + "..."
        say("| %s | %s | source | `%s` | %d | %d / %d | %s | %s |"
            % (cell, run["lang"], gloss, run["sample_points"],
               run["agreements"], run["disagreements"], first,
               jit_note(run["lang"])))
    say("")
    totals = {}
    for run in runs:
        held = totals.setdefault(run["lang"],
                                 {"runs": 0, "rendered": 0,
                                  "agree": 0, "disagree": 0,
                                  "declined": 0, "points": 0,
                                  "whole_sample_agrees": 0})
        held["runs"] = held["runs"] + 1
        if run.get("refusal_cause") is not None:
            continue
        held["rendered"] = held["rendered"] + 1
        held["agree"] = held["agree"] + run["agreements"]
        held["disagree"] = held["disagree"] + run["disagreements"]
        held["declined"] = held["declined"] + run["declined_points"]
        held["points"] = held["points"] + run["sample_points"]
        if run["disagreements"] == 0 and run["agreements"] > 0:
            held["whole_sample_agrees"] = held["whole_sample_agrees"] + 1
    say("| target | runs | rendered | cells whose whole sample agrees | "
        "points | agreements | disagreements | declines |")
    say("|---|---|---|---|---|---|---|---|")
    for lang in IR.LANGUAGES:
        held = totals.get(lang)
        if held is None:
            continue
        say("| %s | %d | %d | %d | %d | %d | %d | %d |"
            % (lang, held["runs"], held["rendered"],
               held["whole_sample_agrees"], held["points"],
               held["agree"], held["disagree"], held["declined"]))
    say("")
    causes = {}
    for run in runs:
        if run.get("refusal_cause") is None:
            continue
        key = "%s" % run["refusal_cause"]
        causes.setdefault(key, {"runs": 0, "langs": set()})
        causes[key]["runs"] = causes[key]["runs"] + 1
        causes[key]["langs"].add(run["lang"])
    say("what did not run, by cause:")
    say("")
    say("| cause | runs | targets |")
    say("|---|---|---|")
    for key in sorted(causes, key=lambda one: -causes[one]["runs"]):
        say("| %s | %d | %s |"
            % (escaped(key), causes[key]["runs"],
               ", ".join(sorted(causes[key]["langs"]))))
    say("")
    declines = {}
    for run in runs:
        for key in (run.get("declines") or {}):
            declines[key] = declines.get(key, 0) + run["declines"][key]
    say("the declines, by cause, over every run (never scored, this "
        "line's own standing rule):")
    say("")
    say("| cause | points |")
    say("|---|---|")
    for key in sorted(declines, key=lambda one: -declines[one]):
        say("| %s | %d |" % (escaped(key), declines[key]))
    return 0


JIT_LANGUAGES = ("javascript", "dart", "csharp")


def jit_note(lang):
    if lang not in JIT_LANGUAGES:
        return "no JIT output in the corpus"
    return "see the JIT section"


def escaped(text):
    return ("%s" % text).replace("|", "/")


def aggregate_command(runs_path, aggregate_path):
    runs = read_runs(runs_path)
    document = {"meta": {"task": "ex1",
                         "what": "the interpreted handful: one run per "
                                 "(cell, target), the cell's mapping "
                                 "rendered as source and compared with "
                                 "the reference's own mapping over a "
                                 "stated sample",
                         "sample_rule": SAMPLE_RULE,
                         "runs": len(runs),
                         "targets": IR.LANGUAGES},
                "runs": runs}
    handle = open(aggregate_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    say("runs on %s: %d" % (runs_path, len(runs)))
    say("wrote %s" % aggregate_path)
    return 0


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    if argv[0] == "sample":
        return sample_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
