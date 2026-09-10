#!/usr/bin/env python3
"""check_no_task_gates.py -- the mechanical guard that no rule in the
driver is keyed on a TASK NAME or on an OPCODE NAME.

WHAT IT IS, one sentence: a checker that parses a python file and
reports every branch whose condition compares against a string literal
that is a task label or an arch mnemonic, so "the gates are gone" is a
measurement of the code rather than a claim about it.

WHY IT EXISTS.  The loop's driver carried nine `use_task_*` entries and
three switches that answered by naming the tasks that set them, so which
contract rules applied to a run depended on the NAME of the task asking
(`DevComms/log_253` SS13, decided item 6, is the last reading of it).
The rules are now unconditional and provenance is `code_version` -- the
sha256 of the driver's own source and of the target's renderer, recorded
on every certificate.  This program is how that stays true.

WHAT COUNTS AS A GATE, stated so the answer is not a matter of reading:
  * a call of a name beginning `use_task_`, or of one of the three
    switch names the driver used to carry;
  * a comparison (`==`, `!=`, `in`, `not in`) against a string literal
    that is a TASK LABEL -- a letter-prefix-plus-number label of the
    form `h1`, `g1b`, `ap5`, `ex2`, `o13`, `bank1`, `hub2`;
  * a comparison against a string literal that is an ARCH MNEMONIC of
    the model table's own vocabulary, read off the cells file the
    caller names and never spelled here.
A comparison inside a COMMENT or a docstring is not a rule and is not
counted; the checker walks the syntax tree, so prose naming the reading
a rule came from is invisible to it, which is the intended reading.

THE ONE EXPECTED HIT is task o2's own chaff rule, which names the return
instruction: a body's last instruction is chaff by the corpus's own
narrow rule, and that is the ruling of 2026-09-07 restated, not a rule
about a cell.  It is reported like any other and named in the tally.

THE SPELLING BAN, and how this program obeys it: the mnemonic
vocabulary is READ from the cells file, never spelled here, and this
program groups nothing, pairs nothing and selects no candidate -- it
reports lines.

Coding discipline: no compound one-liner statements.

usage:
  check_no_task_gates.py <cells file> <python file> [<python file> ...]
"""

import ast
import json
import os
import re
import sys

TASK_LABEL = re.compile(r"^(h|hb|g|ap|ex|o|t|l|m|mn|hub|bank|pub)"
                        r"[0-9]+[a-z]?$")

SWITCH_NAMES = ["fixes_are_on", "primitive_first", "setup_is_allowed"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def chaff_vocabulary():
    """the mnemonics task o2's own narrow chaff rule names, read off
    that program rather than spelled here.

    They are not cells of the model table -- a return and a
    calling-convention move are chaff, which is why the cells file's own
    vocabulary does not carry them -- and a branch that names one is
    still a branch keyed on an opcode name, so the checker reads them
    too."""
    here = os.path.dirname(os.path.abspath(__file__))
    arch = os.path.normpath(os.path.join(here, "..", "..",
                                         "arch_opcodes"))
    if arch not in sys.path:
        sys.path.insert(0, arch)
    import single_opcode_units as SOU
    return set(SOU.NARROW_BARE) | set(SOU.NARROW_PURE_MOVE) | set(
        SOU.WIDTH_CHANGE)


def mnemonics(path):
    """the arch mnemonic vocabulary, off the cells file's own machine
    form: every `mnem` field it carries."""
    handle = open(path)
    document = json.load(handle)
    handle.close()
    out = set()
    for record in document.get("asked") or []:
        out.add(record["asked"]["mnem"])
        for row in record.get("rows") or []:
            out.add(row["mnem"])
            continue
        continue
    for row in document.get("setter_rows") or []:
        out.add(row["mnem"])
        continue
    return out


def literals_of(node):
    """every string literal a comparison names."""
    out = []
    for part in ast.walk(node):
        if isinstance(part, ast.Constant) and isinstance(part.value, str):
            out.append(part.value)
            continue
        continue
    return out


def gates_in(path, vocabulary):
    """every gate in one file, as records."""
    handle = open(path)
    source = handle.read()
    handle.close()
    tree = ast.parse(source)
    lines = source.split("\n")
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            if isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name is None:
                continue
            if name.startswith("use_task_") or name in SWITCH_NAMES:
                out.append({"line": node.lineno, "kind": "a task entry",
                            "what": name,
                            "text": lines[node.lineno - 1].strip()})
            continue
        if not isinstance(node, ast.Compare):
            continue
        for value in literals_of(node):
            if TASK_LABEL.match(value):
                out.append({"line": node.lineno,
                            "kind": "a task label",
                            "what": value,
                            "text": lines[node.lineno - 1].strip()})
                continue
            if value in vocabulary:
                out.append({"line": node.lineno,
                            "kind": "an opcode name",
                            "what": value,
                            "text": lines[node.lineno - 1].strip()})
            continue
        continue
    return out


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    vocabulary = mnemonics(argv[0]) | chaff_vocabulary()
    say("the arch mnemonic vocabulary: %d tokens, read off %s and off "
        "task o2's own chaff tables"
        % (len(vocabulary), os.path.basename(argv[0])))
    say("")
    say("| file | line | what is compared | kind | the line |")
    say("|---|---|---|---|---|")
    counted = {}
    for path in argv[1:]:
        for gate in gates_in(path, vocabulary):
            say("| %s | %d | `%s` | %s | `%s` |"
                % (os.path.basename(path), gate["line"], gate["what"],
                   gate["kind"], gate["text"].replace("|", "\\|")))
            counted[gate["kind"]] = counted.get(gate["kind"], 0) + 1
            continue
        continue
    say("")
    for kind in sorted(counted):
        say("%s: %d" % (kind, counted[kind]))
        continue
    task_gates = counted.get("a task label", 0) + counted.get(
        "a task entry", 0)
    say("task-name gates: %d" % task_gates)
    say("opcode-name branches: %d" % counted.get("an opcode name", 0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
