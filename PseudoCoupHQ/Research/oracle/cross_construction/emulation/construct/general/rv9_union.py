#!/usr/bin/env python3
"""rv9_union.py -- THE TABLE "of 255" FOR THE UNION OF EVERY ROUTE
AFTER THIS TASK, beside the same table computed from the stores that
existed before it, by ONE reader in ONE run -- which is what lets the
two be set against each other.

Node: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv9_brief.md`,
section 3.

THE OBJECTS, one sentence each, in relation.
  * A STORE is one json-lines file this line has written, one row per
    (cell, place, target) with a `kind` and, under `attempts`, one
    entry per route with its own verdict.
  * A ROUTE is the `policy` an attempt carries: the language's own
    operator first, every node constructed, or z3's own circuit.  The
    name is the store's, never this file's.
  * THE DENOMINATOR is `twins.json`'s own row count, which is the 255
    every table of this line counts against.

Nothing here reads a mnemonic except to print it in the field `mnem`,
which is machine form.

usage:
  rv9_union.py table <twins.json> <before:label=prefix,...>
                     <after:label=prefix,...>
"""

import json
import os
import sys

LANGUAGE_NAME = {"c": "c", "cpp": "c++", "go": "go", "rust": "rust"}
ORDER = ["c", "cpp", "rust", "go"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def rows_of(prefix):
    out = []
    path = prefix + ".jsonl"
    if not os.path.exists(path):
        say("   MISSING STORE: %s" % path)
        return out
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        out.append(json.loads(text))
        continue
    handle.close()
    return out


def key_of(row):
    cell = row["cell"]
    return (cell["mnem"], cell["shape"], cell["key_width"])


def proved_by_route(rows):
    """(route name, target) -> the set of cell keys proved."""
    out = {}
    for row in rows:
        attempts = row.get("attempts")
        if attempts is None:
            attempt = row.get("attempt")
            if attempt is None:
                continue
            attempts = [attempt]
        for attempt in attempts:
            verdict = attempt.get("verdict") or {}
            if verdict.get("outcome") != "PROVED":
                continue
            route = attempt.get("policy") or "unnamed"
            out.setdefault((route, row["target"]), set())
            out[(route, row["target"])].add(key_of(row))
            continue
        continue
    return out


def gather(spec):
    """label=prefix,label=prefix -> the merged (route, target) -> keys
    of every store named, with the stores listed."""
    held = {}
    named = []
    for piece in spec.split(","):
        text = piece.strip()
        if not text:
            continue
        label, prefix = text.split("=", 1)
        named.append((label, prefix))
        for key, keys in proved_by_route(rows_of(prefix)).items():
            held.setdefault(key, set())
            held[key] |= keys
            continue
        continue
    return held, named


def routes_of(held):
    out = []
    for (route, _target) in held:
        if route not in out:
            out.append(route)
        continue
    out.sort()
    return out


def one_table(title, held, named, whole):
    say("")
    say("%s" % title)
    say("   the stores read:")
    for label, prefix in named:
        say("     %-10s %s.jsonl" % (label, prefix))
        continue
    routes = routes_of(held)
    say("")
    header = "| language |"
    divider = "|---|"
    for route in routes:
        header = header + " %s |" % route
        divider = divider + "---|"
        continue
    header = header + " any route | of |"
    divider = divider + "---|---|"
    say(header)
    say(divider)
    per_language = {}
    for target in ORDER:
        line = "| %s |" % LANGUAGE_NAME[target]
        union = set()
        for route in routes:
            keys = held.get((route, target), set())
            union |= keys
            line = line + " %d |" % len(keys)
            continue
        per_language[target] = union
        line = line + " %d | %d |" % (len(union), whole)
        say(line)
        continue
    every = set()
    for target in ORDER:
        every |= per_language[target]
        continue
    all_four = None
    for target in ORDER:
        if all_four is None:
            all_four = set(per_language[target])
            continue
        all_four &= per_language[target]
        continue
    line = "| **proved on at least one language** |"
    for route in routes:
        union = set()
        for target in ORDER:
            union |= held.get((route, target), set())
            continue
        line = line + " **%d** |" % len(union)
        continue
    line = line + " **%d** | **%d** |" % (len(every), whole)
    say(line)
    say("| **proved on all four languages** |%s **%d** | **%d** |"
        % (" |" * len(routes), len(all_four or set()), whole))
    return per_language, every, all_four or set()


def table_command(twins_path, before_spec, after_spec):
    whole = len(json.load(open(twins_path))["rows"])
    before, before_named = gather(before_spec)
    after, after_named = gather(after_spec)
    say("THE DENOMINATOR IS twins.json's OWN ROW COUNT: %d cells"
        % whole)
    one, every_before, all_before = one_table(
        "BEFORE THIS TASK -- every route, every language, of %d on "
        "every row" % whole, before, before_named, whole)
    two, every_after, all_after = one_table(
        "AFTER THIS TASK -- every route, every language, of %d on "
        "every row" % whole, after, after_named, whole)
    say("")
    say("WHAT MOVED")
    say("| what | before | after | of |")
    say("|---|---|---|---|")
    for target in ORDER:
        say("| %s, any route | %d | %d | %d |"
            % (LANGUAGE_NAME[target], len(one.get(target, set())),
               len(two.get(target, set())), whole))
        continue
    say("| proved on at least one language | %d | %d | %d |"
        % (len(every_before), len(every_after), whole))
    say("| proved on all four languages | %d | %d | %d |"
        % (len(all_before), len(all_after), whole))
    say("")
    gained = every_after - every_before
    lost = every_before - every_after
    say("| cells this task adds | mnem | shape | width |")
    say("|---|---|---|---|")
    for key in sorted(gained):
        say("|  | `%s` | `%s` | %s |" % (key[0], key[1], key[2]))
        continue
    if not gained:
        say("|  none | | | |")
    say("")
    say("| cells that were proved before and are not now | mnem | "
        "shape | width |")
    say("|---|---|---|---|")
    for key in sorted(lost):
        say("|  | `%s` | `%s` | %s |" % (key[0], key[1], key[2]))
        continue
    if not lost:
        say("|  none | | | |")
    say("")
    say("| cells with no proof on any language by any route, after | "
        "mnem | shape | width |")
    say("|---|---|---|---|")
    everything = set()
    for row in rows_of(after_named[0][1]):
        everything.add(key_of(row))
        continue
    for label, prefix in after_named:
        for row in rows_of(prefix):
            everything.add(key_of(row))
            continue
        continue
    left = sorted(everything - every_after)
    for key in left:
        say("|  | `%s` | `%s` | %s |" % (key[0], key[1], key[2]))
        continue
    if not left:
        say("|  none | | | |")
    say("")
    say("the keys the stores hold: %d; with a proof somewhere: %d; "
        "left: %d" % (len(everything), len(every_after), len(left)))
    return 0


def main():
    command = sys.argv[1]
    if command == "table":
        return table_command(sys.argv[2], sys.argv[3], sys.argv[4])
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
