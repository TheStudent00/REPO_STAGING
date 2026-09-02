"""check_uniformity — the T4 enforcement check.

CORE_0_0_3's governing law: "every operator on a polyfilled type routes
through the wrapper, or none do." Mixed depth is forbidden because an
unwrapped node becomes ambiguous between "proven safe" and "tool missed
it." This module makes that law CHECKABLE: given a Python module (source
text or an already-parsed ast.Module), it finds every polyfilled value and
verifies every arithmetic/bitwise/shift/comparison operator touching it is
immediately wrapped, reporting any bare operator as a violation.

Provenance: the doctrine this enforces is CORE_0_0_3 itself and a
uniform-wrapping POLICY note carried over from a retired reference
backend's Rust support-layer transpile ("Every arithmetic node in a
u8-typed Rust expression is wrapped in u8(), with no exemptions --
even where overflow is provably impossible... The exhaustive proofs
become TESTS of these polyfills, not licence to omit them."). The
worked positive example this check is built to accept verbatim is
that transpile's own `encode_modrm`:

    u8(u8(u8(m0d & 3) << 6) | u8(u8(enc_reg_g & 7) << 3) | u8(rm_e & 7))

-- every single `&`/`<<`/`|` is the immediate argument of a `u8(...)`
call. A version with even one of those bare (say `m0d & 3` unwrapped)
is exactly the violation this module exists to catch; see
test_polyfill.py for both as literal fixtures.

SCOPE (a recorded, deliberate limitation, not an oversight): a name is
"polyfilled" here if it is (a) a function parameter or a variable
annotated with a wrapper type name (`u8`..`i64` or `U8`..`I64`), (b) a
local assigned directly from a call to one of the wrapper functions/
types, or (c) a local assigned from an already-polyfilled name (simple
aliasing, propagated to a fixed point). Statically inferring that some
OTHER, un-annotated, dynamically-typed variable is "secretly" u8-typed by
convention alone (the harvested transpile's own style, e.g. `encode_modrm`'s
bare `m0d`/`enc_reg_g`/`rm_e` parameters) is undecidable in general Python
and out of scope; annotate to bring a value under this check.
"""

import ast

FUNC_WRAPPER_NAMES = {"u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64"}
TYPE_WRAPPER_NAMES = {"U8", "U16", "U32", "U64", "I8", "I16", "I32", "I64"}
WRAPPER_NAMES = FUNC_WRAPPER_NAMES | TYPE_WRAPPER_NAMES

# annotations accepted to mark a name as polyfilled: either spelling
ANNOTATION_NAMES = WRAPPER_NAMES

_OPERATOR_NODE_TYPES = (ast.BinOp, ast.UnaryOp, ast.Compare)


class Violation:
    __slots__ = ("lineno", "col", "kind", "snippet")

    def __init__(self, lineno, col, kind, snippet):
        self.lineno, self.col, self.kind, self.snippet = lineno, col, kind, snippet

    def __repr__(self):
        return f"Violation(line {self.lineno}, col {self.col}, {self.kind}: {self.snippet!r})"

    def __eq__(self, other):
        return (isinstance(other, Violation) and self.lineno == other.lineno
                and self.col == other.col and self.snippet == other.snippet)


def _attach_super_nodes(tree):
    """Record each node's immediate super-node (the AST's own containment
    relation, not a domain object relationship) so a node can look upward
    without a second walk."""
    for node in ast.walk(tree):
        for sub in ast.iter_child_nodes(node):
            sub._uniformity_super = node
    return tree


def _is_wrapper_call(node) -> bool:
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in WRAPPER_NAMES)


def _chain_root_wrapped(node) -> bool:
    """True if `node` is directly wrapped by a Call to a wrapper, OR is a
    link in an associative same-operator BinOp chain (Python's left-assoc
    parse of `A | B | C` as nested BinOp(BinOp(A, B), C), all `BitOr`)
    whose outermost link IS directly wrapped -- the harvested transpile's
    real `u8(u8(...) | u8(...) | u8(...))` wraps the whole OR-chain once, not
    each pairwise `|`. A DIFFERENT operator stacked directly on top (e.g.
    an `&` feeding a `<<`) is never collapsed into that chain -- each
    still needs its own direct wrap, matching that same file's
    `u8(u8(m0d & 3) << 6)` (the `&` and the `<<` are each individually
    wrapped, not just the outermost)."""
    cur = node
    while True:
        sup = getattr(cur, "_uniformity_super", None)
        if _is_wrapper_call(sup):
            return True
        if (isinstance(cur, ast.BinOp) and isinstance(sup, ast.BinOp)
                and type(sup.op) is type(cur.op)):
            cur = sup
            continue
        return False


def _wrapper_call_from_call_value(node) -> bool:
    """value is `wrapper(...)` directly, e.g. `x = u8(y & z)`."""
    return _is_wrapper_call(node)


def _collect_polyfilled_names(tree) -> set:
    polyfilled = set()

    # seed from annotations: `def f(x: u8, ...)`, `x: u8 = ...`
    for node in ast.walk(tree):
        if isinstance(node, ast.arg) and node.annotation is not None:
            ann = node.annotation
            if isinstance(ann, ast.Name) and ann.id in ANNOTATION_NAMES:
                polyfilled.add(node.arg)
        elif isinstance(node, ast.AnnAssign):
            ann = node.annotation
            if (isinstance(ann, ast.Name) and ann.id in ANNOTATION_NAMES
                    and isinstance(node.target, ast.Name)):
                polyfilled.add(node.target.id)

    # fixed point over assignments: `x = u8(...)`, or `x = <already polyfilled>`
    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    changed = True
    while changed:
        changed = False
        for a in assigns:
            value_is_polyfilled = (
                _wrapper_call_from_call_value(a.value)
                or (isinstance(a.value, ast.Name) and a.value.id in polyfilled)
            )
            if value_is_polyfilled:
                for t in a.targets:
                    if isinstance(t, ast.Name) and t.id not in polyfilled:
                        polyfilled.add(t.id)
                        changed = True
    return polyfilled


def _touches_polyfilled(node, polyfilled: set) -> bool:
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in polyfilled:
            return True
    return False


def check_ast(tree: ast.AST) -> list:
    """Return a list of Violation for every bare (unwrapped) operator
    touching a polyfilled value in `tree`. Empty list == uniform."""
    _attach_super_nodes(tree)
    polyfilled = _collect_polyfilled_names(tree)
    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, _OPERATOR_NODE_TYPES):
            continue
        if not _touches_polyfilled(node, polyfilled):
            continue
        if _chain_root_wrapped(node):
            continue
        violations.append(Violation(
            lineno=getattr(node, "lineno", -1),
            col=getattr(node, "col_offset", -1),
            kind=type(node).__name__,
            snippet=ast.unparse(node),
        ))
    return violations


def check(source_or_tree, filename: str = "<module>") -> list:
    """Accept either source text or an ast.AST. -> list[Violation]."""
    if isinstance(source_or_tree, ast.AST):
        tree = source_or_tree
    else:
        tree = ast.parse(source_or_tree, filename=filename)
    return check_ast(tree)


def is_uniform(source_or_tree, filename: str = "<module>") -> bool:
    return not check(source_or_tree, filename=filename)


if __name__ == "__main__":
    import sys
    for path in sys.argv[1:]:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        violations = check(src, filename=path)
        if not violations:
            print(f"{path}: uniform (0 violations)")
        else:
            print(f"{path}: {len(violations)} violation(s)")
            for v in violations:
                print(f"  line {v.lineno}, col {v.col}: bare {v.kind} `{v.snippet}`")
