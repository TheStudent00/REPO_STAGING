#!/usr/bin/env python3
"""run_lemmas_t4.py -- ONE LEAN THEOREM PER OPERATION KIND, instantiated
at each (width, word) the two stores use.

Node: hq.research.compiler_graph.gate.lean (the proof system) and
hq.research.arch_unit_oracle.cross_construction.autopoly (the tier).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`,
section 1 -- "proved ONCE per kind, general in n and W, as a Lean lemma
in the form t2 used for its eight; where a lemma does not close in the
task's budget, the instantiation is proved by z3 at every width the
store uses, and the lemma is recorded in `OWED.md` with where it stops".

WHAT A THEOREM HERE SAYS, in one sentence: at this width and this word,
the term `build.py` constructs out of `& | ^ ~`, constant shifts, a
conditional and variables computes the same mapping as the operation it
replaces.

WHY IT IS INSTANTIATED AND NOT STATED ONCE FOR EVERY WIDTH, which is
task t2's finding and is unchanged: `bv_decide` -- Lean's bit-blasting
tactic, the one this project's proof system already uses -- decides a
goal at a FIXED width and cannot be handed a variable one.  The general
statement, one theorem per kind over `BitVec w` for every `w` with an
induction over the limb count, is STATED in `construct/lean/OWED.md`
and is not machine checked here.  What IS new here is that the
statement can be MADE at all for the constructions whose printed form
grows like 3^width: `lean_general.py` writes one `let` per node.

MEMORY: one `lean` process per theorem, its wall clock and peak read
from `os.wait4`; this process holds only the rows.  Bound 6 GB, named
abort ABORT_MEMORY_T4.

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

HOW THIS FILE OBEYS IT.  Which theorems are stated is
`kind_census.json`'s own list of (operation kind, width), and an
operation kind is `build.py`'s display label on a z3 DECLARATION KIND.

usage:
  run_lemmas_t4.py plan                 the theorems the census asks for
  run_lemmas_t4.py prove [<seconds>] [<part> <of>]
                                        the theorems generated and run
  run_lemmas_t4.py table                what `lemmas_t4.json` holds

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import check_constructions as CC                                 # noqa: E402
import lean_general as LG                                        # noqa: E402

OUT = os.path.join(HERE, "lemmas_t4.json")
LEAN_DIR = os.path.join(HERE, "lean_t4")
ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"
PER_THEOREM_SECONDS = 300

WRITTEN_OUT_CEILING = 200000
"""how large a term may be to be stated WRITTEN OUT.  It is task t2's
own ceiling (`run_lemmas_t2.STATEMENT_CEILING`) and for its own reason:
a printed term names no intermediate.  The `let` form has no such
ceiling, which is why it is tried first."""

FORMS = ["let", "written out"]
"""the two forms a theorem may be stated in, tried in this order.  The
row records which one the theorem was stated in, and a form that Lean
refuses to elaborate is recorded and the next is tried."""


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


def sanitised(text):
    out = []
    for letter in text:
        if letter.isalnum():
            out.append(letter)
            continue
        out.append("_")
        continue
    return "".join(out)


# ==================================================================
# section 1: the plan, off the census
# ==================================================================

def plan_rows():
    """one entry per (kind, width, word) the census names -- the same
    plan `check_constructions.py store` poses to z3, so the two tables
    are about the same instances."""
    return CC.store_plan()


def plan_command():
    plan = plan_rows()
    say("| operation kind | width | word | covers |")
    say("|---|---|---|---|")
    for entry in plan:
        say("| %s | %d | %d | %s |"
            % (entry["kind"], entry["width"], entry["word"],
               ", ".join("%d" % word for word in entry["covers"])))
        continue
    say("")
    say("instances the census names: %d" % len(plan))
    say("peak resident: %d kB" % check_memory("plan"))
    return 0


# ==================================================================
# section 2: one theorem
# ==================================================================

LEAN_MEMORY_MB = 4096
"""the address space ONE `lean` process may hold, under this task's own
6 GB bound.

MEASURED, lane `t4_l11` step [1/3]: `bv_decide` on the multiplier at 16
bits grew until the operating system stopped the whole lane with no
language-level error -- `Killed`, exit 137 -- and the eleven theorems
that had already closed were lost with it.  A bound on the child's
address space turns that into a `lean` process that fails to allocate
and returns, which is a row with its own output on it; nothing here
raises the task's bound and nothing is worked around."""


def bound_the_child():
    """the address-space bound, set in the child between the fork and
    the exec.  `resource.RLIMIT_AS` is inherited by `lean` and by every
    process it starts."""
    import resource as R
    limit = LEAN_MEMORY_MB * 1024 * 1024
    R.setrlimit(R.RLIMIT_AS, (limit, limit))
    return


def lean_command(path):
    """the `lean` invocation, with the address-space bound applied BY THE
    SHELL that starts it.

    WHY BOTH THIS AND `preexec_fn`, and it is measured rather than
    belt-and-braces: lane `t4_l12` set the bound through `preexec_fn`
    and the operating system still stopped the whole lane at the
    multiplier at 16 bits, so the bound either did not reach the process
    or did not reach what grew.  `ulimit -v` in the shell that `exec`s
    `lean` is the same rlimit set one layer out, and it is visible in
    the command the row records."""
    return ["/bin/sh", "-c",
            "ulimit -v %d; exec lean %s"
            % (LEAN_MEMORY_MB * 1024, os.path.basename(path))]


def run_lean(path, seconds):
    started = time.time()
    process = subprocess.Popen(lean_command(path),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, cwd=LEAN_DIR,
                               preexec_fn=bound_the_child)
    timed_out = False
    out = b""
    try:
        out, _ = process.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.terminate()
        try:
            out, _ = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.terminate()
            out, _ = process.communicate()
    wall = time.time() - started
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    return (process.returncode, out.decode("utf-8", "replace"), wall,
            peak, timed_out)


def one_theorem(kind, width, word, shape, node, bindings, seconds,
                covers):
    """one obligation of one kind at one (width, word), stated and run."""
    row = {"kind": kind, "width": width, "word": word, "shape": shape,
           "covers": covers,
           "theorem_name": "construction_%s_w%d_u%d__%s"
                           % (sanitised(kind), width, word,
                              sanitised(shape))}
    started = time.time()
    try:
        made = CC.constructed(node, word, bindings or {})
    except B.Refused as refusal:
        row["outcome"] = "REFUSED_BY_THE_CONSTRUCTION"
        row["cause"] = refusal.cause
        row["cause_detail"] = refusal.detail
        row["wall_seconds"] = round(time.time() - started, 3)
        return row
    except Exception as problem:                              # noqa: BLE001
        row["outcome"] = "REFUSED_BY_THE_CONSTRUCTION"
        row["cause"] = "the construction raised"
        row["cause_detail"] = "%s: %s" % (type(problem).__name__,
                                          problem)
        row["wall_seconds"] = round(time.time() - started, 3)
        return row
    built = B.joined(made)
    row["nodes"] = B.node_count(built, WRITTEN_OUT_CEILING)
    # THE SIZE THAT DECIDES IS THE UNFOLDED ONE, not the distinct-node
    # one, and the difference is the whole reason this file exists.  The
    # multiplier at 16 bits is 190 DISTINCT nodes and its written-out
    # form is past every ceiling: lane `t4_l13` stopped there -- the
    # `lean` process was bounded and answered "the SAT solver timed
    # out", and it was THIS process that then grew, building the
    # written-out fallback's own text.
    row["unfolded_nodes"] = B.unfolded_size(built, WRITTEN_OUT_CEILING)
    row["unfolded_ceiling"] = WRITTEN_OUT_CEILING
    refusals = []
    for form in FORMS:
        if form == "written out" \
                and row["unfolded_nodes"] >= WRITTEN_OUT_CEILING:
            refusals.append({"form": form,
                             "refused": ["TOO_LARGE_TO_STATE",
                                         "at or above %d nodes WRITTEN "
                                         "OUT (%d distinct)"
                                         % (WRITTEN_OUT_CEILING,
                                            row["nodes"])]})
            continue
        try:
            text, bound = LG.theorem(row["theorem_name"], node, built,
                                     form)
        except LG.Refused as refusal:
            refusals.append({"form": form,
                             "refused": [refusal.cause,
                                         refusal.detail]})
            continue
        except Exception as problem:                          # noqa: BLE001
            refusals.append({"form": form,
                             "refused": ["THE_PRINTER_RAISED",
                                         "%s: %s"
                                         % (type(problem).__name__,
                                            problem)]})
            continue
        row["stated_in_the_form"] = form
        row["bindings"] = bound
        row["statement_bytes"] = len(text)
        if not os.path.isdir(LEAN_DIR):
            os.makedirs(LEAN_DIR)
        path = os.path.join(LEAN_DIR, "%s.lean" % row["theorem_name"])
        handle = open(path, "w")
        handle.write(text)
        handle.close()
        row["lean_file"] = os.path.basename(path)
        code, output, wall, peak, timed = run_lean(path, seconds)
        row["lean_exit"] = code
        row["wall_seconds"] = round(wall, 3)
        row["children_peak_rss_kb"] = peak
        row["lean_output"] = output.strip()[:1200]
        row["forms_refused"] = refusals
        if timed:
            row["outcome"] = "TIMED_OUT"
            row["timed_out_at_seconds"] = seconds
            return row
        if code == 0:
            row["outcome"] = "PROVED_BY_LEAN"
            return row
        row["outcome"] = "LEAN_REFUSED"
        if code is not None and code < 0:
            # THE OPERATING SYSTEM STOPPED THE `lean` PROCESS with no
            # language-level error, which is an ABORT and is named one.
            row["outcome"] = "LEAN_ABORTED"
            row["aborted_on_signal"] = -code
            row["memory_bound_mb"] = LEAN_MEMORY_MB
        refusals.append({"form": form,
                         "refused": ["LEAN_REFUSED",
                                     output.strip()[:200]]})
        continue
    row["forms_refused"] = refusals
    if row.get("outcome") is None:
        row["outcome"] = "REFUSED_BEFORE_LEAN"
        row["cause"] = refusals[0]["refused"][0] if refusals else "none"
        row["cause_detail"] = (refusals[0]["refused"][1]
                               if refusals else "")
        row["wall_seconds"] = round(time.time() - started, 3)
    return row


# ==================================================================
# section 3: the run
# ==================================================================

def prove_command(seconds, part, of):
    plan = plan_rows()
    mine = []
    for index, entry in enumerate(plan):
        if index % of == (part - 1):
            mine.append(entry)
        continue
    say("the census names %d instances; this part is %d of %d and "
        "carries %d" % (len(plan), part, of, len(mine)))
    say("the ceiling per theorem: %d s" % seconds)
    say("the toolchain: %s" % toolchain())
    say("")
    rows = []
    index = 0
    path = OUT
    if of > 1:
        path = os.path.join(HERE, "lemmas_t4_%d_of_%d.json" % (part, of))
    for entry in mine:
        posed = CC.obligations_of_kind(entry["kind"], entry["width"],
                                       entry["word"])
        if not posed:
            rows.append({"kind": entry["kind"], "width": entry["width"],
                         "word": entry["word"], "shape": "--",
                         "covers": entry["covers"],
                         "outcome": "NO_OBLIGATION_STATED",
                         "cause": "this task states no obligation of "
                                  "this kind at this width",
                         "wall_seconds": 0.0})
            continue
        for item in posed:
            bindings = None
            if len(item) == 4:
                kind, node, shape, bindings = item
            else:
                kind, node, shape = item
            index = index + 1
            say("[%d] %s at %d over %d: %s"
                % (index, kind, entry["width"], entry["word"], shape))
            row = one_theorem(kind, entry["width"], entry["word"],
                              shape, node, bindings, seconds,
                              entry["covers"])
            rows.append(row)
            say("    %s in %s s (form %s, %s bindings)"
                % (row["outcome"], row.get("wall_seconds"),
                   row.get("stated_in_the_form"), row.get("bindings")))
            # WRITTEN AFTER EVERY THEOREM.  Lane `t4_l11` lost eleven
            # closed theorems when the operating system stopped the
            # process at the twelfth, because the file was written once
            # at the end; it is written now as it goes.
            write_out(path, rows, seconds, part, of)
            check_memory(shape)
            continue
        continue
    collapsed = write_out(path, rows, seconds, part, of)
    report(rows, collapsed)
    say("")
    say("written: %s" % path)
    say("peak resident: %d kB" % peak_kb())
    return 0


TOOLCHAIN = None


def write_out(path, rows, seconds, part, of):
    global TOOLCHAIN
    if TOOLCHAIN is None:
        TOOLCHAIN = toolchain()
    collapsed = collapse(rows)
    document = {
        "meta": {
            "written_by": "construct/general/run_lemmas_t4.py prove",
            "per_theorem_seconds": seconds,
            "part": part, "of": of,
            "lean_memory_bound_mb": LEAN_MEMORY_MB,
            "what": "one Lean theorem per SHAPE of each operation kind "
                    "at each (width, word) the census names; a (kind, "
                    "width, word) row is PROVED_BY_LEAN only where "
                    "every shape of it is",
            "toolchain": TOOLCHAIN,
            "peak_kb": peak_kb(),
        },
        "theorems": rows,
        "rows": collapsed,
    }
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return collapsed


def collapse(rows):
    """one row per (kind, width, word), spread over the words the
    instance covers: PROVED_BY_LEAN only where EVERY shape of it
    proved."""
    held = {}
    for row in rows:
        for word in (row.get("covers") or [row["word"]]):
            key = (row["kind"], row["width"], word)
            entry = held.get(key)
            if entry is None:
                entry = {"kind": row["kind"], "width": row["width"],
                         "word": word, "shapes": [],
                         "outcome": "PROVED_BY_LEAN",
                         "theorem_name": row.get("theorem_name"),
                         "seconds": 0.0}
                held[key] = entry
            entry["shapes"].append({"shape": row.get("shape"),
                                    "outcome": row["outcome"],
                                    "theorem": row.get("theorem_name")})
            entry["seconds"] = round(entry["seconds"]
                                     + (row.get("wall_seconds") or 0.0),
                                     3)
            if row["outcome"] != "PROVED_BY_LEAN":
                entry["outcome"] = row["outcome"]
            continue
        continue
    out = []
    for key in sorted(held, key=lambda one: (one[0], one[1], one[2])):
        out.append(held[key])
        continue
    return out


def toolchain():
    try:
        answer = subprocess.run(["lean", "--version"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=60)
        return answer.stdout.decode("utf-8", "replace").strip()
    except Exception as problem:                              # noqa: BLE001
        return "lean --version raised %s" % problem


def report(rows, collapsed):
    say("")
    say("| operation kind | width | word | shape | form | outcome | s |")
    say("|---|---|---|---|---|---|---|")
    for row in rows:
        say("| %s | %d | %d | %s | %s | %s | %s |"
            % (row["kind"], row["width"], row["word"],
               row.get("shape"), row.get("stated_in_the_form") or "--",
               row["outcome"], row.get("wall_seconds")))
        continue
    counts = {}
    for row in collapsed:
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
        continue
    say("")
    say("| the (kind, width, word) row's outcome | instances |")
    say("|---|---|")
    for outcome in sorted(counts):
        say("| %s | %d |" % (outcome, counts[outcome]))
        continue
    return


def table_command():
    if not os.path.exists(OUT):
        say("no table on disk at %s" % OUT)
        return 2
    handle = open(OUT)
    document = json.load(handle)
    handle.close()
    report(document["theorems"], document["rows"])
    return 0


def main(argv):
    what = argv[1] if len(argv) > 1 else "plan"
    if what == "plan":
        return plan_command()
    if what == "prove":
        seconds = PER_THEOREM_SECONDS
        if len(argv) > 2:
            seconds = int(argv[2])
        part = 1
        of = 1
        if len(argv) > 4:
            part = int(argv[3])
            of = int(argv[4])
        return prove_command(seconds, part, of)
    if what == "table":
        return table_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
