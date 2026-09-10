#!/usr/bin/env python3
"""ref2_suffix_audit.py -- every arch mnemonic whose last letter is an AT&T
size letter, and whether that letter actually decides a width in this
reference, measured by running the builder both ways.

WHAT THIS IS, in relation.  `reference.Operands.width_at` gives a MEMORY
operand its width from the mnemonic's own last letter -- `movb`, `movl`,
`movq` -- unless the mnemonic sits in `reference.WIDTH_IS_NOT_A_SUFFIX`, in
which case the width comes from another operand of the same line, which states
its own.  Task ref1 found `sub` and `sbb` reading their `b` as a size, so
`sub %esi,(%rax)` was modelled at 8 bits; task ref2's correction 4 puts them in
that list and audits every other mnemonic the same rule reaches.

HOW THE AUDIT IS MEASURED, not argued.  For one mnemonic and one operand
spelling that carries a memory operand, the builder is run TWICE over one
machine state each: once with the mnemonic OUT of `WIDTH_IS_NOT_A_SUFFIX` (the
letter decides) and once with it IN (another operand decides).  The two runs'
written places are compared by their z3 s-expressions.  A mnemonic that READS
the flags is handed `model_translate.preseeded_state` rather than a fresh one,
because on a fresh state the reference refuses by name before the width rule
is reached and the run would say nothing about the letter.

  * identical on every shape -- the letter is NOT LOAD-BEARING here: either
    the builder never asks `width_at` for the memory slot, or the fallback
    gives the same number.  Nothing this task does to the list could change
    what this mnemonic computes.
  * different on some shape -- the letter DECIDES, and the row then carries
    both widths so the reading can be judged: the letter's own number, and
    the number the line's other operand states.

`sub` and `sbb` are the two the check found; every other row of this table is
recorded for the coordinator and nothing is decided about it here.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Coding discipline: no compound one-liner statements.

usage:
  ref2_suffix_audit.py <out.json>
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "op_pipeline"))
for _path in (PIPELINE, os.path.join(PIPELINE, "lean")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import z3                                                   # noqa: E402
import reference as R                                       # noqa: E402
import model_translate as MT                                # noqa: E402


def memory_shapes():
    """every operand spelling of the sweep that carries a memory
    operand, at every width the sweep tries."""
    out = []
    for width in MT.SWEEP_WIDTHS:
        for name, texts in MT.shapes_for(width):
            carries = False
            for text in texts:
                if text.startswith("(") or "(" in text:
                    carries = True
            if carries:
                out.append((name, width, list(texts)))
    return out


SEEDING_SETTER = "cmp"
"""THE FLAG STATE A CONSUMER NEEDS.  `adc` and `sbb` READ the carry, and on a
fresh machine state the reference refuses by name before the width rule is
reached -- so a run on a fresh state would say nothing about their size
letter.  The sweep's own answer to this is `model_translate.preseeded_state`,
which seeds the flags with a free pair under one setter; this audit uses it
for exactly the same reason, and the setter it names is the subtract family's,
which is the one every consumer here reads."""


def run_once(mnemonic, texts, in_the_list, width=None):
    """(the written places as text, the refusal) for one run with the
    mnemonic inside or outside `WIDTH_IS_NOT_A_SUFFIX`."""
    standing = R.WIDTH_IS_NOT_A_SUFFIX
    names = set(standing)
    if in_the_list:
        names.add(mnemonic)
    else:
        names.discard(mnemonic)
    R.WIDTH_IS_NOT_A_SUFFIX = frozenset(names)
    try:
        state = None
        entry = R.REFERENCE.opcode_table.entries.get(mnemonic)
        if entry is not None and R.FLAGS in entry.reads:
            state = MT.preseeded_state(width or 64, SEEDING_SETTER)
        written, flags, state, line = MT.run_line(mnemonic, texts,
                                                 state)
        places = {}
        for name in sorted(written):
            places[name] = written[name].sexpr()
        if flags is not None:
            places["flags:setter"] = str(flags[0])
            for index in (1, 2):
                if flags[index] is None:
                    continue
                places["flags:%d" % index] = flags[index].sexpr()
        return places, None
    except R.NotModeled as refusal:
        return None, str(refusal)
    except Exception as problem:                            # noqa: BLE001
        return None, "%s: %s" % (type(problem).__name__, problem)
    finally:
        R.WIDTH_IS_NOT_A_SUFFIX = standing


def width_both_ways(mnemonic, texts):
    """(the width the letter gives, the width another operand gives)
    for the memory slot of one line, or nothing where `width_at`
    refuses."""
    out = []
    for in_the_list in (False, True):
        standing = R.WIDTH_IS_NOT_A_SUFFIX
        names = set(standing)
        if in_the_list:
            names.add(mnemonic)
        else:
            names.discard(mnemonic)
        R.WIDTH_IS_NOT_A_SUFFIX = frozenset(names)
        try:
            state = R.MachineState()
            operands = R.Operands(state, mnemonic, list(texts))
            answer = None
            for index, text in enumerate(texts):
                if operands.is_memory(text) and not \
                        operands.is_rip(text):
                    answer = operands.width_at(index)
                    break
            out.append(answer)
        except Exception:                                   # noqa: BLE001
            out.append(None)
        finally:
            R.WIDTH_IS_NOT_A_SUFFIX = standing
    return out[0], out[1]


def audit_one(mnemonic):
    shapes = memory_shapes()
    reached = 0
    differing = []
    for name, width, texts in shapes:
        letter_places, letter_refusal = run_once(mnemonic, texts,
                                                 False, width)
        other_places, other_refusal = run_once(mnemonic, texts, True,
                                               width)
        if letter_places is None and other_places is None:
            if letter_refusal == other_refusal:
                continue
            reached = reached + 1
            differing.append({
                "shape": name, "sweep_width": width,
                "operands": list(texts),
                "letter_refusal": letter_refusal,
                "other_operand_refusal": other_refusal,
                "letter_width": None, "other_operand_width": None})
            continue
        if letter_places == other_places:
            reached = reached + 1
            continue
        reached = reached + 1
        letter_width, other_width = width_both_ways(mnemonic, texts)
        differing.append({
            "shape": name, "sweep_width": width,
            "operands": list(texts),
            "letter_width": letter_width,
            "other_operand_width": other_width,
            "letter_refusal": letter_refusal,
            "other_operand_refusal": other_refusal})
    return reached, differing


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    names = []
    for mnemonic in sorted(R.REFERENCE.opcode_table.entries):
        if mnemonic[-1:] not in R.SIZE_LETTER:
            continue
        entry = R.REFERENCE.opcode_table.entries[mnemonic]
        if entry.build is None:
            continue
        names.append(mnemonic)
    rows = []
    for mnemonic in names:
        reached, differing = audit_one(mnemonic)
        rows.append({
            "mnem": mnemonic,
            "last_letter": mnemonic[-1:],
            "width_the_letter_states": R.SIZE_LETTER[mnemonic[-1:]],
            "in_the_list_today": mnemonic in R.WIDTH_IS_NOT_A_SUFFIX,
            "memory_shapes_reached": reached,
            "shapes_where_the_letter_decides": len(differing),
            "differing": differing,
        })
    out = {"what": ("every arch mnemonic whose last letter is an AT&T "
                    "size letter, and whether that letter decides a "
                    "width in this reference, measured by running the "
                    "builder with the mnemonic inside and outside "
                    "reference.WIDTH_IS_NOT_A_SUFFIX"),
           "mnemonics": len(rows), "rows": rows}
    with open(argv[1], "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
    print("| `mnem` | letter | the letter's width | in the list today "
          "| memory shapes reached | shapes where the letter decides | "
          "the widths, letter vs other operand |")
    print("|---|---|---|---|---|---|---|")
    for row in rows:
        pairs = set()
        for entry in row["differing"]:
            pairs.add((entry["letter_width"],
                       entry["other_operand_width"]))
        text = ""
        for pair in sorted(pairs, key=str):
            text = text + "%s vs %s " % (pair[0], pair[1])
        print("| `%s` | %s | %d | %s | %d | %d | %s |"
              % (row["mnem"], row["last_letter"],
                 row["width_the_letter_states"],
                 "yes" if row["in_the_list_today"] else "no",
                 row["memory_shapes_reached"],
                 row["shapes_where_the_letter_decides"],
                 text.strip() or "-"))
    decides = [r for r in rows if r["shapes_where_the_letter_decides"]]
    print("")
    print("mnemonics whose last letter is a size letter: %d" % len(rows))
    print("of those, the letter DECIDES a width on at least one shape: "
          "%d" % len(decides))
    print("of those, in WIDTH_IS_NOT_A_SUFFIX today: %d"
          % len([r for r in decides if r["in_the_list_today"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
