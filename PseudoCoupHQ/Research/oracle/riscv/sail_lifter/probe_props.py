#!/usr/bin/env python3
"""probe_props.py -- task sl1's MEASUREMENT of route (a): write Sail
`$property` wrappers for the first K instruction constructors the model
declares, so `sail --smt` can be timed and its output looked at.

Nothing here names an instruction: the constructors are read off the
model's own `union clause instruction = NAME : (types)` lines in the order
the model writes them, and the K first are taken.

usage: probe_props.py <model dir (a writable copy)> <K> [<file to take them from>]
"""
import os
import re
import sys

CLAUSE = re.compile(r"^\s*union clause instruction\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\((.*)\)\s*$")
REGISTER = re.compile(r"^\s*register\s+x(\d+)\s*:\s*regtype")


def split_types(text):
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


def constructors_of(path):
    out = []
    for line in open(path):
        hit = CLAUSE.match(line)
        if hit is None:
            continue
        out.append((hit.group(1), split_types(hit.group(2))))
    return out


def integer_registers(model_dir):
    count = 0
    for root, _dirs, files in os.walk(model_dir):
        for name in files:
            if not name.endswith(".sail"):
                continue
            for line in open(os.path.join(root, name)):
                if REGISTER.match(line):
                    count = count + 1
    return count


def property_text(name, types, registers):
    args = []
    fields = []
    for index, kind in enumerate(types):
        args.append("sl1arg%d : %s" % (index, kind))
        fields.append("sl1arg%d" % index)
    reads = " @ ".join("rX(Regno(%d))" % k for k in range(1, registers + 1))
    lines = []
    lines.append("$property")
    lines.append("function sl1_exec_%s(%s, oracle : bits(%d)) -> bool = {"
                 % (name, ", ".join(args), 64 * registers))
    lines.append("  let _ = execute(%s(%s));" % (name, ", ".join(fields)))
    lines.append("  (%s) == oracle" % reads)
    lines.append("}")
    lines.append("")
    lines.append("$property")
    lines.append("function sl1_enc_%s(%s, oracle : bits(32)) -> bool = "
                 "encdec(%s(%s)) == oracle"
                 % (name, ", ".join(args), name, ", ".join(fields)))
    lines.append("")
    return "\n".join(lines)


def main():
    model_dir = sys.argv[1]
    count = int(sys.argv[2])
    source = sys.argv[3] if len(sys.argv) > 3 else \
        os.path.join(model_dir, "extensions", "I", "base_insts.sail")
    registers = integer_registers(model_dir)
    found = constructors_of(source)[:count]
    text = ["// written by probe_props.py (task sl1), never by hand", ""]
    for name, types in found:
        text.append(property_text(name, types, registers))
        print("constructor %s : (%s)" % (name, ", ".join(types)))
    open(os.path.join(model_dir, "sl1_props.sail"), "w").write("\n".join(text))
    project = os.path.join(model_dir, "riscv.sail_project")
    original = open(project).read()
    top = re.findall(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\{", original, re.M)
    module = "\nsl1_props {\n  requires %s\n  files sl1_props.sail\n}\n" % ", ".join(top)
    open(project, "w").write(original + module)
    print("integer registers declared: %d" % registers)
    print("module added, requires: %s" % ", ".join(top))


if __name__ == "__main__":
    main()
