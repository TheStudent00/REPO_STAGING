#!/usr/bin/env python3
"""rv_general.py -- THE GENERAL TIER ON THE SECOND ARCHITECTURE: every
RISC-V cell with no x86 twin, rendered again by `render_general` under
both policies, compiled for riscv64 at the corpus's ship flags, carved,
walked through the RISC-V reference and gated.

Node: hq.research.arch_unit_oracle.cross_construction.riscv and
hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`,
section 2 -- "on every cell that has no proved certificate for a target
(both architectures: x86-64 and riscv64)" and "the RISC-V count beside
rv3's 117 of 255".

THE OBJECTS, one sentence each, in relation.
  * THE POPULATION is `rv_loop.untwinned(twins.json)`: the RISC-V cells
    no x86 cell twins under either reading, which is the same population
    task rv2's loop ran over, so the count this file prints stands
    beside rv3's.
  * THE RENDER is `render_general.render`, unchanged and shared with the
    x86 leg -- one named intermediate per node, the language's own
    operator where it has one and the construction where it does not.
  * THE COMPILE AND THE CARVE are `inherit.compile_and_carve`, the
    riscv64 half of the pipeline, unchanged and called.
  * THE GATE is stated here rather than called, and the reason is
    measured and not a preference: `rv_loop.gate` prints the carved
    body's answer through `Term.normalize` before it decides, and a
    printed term names no intermediate -- the multiplier at 8 bits is
    190 distinct nodes and at or above 200,000 written out (lane
    `t4_l14` step [1/4]).  So the gate below asks `inherit.decide` the
    same two questions at the same two widths with the same solver
    budget, and does not print either side.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.

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
cells, each a (`mnem`, operand shape, `key_width`) triple; which route a
node takes is whether the target's own renderer raises.  Nothing here
reads a source token.

usage:
  rv_general.py run <ref_dir> <op_dir> <emulation_dir> <twins.json>
                    <model_table_rv.json> <prefix> <src_dir>
                    <work_root> [<limit>]
  rv_general.py count <prefix> <twins.json> <rv3 certificates.jsonl>
                    <rv2 rv_loop.jsonl>

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, CONSTRUCT)

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import render_general as RG                                      # noqa: E402

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"
SOLVER_MS = 3000
TARGETS = ["c", "go"]
POLICIES = ("native_first", "all_constructed")

GATE_INSTRUCTION_CEILING = 4000
"""how many carved instructions the gate is offered, the x86 leg's own
ceiling and for its own measured reason (`general.py`)."""

CAUSE_GATE_TOO_LARGE = ("the carved body is larger than the number of "
                        "instructions this task's gate is offered: the "
                        "walk builds one term per instruction and a "
                        "body of this size is not posed at all")


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
# section 1: one place, one target, one policy
# ==================================================================

def one_attempt(H, RL, INH, reference, cell, place_name, term, target,
                record, word, policy, work_root, number):
    label = "%s_%s_%d__%s__%s__%s" % (cell["mnem"], cell["shape"],
                                      cell["key_width"], place_name,
                                      target, policy)
    label = label.replace(".", "_")
    out = {"policy": policy, "label": label}
    ordered = H.renderer_input(record["term"])
    try:
        made = RG.render(ordered, target, record["families"],
                         record["home"]["family"], record["bits"],
                         label, word, policy, record.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        out["rendered"] = False
        out["refusal_cause"] = "the render refused"
        out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                            ("%s" % problem)[:300])
        return out
    out["rendered"] = True
    out["statements"] = made["statements"]
    out["native_nodes"] = made["native_nodes"]
    out["constructed_nodes"] = made["constructed_nodes"]
    out["constructed_kinds"] = made["constructed_kinds"]
    out["constructed_widths"] = made["constructed_widths"]
    out["source_lines"] = made["source"].count("\n") + 1
    work = os.path.join(work_root, "rv%06d_%s_%s"
                        % (number, target, policy))
    got, command, diagnostic = INH.compile_and_carve(made["source"],
                                                     target, work)
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
    out["gate_instruction_ceiling"] = GATE_INSTRUCTION_CEILING
    if len(body) > GATE_INSTRUCTION_CEILING:
        out["verdict"] = {"outcome": "NOT_GATED",
                          "reason": CAUSE_GATE_TOO_LARGE,
                          "instructions": len(body)}
        return out
    contract = RL.slot_contract(term)
    try:
        state = reference.simulate(body, contract, {})
        answer = reference.answer_of(state, "a0")
    except Exception as problem:                              # noqa: BLE001
        out["verdict"] = {"outcome": "WALK_REFUSED",
                          "reason": "%s: %s" % (type(problem).__name__,
                                                ("%s" % problem)[:300])}
        return out
    width = cell["key_width"] or term.size()
    if width > term.size():
        width = term.size()
    outcome, counterexample = INH.decide(INH.at_width(answer, width),
                                         INH.at_width(term, width),
                                         SOLVER_MS)
    whole = term.size()
    outcome_whole, counter_whole = INH.decide(
        INH.at_width(answer, whole), INH.at_width(term, whole),
        SOLVER_MS)
    out["verdict"] = {"outcome": outcome, "compared_on_bits": width,
                      "counterexample": counterexample,
                      "solver_timeout_ms": SOLVER_MS}
    out["verdict_at_the_whole_place"] = {"outcome": outcome_whole,
                                         "compared_on_bits": whole,
                                         "counterexample": counter_whole}
    return out


def kind_of_attempt(attempt):
    verdict = attempt.get("verdict") or {}
    if verdict.get("outcome") == "PROVED":
        return "proved"
    if verdict.get("outcome") == "DISPROVED":
        return "sat"
    if not attempt.get("rendered"):
        return "refused"
    if not attempt.get("compiled"):
        return "refused"
    if verdict.get("outcome") == "NOT_GATED":
        return "refused"
    return "undecided"


def one_run(H, RL, INH, CONS, reference, cell, place_name, term, target,
            work_root, number):
    row = {"arch": "riscv64", "cell": dict(cell), "place": place_name,
           "target": target, "route": "general"}
    slotted, refusal = RL.in_parameter_slots(sys.modules["term"], term)
    if slotted is None:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "NOT_RENDERED", "reason": refusal}
        return row
    record = H.place_record("reg_rdi", slotted)
    if record.get("families") is None:
        row["kind"] = "refused"
        row["verdict"] = {"outcome": "NOT_RENDERED",
                          "reason": record.get("not_rendered_detail")
                          or record.get("not_rendered")}
        return row
    word = CONS.word_of(target)
    attempts = []
    for policy in POLICIES:
        attempts.append(one_attempt(H, RL, INH, reference, cell,
                                    place_name, term, target, record,
                                    word, policy, work_root, number))
        continue
    row["attempts"] = attempts
    row["kind"] = "refused"
    for attempt in attempts:
        if kind_of_attempt(attempt) == "proved":
            row["kind"] = "proved"
            row["chosen_policy"] = attempt["policy"]
            row["verdict"] = attempt["verdict"]
            return row
        continue
    order = ["sat", "undecided", "refused"]
    best = None
    for attempt in attempts:
        kind = kind_of_attempt(attempt)
        if best is None or order.index(kind) < order.index(best[0]):
            best = (kind, attempt)
        continue
    if best is not None:
        row["kind"] = best[0]
        row["chosen_policy"] = best[1]["policy"]
        row["verdict"] = best[1].get("verdict")
    return row


# ==================================================================
# section 2: the run
# ==================================================================

def run_command(ref_dir, op_dir, emulation_dir, twins_path, rv_path,
                prefix, src_dir, work_root, limit):
    RV = os.path.dirname(os.path.abspath(twins_path))
    sys.path.insert(0, RV)
    sys.path.insert(0, os.path.join(emulation_dir, "handful"))
    sys.path.insert(0, os.path.join(emulation_dir, "autopoly"))
    sys.path.insert(0, emulation_dir)
    sys.path.insert(0, os.path.join(emulation_dir, "rust"))
    sys.path.insert(0, os.path.join(emulation_dir, "go"))
    sys.path.insert(0, os.path.join(emulation_dir, "swift"))
    import twins as TW
    say("[0/4] the x86 reference this run uses, then the driver")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    import rv_loop as RL
    import inherit as INH
    import riscv_reference as RV_REF
    import handful as H
    import construct as CONS
    reference = RV_REF.RiscvReference()
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    if not os.path.isdir(work_root):
        os.makedirs(work_root)
    H.SRC_DIR = src_dir
    RG.renderer_for  # the shared render, named so the import is visible

    say("[1/4] the delta")
    cells = RL.untwinned(twins_path)
    say("   %d RISC-V cells with no x86 twin under either reading"
        % len(cells))
    terms, _operands = RL.riscv_terms(rv_path)

    say("[2/4] the general tier, both policies, on %s"
        % ", ".join(TARGETS))
    rows = []
    started = time.time()
    number = 0
    total = 0
    for cell in cells:
        total = total + len(cell["places"]) * len(TARGETS)
        continue
    for cell in cells:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        for place_name in cell["places"]:
            term = terms.get((key, place_name))
            for target in TARGETS:
                number = number + 1
                if limit is not None and number > limit:
                    break
                if term is None:
                    rows.append({"arch": "riscv64", "cell": dict(cell),
                                 "place": place_name, "target": target,
                                 "kind": "refused",
                                 "verdict": {
                                     "outcome": "NO_TERM",
                                     "reason": "the cell's own line "
                                               "could not be re-run"}})
                    continue
                rows.append(one_run(H, RL, INH, CONS, reference, cell,
                                    place_name, term, target,
                                    work_root, number))
                if number % 10 == 0 or number == total:
                    say("   [%d/%d] runs, %.0f s, peak %.0f MB"
                        % (number, total, time.time() - started,
                           check_memory("run %d" % number) / 1024.0))
                    write_rows(prefix, rows)
                continue
            continue
        continue

    say("[3/4] the census")
    census = {}
    per_target = {}
    for row in rows:
        census[row["kind"]] = census.get(row["kind"], 0) + 1
        held = per_target.setdefault(row["target"], {})
        held[row["kind"]] = held.get(row["kind"], 0) + 1
        continue
    for kind in sorted(census):
        say("   %-12s %d" % (kind, census[kind]))
        continue

    say("[4/4] writing")
    write_rows(prefix, rows)
    document = {
        "meta": {
            "task": "t4",
            "what": "the general construction tier over the RISC-V "
                    "cells with no x86 twin, on riscv64, both policies",
            "targets": list(TARGETS),
            "policies": list(POLICIES),
            "x86_reference_sha256": digest,
            "gate_width": "the cell's own key_width is the headline; "
                          "the whole written place is beside it",
            "solver_timeout_ms": SOLVER_MS,
            "gate_instruction_ceiling": GATE_INSTRUCTION_CEILING,
            "census": census,
            "per_target": per_target,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
        },
        "census": census,
        "per_target": per_target,
    }
    handle = open(prefix + ".json", "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("peak RSS: %d kB" % peak_kb())
    return 0


def write_rows(prefix, rows):
    handle = open(prefix + ".jsonl", "w")
    for row in rows:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()
    return


# ==================================================================
# section 3: the count beside rv3's
# ==================================================================

def cells_of(path, reader):
    out = set()
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        row = json.loads(text)
        key = reader(row)
        if key is not None:
            out.add(key)
        continue
    handle.close()
    return out


def loop_cell(row):
    if row.get("kind") != "proved":
        return None
    cell = row["cell"]
    return (cell["mnem"], cell["shape"], cell["key_width"])


def inherited_cell(row):
    if row.get("kind") not in ("proved", "agreed"):
        return None
    cell = row.get("cell") or {}
    if not cell:
        return None
    return (cell.get("mnem"), cell.get("shape"), cell.get("key_width"))


def count_command(prefix, twins_path, rv3_path, rv2_loop_path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(twins_path)))
    import rv_loop as RL
    cells = RL.untwinned(twins_path)
    say("| what | cells | share of the 255 |")
    say("|---|---|---|")
    # THE DENOMINATOR IS THE TWINS FILE'S OWN ROW COUNT, which is the
    # 255 task rv3 counts against: `twins.json` carries one row per
    # RISC-V CELL, and `model_table_rv.json` carries 1,512 rows because
    # its key is finer -- (mnemonic, operand shape, key width, builder,
    # condition, written places).  Lane `t4_l17` printed its shares
    # against 1,512 and they were wrong; the counts beside them were
    # right and are unchanged.
    handle = open(os.path.abspath(twins_path))
    document = json.load(handle)
    handle.close()
    whole = len(document.get("rows") or [])
    if whole == 0:
        whole = 255
    say("| RISC-V cells `twins.json` holds | %d | 100%% |" % whole)
    inherited = cells_of(rv3_path, inherited_cell)
    say("| reached by an INHERITED proved certificate, rv3 | %d | %.1f%% |"
        % (len(inherited), 100.0 * len(inherited) / whole))
    rv2 = set()
    if os.path.exists(rv2_loop_path):
        rv2 = cells_of(rv2_loop_path, loop_cell)
    say("| PROVED by task rv2's own loop | %d | %.1f%% |"
        % (len(rv2), 100.0 * len(rv2) / whole))
    say("| union, rv3's headline | %d | %.1f%% |"
        % (len(inherited | rv2), 100.0 * len(inherited | rv2) / whole))
    mine = set()
    if os.path.exists(prefix + ".jsonl"):
        mine = cells_of(prefix + ".jsonl", loop_cell)
    say("| PROVED by THIS task's general tier | %d | %.1f%% |"
        % (len(mine), 100.0 * len(mine) / whole))
    whole_union = inherited | rv2 | mine
    say("| **union, the inheritance with rv2's loop and this tier** | "
        "**%d** | **%.1f%%** |"
        % (len(whole_union), 100.0 * len(whole_union) / whole))
    say("")
    say("| what the general tier added over rv3's union | cells |")
    say("|---|---|")
    gained = mine - (inherited | rv2)
    say("| cells only the general tier reaches | %d |" % len(gained))
    for cell in sorted(gained):
        say("| `%s` `%s` %s | -- |" % (cell[0], cell[1], cell[2]))
        continue
    say("")
    say("the untwinned population this tier ran over: %d cells"
        % len(cells))
    say("peak resident: %d kB" % peak_kb())
    return 0


def main():
    command = sys.argv[1]
    if command == "run":
        limit = None
        if len(sys.argv) > 10:
            limit = int(sys.argv[10])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], limit)
    if command == "count":
        return count_command(sys.argv[2], sys.argv[3], sys.argv[4],
                             sys.argv[5])
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
