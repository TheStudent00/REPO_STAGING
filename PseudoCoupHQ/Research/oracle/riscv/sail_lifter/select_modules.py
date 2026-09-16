#!/usr/bin/env python3
"""select_modules.py -- the LEAF modules of the Sail project file that
belong to the extensions the compilers target, read off the project file
itself (task sl1).

A module is a leaf when its body has a `files` list.  The selection is
by the extension names the image's compilers are given in their march
string (rv64gc + Zba/Zbb/Zbs + Zicond: the brief's subset); a leaf is
selected when it, or any group it sits inside, is named in that list.
The substrate leaves every selection needs (the base and `main`) are
what `sail --list-files` resolves; this file only names the leaves.

usage: select_modules.py <riscv.sail_project> <group name>...
"""
import re
import sys

NAME = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$")


def leaves_of(path):
    """[(leaf name, [enclosing group names])] in file order."""
    out = []
    stack = []
    has_files = []
    for raw in open(path):
        line = raw.split("//")[0].rstrip()
        hit = NAME.match(line)
        if hit is not None:
            stack.append(hit.group(1))
            has_files.append(False)
            continue
        if line.strip().startswith("files"):
            if has_files:
                has_files[-1] = True
            continue
        if line.strip() == "}":
            if not stack:
                continue
            name = stack.pop()
            leaf = has_files.pop()
            if leaf:
                out.append((name, list(stack)))
    return out


def main():
    project = sys.argv[1]
    wanted = set(sys.argv[2:])
    chosen = []
    for name, groups in leaves_of(project):
        if name in wanted or any(g in wanted for g in groups):
            chosen.append(name)
    print(" ".join(chosen))


if __name__ == "__main__":
    main()
