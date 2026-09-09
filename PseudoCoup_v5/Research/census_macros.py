#!/usr/bin/env python3
"""Census: how much of a Rust source tree is macros, and how much of it
tree-sitter can parse at all.

    python3 PseudoCoup_v5/Research/census_macros.py \\
        Sources/rust/compiler

Two questions in one pass, because they are measured from the same
parse and the second one bounds the first:

  1. MACRO USE — macro_invocation nodes, macro_rules! definitions, and
     derive attributes, with the most-used macro names ranked.
  2. INGESTIBILITY — how many files parse with no ERROR node. A file
     that does not parse contributes nothing trustworthy to (1), so
     the macro counts are reported against the files that DID parse,
     and the rest are reported separately rather than folded in.

Needs tree-sitter and the rust grammar:

    pip install tree-sitter tree-sitter-rust

Written 2026-08-02 for the `ur` node's open questions. It reads only;
it writes nothing.
"""
import collections
import os
import sys

try:
    from tree_sitter import Language, Parser
    import tree_sitter_rust as tsr
except ImportError:
    sys.exit("missing dependency — run:\n"
             "    pip install tree-sitter tree-sitter-rust")


def crate_of(path, root):
    """The first path segment under the root — 'rustc_middle' etc."""
    rel = os.path.relpath(path, root)
    parts = rel.split(os.sep)
    return parts[0] if parts else "?"


def census(root):
    lang = Language(tsr.language())
    parser = Parser(lang)

    files_ok = files_err = 0
    lines_ok = lines_err = 0
    invocations = 0
    definitions = 0
    derives = 0
    by_name = collections.Counter()
    by_crate_inv = collections.Counter()
    by_crate_files = collections.Counter()
    err_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "target", "tests", "ui")]
        for fn in filenames:
            if not fn.endswith(".rs"):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, "rb") as fh:
                    src = fh.read()
            except OSError:
                continue
            nlines = src.count(b"\n") + 1
            tree = parser.parse(src)
            crate = crate_of(full, root)
            by_crate_files[crate] += 1
            if tree.root_node.has_error:
                files_err += 1
                lines_err += nlines
                err_files.append(os.path.relpath(full, root))
                continue          # counts below would not be trustworthy
            files_ok += 1
            lines_ok += nlines

            stack = [tree.root_node]
            while stack:
                n = stack.pop()
                t = n.type
                if t == "macro_invocation":
                    invocations += 1
                    by_crate_inv[crate] += 1
                    name = n.child_by_field_name("macro")
                    if name is not None:
                        by_name[src[name.start_byte:name.end_byte]
                                .decode("utf-8", "replace")] += 1
                elif t == "macro_definition":
                    definitions += 1
                elif t == "attribute_item":
                    text = src[n.start_byte:n.end_byte]
                    if b"derive" in text:
                        derives += 1
                stack.extend(n.children)

    return dict(files_ok=files_ok, files_err=files_err,
                lines_ok=lines_ok, lines_err=lines_err,
                invocations=invocations, definitions=definitions,
                derives=derives, by_name=by_name,
                by_crate_inv=by_crate_inv,
                by_crate_files=by_crate_files, err_files=err_files)


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: python3 {sys.argv[0]} <rust source dir>")
    root = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    r = census(root)
    total_files = r["files_ok"] + r["files_err"]
    total_lines = r["lines_ok"] + r["lines_err"]
    if total_files == 0:
        sys.exit(f"no .rs files under {root}")

    print(f"root: {root}")
    print()
    print("== ingestibility (stock tree-sitter-rust grammar)")
    print(f"  .rs files             {total_files}")
    print(f"  parse clean           {r['files_ok']} "
          f"({100*r['files_ok']/total_files:.1f}%)")
    print(f"  contain an ERROR node {r['files_err']} "
          f"({100*r['files_err']/total_files:.1f}%)")
    print(f"  lines clean           {r['lines_ok']} of {total_lines} "
          f"({100*r['lines_ok']/max(total_lines,1):.1f}%)")
    print()
    print("== macro use, over the CLEAN files only")
    print(f"  macro invocations     {r['invocations']}")
    print(f"  macro_rules! defs     {r['definitions']}")
    print(f"  derive attributes     {r['derives']}")
    if r["files_ok"]:
        print(f"  invocations per file  "
              f"{r['invocations']/r['files_ok']:.1f}")
        print(f"  invocations per kloc  "
              f"{1000*r['invocations']/max(r['lines_ok'],1):.1f}")
    print()
    print("== most-invoked macros")
    for name, n in r["by_name"].most_common(25):
        print(f"  {n:>7}  {name}!")
    print()
    print("== by crate (invocations / clean files / total files)")
    rows = sorted(r["by_crate_inv"].items(), key=lambda kv: -kv[1])[:20]
    for crate, n in rows:
        print(f"  {n:>7}  {crate}  "
              f"({r['by_crate_files'][crate]} files)")
    print()
    print("== files the grammar could not parse")
    print(f"  {r['files_err']} file(s); first 20:")
    for f in r["err_files"][:20]:
        print(f"    {f}")
    if r["files_err"] > 20:
        print(f"    ... and {r['files_err']-20} more")


if __name__ == "__main__":
    main()
