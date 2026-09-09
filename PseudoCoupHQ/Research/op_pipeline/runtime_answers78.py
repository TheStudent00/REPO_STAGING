#!/usr/bin/env python3
"""runtime_answers78.py -- the attached callees' own answer registers.

TASK 78.  The driver for the settled rule "THE ANSWER REGISTERS ARE
READ OFF THE ATTACHED CALLEE'S BODY" of
`CORE_0_3_5_3_3_destination_rules.md` (node
`hq.research.compiler_graph.ledger.destination_rules`).  The RULE
itself lives in `ledger.py` (`answer_registers_of_body`), because the
rule is the ledger node's; this file only applies it to the callee
bodies task 63 extracted and writes the answer down as data.

Input   canon39_callee_units.json   -- 76 callee arch units, each with
                                       its own body, from the archive
                                       of the toolchain that built the
                                       caller (log_167).
Output  runtime_answers78.json      -- per `toolchain/name`, the
                                       register families that body
                                       changes, in the order of their
                                       last change, or a named refusal.
        runtime_answers78_printed.txt -- the transcript.

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

No operator token appears in this file.  Its keys are toolchain names
and routine names read out of an archive's own symbol index.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger as L                                                # noqa: E402


CALLEE_UNITS = "canon39_callee_units.json"
OUT_JSON = "runtime_answers78.json"
OUT_TEXT = "runtime_answers78_printed.txt"

# The x86-64 answer homes, used ONLY as a cross-check to report
# agreement or disagreement with the reading.  Nothing is decided from
# this set: it is the weakest evidence class (human interpretation of
# stated design) and it never reaches the ledger.
CROSS_CHECK_HOMES = ("rax", "rdx", "xmm0", "xmm1")


def read_bodies():
    path = os.path.join(HERE, CALLEE_UNITS)
    document = json.load(open(path))
    return document["units"], document.get("meta", {})


def build(bodies):
    """every callee's reading, with nested and tail transfers resolved
    inside the SAME toolchain's archive."""
    readings = {}

    def resolve(name, seen):
        key = None
        for candidate in bodies:
            if candidate.endswith("/" + name):
                key = candidate
                break
        if key is None:
            return None
        if key in seen:
            return {"families": [], "x87": False, "saw_return": True,
                    "how": "already being read: the cycle guard "
                           "stopped here"}
        return read_one(key, set(seen) | {key})

    def read_one(key, seen):
        if key in readings:
            return readings[key]
        record = bodies[key]
        lines = record.get("body_verbatim") or []

        def scoped(name, inner_seen):
            toolchain = key.split("/", 1)[0]
            wanted = toolchain + "/" + name
            if wanted in bodies:
                if wanted in inner_seen:
                    return {"families": [], "x87": False,
                            "saw_return": True,
                            "how": "the cycle guard stopped here"}
                return read_one(wanted, set(inner_seen) | {wanted})
            return resolve(name, inner_seen)

        reading = L.answer_registers_of_body(lines, resolve=scoped,
                                             seen=seen)
        reading["toolchain"] = key.split("/", 1)[0]
        reading["callee"] = record.get("callee")
        reading["instruction_count"] = record.get("instruction_count")
        readings[key] = reading
        return reading

    for key in sorted(bodies):
        read_one(key, {key})
    return readings


def cross_check(reading):
    """agreement with the stated calling convention, reported and
    never used."""
    families = reading.get("families") or []
    inside = []
    for family in families:
        if family in CROSS_CHECK_HOMES:
            inside.append(family)
    if reading.get("x87"):
        inside.append("st(0)")
    return inside


def main(argv):
    bodies, meta = read_bodies()
    readings = build(bodies)
    lines = []
    lines.append("TASK 78 -- THE ATTACHED CALLEE'S OWN ANSWER "
                 "REGISTERS, READ OFF ITS BODY")
    lines.append("")
    lines.append("bodies read: %d, from %s"
                 % (len(bodies), CALLEE_UNITS))
    lines.append("archives: %s"
                 % json.dumps(meta.get("location_record", {})
                              .get("archive_paths", {}),
                              sort_keys=True))
    lines.append("")
    lines.append("%-72s %-4s %s" % ("callee arch unit", "n",
                                    "families changed / refusal"))
    refused = 0
    with_x87 = 0
    disagree = []
    for key in sorted(readings):
        reading = readings[key]
        if reading.get("refuse"):
            refused = refused + 1
            lines.append("%-72s %-4s REFUSE:%s"
                         % (key, reading.get("instruction_count"),
                            reading["refuse"]))
            continue
        if reading.get("x87"):
            with_x87 = with_x87 + 1
        text = ",".join(reading["families"])
        if reading.get("x87"):
            text = text + " +x87"
        lines.append("%-72s %-4s %s"
                     % (key, reading.get("instruction_count"), text))
        if not cross_check(reading):
            disagree.append(key)
    lines.append("")
    lines.append("readings made: %d   refused by name: %d   "
                 "leaving a value on the x87 stack: %d"
                 % (len(readings) - refused, refused, with_x87))
    lines.append("")
    lines.append("CROSS-CHECK, reported and never used: the reading "
                 "names at least one of the stated calling "
                 "convention's answer homes")
    lines.append("  bodies whose reading names none of %s: %d %s"
                 % (str(CROSS_CHECK_HOMES), len(disagree),
                    ("-- " + ", ".join(disagree)) if disagree else ""))
    text = "\n".join(lines) + "\n"
    handle = open(os.path.join(HERE, OUT_TEXT), "w")
    handle.write(text)
    handle.close()
    document = {
        "meta": {
            "generated_by": "runtime_answers78.py",
            "node": "hq.research.compiler_graph.ledger."
                    "destination_rules",
            "rule": "CORE_0_3_5_3_3_destination_rules.md, the settled "
                    "rule 'THE ANSWER REGISTERS ARE READ OFF THE "
                    "ATTACHED CALLEE'S BODY'",
            "read_from": CALLEE_UNITS,
            "bodies": len(bodies),
            "refused": refused,
        },
        "readings": readings,
    }
    handle = open(os.path.join(HERE, OUT_JSON), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
