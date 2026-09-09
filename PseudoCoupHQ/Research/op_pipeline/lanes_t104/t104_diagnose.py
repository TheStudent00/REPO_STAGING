#!/usr/bin/env python3
"""t104_diagnose.py -- WHY the layer-5 texts of log_224 section 4
differ, measured rather than reasoned about.

THE QUESTION.  The normalize node's CORE already rules that the
arguments of every commutative operator are put in a fixed order
computed from the arguments themselves (design step 2 and step 4, task
79), and `term.py` carries that step.  Yet log_224 section 4 shows two
pool5 entries printing

    If(v0 == Concat(0, Extract(31, 0, v1)), 0, 1)
    If(Concat(0, Extract(31, 0, v0)) == v1, 0, 1)

for terms the solver proves equal.  So either the ordering step is not
reached for these units, or its key ties and the tie is settled by the
order the term arrived in.  This program prints the evidence for
whichever it is: for each unit named on the command line it rebuilds
the layer-4 term from canon40, prints the term, walks every commutative
node, and prints each argument's ordering key beside the order the
printed text puts them in.

It changes nothing.  It writes `t104_diagnose.json` and prints.

MEMORY: six units, one canon40 shard held at a time; the walk of task
79 over 26,152 units peaked at 83 MB resident.  The named abort is
ABORT_MEMORY_T104 at 6 GB.

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

No operator token appears in this file.

Coding discipline: no compound one-liner statements.

usage:
  t104_diagnose.py table
  t104_diagnose.py units
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)

import z3                                                        # noqa: E402
import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402

OUT = os.path.join(PIPELINE, "t104_diagnose.json")
MEMORY_CAP_KB = 6 * 1024 * 1024

# The six units log_224 section 4 names, as the three pairs it prints.
WANTED = [
    "cpp/op_509", "swift/regen_1023",
    "cpp/op_473", "swift/regen_1413",
    "swift/op_446", "swift/op_451",
]


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: peak resident %d kB passed the stated "
            "cap of %d kB" % (used, MEMORY_CAP_KB))
    return used


def opcode_names():
    """every `Z3_OP_*` name z3 exports, with its number.  Read off the
    module, so the table in the report is the table the code sees."""
    out = {}
    for name in dir(z3.z3consts):
        if not name.startswith("Z3_OP_"):
            continue
        value = getattr(z3.z3consts, name)
        if not isinstance(value, int):
            continue
        out.setdefault(value, [])
        out[value].append(name)
    return out


def print_table():
    names = opcode_names()
    rows = []
    for kind in sorted(T.COMMUTATIVE_OPERATORS):
        rows.append({
            "kind_number": kind,
            "kind_names": sorted(names.get(kind, [])),
            "table": "COMMUTATIVE_OPERATORS",
        })
    for kind in sorted(T.ROUNDED_COMMUTATIVE_OPERATORS):
        rows.append({
            "kind_number": kind,
            "kind_names": sorted(names.get(kind, [])),
            "table": "ROUNDED_COMMUTATIVE_OPERATORS",
        })
    sys.stdout.write(
        "-- the two tables in term.py, resolved against z3's own "
        "opcode enumeration\n")
    for row in rows:
        sys.stdout.write("   %-28s %5d  %s\n"
                         % (row["table"], row["kind_number"],
                            ",".join(row["kind_names"])))
    sys.stdout.flush()
    return rows


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(PIPELINE,
                                "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(PIPELINE, "canon40_interp.json"))
    pattern = os.path.join(PIPELINE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def find_units(wanted):
    """unit label -> its canon40 record, one shard held at a time."""
    left = set(wanted)
    found = {}
    for path in shards():
        document = json.load(open(path))
        units = document.get("units") or {}
        for name in list(left):
            if name not in units:
                continue
            record = dict(units[name])
            record["unit"] = name
            found[name] = record
            left.discard(name)
        document = None
        if not left:
            break
    return found, sorted(left)


def commutative_report(term):
    """every node of `term` whose declaration kind is in either table,
    with each argument's ordering key and the order it is printed in.

    The keys are `term.ordering_key`'s own, called on the argument, so
    the report shows the key the rule actually uses and not a second
    implementation of it."""
    rows = []
    seen = set()
    stack = [term]
    while stack:
        current = stack.pop()
        key = current.get_id()
        if key in seen:
            continue
        seen.add(key)
        if not z3.is_app(current):
            continue
        for index in range(current.num_args()):
            stack.append(current.arg(index))
        kind = current.decl().kind()
        in_plain = kind in T.COMMUTATIVE_OPERATORS
        in_rounded = kind in T.ROUNDED_COMMUTATIVE_OPERATORS
        if not in_plain:
            if not in_rounded:
                continue
        arguments = []
        for index in range(current.num_args()):
            cache = {}
            piece = T.ordering_key(current.arg(index), cache)
            arguments.append({
                "printed_position": index,
                "shape_key": piece[1],
                "concrete_key": piece[2],
                "printed": T.one_line(current.arg(index)),
            })
        order = list(range(len(arguments)))
        order.sort(key=lambda i: (arguments[i]["shape_key"],
                                  arguments[i]["concrete_key"]))
        rows.append({
            "node": T.one_line(current),
            "kind_number": kind,
            "table": "plain" if in_plain else "rounded",
            "arguments": arguments,
            "order_the_key_asks_for": order,
            "already_in_that_order": order == sorted(order),
        })
    return rows

# `operator_name` was dropped from the row above (2026-09-07, lane 11's
# guard): it put a bare operator token on a dict that is not a unit
# object (the row carries no `lang`/`id` of its own -- those live one
# level up, on the `out[name]` key), which is a spelling-ban violation.
# `kind_number` is the same machine form with no name attached; the
# print loop below names the node by its kind number alone.


def print_units():
    found, missing = find_units(WANTED)
    if missing:
        sys.stdout.write("   NOT FOUND in canon40: %s\n"
                         % ", ".join(missing))
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    out = {}
    total = len(WANTED)
    index = 0
    for name in WANTED:
        index = index + 1
        sys.stdout.write("[%d/%d] %s\n" % (index, total, name))
        sys.stdout.flush()
        if name not in found:
            out[name] = {"state": "not in canon40"}
            continue
        walked = maker.transcribe(found[name])
        if walked.out_term is None:
            out[name] = {"state": "no OUT-0 term"}
            continue
        raw = walked.out_term
        simplified = z3.simplify(raw)
        ordered = T.order_commutative(simplified)
        record = {
            "state": "TERM",
            "layer4_sexpr_length": len(raw.sexpr()),
            "raw_one_line": T.one_line(raw),
            "after_simplify_one_line": T.one_line(simplified),
            "after_order_one_line": T.one_line(ordered),
            "normalized_text_today": maker.normalize(raw),
            "commutative_nodes_after_simplify":
                commutative_report(simplified),
            "commutative_nodes_after_order":
                commutative_report(ordered),
        }
        out[name] = record
        sys.stdout.write("   today's layer-5 text: %s\n"
                         % record["normalized_text_today"])
        sys.stdout.write("   after simplify:       %s\n"
                         % record["after_simplify_one_line"])
        sys.stdout.write("   after order:          %s\n"
                         % record["after_order_one_line"])
        for row in record["commutative_nodes_after_simplify"]:
            sys.stdout.write("   commutative node kind %d (%s)\n"
                             % (row["kind_number"], row["table"]))
            for one in row["arguments"]:
                sys.stdout.write("      arg %d shape %s\n"
                                 % (one["printed_position"],
                                    one["shape_key"]))
            sys.stdout.write("      the key asks for order %s; already "
                             "in it: %s\n"
                             % (row["order_the_key_asks_for"],
                                row["already_in_that_order"]))
        sys.stdout.flush()
        check_memory()
    handle = open(OUT, "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    sys.stdout.write("-- wrote %s, peak resident %d kB\n"
                     % (OUT, check_memory()))
    sys.stdout.flush()
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: t104_diagnose.py table|units")
    if sys.argv[1] == "table":
        print_table()
        return 0
    if sys.argv[1] == "units":
        print_units()
        return 0
    raise SystemExit("unknown command %s" % sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
