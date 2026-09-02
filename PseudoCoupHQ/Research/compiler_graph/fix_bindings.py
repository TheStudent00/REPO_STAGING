#!/usr/bin/env python3
"""fix_bindings.py -- lap four, fix ONE: the name-collision keying defect.

WHAT WAS WRONG.  build_graph.py keeps ONE table per package, `{name: node_id}`,
filled with `table.setdefault(name, i)` over every top-level declaration in
file order (build_graph.py, top_level_decls).  A func and a method may carry
the SAME bare name -- a method's name lives in its receiver type's method set,
not in the package scope, so Go allows it -- and `setdefault` then keeps
whichever the walker met first.  internal/ssa holds both:

    expand_calls.go:876   func (x *expandState) ArgOpAndRegisterFor() ...
    expand_calls.go:883   func ArgOpAndRegisterFor(r abi.RegIndex, a *abi.ABIConfig) ...

876 comes first, so the package table for internal/ssa maps the bare name
ArgOpAndRegisterFor to the METHOD, and the call written in ssagen

    op, reg := ssa.ArgOpAndRegisterFor(r, abi)                (ssagen/ssa.go:630)

binds to the method.  The method takes no parameters, so flow_forward.py's
positional argument binding has nothing to bind and the FUNC's return never
reaches the call node.  That is the map defect pasted in acceptance_query3.txt
as the first of the three stops on the register index.

THE RULE APPLIED HERE, and it is syntax, not inference.

  * A selector whose base identifier is an IMPORT NAME of the file is a
    PACKAGE QUALIFIER.  Go has no way to write a method through a package
    qualifier: `pkg.F` names a package-scope declaration and nothing else.
    So a package-qualified name binds to the FUNC (or type / var / const) of
    that name, never to a method of that name.
  * A selector whose base is a VALUE is a field or method selection; those
    bind through the method index / the declared-type rule and are not
    touched here.
  * A plain call `F(...)` on a bare identifier is likewise a package-scope
    name and never a method.  The SAME collision bites inside one package:
    internal/ssa declares `func newSparseSet(...)` in sparseset.go and a
    method `func (f *Func) newSparseSet(...)` in func.go, and files are walked
    in name order, so func.go's METHOD is what the package table holds and
    every bare `newSparseSet(n)` in the package binds to it.  Rule B below
    catches those by reading the map itself: a bare identifier (no dot in the
    node's name) whose binding landed on a METHOD node, in a package that
    does declare a package-scope name of that spelling, is the same defect.

Rule B needs no scope analysis to be safe.  build_graph.py consults the local
scopes FIRST and only falls through to the package table when nothing local
matched, so a map edge from a bare identifier to a method node is already
proof that no local declaration shadowed the name at that spot.

WHERE IT CANNOT TELL, IT KEEPS BOTH.  If a package-qualified name has no
package-scope declaration of that name in the parsed region but does have
methods of that name, the true target is outside what was parsed (an
unexported spelling difference, a build-tagged file, a generated file the
region rule excludes).  The old singleton edge is then replaced by the whole
CANDIDATE SET, marked one_to_many, per the node's frontier rule: a named set,
never a guess.

Why a co-module.  Same reason as resolve_dots.py and flow_forward.py:
build_graph.py and graph_go.json are the artifacts of record for lap one and
stay byte-identical.  This tool reads a map and writes a new one, so the
difference between the two IS the measured answer to "how many bindings were
wrong".  It re-parses the region with the same pins because the map recorded
targets, never the SYNTACTIC FORM of the call site that chose them.

NOT DONE, and stated so the number is read correctly:
  * local shadowing of a package name is not modelled by THIS tool.  `abi :=
    ...` followed by `abi.F()` in the same function is a value selection, and
    this tool's own scan would call it package-qualified.  Measured: the
    region holds 0 package-level declarations that shadow an import name of
    their own file, and 27 function-local `:=` declarations that do (`abi`
    once in ssagen/abi.go:82, `cmp` and `base` the rest, all in
    ssagen/ssa.go).  The defect is CONTAINED, and by construction: this tool
    only ever REPLACES a cross-package binding the map already had, and
    build_graph.py emits one only when its own scope walk found no shadow.
    At a shadowed site there is no binding to replace, so nothing is
    rewritten.  A future tool that INVENTS bindings would have to do the
    scope walk first.
  * dot-imports are not modelled; the region contains none.
  * the receiver TYPE is not used to pick among same-named methods; that is
    resolve_dots' job and it is untouched here.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

import argparse
import json
import os
import sys
from collections import defaultdict

import build_graph as bg
from tree_sitter import Parser


CROSS = "cross_package_in_region"

# package-scope declaration kinds a `pkg.Name` may legally name
PACKAGE_SCOPE_KINDS = ("func", "type", "package_var", "package_const")


_SRC = b""


def set_source(src):
    global _SRC
    _SRC = src


def text(node):
    return _SRC[node.start_byte:node.end_byte].decode("utf-8", "replace")


def ref_id(rel, node):
    return "%s:%d-%d:ref" % (rel, node.start_byte, node.end_byte)


def call_id(rel, node):
    return "%s:%d-%d:call" % (rel, node.start_byte, node.end_byte)


# ------------------------------------------------------- declaration tables --

class DeclTable:
    """Every top-level declaration of every parsed package, by name.

    build_graph.py's table keeps the FIRST declaration of a name.  This one
    keeps ALL of them, split by kind, which is the whole point.
    """

    def __init__(self):
        # pkg_dir -> name -> {"package_scope": [ids], "method": [ids]}
        self.by_pkg = defaultdict(lambda: defaultdict(
            lambda: {"package_scope": [], "method": []}))

    def add(self, pkg, name, kind, node_id):
        if name == "_":
            return
        slot = "method"
        if kind in PACKAGE_SCOPE_KINDS:
            slot = "package_scope"
        bucket = self.by_pkg[pkg][name][slot]
        if node_id in bucket:
            return
        bucket.append(node_id)

    def lookup(self, pkg, name):
        pkg_names = self.by_pkg.get(pkg)
        if pkg_names is None:
            return None
        return pkg_names.get(name)


def scan_top_level(table, rel, pkg, root):
    """Mirror build_graph.top_level_decls, but keep every declaration."""
    for child in root.named_children:
        kind = child.type
        if kind == "function_declaration":
            record_named(table, rel, pkg, child, child, "func")
        elif kind == "method_declaration":
            record_named(table, rel, pkg, child, child, "method")
        elif kind == "type_declaration":
            for spec in child.named_children:
                if spec.type not in ("type_spec", "type_alias"):
                    continue
                record_named(table, rel, pkg, spec, spec, "type")
        elif kind in ("var_declaration", "const_declaration"):
            decl_kind = "package_var"
            if kind == "const_declaration":
                decl_kind = "package_const"
            scan_top_level_vars(table, rel, pkg, child, decl_kind)


def scan_top_level_vars(table, rel, pkg, node, decl_kind):
    for spec in node.named_children:
        if spec.type not in ("var_spec", "const_spec",
                             "var_spec_list", "const_spec_list"):
            continue
        for item in spec.children:
            if item.type == "identifier":
                node_id = bg.nid(rel, spec, decl_kind)
                table.add(pkg, text(item), decl_kind, node_id)
            elif item.type in ("expression_list", "=", ":="):
                break


def record_named(table, rel, pkg, id_node, name_holder, kind):
    name_node = name_holder.child_by_field_name("name")
    if name_node is None:
        return
    node_id = bg.nid(rel, id_node, kind)
    table.add(pkg, text(name_node), kind, node_id)


# ------------------------------------------------------------- the decisions --

def bare_new_kind(edge_type):
    """The kind a corrected bare-name edge carries: the one it carried before."""
    if edge_type == "calls":
        return "direct"
    return None


class Decision:
    """One call site or reference whose binding this tool re-decides."""

    def __init__(self, node_id, edge_type, targets, basis, one_to_many):
        self.node_id = node_id
        self.edge_type = edge_type
        self.targets = targets
        self.basis = basis
        self.one_to_many = one_to_many


class FileScan:
    """Walk one file, deciding the correct target of every qualified name."""

    def __init__(self, table, rel, pkg, imports, path_to_pkg):
        self.table = table
        self.rel = rel
        self.pkg = pkg
        self.imports = imports
        self.path_to_pkg = path_to_pkg
        self.decisions = []
        self.qualified_seen = 0
        self.bare_calls_seen = 0

    def qualifier_package(self, operand):
        """An identifier operand -> the in-region package it names, or None."""
        if operand is None:
            return None
        if operand.type != "identifier":
            return None
        alias = text(operand)
        path = self.imports.get(alias)
        if path is None:
            return None
        own = self.table.by_pkg.get(self.pkg, {})
        if alias in own:
            # a package-level declaration of this file's own package shares the
            # import's name: build_graph would have preferred the declaration,
            # and so does this tool.  Refused rather than guessed.
            return None
        return self.path_to_pkg.get(path)

    def choose(self, other_pkg, name):
        """(target ids, basis, one_to_many) for `other_pkg.name`, or None."""
        record = self.table.lookup(other_pkg, name)
        if record is None:
            return None
        package_scope = record["package_scope"]
        methods = record["method"]
        if len(package_scope) == 1:
            return (list(package_scope),
                    "package qualifier: package-scope declaration of that name",
                    False)
        if len(package_scope) > 1:
            return (list(package_scope),
                    "package qualifier: several package-scope declarations of "
                    "that name in the parsed region (build tags); candidate set",
                    True)
        if methods:
            return (list(methods),
                    "package qualifier, but no package-scope declaration of "
                    "that name was parsed; the same-named methods are kept as "
                    "the candidate set rather than dropped or guessed",
                    len(methods) > 1)
        return None

    def visit(self, node, depth=0):
        if depth > 250:
            return
        kind = node.type
        if kind == "call_expression":
            self.visit_call(node)
        elif kind == "selector_expression":
            self.visit_selector(node)
        for child in node.named_children:
            self.visit(child, depth + 1)

    def visit_call(self, node):
        fn = node.child_by_field_name("function")
        if fn is None:
            return
        if fn.type != "selector_expression":
            return
        operand = fn.child_by_field_name("operand")
        field = fn.child_by_field_name("field")
        if field is None:
            return
        other = self.qualifier_package(operand)
        if other is None:
            return
        self.qualified_seen = self.qualified_seen + 1
        chosen = self.choose(other, text(field))
        if chosen is None:
            return
        targets, basis, many = chosen
        self.decisions.append(Decision(call_id(self.rel, node), "calls",
                                       targets, basis, many))

    def visit_selector(self, node):
        operand = node.child_by_field_name("operand")
        field = node.child_by_field_name("field")
        if field is None:
            return
        other = self.qualifier_package(operand)
        if other is None:
            return
        chosen = self.choose(other, text(field))
        if chosen is None:
            return
        targets, basis, many = chosen
        self.decisions.append(Decision(ref_id(self.rel, node), "resolves_to",
                                       targets, basis, many))


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go-src", required=True)
    ap.add_argument("--graph", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report")
    args = ap.parse_args()

    parser = Parser(bg.GO_LANG)
    files = bg.collect_region(args.go_src)
    sys.stderr.write("region: %d files\n" % len(files))

    path_to_pkg = {}
    for pkg_rel in bg.WHOLE_PACKAGES + [bg.SSA_PACKAGE]:
        path_to_pkg["cmd/compile/" + pkg_rel] = pkg_rel

    trees = {}
    table = DeclTable()
    for path, pkg_rel, fname, gen in files:
        rel = os.path.relpath(path, args.go_src)
        handle = open(path, "rb")
        src = handle.read()
        handle.close()
        tree = parser.parse(src)
        trees[rel] = (src, tree, pkg_rel)
        set_source(src)
        scan_top_level(table, rel, pkg_rel, tree.root_node)

    collisions = []
    for pkg, names in table.by_pkg.items():
        for name, record in names.items():
            if not record["package_scope"]:
                continue
            if not record["method"]:
                continue
            collisions.append((pkg, name,
                               list(record["package_scope"]),
                               list(record["method"])))
    collisions.sort()
    sys.stderr.write("names held by BOTH a package-scope decl and a method: "
                     "%d\n" % len(collisions))

    decisions = []
    qualified_total = 0
    for rel, (src, tree, pkg_rel) in trees.items():
        set_source(src)
        imports = bg.collect_imports(src, tree.root_node)
        scan = FileScan(table, rel, pkg_rel, imports, path_to_pkg)
        scan.visit(tree.root_node)
        qualified_total = qualified_total + scan.qualified_seen
        decisions.extend(scan.decisions)

    sys.stderr.write("package-qualified call sites into the region: %d\n"
                     % qualified_total)
    sys.stderr.write("bindings re-decided (before comparison): %d\n"
                     % len(decisions))

    sys.stderr.write("loading the map ...\n")
    handle = open(args.graph)
    doc = json.load(handle)
    handle.close()

    have = set()
    node_kind = {}
    node_name = {}
    node_file = {}
    for node in doc["nodes"]:
        have.add(node["id"])
        node_kind[node["id"]] = node["kind"]
        node_name[node["id"]] = node.get("name") or ""
        node_file[node["id"]] = node["file"]

    file_pkg = {}
    for rel, (src, tree, pkg_rel) in trees.items():
        file_pkg[rel] = pkg_rel

    # existing cross-package bindings, per (src node, edge type)
    existing = defaultdict(set)
    for edge in doc["edges"]:
        if edge.get("kind") != CROSS:
            continue
        existing[(edge["src"], edge["type"])].add(edge["dst"])

    # -- rule A: decide what actually changes, package-qualified names -------
    changed = {}
    unchanged = 0
    skipped_missing = 0
    for decision in decisions:
        key = (decision.node_id, decision.edge_type)
        if decision.node_id not in have:
            skipped_missing = skipped_missing + 1
            continue
        kept = []
        for target in decision.targets:
            if target in have:
                kept.append(target)
        if not kept:
            skipped_missing = skipped_missing + 1
            continue
        old = existing.get(key, set())
        if old == set(kept):
            unchanged = unchanged + 1
            continue
        if not old:
            # the map had no cross-package binding here at all; this tool only
            # CORRECTS bindings, it does not invent new ones.
            continue
        changed[key] = {
            "targets": kept,
            "basis": decision.basis,
            "one_to_many": decision.one_to_many,
            "was": sorted(old),
            "remove_kinds": set([CROSS]),
            "new_kind": CROSS,
            "rule": "A: package qualifier",
        }

    rule_a_changed = len(changed)
    sys.stderr.write("rule A -- bindings already correct: %d\n" % unchanged)
    sys.stderr.write("rule A -- bindings CHANGED: %d\n" % rule_a_changed)
    sys.stderr.write("rule A -- decisions skipped (node or target not in map): "
                     "%d\n" % skipped_missing)

    # -- rule B: bare identifiers that landed on a method -------------------
    # Read straight off the map: build_graph.py consults local scopes first, so
    # an edge from a bare name to a method node means the package table
    # answered, and the package table is the thing with the collision.
    bare_hits = defaultdict(set)
    bare_kinds = defaultdict(set)
    for edge in doc["edges"]:
        if edge["type"] not in ("resolves_to", "calls"):
            continue
        if edge.get("kind") not in (None, "direct"):
            continue
        dst = edge["dst"]
        if node_kind.get(dst) != "method":
            continue
        src = edge["src"]
        if node_kind.get(src) not in ("ref", "call"):
            continue
        if "." in node_name.get(src, "."):
            continue
        bare_hits[(src, edge["type"])].add(dst)
        bare_kinds[(src, edge["type"])].add(edge.get("kind"))

    rule_b_changed = 0
    rule_b_no_alternative = 0
    for key, olds in bare_hits.items():
        src, edge_type = key
        if key in changed:
            continue
        pkg = file_pkg.get(node_file.get(src))
        if pkg is None:
            continue
        record = table.lookup(pkg, node_name.get(src, ""))
        if record is None:
            rule_b_no_alternative = rule_b_no_alternative + 1
            continue
        scope = []
        for target in record["package_scope"]:
            if target in have:
                scope.append(target)
        if not scope:
            rule_b_no_alternative = rule_b_no_alternative + 1
            continue
        if set(scope) == olds:
            continue
        many = len(scope) > 1
        changed[key] = {
            "targets": scope,
            "basis": "bare identifier: a package-scope declaration of that "
                     "name exists in the same package; a bare name can never "
                     "name a method",
            "one_to_many": many,
            "was": sorted(olds),
            "remove_kinds": set(bare_kinds[key]),
            # a resolves_to edge from a bare name carried NO kind before this
            # fix, and flow_forward.py's decl_to_read rule selects on exactly
            # that; the corrected edge keeps the same kind so no downstream
            # rule changes shape because of the fix.
            "new_kind": bare_new_kind(edge_type),
            "rule": "B: bare identifier",
        }
        rule_b_changed = rule_b_changed + 1

    sys.stderr.write("rule B -- bare names bound to a method: %d\n"
                     % len(bare_hits))
    sys.stderr.write("rule B -- bindings CHANGED: %d\n" % rule_b_changed)
    sys.stderr.write("rule B -- left alone (no package-scope name to move to): "
                     "%d\n" % rule_b_no_alternative)
    sys.stderr.write("bindings CHANGED, both rules: %d\n" % len(changed))

    # rewrite the edge list
    edges = []
    removed = 0
    for edge in doc["edges"]:
        key = (edge["src"], edge["type"])
        record = changed.get(key)
        if record is not None and edge.get("kind") in record["remove_kinds"]:
            removed = removed + 1
            continue
        edges.append(edge)

    added = 0
    for (node_id, edge_type), record in changed.items():
        for target in record["targets"]:
            new_edge = {
                "src": node_id,
                "dst": target,
                "type": edge_type,
                "kind": record["new_kind"],
                "basis": record["basis"],
                "one_to_many": record["one_to_many"],
                "fixed_by": "fix_bindings.py",
                "was": record["was"],
            }
            if record["one_to_many"]:
                new_edge["candidate_set"] = list(record["targets"])
            edges.append(new_edge)
            added = added + 1

    sys.stderr.write("edges removed: %d, edges added: %d\n" % (removed, added))

    # the named case, before and after, for the report
    named = []
    for (node_id, edge_type), record in changed.items():
        named.append({"node": node_id, "edge_type": edge_type,
                      "was": record["was"], "now": list(record["targets"]),
                      "one_to_many": record["one_to_many"],
                      "rule": record["rule"],
                      "basis": record["basis"]})
    named.sort(key=lambda item: item["node"])

    by_target_kind = defaultdict(int)
    for item in named:
        was_kinds = []
        for old_id in item["was"]:
            was_kinds.append(node_kind.get(old_id, "?"))
        now_kinds = []
        for new_id in item["now"]:
            now_kinds.append(node_kind.get(new_id, "?"))
        label = "%s -> %s" % (",".join(sorted(set(was_kinds))),
                              ",".join(sorted(set(now_kinds))))
        by_target_kind[label] = by_target_kind[label] + 1
    for label, count in sorted(by_target_kind.items(), key=lambda kv: -kv[1]):
        sys.stderr.write("  %-30s %d\n" % (label, count))

    meta = doc["meta"]
    meta["lap"] = 4
    meta["binding_fix_step"] = {
        "tool": "compiler_graph/fix_bindings.py",
        "defect": "build_graph.py keys its per-package declaration table on the "
                  "bare name with setdefault, so a func and a method of the "
                  "same name collide and the first one parsed wins",
        "rule": "a selector whose base identifier is an import name of the file "
                "is a PACKAGE QUALIFIER and can only name a package-scope "
                "declaration (func / type / var / const), never a method; where "
                "the parsed region holds no package-scope declaration of that "
                "name, the same-named methods are kept as a CANDIDATE SET, "
                "marked one_to_many, never narrowed to a guess",
        "names_held_by_both_a_package_scope_decl_and_a_method": len(collisions),
        "package_qualified_call_sites_into_the_region": qualified_total,
        "rule_A_bindings_examined": len(decisions),
        "rule_A_bindings_already_correct": unchanged,
        "rule_A_bindings_changed": rule_a_changed,
        "rule_B_bare_names_bound_to_a_method": len(bare_hits),
        "rule_B_bindings_changed": rule_b_changed,
        "rule_B_left_alone_no_package_scope_name": rule_b_no_alternative,
        "bindings_changed": len(changed),
        "edges_removed": removed,
        "edges_added": added,
        "change_shapes": dict(by_target_kind),
        "not_done": [
            "local shadowing of an import name inside a function body (27 in "
            "the region; contained, because this tool only replaces bindings "
            "the map already made and the map makes none at a shadowed site)",
            "dot-imports (the region contains none)",
            "receiver-type selection among same-named methods "
            "(resolve_dots' job, untouched here)",
            "call sites the map never bound at all: this tool corrects "
            "bindings, it does not invent them",
        ],
    }
    meta["counts"]["edges"] = len(edges)
    doc["edges"] = edges

    handle = open(args.out, "w")
    json.dump(doc, handle)
    handle.close()
    sys.stderr.write("wrote %s\n" % args.out)

    if args.report:
        report = {
            "collisions": [
                {"pkg": pkg, "name": name,
                 "package_scope": scope, "methods": methods}
                for (pkg, name, scope, methods) in collisions
            ],
            "changed": named,
            "summary": meta["binding_fix_step"],
        }
        handle = open(args.report, "w")
        json.dump(report, handle, indent=2)
        handle.close()
        sys.stderr.write("wrote %s\n" % args.report)


if __name__ == "__main__":
    main()
