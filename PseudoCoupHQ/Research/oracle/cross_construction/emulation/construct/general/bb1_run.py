#!/usr/bin/env python3
"""bb1_run.py -- THE BIT-BLAST ROUTE OVER EVERY RISC-V CELL: rv6's driver
with ONE thing swapped, the render.

Node: hq.research.arch_unit_oracle.cross_construction.riscv.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_bb1_brief.md`.

WHAT THIS FILE IS, one sentence, in relation: `rv6_all_langs.py` with
`rv_general.one_attempt` replaced by one that asks `bitblast.blast` for
the circuit and `bitblast.render_gates` for the source -- so the
population, the compile routes, the carve, the walk, the gate, the
census and the store are `rv_general`'s own and are CALLED, not copied.

WHAT IS THE SAME AS rv6, and this is what lets the two counts stand side
by side: the population is every row of `twins.json` (255 RISC-V cells),
the compile routes are rv3's (`inherit_rv3.install()`: c and cpp with
`--gcc-toolchain=/usr`, rust on the linux-gnu target, go unchanged), the
targets are c, cpp, go and rust, the gate's solver budget is 3,000 ms
and the gate is offered 4,000 carved instructions and no more.  swift
has no riscv64 SDK in the image and is a flag, not a row.

WHAT IS DIFFERENT: there is ONE route rather than two, so `POLICIES` is
the single name `bit_blast`; the source is a circuit of gates and not a
term printed in the language's own operators; and the store carries, per
attempt, the gate count, the source line count, the compile seconds, the
carved body's instruction count AND ITS TEXT, and the check's outcome
and seconds -- every one of them the brief's own section 4.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB1.  One process,
no pool, no clock in the driver.

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

HOW THIS FILE OBEYS IT.  The population is the twins file's own list of
cells, each a (`mnem`, operand shape, `key_width`) triple; every row of
every table below is keyed on that triple and on the target, and the
mnemonic rides in the field `mnem`, which is machine form.  Nothing here
reads a source token.

usage:
  bb1_run.py run   <ref_dir> <op_dir> <emulation_dir> <twins.json>
                   <model_table_rv.json> <prefix> <src_dir>
                   <work_root> [<limit>]
  bb1_run.py sizes <ref_dir> <op_dir> <emulation_dir> <twins.json>
                   <model_table_rv.json> <prefix>
  bb1_run.py table <bb1 prefix> <rv6 prefix> <twins.json>

`BB1_SIZES=<prefix>_sizes.json` in the environment orders the population
by circuit size, largest first, so the driver's own `limit` samples the
expensive end.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rv_general as RG                                          # noqa: E402
import bitblast as BB                                            # noqa: E402

def the_riscv_folder():
    """where `rv_loop` and `inherit_rv3` live: the folder of the
    `twins.json` this run was handed, and where a report command was
    handed none, the folder this file's own tree puts it in."""
    for argument in sys.argv[2:]:
        if argument.endswith("twins.json"):
            return os.path.dirname(os.path.abspath(argument))
        continue
    return os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                         "riscv"))


RV_DIR = the_riscv_folder()
sys.path.insert(0, RV_DIR)
import rv_loop as RL                                             # noqa: E402
import inherit_rv3 as INH3                                       # noqa: E402


SOURCE_KEPT_LINES = 2000
"""how long a rendered source may be and still be written into the
task's `src` folder beside the store.  The reason is measured and is not
a preference: a blasted divide is about fourteen thousand gates, so its
source is about fourteen thousand lines, and 1,020 attempts of that size
would put hundreds of megabytes of generated source into the repository.
The CARVED BODY is what the owner asked for and it is in the store for every
attempt, at every size, with no bound at all."""

BODY_TEXT_CEILING = 20000
"""how many instructions of a carved body are kept AS TEXT in the store.

THE COUNT IS ALWAYS EXACT AND IS NEVER BOUNDED; this is a bound on the
TRANSCRIPT and on nothing else, and where it bites, the row's own body
list says so in a sentence of its own.

WHY IT IS HERE, measured in lane `bb1_l4_the_cost_at_the_largest_six.sh`:
the largest circuit of the population, `mulh gpr_gpr_gpr 64`, carves to
250,188 instructions on c, and 24 attempts at that end of the population
wrote a 53.9 MB store.  The whole run's over-ceiling tail is about 175 MB
and the store is a REPOSITORY file.

WHY THE NUMBER IS 20,000: it is five times the 4,000 instructions the
gate is offered, so every body that was gated, and every body that could
ever be gated, is kept whole with a margin of four times over.  A body
above it was NOT_GATED by definition and is the one thing in the store
nobody can read across languages anyway."""

WRITTEN = {"prefix": None, "count": 0}

THE_LAST_BLAST = {"key": None, "circuit": None, "refusal": None}
"""the circuit of the (cell, place) the driver is on, kept for the four
targets that follow it.  THE BLAST DOES NOT DEPEND ON THE LANGUAGE --
the gates are z3's, over the term's bits -- and the driver's own loop
runs the four targets of one place one after another, so one entry is
the whole saving and nothing accumulates."""


def write_rows(prefix, rows):
    """the store, APPENDED rather than rewritten.

    `rv_general.write_rows` opens the file for writing and writes every
    row it has, every ten runs.  That is right where a row is a few
    hundred bytes; this task's rows carry the carved body's TEXT, so the
    same loop would rewrite a store of hundreds of megabytes a hundred
    times over.  The file this writes is byte-identical to the file that
    would rewrite it -- the same rows, in the same order, one json per
    line."""
    if WRITTEN["prefix"] != prefix:
        handle = open(prefix + ".jsonl", "w")
        handle.close()
        WRITTEN["prefix"] = prefix
        WRITTEN["count"] = 0
    if WRITTEN["count"] >= len(rows):
        return
    handle = open(prefix + ".jsonl", "a")
    for row in rows[WRITTEN["count"]:]:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()
    WRITTEN["count"] = len(rows)
    return


def every_cell(twins_path):
    """the population: every row of `twins.json`, which is rv5's and
    rv6's own population and the 255 this task counts against.

    THE ORDER IS THE FILE'S OWN unless `BB1_SIZES` names a sizes file
    this task wrote, and then it is BY CIRCUIT SIZE, largest first.  The
    reason is the cost sample and nothing else: the driver's `limit`
    takes the first n attempts, and the first n rows of `twins.json` are
    the cheap end, so a sample of them says nothing about what the
    expensive end costs.  The ordering key is the number of GATES z3's
    own blast produced -- machine-form evidence, measured, and not a
    reading of any name."""
    out = []
    for row in json.load(open(twins_path))["rows"]:
        out.append({"mnem": row["mnem"], "shape": row["shape"],
                    "key_width": row["key_width"],
                    "places": [p["writes"] for p in row["places"]]})
        continue
    sizes_path = os.environ.get("BB1_SIZES")
    if not sizes_path:
        return out
    if not os.path.exists(sizes_path):
        return out
    largest = {}
    for row in json.load(open(sizes_path))["rows"]:
        key = (row["mnem"], row["shape"], row["key_width"])
        gates = row.get("gates")
        if gates is None:
            continue
        if gates > largest.get(key, -1):
            largest[key] = gates
        continue

    def size_of(cell):
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        return -largest.get(key, -1)

    out.sort(key=size_of)
    return out


# ==================================================================
# section 1a: the circuit size of every cell, before anything is
# compiled
# ==================================================================

def bring_in(ref_dir, op_dir, emulation_dir, twins_path):
    """the same path setup and the same imports `rv_general.run_command`
    makes, so a report command reads the same objects the run does."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(twins_path)))
    sys.path.insert(0, os.path.join(emulation_dir, "handful"))
    sys.path.insert(0, os.path.join(emulation_dir, "autopoly"))
    sys.path.insert(0, emulation_dir)
    sys.path.insert(0, os.path.join(emulation_dir, "rust"))
    sys.path.insert(0, os.path.join(emulation_dir, "go"))
    sys.path.insert(0, os.path.join(emulation_dir, "swift"))
    import twins as TW
    TW.bring_in(ref_dir, op_dir)
    import rv_loop as THE_LOOP
    import handful as H
    return THE_LOOP, H


def sizes_command(ref_dir, op_dir, emulation_dir, twins_path, rv_path,
                  prefix):
    """how many gates z3's blast gives every cell of the population,
    with nothing compiled and nothing gated.

    This is the cheap half of the task and it is run first, because it
    is what says where the expensive end is -- and the expensive end is
    then what the cost sample compiles."""
    THE_LOOP, H = bring_in(ref_dir, op_dir, emulation_dir, twins_path)
    import term as TERMS
    cells = every_cell(twins_path)
    terms, _operands = THE_LOOP.riscv_terms(rv_path)
    say("[1/2] blasting %d cells" % len(cells))
    rows = []
    started = time.time()
    number = 0
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        for place_name in cell["places"]:
            number = number + 1
            row = {"mnem": cell["mnem"], "shape": cell["shape"],
                   "key_width": cell["key_width"], "place": place_name}
            term = terms.get((key, place_name))
            if term is None:
                row["refusal"] = "the cell's own line could not be re-run"
                rows.append(row)
                continue
            slotted, refusal = THE_LOOP.in_parameter_slots(TERMS, term)
            if slotted is None:
                row["refusal"] = refusal
                rows.append(row)
                continue
            record = H.place_record("reg_rdi", slotted)
            if record.get("families") is None:
                row["refusal"] = record.get("not_rendered_detail") \
                    or record.get("not_rendered")
                rows.append(row)
                continue
            row["bits"] = record["bits"]
            ordered = H.renderer_input(record["term"])
            try:
                circuit = BB.blast(ordered)
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
            if number % 25 == 0:
                say("   [%d/%d] blasted, %.0f s"
                    % (number, len(cells), time.time() - started))
            continue
        continue
    say("[2/2] writing %s_sizes.json" % prefix)
    document = {
        "meta": {
            "task": "bb1",
            "what": "how many gates z3's own bit-blast tactic gives "
                    "every RISC-V cell of twins.json, with nothing "
                    "compiled and nothing gated",
            "seconds": round(time.time() - started, 1),
            "cells": len(cells),
        },
        "rows": rows,
    }
    handle = open(prefix + "_sizes.json", "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    sizes_tables(rows)
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
        held = 0
        for value in gates:
            if value >= low and value < high:
                held = held + 1
            continue
        say("| %d to %d | %d |" % (low, high, held))
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
    say("THE PLACES THE BLAST REFUSED: %d" % len(refused))
    say("| mnem | shape | width | place | cause, LITERAL |")
    say("|---|---|---|---|---|")
    for row in refused:
        say("| `%s` | `%s` | %s | %s | %s |"
            % (row["mnem"], row["shape"], row["key_width"],
               row["place"],
               " ".join((row.get("refusal") or "").split())[:160]))
        continue
    say("")
    return


# ==================================================================
# section 1: one place, one target, by the bit-blast route
# ==================================================================

def one_attempt(H, RL_, INH, reference, cell, place_name, term, target,
                record, word, policy, work_root, number):
    """`rv_general.one_attempt` with the render swapped and the brief's
    own fields stored.  Everything after the source -- the compile, the
    carve, the walk, the two widths, the solver budget and the
    instruction ceiling -- is `rv_general`'s own and is called."""
    label = "%s_%s_%d__%s__%s__%s" % (cell["mnem"], cell["shape"],
                                      cell["key_width"], place_name,
                                      target, policy)
    label = label.replace(".", "_")
    out = {"policy": policy, "label": label}
    ordered = H.renderer_input(record["term"])

    circuit, refusal = the_circuit(cell, place_name, ordered)
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

    try:
        made = BB.render_gates(circuit, target, record["families"],
                               record["home"]["family"], record["bits"],
                               label, record.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        out["rendered"] = False
        out["refusal_cause"] = "the gate render refused"
        out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                            ("%s" % problem)[:300])
        return out
    out["rendered"] = True
    out["statements"] = made["statements"]
    out["source_lines"] = made["source_lines"]
    keep_source(H, label, target, made["source"])

    work = os.path.join(work_root, "bb%06d_%s" % (number, target))
    started = time.time()
    got, command, diagnostic = INH.compile_and_carve(made["source"],
                                                     target, work)
    out["compile_seconds"] = round(time.time() - started, 3)
    out["compiler"] = {"command": command,
                       "target_triple": INH.triple_of(target)}
    if got is None:
        out["compiled"] = False
        out["verdict"] = {"outcome": "BUILD_REFUSED",
                          "reason": (diagnostic or "").strip()[:600]}
        return out
    out["compiled"] = True
    raw, body = got
    out["instructions"] = len(body)
    out["body"] = the_body_text(body)
    out["gate_instruction_ceiling"] = RG.GATE_INSTRUCTION_CEILING
    if len(body) > RG.GATE_INSTRUCTION_CEILING:
        out["verdict"] = {"outcome": "NOT_GATED",
                          "reason": RG.CAUSE_GATE_TOO_LARGE,
                          "instructions": len(body)}
        return out

    contract = RL_.slot_contract(term)
    started = time.time()
    try:
        state = reference.simulate(body, contract, {})
        answer = reference.answer_of(state, "a0")
    except Exception as problem:                              # noqa: BLE001
        out["check_seconds"] = round(time.time() - started, 3)
        out["verdict"] = {"outcome": "WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                ("%s" % problem)[:300])}
        return out
    width = cell["key_width"] or term.size()
    if width > term.size():
        width = term.size()
    outcome, counterexample = INH.decide(INH.at_width(answer, width),
                                         INH.at_width(term, width),
                                         RG.SOLVER_MS)
    whole = term.size()
    outcome_whole, counter_whole = INH.decide(
        INH.at_width(answer, whole), INH.at_width(term, whole),
        RG.SOLVER_MS)
    out["check_seconds"] = round(time.time() - started, 3)
    out["verdict"] = {"outcome": outcome, "compared_on_bits": width,
                      "counterexample": counterexample,
                      "solver_timeout_ms": RG.SOLVER_MS}
    out["verdict_at_the_whole_place"] = {"outcome": outcome_whole,
                                         "compared_on_bits": whole,
                                         "counterexample": counter_whole}
    return out


def the_body_text(body):
    """the carved body as the store keeps it: the whole text under this
    file's stated ceiling, and above it the first and last two hundred
    instructions with ONE LINE BETWEEN THEM saying, in the list itself,
    exactly what is not there and how to get it.  The row's shape does
    not change and the row's `instructions` count is the whole body's."""
    if len(body) <= BODY_TEXT_CEILING:
        return list(body)
    elided = len(body) - 400
    middle = ("... %d instructions of this body are not kept as text: "
              "the store's own ceiling is %d instructions and this body "
              "is %d, which is above the %d the gate is offered and so "
              "was never posed.  Re-derive the whole body by running "
              "bb1_run.py over this one cell."
              % (elided, BODY_TEXT_CEILING, len(body),
                 RG.GATE_INSTRUCTION_CEILING))
    return list(body[:200]) + [middle] + list(body[-200:])


def the_circuit(cell, place_name, ordered):
    """(the circuit, the refusal text) for one place, blasted once and
    kept for the four targets that follow."""
    key = (cell["mnem"], cell["shape"], cell["key_width"], place_name)
    if THE_LAST_BLAST["key"] == key:
        return THE_LAST_BLAST["circuit"], THE_LAST_BLAST["refusal"]
    circuit = None
    refusal = None
    try:
        circuit = BB.blast(ordered)
    except Exception as problem:                              # noqa: BLE001
        refusal = "%s: %s" % (type(problem).__name__,
                              ("%s" % problem)[:300])
    THE_LAST_BLAST["key"] = key
    THE_LAST_BLAST["circuit"] = circuit
    THE_LAST_BLAST["refusal"] = refusal
    return circuit, refusal


def keep_source(H, label, target, source):
    """the rendered source written beside the store, under the line
    bound this file states."""
    folder = getattr(H, "SRC_DIR", None)
    if not folder:
        return
    if source.count("\n") + 1 > SOURCE_KEPT_LINES:
        return
    if not os.path.isdir(folder):
        os.makedirs(folder)
    suffix = {"c": ".c", "cpp": ".cpp", "go": ".go", "rust": ".rs"}
    handle = open(os.path.join(folder,
                               label + suffix.get(target, ".txt")), "w")
    handle.write(source)
    handle.close()
    return


# ==================================================================
# section 2: the three routes in one table
# ==================================================================

LANGUAGE_NAME = {"c": "c", "cpp": "c++", "go": "go", "rust": "rust"}
ORDER = ["c", "cpp", "rust", "go"]


def say(line):
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


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


def key_of(row):
    cell = row["cell"]
    return (cell["mnem"], cell["shape"], cell["key_width"])


def by_route(rows, policy):
    """(target, cell key) -> the kind of that target's attempt under one
    policy, by `rv_general.kind_of_attempt` and by nothing else."""
    out = {}
    for row in rows:
        for attempt in row.get("attempts") or []:
            if attempt.get("policy") != policy:
                continue
            out[(row["target"], key_of(row))] = \
                RG.kind_of_attempt(attempt)
            continue
        continue
    return out


def tally(held, target, whole):
    counts = {"proved": 0, "sat": 0, "undecided": 0, "refused": 0}
    for (this_target, _key) in held:
        if this_target != target:
            continue
        counts[held[(this_target, _key)]] += 1
        continue
    counts["refused"] += whole - sum(counts.values())
    return counts


def proved_cells(held, target):
    out = set()
    for (this_target, key) in held:
        if this_target != target:
            continue
        if held[(this_target, key)] == "proved":
            out.add(key)
        continue
    return out


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


def table_command(bb_prefix, rv6_prefix, twins_path):
    whole = len(json.load(open(twins_path))["rows"])
    rv6 = read_rows(rv6_prefix + ".jsonl")
    mine = read_rows(bb_prefix + ".jsonl")
    native = by_route(rv6, "native_first")
    backstop = by_route(rv6, "all_constructed")
    blasted = by_route(mine, "bit_blast")

    say("")
    say("THE THREE ROUTES, PROVED, of %d on every row" % whole)
    say("| language | native route (rv6) | backstop (rv6) | "
        "bit-blast (bb1) | any of the three | of |")
    say("|---|---|---|---|---|---|")
    union_native = set()
    union_backstop = set()
    union_blast = set()
    for target in ORDER:
        one = proved_cells(native, target)
        two = proved_cells(backstop, target)
        three = proved_cells(blasted, target)
        union_native |= one
        union_backstop |= two
        union_blast |= three
        say("| %s | %d | %d | %d | %d | %d |"
            % (LANGUAGE_NAME[target], len(one), len(two), len(three),
               len(one | two | three), whole))
        continue
    say("| **proved on at least one language** | **%d** | **%d** | "
        "**%d** | **%d** | **%d** |"
        % (len(union_native), len(union_backstop), len(union_blast),
           len(union_native | union_backstop | union_blast), whole))
    say("")

    say("THE BIT-BLAST ROUTE'S OWN OUTCOMES, of %d on every row" % whole)
    say("| language | proved | disproved | undecided | refused | of |")
    say("|---|---|---|---|---|---|")
    for target in ORDER:
        counts = tally(blasted, target, whole)
        say("| %s | %d | %d | %d | %d | %d |"
            % (LANGUAGE_NAME[target], counts["proved"], counts["sat"],
               counts["undecided"], counts["refused"], whole))
        continue
    say("")

    say("WHAT THE BIT-BLAST ROUTE ADDS OVER THE OTHER TWO")
    say("| cells only the bit-blast route proves | mnem | shape | width |")
    say("|---|---|---|---|")
    gained = union_blast - (union_native | union_backstop)
    for key in sorted(gained):
        say("|  | `%s` | `%s` | %s |" % (key[0], key[1], key[2]))
        continue
    if not gained:
        say("|  none | | | |")
    say("")

    distributions(mine)
    causes(mine)
    return 0


def rows_command(prefix, bodies):
    """one line per ATTEMPT of a store: what the brief asks be stored,
    printed in the order the driver ran it."""
    rows = read_rows(prefix + ".jsonl")
    say("| mnem | shape | width | language | gates | source lines | "
        "compile s | body instructions | outcome | check s |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        key = key_of(row)
        for attempt in row.get("attempts") or []:
            verdict = attempt.get("verdict") or {}
            outcome = verdict.get("outcome")
            if outcome is None:
                outcome = attempt.get("refusal_cause") or "no verdict"
            say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s |"
                % (key[0], key[1], key[2],
                   LANGUAGE_NAME.get(row["target"], row["target"]),
                   attempt.get("gates"), attempt.get("source_lines"),
                   attempt.get("compile_seconds"),
                   attempt.get("instructions"), outcome,
                   attempt.get("check_seconds")))
            continue
        continue
    say("")
    say("EVERY REFUSAL AND EVERY COUNTEREXAMPLE, LITERAL")
    for row in rows:
        key = key_of(row)
        for attempt in row.get("attempts") or []:
            verdict = attempt.get("verdict") or {}
            detail = attempt.get("refusal_detail")
            if detail:
                say("  %s %s %s %s: %s"
                    % (key[0], key[1], key[2], row["target"],
                       " ".join(detail.split())[:400]))
            reason = verdict.get("reason")
            if reason:
                say("  %s %s %s %s %s: %s"
                    % (key[0], key[1], key[2], row["target"],
                       verdict.get("outcome"),
                       " ".join(reason.split())[:400]))
            counter = verdict.get("counterexample")
            if counter:
                say("  %s %s %s %s counterexample: %s"
                    % (key[0], key[1], key[2], row["target"],
                       " ".join(("%s" % counter).split())[:400]))
            continue
        continue
    say("")
    if not bodies:
        return 0
    say("THE CARVED BODIES, LITERAL, where the gate was offered them")
    for row in rows:
        key = key_of(row)
        for attempt in row.get("attempts") or []:
            body = attempt.get("body")
            if not body:
                continue
            if len(body) > int(bodies):
                say("  %s %s %s %s: %d instructions, not printed here "
                    "(the store carries all of them)"
                    % (key[0], key[1], key[2], row["target"], len(body)))
                continue
            say("  %s %s %s %s: %d instructions"
                % (key[0], key[1], key[2], row["target"], len(body)))
            for line in body:
                say("      %s" % line)
                continue
            continue
        continue
    return 0


def distributions(rows):
    gates = []
    blasts = []
    lines = []
    compiles = []
    instructions = []
    checks = []
    not_gated = []
    per_target = {}
    for row in rows:
        for attempt in row.get("attempts") or []:
            target = row["target"]
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
            if attempt.get("compile_seconds") is not None:
                compiles.append(attempt["compile_seconds"])
                held["compile"].append(attempt["compile_seconds"])
            if attempt.get("instructions") is not None:
                instructions.append(attempt["instructions"])
                held["instructions"].append(attempt["instructions"])
            if attempt.get("check_seconds") is not None:
                checks.append(attempt["check_seconds"])
                held["check"].append(attempt["check_seconds"])
            verdict = attempt.get("verdict") or {}
            if verdict.get("outcome") == "NOT_GATED":
                not_gated.append((row["target"], key_of(row),
                                  verdict.get("instructions")))
            continue
        continue
    say("THE SIZES AND THE SECONDS")
    say("| what | attempts | smallest | median | mean | largest |")
    say("|---|---|---|---|---|---|")
    for name, values in (("gates per definition", gates),
                         ("blast seconds", blasts),
                         ("source lines", lines),
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
    say("NOT GATED -- the carved body is above the %d instructions the "
        "gate is offered: %d attempts" % (RG.GATE_INSTRUCTION_CEILING,
                                          len(not_gated)))
    say("| language | mnem | shape | width | instructions |")
    say("|---|---|---|---|---|")
    for target, key, size in sorted(not_gated,
                                    key=lambda r: -(r[2] or 0)):
        say("| %s | `%s` | `%s` | %s | %s |"
            % (LANGUAGE_NAME.get(target, target), key[0], key[1],
               key[2], size))
        continue
    say("")
    return


def causes(rows):
    held = {}
    for row in rows:
        for attempt in row.get("attempts") or []:
            verdict = attempt.get("verdict") or {}
            outcome = verdict.get("outcome")
            if outcome is None and attempt.get("refusal_cause"):
                outcome = attempt["refusal_cause"]
            if outcome in (None, "PROVED"):
                continue
            detail = attempt.get("refusal_detail") or \
                verdict.get("reason") or ""
            key = (row["target"], outcome, " ".join(detail.split())[:140])
            held[key] = held.get(key, 0) + 1
            continue
        continue
    say("EVERY OUTCOME THAT IS NOT A PROOF, with its cause, LITERAL")
    say("| language | outcome | cause | attempts |")
    say("|---|---|---|---|")
    for key in sorted(held, key=lambda k: (-held[k], k)):
        say("| %s | %s | %s | %d |"
            % (LANGUAGE_NAME.get(key[0], key[0]), key[1], key[2],
               held[key]))
        continue
    say("")
    return


# ==================================================================
# section 3: the swap, and the run
# ==================================================================

THE_GENERAL_ONE_RUN = RG.one_run


def one_run(*arguments):
    """`rv_general.one_run` called, with the row's route named for what
    actually rendered it.  The field is `rv_general`'s own and that file
    is READ on this task, so the name is put on afterwards rather than
    by editing it."""
    row = THE_GENERAL_ONE_RUN(*arguments)
    row["route"] = "bit_blast"
    return row


RL.untwinned = every_cell
INH3.install()
RG.TARGETS = ["c", "cpp", "go", "rust"]
RG.POLICIES = ("bit_blast",)
RG.ABORT_NAME = "ABORT_MEMORY_BB1"
RG.one_attempt = one_attempt
RG.one_run = one_run
RG.write_rows = write_rows


def name_the_document(prefix):
    """the run's own `<prefix>.json`, with the task and the sentence it
    is about put on it.  `rv_general.run_command` writes task t4's, and
    that file is READ here."""
    path = prefix + ".json"
    if not os.path.exists(path):
        return
    handle = open(path)
    document = json.load(handle)
    handle.close()
    document["meta"]["task"] = "bb1"
    document["meta"]["what"] = (
        "every RISC-V cell of twins.json turned into an and-or-not-xor "
        "circuit by z3's own bit-blast tactic, that circuit written as "
        "one named local per gate in c, cpp, go and rust, compiled for "
        "riscv64 at the corpus's ship flags, carved, walked and gated")
    document["meta"]["route"] = "bit_blast"
    document["meta"]["memory_abort"] = "ABORT_MEMORY_BB1"
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


def main():
    command = sys.argv[1]
    if command == "table":
        return table_command(sys.argv[2], sys.argv[3], sys.argv[4])
    if command == "sizes":
        return sizes_command(sys.argv[2], sys.argv[3], sys.argv[4],
                             sys.argv[5], sys.argv[6], sys.argv[7])
    if command == "rows":
        bodies = 0
        if len(sys.argv) > 3:
            bodies = sys.argv[3]
        return rows_command(sys.argv[2], bodies)
    print("bb1: every RISC-V cell x %s, the bit-blast route, "
          "rv3's compile routes" % RG.TARGETS, flush=True)
    code = RG.main()
    name_the_document(sys.argv[7])
    return code


if __name__ == "__main__":
    sys.exit(main())
