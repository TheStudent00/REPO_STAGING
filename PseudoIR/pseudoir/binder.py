"""
binder.py -- construct classification, extracted from v2/gate/gate.py.

WHAT THIS IS
------------
The MAP half of the registry gate: given a parsed Hub source tree, decide for every
named tree-sitter node whether it is

    baseline   -- plain Python that lowers to every target with no registry op
                  (literals, names, if/while/for, def, plain assignment, arithmetic).
    bound      -- a construct the gate RECOGNIZES as one registry op/xform, by the
                  same source shapes the probers recorded (U.coalesce -> op.null_coalesce,
                  a keyword-arg call site -> xform.named_args, a tuple-target assignment
                  -> op.destructure, an operator over user-typed operands ->
                  op.overloaded_binary, an f-string -> op.string_interp, ...).
    forbidden  -- discipline-banned (lambda, yield, with, global) or out-of-scope
                  (comprehensions): no registry op covers it, so it is a visible gap.

gate.py had all of this inline (BASELINE_NODES, FORBIDDEN_NODES, collect_bindings,
the U-import verification, the user-type annotation tracking). This module is that
logic lifted out VERBATIM in behavior, so both the gate (pseudoir/gate.py) and the
transpiler (pseudoir/transpile.py) classify constructs through ONE binder instead of
each re-walking the tree with its own rules. The recognizer shapes are unchanged --
this is a move, not a rewrite.

PUBLIC SURFACE
--------------
    parse(src_bytes) -> tree_sitter tree
    u_import_present(root, src) -> bool     (the U-namespace disambiguation)
    classify(root, src, u_ok) -> Classification

`Classification` carries: the list of op/xform Bindings (each with op_id, line,
snippet), the forbidden/out-of-scope constructs, the baseline node-type counts, and
the unknown (out-of-scope) node types -- exactly what gate.py's collect_bindings
returned, packaged as one object.
"""
import tree_sitter as ts
import tree_sitter_python

PY_LANG = ts.Language(tree_sitter_python.language())
PARSER = ts.Parser(PY_LANG)


def _txt(node, src):
    return src[node.start_byte:node.end_byte].decode()


def parse(src_bytes):
    """Parse Hub source bytes; return the tree-sitter tree."""
    return PARSER.parse(src_bytes)


# ===========================================================================
# THE BASELINE SET (verbatim from gate.py). A named node NOT here and NOT bound
# to an op is a visible gap, never a silent pass -- the coverage.py posture.
# ===========================================================================
BASELINE_NODES = frozenset({
    "module", "block", "comment",
    "function_definition", "parameters", "typed_parameter", "default_parameter",
    "typed_default_parameter", "class_definition", "decorated_definition",
    "decorator",
    "expression_statement", "return_statement", "pass_statement",
    "break_statement", "continue_statement", "import_statement",
    "import_from_statement", "aliased_import", "dotted_name", "raise_statement",
    "assert_statement",
    "if_statement", "elif_clause", "else_clause", "while_statement",
    "for_statement", "try_statement", "except_clause", "finally_clause",
    "call", "argument_list", "attribute", "identifier", "integer", "float",
    "string", "string_content", "string_start", "string_end", "escape_sequence",
    "true", "false", "none", "concatenated_string",
    "parenthesized_expression", "boolean_operator", "not_operator",
    "comparison_operator", "binary_operator", "unary_operator",
    "conditional_expression", "subscript", "slice",
    "assignment", "augmented_assignment", "type",
    "pattern_list", "tuple_pattern", "list_pattern", "expression_list",
    "interpolation", "format_specifier", "format_expression",
    "list", "dictionary", "set", "tuple", "pair",
    "keyword_argument",
    # match-statement structure is baseline; op.match_expr binds at match_statement.
    "case_clause", "case_pattern", "if_clause",
})

FORBIDDEN_NODES = {
    "lambda": "lambda -- FORBIDDEN (discipline: no anonymous fns; name the function)",
    "yield": "yield / generator -- FORBIDDEN (discipline: generators need a "
             "state-machine transform; eager-list lowering silently changes laziness)",
    "with_statement": "with -- FORBIDDEN (context-manager protocol has no honest "
                      "cross-target lowering)",
    "global_statement": "global -- FORBIDDEN (dynamism ban)",
    "nonlocal_statement": "nonlocal -- FORBIDDEN (dynamism ban)",
    "await": "await -- FORBIDDEN (async has no synchronous lowering)",
    "list_comprehension": "list comprehension -- OUT OF SCOPE (no registry op covers "
                          "comprehensions; rewrite as an explicit loop)",
    "dictionary_comprehension": "dict comprehension -- OUT OF SCOPE (no registry op)",
    "set_comprehension": "set comprehension -- OUT OF SCOPE (no registry op)",
    "generator_expression": "generator expression -- FORBIDDEN (generator; "
                            "same laziness problem as yield)",
}

_PRIMITIVE_TYPES = frozenset({
    "int", "float", "str", "bool", "bytes", "complex", "None",
    "list", "dict", "set", "tuple", "frozenset", "object",
    "List", "Dict", "Set", "Tuple", "Optional", "Any", "Sequence",
})
_OVERLOADABLE_SYMS = frozenset({"+", "-", "*", "/", "%", "==", "<", "<=", ">", ">="})


class Binding:
    """One recognized construct: which op it bound to, and where it sits."""
    __slots__ = ("op_id", "kind", "line", "snippet")

    def __init__(self, op_id, kind, line, snippet):
        self.op_id = op_id
        self.kind = kind   # "op" | "xform" | "forbidden" | "out_of_scope"
        self.line = line
        self.snippet = snippet


class Classification:
    """The result of classify(): op/xform bindings, forbidden constructs, baseline
    node counts, and unknown (out-of-scope) node types."""
    __slots__ = ("bindings", "forbidden", "baseline_types", "unknown", "u_ok")

    def __init__(self, bindings, forbidden, baseline_types, unknown, u_ok):
        self.bindings = bindings
        self.forbidden = forbidden
        self.baseline_types = baseline_types
        self.unknown = unknown
        self.u_ok = u_ok

    @property
    def bound_op_ids(self):
        return sorted({b.op_id for b in self.bindings if b.op_id})


# ---- U-import verification (verbatim from gate.py) -------------------------
def u_import_present(root, src):
    """Is the Hub `U` module actually imported? Recognizes `import U`,
    `from hub import U`, `import hub.U as U`. A bare `coalesce(...)` never binds an
    op; only `U.coalesce` does, and only when this returns True."""
    def walk(n):
        if n.type == "import_statement":
            for c in n.named_children:
                if c.type == "dotted_name" and _txt(c, src) in ("U", "hub.U"):
                    return True
                if c.type == "aliased_import":
                    alias = c.child_by_field_name("alias")
                    if alias is not None and _txt(alias, src) == "U":
                        return True
        if n.type == "import_from_statement":
            mod = n.child_by_field_name("module_name")
            names = [ch for ch in n.named_children if ch is not mod]
            for ch in names:
                if ch.type == "dotted_name" and _txt(ch, src) == "U":
                    if mod is not None and _txt(mod, src) in ("hub", "hub.U", "."):
                        return True
        for c in n.children:
            if walk(c):
                return True
        return False
    return walk(root)


def _callee_is_U(call, src, attr_name):
    fn = call.child_by_field_name("function")
    return (fn is not None and fn.type == "attribute"
            and _txt(fn, src) == f"U.{attr_name}")


def _is_safe_unwrap_chain(call, src):
    """Recognize `U.safe(x).a.b.unwrap(default)` -- op.safe_call. Verbatim from
    gate.py, itself ported from demo_u_namespace.py::_walk_safe_chain."""
    fn = call.child_by_field_name("function")
    if fn is None or fn.type != "attribute":
        return False
    attr = fn.child_by_field_name("attribute")
    if attr is None or _txt(attr, src) != "unwrap":
        return False
    cur = fn.child_by_field_name("object")
    while cur is not None and cur.type == "attribute":
        cur = cur.child_by_field_name("object")
    if cur is not None and cur.type == "call":
        inner = cur.child_by_field_name("function")
        return inner is not None and inner.type == "attribute" and _txt(inner, src) == "U.safe"
    return False


def classify(root, src, u_ok):
    """Walk the tree; classify every NAMED node. Behaviorally identical to gate.py's
    collect_bindings, returned as a Classification object."""
    bindings = []
    forbidden = []
    baseline_types = {}
    unknown = {}
    user_typed_names = {}

    def annotate_user_types(n):
        if n.type in ("typed_parameter", "typed_default_parameter"):
            name_node = n.child_by_field_name("name") or (n.children[0] if n.children else None)
            type_node = n.child_by_field_name("type")
            if name_node is not None and type_node is not None:
                tname = _txt(type_node, src).strip()
                if tname not in _PRIMITIVE_TYPES:
                    user_typed_names[_txt(name_node, src)] = tname
        if n.type == "assignment":
            type_node = n.child_by_field_name("type")
            left = n.child_by_field_name("left")
            if type_node is not None and left is not None and left.type == "identifier":
                tname = _txt(type_node, src).strip()
                if tname not in _PRIMITIVE_TYPES:
                    user_typed_names[_txt(left, src)] = tname
        for c in n.children:
            annotate_user_types(c)

    annotate_user_types(root)

    def line_of(n):
        return n.start_point[0] + 1

    def is_user_operand(expr_node):
        if expr_node.type == "identifier":
            return _txt(expr_node, src) in user_typed_names
        if expr_node.type == "call":
            fn = expr_node.child_by_field_name("function")
            if fn is not None and fn.type == "identifier":
                return _txt(fn, src) in set(user_typed_names.values())
        if expr_node.type in ("binary_operator", "unary_operator", "parenthesized_expression"):
            inner = expr_node.child_by_field_name("left") or (
                expr_node.named_children[0] if expr_node.named_children else None)
            return inner is not None and is_user_operand(inner)
        return False

    def visit(n):
        t = n.type

        if t in FORBIDDEN_NODES:
            kind = "out_of_scope" if "OUT OF SCOPE" in FORBIDDEN_NODES[t] else "forbidden"
            forbidden.append(Binding(None, kind, line_of(n), FORBIDDEN_NODES[t]))
            return

        if t == "call":
            if u_ok and _callee_is_U(n, src, "coalesce"):
                bindings.append(Binding("op.null_coalesce", "op", line_of(n), _txt(n, src)))
            elif u_ok and _callee_is_U(n, src, "not_null"):
                bindings.append(Binding("op.not_null_assert", "op", line_of(n), _txt(n, src)))
            elif u_ok and _is_safe_unwrap_chain(n, src):
                bindings.append(Binding("op.safe_call", "op", line_of(n), _txt(n, src)))
            else:
                # op.range Hub spelling: range(...) / range_inclusive(...) call.
                fn = n.child_by_field_name("function")
                fn_name = _txt(fn, src) if fn is not None else ""
                if fn_name in ("range", "range_inclusive"):
                    bindings.append(Binding("op.range", "op", line_of(n), _txt(n, src)))
                else:
                    arglist = n.child_by_field_name("arguments")
                    if arglist is not None and any(
                            c.type == "keyword_argument" for c in arglist.named_children):
                        bindings.append(Binding("xform.named_args", "xform", line_of(n), _txt(n, src)))
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if t == "assignment":
            left = n.child_by_field_name("left")
            right = n.child_by_field_name("right")
            if (u_ok and left is not None and left.type == "identifier"
                    and right is not None and right.type == "call"
                    and _callee_is_U(right, src, "coalesce")):
                al = right.child_by_field_name("arguments")
                first = al.named_children[0] if al and al.named_children else None
                if first is not None and _txt(first, src) == _txt(left, src):
                    bindings.append(Binding("op.coalesce_assign", "op", line_of(n), _txt(n, src)))
                    baseline_types[t] = baseline_types.get(t, 0) + 1
                    for c in n.children:
                        visit(c)
                    return
            if left is not None and left.type in ("pattern_list", "tuple_pattern", "list_pattern"):
                bindings.append(Binding("op.destructure", "op", line_of(n), _txt(n, src)))
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if t in ("binary_operator", "unary_operator"):
            sym = None
            opnode = n.child_by_field_name("operator")
            if opnode is not None:
                sym = _txt(opnode, src)
            is_user = False
            if t == "binary_operator":
                lft = n.child_by_field_name("left")
                rgt = n.child_by_field_name("right")
                is_user = (lft is not None and is_user_operand(lft)) or \
                          (rgt is not None and is_user_operand(rgt))
            else:
                arg = n.child_by_field_name("argument") or (
                    n.named_children[0] if n.named_children else None)
                is_user = arg is not None and is_user_operand(arg)
            if is_user and (sym in _OVERLOADABLE_SYMS or (t == "unary_operator" and sym == "-")):
                bindings.append(Binding("op.overloaded_binary", "op", line_of(n), _txt(n, src)))
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if t == "string":
            if any(c.type == "interpolation" for c in n.children):
                bindings.append(Binding("op.string_interp", "op", line_of(n), _txt(n, src)))
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if t == "match_statement":
            bindings.append(Binding("op.match_expr", "op", line_of(n), "match ..."))
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if t in BASELINE_NODES:
            baseline_types[t] = baseline_types.get(t, 0) + 1
            for c in n.children:
                visit(c)
            return

        if n.is_named:
            cnt, ex = unknown.get(t, (0, line_of(n)))
            unknown[t] = (cnt + 1, ex)
        for c in n.children:
            visit(c)

    visit(root)
    return Classification(bindings, forbidden, baseline_types, unknown, u_ok)
