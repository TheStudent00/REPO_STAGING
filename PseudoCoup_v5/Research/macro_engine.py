#!/usr/bin/env python3
"""The macro operator itself, in Python — one engine, macros as data.

    python3 ~/Programming/PseudoCoup_v5/Research/macro_engine.py

This is NOT a hand-written Python version of any particular macro. It is
the machinery that runs ALL of them: give it a definition (a pattern and
a template) and an invocation, and it produces the tokens the compiler
then parses.

rustc calls this macro-by-example. Its version is at
rust/compiler/rustc_expand/src/mbe/macro_rules.rs — this file is that
idea at small scale, not a port of it.

Two bugs found while writing it, kept as comments where they bit:
the group-boundary stop, and fragment specifiers in templates.

Written 2026-08-02. Standard library only.
"""
import re


def lex(t):
    """Text -> the smallest pieces a compiler recognizes."""
    return re.findall(
        r'\$|[A-Za-z_][A-Za-z0-9_]*|\d+|"[^"]*"|=>|::|->|==|[^\s]', t)


OPEN, CLOSE = "([{", ")]}"
PAIR = {")": "(", "]": "[", "}": "{"}
SHUT = {"(": ")", "[": "]", "{": "}"}


def group(toks, i=0, want=None):
    """Pieces -> nested by bracket. This nesting is the ONE thing Rust
    guarantees about macro input: the delimiters balance."""
    out = []
    while i < len(toks):
        t = toks[i]
        if t in OPEN:
            inner, i = group(toks, i + 1, t)
            out.append(("grp", t, inner))
            continue
        if t in CLOSE:
            if want is None or PAIR[t] != want:
                raise SyntaxError(f"unbalanced {t}")
            return out, i + 1
        out.append(t)
        i += 1
    if want is not None:
        raise SyntaxError("unclosed")
    return out, i


def tt(text):
    return group(lex(text))[0]


def flat(items):
    out = []
    for it in items:
        if isinstance(it, tuple):
            _, d, inner = it
            out += [d] + flat(inner) + [SHUT[d]]
        else:
            out.append(it)
    return out


def parse_pat(items, frags=True):
    """Read a pattern or a template into nodes.

    frags=True for a PATTERN, where `$x:expr` names a fragment kind.
    frags=False for a TEMPLATE, where `$x` is followed by ordinary
    tokens — a ':' there is a real colon. Parsing templates with
    frags=True ate the ": u32" out of `const $n : u32 = $v ;`.
    """
    out, i = [], 0
    while i < len(items):
        it = items[i]
        if it == "$" and i + 1 < len(items):
            nxt = items[i + 1]
            if isinstance(nxt, tuple):                     # $( ... ) sep op
                _, _, inner = nxt
                j, sep, op = i + 2, None, None
                if j < len(items) and items[j] in "*+?":
                    op = items[j]; j += 1
                else:
                    if j < len(items) and not isinstance(items[j], tuple):
                        sep = items[j]; j += 1
                    if j < len(items) and items[j] in "*+?":
                        op = items[j]; j += 1
                out.append(("rep", parse_pat(inner, frags), sep, op or "*"))
                i = j
                continue
            name, frag, j = nxt, None, i + 2               # $name:frag
            if frags and j < len(items) and items[j] == ":":
                frag = items[j + 1]; j += 2
            out.append(("var", name, frag))
            i = j
            continue
        if isinstance(it, tuple):
            _, d, inner = it
            out.append(("grp", d, parse_pat(inner, frags)))
        else:
            out.append(("lit", it))
        i += 1
    return out


def vars_of(nodes):
    s = set()
    for n in nodes:
        if n[0] == "var":
            s.add(n[1])
        elif n[0] == "grp":
            s |= vars_of(n[2])
        elif n[0] == "rep":
            s |= vars_of(n[1])
    return s


def stopper(nodes):
    """Where does a metavariable's capture end? At whatever the pattern
    expects NEXT — which may be a literal token OR the opening of a
    group. Handling only the literal made `$name:ident(...)` swallow the
    whole invocation."""
    for n in nodes:
        if n[0] == "lit":
            return lambda x, tok=n[1]: (not isinstance(x, tuple)) and x == tok
        if n[0] == "grp":
            return lambda x, d=n[1]: isinstance(x, tuple) and x[1] == d
        return None
    return None


def match_seq(nodes, items, binds):
    """Match a pattern against tokens, filling `binds`. None = no match."""
    i = 0
    for k, node in enumerate(nodes):
        kind = node[0]
        if kind == "lit":
            if i >= len(items) or isinstance(items[i], tuple) \
                    or items[i] != node[1]:
                return None
            i += 1
        elif kind == "grp":
            if i >= len(items) or not isinstance(items[i], tuple) \
                    or items[i][1] != node[1]:
                return None
            if match_seq(node[2], items[i][2], binds) is None:
                return None
            i += 1
        elif kind == "var":
            stop = stopper(nodes[k + 1:])
            j = i
            while j < len(items) and not (stop and stop(items[j])):
                j += 1
            if j == i:
                return None
            binds[node[1]] = items[i:j]
            i = j
        elif kind == "rep":
            sub_nodes, sep = node[1], node[2]
            reps = []
            while i < len(items):
                if sep:
                    j = i
                    while j < len(items):
                        x = items[j]
                        if not isinstance(x, tuple) and x == sep:
                            break
                        j += 1
                    chunk, nxt = items[i:j], j
                else:
                    chunk, nxt = items[i:], len(items)
                if not chunk:
                    break
                sub = {}
                if match_seq(sub_nodes, chunk, sub) is None:
                    break
                reps.append(sub)
                i = nxt
                if sep and i < len(items) and items[i] == sep:
                    i += 1
            binds.setdefault("__reps__", []).append((vars_of(sub_nodes), reps))
    return i


def subst(nodes, binds):
    """Fill the template from the bindings."""
    out = []
    for node in nodes:
        kind = node[0]
        if kind == "lit":
            out.append(node[1])
        elif kind == "grp":
            out.append(("grp", node[1], subst(node[2], binds)))
        elif kind == "var":
            out += binds.get(node[1], [])
        elif kind == "rep":
            want = vars_of(node[1])
            best, score = [], -1
            for names, reps in binds.get("__reps__", []):
                s = len(want & names)
                if s > score:
                    best, score = reps, s
            for n, r in enumerate(best):
                merged = dict(binds)
                merged.update(r)
                out += subst(node[1], merged)
                if node[2] and n < len(best) - 1:
                    out.append(node[2])
    return out


def expand(definition, invocation):
    """definition: '( PATTERN ) => { TEMPLATE }'.

    The split is on the TOP-LEVEL `=>`, found by structure, not by
    string search — a macro's own pattern may contain `=>`, which is
    exactly what `math_builder_methods!` does.
    """
    items = tt(definition)
    pat = parse_pat(items[0][2], frags=True)
    tpl = parse_pat(items[2][2], frags=False)
    binds = {}
    if match_seq(pat, tt(invocation), binds) is None:
        return None
    return " ".join(flat(subst(tpl, binds)))


def demo(title, definition, invocation):
    print(f"=== {title}")
    print(f"  DEFINITION (data): {definition.strip()}")
    print(f"  INVOCATION:        {invocation.strip()}")
    r = expand(definition, invocation)
    print(f"  ENGINE OUTPUT:     {r if r else '<no match>'}")
    print()


if __name__ == "__main__":
    demo("assert_eq-shaped",
         '($a:expr, $b:expr) => { if ! ( $a == $b ) { panic ( "failed" ) } }',
         "x + 1, y")

    demo("math_builder_methods — the shape of the real one",
         "($($name:ident($($arg:ident),*) => $capi:ident),*) => "
         "{ $( fn $name ( & mut self , $($arg : & Value),* ) -> & Value "
         "{ unsafe { llvm :: $capi ( self . llbuilder , $($arg),* ) } } )* }",
         "add(a, b) => LLVMBuildAdd, sdiv(a, b) => LLVMBuildSDiv")

    demo("a third macro the engine has never seen",
         "($n:ident, $v:expr) => { const $n : u32 = $v ; }",
         "MAX, 4096")

    print("=== the point")
    print("  One engine. It names no macro.")
    print("  Each macro is a PATTERN and a TEMPLATE handed to it as data.")
