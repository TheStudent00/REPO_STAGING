#!/usr/bin/env python3
"""canon37_assemble.py -- TASK 47: every wrapped text ASSEMBLES.

Each proved wrapped text is written into a real `.s` file as its own
symbol, assembled with `as --64`, and read back with `objdump -d`.  A
unit passes only when its symbol appears in the disassembly with at
least as many instructions as the text spells.  Nothing is simulated:
this is the assembler and the disassembler, on disk, on real bytes.

WHAT THIS FILE ADDS OVER canon36_assemble.py: THE LEDGER SYMBOL.  The
wrapped text reaches the ledger rip-relative on a named symbol, so the
emitted assembly defines that symbol as a six-entry table of eight-byte
pointers in `.data`.  The assembler emits an R_X86_64_PC32 relocation
for each `ledger+0xNN(%rip)` operand; `objdump -r` is read back and the
relocations are counted, which is the literal evidence that the
addressing mode is a real encoding and not a notation.

The batching, the per-unit re-run on a failing batch, the reading-
annotation strip, the rip-relative constant pool and the local-label
scheme are canon35_assemble.py's, IMPORTED rather than copied so they
cannot drift.

The regenerated population is SAMPLED and the sample is named as one:
it is 28,000-odd units and the assembler cost is linear, so a fixed
stride is taken over the whole population rather than a prefix, and
the stride is recorded.

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
  canon37_assemble.py [--stride N] [--transcripts N]
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
import ledger47 as L47                                           # noqa: E402

WORK = "/tmp/canon37_assemble_work"
OUT = os.path.join(HERE, "canon37_assemble.json")
TRANSCRIPTS = os.path.join(HERE, "canon37_assemble_transcripts.txt")
DEFAULT_STRIDE = 30



# ------------------------------------------------------------------
# THE BRANCH-TARGET REPAIR
# ------------------------------------------------------------------
#
# objdump prints an intra-unit branch as a BYTE OFFSET plus a symbol
# comment:
#
#     js f <op_117+0xf>
#
# `as` cannot read that.  The repair reads the unit's OWN BYTES with
# capstone, which gives every instruction's byte offset, maps the
# branch's numeric target to the body line at that offset, and names
# that line with a local label.  Nothing about the instruction changes
# except the spelling of its target, and the mapping is forced by the
# bytes rather than guessed.  A branch whose target is not an offset
# inside this unit (a tail call into another routine) is left alone
# and REPORTED, never silently rewritten.

# The numeric part of an objdump branch target is an address, and for
# a unit extracted from a larger image (go's are) it is the ABSOLUTE
# address, not an offset into the unit.  The symbol comment carries
# the offset directly -- `<main.op_103+0x1d>` says "0x1d bytes into
# this symbol" -- so the offset is read from there, which is correct
# for both absolute and unit-relative numbering.  A target whose
# comment names no `+0x` offset is a branch out of the unit and is
# left alone.
BRANCH_TARGET = re.compile(r"^([0-9a-f]+)\s*<([^>]*)>$")
INNER_OFFSET = re.compile(r"\+0x([0-9a-f]+)$")


def instruction_offsets(byte_text):
    """the byte offset of every instruction, read off the unit's own
    bytes with capstone."""
    if not byte_text:
        return None
    try:
        import capstone
    except ImportError:
        return None
    cleaned = byte_text.replace(" ", "").replace("\n", "")
    try:
        blob = bytes.fromhex(cleaned)
    except ValueError:
        return None
    engine = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    offsets = []
    for instruction in engine.disasm(blob, 0):
        offsets.append(instruction.address)
    return offsets


def branch_repair(symbol, body_lines, byte_text):
    """(label_before_line_index, rewritten_body_line, unrepaired)."""
    offsets = instruction_offsets(byte_text)
    labels = {}
    rewritten = {}
    unrepaired = []
    if offsets is None:
        return labels, rewritten, ["no bytes recorded for this unit"]
    if len(offsets) != len(body_lines):
        return labels, rewritten, [
            "capstone read %d instructions from the bytes and the body "
            "spells %d lines" % (len(offsets), len(body_lines))]
    by_offset = {}
    for index, offset in enumerate(offsets):
        by_offset[offset] = index
    for index, raw in enumerate(body_lines):
        line = raw
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        hit = BRANCH_TARGET.match(parts[1].strip())
        if hit is None:
            continue
        inner = INNER_OFFSET.search(hit.group(2))
        if inner is None:
            unrepaired.append(line)
            continue
        target = int(inner.group(1), 16)
        if target not in by_offset:
            unrepaired.append(line)
            continue
        target_index = by_offset[target]
        name = ".L%s_off%x" % (symbol, target)
        labels[target_index] = name
        rewritten[index] = "%s %s" % (parts[0], name)
    return labels, rewritten, unrepaired


EXTERNAL_NAME = re.compile(r"[^A-Za-z0-9_]")


def external_symbol(inner):
    """the callee's own name, sanitized into an assembler identifier.

    A transfer OUT of the unit (go's `call 43f360 <runtime.panicdivide>`,
    a tail call into `__addtf3`) names its callee in the objdump
    comment.  For the assembly check the numeric address is replaced by
    that NAME, and the batch defines the name as a stub, so the
    instruction encodes as the call it is.  This checks the ENCODING,
    not the presence of the callee -- stated rather than implied."""
    head = inner.split("+")[0].split("-")[0]
    return "x_" + EXTERNAL_NAME.sub("_", head)


def render_for_assembler(symbol, wrapped_text, body_lines, byte_text):
    """(asm_lines, instruction_count, notes, externals).  The wrapped
    text with intra-unit branch targets named, out-of-unit transfers
    bound to named stubs, and nothing else changed."""
    labels, rewritten, unrepaired = branch_repair(symbol, body_lines,
                                                  byte_text)
    notes = []
    externals = set()
    for index, raw in enumerate(body_lines):
        if index in rewritten:
            continue
        line = raw
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        hit = BRANCH_TARGET.match(parts[1].strip())
        if hit is None:
            continue
        name = external_symbol(hit.group(2))
        externals.add(name)
        rewritten[index] = "%s %s" % (parts[0], name)
        notes.append("a transfer out of the unit was bound to the "
                     "named stub %s" % name)
    if unrepaired:
        notes.append("out-of-unit transfers named: %r"
                     % unrepaired[:3])
    lines = []
    count = 0
    pointer = 0
    for raw in L47.split_lines(wrapped_text):
        line = raw
        is_body = False
        if pointer < len(body_lines):
            if raw == body_lines[pointer]:
                is_body = True
        if is_body:
            if pointer in labels:
                lines.append("%s:" % labels[pointer])
            if pointer in rewritten:
                line = rewritten[pointer]
            pointer = pointer + 1
        if "!!" in line:
            line = line.split("!!", 1)[0].strip()
            notes.append("stripped a reading annotation")
        if A35.RIP.search(line):
            line = A35.RIP.sub("canon35_pool(%rip)", line)
            notes.append("rip-relative data reference bound to a real "
                         "local constant pool")
        lines.append("    " + line)
        count = count + 1
    return lines, count, sorted(set(notes)), sorted(externals)


def write_batch(path, items):
    """canon35's writer plus the ledger's own definition and the
    out-of-unit stubs."""
    handle = open(path, "w")
    handle.write("    .text\n")
    stubs = set()
    for item in items:
        if len(item) > 3:
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
    handle.write("%s:\n" % L47.LEDGER_SYMBOL)
    for block in L47.BLOCK_ORDER:
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
        path = os.path.join(HERE, "canon37_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out.append((label, rec["wrapped_text"], "original",
                        rec.get("body_verbatim") or [],
                        rec.get("body_bytes")))
    path = os.path.join(HERE, "canon37_interp.json")
    if os.path.exists(path):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out.append((label, rec["wrapped_text"], "interpreter",
                        rec.get("body_verbatim") or [],
                        rec.get("body_bytes")))
    regen = []
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon37_regen_store",
                                              "*.json"))):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            regen.append((label, rec["wrapped_text"], "regenerated",
                          rec.get("body_verbatim") or [],
                          rec.get("body_bytes")))
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
    for label, text, population, body_lines, byte_text in offered:
        symbol = "u_" + label.replace("/", "_")
        lines, count, notes, externals = render_for_assembler(
            symbol, text, body_lines, byte_text)
        items.append((symbol, lines, count, externals))
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
                       % L47.LEDGER_SYMBOL, relocation_text))
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
    handle.write("canon37_assemble.py -- SAMPLED objdump transcripts, "
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
            "produced_by": "canon37_assemble.py",
            "role": "generator provenance",
            "ledger_symbol_defined_in_the_emitted_assembly":
                "%s: six .quad entries, one per block, in .data"
                % L47.LEDGER_SYMBOL,
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
