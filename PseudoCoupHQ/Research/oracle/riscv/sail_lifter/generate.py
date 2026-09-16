#!/usr/bin/env python3
"""generate.py -- THE GENERATOR OF THE RISC-V LIFTER'S TABLE FROM THE SAIL
MODEL (task sl1).

Node: hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_0_lifter_from_sail/CORE_0_3_2_3_1_0_lifter_from_sail.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_sl1_brief.md`.

WHAT THIS FILE IS, one sentence, in relation: the tool that turns the
Sail model's own `execute` clauses into the lifter's table -- one z3
formula per written register per instruction -- so that
`riscv_reference.py` looks its definitions up instead of holding rows a
person typed.

HOW, in one paragraph.  Stage 1 SCANS the model's source for three
things it declares in a fixed syntax: the constructors of the
`instruction` union with their field types, the count of integer and
floating-point registers, and nothing else.  Stage 2 WRITES one Sail
`$property` per constructor whose arguments are the constructor's own
fields (every one symbolic, the enum-typed and the register-index-typed
included) and whose body runs `execute` and compares the whole register
file with an oracle argument; a second property per constructor does
the same with `encdec`, the model's own encoding.  Stage 3 RUNS Sail's
own SMT backend over the model plus that file.  Stage 4 READS the SMT2
back with z3 and takes, per constructor, the term of every register
that can differ from its initial value, and the term of the encoding.
No stage names an instruction: a constructor name is data read off
the model, carried through, and displayed.

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

HOW THIS FILE OBEYS IT: the table's rows are keyed by the model's own
constructor and the concrete values of its fields -- machine form read
off the instruction WORD -- and the mnemonic is carried in the field
`mnem` as a display label only.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  generate.py scan  <model dir>                       (stage 1, prints)
  generate.py props <model copy dir> [<first N>]      (stages 1-2, writes
                                                      sl1_props.sail and
                                                      the project module)
"""
import json
import os
import re
import sys

CLAUSE = re.compile(
    r"^\s*union clause instruction\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
INTEGER_REGISTER = re.compile(r"^\s*register\s+x(\d+)\s*:\s*regtype")
FLOAT_REGISTER = re.compile(r"^\s*register\s+f(\d+)\s*:\s*fregtype")
FIELD_PREFIX = "sl1arg"


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def sail_files(model_dir):
    out = []
    for root, _dirs, files in os.walk(model_dir):
        for name in sorted(files):
            if name.endswith(".sail"):
                out.append(os.path.join(root, name))
    return sorted(out)


def split_top_level(text):
    """split on the commas at depth zero of parentheses."""
    out = []
    depth = 0
    current = ""
    for char in text:
        if char == "(":
            depth = depth + 1
        if char == ")":
            depth = depth - 1
        if char == "," and depth == 0:
            out.append(current.strip())
            current = ""
            continue
        current = current + char
    if current.strip():
        out.append(current.strip())
    return out


def field_types_of(text):
    """the field types of one constructor, from the text after its colon:
    a tuple `(T1, ..., Tn)`, the unit type, or one bare type."""
    text = text.strip()
    if text == "unit":
        return []
    if text.startswith("(") and text.endswith(")"):
        inner = text[1:-1]
        parts = split_top_level(inner)
        if len(parts) > 1:
            return parts
        return [inner.strip()]
    return [text]


def scan(model_dir):
    """(constructors in source order, integer register count, float
    register count).  A constructor is (name, [field types], file)."""
    constructors = []
    seen = set()
    integer_count = 0
    float_count = 0
    for path in sail_files(model_dir):
        for line in open(path):
            hit = CLAUSE.match(line)
            if hit is not None:
                name = hit.group(1)
                if name in seen:
                    continue
                seen.add(name)
                constructors.append((name, field_types_of(hit.group(2)),
                                     os.path.relpath(path, model_dir)))
                continue
            if INTEGER_REGISTER.match(line):
                integer_count = integer_count + 1
                continue
            if FLOAT_REGISTER.match(line):
                float_count = float_count + 1
    return constructors, integer_count, float_count


def property_text(name, types, integer_count, float_count):
    args = []
    fields = []
    for index, kind in enumerate(types):
        args.append("%s%d : %s" % (FIELD_PREFIX, index, kind))
        fields.append("%s%d" % (FIELD_PREFIX, index))
    signature = ", ".join(args)
    if signature:
        signature = signature + ", "
    call = "%s(%s)" % (name, ", ".join(fields))
    if not fields:
        call = "%s()" % name
    reads = []
    for k in range(1, integer_count + 1):
        reads.append("rX(Regno(%d))" % k)
    width = 64 * integer_count
    lines = []
    lines.append("$property")
    lines.append("function sl1_exec_%s(%soracle : bits(%d)) -> bool = {"
                 % (name, signature, width))
    lines.append("  let _ = execute(%s);" % call)
    lines.append("  (%s) == oracle" % " @ ".join(reads))
    lines.append("}")
    lines.append("")
    lines.append("$property")
    lines.append("function sl1_enc_%s(%soracle : bits(32)) -> bool = "
                 "encdec(%s) == oracle" % (name, signature, call))
    lines.append("")
    return "\n".join(lines)


def write_props(model_dir, constructors, integer_count, float_count):
    text = ["// written by generate.py (task sl1), never by hand", ""]
    for name, types, _path in constructors:
        text.append(property_text(name, types, integer_count, float_count))
    target = os.path.join(model_dir, "sl1_props.sail")
    open(target, "w").write("\n".join(text))
    project = os.path.join(model_dir, "riscv.sail_project")
    original = open(project).read()
    if "sl1_props {" in original:
        return target
    top = re.findall(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\{", original, re.M)
    module = ("\nsl1_props {\n  requires %s\n  files sl1_props.sail\n}\n"
              % ", ".join(top))
    open(project, "w").write(original + module)
    return target


def scan_command(model_dir):
    constructors, integer_count, float_count = scan(model_dir)
    say("constructors: %d" % len(constructors))
    say("integer registers: %d, float registers: %d"
        % (integer_count, float_count))
    by_file = {}
    for name, types, path in constructors:
        by_file[path] = by_file.get(path, 0) + 1
    for path in sorted(by_file):
        say("  %4d  %s" % (by_file[path], path))
    for name, types, path in constructors:
        say("%s : (%s)   [%s]" % (name, ", ".join(types), path))
    return 0


def props_command(model_dir, first=None):
    constructors, integer_count, float_count = scan(model_dir)
    if first is not None:
        constructors = constructors[:first]
    target = write_props(model_dir, constructors, integer_count, float_count)
    say("wrote %s: %d constructors, %d properties"
        % (target, len(constructors), 2 * len(constructors)))
    return 0


def main():
    command = sys.argv[1]
    if command == "scan":
        return scan_command(sys.argv[2])
    if command == "props":
        first = None
        if len(sys.argv) > 3:
            first = int(sys.argv[3])
        return props_command(sys.argv[2], first)
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
