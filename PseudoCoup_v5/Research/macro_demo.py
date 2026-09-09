#!/usr/bin/env python3
"""What a Rust macro IS, written in Python.

Run it:  python3 PseudoCoup_v5/Research/macro_demo.py

A macro is a function. Its input is a list of tokens. Its output is a
list of tokens. It runs BEFORE anything is parsed, and what it returns
is then parsed as ordinary code.

The macro's author writes two things:
  - a PATTERN, saying how to read the incoming list;
  - a TEMPLATE, saying which list to hand back.

Written 2026-08-02 for the `ur` node discussion. Standard library only.
"""
import re


def tokens(text):
    """Split text into the smallest pieces a compiler recognizes."""
    return re.findall(r'[A-Za-z_][A-Za-z0-9_]*|\d+|"[^"]*"|=>|::|[^\s]', text)


def split_top(toks, sep=","):
    """Split a token list on separators that are NOT inside brackets."""
    parts, cur, depth = [], [], 0
    for t in toks:
        if t in "([{":
            depth += 1
        elif t in ")]}":
            depth -= 1
        if t == sep and depth == 0:
            parts.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        parts.append(cur)
    return parts


def assert_eq(input_tokens):
    """An ORDINARY macro: returns a check.

    PATTERN:  $a , $b        -- two holes, split at the top-level comma
    TEMPLATE: fixed tokens with the two holes dropped in
    """
    a, b = split_top(input_tokens)
    return (tokens("if ! (") + a + tokens("==") + b
            + tokens(') { panic ( "assertion failed" ) }'))


def math_builder_methods(input_tokens):
    """A STRUCTURE-GENERATING macro: returns whole functions.

    PATTERN:  repeating -- for each top-level group `name ( args ) => call`
    TEMPLATE: one complete function per group

    This is the real shape of the macro at
    rust/compiler/rustc_codegen_llvm/src/builder.rs:267, which generates
    the 22 methods of the MIR-to-LLVM routing table, `sdiv` among them.
    """
    out = []
    for entry in split_top(input_tokens):
        if not entry:
            continue
        name = entry[0]
        args = split_top(entry[entry.index("(") + 1:entry.index(")")])
        call = entry[entry.index("=>") + 1]
        params = []
        for a in args:
            params += a + tokens(": & Value ,")
        params = params[:-1] if params else params
        passed = []
        for a in args:
            passed += a + [","]
        passed = passed[:-1] if passed else passed
        out += (tokens(f"fn {name} ( & mut self ,") + params
                + tokens(") -> & Value { unsafe {")
                + tokens(f"llvm :: {call} (")
                + tokens("self . llbuilder ,") + passed + tokens(") } }"))
    return out


def show(title, written, inner_text, fn):
    print(f"=== {title}")
    print("  1. what you write:")
    print(f"       {written}")
    ins = tokens(inner_text)
    print(f"  2. what the macro RECEIVES — {len(ins)} tokens, no structure:")
    print(f"       {ins}")
    outs = fn(ins)
    print(f"  3. what the macro RETURNS — {len(outs)} tokens:")
    print(f"       {' '.join(outs)}")
    print("  4. the compiler parses THAT as ordinary code.")
    print()


if __name__ == "__main__":
    show("ordinary macro", "assert_eq!(a, b)", "a , b", assert_eq)
    show("structure-generating macro",
         "math_builder_methods! { add(a,b) => LLVMBuildAdd, "
         "sdiv(a,b) => LLVMBuildSDiv }",
         "add ( a , b ) => LLVMBuildAdd , sdiv ( a , b ) => LLVMBuildSDiv",
         math_builder_methods)

    print("=== the point")
    print("  Same kind of thing both times: tokens in, tokens out.")
    print("  The first returns a check.")
    print("  The second returns two FUNCTIONS never written in the file.")
    print()
    print("=== why a parser cannot do this for you")
    print("  Step 2 is a plain list. Nothing in it says which macro it")
    print("  belongs to, and each macro reads that list its own way.")
    print("  assert_eq splits at a comma and expects two values;")
    print("  math_builder_methods expects groups ending in '=> name'.")
    print("  Neither reading works for the other.")
