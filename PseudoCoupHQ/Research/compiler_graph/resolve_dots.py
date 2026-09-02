#!/usr/bin/env python3
"""resolve_dots.py -- the SECOND resolution step: the map learns to cross `x.field`.

Lap one stopped at every `state.rUsed` and every `t.Size()`: 20,216 frontier
records with the reason "field or method selector; no type information in lap
one".  This tool closes the ones that can be closed WITHOUT type inference.

Why a co-module and not a change to build_graph.py.  build_graph.py is the
artifact of record for lap one; graph_go.json and every number reported
against it were produced by it, and the acceptance query of lap one is a
result about that file.  A post-processor keeps lap one reproducible and
makes the second step separately measurable: run it, and the difference
between graph_go.json and graph_go2.json IS the answer to "how many of the
20,216 fell".  It re-parses the same region with the same pins rather than
reading types out of the map, because the map records spans and kinds and
never recorded a declared type.

THE RULE, and it is deliberately small.  A `x.f` is crossed only when the
type of `x` is DECLARED and the declaration is IN THE PARSED REGION:

  * `x` is a receiver, a parameter, a result parameter, a `var x T`, a
    package-level `var x T`, or a `x := T{...}` / `x := &T{...}`;
  * one level of wrapping is stripped: `*T`, `[]T`, `[N]T`;
  * `T` is a named type declared in the parsed region, either in the same
    package or in another parsed package named through an import;
  * `f` is then either a field of that type's struct declaration or a
    method whose receiver base type is that type.

A base that is itself a selector is resolved the same way, so `a.b.c` is
crossed when every step of it is declared.  Nothing else.  No inference from
assignments, no interface method sets, no embedded-field promotion, no
generics instantiation.  Where the rule does not apply the lap-one frontier
record STAYS, with its reason unchanged.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

import argparse
import json
import os
import sys
from collections import defaultdict

import build_graph as bg
from tree_sitter import Parser


FIELD_SELECTOR_REASON = "field or method selector; no type information in lap one"

MAX_UNWRAP = 3


# -------------------------------------------------------------- type table --

class TypeTable:
    """Named types declared in the region, their fields and their methods."""

    def __init__(self):
        # (pkg_dir, type_name) -> {"file", "fields": {name: field_node_id},
        #                          "field_types": {name: (pkg, type)},
        #                          "kind": "struct" | "other"}
        self.types = {}
        # (pkg_dir, type_name, method_name) -> method node id
        self.methods = {}
        # new nodes this tool adds to the map (struct field declarations)
        self.new_nodes = {}

    def add_type(self, pkg, name, record):
        key = (pkg, name)
        if key in self.types:
            return
        self.types[key] = record

    def add_method(self, pkg, recv, name, node_id):
        key = (pkg, recv, name)
        if key in self.methods:
            return
        self.methods[key] = node_id


def unwrap_type(node, depth=0):
    """A type expression -> (package_alias_or_None, type_name), or None.

    Strips pointer, slice and array wrapping.  Everything else that is not a
    plain or qualified name is refused, which is the point: no guessing.
    """
    if node is None:
        return None
    if depth > MAX_UNWRAP:
        return None
    kind = node.type
    if kind == "type_identifier":
        return (None, kind_text(node))
    if kind == "qualified_type":
        pkg = node.child_by_field_name("package")
        name = node.child_by_field_name("name")
        if pkg is None or name is None:
            return None
        return (kind_text(pkg), kind_text(name))
    if kind == "pointer_type":
        inner = None
        for child in node.named_children:
            inner = child
            break
        return unwrap_type(inner, depth + 1)
    if kind in ("slice_type", "array_type"):
        inner = node.child_by_field_name("element")
        return unwrap_type(inner, depth + 1)
    if kind == "parenthesized_type":
        inner = None
        for child in node.named_children:
            inner = child
            break
        return unwrap_type(inner, depth + 1)
    if kind == "generic_type":
        inner = node.child_by_field_name("type")
        return unwrap_type(inner, depth + 1)
    return None


# kind_text is bound to the current file's source before each file is walked.
def kind_text(node):
    return _SRC[node.start_byte:node.end_byte].decode("utf-8", "replace")


_SRC = b""


def set_source(src):
    global _SRC
    _SRC = src


# ---------------------------------------------------------------- pass one --

def scan_declarations(table, rel, pkg, src, root):
    """Record this file's named types, their struct fields, and its methods."""
    set_source(src)
    for child in root.named_children:
        if child.type == "type_declaration":
            for spec in child.named_children:
                if spec.type != "type_spec":
                    continue
                scan_type_spec(table, rel, pkg, spec)
        elif child.type == "method_declaration":
            scan_method(table, rel, pkg, child)


def scan_type_spec(table, rel, pkg, spec):
    name_node = spec.child_by_field_name("name")
    type_node = spec.child_by_field_name("type")
    if name_node is None:
        return
    name = kind_text(name_node)
    record = {
        "file": rel,
        "fields": {},
        "field_types": {},
        "kind": "other",
    }
    if type_node is not None and type_node.type == "struct_type":
        record["kind"] = "struct"
        scan_struct_fields(table, rel, type_node, record)
    table.add_type(pkg, name, record)


def scan_struct_fields(table, rel, struct_node, record):
    body = None
    for child in struct_node.named_children:
        if child.type == "field_declaration_list":
            body = child
    if body is None:
        return
    for decl in body.named_children:
        if decl.type != "field_declaration":
            continue
        type_node = decl.child_by_field_name("type")
        names = []
        for child in decl.children:
            if child.type == "field_identifier":
                names.append(child)
        if not names:
            continue  # embedded field: promotion is not in this rule
        wrapped = unwrap_type(type_node)
        for name_node in names:
            field_name = kind_text(name_node)
            node_id = bg.nid(rel, name_node, "field")
            start_byte, end_byte, start_line, end_line = bg.spans(name_node)
            table.new_nodes[node_id] = {
                "id": node_id,
                "kind": "field",
                "name": field_name,
                "file": rel,
                "start_byte": start_byte,
                "end_byte": end_byte,
                "start_line": start_line,
                "end_line": end_line,
            }
            record["fields"][field_name] = node_id
            if wrapped is not None:
                record["field_types"][field_name] = wrapped


def scan_method(table, rel, pkg, decl):
    name_node = decl.child_by_field_name("name")
    recv = decl.child_by_field_name("receiver")
    if name_node is None or recv is None:
        return
    recv_type = None
    for param in recv.named_children:
        if param.type != "parameter_declaration":
            continue
        recv_type = unwrap_type(param.child_by_field_name("type"))
    if recv_type is None:
        return
    node_id = bg.nid(rel, decl, "method")
    table.add_method(pkg, recv_type[1], kind_text(name_node), node_id)


# ---------------------------------------------------------------- pass two --

class DotWalker:
    """One file: declared-type bindings, then every selector re-examined."""

    def __init__(self, table, rel, pkg, src, root, imports, path_to_pkg):
        self.table = table
        self.rel = rel
        self.pkg = pkg
        self.src = src
        self.root = root
        self.imports = imports
        self.path_to_pkg = path_to_pkg
        self.package_bindings = {}
        self.bindings = {}
        self.ambiguous = set()
        self.results = []          # (selector_node, target_id, how)
        self.refused = 0

    # -- bindings ----------------------------------------------------------
    def bind(self, name, wrapped):
        if name == "_":
            return
        if wrapped is None:
            return
        resolved = self.to_region_type(wrapped)
        if resolved is None:
            return
        old = self.bindings.get(name)
        if old is not None and old != resolved:
            self.ambiguous.add(name)
            return
        self.bindings[name] = resolved

    def to_region_type(self, wrapped):
        """(alias_or_None, name) -> (pkg_dir, name) if declared in region."""
        alias, name = wrapped
        if alias is None:
            key = (self.pkg, name)
            if key in self.table.types:
                return key
            return None
        path = self.imports.get(alias)
        if path is None:
            return None
        other = self.path_to_pkg.get(path)
        if other is None:
            return None
        key = (other, name)
        if key in self.table.types:
            return key
        return None

    def scan_package_bindings(self):
        for child in self.root.named_children:
            if child.type != "var_declaration":
                continue
            for spec in child.named_children:
                self.bind_var_spec(spec)
        self.package_bindings = dict(self.bindings)

    def bind_var_spec(self, spec):
        type_node = spec.child_by_field_name("type")
        if type_node is None:
            return
        wrapped = unwrap_type(type_node)
        for child in spec.children:
            if child.type == "identifier":
                self.bind(kind_text(child), wrapped)

    def bind_params(self, plist, ):
        if plist is None:
            return
        for param in plist.named_children:
            if param.type not in ("parameter_declaration",
                                  "variadic_parameter_declaration"):
                continue
            wrapped = unwrap_type(param.child_by_field_name("type"))
            for child in param.children:
                if child.type == "identifier":
                    self.bind(kind_text(child), wrapped)

    def bind_composite(self, spec_left, spec_right):
        """x := T{...} and x := &T{...}: the type is written down, so take it."""
        if len(spec_left) != 1:
            return
        if len(spec_right) != 1:
            return
        value = spec_right[0]
        if value.type == "unary_expression":
            inner = value.child_by_field_name("operand")
            if inner is not None:
                value = inner
        if value.type != "composite_literal":
            return
        wrapped = unwrap_type(value.child_by_field_name("type"))
        left = spec_left[0]
        if left.type != "identifier":
            return
        self.bind(kind_text(left), wrapped)

    def collect_bindings(self, node):
        if node is None:
            return
        kind = node.type
        if kind == "var_declaration":
            for spec in node.named_children:
                self.bind_var_spec(spec)
            return
        if kind == "short_var_declaration":
            left = _list(node.child_by_field_name("left"))
            right = _list(node.child_by_field_name("right"))
            self.bind_composite(left, right)
            return
        if kind == "func_literal":
            self.bind_params(node.child_by_field_name("parameters"))
            result = node.child_by_field_name("result")
            if result is not None and result.type == "parameter_list":
                self.bind_params(result)
        for child in node.named_children:
            self.collect_bindings(child)

    # -- resolution --------------------------------------------------------
    def operand_type(self, node, depth=0):
        if node is None:
            return None
        if depth > MAX_UNWRAP:
            return None
        kind = node.type
        if kind == "identifier":
            name = kind_text(node)
            if name in self.ambiguous:
                return None
            return self.bindings.get(name)
        if kind == "parenthesized_expression":
            inner = None
            for child in node.named_children:
                inner = child
                break
            return self.operand_type(inner, depth + 1)
        if kind == "selector_expression":
            base = self.operand_type(node.child_by_field_name("operand"),
                                     depth + 1)
            if base is None:
                return None
            field = node.child_by_field_name("field")
            if field is None:
                return None
            record = self.table.types.get(base)
            if record is None:
                return None
            wrapped = record["field_types"].get(kind_text(field))
            if wrapped is None:
                return None
            return self.to_region_type_for(base[0], wrapped)
        if kind == "index_expression":
            base = self.operand_type(node.child_by_field_name("operand"),
                                     depth + 1)
            return base
        return None

    def to_region_type_for(self, pkg, wrapped):
        """Resolve a field's declared type, read in the package it is declared in."""
        alias, name = wrapped
        if alias is None:
            key = (pkg, name)
            if key in self.table.types:
                return key
            return None
        # a qualified field type is resolved through the DECLARING file's
        # imports, which this tool does not carry; refused rather than guessed.
        return None

    def resolve_selectors(self, node):
        if node is None:
            return
        if node.type == "selector_expression":
            self.try_selector(node)
        for child in node.named_children:
            self.resolve_selectors(child)

    def try_selector(self, node):
        operand = node.child_by_field_name("operand")
        field = node.child_by_field_name("field")
        if operand is None or field is None:
            return
        base = self.operand_type(operand)
        if base is None:
            self.refused = self.refused + 1
            return
        field_name = kind_text(field)
        pkg, type_name = base
        method_id = self.table.methods.get((pkg, type_name, field_name))
        if method_id is not None:
            self.results.append((node, method_id, "method"))
            return
        record = self.table.types.get(base)
        if record is None:
            self.refused = self.refused + 1
            return
        field_id = record["fields"].get(field_name)
        if field_id is not None:
            self.results.append((node, field_id, "field"))
            return
        self.refused = self.refused + 1

    def run(self):
        set_source(self.src)
        self.scan_package_bindings()
        for child in self.root.named_children:
            if child.type not in ("function_declaration", "method_declaration"):
                continue
            self.bindings = dict(self.package_bindings)
            self.ambiguous = set()
            if child.type == "method_declaration":
                self.bind_params(child.child_by_field_name("receiver"))
            self.bind_params(child.child_by_field_name("parameters"))
            result = child.child_by_field_name("result")
            if result is not None and result.type == "parameter_list":
                self.bind_params(result)
            body = child.child_by_field_name("body")
            self.collect_bindings(body)
            self.resolve_selectors(body)
        return self.results


def _list(node):
    if node is None:
        return []
    if node.type == "expression_list":
        return list(node.named_children)
    return [node]


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go-src", required=True)
    ap.add_argument("--graph", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    parser = Parser(bg.GO_LANG)
    files = bg.collect_region(args.go_src)
    sys.stderr.write("region: %d files\n" % len(files))

    path_to_pkg = {}
    for pkg_rel in bg.WHOLE_PACKAGES + [bg.SSA_PACKAGE]:
        path_to_pkg["cmd/compile/" + pkg_rel] = pkg_rel

    table = TypeTable()
    trees = {}
    for path, pkg_rel, fname, gen in files:
        rel = os.path.relpath(path, args.go_src)
        handle = open(path, "rb")
        src = handle.read()
        handle.close()
        tree = parser.parse(src)
        trees[rel] = (src, tree, pkg_rel)
        scan_declarations(table, rel, pkg_rel, src, tree.root_node)

    sys.stderr.write("named types in region: %d\n" % len(table.types))
    sys.stderr.write("struct fields recorded: %d\n" % len(table.new_nodes))
    sys.stderr.write("methods by receiver type: %d\n" % len(table.methods))

    # resolved[(file, start_byte, end_byte)] = (target_id, how)
    resolved = {}
    refused_total = 0
    for rel, (src, tree, pkg_rel) in trees.items():
        set_source(src)
        imports = bg.collect_imports(src, tree.root_node)
        walker = DotWalker(table, rel, pkg_rel, src, tree.root_node,
                           imports, path_to_pkg)
        got = walker.run()
        refused_total = refused_total + walker.refused
        for (node, target_id, how) in got:
            key = (rel, node.start_byte, node.end_byte)
            resolved[key] = (target_id, how)

    sys.stderr.write("selectors crossed by the rule: %d\n" % len(resolved))
    sys.stderr.write("selectors refused by the rule: %d\n" % refused_total)

    sys.stderr.write("loading the map ...\n")
    handle = open(args.graph)
    doc = json.load(handle)
    handle.close()

    old_frontier = doc["frontier"]
    kept = []
    dropped = 0
    dropped_ids = set()
    selector_total = 0
    for record in old_frontier:
        if record.get("reason") != FIELD_SELECTOR_REASON:
            kept.append(record)
            continue
        selector_total = selector_total + 1
        span = record["span"]
        key = (record["file"], span[0], span[1])
        if key in resolved:
            dropped = dropped + 1
            dropped_ids.add(record["id"])
            continue
        kept.append(record)

    sys.stderr.write("lap-one selector frontier records: %d\n" % selector_total)
    sys.stderr.write("of those, now crossed: %d\n" % dropped)

    # nodes: drop the frontier nodes that fell, add the field nodes
    nodes = []
    for node in doc["nodes"]:
        if node["id"] in dropped_ids:
            continue
        nodes.append(node)
    have = set()
    for node in nodes:
        have.add(node["id"])
    added_fields = 0
    for node_id, node in table.new_nodes.items():
        if node_id in have:
            continue
        nodes.append(node)
        added_fields = added_fields + 1

    # edges: drop the ref -> dead frontier edges, add the real ones
    edges = []
    for edge in doc["edges"]:
        if edge["dst"] in dropped_ids:
            continue
        edges.append(edge)

    seen_edge = set()
    for edge in edges:
        seen_edge.add((edge["src"], edge["dst"], edge["type"],
                       edge.get("kind")))

    added_edges = 0
    for (rel, start_byte, end_byte), (target_id, how) in resolved.items():
        ref_id = "%s:%d-%d:ref" % (rel, start_byte, end_byte)
        call_id = None
        edge_kind = "field_via_declared_type"
        if how == "method":
            edge_kind = "method_via_declared_type"
        key = (ref_id, target_id, "resolves_to", edge_kind)
        if key not in seen_edge:
            edges.append({"src": ref_id, "dst": target_id,
                          "type": "resolves_to", "kind": edge_kind})
            seen_edge.add(key)
            added_edges = added_edges + 1

    # a call whose callee is a crossed selector gets a precise calls edge too
    call_index = defaultdict(list)
    for node in nodes:
        if node["kind"] != "call":
            continue
        call_index[node["file"]].append(node)

    added_calls = 0
    for (rel, start_byte, end_byte), (target_id, how) in resolved.items():
        if how != "method":
            continue
        for node in call_index.get(rel, ()):
            if node["start_byte"] != start_byte:
                continue
            key = (node["id"], target_id, "calls", "method_via_declared_type")
            if key in seen_edge:
                continue
            edges.append({"src": node["id"], "dst": target_id,
                          "type": "calls", "kind": "method_via_declared_type",
                          "one_to_many": False,
                          "basis": "receiver's declared type, declared in region"})
            seen_edge.add(key)
            added_calls = added_calls + 1

    # containment: a type declaration is the super-node of its field nodes is
    # not modelled here; the field node stands on its own span, which is what
    # the path query lands on.

    meta = doc["meta"]
    meta["lap"] = 2
    meta["second_resolution_step"] = {
        "tool": "compiler_graph/resolve_dots.py",
        "rule": "declared types only: receiver / parameter / result parameter "
                "/ var x T / package var x T / x := T{...}; one level of "
                "*T, []T, [N]T unwrapping; T must be a named type declared in "
                "the parsed region; f must be a field of its struct "
                "declaration or a method with that receiver base type",
        "not_done": ["type inference from assignments", "interface method sets",
                     "embedded-field promotion", "generic instantiation",
                     "qualified field types resolved through the declaring "
                     "file's imports"],
        "named_types_in_region": len(table.types),
        "struct_field_nodes_added": added_fields,
        "methods_by_receiver_type": len(table.methods),
        "selectors_crossed": len(resolved),
        "selectors_refused": refused_total,
        "lap_one_selector_frontier_records": selector_total,
        "selector_frontier_records_closed": dropped,
        "resolves_to_edges_added": added_edges,
        "calls_edges_added": added_calls,
    }
    meta["counts"]["nodes"] = len(nodes)
    meta["counts"]["edges"] = len(edges)
    meta["counts"]["frontier"] = len(kept)

    doc["nodes"] = nodes
    doc["edges"] = edges
    doc["frontier"] = kept

    handle = open(args.out, "w")
    json.dump(doc, handle)
    handle.close()
    sys.stderr.write(json.dumps(meta["second_resolution_step"], indent=2) + "\n")
    sys.stderr.write("wrote %s\n" % args.out)


if __name__ == "__main__":
    main()
