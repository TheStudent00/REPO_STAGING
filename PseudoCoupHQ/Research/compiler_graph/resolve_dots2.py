#!/usr/bin/env python3
"""resolve_dots2.py -- lap four, fix TWO: qualified types in the dot resolver.

Lap two's resolve_dots.py crossed `x.f` only when the type of `x` was written
down AND that type was spelled with a BARE name.  Its own code says why it
stopped at a qualified one (resolve_dots.py, to_region_type_for):

    # a qualified field type is resolved through the DECLARING file's
    # imports, which this tool does not carry; refused rather than guessed.

So `s.curBlock` resolved to the field declaration

    ssagen/ssa.go:1037   curBlock *ssa.Block

and then STOPPED, because `ssa.Block` is `pkg.T`.  internal/ssa IS in the
parsed region and ssagen DOES import cmd/compile/internal/ssa, so nothing
about that refusal was necessary; the tool simply never read the imports of
the file the FIELD was declared in.  That refusal is the second of the three
stops pasted in acceptance_query3.txt.

WHAT THIS TOOL ADDS, in two named rules.

  RULE 1 -- IMPORT-AWARE QUALIFIED TYPES.  A declared type spelled `pkg.T` is
  resolved through the imports of the file where the DECLARATION is written
  (not the file where the selector is read -- those are different files and
  may bind the same alias to different paths).  `pkg` -> import path ->
  parsed package, and `T` is then looked up in that package exactly as a bare
  name is.  Where the import path is NOT one of the parsed packages the
  frontier STAYS, and its reason is rewritten to NAME the package, so a
  dead-end says which package it is waiting on instead of blaming "no type
  information".

  RULE 2 -- DECLARED RESULT TYPES.  `v := b.Func.newValue(...)` gives `v` no
  type of its own, and lap two therefore refused `v.AuxInt`.  But the type IS
  declared -- in the callee's signature:

      ssa/func.go:461  func (f *Func) newValue(op Op, t *types.Type,
                                               b *Block, pos src.XPos) *Value

  Reading a callee's written result type is not inference; it is the same act
  as reading a parameter's written type, which lap two already did.  So: a
  short variable declaration `x := call(...)` whose callee is a func or
  method declared in the parsed region, with exactly ONE result, binds `x` to
  that result's declared type.  Callees with several results are refused
  (which of them `x` is would be positional inference, and the map has no
  business guessing when the left side has one name and the right has many).

Rule 2 is reported separately from rule 1 so the two numbers can be read
apart.  Both are still DECLARED types only.  Everything lap two refused for
other reasons is still refused: no inference from ordinary assignments, no
interface method sets, no embedded-field promotion, no generic instantiation.

Why a new co-module and a new output.  Same rule as every lap of this node:
resolve_dots.py and graph_go2.json are the artifacts of record for lap two
and are not edited.  This tool reads a map and writes a new one, so the
difference IS the measured answer to "how many of the remaining refusals
fell".  It re-uses resolve_dots' own TypeTable and declaration scan unchanged
(imported, not copied), so only the resolution step differs.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

import argparse
import json
import os
import sys
from collections import defaultdict

import build_graph as bg
import resolve_dots as rd
from tree_sitter import Parser


FIELD_SELECTOR_REASON = rd.FIELD_SELECTOR_REASON

MAX_UNWRAP = rd.MAX_UNWRAP


# ------------------------------------------------------------ result types --

class ResultTable:
    """Declared single-result types of every func and method in the region."""

    def __init__(self):
        # (pkg, func_name) -> (wrapped_type, declaring_file)
        self.funcs = {}
        # (pkg, receiver_type_name, method_name) -> (wrapped_type, declaring_file)
        self.methods = {}


def single_result(decl):
    """The one declared result type of a declaration, or None."""
    result = decl.child_by_field_name("result")
    if result is None:
        return None
    if result.type != "parameter_list":
        return rd.unwrap_type(result)
    entries = []
    for child in result.named_children:
        if child.type in ("parameter_declaration",
                          "variadic_parameter_declaration"):
            entries.append(child)
    if len(entries) != 1:
        return None
    return rd.unwrap_type(entries[0].child_by_field_name("type"))


def scan_results(results, rel, pkg, root):
    for child in root.named_children:
        if child.type == "function_declaration":
            scan_func_result(results, rel, pkg, child)
        elif child.type == "method_declaration":
            scan_method_result(results, rel, pkg, child)


def scan_func_result(results, rel, pkg, decl):
    name_node = decl.child_by_field_name("name")
    if name_node is None:
        return
    wrapped = single_result(decl)
    if wrapped is None:
        return
    key = (pkg, rd.kind_text(name_node))
    if key in results.funcs:
        return
    results.funcs[key] = (wrapped, rel)


def scan_method_result(results, rel, pkg, decl):
    name_node = decl.child_by_field_name("name")
    recv = decl.child_by_field_name("receiver")
    if name_node is None or recv is None:
        return
    recv_type = None
    for param in recv.named_children:
        if param.type != "parameter_declaration":
            continue
        recv_type = rd.unwrap_type(param.child_by_field_name("type"))
    if recv_type is None:
        return
    wrapped = single_result(decl)
    if wrapped is None:
        return
    key = (pkg, recv_type[1], rd.kind_text(name_node))
    if key in results.methods:
        return
    results.methods[key] = (wrapped, rel)


# ----------------------------------------------------------------- walker ---

class DotWalker2(rd.DotWalker):
    """Lap two's walker, with the declaring file's imports in hand."""

    def __init__(self, table, results, rel, pkg, src, root, imports,
                 path_to_pkg, imports_by_file, file_pkg):
        rd.DotWalker.__init__(self, table, rel, pkg, src, root, imports,
                              path_to_pkg)
        # rd.DotWalker uses self.results for its crossing list; this subclass
        # keeps the crossings in self.crossings and gives self.result_types to
        # the declared-result table, so the two never share a name.
        self.results = None
        self.crossings = []
        self.result_types = results
        self.imports_by_file = imports_by_file
        self.file_pkg = file_pkg
        self.used_qualified = 0
        self.used_result_type = 0
        # selector byte span -> the import path a refusal is waiting on
        self.waiting_on = {}

    # -- the fix: a type spelled in SOME file, resolved with THAT file's
    #    imports -----------------------------------------------------------
    def resolve_written_type(self, wrapped, declaring_file):
        """(alias_or_None, name) as written in declaring_file -> region type."""
        alias, name = wrapped
        if alias is None:
            pkg = self.file_pkg.get(declaring_file)
            if pkg is None:
                return None
            key = (pkg, name)
            if key in self.table.types:
                return key
            return None
        imports = self.imports_by_file.get(declaring_file)
        if imports is None:
            return None
        path = imports.get(alias)
        if path is None:
            return None
        other = self.path_to_pkg.get(path)
        if other is None:
            return None
        key = (other, name)
        if key in self.table.types:
            return key
        return None

    def import_path_of(self, wrapped, declaring_file):
        """The import path a refusal is waiting on, for the frontier reason."""
        alias, _name = wrapped
        if alias is None:
            return None
        imports = self.imports_by_file.get(declaring_file)
        if imports is None:
            return None
        return imports.get(alias)

    # -- operand typing ----------------------------------------------------
    def operand_type(self, node, depth=0):
        if node is None:
            return None
        if depth > MAX_UNWRAP:
            return None
        kind = node.type
        if kind == "identifier":
            name = rd.kind_text(node)
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
            return self.selector_type(node, depth)
        if kind == "index_expression":
            base = self.operand_type(node.child_by_field_name("operand"),
                                     depth + 1)
            return base
        if kind == "call_expression":
            return self.call_type(node, depth)
        return None

    def selector_type(self, node, depth):
        operand = node.child_by_field_name("operand")
        field = node.child_by_field_name("field")
        if field is None:
            return None
        base = self.operand_type(operand, depth + 1)
        if base is None:
            return None
        record = self.table.types.get(base)
        if record is None:
            return None
        wrapped = record["field_types"].get(rd.kind_text(field))
        if wrapped is None:
            return None
        resolved = self.resolve_written_type(wrapped, record["file"])
        if resolved is not None and wrapped[0] is not None:
            self.used_qualified = self.used_qualified + 1
        if resolved is None:
            path = self.import_path_of(wrapped, record["file"])
            if path is not None:
                self.waiting_on[(node.start_byte, node.end_byte)] = path
        return resolved

    def call_type(self, node, depth):
        """A call's declared result type, when the callee is in the region."""
        fn = node.child_by_field_name("function")
        if fn is None:
            return None
        if fn.type == "identifier":
            key = (self.pkg, rd.kind_text(fn))
            found = self.result_types.funcs.get(key)
            return self.finish_result(found)
        if fn.type != "selector_expression":
            return None
        field = fn.child_by_field_name("field")
        base_node = fn.child_by_field_name("operand")
        if field is None or base_node is None:
            return None
        name = rd.kind_text(field)
        if base_node.type == "identifier":
            alias = rd.kind_text(base_node)
            shadow = self.bindings.get(alias)
            path = self.imports.get(alias)
            if shadow is None and path is not None:
                other = self.path_to_pkg.get(path)
                if other is not None:
                    found = self.result_types.funcs.get((other, name))
                    return self.finish_result(found)
        base = self.operand_type(base_node, depth + 1)
        if base is None:
            return None
        found = self.result_types.methods.get((base[0], base[1], name))
        return self.finish_result(found)

    def finish_result(self, found):
        if found is None:
            return None
        wrapped, declaring_file = found
        resolved = self.resolve_written_type(wrapped, declaring_file)
        if resolved is not None:
            self.used_result_type = self.used_result_type + 1
        return resolved

    # -- bindings ----------------------------------------------------------
    def bind_from_call(self, spec_left, spec_right):
        """x := call(...): bind x to the callee's ONE declared result type."""
        if len(spec_left) != 1:
            return
        if len(spec_right) != 1:
            return
        left = spec_left[0]
        if left.type != "identifier":
            return
        value = spec_right[0]
        if value.type != "call_expression":
            return
        resolved = self.call_type(value, 0)
        if resolved is None:
            return
        name = rd.kind_text(left)
        if name == "_":
            return
        old = self.bindings.get(name)
        if old is not None and old != resolved:
            self.ambiguous.add(name)
            return
        self.bindings[name] = resolved

    def collect_bindings(self, node):
        if node is None:
            return
        kind = node.type
        if kind == "var_declaration":
            for spec in node.named_children:
                self.bind_var_spec(spec)
            return
        if kind == "short_var_declaration":
            left = rd._list(node.child_by_field_name("left"))
            right = rd._list(node.child_by_field_name("right"))
            self.bind_composite(left, right)
            self.bind_from_call(left, right)
            return
        if kind == "func_literal":
            self.bind_params(node.child_by_field_name("parameters"))
            result = node.child_by_field_name("result")
            if result is not None and result.type == "parameter_list":
                self.bind_params(result)
        for child in node.named_children:
            self.collect_bindings(child)

    def run(self):
        rd.set_source(self.src)
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
            # twice: a binding taken from a call's result type may itself need
            # a binding that the first pass had not yet made.
            self.collect_bindings(body)
            self.collect_bindings(body)
            self.resolve_selectors(body)
        return self.crossings

    def carry_waiting(self, operand, node):
        """A refusal caused by an out-of-region package names that package.

        The reason is recorded against the BASE (`s.curBlock`), while the
        frontier record the map holds is for the WHOLE selector
        (`s.curBlock.NewValue0I`); this carries it up one level so the record
        that survives is the one that gets the better reason.
        """
        if operand is None:
            return
        key = (operand.start_byte, operand.end_byte)
        path = self.waiting_on.get(key)
        if path is None:
            return
        self.waiting_on[(node.start_byte, node.end_byte)] = path

    def try_selector(self, node):
        operand = node.child_by_field_name("operand")
        field = node.child_by_field_name("field")
        if operand is None or field is None:
            return
        base = self.operand_type(operand)
        if base is None:
            self.refused = self.refused + 1
            self.carry_waiting(operand, node)
            return
        field_name = rd.kind_text(field)
        pkg, type_name = base
        method_id = self.table.methods.get((pkg, type_name, field_name))
        if method_id is not None:
            self.crossings.append((node, method_id, "method"))
            return
        record = self.table.types.get(base)
        if record is None:
            self.refused = self.refused + 1
            return
        field_id = record["fields"].get(field_name)
        if field_id is not None:
            self.crossings.append((node, field_id, "field"))
            return
        self.refused = self.refused + 1


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go-src", required=True)
    ap.add_argument("--graph", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--compare-closed", type=int, default=8424,
                    help="how many selector frontier records lap two closed, "
                         "so this run can report the DELTA honestly")
    args = ap.parse_args()

    parser = Parser(bg.GO_LANG)
    files = bg.collect_region(args.go_src)
    sys.stderr.write("region: %d files\n" % len(files))

    path_to_pkg = {}
    for pkg_rel in bg.WHOLE_PACKAGES + [bg.SSA_PACKAGE]:
        path_to_pkg["cmd/compile/" + pkg_rel] = pkg_rel

    table = rd.TypeTable()
    results = ResultTable()
    trees = {}
    file_pkg = {}
    for path, pkg_rel, fname, gen in files:
        rel = os.path.relpath(path, args.go_src)
        handle = open(path, "rb")
        src = handle.read()
        handle.close()
        tree = parser.parse(src)
        trees[rel] = (src, tree, pkg_rel)
        file_pkg[rel] = pkg_rel
        rd.scan_declarations(table, rel, pkg_rel, src, tree.root_node)
        rd.set_source(src)
        scan_results(results, rel, pkg_rel, tree.root_node)

    imports_by_file = {}
    for rel, (src, tree, pkg_rel) in trees.items():
        imports_by_file[rel] = bg.collect_imports(src, tree.root_node)

    sys.stderr.write("named types in region: %d\n" % len(table.types))
    sys.stderr.write("struct fields recorded: %d\n" % len(table.new_nodes))
    sys.stderr.write("methods by receiver type: %d\n" % len(table.methods))
    sys.stderr.write("funcs with one declared result: %d\n" % len(results.funcs))
    sys.stderr.write("methods with one declared result: %d\n"
                     % len(results.methods))

    resolved = {}
    refused_total = 0
    qualified_used = 0
    result_type_used = 0
    waiting = {}
    for rel, (src, tree, pkg_rel) in trees.items():
        rd.set_source(src)
        walker = DotWalker2(table, results, rel, pkg_rel, src, tree.root_node,
                            imports_by_file[rel], path_to_pkg,
                            imports_by_file, file_pkg)
        got = walker.run()
        refused_total = refused_total + walker.refused
        qualified_used = qualified_used + walker.used_qualified
        result_type_used = result_type_used + walker.used_result_type
        for (node, target_id, how) in got:
            key = (rel, node.start_byte, node.end_byte)
            resolved[key] = (target_id, how)
        for (start_byte, end_byte), path in walker.waiting_on.items():
            waiting[(rel, start_byte, end_byte)] = path

    sys.stderr.write("selectors crossed by the rules: %d\n" % len(resolved))
    sys.stderr.write("selectors refused: %d\n" % refused_total)
    sys.stderr.write("crossings that used a QUALIFIED field type: %d\n"
                     % qualified_used)
    sys.stderr.write("crossings that used a DECLARED RESULT type: %d\n"
                     % result_type_used)

    sys.stderr.write("loading the map ...\n")
    handle = open(args.graph)
    doc = json.load(handle)
    handle.close()

    old_frontier = doc["frontier"]
    kept = []
    dropped = 0
    dropped_ids = set()
    selector_total = 0
    renamed = 0
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
        path = waiting.get(key)
        if path is not None:
            record["reason"] = ("field or method selector; the declared type "
                                "is qualified and its package %s is OUTSIDE "
                                "the parsed region" % path)
            record["waiting_on_package"] = path
            renamed = renamed + 1
        kept.append(record)

    sys.stderr.write("lap-one selector frontier records: %d\n" % selector_total)
    sys.stderr.write("of those, now crossed: %d\n" % dropped)
    sys.stderr.write("lap two crossed: %d\n" % args.compare_closed)
    sys.stderr.write("NEW this lap: %d\n" % (dropped - args.compare_closed))
    sys.stderr.write("refusals given a named package instead of "
                     "'no type information': %d\n" % renamed)

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
        have.add(node_id)
        added_fields = added_fields + 1

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
        edge_kind = "field_via_declared_type"
        if how == "method":
            edge_kind = "method_via_declared_type"
        key = (ref_id, target_id, "resolves_to", edge_kind)
        if key in seen_edge:
            continue
        edges.append({"src": ref_id, "dst": target_id,
                      "type": "resolves_to", "kind": edge_kind})
        seen_edge.add(key)
        added_edges = added_edges + 1

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

    meta = doc["meta"]
    meta["lap"] = 4
    meta["third_resolution_step"] = {
        "tool": "compiler_graph/resolve_dots2.py",
        "rule_1": "a declared type spelled pkg.T is resolved through the "
                  "imports of the file where the DECLARATION is written; if "
                  "that import path is a parsed package, T is looked up there "
                  "exactly as a bare name is",
        "rule_2": "x := call(...) binds x to the callee's ONE declared result "
                  "type, when the callee is a func or method declared in the "
                  "parsed region; callees with several results are refused",
        "not_done": ["type inference from ordinary assignments",
                     "interface method sets", "embedded-field promotion",
                     "generic instantiation",
                     "multi-result calls bound positionally"],
        "named_types_in_region": len(table.types),
        "funcs_with_one_declared_result": len(results.funcs),
        "methods_with_one_declared_result": len(results.methods),
        "struct_field_nodes_added": added_fields,
        "selectors_crossed": len(resolved),
        "selectors_refused": refused_total,
        "crossings_using_a_qualified_field_type": qualified_used,
        "crossings_using_a_declared_result_type": result_type_used,
        "lap_one_selector_frontier_records": selector_total,
        "selector_frontier_records_closed": dropped,
        "selector_frontier_records_closed_by_lap_two": args.compare_closed,
        "selector_frontier_records_closed_NEW_this_lap":
            dropped - args.compare_closed,
        "refusals_renamed_with_the_package_they_wait_on": renamed,
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
    sys.stderr.write(json.dumps(meta["third_resolution_step"], indent=2) + "\n")
    sys.stderr.write("wrote %s\n" % args.out)


if __name__ == "__main__":
    main()
