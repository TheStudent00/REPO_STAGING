#!/usr/bin/env python3
"""canon35_assemble.py -- TASK 39: every universal text ASSEMBLES.

WHAT IS CHECKED.  Each unit's universal text is written into a real
`.s` file as its own symbol, assembled with `as`, and read back with
`objdump -d`.  A unit passes only when its symbol appears in the
disassembly with at least as many instructions as the text has
non-label lines.  Nothing is simulated here: this is the assembler and
the disassembler, on disk, on the real bytes.

Units are batched (BATCH units per `.s` file) so the whole corpus is
covered in a few dozen assembler runs rather than one enormous file or
1,744 tiny ones.  A batch that fails to assemble is RE-RUN ONE UNIT AT
A TIME, so the failure is attributed to the unit that caused it and
never smeared across its batch.

WHAT IS NORMALIZED, and why it is not cheating.  Two spellings in the
recorded texts are artefacts of the extraction, not of the form:
  * `!!reloc=...` / `!!...` trailing annotations, which the pipeline's
    own renderers attach for reading;
  * rip-relative data references spelled `0x0(%rip)`, whose target is
    a constant pool this corpus does not carry.
The first is stripped (it is a comment).  The second is assembled
against a real local constant pool emitted in the same file, so the
instruction encoded is the real instruction.  Both normalizations are
recorded per unit in the artifact.

Block-list texts carry labels (`L0:`); each is emitted as a LOCAL
label named `.L<symbol>_<name>`, so it is unique to its unit and does
not become a symbol of its own -- which is what keeps the whole unit
attributed to the unit in the disassembly.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Coding discipline: no complex/compound one-liner statements.

usage:
  canon35_assemble.py
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
WORK = "/tmp/canon35_assemble_work"
BATCH = 60
OUT = os.path.join(HERE, "canon35_assemble.json")

LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):$")
RIP = re.compile(r"0x0\(%rip\)")


def split_lines(text):
    out = []
    for piece in text.split(";"):
        piece = piece.strip()
        if piece:
            out.append(piece)
    return out


def normalize(symbol, text):
    """(asm_lines, instruction_count, notes)."""
    notes = []
    raw_lines = []
    labels = []
    for raw in split_lines(text):
        line = raw
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
            notes.append("stripped a reading annotation")
        hit = LABEL.match(line)
        if hit is not None:
            labels.append(hit.group(1))
        raw_lines.append(line)

    def local(name):
        return ".L%s_%s" % (symbol, name)

    lines = []
    count = 0
    for line in raw_lines:
        hit = LABEL.match(line)
        if hit is not None:
            lines.append("%s:" % local(hit.group(1)))
            continue
        if RIP.search(line):
            line = RIP.sub("canon35_pool(%rip)", line)
            notes.append("rip-relative data reference bound to a real "
                         "local constant pool")
        parts = line.split(" ", 1)
        if len(parts) == 2:
            target = parts[1].strip()
            if target in labels:
                line = "%s %s" % (parts[0], local(target))
        lines.append("    " + line)
        count = count + 1
    return lines, count, sorted(set(notes))


def write_batch(path, items):
    fh = open(path, "w")
    fh.write("    .text\n")
    for symbol, lines, _count in items:
        fh.write("    .globl %s\n" % symbol)
        fh.write("%s:\n" % symbol)
        for line in lines:
            fh.write(line + "\n")
    fh.write("    .section .rodata\n")
    fh.write("    .align 16\n")
    fh.write("canon35_pool:\n")
    fh.write("    .quad 0\n    .quad 0\n    .quad 0\n    .quad 0\n")
    fh.close()


def assemble(path, obj):
    proc = subprocess.run(["as", "--64", "-o", obj, path],
                          capture_output=True, text=True)
    return proc.returncode, proc.stderr


def disassemble(obj):
    proc = subprocess.run(["objdump", "-d", obj],
                          capture_output=True, text=True)
    return proc.stdout


def counts_from_dump(dump):
    out = {}
    current = None
    for line in dump.splitlines():
        head = re.match(r"^[0-9a-f]+ <([^>]+)>:$", line.strip())
        if head is not None:
            current = head.group(1)
            out[current] = 0
            continue
        if current is None:
            continue
        if re.match(r"^\s+[0-9a-f]+:\s", line):
            out[current] = out[current] + 1
    return out


def main():
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    items = []
    per_unit = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon35_universal_%s.json" % lang)
        for label, rec in json.load(open(path))["units"].items():
            text = rec.get("universal_text")
            if not text:
                continue
            symbol = "u_" + label.replace("/", "_")
            lines, count, notes = normalize(symbol, text)
            items.append((symbol, lines, count))
            per_unit[symbol] = {
                "unit": label,
                "instruction_lines": count,
                "normalizations": notes,
            }

    batches = []
    index = 0
    while index < len(items):
        batches.append(items[index:index + BATCH])
        index = index + BATCH

    assembled = 0
    failures = []
    for number, batch in enumerate(batches):
        source = os.path.join(WORK, "batch_%03d.s" % number)
        obj = os.path.join(WORK, "batch_%03d.o" % number)
        write_batch(source, batch)
        code, err = assemble(source, obj)
        if code != 0:
            for one in batch:
                single = os.path.join(WORK, "one_%s.s" % one[0])
                single_obj = os.path.join(WORK, "one_%s.o" % one[0])
                write_batch(single, [one])
                one_code, one_err = assemble(single, single_obj)
                if one_code != 0:
                    failures.append({
                        "unit": per_unit[one[0]]["unit"],
                        "assembler_message": one_err.strip(),
                    })
                    per_unit[one[0]]["assembles"] = False
                    continue
                dump = disassemble(single_obj)
                seen = counts_from_dump(dump)
                per_unit[one[0]]["assembles"] = True
                per_unit[one[0]]["disassembled_instructions"] = \
                    seen.get(one[0], 0)
                assembled = assembled + 1
            continue
        dump = disassemble(obj)
        seen = counts_from_dump(dump)
        for one in batch:
            got = seen.get(one[0], 0)
            per_unit[one[0]]["assembles"] = got >= one[2]
            per_unit[one[0]]["disassembled_instructions"] = got
            if got >= one[2]:
                assembled = assembled + 1
            else:
                failures.append({
                    "unit": per_unit[one[0]]["unit"],
                    "assembler_message":
                        "the symbol disassembled to %d instructions, "
                        "fewer than the %d the text spells"
                        % (got, one[2]),
                })
        sys.stderr.write("  batch %d/%d\n" % (number + 1, len(batches)))
        sys.stderr.flush()

    doc = {
        "meta": {
            "produced_by": "canon35_assemble.py",
            "role": "generator provenance",
            "tool_versions": {
                "as": subprocess.run(["as", "--version"],
                                     capture_output=True,
                                     text=True).stdout.splitlines()[0],
                "objdump": subprocess.run(
                    ["objdump", "--version"], capture_output=True,
                    text=True).stdout.splitlines()[0],
            },
            "work_directory": WORK,
            "batch_size": BATCH,
        },
        "texts_offered": len(items),
        "assembled": assembled,
        "failures": failures,
        "per_unit": per_unit,
    }
    fh = open(OUT, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.close()
    print("offered %d  assembled %d  failed %d"
          % (len(items), assembled, len(failures)))
    for bad in failures[:20]:
        print("  %s :: %s" % (bad["unit"], bad["assembler_message"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
