#!/usr/bin/env python3
"""probe80_conditional_shapes.py -- READ THE CONDITIONAL TEMPLATE OFF
THE CORPUS, before any template is written.

TASK 80's first instruction: "READ THE SHAPE OFF THE CORPUS -- the
units whose own ship bodies compute a conditional (compare then
`set<cc>`, or compare then `cmov<cc>`) show what the machine actually
does; take the template from them, do not invent one."

So this file MEASURES, it does not render.  It walks the same 332
canon39 shards `term61_run.shards()` names, one shard at a time, and
tallies, over the units whose own ship body spells a `set<cc>` or a
`cmov<cc>`:

  * the flag-setting arch opcode that precedes the conditional read,
    and how many lines back it sits;
  * the instruction window the machine writes around it, with the
    register names replaced by their POSITION in the window, so two
    units that wrote the same shape in different registers count as
    one shape;
  * the answer width the conditional read leaves, and what the body
    does to it afterwards (the widening).

MEMORY BOUND: one shard is read, tallied and dropped before the next
is opened; the tallies are counters over short strings.  The largest
shard on disk is under 5 MB.  Bound stated: 2 GB resident, with a
named abort (`ABORT_MEMORY`) if the process passes it.

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

Every grouping below is keyed by MACHINE FORM -- arch mnemonics and
positions in a window of instructions.  The `operator` field of a unit
record is never read by this file.

Coding discipline: no compound one-liner statements.
"""

import collections
import json
import os
import re
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table as CT                                     # noqa: E402
import term61_run as D                                           # noqa: E402

MEMORY_CAP_KB = 2 * 1024 * 1024
OUT = os.path.join(HERE, "probe80_conditional_shapes.json")
PRINTED = os.path.join(HERE, "probe80_conditional_shapes_printed.txt")

MNEM = re.compile(r"^([a-z][a-z0-9]*)")
REGISTER = re.compile(r"%[a-z0-9]+")


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY: peak resident %d kB passed the stated cap "
            "of %d kB" % (used, MEMORY_CAP_KB))
    return used


def mnemonic_of(line):
    found = MNEM.match(line.strip())
    if found is None:
        return None
    return found.group(1)


def is_conditional_read(mnemonic):
    """`set<cc>` or `cmov<cc>` -- a flag read that WRITES a place, so
    the value it leaves is part of the computation.  `j<cc>` writes no
    place; the walk's fork handles it and it is counted separately."""
    for prefix in ("set", "cmov"):
        if not mnemonic.startswith(prefix):
            continue
        suffix = mnemonic[len(prefix):]
        if suffix in CT.SUFFIX_TO_COND:
            return prefix, suffix
    return None, None


def is_branch(mnemonic):
    if not mnemonic.startswith("j"):
        return None
    suffix = mnemonic[1:]
    if suffix in CT.SUFFIX_TO_COND:
        return suffix
    return None


def shape_of(window):
    """the window with every register replaced by the position it
    first appeared at, so `cmp %rsi,%rdi; cmovl %rsi,%rdi` and
    `cmp %ecx,%edx; cmovl %ecx,%edx` are ONE shape."""
    seen = {}
    out = []
    for line in window:
        pieces = []
        position = 0
        for match in REGISTER.finditer(line):
            name = match.group(0)
            if name not in seen:
                seen[name] = "<%d>" % len(seen)
            pieces.append((match.start(), match.end(), seen[name]))
        rebuilt = line
        for start, end, replacement in reversed(pieces):
            rebuilt = rebuilt[:start] + replacement + rebuilt[end:]
        out.append(rebuilt)
        position = position + 1
    return "; ".join(out)


def walk_one_unit(name, unit, tallies):
    body = unit.get("body_verbatim") or []
    mnemonics = []
    for line in body:
        mnemonics.append(mnemonic_of(line))
    saw = False
    for index, mnemonic in enumerate(mnemonics):
        if mnemonic is None:
            continue
        prefix, suffix = is_conditional_read(mnemonic)
        if prefix is None:
            continue
        saw = True
        setter_index = None
        for back in range(index - 1, -1, -1):
            if mnemonics[back] in CT.FLAGSETTER_MNEMONICS:
                setter_index = back
                break
        if setter_index is None:
            tallies["no_setter"][prefix] += 1
            continue
        distance = index - setter_index
        tallies["distance"][(prefix, distance)] += 1
        tallies["setter"][(prefix, mnemonics[setter_index])] += 1
        window = body[setter_index:index + 1]
        tallies["shape"][shape_of(window)] += 1
        after = body[index + 1:index + 3]
        tallies["after"][shape_of(after)] += 1
        tallies["suffix"][suffix] += 1
    for index, mnemonic in enumerate(mnemonics):
        if mnemonic is None:
            continue
        suffix = is_branch(mnemonic)
        if suffix is None:
            continue
        saw = True
        tallies["branch_suffix"][suffix] += 1
    if saw:
        tallies["units"][unit.get("lang")] += 1
    return saw


def run():
    tallies = {
        "units": collections.Counter(),
        "shape": collections.Counter(),
        "after": collections.Counter(),
        "setter": collections.Counter(),
        "distance": collections.Counter(),
        "suffix": collections.Counter(),
        "branch_suffix": collections.Counter(),
        "no_setter": collections.Counter(),
    }
    total = 0
    for path in D.shards():
        document = json.load(open(path))
        for name in sorted(document.get("units", {})):
            unit = document["units"][name]
            total = total + 1
            walk_one_unit(name, unit, tallies)
        document = None
        check_memory()
    peak = check_memory()
    return tallies, total, peak


def printable(tallies, total, peak):
    lines = []
    lines.append("probe80 -- the conditional shape, read off the "
                 "corpus's own ship bodies")
    lines.append("")
    lines.append("population: %d units over the 332 canon39 shards"
                 % total)
    lines.append("peak resident: %d kB (stated cap %d kB)"
                 % (peak, MEMORY_CAP_KB))
    lines.append("")
    lines.append("units whose own ship body spells a flag-reading "
                 "arch opcode, by language:")
    for lang in sorted(tallies["units"]):
        lines.append("  %-8s %6d" % (lang, tallies["units"][lang]))
    lines.append("")
    lines.append("the flag-setting arch opcode the read binds to:")
    for key in sorted(tallies["setter"],
                      key=lambda one: -tallies["setter"][one]):
        lines.append("  %-6s after %-10s %7d"
                     % (key[0], key[1], tallies["setter"][key]))
    lines.append("")
    lines.append("how many lines back that setter sits:")
    for key in sorted(tallies["distance"]):
        lines.append("  %-6s %2d lines back %7d"
                     % (key[0], key[1], tallies["distance"][key]))
    lines.append("")
    lines.append("condition suffixes on the flag READ (set/cmov):")
    for key in sorted(tallies["suffix"],
                      key=lambda one: -tallies["suffix"][one]):
        lines.append("  %-4s %7d" % (key, tallies["suffix"][key]))
    lines.append("")
    lines.append("condition suffixes on a conditional TRANSFER:")
    for key in sorted(tallies["branch_suffix"],
                      key=lambda one: -tallies["branch_suffix"][key]
                      if False else -tallies["branch_suffix"][key]):
        lines.append("  %-4s %7d"
                     % (key, tallies["branch_suffix"][key]))
    lines.append("")
    lines.append("THE SHAPE ITSELF -- setter through read, registers "
                 "replaced by first-appearance position.")
    lines.append("the 30 most frequent, of %d distinct:"
                 % len(tallies["shape"]))
    ordered = sorted(tallies["shape"],
                     key=lambda one: -tallies["shape"][one])
    for shape in ordered[:30]:
        lines.append("  %7d  %s" % (tallies["shape"][shape], shape))
    lines.append("")
    lines.append("WHAT FOLLOWS THE READ -- the next two lines, same "
                 "replacement.  the 20 most frequent, of %d distinct:"
                 % len(tallies["after"]))
    ordered = sorted(tallies["after"],
                     key=lambda one: -tallies["after"][one])
    for shape in ordered[:20]:
        lines.append("  %7d  %s" % (tallies["after"][shape], shape))
    lines.append("")
    lines.append("flag reads with no flag setter before them in the "
                 "same body: %d"
                 % sum(tallies["no_setter"].values()))
    return "\n".join(lines)


def as_document(tallies, total, peak):
    out = {
        "what": "the conditional shape read off the corpus's own "
                "ship bodies, before any template is written",
        "population_units_walked": total,
        "peak_resident_kb": peak,
        "memory_cap_kb": MEMORY_CAP_KB,
    }
    for key in tallies:
        rows = []
        for item in sorted(tallies[key],
                           key=lambda one: -tallies[key][one]):
            if isinstance(item, tuple):
                shown = list(item)
            else:
                shown = item
            rows.append({"machine_form": shown,
                         "count": tallies[key][item]})
        out[key] = rows
    return out


if __name__ == "__main__":
    tallies, total, peak = run()
    text = printable(tallies, total, peak)
    print(text)
    handle = open(PRINTED, "w")
    handle.write(text)
    handle.write("\n")
    handle.close()
    handle = open(OUT, "w")
    json.dump(as_document(tallies, total, peak), handle,
              indent=1, sort_keys=True)
    handle.close()
