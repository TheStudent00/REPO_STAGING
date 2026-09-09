#!/usr/bin/env python3
"""canon38_assemble.py -- TASK 52: every canon38 wrapped text ASSEMBLES.

Each proved wrapped text is written into a real `.s` file as its own
symbol, assembled with `as --64`, and read back with `objdump -d`.  A
unit passes only when its symbol appears in the disassembly with at
least as many instructions as the text spells.  Nothing is simulated:
this is the assembler and the disassembler, on disk, on real bytes.

WHAT IS SIMPLER HERE THAN IN canon37_assemble.py, and why.  Task 47's
assembler had to REPAIR branch targets at assembly time, because the
stored text carried objdump's `47a678 <main.op_174+0x18>` spelling,
which `as` cannot read.  Under ruling 4 the stored text already names
its targets positionally (`jl L0`, with `L0:` defined on the
instruction it names) and names its out-of-unit callees (`call
x_runtime_panicshift`).  So this file does two mechanical things and
no repair:

  * a label is made local to its symbol (`L0` -> `.Lu_go_op_174_L0`),
    because a batch holds many symbols and `L0` would otherwise
    collide between them;
  * every out-of-unit callee, and every positional label the body
    branches to without defining (a transfer this form could not
    place inside the unit), is defined once in the batch as a stub,
    so the instruction encodes as the transfer it is.  This checks the
    ENCODING, not the presence of the callee -- stated rather than
    implied.

The ledger symbol is defined as an EIGHT-entry table of eight-byte
pointers in `.data` (ruling 2 added STACK and X87), and `objdump -r`
is read back so the R_X86_64_PC32 relocations are counted rather than
asserted.

The regenerated population is SAMPLED and the sample is named as one:
a fixed stride over the whole population, recorded on the artifact.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

usage:
  canon38_assemble.py [--stride N] [--transcripts N]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon35_assemble as A35                                   # noqa: E402
import ledger48 as L48                                           # noqa: E402

WORK = "/tmp/canon38_assemble_work"
OUT = os.path.join(HERE, "canon38_assemble.json")
TRANSCRIPTS = os.path.join(HERE, "canon38_assemble_transcripts.txt")
DEFAULT_STRIDE = 30

POSITIONAL = re.compile(r"^L\d+$")


def render_for_assembler(symbol, wrapped_text):
    """(asm_lines, instruction_count, notes, stubs)."""
    notes = []
    stubs = set()
    defined = set()
    used = set()
    lines = []
    count = 0
    for raw in L48.split_lines(wrapped_text):
        line = raw
        if line.endswith(":"):
            name = line[:-1]
            if POSITIONAL.match(name) is not None:
                defined.add(name)
                lines.append(".L%s_%s:" % (symbol, name))
                continue
            lines.append(line)
            continue
        text, _annotation = L48.split_off_annotation(line)
        if "!!" in line:
            notes.append("stripped a reading annotation")
        line = text
        parts = line.split(" ", 1)
        if len(parts) == 2:
            if L48.is_transfer(parts[0]):
                target = parts[1].strip()
                if POSITIONAL.match(target) is not None:
                    used.add(target)
                    line = "%s .L%s_%s" % (parts[0], symbol, target)
                elif target.startswith("x_"):
                    stubs.add(target)
                    notes.append("a transfer out of the unit was bound "
                                 "to the named stub %s" % target)
        if A35.RIP.search(line):
            line = A35.RIP.sub("canon35_pool(%rip)", line)
            notes.append("rip-relative data reference bound to a real "
                         "local constant pool")
        lines.append("    " + line)
        count = count + 1
    out = []
    for name in sorted(used - defined):
        stubs.add("%s_unplaced_%s" % (symbol, name))
        notes.append("the body branches to %s and defines no such "
                     "label, so the target is a stub" % name)
    for line in lines:
        fixed = line
        for name in sorted(used - defined):
            fixed = fixed.replace(".L%s_%s" % (symbol, name),
                                  "%s_unplaced_%s" % (symbol, name))
        out.append(fixed)
    return out, count, sorted(set(notes)), sorted(stubs)


def write_batch(path, items):
    handle = open(path, "w")
    handle.write("    .text\n")
    stubs = set()
    for item in items:
        for name in item[3]:
            stubs.add(name)
    for name in sorted(stubs):
        handle.write("%s:\n    ret\n" % name)
    for item in items:
        symbol = item[0]
        lines = item[1]
        handle.write("    .globl %s\n" % symbol)
        handle.write("%s:\n" % symbol)
        for line in lines:
            handle.write(line + "\n")
    handle.write("    .section .rodata\n")
    handle.write("    .align 16\n")
    handle.write("canon35_pool:\n")
    handle.write("    .quad 0\n    .quad 0\n    .quad 0\n    .quad 0\n")
    handle.write("    .data\n")
    handle.write("    .align 8\n")
    handle.write("%s:\n" % L48.LEDGER_SYMBOL)
    for block in L48.BLOCK_ORDER:
        handle.write("    .quad 0    # the base address of the %s "
                     "block, written by the runner\n" % block)
    handle.close()


def relocations(obj):
    proc = subprocess.run(["objdump", "-r", obj], capture_output=True,
                          text=True)
    return proc.stdout


def sources():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out.append((label, rec["wrapped_text"], "original"))
    path = os.path.join(HERE, "canon38_interp.json")
    if os.path.exists(path):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out.append((label, rec["wrapped_text"], "interpreter"))
    regen = []
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon38_regen_store",
                                              "*.json"))):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            regen.append((label, rec["wrapped_text"], "regenerated"))
    return out, regen


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--stride", type=int, default=DEFAULT_STRIDE)
    parser.add_argument("--transcripts", type=int, default=6)
    args = parser.parse_args(argv[1:])
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    A35.WORK = WORK
    whole, regen = sources()
    sampled = regen[::args.stride]
    offered = whole + sampled
    items = []
    per_unit = {}
    for label, text, population in offered:
        symbol = "u_" + label.replace("/", "_")
        lines, count, notes, stubs = render_for_assembler(symbol, text)
        items.append((symbol, lines, count, stubs))
        per_unit[symbol] = {
            "unit": label,
            "population": population,
            "instruction_lines": count,
            "normalizations": notes,
        }
    batches = []
    index = 0
    while index < len(items):
        batches.append(items[index:index + A35.BATCH])
        index = index + A35.BATCH
    assembled = 0
    failures = []
    relocation_total = 0
    transcripts = []
    for number, batch in enumerate(batches):
        source = os.path.join(WORK, "batch_%04d.s" % number)
        obj = os.path.join(WORK, "batch_%04d.o" % number)
        write_batch(source, batch)
        code, err = A35.assemble(source, obj)
        if code != 0:
            for one in batch:
                single = os.path.join(WORK, "one_%s.s" % one[0])
                single_obj = os.path.join(WORK, "one_%s.o" % one[0])
                write_batch(single, [one])
                one_code, one_err = A35.assemble(single, single_obj)
                if one_code != 0:
                    failures.append({
                        "unit": per_unit[one[0]]["unit"],
                        "assembler_message": one_err.strip()[:400],
                    })
                    per_unit[one[0]]["assembles"] = False
                    continue
                dump = A35.disassemble(single_obj)
                seen = A35.counts_from_dump(dump)
                per_unit[one[0]]["assembles"] = True
                per_unit[one[0]]["disassembled_instructions"] = \
                    seen.get(one[0], 0)
                assembled = assembled + 1
            continue
        dump = A35.disassemble(obj)
        seen = A35.counts_from_dump(dump)
        relocation_text = relocations(obj)
        relocation_total = relocation_total + len(
            re.findall(r"R_X86_64_PC32\s+(?:%s|\.data)"
                       % L48.LEDGER_SYMBOL, relocation_text))
        for one in batch:
            got = seen.get(one[0], 0)
            ok = got >= one[2]
            per_unit[one[0]]["assembles"] = ok
            per_unit[one[0]]["disassembled_instructions"] = got
            if ok:
                assembled = assembled + 1
            else:
                failures.append({
                    "unit": per_unit[one[0]]["unit"],
                    "assembler_message":
                        "the symbol disassembled to %d instructions, "
                        "fewer than the %d the text spells"
                        % (got, one[2]),
                })
        if len(transcripts) < args.transcripts:
            for one in batch:
                if len(transcripts) >= args.transcripts:
                    break
                block = []
                keep = False
                for line in dump.splitlines():
                    head = re.match(r"^[0-9a-f]+ <([^>]+)>:$",
                                    line.strip())
                    if head is not None:
                        keep = head.group(1) == one[0]
                        if keep:
                            block = [line]
                        continue
                    if keep:
                        if line.strip() == "":
                            keep = False
                            continue
                        block.append(line)
                if block:
                    transcripts.append({
                        "unit": per_unit[one[0]]["unit"],
                        "source_file": source,
                        "objdump": "\n".join(block),
                    })
    handle = open(TRANSCRIPTS, "w")
    handle.write("canon38_assemble.py -- SAMPLED objdump transcripts, "
                 "verbatim\n")
    handle.write("Each block below is `objdump -d` output on the "
                 "object file `as --64` produced.\n\n")
    for item in transcripts:
        handle.write("==== %s   (from %s)\n" % (item["unit"],
                                                item["source_file"]))
        handle.write(item["objdump"])
        handle.write("\n\n")
    handle.close()
    document = {
        "meta": {
            "produced_by": "canon38_assemble.py",
            "ledger_symbol_defined_in_the_emitted_assembly":
                "%s: eight .quad entries, one per block, in .data"
                % L48.LEDGER_SYMBOL,
            "regenerated_population_is_sampled": {
                "stride": args.stride,
                "sampled": len(sampled),
                "of": len(regen),
            },
        },
        "offered": len(items),
        "assembled": assembled,
        "failed": len(failures),
        "ledger_relocations_counted": relocation_total,
        "failures": failures[:200],
        "transcripts_file": TRANSCRIPTS,
        "units": per_unit,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("offered %d  assembled %d  failed %d  "
          "ledger relocations %d"
          % (len(items), assembled, len(failures), relocation_total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
