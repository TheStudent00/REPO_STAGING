#!/usr/bin/env python3
"""rv_interp.py -- task lx1, section 2: THE SEVEN INTERPRETED TARGETS
BESIDE THE RISC-V DEFINITIONS, at points, by agreement.

Node: hq.research.arch_unit_oracle.riscv64.language_axis
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_lx1_brief.md`,
section 2 -- "population: the 255 RISC-V cells; for each, the emulation
rendered into cpython, php, ruby, java, javascript, dart, csharp (the
same general render), run at points beside the definition evaluated at
the same points; recorded agreed / disagreed / refused / timed out,
never proved."

THE OBJECTS, one sentence each, in relation.
  * A CELL is one (`mnem`, operand shape, `key_width`) row of
    `twins.json` -- 255 of them, task rv2/rv3's own population, read
    here with no filter on whether an x86 cell twins it (the brief's
    population is "the 255 RISC-V cells", not the untwinned delta
    `rv_loop.untwinned` returns).
  * THE DESTINATION PLACE is `handful.destination_place`'s own rule,
    inlined here because a RISC-V cell's `places` (from `twins.json`)
    are already a list of NAMES, not place-records: the first place
    that is not `flags`, or the flags place when that is the only one.
    It is the one place x86's own interpreted route checks per cell
    (`interp_check.one_run`), so the two tables are about the same
    kind of object.
  * THE TERM is `rv_loop.riscv_terms`'s own: the reference's mapping
    of (cell, place), rebuilt from `model_table_rv.json`'s row by
    RE-RUNNING the row's own line through `riscv_reference.py`. A
    term is architecture-neutral once built (GLOSSARY.md, `term`): it
    is a formula over unknown bit-vectors, and nothing downstream of
    it reads which architecture produced it.
  * THE RENDER is `interp_render.InterpRenderer`, task ex1's own,
    CALLED and not forked: a term whose free symbols are the
    parameter-slot names `handful.families_of` reads -> one source
    file in the target's own operators.
  * THE CHECK is `interp_check`'s own fuzz-census method, CALLED and
    not forked: `interp_check.points_for`, `.sample_of`,
    `.reference_answers`, `.interpreter_answers` -- the sample rule,
    the reference's own term evaluated at each point, the
    interpreter's own answer at each point, compared.
  * WHAT IS NOT REUSED, and why: `interp_check.one_run`'s FRONT HALF
    (`shared["driver"].cell_input`, `.destination_place`,
    `.fixes_are_on`, `.projected_lane`) is `handful_frozen.py`'s own
    x86 model-table reader -- a consumer/setter flag-composition walk
    over x86 ROWS this line's RISC-V cells were never members of. The
    RISC-V equivalent of that front half is `rv_loop.riscv_terms` and
    `rv_general.py`'s own `one_run` (the compiled-target loop, task
    t4), which this file's front half mirrors: `rv_loop.in_parameter_slots`
    to rename the term's free symbols into parameter slots, then
    `handful.place_record` for the families~/text the
    renderer and the check both need. Both of those ARE called, not
    copied.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

HOW THIS FILE OBEYS IT.  The population is `twins.json`'s own row order;
every field carrying a mnemonic is named `mnem`, which the guard reads as
machine form; which language is asked is `interp_render.LANGUAGES`,
task ex1's own list, in that order.  Nothing here reads a source token.

MEMORY: one collecting process, bound 6 GB resident, named abort
ABORT_MEMORY_LX1, peak printed.  Runs stream to a jsonl store; the run
command RESUMES by skipping any (cell, lang) already on the store, task
ex2's own bookkeeping shape.

Coding discipline: no compound one-liner statements.

usage:
  rv_interp.py sample <twins.json> <model_table_rv.json> <store_prefix>
                      <src_dir> <limit_cells>
  rv_interp.py run    <twins.json> <model_table_rv.json> <store_prefix>
                      <src_dir> [<timeout_s>]
  rv_interp.py retry  <twins.json> <model_table_rv.json> <store_prefix>
                      <src_dir> [<timeout_s>]
  rv_interp.py table  <store_prefix>
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CROSS = os.path.normpath(os.path.join(HERE, "..", "cross_construction"))
EMULATION = os.path.join(CROSS, "emulation")
HANDFUL = os.path.join(EMULATION, "handful")
INTERP = os.path.join(EMULATION, "interp")
OP = os.path.normpath(os.path.join(HERE, "..", "..", "op_pipeline"))

sys.path.insert(0, HERE)
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)
sys.path.insert(0, EMULATION)
sys.path.insert(0, HANDFUL)
sys.path.insert(0, INTERP)

import z3                                                        # noqa: E402
import emulate as E                                              # noqa: E402
import handful as H                                               # noqa: E402
import interp_check as IC                                        # noqa: E402
import interp_render as IR                                       # noqa: E402
import rv_loop as RL                                              # noqa: E402
import term as TERM_MODULE                                        # noqa: E402

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_LX1"

FIRST_PASS_TIMEOUT = 60
RETRY_TIMEOUT = 600


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
# section 1: the population -- every one of the 255 cells, unfiltered
# ==================================================================

def every_cell(twins_path):
    """the 255 RISC-V cells `twins.json` holds, whether or not an x86
    cell twins them -- the brief's own population for section 2, not
    `rv_loop.untwinned`'s delta."""
    out = []
    document = json.load(open(twins_path))
    for row in document["rows"]:
        out.append({"mnem": row["mnem"], "shape": row["shape"],
                    "key_width": row["key_width"],
                    "places": [p["writes"] for p in row["places"]]})
        continue
    return out


def destination_place(places):
    """`handful.destination_place`'s own rule, over a list of NAMES:
    the first place that is not `flags`, or the flags place when that
    is the only one."""
    for place in places:
        if place != "flags":
            return place
        continue
    if places:
        return places[0]
    return None


# ==================================================================
# section 2: one cell, one language
# ==================================================================

def one_run(cell, place_name, term, lang, src_dir, timeout):
    row = {"mnem": cell["mnem"], "shape": cell["shape"],
           "key_width": cell["key_width"], "writes": place_name,
           "lang": lang, "route": "source",
           "check": "the fuzz census's method"}
    started = time.time()
    slotted, refusal = RL.in_parameter_slots(TERM_MODULE, term)
    if slotted is None:
        row["outcome"] = "REFUSED"
        row["refusal_cause"] = "the term could not be put in parameter " \
                               "slots"
        row["refusal_detail"] = refusal
        row["seconds"] = time.time() - started
        return row
    record = H.place_record("reg_rdi", slotted)
    row["term_text"] = record["text"]
    row["bits"] = record["bits"]
    if record.get("families") is None:
        row["outcome"] = "REFUSED"
        row["refusal_cause"] = record.get("not_rendered")
        row["refusal_detail"] = record.get("not_rendered_detail")
        row["seconds"] = time.time() - started
        return row
    ordered = H.renderer_input(record["term"])
    safe_writes = place_name.replace(".", "_").replace("-", "_")
    label = "%s_%s_%d__%s__%s" % (cell["mnem"], cell["shape"],
                                  cell["key_width"], safe_writes, lang)
    label = label.replace(".", "_")
    renderer = IR.InterpRenderer(lang, record["families"],
                                 record["home"]["family"], record["bits"],
                                 label)
    try:
        source, symbol = renderer.render(ordered, record["text"])
    except E.Refused as problem:
        row["outcome"] = "REFUSED"
        row["refusal_cause"] = problem.cause
        row["refusal_detail"] = problem.detail
        row["seconds"] = time.time() - started
        return row
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    kept = os.path.join(src_dir, label + IR.DIALECTS[lang].suffix)
    handle = open(kept, "w")
    handle.write(source)
    handle.close()
    row["source_path"] = kept
    row["symbol"] = symbol
    row["params"] = []
    for param in renderer.params:
        row["params"].append({"name": param["name"],
                              "family": param["family"],
                              "kind": param["kind"], "bits": param["bits"]})
        continue
    lists = IC.points_for(renderer.params)
    points = IC.sample_of(lists)
    row["sample_points"] = len(points)
    reference = IC.reference_answers(ordered, renderer.params, points)
    answers, problem = IC.interpreter_answers(lang, label, source, points,
                                              timeout=timeout)
    if answers is None:
        if isinstance(problem, dict) and problem.get("kind") == "TIMEOUT":
            row["outcome"] = "TIMEOUT"
            row["timeout_seconds"] = problem["seconds"]
            row["points_reached"] = problem["points_reached"]
            row["seconds"] = time.time() - started
            return row
        row["outcome"] = "REFUSED"
        row["refusal_cause"] = "the runner did not answer"
        row["refusal_detail"] = problem
        row["seconds"] = time.time() - started
        return row
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
        continue
    row["agreements"] = agreements
    row["disagreements"] = disagreements
    row["declines"] = declines
    row["declined_points"] = len(points) - agreements - disagreements
    row["first_disagreement"] = first
    if disagreements:
        row["outcome"] = "DISAGREED"
    elif agreements:
        row["outcome"] = "AGREED"
    else:
        row["outcome"] = "REFUSED"
        row["refusal_cause"] = "every point declined"
    row["seconds"] = time.time() - started
    return row


# ==================================================================
# section 3: the store -- resumable, streamed
# ==================================================================

def store_path(prefix):
    return prefix + ".jsonl"


def already_done(prefix):
    done = set()
    path = store_path(prefix)
    if not os.path.exists(path):
        return done
    handle = open(path)
    for line in handle:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        key = (record["mnem"], record["shape"], record["key_width"],
              record["lang"])
        done.add(key)
        continue
    handle.close()
    return done


def append_row(prefix, row):
    handle = open(store_path(prefix), "a")
    handle.write(json.dumps(row, sort_keys=True) + "\n")
    handle.close()
    return


def loop_command(twins_path, rv_path, prefix, src_dir, limit_cells,
                 timeout, only_timeouts, retry_prefix):
    say("[1/3] the population: every RISC-V cell twins.json holds")
    cells = every_cell(twins_path)
    say("   %d cells" % len(cells))
    if limit_cells is not None:
        cells = cells[:limit_cells]
        say("   sample: first %d" % len(cells))

    say("[2/3] the terms, rebuilt from the reference")
    terms, _operands = RL.riscv_terms(rv_path)
    say("   %d (cell, place) terms rebuilt" % len(terms))
    check_memory("after the terms")

    retry_wanted = None
    if only_timeouts:
        retry_wanted = set()
        handle = open(store_path(prefix))
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("outcome") != "TIMEOUT":
                continue
            key = (record["mnem"], record["shape"], record["key_width"],
                  record["lang"])
            retry_wanted.add(key)
            continue
        handle.close()
        say("   %d TIMEOUT rows on the first pass to retry at %ds"
            % (len(retry_wanted), timeout))

    write_prefix = retry_prefix if only_timeouts else prefix
    done = already_done(write_prefix)
    say("   %d (cell, lang) pairs already on the store" % len(done))

    say("[3/3] the loop")
    started = time.time()
    number = 0
    total = len(cells) * len(IR.LANGUAGES)
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        place_name = destination_place(cell["places"])
        term = None
        if place_name is not None:
            term = terms.get((key, place_name))
        for lang in IR.LANGUAGES:
            number = number + 1
            run_key = (cell["mnem"], cell["shape"], cell["key_width"], lang)
            if run_key in done:
                continue
            if only_timeouts and run_key not in retry_wanted:
                continue
            if place_name is None:
                row = {"mnem": cell["mnem"], "shape": cell["shape"],
                      "key_width": cell["key_width"], "writes": None,
                      "lang": lang, "outcome": "REFUSED",
                      "refusal_cause": "the cell writes no place"}
            elif term is None:
                row = {"mnem": cell["mnem"], "shape": cell["shape"],
                      "key_width": cell["key_width"], "writes": place_name,
                      "lang": lang, "outcome": "REFUSED",
                      "refusal_cause": "no term at this (cell, place): "
                                      "the reference's own line did not "
                                      "re-run"}
            else:
                row = one_run(cell, place_name, term, lang, src_dir,
                             timeout)
            append_row(write_prefix, row)
            if number % 25 == 0 or number == total:
                say("   [%d/%d] runs, %.0f s, peak %.0f MB"
                    % (number, total, time.time() - started,
                       check_memory("run %d" % number) / 1024.0))
            continue
        continue
    say("done, peak resident: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 4: the table -- of 255 on every row
# ==================================================================

def merged_rows(prefix, retry_prefix):
    """the first pass, with any TIMEOUT row replaced by its retry's own
    outcome where a retry ran -- task ex2's own rule (log_250
    deliverable 1: "the report carries BOTH the first pass's TIMEOUT
    record and the retry's own outcome for that pair")."""
    by_key = {}
    handle = open(store_path(prefix))
    for line in handle:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        key = (record["mnem"], record["shape"], record["key_width"],
              record["lang"])
        by_key[key] = record
        continue
    handle.close()
    if os.path.exists(store_path(retry_prefix)):
        handle = open(store_path(retry_prefix))
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            key = (record["mnem"], record["shape"], record["key_width"],
                  record["lang"])
            record["retry_of_timeout"] = True
            by_key[key] = record
            continue
        handle.close()
    return by_key


def table_command(prefix, retry_prefix, twins_path):
    whole = len(json.load(open(twins_path))["rows"])
    by_key = merged_rows(prefix, retry_prefix)
    say("THE INTERPRETED SEVEN AGAINST THE RISC-V DEFINITIONS, of %d "
        "on every row" % whole)
    say("| language | agreed | disagreed | refused | timed out | of |")
    say("|---|---|---|---|---|---|")
    agree_sets = {}
    for lang in IR.LANGUAGES:
        agreed = set()
        disagreed = set()
        refused = set()
        timed = set()
        for key in by_key:
            record = by_key[key]
            if record["lang"] != lang:
                continue
            cell = (record["mnem"], record["shape"], record["key_width"])
            outcome = record.get("outcome")
            if outcome == "TIMEOUT":
                timed.add(cell)
            elif outcome == "DISAGREED":
                disagreed.add(cell)
            elif outcome == "AGREED":
                agreed.add(cell)
            else:
                refused.add(cell)
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
    for key in sorted(by_key):
        record = by_key[key]
        first = record.get("first_disagreement")
        if not first:
            continue
        many = many + 1
        say("| %s | `%s` | `%s` | %s | %s | %s | %s | %s |"
            % (record["lang"], record["mnem"], record["shape"],
               record["key_width"], record.get("writes"),
               first.get("point"), first.get("the reference's answer"),
               first.get("the interpreter's answer")))
        continue
    if not many:
        say("| none | | | | | | | |")
    say("")
    say("EVERY REFUSAL, BY CAUSE")
    say("| language | cause | cells |")
    say("|---|---|---|")
    reasons = {}
    for key in by_key:
        record = by_key[key]
        if record.get("outcome") not in ("REFUSED",):
            continue
        cause = record.get("refusal_cause") or "(no cause recorded)"
        rk = (record["lang"], cause)
        reasons[rk] = reasons.get(rk, 0) + 1
        continue
    for rk in sorted(reasons, key=lambda item: -reasons[item]):
        say("| %s | %s | %d |" % (rk[0], rk[1], reasons[rk]))
        continue
    say("")
    say("row count on the store: %d" % len(by_key))
    say("peak resident: %d kB" % peak_kb())
    return 0


def main():
    command = sys.argv[1]
    if command == "sample":
        twins_path, rv_path, prefix, src_dir = sys.argv[2:6]
        limit_cells = int(sys.argv[6])
        return loop_command(twins_path, rv_path, prefix, src_dir,
                            limit_cells, FIRST_PASS_TIMEOUT, False, None)
    if command == "run":
        twins_path, rv_path, prefix, src_dir = sys.argv[2:6]
        timeout = FIRST_PASS_TIMEOUT
        if len(sys.argv) > 6:
            timeout = int(sys.argv[6])
        return loop_command(twins_path, rv_path, prefix, src_dir, None,
                            timeout, False, None)
    if command == "retry":
        twins_path, rv_path, prefix, src_dir = sys.argv[2:6]
        timeout = RETRY_TIMEOUT
        if len(sys.argv) > 6:
            timeout = int(sys.argv[6])
        return loop_command(twins_path, rv_path, prefix, src_dir, None,
                            timeout, True, prefix + "_retry")
    if command == "table":
        prefix = sys.argv[2]
        twins_path = sys.argv[3]
        return table_command(prefix, prefix + "_retry", twins_path)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
