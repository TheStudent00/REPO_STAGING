#!/usr/bin/env python3
"""rv9_settings.py -- THE BIT-BLAST ROUTE AT THREE OPTIMIZATION
SETTINGS: `bb1_run.py`'s route with ONE thing varied, how much the
target's compiler is allowed to rewrite z3's circuit before the body is
carved.

Node: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv9_brief.md`,
section 2.

WHAT THIS FILE IS, one sentence, in relation: `bb1_run.py` imported so
its render, its store shape and its swaps into `rv_general` are CALLED
and not copied, with the population narrowed to the cells the blast
route did not close and the compile flags moved by one general rule per
language.

WHY THE SETTINGS EXIST, from the brief: at ship flags the compiler is
free to rewrite z3's circuit, so the check compares two unlike
circuits; with less rewriting the carved body should follow the circuit
gate by gate.  The question is measured, not assumed, and the answer is
three columns.

THE THREE SETTINGS, and every one of them is a rule about a FLAG and
never about a cell.

| setting | c and c++ | rust | go |
|---|---|---|---|
| `ship` | the route's own line, untouched | the route's own line | `go build` with no flag |
| `one` | the optimization flag moved to level 1 | `opt-level=1` | `go build` with inlining off |
| `off` | the optimization flag moved to level 0 | `opt-level=0` | `go build` with the local optimizations and inlining off |

`ship` and `one` differ only where a route's own level is not 1, which
on these four routes is go alone -- and that identity is itself a check
on the table, so both columns are run and neither is assumed.

DEE'S RULE OF 2026-09-13: nothing in this file is written for a
particular arch-opcode.  The population is a reading of VERDICTS in a
store this file did not write; the flag rewrite is textual and general
(any `-O<level>` becomes the stated level, any `opt-level=<n>` becomes
the stated level); every question is asked of every member.

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

HOW THIS FILE OBEYS IT.  The population is a reading of verdicts; every
row is keyed on (`mnem`, operand shape, `key_width`, place, target,
setting), which is machine form.  Nothing here reads a source token and
no branch anywhere is taken on a mnemonic.

usage:
  rv9_settings.py run <setting> <ref_dir> <op_dir> <emulation_dir>
                      <twins.json> <model_table_rv.json> <prefix>
                      <src_dir> <work_root> <blast store.jsonl>
                      <other store.jsonl,...> [<spread count>]
  rv9_settings.py table <prefix ship> <prefix one> <prefix off>
                        <twins.json>
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bb1_run as BB1                                            # noqa: E402
import rv_general as RG                                          # noqa: E402


SETTINGS = ("ship", "one", "off")
LEVEL = {"ship": None, "one": "1", "off": "0"}
GO_FLAGS = {"ship": None, "one": "-gcflags=all=-l",
            "off": "-gcflags=all=-N -l"}

RG.ABORT_NAME = "ABORT_MEMORY_RV9"


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ==================================================================
# section 1: the setting, as one general rewrite per language
# ==================================================================

def at_level(flags, level):
    """the same flag list with any optimization-level flag moved to the
    stated level.  The rule is textual and holds for every list."""
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


def apply_setting(name):
    """put the setting in place on the four routes and print what each
    route's line now is, LITERAL."""
    import inherit_rv3 as INH3
    import riscv_carve as CARVE
    level = LEVEL[name]
    if level is not None:
        INH3.SHIP_C = at_level(INH3.SHIP_C, level)
        INH3.SHIP_CPP = at_level(INH3.SHIP_CPP, level)
        INH3.RUST_SHIP = at_level(INH3.RUST_SHIP, level)
    go_flag = GO_FLAGS[name]
    if go_flag is not None:
        plain = CARVE.sh

        def with_the_flag(command, *arguments, **named):
            if command[:2] == ["go", "build"]:
                command = command[:2] + [go_flag] + command[2:]
            return plain(command, *arguments, **named)

        CARVE.sh = with_the_flag
    say("   the setting: %s" % name)
    say("   c    : clang %s" % " ".join(INH3.SHIP_C))
    say("   cpp  : %s %s" % (INH3.CLANGXX, " ".join(INH3.SHIP_CPP)))
    say("   rust : rustc %s" % " ".join(INH3.RUST_SHIP))
    if go_flag is None:
        say("   go   : GOARCH=riscv64 GOOS=linux go build -o <obj> .")
    else:
        say("   go   : GOARCH=riscv64 GOOS=linux go build %s -o <obj> ."
            % go_flag)
    return


# ==================================================================
# section 2: the population -- a reading of verdicts
# ==================================================================

def read_keys(path):
    """(the keys the store holds, the keys it proves on every target it
    ran, the body size it recorded for each key)."""
    held = {}
    proved = {}
    size = {}
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        row = json.loads(text)
        cell = row["cell"]
        key = (cell["mnem"], cell["shape"], cell["key_width"],
               row["place"])
        held.setdefault(key, 0)
        held[key] = held[key] + 1
        if row.get("kind") == "proved":
            proved.setdefault(key, 0)
            proved[key] = proved[key] + 1
        for attempt in row.get("attempts") or []:
            count = attempt.get("gates")
            if count is None:
                continue
            if count > size.get(key, -1):
                size[key] = count
            continue
        continue
    handle.close()
    return held, proved, size


def population(blast_path, other_paths, twins_path, spread):
    """the cells this task's section 2 runs over: every key the blast
    route did not prove on every language it ran, together with every
    key no store proves at all.

    THE ORDER IS BY THE BLAST'S OWN GATE COUNT, largest first, because
    the sample's whole purpose is to say what the expensive end costs
    and the file's own order is the cheap end."""
    held, proved, size = read_keys(blast_path)
    unclosed = set()
    for key in held:
        if proved.get(key, 0) < held[key]:
            unclosed.add(key)
        continue
    proved_anywhere = set()
    every = set()
    for path in [blast_path] + other_paths:
        one_held, one_proved, _size = read_keys(path)
        every |= set(one_held)
        proved_anywhere |= set(one_proved)
        continue
    no_proof = every - proved_anywhere
    keys = sorted(unclosed | no_proof, key=lambda k: (-size.get(k, -1),
                                                      k))
    say("   the blast route left %d of %d (cell, place) keys unproved "
        "on at least one language" % (len(unclosed), len(held)))
    say("   %d keys carry no proof in any store, by any route"
        % len(no_proof))
    say("   the population is their union: %d keys" % len(keys))
    if spread is not None and spread < len(keys):
        picked = []
        for index in range(spread):
            place = int(round(index * (len(keys) - 1)
                              / float(max(spread - 1, 1))))
            if keys[place] not in picked:
                picked.append(keys[place])
            continue
        keys = picked
        say("   the sample takes %d of them, spread evenly over the "
            "gate-count order" % len(keys))
    for key in keys:
        say("     %s %s %s, place %s, gates %s"
            % (key[0], key[1], key[2], key[3], size.get(key)))
        continue
    shaped = {}
    order = []
    for key in keys:
        head = (key[0], key[1], key[2])
        if head not in shaped:
            shaped[head] = []
            order.append(head)
        shaped[head].append(key[3])
        continue
    out = []
    for head in order:
        out.append({"mnem": head[0], "shape": head[1],
                    "key_width": head[2], "places": shaped[head]})
        continue
    return out


# ==================================================================
# section 3: the table over the three settings
# ==================================================================

LANGUAGE_NAME = {"c": "c", "cpp": "c++", "go": "go", "rust": "rust"}
ORDER = ["c", "cpp", "rust", "go"]


def rows_of(prefix):
    rows = []
    path = prefix + ".jsonl"
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


def table_command(prefixes, twins_path):
    whole = len(json.load(open(twins_path))["rows"])
    per_setting = {}
    for name in SETTINGS:
        per_setting[name] = rows_of(prefixes[name])
        continue
    say("")
    say("THE THREE SETTINGS, OUTCOME BY LANGUAGE, of %d on every row"
        % whole)
    say("| setting | language | attempts | proved | disproved | "
        "undecided | refused | of |")
    say("|---|---|---|---|---|---|---|---|")
    for name in SETTINGS:
        for target in ORDER:
            counts = {"proved": 0, "sat": 0, "undecided": 0,
                      "refused": 0}
            attempts = 0
            for row in per_setting[name]:
                if row["target"] != target:
                    continue
                attempts = attempts + 1
                counts[row["kind"]] = counts[row["kind"]] + 1
                continue
            say("| %s | %s | %d | %d | %d | %d | %d | %d |"
                % (name, LANGUAGE_NAME[target], attempts,
                   counts["proved"], counts["sat"], counts["undecided"],
                   counts["refused"], whole))
            continue
        continue
    say("")
    say("EVERY ATTEMPT, THE THREE SETTINGS SIDE BY SIDE")
    say("| mnem | shape | width | place | language | setting | "
        "compiled | carved instructions | lifted | verdict | compile s "
        "| check s |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|")
    keyed = {}
    for name in SETTINGS:
        for row in per_setting[name]:
            cell = row["cell"]
            key = (cell["mnem"], cell["shape"], cell["key_width"],
                   row["place"], row["target"])
            keyed.setdefault(key, {})
            keyed[key][name] = row
            continue
        continue
    for key in sorted(keyed):
        for name in SETTINGS:
            row = keyed[key].get(name)
            if row is None:
                continue
            attempt = (row.get("attempts") or [{}])[0]
            verdict = attempt.get("verdict") or {}
            outcome = verdict.get("outcome")
            if outcome is None:
                outcome = attempt.get("refusal_cause") or "no verdict"
            lifted = "yes"
            if outcome in ("WALK_REFUSED", "NOT_GATED", "BUILD_REFUSED"):
                lifted = "no"
            if not attempt.get("rendered"):
                lifted = "no"
            say("| `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s "
                "| %s | %s |"
                % (key[0], key[1], key[2], key[3],
                   LANGUAGE_NAME.get(key[4], key[4]), name,
                   attempt.get("compiled"), attempt.get("instructions"),
                   lifted, outcome, attempt.get("compile_seconds"),
                   attempt.get("check_seconds")))
            continue
        continue
    say("")
    say("THE BODY SIZE, SETTING BY SETTING")
    say("| language | setting | bodies carved | smallest | median | "
        "mean | largest |")
    say("|---|---|---|---|---|---|---|")
    for target in ORDER:
        for name in SETTINGS:
            sizes = []
            for row in per_setting[name]:
                if row["target"] != target:
                    continue
                attempt = (row.get("attempts") or [{}])[0]
                if attempt.get("instructions") is None:
                    continue
                sizes.append(attempt["instructions"])
                continue
            count, low, middle, mean, high = BB1.quantiles(sizes)
            say("| %s | %s | %d | %s | %s | %s | %s |"
                % (LANGUAGE_NAME[target], name, count, low, middle,
                   mean, high))
            continue
        continue
    say("")
    say("EVERY OUTCOME THAT IS NOT A PROOF, WITH ITS CAUSE, LITERAL")
    say("| setting | language | outcome | cause | attempts |")
    say("|---|---|---|---|---|")
    held = {}
    for name in SETTINGS:
        for row in per_setting[name]:
            for attempt in row.get("attempts") or []:
                verdict = attempt.get("verdict") or {}
                outcome = verdict.get("outcome")
                if outcome is None and attempt.get("refusal_cause"):
                    outcome = attempt["refusal_cause"]
                if outcome in (None, "PROVED"):
                    continue
                detail = attempt.get("refusal_detail") \
                    or verdict.get("reason") or ""
                key = (name, row["target"], outcome,
                       " ".join(detail.split())[:120])
                held[key] = held.get(key, 0) + 1
                continue
            continue
        continue
    for key in sorted(held, key=lambda k: (-held[k], k)):
        say("| %s | %s | %s | %s | %d |"
            % (key[0], LANGUAGE_NAME.get(key[1], key[1]), key[2],
               key[3], held[key]))
        continue
    say("")
    return 0


# ==================================================================
# section 4: the run
# ==================================================================

def run_command(setting, ref_dir, op_dir, emulation_dir, twins_path,
                rv_path, prefix, src_dir, work_root, blast_path,
                other_arg, spread):
    if setting not in SETTINGS:
        raise SystemExit("unknown setting %r" % setting)
    sys.path.insert(0, os.path.dirname(os.path.abspath(twins_path)))
    import rv_loop as RL
    say("[0/2] the setting, LITERAL")
    apply_setting(setting)
    others = []
    for name in other_arg.split(","):
        text = name.strip()
        if text:
            others.append(text)
        continue
    say("[1/2] the population")
    chosen = population(blast_path, others, twins_path, spread)

    def the_population(_twins_path):
        return chosen

    RL.untwinned = the_population
    say("[2/2] the run")
    arguments = ["run", ref_dir, op_dir, emulation_dir, twins_path,
                 rv_path, prefix, src_dir, work_root]
    sys.argv = [sys.argv[0]] + arguments
    code = RG.main()
    name_the_document(prefix, setting)
    return code


def name_the_document(prefix, setting):
    """the run's own `<prefix>.json`, with this task and this setting
    put on it.  `rv_general.run_command` writes task t4's own header and
    that file is READ here, so the name goes on afterwards."""
    path = prefix + ".json"
    if not os.path.exists(path):
        return
    handle = open(path)
    document = json.load(handle)
    handle.close()
    document["meta"]["task"] = "rv9"
    document["meta"]["setting"] = setting
    document["meta"]["route"] = "bit_blast"
    document["meta"]["what"] = (
        "the bit-blast route over every cell the blast route did not "
        "close, and every cell no store proves at all, compiled for "
        "riscv64 at the '%s' optimization setting, carved, walked and "
        "gated" % setting)
    document["meta"]["memory_abort"] = "ABORT_MEMORY_RV9"
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


def main():
    command = sys.argv[1]
    if command == "table":
        prefixes = {"ship": sys.argv[2], "one": sys.argv[3],
                    "off": sys.argv[4]}
        return table_command(prefixes, sys.argv[5])
    if command == "run":
        spread = None
        if len(sys.argv) > 13:
            spread = int(sys.argv[13])
        return run_command(sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], sys.argv[6], sys.argv[7],
                           sys.argv[8], sys.argv[9], sys.argv[10],
                           sys.argv[11], sys.argv[12], spread)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
