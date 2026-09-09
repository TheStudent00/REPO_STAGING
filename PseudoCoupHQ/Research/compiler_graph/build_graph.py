#!/usr/bin/env python3
# SUPERSEDED RECORD (2026-09-03, task 71): graph.py is the deliverable of plan node hq.research.compiler_graph.graph; this file is kept as the record of its lap and is no longer run.
"""build_graph.py -- static layer of the compiler-graph instrument (lap one).

Parses a bounded REGION of the Go compiler's own source with tree-sitter-go and
emits graph_go.json: nodes (declarations + references), typed edges
(resolves_to / flows_into / calls) and frontier records.

Vocabulary: structural relations are super-node / sub-node / co-node / sub-tree,
higher / lower. Botanical terms (root, leaf, branch, tree) are used freely.

Pins of record (asserted at run time):
  tree-sitter    == 0.26.0
  tree-sitter-go == 0.25.0

Resolution scope (lap one, deliberately bounded):
  * same-file lexical scoping (function scope, block scope, func literals)
  * same-package (= same directory) top-level names
Anything else is a frontier record, never a guess.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

import tree_sitter_go
from tree_sitter import Language, Parser

try:  # importlib.metadata is the pin witness
    from importlib.metadata import version as _pkg_version
except ImportError:  # pragma: no cover
    _pkg_version = None

GO_LANG = Language(tree_sitter_go.language())

# ---------------------------------------------------------------- region ----

COMPILE_ROOT = "src/cmd/compile"

# Whole packages taken in (non-test files only).
WHOLE_PACKAGES = [
    "internal/ssagen",
    "internal/abi",
    "internal/amd64",
]
# ssa is huge (13 MB, mostly generated rewrite tables), so it is taken by rule.
SSA_PACKAGE = "internal/ssa"


def in_region(pkg_rel: str, fname: str, is_generated: bool) -> bool:
    """Region membership rule, applied per file."""
    if fname.endswith("_test.go") or not fname.endswith(".go"):
        return False
    if pkg_rel in WHOLE_PACKAGES:
        return True
    if pkg_rel == SSA_PACKAGE:
        # brief's named targets, plus every hand-written ssa file (the generated
        # rewrite*.go tables are ~12 MB of machine output and are excluded).
        if fname.startswith("op") or fname == "expand_calls.go":
            return True
        return not is_generated
    return False


def collect_region(go_src_root: str):
    """Return list of (abs_path, pkg_rel, fname, is_generated)."""
    base = os.path.join(go_src_root, COMPILE_ROOT)
    out = []
    for pkg_rel in WHOLE_PACKAGES + [SSA_PACKAGE]:
        d = os.path.join(base, pkg_rel)
        if not os.path.isdir(d):
            sys.stderr.write("region: missing directory %s\n" % d)
            continue
        for fname in sorted(os.listdir(d)):
            p = os.path.join(d, fname)
            if not os.path.isfile(p) or not fname.endswith(".go"):
                continue
            gen = file_is_generated(p)
            if in_region(pkg_rel, fname, gen):
                out.append((p, pkg_rel, fname, gen))
    return out


def file_is_generated(path: str) -> bool:
    try:
        with open(path, "rb") as fh:
            head = fh.read(4096).decode("utf-8", "replace")
    except OSError:
        return False
    for line in head.splitlines()[:8]:
        if "Code generated" in line and "DO NOT EDIT" in line:
            return True
    return False


# ------------------------------------------------------------- universe ----

GO_UNIVERSE = {
    "append", "cap", "clear", "close", "complex", "copy", "delete", "imag",
    "len", "make", "max", "min", "new", "panic", "print", "println", "real",
    "recover", "bool", "byte", "complex64", "complex128", "error", "float32",
    "float64", "int", "int8", "int16", "int32", "int64", "rune", "string",
    "uint", "uint8", "uint16", "uint32", "uint64", "uintptr", "any", "true",
    "false", "iota", "nil", "comparable", "_",
}

DECL_KINDS = {
    "func", "method", "type", "package_var", "package_const", "param",
    "result_param", "receiver", "local_var", "local_const", "type_param",
    "label",
}


# ------------------------------------------------------------- the graph ----

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.frontier = []
        self._edge_seen = set()

    def add_node(self, nid, kind, name, file, sb, eb, sl, el, extra=None):
        if nid not in self.nodes:
            n = {
                "id": nid, "kind": kind, "name": name, "file": file,
                "start_byte": sb, "end_byte": eb,
                "start_line": sl, "end_line": el,
            }
            if extra:
                n.update(extra)
            self.nodes[nid] = n
        return nid

    def add_edge(self, src, dst, etype, **extra):
        if src is None or dst is None:
            return
        key = (src, dst, etype, extra.get("kind"))
        if key in self._edge_seen:
            return
        self._edge_seen.add(key)
        e = {"src": src, "dst": dst, "type": etype}
        e.update(extra)
        self.edges.append(e)

    def add_frontier(self, fid, kind, file, span, detail, extra=None):
        if fid in self.nodes:
            return fid
        rec = {"id": fid, "kind": kind, "file": file, "span": span,
               "detail": detail}
        if extra:
            rec.update(extra)
        self.frontier.append(rec)
        # frontier records are also terminal nodes, so a path query can END on
        # one and name it as the reason a branch died.
        self.add_node(fid, kind, detail, file, span[0], span[1],
                      span[2], span[3], {"frontier": True})
        return fid


def nid(rel, node, kind):
    return "%s:%d-%d:%s" % (rel, node.start_byte, node.end_byte, kind)


def txt(src, node):
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def spans(node):
    return (node.start_byte, node.end_byte,
            node.start_point[0] + 1, node.end_point[0] + 1)


# --------------------------------------------------------------- pass one ----

def named_children(node, typ):
    return [c for c in node.named_children if c.type == typ]


def spec_names(spec):
    """Names declared by a var_spec / const_spec / type_spec / type_alias."""
    out = []
    for c in spec.children:
        if c.type == "identifier" and (spec.field_name_for_child(
                spec.children.index(c)) in ("name", None)):
            out.append(c)
        elif c.type == "expression_list":
            break
    # field-based extraction is more reliable where available
    fielded = [spec.child_by_field_name("name")]
    fielded = [f for f in fielded if f is not None]
    if fielded and not out:
        out = fielded
    return out


def top_level_decls(graph, rel, src, root):
    """Collect this file's package-level declarations. Returns {name: node_id}."""
    table = {}

    def decl(node, name_node, kind):
        if name_node is None:
            return
        name = txt(src, name_node)
        sb, eb, sl, el = spans(node)
        i = graph.add_node(nid(rel, node, kind), kind, name, rel, sb, eb, sl, el)
        if name != "_":
            table.setdefault(name, i)
        return i

    for ch in root.named_children:
        t = ch.type
        if t == "function_declaration":
            decl(ch, ch.child_by_field_name("name"), "func")
        elif t == "method_declaration":
            decl(ch, ch.child_by_field_name("name"), "method")
        elif t == "type_declaration":
            for spec in ch.named_children:
                if spec.type in ("type_spec", "type_alias"):
                    decl(spec, spec.child_by_field_name("name"), "type")
        elif t in ("var_declaration", "const_declaration"):
            kind = "package_var" if t == "var_declaration" else "package_const"
            for spec in ch.named_children:
                if spec.type in ("var_spec", "const_spec",
                                 "var_spec_list", "const_spec_list"):
                    for nm in spec.children:
                        if nm.type == "identifier":
                            decl(spec, nm, kind)
                        elif nm.type in ("expression_list", "=", ":="):
                            break
    return table


def collect_imports(src, root):
    """{local package name: import path} for one file."""
    imports = {}
    for ch in root.named_children:
        if ch.type != "import_declaration":
            continue
        stack = [ch]
        while stack:
            n = stack.pop()
            if n.type == "import_spec":
                path = txt(src, n.child_by_field_name("path")).strip('"')
                alias = n.child_by_field_name("name")
                local = txt(src, alias) if alias is not None \
                    else path.rsplit("/", 1)[-1]
                imports[local] = path
            else:
                stack.extend(n.named_children)
    return imports


# --------------------------------------------------------------- pass two ----

class FileWalker:
    """Walks one file, emitting reference nodes, dataflow and call edges."""

    def __init__(self, graph, rel, src, root, pkg_table, imports, generated,
                 method_index=None, pkg_tables=None, path_to_pkg=None):
        self.g = graph
        self.rel = rel
        self.src = src
        self.root = root
        self.pkg_table = pkg_table
        self.imports = imports
        self.generated = generated
        # name -> [method node ids] within this package; a selector call whose
        # receiver type is unknown in lap one resolves to this CANDIDATE SET
        # (log_072 section 4: the set, never a guess).
        self.method_index = method_index or {}
        # other parsed packages, for cross-package references we CAN follow
        self.pkg_tables = pkg_tables or {}
        self.path_to_pkg = path_to_pkg or {}
        self.scopes = []            # list of {name: node_id}
        self.func_kinds = {}        # node_id -> kind, for candidate sets
        self.candidates = {}        # local var node_id -> set(func node ids)

    # -- scope helpers -----------------------------------------------------
    def push(self):
        self.scopes.append({})

    def pop(self):
        self.scopes.pop()

    def bind(self, name, node_id):
        if name != "_" and self.scopes:
            self.scopes[-1][name] = node_id

    def lookup(self, name):
        for sc in reversed(self.scopes):
            if name in sc:
                return sc[name]
        return self.pkg_table.get(name)

    # -- node factories ----------------------------------------------------
    def decl_node(self, node, name, kind):
        sb, eb, sl, el = spans(node)
        i = self.g.add_node(nid(self.rel, node, kind), kind, name, self.rel,
                            sb, eb, sl, el)
        self.bind(name, i)
        return i

    def ref_node(self, node, name):
        sb, eb, sl, el = spans(node)
        return self.g.add_node(nid(self.rel, node, "ref"), "ref", name,
                               self.rel, sb, eb, sl, el)

    # -- reference resolution ---------------------------------------------
    def resolve_ident(self, node):
        """Emit a ref node for an identifier and its resolves_to edge.

        Returns (ref_id, target_id_or_None).
        """
        name = txt(self.src, node)
        if name in GO_UNIVERSE:
            return (None, None)
        r = self.ref_node(node, name)
        tgt = self.lookup(name)
        if tgt is not None:
            self.g.add_edge(r, tgt, "resolves_to")
            return (r, tgt)
        sb, eb, sl, el = spans(node)
        f = self.g.add_frontier(
            "frontier:%s:%d-%d:unresolved_import" % (self.rel, sb, eb),
            "unresolved_import", self.rel, (sb, eb, sl, el), name,
            {"selector": name, "reason": "name not in file scope or package"})
        self.g.add_edge(r, f, "resolves_to", kind="frontier")
        return (r, f)

    def resolve_selector(self, node):
        """selector_expression. Returns (ref_id, target_id_or_None)."""
        operand = node.child_by_field_name("operand")
        field = node.child_by_field_name("field")
        sel_text = txt(self.src, node)
        if operand is not None and operand.type == "identifier":
            base = txt(self.src, operand)
            if base in self.imports and self.lookup(base) is None:
                sb, eb, sl, el = spans(node)
                r = self.ref_node(node, sel_text)
                # cross-package, but the named package may itself be inside the
                # parsed region -- then the reference is followed, not guessed.
                other = self.path_to_pkg.get(self.imports[base])
                fname = txt(self.src, field) if field is not None else None
                if other is not None and fname:
                    tgt = self.pkg_tables.get(other, {}).get(fname)
                    if tgt is not None:
                        self.g.add_edge(r, tgt, "resolves_to",
                                        kind="cross_package_in_region")
                        return (r, tgt)
                f = self.g.add_frontier(
                    "frontier:%s:%d-%d:unresolved_import" % (self.rel, sb, eb),
                    "unresolved_import", self.rel, (sb, eb, sl, el), sel_text,
                    {"selector": sel_text, "import_path": self.imports[base]})
                self.g.add_edge(r, f, "resolves_to", kind="frontier")
                return (r, f)
        # x.Field / x.Method on a local or package value: resolve the base only.
        base_ref = None
        if operand is not None:
            base_ref, _ = self.expr_refs_single(operand)
        r = self.ref_node(node, sel_text)
        if base_ref:
            self.g.add_edge(base_ref, r, "flows_into", kind="selector_base")
        sb, eb, sl, el = spans(node)
        fname = txt(self.src, field) if field is not None else None
        cands = self.method_index.get(fname, []) if fname else []
        if cands:
            for c in cands:
                self.g.add_edge(r, c, "resolves_to", kind="method_candidate",
                                one_to_many=len(cands) > 1,
                                candidate_set=cands)
            return (r, cands[0] if len(cands) == 1 else r)
        f = self.g.add_frontier(
            "frontier:%s:%d-%d:unresolved_import" % (self.rel, sb, eb),
            "unresolved_import", self.rel, (sb, eb, sl, el), sel_text,
            {"selector": sel_text,
             "reason": "field or method selector; no type information in lap one",
             "field": txt(self.src, field) if field is not None else None})
        self.g.add_edge(r, f, "resolves_to", kind="frontier")
        return (r, f)

    def expr_refs_single(self, node):
        got = self.expr_refs(node)
        return (got[0] if got else (None, None))

    def expr_refs(self, node):
        """Walk an expression, emitting refs/calls. Returns [(ref,target)]."""
        out = []
        if node is None:
            return out
        t = node.type
        if t == "identifier":
            got = self.resolve_ident(node)
            if got[0]:
                out.append(got)
            return out
        if t == "selector_expression":
            got = self.resolve_selector(node)
            if got[0]:
                out.append(got)
            return out
        if t == "call_expression":
            cid = self.handle_call(node)
            if cid:
                out.append((cid, None))
            return out
        if t == "func_literal":
            self.handle_func_literal(node)
            return out
        if t in ("type_identifier", "field_identifier", "package_identifier",
                 "interpreted_string_literal", "raw_string_literal",
                 "int_literal", "float_literal", "rune_literal",
                 "true", "false", "nil"):
            return out
        for c in node.named_children:
            out.extend(self.expr_refs(c))
        return out

    # -- calls -------------------------------------------------------------
    def handle_call(self, node):
        fn = node.child_by_field_name("function")
        args = node.child_by_field_name("arguments")
        sb, eb, sl, el = spans(node)
        callee_text = txt(self.src, fn) if fn is not None else "?"
        cid = self.g.add_node(nid(self.rel, node, "call"), "call", callee_text,
                              self.rel, sb, eb, sl, el)
        if fn is not None:
            if fn.type == "identifier":
                name = txt(self.src, fn)
                if name not in GO_UNIVERSE:
                    ref, tgt = self.resolve_ident(fn)
                    if tgt is not None:
                        tk = self.g.nodes[tgt]["kind"]
                        if tk in ("func", "method"):
                            self.g.add_edge(cid, tgt, "calls", kind="direct")
                        elif tk in ("param", "local_var", "package_var",
                                    "result_param", "receiver"):
                            self.indirect_call(cid, tgt, node)
                        else:
                            self.g.add_edge(cid, tgt, "calls", kind="direct")
            elif fn.type == "selector_expression":
                ref, tgt = self.resolve_selector(fn)
                fld = fn.child_by_field_name("field")
                fldname = txt(self.src, fld) if fld is not None else None
                cands = self.method_index.get(fldname, []) if fldname else []
                if cands:
                    # method dispatch without type information: the CANDIDATE
                    # SET of same-package methods of that name (log_072 s4).
                    for c in cands:
                        self.g.add_edge(cid, c, "calls", kind="indirect",
                                        one_to_many=len(cands) > 1,
                                        candidate_set=cands,
                                        basis="same-package method name")
                elif tgt is not None and self.g.nodes[tgt]["kind"] in (
                        "func", "method"):
                    self.g.add_edge(cid, tgt, "calls",
                                    kind="cross_package_in_region")
                elif tgt is not None:
                    self.g.add_edge(cid, tgt, "calls", kind="indirect")
            else:
                self.expr_refs(fn)
                f = self.g.add_frontier(
                    "frontier:%s:%d-%d:unresolved_indirect" % (self.rel, sb, eb),
                    "unresolved_indirect", self.rel, (sb, eb, sl, el),
                    callee_text,
                    {"reason": "callee is a computed expression"})
                self.g.add_edge(cid, f, "calls", kind="indirect")
        # arguments flow into the call node
        if args is not None:
            for a in args.named_children:
                for (r, _t) in self.expr_refs(a):
                    self.g.add_edge(r, cid, "flows_into", kind="argument")
        return cid

    def indirect_call(self, cid, holder_id, node):
        """Call through a variable holding a function value: candidate SET."""
        cand = sorted(self.candidates.get(holder_id, ()))
        if cand:
            for c in cand:
                self.g.add_edge(cid, c, "calls", kind="indirect",
                                one_to_many=True, holder=holder_id,
                                candidate_set=cand)
        else:
            sb, eb, sl, el = spans(node)
            f = self.g.add_frontier(
                "frontier:%s:%d-%d:unresolved_indirect" % (self.rel, sb, eb),
                "unresolved_indirect", self.rel, (sb, eb, sl, el),
                txt(self.src, node)[:120],
                {"holder": holder_id,
                 "reason": "no function value stored into the holder within the region"})
            self.g.add_edge(cid, f, "calls", kind="indirect")

    def note_candidate(self, holder_id, rhs_node):
        """Record function values stored into a holder (for candidate sets)."""
        if holder_id is None or rhs_node is None:
            return
        stack = [rhs_node]
        while stack:
            n = stack.pop()
            if n.type == "identifier":
                t = self.lookup(txt(self.src, n))
                if t and self.g.nodes.get(t, {}).get("kind") in ("func", "method"):
                    self.candidates.setdefault(holder_id, set()).add(t)
            elif n.type in ("composite_literal", "literal_value",
                            "keyed_element", "literal_element",
                            "expression_list", "parenthesized_expression"):
                stack.extend(n.named_children)

    # -- declarations inside a function ------------------------------------
    def bind_params(self, plist, kind):
        ids = []
        if plist is None:
            return ids
        for p in plist.named_children:
            if p.type not in ("parameter_declaration",
                              "variadic_parameter_declaration"):
                continue
            names = [c for c in p.children if c.type == "identifier"]
            ptype = p.child_by_field_name("type")
            if ptype is not None:
                self.type_refs(ptype)
            if not names:
                continue
            for nm in names:
                ids.append(self.decl_node(nm, txt(self.src, nm), kind))
        return ids

    def type_refs(self, node):
        """References that appear inside a type expression."""
        if node is None:
            return
        if node.type in ("type_identifier", "identifier"):
            name = txt(self.src, node)
            if name not in GO_UNIVERSE:
                r = self.ref_node(node, name)
                tgt = self.lookup(name)
                if tgt is not None:
                    self.g.add_edge(r, tgt, "resolves_to", kind="type")
            return
        if node.type == "qualified_type":
            pkg = node.child_by_field_name("package")
            if pkg is not None:
                base = txt(self.src, pkg)
                sb, eb, sl, el = spans(node)
                sel = txt(self.src, node)
                r = self.ref_node(node, sel)
                nm = node.child_by_field_name("name")
                other = self.path_to_pkg.get(self.imports.get(base))
                if other is not None and nm is not None:
                    tgt = self.pkg_tables.get(other, {}).get(txt(self.src, nm))
                    if tgt is not None:
                        self.g.add_edge(r, tgt, "resolves_to",
                                        kind="cross_package_type_in_region")
                        return
                f = self.g.add_frontier(
                    "frontier:%s:%d-%d:unresolved_import" % (self.rel, sb, eb),
                    "unresolved_import", self.rel, (sb, eb, sl, el), sel,
                    {"selector": sel,
                     "import_path": self.imports.get(base),
                     "reason": "cross-package type"})
                self.g.add_edge(r, f, "resolves_to", kind="type")
            return
        for c in node.named_children:
            self.type_refs(c)

    # -- statements --------------------------------------------------------
    def lhs_target(self, node, declaring, kind="local_var"):
        """Return the node id an lhs expression assigns into."""
        if node.type == "identifier":
            name = txt(self.src, node)
            if declaring:
                return self.decl_node(node, name, kind)
            ref, tgt = self.resolve_ident(node)
            return tgt if tgt is not None else ref
        got = self.expr_refs(node)
        return got[0][0] if got else None

    def assignment(self, lhs_nodes, rhs_nodes, declaring, kind="local_var"):
        rhs_results = []
        for rn in rhs_nodes:
            rhs_results.append((rn, self.expr_refs(rn)))
        targets = [self.lhs_target(l, declaring, kind) for l in lhs_nodes]
        for tgt in targets:
            if tgt is None:
                continue
            for (rn, refs) in rhs_results:
                for (r, _t) in refs:
                    etype_kind = "call_result" \
                        if self.g.nodes.get(r, {}).get("kind") == "call" else "value"
                    self.g.add_edge(r, tgt, "flows_into", kind=etype_kind)
                self.note_candidate(tgt, rn)

    def handle_func_literal(self, node):
        self.push()
        self.bind_params(node.child_by_field_name("parameters"), "param")
        res = node.child_by_field_name("result")
        if res is not None:
            if res.type == "parameter_list":
                self.bind_params(res, "result_param")
            else:
                self.type_refs(res)
        self.walk(node.child_by_field_name("body"))
        self.pop()

    def walk(self, node):
        if node is None:
            return
        t = node.type

        if t == "block":
            self.push()
            for c in node.named_children:
                self.walk(c)
            self.pop()
            return

        if t == "short_var_declaration":
            self.assignment(
                _list(node.child_by_field_name("left")),
                _list(node.child_by_field_name("right")), True)
            return

        if t == "assignment_statement":
            self.assignment(
                _list(node.child_by_field_name("left")),
                _list(node.child_by_field_name("right")), False)
            return

        if t in ("var_declaration", "const_declaration"):
            kind = "local_var" if t == "var_declaration" else "local_const"
            for spec in node.named_children:
                names = [c for c in spec.children if c.type == "identifier"]
                ty = spec.child_by_field_name("type")
                if ty is not None:
                    self.type_refs(ty)
                val = spec.child_by_field_name("value")
                self.assignment(names, _list(val), True, kind)
            return

        if t == "range_clause":
            left = _list(node.child_by_field_name("left"))
            right = node.child_by_field_name("right")
            declaring = any(c.type == ":=" for c in node.children)
            self.assignment(left, [right] if right is not None else [],
                            declaring)
            return

        if t == "func_literal":
            self.handle_func_literal(node)
            return

        if t == "call_expression":
            self.handle_call(node)
            return

        if t in ("selector_expression", "identifier"):
            self.expr_refs(node)
            return

        if t == "type_declaration":
            for spec in node.named_children:
                ty = spec.child_by_field_name("type")
                self.type_refs(ty)
            return

        for c in node.named_children:
            self.walk(c)

    # -- top of file -------------------------------------------------------
    def run(self):
        self.push()  # file scope (package table consulted after it)
        for ch in self.root.named_children:
            t = ch.type
            if t in ("function_declaration", "method_declaration"):
                name = ch.child_by_field_name("name")
                kind = "func" if t == "function_declaration" else "method"
                fid = nid(self.rel, ch, kind)
                self.push()
                if t == "method_declaration":
                    self.bind_params(ch.child_by_field_name("receiver"),
                                     "receiver")
                self.bind_params(ch.child_by_field_name("parameters"), "param")
                res = ch.child_by_field_name("result")
                if res is not None:
                    if res.type == "parameter_list":
                        self.bind_params(res, "result_param")
                    else:
                        self.type_refs(res)
                # every declaration made inside belongs to this function's
                # sub-tree; the enclosing node id is recorded on each of them
                before = set(self.g.nodes)
                self.walk(ch.child_by_field_name("body"))
                for n in set(self.g.nodes) - before:
                    self.g.nodes[n].setdefault("in_func", fid)
                for p, sc in enumerate(self.scopes):
                    pass
                for n in self.scopes[-1].values():
                    self.g.nodes[n].setdefault("in_func", fid)
                self.pop()
            elif t in ("var_declaration", "const_declaration"):
                if self.generated:
                    continue  # generated tables: declarations only (see report)
                for spec in ch.named_children:
                    names = [c for c in spec.children if c.type == "identifier"]
                    ty = spec.child_by_field_name("type")
                    if ty is not None:
                        self.type_refs(ty)
                    val = spec.child_by_field_name("value")
                    if names and val is not None:
                        targets = [self.pkg_table.get(txt(self.src, n))
                                   for n in names]
                        for (r, _t) in self.expr_refs(val):
                            for tg in targets:
                                self.g.add_edge(r, tg, "flows_into",
                                                kind="value")
                        for tg in targets:
                            self.note_candidate(tg, val)
            elif t == "type_declaration":
                for spec in ch.named_children:
                    self.type_refs(spec.child_by_field_name("type"))
        self.pop()


def _list(node):
    """Normalise an expression_list / single expression into a list."""
    if node is None:
        return []
    if node.type == "expression_list":
        return list(node.named_children)
    return [node]


# ----------------------------------------------------------------- errors ----

def record_parse_errors(graph, rel, src, root):
    n = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if node.type == "ERROR" or node.is_missing:
            sb, eb, sl, el = spans(node)
            graph.add_frontier(
                "frontier:%s:%d-%d:parse_error" % (rel, sb, eb),
                "parse_error", rel, (sb, eb, sl, el),
                txt(src, node)[:160],
                {"missing": bool(node.is_missing)})
            n += 1
            continue
        if node.has_error:
            stack.extend(node.children)
    return n


def scan_nongo_frontiers(graph, go_src_root):
    """Assembly and .rules regions inside cmd/compile: recorded, not parsed."""
    base = os.path.join(go_src_root, COMPILE_ROOT)
    for dirpath, _dirs, files in os.walk(base):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, go_src_root)
            if f.endswith((".s", ".S")):
                graph.add_frontier("frontier:%s:assembly_file" % rel,
                                   "assembly_file", rel, (0, 0, 0, 0), f,
                                   {"reason": "assembly grammar, not lap one"})
            elif f.endswith(".rules"):
                graph.add_frontier("frontier:%s:rules_file" % rel,
                                   "rules_file", rel, (0, 0, 0, 0), f,
                                   {"reason": "private rewrite-rule table format"})


# ------------------------------------------------------------------- main ----

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go-src", required=True,
                    help="root of the Go tree (the dir holding src/)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "graph_go.json")
    parser = Parser(GO_LANG)
    graph = Graph()

    files = collect_region(args.go_src)
    sys.stderr.write("region: %d files\n" % len(files))

    parsed = []
    trees = {}
    pkg_tables = defaultdict(dict)
    parse_errors = 0

    # pass one: declarations, per package
    for path, pkg_rel, fname, gen in files:
        rel = os.path.relpath(path, args.go_src)
        with open(path, "rb") as fh:
            src = fh.read()
        tree = parser.parse(src)
        root = tree.root_node
        parse_errors += record_parse_errors(graph, rel, src, root)
        if gen:
            graph.add_frontier("frontier:%s:generated_code" % rel,
                               "generated_code", rel, (0, len(src), 1,
                                                       src.count(b"\n") + 1),
                               fname,
                               {"reason": "header says Code generated ... DO NOT EDIT",
                                "handling": "declarations recorded; package-level table initialisers not walked"})
        table = top_level_decls(graph, rel, src, root)
        for k, v in table.items():
            pkg_tables[pkg_rel].setdefault(k, v)
        trees[rel] = (src, root, pkg_rel, gen)
        parsed.append({"file": rel, "package_dir": pkg_rel,
                       "bytes": len(src), "generated": gen})

    # method index per package: name -> [method node ids]
    method_index = defaultdict(lambda: defaultdict(list))
    for n in graph.nodes.values():
        if n["kind"] == "method":
            pkg = os.path.dirname(n["file"])
            method_index[pkg][n["name"]].append(n["id"])

    # import path -> package dir, for the packages we actually parsed
    path_to_pkg = {}
    for pkg_rel in WHOLE_PACKAGES + [SSA_PACKAGE]:
        path_to_pkg["cmd/compile/" + pkg_rel] = pkg_rel

    # pass two: references, dataflow, calls
    for rel, (src, root, pkg_rel, gen) in trees.items():
        imports = collect_imports(src, root)
        mi = {k: sorted(v) for k, v in
              method_index[os.path.dirname(rel)].items()}
        FileWalker(graph, rel, src, root, pkg_tables[pkg_rel], imports,
                   gen, mi, pkg_tables, path_to_pkg).run()

    # structural containment: a function/method super-node to the declaration
    # and call sub-nodes inside its sub-tree. Purely structural, so a path
    # query can step from a resolved callee into that callee's body.
    for n in list(graph.nodes.values()):
        holder = n.get("in_func")
        if holder and holder in graph.nodes and n["kind"] in (
                "param", "receiver", "result_param", "local_var",
                "local_const", "call"):
            graph.add_edge(holder, n["id"], "contains")

    scan_nongo_frontiers(graph, args.go_src)

    node_kinds = defaultdict(int)
    for n in graph.nodes.values():
        node_kinds[n["kind"]] += 1
    edge_types = defaultdict(int)
    for e in graph.edges:
        edge_types[e["type"] + ("/" + e["kind"] if e.get("kind") else "")] += 1
    frontier_kinds = defaultdict(int)
    for f in graph.frontier:
        frontier_kinds[f["kind"]] += 1

    doc = {
        "meta": {
            "tool": "compiler_graph/build_graph.py",
            "lap": 1,
            "go_tree": os.path.abspath(args.go_src),
            "pins": {
                "tree-sitter": _pkg_version("tree-sitter") if _pkg_version else "?",
                "tree-sitter-go": _pkg_version("tree_sitter_go") if _pkg_version else "?",
            },
            "region_rule": {
                "whole_packages": WHOLE_PACKAGES,
                "ssa_rule": "op*.go and expand_calls.go always; every other "
                            "hand-written (non-generated) ssa file; generated "
                            "rewrite*.go tables excluded",
                "tests_excluded": True,
            },
            "resolution_scope": "same-file lexical + same-directory package "
                                "top level; anything else is a frontier record",
            "counts": {
                "files_parsed": len(parsed),
                "nodes": len(graph.nodes),
                "edges": len(graph.edges),
                "frontier": len(graph.frontier),
                "parse_errors": parse_errors,
                "node_kinds": dict(sorted(node_kinds.items())),
                "edge_types": dict(sorted(edge_types.items())),
                "frontier_kinds": dict(sorted(frontier_kinds.items())),
            },
        },
        "files_parsed": parsed,
        "nodes": list(graph.nodes.values()),
        "edges": graph.edges,
        "frontier": graph.frontier,
    }
    with open(out, "w") as fh:
        json.dump(doc, fh)
    sys.stderr.write(json.dumps(doc["meta"]["counts"], indent=2) + "\n")
    sys.stderr.write("wrote %s\n" % out)


if __name__ == "__main__":
    main()
