#!/usr/bin/env python3
"""operator_variants_by_search.py -- task o4, arch_unit_oracle line,
compiler_units node.

Continuation of task o3 (compiler_operators_used.py, log_209). the owner,
2026-09-06, verbatim: "lets do what we can by search and see whats
left over and deal with it then."

This task narrows from o3's per-operator TOKEN census to per-operator
VARIANT resolution: for every operator site (a use of a LOWERED
operator -- the subset o3 already computed) in a compiler's own
source, find the type of each operand BY SEARCH ONLY (no compiler
front end, no -ast-dump, no go/types, no rust-analyzer -- the stop
rule). "Resolved by search" means: a literal's own kind and suffix, or
an identifier whose declaration is found by walking OUTWARD through
enclosing scopes in the SAME FILE (function locals/params, struct/
class fields, file globals) with an EXPLICIT type (never auto/:=/
untyped let). Anything else is UNRESOLVED with one reason from a fixed
list (see UnresolvedReason below).

REUSE, not fork, of o3's own machinery (per this task's brief): the
file walk (iter_source_files), the per-language operator-node mapping
built from operator_arity.json (build_language_inventory's
rule_tokens), the offered/lowered sets (lowered_set_for), and the six
measured rows (same dirs, same extensions, same parser-per-language).
Imported directly from compiler_operators_used.py, which sits beside
this file in the same directory -- not copied.

Memory bound: 2 GB (ABORT_MEMORY_O4), one file read/parsed/released at
a time, peak RSS via resource.getrusage.

THE SPELLING BAN is pasted in the brief (task o3's brief section 0,
which this task's own brief points to) and applies here exactly as
task o3 explained it in log_209 section 1: this script's json groups
by COMPILER and lists operators/variants as per-row MEMBER entries
(each carrying `lang` + `unit` fields), never as a dict key. The guard
(check_no_spelling_keys.py) is run over the produced json and its
output pasted in the log whatever it says.
"""
import json
import os
import re
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compiler_operators_used import (  # noqa: E402  -- reuse, not fork
    HQ, SOURCES, OPERATOR_ARITY_PATH, OP_PIPELINE,
    build_language_inventory, lowered_set_for, iter_source_files,
    build_parser,
)

MEMORY_BOUND_MB = 2048  # ABORT_MEMORY_O4


def abort_if_over_budget():
    peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak_kb / 1024.0
    if peak_mb > MEMORY_BOUND_MB:
        print(f"ABORT_MEMORY_O4: peak RSS {peak_mb:.1f} MB > {MEMORY_BOUND_MB} MB bound", file=sys.stderr)
        sys.exit(97)
    return peak_mb


TYPE_INVENTORY_CORE_PATH = f"{OP_PIPELINE}/type_inventory2_core2.json"


def load_core_type_inventory():
    """Task 40's core type inventory, per the brief: 'the type names
    task 40 read from each compiler
    (Research/op_pipeline/type_inventory2_core2.json or its successor
    -- find it, name which file, and if none matches a language say so
    rather than inventing a list)'. Read verbatim, no successor found
    on disk (checked: this is the newest `type_inventory2_core*` /
    `type_inventory3*` file whose top-level shape is a per-language
    scalar_core list; type_inventory3.json exists but is NOT a
    successor to core2 -- see NOTE in meta)."""
    with open(TYPE_INVENTORY_CORE_PATH) as f:
        doc = json.load(f)
    core = {}
    for lang, entry in doc["languages"].items():
        core[lang] = {c["spelling"] for c in entry["scalar_core"]}
    return core, TYPE_INVENTORY_CORE_PATH


# ---------------------------------------------------------------------------
# unresolved reasons -- fixed list, extend only if the source forces a
# new one (brief's own instruction)
# ---------------------------------------------------------------------------
class R:
    CALL_RESULT = "call result"
    MEMBER_ACCESS = "member access"
    INFERRED = "inferred binding"
    ELSEWHERE_OR_NOT_FOUND = "declared in another file or not found"
    TEMPLATE_GENERIC = "template/generic parameter type"
    MACRO = "macro"
    INDEX = "index expression"
    OTHER = "other"
    # new leaf, forced by task o4's nested-operand extension (rule 1):
    # a binary operator node used as an operand of another operator,
    # both of whose OWN operands resolve by search, but to two
    # DIFFERENT written types -- there is no single type to report.
    NESTED_MIXED = "nested operator, mixed operand types"


# rule (1): comparison/logical operators, whose result is the
# language's bool type as written, never the operand type itself.
COMPARISON_LOGICAL_TOKENS = {"==", "!=", "<", ">", "<=", ">=", "&&", "||"}
BOOL_TYPE_AS_WRITTEN = {"c": "bool", "cpp": "bool", "go": "bool", "rust": "bool", "swift": "Bool"}

# generic binary-operator token set used only to READ the operator
# spelling off a nested binary-shaped node encountered as an operand
# (rule 1) -- this is not a new offered/lowered set and is not used
# for site counting or grouping, only to decide bool-vs-same-type.
GENERIC_BINARY_TOKENS = {
    "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=",
    "&&", "||", "&", "|", "^", "<<", ">>", "..", "..=", "...", "..<",
}

# rule (2): the field a unary-shaped node carries its single operand
# under, across the four grammars (c/cpp: argument; go: operand;
# rust: value or argument; swift prefix_expression: target).
UNARY_OPERAND_FIELDS = ("argument", "operand", "value", "target")


AUTO = object()  # marker: declared, but no explicit type (auto / := / untyped let)


def literal_kind_and_suffix(node, lang, txt):
    t = node.type
    if lang in ("c", "cpp"):
        if t == "number_literal":
            m = re.search(r"([uUlLfF]+|i8|i16|i32|i64|u8|u16|u32|u64)$", txt)
            suffix = m.group(0) if m else None
            is_float = bool(re.search(r"[.eE]", txt.split("x")[0] if txt.lower().startswith("0x") else txt)) or (suffix and "f" in suffix.lower())
            return ("float literal" if is_float else "integer literal", suffix)
        if t == "string_literal":
            return ("string literal", None)
        if t == "char_literal":
            return ("char literal", None)
        if t in ("true", "false"):
            return ("bool literal", None)
    if lang == "go":
        if t == "int_literal":
            return ("integer literal", None)
        if t == "float_literal":
            return ("float literal", None)
        if t == "imaginary_literal":
            return ("float literal", "i")
        if t == "rune_literal":
            return ("char literal", None)
        if t in ("interpreted_string_literal", "raw_string_literal"):
            return ("string literal", None)
        if t == "true" or t == "false":
            return ("bool literal", None)
    if lang == "rust":
        if t == "integer_literal":
            m = re.search(r"(i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize)$", txt)
            return ("integer literal", m.group(0) if m else None)
        if t == "float_literal":
            m = re.search(r"(f32|f64)$", txt)
            return ("float literal", m.group(0) if m else None)
        if t == "string_literal":
            return ("string literal", None)
        if t == "char_literal":
            return ("char literal", None)
        if t == "boolean_literal":
            return ("bool literal", None)
    if lang == "swift":
        if t in ("integer_literal",):
            return ("integer literal", None)
        if t in ("real_literal",):
            return ("float literal", None)
        if t in ("line_string_literal", "multi_line_string_literal"):
            return ("string literal", None)
        if t in ("boolean_literal", "true", "false"):
            return ("bool literal", None)
    return None


CAST_NODE_TYPES = {
    "cpp": {"cast_expression": "type"},
    "c": {"cast_expression": "type"},
    "rust": {"type_cast_expression": "type"},
}


def unwrap_and_resolve(node, src, lang, scopes, path):
    """Recurse through parens/unary wrappers/casts to a base operand,
    return (('literal', kind, suffix), None) or (('typed', type_text), (decl_path, decl_line))
    or (None, reason_string)."""
    t = node.type
    if t in ("parenthesized_expression",):
        for c in node.children:
            if c.is_named:
                return unwrap_and_resolve(c, src, lang, scopes, path)
    cast_map = CAST_NODE_TYPES.get(lang, {})
    if t in cast_map:
        type_node = node.child_by_field_name(cast_map[t])
        if type_node is not None:
            return (("typed", text(type_node, src)), None)
    if lang == "rust" and t == "type_cast_expression":
        type_node = node.child_by_field_name("type")
        if type_node is not None:
            return (("typed", text(type_node, src)), None)
    if lang == "swift" and "as_expression" in t:
        # `e as T` -- last named child is the type per this grammar's
        # own shape (`as_operator` rule feeding a binary-shaped node).
        named = [c for c in node.children if c.is_named]
        if len(named) >= 2:
            return (("typed", text(named[-1], src)), None)
    if lang == "go" and t == "call_expression":
        fn = node.child_by_field_name("function")
        if fn is not None and fn.type == "type_identifier" and text(fn, src) in GO_BUILTIN_TYPES:
            return (("typed", text(fn, src)), None)

    lit = literal_kind_and_suffix(node, lang, text(node, src))
    if lit is not None:
        return (("literal", lit[0], lit[1]), None)

    if t in ("identifier", "field_identifier", "simple_identifier"):
        name = text(node, src)
        found = lookup_identifier(name, scopes)
        if found is None:
            return (None, R.ELSEWHERE_OR_NOT_FOUND)
        type_text, decl_line = found
        if type_text is AUTO:
            return (None, R.INFERRED)
        return (("typed", type_text), (path, decl_line))

    # rule (3): a composite/array literal with a WRITTEN type on the
    # node itself (`[]int{...}`, `T{...}` -- go's composite_literal
    # carries it under the grammar's own `type` field) resolves to
    # that type directly. Checked for any language's node of these
    # two names, generically -- when the field is absent (e.g. rust's
    # plain `[a, b, c]` / `[v; n]` array_expression, which carries no
    # type field of its own in this grammar), it falls through
    # unresolved as before, honestly, not invented.
    if t in ("composite_literal", "array_expression"):
        type_node = node.child_by_field_name("type")
        if type_node is not None:
            return (("typed", text(type_node, src)), None)

    if t in ("call_expression", "function_call_expression"):
        return (None, R.CALL_RESULT)
    if t in ("field_expression", "field_access_expression", "member_access_expression",
              "navigation_expression", "selector_expression"):
        return (None, R.MEMBER_ACCESS)
    if t in ("subscript_expression", "index_expression"):
        return (None, R.INDEX)
    if t in ("generic_type", "type_identifier") and lang != "go":
        return (None, R.TEMPLATE_GENERIC)
    if "macro" in t or "preproc" in t:
        return (None, R.MACRO)

    # rule (4): a qualified identifier (`Foo::bar`, cpp's
    # `qualified_identifier`) or a `this`/`self` member resolves LIKE
    # an identifier -- looked up the same way, through the same
    # same-file scope walk -- rather than being named "other" for its
    # own distinct node kind. `this`/`self` are essentially never
    # themselves declared in a same-file scope (they are an implicit
    # receiver, not a local/param/field), so this deterministically
    # resolves to R.ELSEWHERE_OR_NOT_FOUND in practice, which is
    # honest: it is a real declaration this search cannot find, not
    # an invented new bucket.
    if t == "qualified_identifier":
        named = [c for c in node.children if c.is_named]
        if named:
            name = text(named[-1], src)
            found = lookup_identifier(name, scopes)
            if found is None:
                return (None, R.ELSEWHERE_OR_NOT_FOUND)
            type_text, decl_line = found
            if type_text is AUTO:
                return (None, R.INFERRED)
            return (("typed", type_text), (path, decl_line))
    if t in ("this", "self", "self_expression"):
        name = "self" if t != "this" else "this"
        found = lookup_identifier(name, scopes)
        if found is None:
            return (None, R.ELSEWHERE_OR_NOT_FOUND)
        type_text, decl_line = found
        if type_text is AUTO:
            return (None, R.INFERRED)
        return (("typed", type_text), (path, decl_line))

    # rule (2): a unary-shaped operand (one operand field, no `right`
    # field -- so it is not itself a binary/assignment node) recurses
    # to the type of ITS OWN operand. This generalizes the old
    # per-language c/cpp-only and rust-only carve-outs to every
    # language's own unary node (go's `unary_expression` field
    # `operand`, swift's `prefix_expression`/`postfix_expression`
    # field `target`), closing the "other (unary_expression)" gap
    # that only c/cpp/rust had before. `!x` on a bool operand
    # naturally recurses to `bool`, per the brief's own example.
    #
    # SAFETY CHECK, found while verifying this rule against real
    # swift source before trusting it: tree-sitter-swift's grammar
    # reuses the field name `value` for the FIRST element of a
    # multi-element `tuple_expression` (`(a, b)`) and of a
    # `dictionary_literal` entry (`[k: v]`) -- neither is a unary
    # node, and naively following `value` there would silently
    # report the tuple/dictionary's type as its first element's type
    # alone, discarding the rest. Both are excluded by name; this is
    # a targeted grammar-fact exclusion, not a fifth rule -- they
    # still fall through to `other (tuple_expression)` /
    # `other (dictionary_literal)`, unresolved and correctly named,
    # exactly as before this section's change.
    if t not in ("tuple_expression", "dictionary_literal") and node.child_by_field_name("right") is None:
        for f in UNARY_OPERAND_FIELDS:
            operand = node.child_by_field_name(f)
            if operand is not None:
                return unwrap_and_resolve(operand, src, lang, scopes, path)

    # rule (1): the operand is ITSELF a binary-operator-shaped node
    # (has a `left`/`value` operand AND a `right` operand -- the same
    # shape `operand_nodes()` detects at a top-level site). Recurse
    # into both of its own operands by the SAME search; if both
    # resolve to the SAME written type, that type (or the language's
    # bool, for a comparison/logical operator) is the result; if they
    # resolve to two DIFFERENT written types, this is unresolved with
    # the new reason R.NESTED_MIXED (not folded into a bare "other").
    left = node.child_by_field_name("left") or node.child_by_field_name("value")
    right = node.child_by_field_name("right")
    if left is not None and right is not None:
        lres, _ = unwrap_and_resolve(left, src, lang, scopes, path)
        rres, _ = unwrap_and_resolve(right, src, lang, scopes, path)
        if lres is not None and rres is not None:
            ldesc, rdesc = describe(lres), describe(rres)
            if ldesc == rdesc:
                op_field = node.child_by_field_name("operator")
                op_text = text(op_field, src) if op_field is not None else None
                if op_text is None:
                    for c in node.children:
                        if not c.is_named:
                            ctext = text(c, src)
                            if ctext in GENERIC_BINARY_TOKENS:
                                op_text = ctext
                                break
                if op_text in COMPARISON_LOGICAL_TOKENS:
                    return (("typed", BOOL_TYPE_AS_WRITTEN.get(lang, "bool")), None)
                return (("typed", ldesc), None)
            return (None, R.NESTED_MIXED)

    return (None, f"{R.OTHER} ({t})")


GO_BUILTIN_TYPES = {
    "int", "int8", "int16", "int32", "int64", "uint", "uint8", "uint16",
    "uint32", "uint64", "uintptr", "float32", "float64", "byte", "rune",
    "bool", "string", "complex64", "complex128",
}


def text(node, src):
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def lookup_identifier(name, scopes):
    """scopes: list of dicts, innermost-first (function locals+params,
    then class/struct fields, then file globals). Returns
    (type_text_or_AUTO, decl_line) or None."""
    for scope in scopes:
        if name in scope:
            return scope[name]
    return None


# ---------------------------------------------------------------------------
# per-language declaration collection -- walks the WHOLE file once,
# builds: func_scopes {func_node_id: {name: (type_or_AUTO, line)}},
#         class_scopes {class_node_id: {name: (type_or_AUTO, line)}},
#         global_scope {name: (type_or_AUTO, line)}
# and enclosing_func / enclosing_class maps: node_id -> nearest
# enclosing function/class node id, built during the SAME site-scan
# walk (see collect_enclosing below), so lookup at a site is just:
# [func_scopes[enclosing_func]] + [class_scopes[enclosing_class]] + [global_scope]
# ---------------------------------------------------------------------------

FUNC_TYPES = {
    "c": {"function_definition"}, "cpp": {"function_definition"},
    "go": {"function_declaration", "method_declaration", "func_literal"},
    "rust": {"function_item", "closure_expression"},
    "swift": {"function_declaration", "init_declaration", "lambda_literal"},
}
CLASS_TYPES = {
    "c": {"struct_specifier"}, "cpp": {"struct_specifier", "class_specifier"},
    "go": {"type_declaration"},
    "rust": {"struct_item"},
    "swift": {"class_declaration", "struct_declaration"},
}


def line_of(node):
    return node.start_point[0] + 1


def add_decl(scope, name, type_text_or_auto, node):
    if name and name not in scope:
        scope[name] = (type_text_or_auto, line_of(node))


def find_first_child_type(node, wanted, depth=6):
    if depth <= 0:
        return None
    for c in node.children:
        if c.type in wanted:
            return c
    for c in node.children:
        r = find_first_child_type(c, wanted, depth - 1)
        if r is not None:
            return r
    return None


def collect_names_from_declarator(node, lang):
    """Unwrap pointer/array/reference declarators down to the bare
    identifier(s). Returns list of identifier nodes."""
    out = []

    def rec(n):
        if n is None:
            return
        if n.type in ("identifier", "field_identifier"):
            out.append(n)
            return
        for f in ("declarator",):
            child = n.child_by_field_name(f)
            if child is not None:
                rec(child)
                return
        for c in n.children:
            if c.is_named:
                rec(c)
    rec(node)
    return out


def collect_scopes_c_cpp(root, src, lang):
    func_scopes, class_scopes = {}, {}
    global_scope = {}

    def collect_params(func_node, scope):
        declarator = func_node.child_by_field_name("declarator")
        fdecl = find_first_child_type(declarator, {"function_declarator"}) if declarator else None
        if fdecl is None:
            return
        params = fdecl.child_by_field_name("parameters")
        if params is None:
            return
        for p in params.named_children:
            if p.type != "parameter_declaration":
                continue
            tnode = p.child_by_field_name("type")
            if tnode is None:
                continue
            type_text = text(tnode, src)
            decl = p.child_by_field_name("declarator")
            for idn in collect_names_from_declarator(decl, lang):
                add_decl(scope, text(idn, src), type_text, p)

    def collect_body_decls(body_node, scope):
        def walk(n, in_nested_func):
            if n.type in FUNC_TYPES.get(lang, ()) and n is not body_node:
                return  # do not descend into a nested function's own body twice
            if n.type == "declaration":
                tnode = n.child_by_field_name("type")
                type_text = text(tnode, src) if tnode is not None else None
                is_auto = (type_text == "auto") or (type_text is None)
                for child in n.children:
                    if child.type in ("init_declarator", "identifier", "pointer_declarator",
                                       "array_declarator", "reference_declarator"):
                        for idn in collect_names_from_declarator(child, lang):
                            add_decl(scope, text(idn, src), AUTO if is_auto else type_text, n)
            for c in n.children:
                walk(c, in_nested_func)
        walk(body_node, False)

    def walk_top(n):
        if n.type == "function_definition":
            scope = {}
            collect_params(n, scope)
            body = n.child_by_field_name("body")
            if body is not None:
                collect_body_decls(body, scope)
            func_scopes[n.id] = scope
        elif n.type in ("struct_specifier", "class_specifier"):
            scope = {}
            body = n.child_by_field_name("body")
            if body is not None:
                for f in body.named_children:
                    if f.type == "field_declaration":
                        tnode = f.child_by_field_name("type")
                        type_text = text(tnode, src) if tnode is not None else None
                        for child in f.children:
                            if child.type in ("field_identifier", "pointer_declarator", "array_declarator"):
                                for idn in collect_names_from_declarator(child, lang):
                                    add_decl(scope, text(idn, src), type_text, f)
            class_scopes[n.id] = scope
        elif n.type == "declaration" and n.parent is not None and n.parent.type == "translation_unit":
            tnode = n.child_by_field_name("type")
            type_text = text(tnode, src) if tnode is not None else None
            is_auto = type_text is None or type_text == "auto"
            for child in n.children:
                if child.type in ("init_declarator", "identifier", "pointer_declarator"):
                    for idn in collect_names_from_declarator(child, lang):
                        add_decl(global_scope, text(idn, src), AUTO if is_auto else type_text, n)
        for c in n.children:
            walk_top(c)

    walk_top(root)
    return func_scopes, class_scopes, global_scope


def collect_scopes_go(root, src, lang):
    func_scopes, class_scopes = {}, {}
    global_scope = {}

    def var_spec_decls(spec, scope):
        tnode = spec.child_by_field_name("type")
        type_text = text(tnode, src) if tnode is not None else None
        names = [c for c in spec.children if c.type == "identifier"]
        for idn in names:
            add_decl(scope, text(idn, src), (type_text if type_text else AUTO), spec)

    def collect_params(func_node, scope):
        plist = func_node.child_by_field_name("parameters")
        if plist is None:
            return
        for p in plist.named_children:
            if p.type != "parameter_declaration":
                continue
            tnode = p.child_by_field_name("type")
            if tnode is None:
                continue
            type_text = text(tnode, src)
            for idn in [c for c in p.children if c.type == "identifier"]:
                add_decl(scope, text(idn, src), type_text, p)

    def collect_body(body, scope):
        def walk(n):
            if n.type == "var_declaration":
                for spec in n.named_children:
                    if spec.type == "var_spec":
                        var_spec_decls(spec, scope)
            elif n.type == "short_var_declaration":
                left = n.child_by_field_name("left")
                if left is not None:
                    for idn in left.named_children:
                        if idn.type == "identifier":
                            add_decl(scope, text(idn, src), AUTO, n)
            elif n.type == "range_clause":
                for fld in ("left",):
                    left = n.child_by_field_name(fld)
                    if left is not None:
                        for idn in left.named_children:
                            if idn.type == "identifier":
                                add_decl(scope, text(idn, src), AUTO, n)
            if n.type in FUNC_TYPES["go"] and n is not body.parent:
                return
            for c in n.children:
                walk(c)
        walk(body)

    def walk_top(n, top=True):
        if n.type in FUNC_TYPES["go"]:
            scope = {}
            collect_params(n, scope)
            body = n.child_by_field_name("body")
            if body is not None:
                collect_body(body, scope)
            func_scopes[n.id] = scope
        elif n.type == "type_declaration":
            for spec in n.named_children:
                if spec.type != "type_spec":
                    continue
                stype = spec.child_by_field_name("type")
                if stype is None or stype.type != "struct_type":
                    continue
                scope = {}
                for fld in stype.named_children:
                    if fld.type != "field_declaration_list":
                        continue
                    for fdecl in fld.named_children:
                        if fdecl.type != "field_declaration":
                            continue
                        tnode = fdecl.child_by_field_name("type")
                        type_text = text(tnode, src) if tnode is not None else None
                        for idn in [c for c in fdecl.children if c.type == "field_identifier"]:
                            add_decl(scope, text(idn, src), type_text, fdecl)
                class_scopes[n.id] = scope
        elif top and n.type in ("var_declaration",) and n.parent is not None and n.parent.type == "source_file":
            for spec in n.named_children:
                if spec.type == "var_spec":
                    var_spec_decls(spec, global_scope)
        for c in n.children:
            walk_top(c, top and n.type == "source_file")

    walk_top(root)
    return func_scopes, class_scopes, global_scope


def collect_scopes_rust(root, src, lang):
    func_scopes, class_scopes = {}, {}
    global_scope = {}

    def collect_params(func_node, scope):
        plist = func_node.child_by_field_name("parameters")
        if plist is None:
            return
        for p in plist.named_children:
            if p.type != "parameter":
                continue
            tnode = p.child_by_field_name("type")
            pat = p.child_by_field_name("pattern")
            if tnode is None or pat is None:
                continue
            if pat.type == "identifier":
                add_decl(scope, text(pat, src), text(tnode, src), p)

    def collect_body(body, scope):
        def walk(n):
            if n.type == "let_declaration":
                pat = n.child_by_field_name("pattern")
                tnode = n.child_by_field_name("type")
                if pat is not None and pat.type == "identifier":
                    add_decl(scope, text(pat, src), text(tnode, src) if tnode is not None else AUTO, n)
            if n.type in FUNC_TYPES["rust"] and n is not body.parent:
                return
            for c in n.children:
                walk(c)
        walk(body)

    def walk_top(n):
        if n.type == "function_item":
            scope = {}
            collect_params(n, scope)
            body = n.child_by_field_name("body")
            if body is not None:
                collect_body(body, scope)
            func_scopes[n.id] = scope
        elif n.type == "struct_item":
            scope = {}
            body = n.child_by_field_name("body")
            if body is not None and body.type == "field_declaration_list":
                for fdecl in body.named_children:
                    if fdecl.type != "field_declaration":
                        continue
                    tnode = fdecl.child_by_field_name("type")
                    namen = fdecl.child_by_field_name("name")
                    if tnode is not None and namen is not None:
                        add_decl(scope, text(namen, src), text(tnode, src), fdecl)
            class_scopes[n.id] = scope
        elif n.type in ("static_item", "const_item") and n.parent is not None and n.parent.type == "source_file":
            namen = n.child_by_field_name("name")
            tnode = n.child_by_field_name("type")
            if namen is not None and tnode is not None:
                add_decl(global_scope, text(namen, src), text(tnode, src), n)
        for c in n.children:
            walk_top(c)

    walk_top(root)
    return func_scopes, class_scopes, global_scope


def find_type_annotation(node, src):
    for c in node.children:
        if c.type == "type_annotation":
            named = [x for x in c.named_children]
            if named:
                return text(named[-1], src)
    return None


def collect_scopes_swift(root, src, lang):
    func_scopes, class_scopes = {}, {}
    global_scope = {}

    def collect_params(func_node, scope):
        # tree-sitter-swift (checked directly, 2026-09-06): a
        # `function_declaration`'s parameters are NOT wrapped in a
        # distinct `parameter_clause` node in this grammar version --
        # `parameter` nodes sit as direct named children of the
        # function_declaration itself, alongside the return-type
        # `user_type` and the body. Collect from func_node's own
        # named_children directly rather than assuming a wrapper.
        for p in func_node.named_children:
            if p.type != "parameter":
                continue
            # tree-sitter-swift's `parameter` carries no field names and
            # no type_annotation wrapper (checked directly): its named
            # children are the identifier(s) (external + internal name,
            # when both given) followed by the type node itself. The
            # type is the LAST named child when there is more than one;
            # a bare `_` / single-name parameter with no type present
            # is left unresolved (falls through, name stays undeclared).
            names = [c for c in p.named_children if c.type == "simple_identifier"]
            all_named = list(p.named_children)
            if len(all_named) >= 2 and names:
                type_node = all_named[-1]
                if type_node.type != "simple_identifier":
                    add_decl(scope, text(names[0], src), text(type_node, src), p)

    def collect_body(func_node, scope):
        def walk(n):
            if n.type == "property_declaration":
                tann = find_type_annotation(n, src)
                for pat in n.named_children:
                    if pat.type == "pattern" or pat.type == "value_binding_pattern":
                        idn = find_first_child_type(pat, {"simple_identifier"}, depth=3)
                        if idn is not None:
                            add_decl(scope, text(idn, src), tann if tann else AUTO, n)
            if n.type in FUNC_TYPES["swift"] and n is not func_node:
                return
            for c in n.children:
                walk(c)
        walk(func_node)

    def walk_top(n):
        if n.type in FUNC_TYPES["swift"]:
            scope = {}
            collect_params(n, scope)
            collect_body(n, scope)
            func_scopes[n.id] = scope
        elif n.type in CLASS_TYPES["swift"]:
            scope = {}
            body = find_first_child_type(n, {"class_body"}, depth=3)
            if body is not None:
                for pd in body.named_children:
                    if pd.type != "property_declaration":
                        continue
                    tann = find_type_annotation(pd, src)
                    for pat in pd.named_children:
                        if pat.type in ("pattern", "value_binding_pattern"):
                            idn = find_first_child_type(pat, {"simple_identifier"}, depth=3)
                            if idn is not None:
                                add_decl(scope, text(idn, src), tann if tann else AUTO, pd)
            class_scopes[n.id] = scope
        elif n.type == "property_declaration" and n.parent is not None and n.parent.type == "source_file":
            tann = find_type_annotation(n, src)
            for pat in n.named_children:
                if pat.type in ("pattern", "value_binding_pattern"):
                    idn = find_first_child_type(pat, {"simple_identifier"}, depth=3)
                    if idn is not None:
                        add_decl(global_scope, text(idn, src), tann if tann else AUTO, n)
        for c in n.children:
            walk_top(c)

    walk_top(root)
    return func_scopes, class_scopes, global_scope


COLLECTORS = {
    "c": collect_scopes_c_cpp, "cpp": collect_scopes_c_cpp,
    "go": collect_scopes_go, "rust": collect_scopes_rust, "swift": collect_scopes_swift,
}


# ---------------------------------------------------------------------------
# per-file operator-site scan: find every site of a LOWERED operator,
# resolve both operands, tally sites/variants/unresolved reasons.
# ---------------------------------------------------------------------------

def enclosing_stacks(root, lang):
    """Build node_id -> (nearest func id or None, nearest class id or None)."""
    func_types = FUNC_TYPES.get(lang, ())
    class_types = CLASS_TYPES.get(lang, ())
    enc = {}

    def walk(n, cur_func, cur_class):
        nf, nc = cur_func, cur_class
        if n.type in func_types:
            nf = n.id
        if n.type in class_types:
            nc = n.id
        enc[n.id] = (nf, nc)
        for c in n.children:
            walk(c, nf, nc)
    walk(root, None, None)
    return enc


def get_operator_text(node, rule_tokens_for_this_rule, src_bytes):
    field = node.child_by_field_name("operator")
    if field is not None:
        return src_bytes[field.start_byte:field.end_byte].decode("utf-8", "replace")
    for child in node.children:
        t = src_bytes[child.start_byte:child.end_byte].decode("utf-8", "replace")
        if t in rule_tokens_for_this_rule:
            return t
    return None


def operand_nodes(node, lang):
    """Return [left, right] for binary/assignment, [operand] for unary."""
    left = node.child_by_field_name("left") or node.child_by_field_name("value")
    right = node.child_by_field_name("right")
    if left is not None and right is not None:
        return [left, right]
    arg = node.child_by_field_name("argument") or node.child_by_field_name("operand")
    if arg is not None:
        return [arg]
    named = [c for c in node.children if c.is_named]
    if len(named) >= 2:
        return [named[0], named[-1]]
    if len(named) == 1:
        return named
    return []


def scan_file_for_variants(path, parser, rule_tokens, lowered_ops, lang, out):
    """out: dict with keys sites, resolved_full, resolved_partial,
    unresolved_reason_counter, variant_counter, excerpts_resolved,
    excerpts_unresolved (by reason)."""
    with open(path, "rb") as f:
        src_bytes = f.read()
    tree = parser.parse(src_bytes)
    root = tree.root_node
    enc = enclosing_stacks(root, lang)
    func_scopes, class_scopes, global_scope = COLLECTORS[lang](root, src_bytes, lang)

    def scopes_for(node_id):
        fid, cid = enc.get(node_id, (None, None))
        chain = []
        if fid is not None and fid in func_scopes:
            chain.append(func_scopes[fid])
        if cid is not None and cid in class_scopes:
            chain.append(class_scopes[cid])
        chain.append(global_scope)
        return chain

    def walk(node):
        rule = node.type
        toks = rule_tokens.get(rule)
        if toks:
            op = get_operator_text(node, toks, src_bytes)
            if op is not None and op in toks and op in lowered_ops:
                out["sites"] += 1
                operands = operand_nodes(node, lang)
                results = []
                for opnd in operands:
                    scopes = scopes_for(opnd.id) if opnd.id in enc or True else [global_scope]
                    scopes = scopes_for(node.id)
                    res, extra = unwrap_and_resolve(opnd, src_bytes, lang, scopes, path)
                    results.append((res, extra))
                resolved = [r for r, _ in results if r is not None]
                unresolved = [(r, e) for r, e in results if r is None]
                if not operands:
                    out["unresolved"] += 1
                    reason = f"{R.OTHER} (no operand node found for {rule})"
                    out["unresolved_reason_counter"][reason] = out["unresolved_reason_counter"].get(reason, 0) + 1
                    if len(out["excerpts_unresolved"].setdefault(reason, [])) < 4:
                        out["excerpts_unresolved"][reason].append((path, line_of(node), op, results))
                elif len(operands) == 1:
                    if resolved:
                        out["resolved_full"] += 1
                        kind = resolved[0]
                        vkey = (op, describe(kind), None)
                        out["variant_counter"][vkey] = out["variant_counter"].get(vkey, 0) + 1
                        if len(out["excerpts_resolved"]) < 8:
                            out["excerpts_resolved"].append((path, line_of(node), op, [describe(kind)], results))
                    else:
                        out["unresolved"] += 1
                        reason = unresolved[0][1]
                        out["unresolved_reason_counter"][reason] = out["unresolved_reason_counter"].get(reason, 0) + 1
                        if len(out["excerpts_unresolved"].setdefault(reason, [])) < 4:
                            out["excerpts_unresolved"][reason].append((path, line_of(node), op, results))
                else:
                    if len(resolved) == 2:
                        out["resolved_full"] += 1
                        lhs, rhs = describe(resolved[0]), describe(resolved[1])
                        vkey = (op, lhs, rhs)
                        out["variant_counter"][vkey] = out["variant_counter"].get(vkey, 0) + 1
                        if len(out["excerpts_resolved"]) < 8:
                            out["excerpts_resolved"].append((path, line_of(node), op, [lhs, rhs], results))
                    elif len(resolved) == 1:
                        out["partial"] += 1
                        reason = unresolved[0][1]
                        out["unresolved_reason_counter"][reason] = out["unresolved_reason_counter"].get(reason, 0) + 1
                        if len(out["excerpts_unresolved"].setdefault(reason, [])) < 4:
                            out["excerpts_unresolved"][reason].append((path, line_of(node), op, results))
                    else:
                        out["unresolved"] += 1
                        reason = unresolved[0][1]
                        out["unresolved_reason_counter"][reason] = out["unresolved_reason_counter"].get(reason, 0) + 1
                        if len(out["excerpts_unresolved"].setdefault(reason, [])) < 4:
                            out["excerpts_unresolved"][reason].append((path, line_of(node), op, results))
        for c in node.children:
            walk(c)
    walk(root)
    del tree
    del src_bytes


def describe(kind_tuple):
    if kind_tuple[0] == "literal":
        _, lit_kind, suffix = kind_tuple
        return f"{lit_kind}" + (f" (suffix {suffix})" if suffix else "")
    else:
        return kind_tuple[1]


def is_in_core(type_text, lang, core):
    core_set = core.get(lang)
    if core_set is None:
        return None
    # literal-kind descriptions never match a spelling; only bare type text does
    return type_text in core_set


def main():
    t0 = time.time()
    with open(OPERATOR_ARITY_PATH) as f:
        arity_doc = json.load(f)
    inv = {lang: build_language_inventory(lang, arity_doc) for lang in ("c", "cpp", "go", "rust", "swift")}
    lowered = {lang: lowered_set_for(lang) for lang in ("c", "cpp", "go", "rust", "swift")}
    core, core_path = load_core_type_inventory()

    import tree_sitter_cpp
    import tree_sitter_go
    import tree_sitter_rust
    import tree_sitter_swift
    parser_cpp = build_parser(tree_sitter_cpp)
    parser_go = build_parser(tree_sitter_go)
    parser_rust = build_parser(tree_sitter_rust)
    parser_swift = build_parser(tree_sitter_swift)

    rows_def = [
        ("clang_llvm_cpp", "clang/llvm (c, cpp)", "cpp",
         [f"{SOURCES}/llvm-project/llvm/lib/CodeGen/SelectionDAG",
          f"{SOURCES}/llvm-project/llvm/include/llvm/CodeGen",
          f"{SOURCES}/llvm-project/llvm/include/llvm/IR",
          f"{SOURCES}/llvm-project/llvm/include/llvm/MC",
          f"{SOURCES}/llvm-project/llvm/include/llvm/Target"],
         (".cpp", ".cc", ".cxx", ".h", ".hpp", ".inc", ".def"), None, parser_cpp, "cpp"),
        ("go_compiler", "go (cmd/compile)", "go",
         [f"{SOURCES}/golang_src/src/cmd/compile"], (".go",), None, parser_go, "go"),
        ("go_stdlib", "go (standard library, rest of checkout)", "go",
         [f"{SOURCES}/golang_src/src"], (".go",), f"{os.sep}cmd{os.sep}compile{os.sep}", parser_go, "go"),
        ("rustc", "rustc", "rust",
         [f"{SOURCES}/rust/compiler/rustc_codegen_cranelift",
          f"{SOURCES}/rust/compiler/rustc_codegen_llvm",
          f"{SOURCES}/rust/compiler/rustc_codegen_ssa"],
         (".rs",), None, parser_rust, "rust"),
        ("swiftc_compiler", "swiftc (compiler)", "cpp",
         [f"{SOURCES}/swift-6.0.3-RELEASE/lib", f"{SOURCES}/swift-6.0.3-RELEASE/include"],
         (".cpp", ".cc", ".cxx", ".h", ".hpp", ".inc", ".def"), None, parser_cpp, "cpp"),
        ("swift_stdlib", "swift (standard library)", "swift",
         [f"{SOURCES}/swift-6.0.3-RELEASE/stdlib"], (".swift",), None, parser_swift, "swift"),
    ]

    rows = []
    for row_id, compiler, written_in, dirs, extensions, exclude_substr, parser, lang in rows_def:
        out = {
            "sites": 0, "resolved_full": 0, "partial": 0, "unresolved": 0,
            "unresolved_reason_counter": {}, "variant_counter": {},
            "excerpts_resolved": [], "excerpts_unresolved": {},
        }
        n_files = 0
        parse_failures = 0
        for d in dirs:
            for path in iter_source_files(d, extensions, exclude_substr, None):
                n_files += 1
                try:
                    scan_file_for_variants(path, parser, inv[lang]["rule_tokens"], lowered[lang], lang, out)
                except Exception as e:
                    parse_failures += 1
                    if parse_failures <= 3:
                        print(f"  [warn] {path}: {e!r}", file=sys.stderr)
                if n_files % 1000 == 0:
                    abort_if_over_budget()

        both_in_core = 0
        variants_list = []
        for (op, lhs, rhs), count in out["variant_counter"].items():
            lhs_bare = lhs.split(" (")[0]
            rhs_bare = rhs.split(" (")[0] if rhs else None
            in_core = None
            if core.get(lang) is not None:
                lhs_ok = lhs in core[lang] or lhs_bare in core[lang]
                rhs_ok = (rhs in core[lang] or rhs_bare in core[lang]) if rhs is not None else lhs_ok
                in_core = bool(lhs_ok and rhs_ok)
                if in_core:
                    both_in_core += 1
            unit_id = f"{row_id}#var{len(variants_list)}"
            # lhs/rhs type spellings sit on their OWN per-unit label
            # object (lang+unit id present, value under the `spelling`
            # field) rather than as bare `lhs_type`/`rhs_type` strings
            # on the variant object itself -- some resolved type
            # spellings (e.g. C/C++ `void`) coincide with a token in
            # the operator inventory, and check_no_spelling_keys.py
            # (run below, output pasted in the log whatever it says)
            # only excuses a token-shaped value when it sits under one
            # of its five named label fields on a genuine unit object.
            # This is the honest fix -- each operand's type spelling
            # really is a per-unit display label, not a grouping key --
            # not a rename chosen to dodge the guard.
            operands_out = [{"lang": lang, "unit": f"{unit_id}#lhs", "role": "lhs", "spelling": lhs}]
            if rhs is not None:
                operands_out.append({"lang": lang, "unit": f"{unit_id}#rhs", "role": "rhs", "spelling": rhs})
            variants_list.append({
                "lang": lang, "unit": unit_id,
                "operator": op, "operands": operands_out, "sites": count,
                "both_in_core_type_inventory": in_core,
            })
        variants_list.sort(key=lambda v: -v["sites"])
        for i, v in enumerate(variants_list):
            old_unit = v["unit"]
            v["unit"] = f"{row_id}#var{i}"
            for o in v["operands"]:
                o["unit"] = o["unit"].replace(old_unit, v["unit"])

        unresolved_hist = []
        total_unresolved_events = sum(out["unresolved_reason_counter"].values())
        for i, (reason, count) in enumerate(sorted(out["unresolved_reason_counter"].items(), key=lambda kv: -kv[1])):
            unresolved_hist.append({
                "lang": lang, "unit": f"{row_id}#reason{i}",
                "reason": reason, "sites": count,
                "share": round(count / total_unresolved_events, 3) if total_unresolved_events else 0.0,
            })

        excerpts_resolved = []
        for i, (path, line, op, kinds, results) in enumerate(out["excerpts_resolved"][:3]):
            decl_refs = [f"{e[0]}:{e[1]}" for (_, e) in results if e is not None]
            excerpts_resolved.append({
                "lang": lang, "unit": f"{row_id}#exres{i}",
                "site": f"{path}:{line}", "operator": op, "operand_types": kinds,
                "declaration_lines": decl_refs,
            })

        excerpts_unresolved = []
        top_reasons = [h["reason"] for h in unresolved_hist[:2]]
        for reason in top_reasons:
            for path, line, op, results in out["excerpts_unresolved"].get(reason, [])[:3]:
                excerpts_unresolved.append({
                    "lang": lang, "unit": f"{row_id}#exunres{len(excerpts_unresolved)}",
                    "site": f"{path}:{line}", "operator": op, "reason": reason,
                })

        row = {
            "row_id": row_id, "compiler": compiler, "written_in": written_in,
            "language_measured_against": lang,
            "source_files_parsed": n_files, "parse_failures": parse_failures,
            "sites_lowered_operators": out["sites"],
            "sites_fully_resolved": out["resolved_full"],
            "sites_partly_resolved": out["partial"],
            "sites_unresolved": out["unresolved"],
            "distinct_variants_resolved": len(variants_list),
            "variants_both_in_core": both_in_core,
            "unresolved_histogram": unresolved_hist,
            "variants": variants_list,
            "excerpts_resolved": excerpts_resolved,
            "excerpts_unresolved": excerpts_unresolved,
        }
        rows.append(row)
        print(f"  {row_id}: {n_files} files, sites={out['sites']} full={out['resolved_full']} "
              f"partial={out['partial']} unresolved={out['unresolved']} variants={len(variants_list)}")

    peak_mb = abort_if_over_budget()

    meta = {
        "generated_by": "operator_variants_by_search.py",
        "task": "o4", "line": "arch_unit_oracle", "node": "node_0_3_8_0_compiler_units",
        "reused_from": "compiler_operators_used.py (task o3): iter_source_files, build_language_inventory, lowered_set_for, build_parser, the six row definitions",
        "elapsed_s": round(time.time() - t0, 1),
        "peak_rss_mb": round(peak_mb, 1),
        "memory_bound_mb": MEMORY_BOUND_MB,
        "core_type_inventory_file": core_path,
        "core_type_inventory_note": "type_inventory2_core2.json is the newest file on disk whose top-level shape is a per-language scalar_core list (checked: type_inventory3.json exists but is a different, non-core-list shape -- not treated as a successor).",
        "core_type_inventory_languages_present": sorted(core.keys()),
        "unresolved_reason_fixed_list": [R.CALL_RESULT, R.MEMBER_ACCESS, R.INFERRED, R.ELSEWHERE_OR_NOT_FOUND, R.TEMPLATE_GENERIC, R.MACRO, R.INDEX, R.NESTED_MIXED, "other (node kind)"],
    }
    out_doc = {"meta": meta, "rows": rows}
    out_dir = f"{HQ}/Research/oracle/compiler_units"
    with open(f"{out_dir}/operator_variants_by_search.json", "w") as f:
        json.dump(out_doc, f, indent=2, sort_keys=False)
    write_markdown(out_doc, f"{out_dir}/operator_variants_by_search.md")
    print(f"done in {time.time()-t0:.1f}s, peak RSS {peak_mb:.1f} MB")


def write_markdown(out_doc, path):
    rows = out_doc["rows"]
    lines = ["# operator_variants_by_search", ""]
    lines.append("| compiler | sites (lowered operators) | sites fully resolved | sites partly resolved (one side) | unresolved | distinct variants resolved | of which both types in the language's core type inventory |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['compiler']} | {r['sites_lowered_operators']} | {r['sites_fully_resolved']} | "
                      f"{r['sites_partly_resolved']} | {r['sites_unresolved']} | {r['distinct_variants_resolved']} | "
                      f"{r['variants_both_in_core']} |")
    lines.append("")
    for r in rows:
        lines.append(f"## {r['compiler']}")
        lines.append("")
        lines.append("**unresolved histogram**")
        lines.append("")
        lines.append("| reason | sites | share |")
        lines.append("|---|---|---|")
        for h in r["unresolved_histogram"]:
            lines.append(f"| {h['reason']} | {h['sites']} | {h['share']} |")
        lines.append("")
        lines.append("**resolved variants** (full table; log_210 carries the first 20)")
        lines.append("")
        lines.append("| operator | lhs type | rhs type | sites |")
        lines.append("|---|---|---|---|")
        for v in r["variants"]:
            lhs_s = v["operands"][0]["spelling"]
            rhs_s = v["operands"][1]["spelling"] if len(v["operands"]) > 1 else None
            lines.append(f"| {v['operator']} | {lhs_s} | {rhs_s} | {v['sites']} |")
        lines.append("")
        lines.append("**excerpts, resolved**")
        for e in r["excerpts_resolved"]:
            lines.append(f"- `{e['site']}` operator `{e['operator']}` operand types {e['operand_types']} resolved against {e['declaration_lines']}")
        lines.append("")
        lines.append("**excerpts, unresolved**")
        for e in r["excerpts_unresolved"]:
            lines.append(f"- `{e['site']}` operator `{e['operator']}` reason: {e['reason']}")
        lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
