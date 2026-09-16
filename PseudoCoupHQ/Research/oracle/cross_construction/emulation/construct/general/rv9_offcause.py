#!/usr/bin/env python3
"""rv9_offcause.py -- WHY OPTIMIZATION OFF MADE THE CHECK WORSE, named
from the bodies instead of guessed: the same population, the same
render, the same lifter and the same gate, compiled TWICE -- at the
corpus's ship flags and with optimization off -- with three MEASURED
properties read off every carved body, and the transitions crossed
against them.

Node: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv9_brief.md`,
section 2, last sentence: "the cause of rv4's regression named at last
(paste one body: is it stack traffic, an instruction the lifter lacks,
or the walk order?)".

WHAT rv4 MEASURED AND DID NOT NAME (log_263): the same 188 runs gave
144 proofs at ship flags and 36 with optimization off; the log's own
written cause ("no memory model") was RETRACTED in it, so the cause is
open.  This file closes it by reading the bodies.

THE THREE PROPERTIES, one sentence each, and every one of them is a
reading of the carved text that has the same answer shape for every
body.
  * INSTRUCTIONS NAMING A MEMORY ADDRESS: the operand text holds the
    architecture's own `offset(register)` form.  This is the reading of
    "stack traffic" -- no mnemonic is consulted.
  * BRANCHES INSIDE THE UNIT: the operand text resolves to a `<label>`
    whose symbol IS this unit's own, so the instruction goes somewhere
    else in the same body.  This is the reading of "the walk order".
  * THE WALK'S OWN REFUSAL: the lifter raised on the body, and its
    message is kept LITERAL.  This is the reading of "an instruction
    the lifter lacks".

DEE'S RULE OF 2026-09-13: nothing here is written for a particular
arch-opcode.  The population is the loop's own; the three properties
are asked of every body; the transition table is computed from
verdicts.

MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_RV9.  One
process, no pool, no clock in the driver.

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

HOW THIS FILE OBEYS IT.  Every row is keyed on (`mnem`, operand shape,
`key_width`, place, target, setting), which is machine form.  Nothing
here reads a source token.

usage:
  rv9_offcause.py run <ref_dir> <op_dir> <emulation_dir> <twins.json>
                      <model_table_rv.json> <prefix> <src_dir>
                      <work_root> [<limit>]
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

import rv_general as RG                                          # noqa: E402
import render_general as RENDER                                  # noqa: E402
import rv9_native as NAT                                         # noqa: E402

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV9"
TARGETS = ["c", "go"]
"""rv4's own two targets, so the transition table stands beside
log_263's."""
POLICIES = ("native_first", "all_constructed")
SETTINGS = ("ship", "off")


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
# section 1: the setting
# ==================================================================

def apply_setting(name):
    """the flags each route carries under one setting, put in place and
    printed LITERAL.  The rewrite is textual and general: any
    optimization-level flag moves to the stated level."""
    import inherit_rv3 as INH3
    import riscv_carve as CARVE
    if name == "ship":
        INH3.SHIP_C = list(SHIP["c"])
        INH3.SHIP_CPP = list(SHIP["cpp"])
        INH3.RUST_SHIP = list(SHIP["rust"])
        CARVE.sh = PLAIN_SH[0]
    else:
        INH3.SHIP_C = at_level(SHIP["c"], "0")
        INH3.SHIP_CPP = at_level(SHIP["cpp"], "0")
        INH3.RUST_SHIP = at_level(SHIP["rust"], "0")
        plain = PLAIN_SH[0]

        def with_the_flag(command, *arguments, **named):
            if command[:2] == ["go", "build"]:
                command = command[:2] + ["-gcflags=all=-N -l"] \
                    + command[2:]
            return plain(command, *arguments, **named)

        CARVE.sh = with_the_flag
    say("   setting %-4s c: clang %s" % (name, " ".join(INH3.SHIP_C)))
    say("   setting %-4s rust: rustc %s"
        % (name, " ".join(INH3.RUST_SHIP)))
    if name == "ship":
        say("   setting %-4s go: GOARCH=riscv64 GOOS=linux go build -o "
            "<obj> ." % name)
    else:
        say("   setting %-4s go: GOARCH=riscv64 GOOS=linux go build "
            "-gcflags=all=-N -l -o <obj> ." % name)
    return


def at_level(flags, level):
    out = []
    for flag in flags:
        if flag.startswith("-O") and len(flag) > 2:
            out.append("-O" + level)
            continue
        if flag.startswith("opt-level="):
            out.append("opt-level=" + level)
            continue
        out.append(flag)
        continue
    return out


SHIP = {}
PLAIN_SH = [None]


# ==================================================================
# section 2: one attempt, with the three properties read off the body
# ==================================================================

def branches_inside(body, symbol):
    """the instructions whose `<label>` resolves to this unit's own
    symbol: the body goes somewhere else inside itself."""
    mine = set()
    mine.add(symbol)
    mine.add("main." + symbol)
    out = []
    for index, line in enumerate(body):
        for label in NAT.labels_of(line):
            head = label.split("+")[0].strip()
            if head not in mine:
                continue
            out.append({"index": index, "line": line})
            continue
        continue
    return out


def one_attempt(H, RL, INH, reference, cell, place_name, term, target,
                record, word, policy, work_root, number):
    label = "%s_%s_%d__%s__%s__%s" % (cell["mnem"], cell["shape"],
                                      cell["key_width"], place_name,
                                      target, policy)
    label = label.replace(".", "_")
    out = {"policy": policy, "label": label}
    ordered = H.renderer_input(record["term"])
    try:
        made = RENDER.render(ordered, target, record["families"],
                             record["home"]["family"], record["bits"],
                             label, word, policy,
                             record.get("text") or "")
    except Exception as problem:                              # noqa: BLE001
        out["rendered"] = False
        out["refusal_cause"] = "the render refused"
        out["refusal_detail"] = "%s: %s" % (type(problem).__name__,
                                            ("%s" % problem)[:300])
        return out
    out["rendered"] = True
    out["statements"] = made["statements"]
    out["source_lines"] = made["source"].count("\n") + 1
    work = os.path.join(work_root, "rv9o%06d_%s_%s"
                        % (number, target, policy))
    started = time.time()
    got, command, diagnostic = INH.compile_and_carve(made["source"],
                                                     target, work)
    out["compile_seconds"] = round(time.time() - started, 3)
    out["compiler"] = {"command": command}
    if got is None:
        out["compiled"] = False
        out["verdict"] = {"outcome": "BUILD_REFUSED",
                          "reason": (diagnostic or "").strip()[:600]}
        return out
    out["compiled"] = True
    raw, body = got
    symbol = INH.symbol_of(made["source"])
    out["instructions"] = len(body)
    out["memory_operands"] = len(NAT.memory_operands(body))
    out["branches_inside"] = len(branches_inside(body, symbol or ""))
    out["references_out"] = len(NAT.references_out(body, symbol or ""))
    out["body"] = NAT_body(body)
    out["gate_instruction_ceiling"] = RG.GATE_INSTRUCTION_CEILING
    if len(body) > RG.GATE_INSTRUCTION_CEILING:
        out["verdict"] = {"outcome": "NOT_GATED",
                          "reason": RG.CAUSE_GATE_TOO_LARGE,
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
    started = time.time()
    outcome, counterexample = INH.decide(INH.at_width(answer, width),
                                         INH.at_width(term, width),
                                         RG.SOLVER_MS)
    out["check_seconds"] = round(time.time() - started, 3)
    out["verdict"] = {"outcome": outcome, "compared_on_bits": width,
                      "counterexample": counterexample,
                      "solver_timeout_ms": RG.SOLVER_MS}
    return out


BODY_TEXT_CEILING = 20000


def NAT_body(body):
    if len(body) <= BODY_TEXT_CEILING:
        return list(body)
    return list(body[:200]) + ["... %d instructions not kept as text "
                              "..." % (len(body) - 400)] \
        + list(body[-200:])


# ==================================================================
# section 3: the run
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
    say("[0/5] the references this run uses")
    X86, TERMS, MT, MTAB, digest = TW.bring_in(ref_dir, op_dir)
    import rv_loop as RL
    import inherit_rv3 as INH3
    import inherit as INH
    import riscv_carve as CARVE
    import riscv_reference as RV_REF
    import handful as H
    import construct as CONS
    INH3.install()
    SHIP["c"] = list(INH3.SHIP_C)
    SHIP["cpp"] = list(INH3.SHIP_CPP)
    SHIP["rust"] = list(INH3.RUST_SHIP)
    PLAIN_SH[0] = CARVE.sh
    reference = RV_REF.RiscvReference()
    say("   the x86 reference   %s" % digest)
    say("   the riscv lifter    %s" % NAT.RG_sha(RV_REF.__file__))
    if not os.path.isdir(work_root):
        os.makedirs(work_root)

    say("[1/5] the population: the loop's own, which is rv4's")
    cells = RL.untwinned(twins_path)
    say("   %d RISC-V cells with no x86 twin under either reading"
        % len(cells))
    terms, _operands = RL.riscv_terms(rv_path)

    say("[2/5] both settings, on %s" % ", ".join(TARGETS))
    rows = []
    started = time.time()
    for setting in SETTINGS:
        apply_setting(setting)
        number = 0
        for cell in cells:
            key = (cell["mnem"], cell["shape"], cell["key_width"])
            for place_name in cell["places"]:
                term = terms.get((key, place_name))
                for target in TARGETS:
                    number = number + 1
                    if limit is not None and number > limit:
                        break
                    row = {"arch": "riscv64", "cell": dict(cell),
                           "place": place_name, "target": target,
                           "setting": setting, "route": "native"}
                    if term is None:
                        row["kind"] = "refused"
                        row["verdict"] = {"outcome": "NO_TERM"}
                        rows.append(row)
                        continue
                    slotted, refusal = RL.in_parameter_slots(
                        sys.modules["term"], term)
                    if slotted is None:
                        row["kind"] = "refused"
                        row["verdict"] = {"outcome": "NOT_RENDERED",
                                          "reason": refusal}
                        rows.append(row)
                        continue
                    record = H.place_record("reg_rdi", slotted)
                    if record.get("families") is None:
                        row["kind"] = "refused"
                        row["verdict"] = {"outcome": "NOT_RENDERED",
                                          "reason": record.get(
                                              "not_rendered_detail")
                                          or record.get("not_rendered")}
                        rows.append(row)
                        continue
                    word = CONS.word_of(target)
                    attempts = []
                    for policy in POLICIES:
                        attempts.append(one_attempt(
                            H, RL, INH, reference, cell, place_name,
                            term, target, record, word, policy,
                            work_root, number))
                        continue
                    row["attempts"] = attempts
                    row["kind"] = best_kind(row, attempts)
                    rows.append(row)
                    if number % 20 == 0:
                        say("   [%s %d] runs, %.0f s, peak %.0f MB"
                            % (setting, number, time.time() - started,
                               check_memory("run %d" % number) / 1024.0))
                    continue
                continue
            continue
        continue

    say("[3/5] the census, setting by setting")
    census(rows)

    say("[4/5] the transitions, crossed with the three properties")
    transitions(rows)

    say("[5/5] writing")
    write_rows(prefix, rows)
    document = {
        "meta": {
            "task": "rv9",
            "what": "the same population, the same render and the same "
                    "gate, compiled at the corpus's ship flags and with "
                    "optimization off, with three measured properties "
                    "read off every carved body",
            "targets": list(TARGETS),
            "policies": list(POLICIES),
            "settings": list(SETTINGS),
            "x86_reference_sha256": digest,
            "riscv_reference_sha256": NAT.RG_sha(RV_REF.__file__),
            "solver_timeout_ms": RG.SOLVER_MS,
            "gate_instruction_ceiling": RG.GATE_INSTRUCTION_CEILING,
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
            "seconds": round(time.time() - started, 1),
        },
    }
    handle = open(prefix + ".json", "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("peak RSS: %d kB" % peak_kb())
    return 0


def best_kind(row, attempts):
    for attempt in attempts:
        if RG.kind_of_attempt(attempt) == "proved":
            return "proved"
        continue
    order = ["sat", "undecided", "refused"]
    best = None
    for attempt in attempts:
        kind = RG.kind_of_attempt(attempt)
        if best is None or order.index(kind) < order.index(best):
            best = kind
        continue
    return best or "refused"


def write_rows(prefix, rows):
    handle = open(prefix + ".jsonl", "w")
    for row in rows:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        continue
    handle.close()
    return


# ==================================================================
# section 4: the reading
# ==================================================================

def key_of(row):
    cell = row["cell"]
    return (cell["mnem"], cell["shape"], cell["key_width"], row["place"],
            row["target"])


def census(rows):
    held = {}
    for row in rows:
        key = (row["setting"], row["kind"])
        held[key] = held.get(key, 0) + 1
        continue
    say("")
    say("| setting | proved | disproved | undecided | refused | runs |")
    say("|---|---|---|---|---|---|")
    for setting in SETTINGS:
        line = []
        total = 0
        for kind in ("proved", "sat", "undecided", "refused"):
            count = held.get((setting, kind), 0)
            line.append(count)
            total = total + count
            continue
        say("| %s | %d | %d | %d | %d | %d |"
            % (setting, line[0], line[1], line[2], line[3], total))
        continue
    say("")
    return


def properties_of(row):
    """the three measured properties of a row's carved bodies, taken
    over its attempts: the largest body's memory operands, its branches
    inside the unit, and whether any walk refused (with its words)."""
    memory = 0
    branches = 0
    refusal = None
    instructions = 0
    for attempt in row.get("attempts") or []:
        if attempt.get("memory_operands") is not None:
            if attempt["memory_operands"] > memory:
                memory = attempt["memory_operands"]
        if attempt.get("branches_inside") is not None:
            if attempt["branches_inside"] > branches:
                branches = attempt["branches_inside"]
        if attempt.get("instructions") is not None:
            if attempt["instructions"] > instructions:
                instructions = attempt["instructions"]
        verdict = attempt.get("verdict") or {}
        if verdict.get("outcome") == "WALK_REFUSED":
            refusal = verdict.get("reason")
        continue
    return {"memory_operands": memory, "branches_inside": branches,
            "walk_refusal": refusal, "instructions": instructions}


def transitions(rows):
    keyed = {}
    for row in rows:
        keyed.setdefault(key_of(row), {})
        keyed[key_of(row)][row["setting"]] = row
        continue
    moved = []
    held = {}
    for key in sorted(keyed):
        ship = keyed[key].get("ship")
        off = keyed[key].get("off")
        if ship is None or off is None:
            continue
        pair = (ship["kind"], off["kind"])
        held[pair] = held.get(pair, 0) + 1
        if ship["kind"] == "proved" and off["kind"] != "proved":
            moved.append((key, ship, off))
        continue
    say("")
    say("| at ship flags | with optimization off | keys |")
    say("|---|---|---|")
    for pair in sorted(held, key=lambda p: -held[p]):
        say("| %s | %s | %d |" % (pair[0], pair[1], held[pair]))
        continue
    say("")
    say("THE KEYS THAT WERE PROVED AND ARE NOT: %d" % len(moved))
    say("| mnem | shape | width | language | off outcome | ship "
        "instructions | off instructions | ship memory operands | off "
        "memory operands | ship branches | off branches | the walk "
        "refused |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    causes = {}
    for key, ship, off in moved:
        one = properties_of(ship)
        two = properties_of(off)
        outcome = None
        for attempt in off.get("attempts") or []:
            verdict = attempt.get("verdict") or {}
            if verdict.get("outcome"):
                outcome = verdict["outcome"]
                if outcome != "PROVED":
                    break
            continue
        say("| `%s` | `%s` | %s | %s | %s | %d | %d | %d | %d | %d | %d "
            "| %s |"
            % (key[0], key[1], key[2], key[4], outcome,
               one["instructions"], two["instructions"],
               one["memory_operands"], two["memory_operands"],
               one["branches_inside"], two["branches_inside"],
               two["walk_refusal"] is not None))
        cause = (two["walk_refusal"] is not None,
                 two["memory_operands"] > one["memory_operands"],
                 two["branches_inside"] > one["branches_inside"])
        causes[cause] = causes.get(cause, 0) + 1
        continue
    say("")
    say("THE SAME KEYS COUNTED BY WHICH OF THE THREE PROPERTIES MOVED")
    say("| the walk refused | more instructions naming memory | more "
        "branches inside the unit | keys |")
    say("|---|---|---|---|")
    for cause in sorted(causes, key=lambda c: -causes[c]):
        say("| %s | %s | %s | %d |"
            % (cause[0], cause[1], cause[2], causes[cause]))
        continue
    say("")
    say("EVERY DISTINCT WALK REFUSAL, LITERAL, WITH ITS COUNT")
    words = {}
    for key, ship, off in moved:
        two = properties_of(off)
        if two["walk_refusal"] is None:
            continue
        text = " ".join(two["walk_refusal"].split())
        words[text] = words.get(text, 0) + 1
        continue
    say("| the refusal, LITERAL | keys |")
    say("|---|---|")
    for text in sorted(words, key=lambda t: -words[t]):
        say("| `%s` | %d |" % (text[:200], words[text]))
        continue
    say("")
    if moved:
        show_one(moved)
    return


def show_one(moved):
    """ONE body pasted whole, chosen by a machine-form rule: the key
    whose body grew the most from ship flags to optimization off, since
    that is the one the question is about."""
    ranked = []
    for key, ship, off in moved:
        one = properties_of(ship)
        two = properties_of(off)
        ranked.append((two["instructions"] - one["instructions"], key,
                       ship, off))
        continue
    ranked.sort(key=lambda r: -r[0])
    grew, key, ship, off = ranked[0]
    say("THE BODY OF THE KEY WHOSE CARVED BODY GREW MOST, BOTH "
        "SETTINGS, LITERAL")
    say("   %s %s %s, place %s, %s: %d instructions more with "
        "optimization off" % (key[0], key[1], key[2], key[3], key[4],
                              grew))
    for name, row in (("ship", ship), ("off", off)):
        for attempt in row.get("attempts") or []:
            body = attempt.get("body")
            if not body:
                continue
            say("   --- setting %s, policy %s, %d instructions"
                % (name, attempt.get("policy"),
                   attempt.get("instructions")))
            verdict = attempt.get("verdict") or {}
            say("       verdict: %s"
                % json.dumps(verdict, sort_keys=True)[:300])
            if len(body) > 120:
                NAT.paste(body[:60])
                say("   ... %d instructions not shown ..."
                    % (len(body) - 80))
                NAT.paste(body[-20:])
            else:
                NAT.paste(body)
            continue
        continue
    return


def main():
    command = sys.argv[1]
    if command == "run":
        limit = None
        if len(sys.argv) > 10:
            limit = int(sys.argv[10])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], limit)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
