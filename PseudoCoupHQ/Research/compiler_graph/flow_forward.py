#!/usr/bin/env python3
"""flow_forward.py -- the THIRD step: value MOVEMENT, forward only.

Lap two taught the map to cross `x.f` (resolve_dots.py, graph_go2.json).  That
gave a CONNECTION between the abi region and internal/amd64, but only when
several edges were walked backwards, and a backwards edge means "this same
declaration is also read over there", not "this value moves to there".  The
identity proof needs movement: a chain every hop of which is followed in the
direction the value travels.

Four things the map could not say, added here as new directed edges.

  1. store_to_field       v -> the field DECLARATION of f, for `x.f = v`
                          (and `x.f += v`, and `x.f = append(x.f, v)`, which
                          the map already routes through a call node).
     literal_to_field     v -> the field declaration of f, for the OTHER way
                          a field is written in Go: `T{f: v}`.  Without this
                          the movement dies at every constructor, and Go's
                          compiler builds most of its records that way
                          (abiutils.go:616 `Registers: registers,` is the
                          exact spot lap three had to cross).
  2. field_to_read        the field declaration -> every resolved read `y.f`.
                          Rules 1 and 2 together make `v -> f -> read` a
                          forward walk: the value moves THROUGH the field.
     decl_to_read         the same shape for a plain value-holding
                          declaration: a parameter / local var / result
                          parameter / receiver / package var -> every
                          reference that resolves to it.  The map's
                          resolves_to edge is authored reference ->
                          declaration, which is the direction a NAME is
                          looked up, not the direction a VALUE travels; lap
                          two had to walk it backwards for that reason.  This
                          is that relation written down forwards, once, as
                          its own edge, so the query never reverses anything.
  3. argument_to_param    a call argument -> the callee's parameter
                          declaration, bound BY POSITION.
     return_to_call       a callee's return expression -> the call node.
     result_param_to_call a callee's named result declaration -> the call node.
                          Without these, movement dies at every function
                          boundary.
  4. (verified, not duplicated) the call node -> what the call's result is
                          assigned into is already flows_into/call_result,
                          emitted by build_graph.py's assignment().  This tool
                          counts those edges and re-uses them; it adds none.

THE MINIMALITY RULE (the owner, lap three).  Field-SENSITIVE, object-INsensitive:
which field f is matters; which object x holds it does not.  So rule 2 sends a
store into `a.f` to every read of `.f` anywhere in the region, including
`b.f`.  That is an OVER-APPROXIMATION and it is stated on every result this
map produces.  The static map bounds all runs; it does not claim any single
run took the path.  The diary's per-run events and the arch campaign's forced
probe stay the judges.

It is also FLOW-INsensitive: statement order inside a function is not
modelled, so a declaration reaches every read of it whether or not that read
runs after the store.  Same class of over-approximation, stated the same way.

Positional call binding inherits the map's call edges as they are, including
the one_to_many candidate sets (`calls/indirect` with a candidate_set): an
argument is bound to the matching parameter of EVERY candidate.  That is the
same over-approximation lap one already declared for dispatch.

Why a co-module, and why graph_go3.json.  Same reasoning as resolve_dots.py:
graph_go.json and graph_go2.json are the artifacts of record for laps one and
two and stay untouched, so the difference go2 -> go3 IS the measured answer to
"what did forward dataflow add".  A whole map rather than a side-car edge file
because query_path.py takes exactly one --graph and must run unchanged; a
side-car would have forced an edit to the query tool, and the query tool is
the thing whose behaviour must not move between laps.

Re-parses the region with the same pins as build_graph.py / resolve_dots.py,
because argument POSITION and return statements are syntax the map never
recorded.

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


# ------------------------------------------------------------ small helpers --

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


# --------------------------------------------------------- value-node lookup --

VALUE_KINDS = ("selector_expression", "identifier", "call_expression")

# declaration kinds that HOLD A VALUE at run time.  A func, a method, a type
# and a label are named things a value never sits inside, so they are not
# sources of movement.
VALUE_DECL_KINDS = ("param", "result_param", "receiver", "local_var",
                    "package_var")


def value_nodes(rel, node, have, out, depth=0):
    """Map-node ids that carry the value of an expression.

    An identifier or a selector is one ref node; a call is one call node.
    Anything else (a binary expression, a composite literal, a type
    conversion's operand) is descended into, and every mapped node found at
    the first mapped level is taken.  Descent stops as soon as a level maps,
    so `f(g(x))` binds the argument to g's call node, not to x as well.
    """
    if node is None:
        return
    if depth > 6:
        return
    kind = node.type
    if kind in VALUE_KINDS:
        if kind == "call_expression":
            candidate = call_id(rel, node)
        else:
            candidate = ref_id(rel, node)
        if candidate in have:
            out.append(candidate)
            return
    for child in node.named_children:
        value_nodes(rel, child, have, out, depth + 1)


# ------------------------------------------------------------ function index --

class FuncIndex:
    """Every function/method declaration: its id, its parameters in order."""

    def __init__(self):
        self.params = {}        # func node id -> [param node id, ...]
        self.variadic = {}      # func node id -> True/False
        self.returns = {}       # func node id -> [value node id, ...]
        self.result_params = {}  # func node id -> [result_param node id, ...]


def scan_params(rel, plist, kind, have):
    """Ordered declaration node ids of a parameter list, and the variadic flag."""
    ids = []
    variadic = False
    if plist is None:
        return ids, variadic
    for param in plist.named_children:
        if param.type == "variadic_parameter_declaration":
            variadic = True
        elif param.type != "parameter_declaration":
            continue
        names = []
        for child in param.children:
            if child.type == "identifier":
                names.append(child)
        if not names:
            # an unnamed parameter still occupies a position; a placeholder
            # keeps positional binding honest for the parameters after it.
            ids.append(None)
            continue
        for name_node in names:
            node_id = bg.nid(rel, name_node, kind)
            if node_id in have:
                ids.append(node_id)
            else:
                ids.append(None)
    return ids, variadic


def scan_returns(rel, body, have, out, depth=0):
    """Value node ids of every `return expr, ...` inside a function body."""
    if body is None:
        return
    if depth > 60:
        return
    for child in body.named_children:
        if child.type == "func_literal":
            continue          # a literal's returns belong to the literal
        if child.type == "return_statement":
            for item in child.named_children:
                if item.type == "expression_list":
                    for expr in item.named_children:
                        value_nodes(rel, expr, have, out)
                else:
                    value_nodes(rel, item, have, out)
        scan_returns(rel, child, have, out, depth + 1)


def index_functions(rel, root, have, index):
    for child in root.named_children:
        if child.type not in ("function_declaration", "method_declaration"):
            continue
        kind = "func"
        if child.type == "method_declaration":
            kind = "method"
        func_id = bg.nid(rel, child, kind)
        if func_id not in have:
            continue
        plist = child.child_by_field_name("parameters")
        params, variadic = scan_params(rel, plist, "param", have)
        index.params[func_id] = params
        index.variadic[func_id] = variadic
        result = child.child_by_field_name("result")
        results = []
        if result is not None and result.type == "parameter_list":
            results, _unused = scan_params(rel, result, "result_param", have)
        keep = []
        for item in results:
            if item is not None:
                keep.append(item)
        index.result_params[func_id] = keep
        returns = []
        scan_returns(rel, child.child_by_field_name("body"), have, returns)
        index.returns[func_id] = returns


# ------------------------------------------------------------- call scanning --

def scan_calls(rel, root, have, out, depth=0):
    """(call node id, [value node ids of argument 0, 1, ...]) for every call."""
    if depth > 200:
        return
    for child in root.named_children:
        if child.type == "call_expression":
            node_id = call_id(rel, child)
            if node_id in have:
                args = child.child_by_field_name("arguments")
                per_position = []
                if args is not None:
                    for arg in args.named_children:
                        found = []
                        value_nodes(rel, arg, have, found)
                        per_position.append(found)
                out.append((node_id, per_position))
        scan_calls(rel, child, have, out, depth + 1)


# ------------------------------------------------------- composite literals --

def literal_type(pkg_rel, type_node, table, imports, path_to_pkg):
    """`T{...}` / `pkg.T{...}` -> (pkg_dir, type_name) if declared in region."""
    wrapped = rd.unwrap_type(type_node)
    if wrapped is None:
        return None
    alias, name = wrapped
    if alias is None:
        key = (pkg_rel, name)
        if key in table.types:
            return key
        return None
    path = imports.get(alias)
    if path is None:
        return None
    other = path_to_pkg.get(path)
    if other is None:
        return None
    key = (other, name)
    if key in table.types:
        return key
    return None


def scan_literals(rel, pkg_rel, node, have, table, imports, path_to_pkg, out,
                  depth=0):
    """(value node id, field node id) for every `T{f: v}` written in the region."""
    if depth > 200:
        return
    for child in node.named_children:
        if child.type == "composite_literal":
            key = literal_type(pkg_rel, child.child_by_field_name("type"),
                               table, imports, path_to_pkg)
            body = child.child_by_field_name("body")
            if key is not None and body is not None:
                record = table.types.get(key)
                if record is not None:
                    collect_keyed(rel, body, have, record, out)
        scan_literals(rel, pkg_rel, child, have, table, imports, path_to_pkg,
                      out, depth + 1)


def unwrap_element(node):
    """tree-sitter-go wraps each half of a keyed_element in a literal_element."""
    if node is None:
        return None
    if node.type != "literal_element":
        return node
    for child in node.named_children:
        return child
    return None


def collect_keyed(rel, body, have, record, out):
    for element in body.named_children:
        if element.type != "keyed_element":
            continue
        pair = element.named_children
        if len(pair) != 2:
            continue
        key_node = unwrap_element(pair[0])
        value_node = unwrap_element(pair[1])
        if key_node is None or value_node is None:
            continue
        if key_node.type not in ("field_identifier", "identifier"):
            continue
        field_id = record["fields"].get(text(key_node))
        if field_id is None:
            continue
        found = []
        value_nodes(rel, value_node, have, found)
        for src in found:
            out.append((src, field_id))


# --------------------------------------------------------------------- main --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go-src", required=True)
    ap.add_argument("--graph", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sys.stderr.write("loading the map ...\n")
    handle = open(args.graph)
    doc = json.load(handle)
    handle.close()

    nodes_by_id = {}
    for node in doc["nodes"]:
        nodes_by_id[node["id"]] = node
    have = set(nodes_by_id)

    edges = list(doc["edges"])
    seen_edge = set()
    for edge in edges:
        key = (edge["src"], edge["dst"], edge["type"], edge.get("kind"))
        seen_edge.add(key)

    def add_edge(src, dst, kind, **extra):
        if src is None or dst is None:
            return 0
        if src not in have or dst not in have:
            return 0
        key = (src, dst, "flows_into", kind)
        if key in seen_edge:
            return 0
        record = {"src": src, "dst": dst, "type": "flows_into", "kind": kind}
        record.update(extra)
        edges.append(record)
        seen_edge.add(key)
        return 1

    # -- rule 1 and rule 2: through the field ------------------------------
    # A ref node that resolves to a field declaration is a resolved selector.
    field_of_ref = {}
    for edge in doc["edges"]:
        if edge["type"] != "resolves_to":
            continue
        if edge.get("kind") != "field_via_declared_type":
            continue
        field_of_ref[edge["src"]] = edge["dst"]

    # A ref node that something flows INTO is the left side of an assignment;
    # build_graph.py's assignment() emits exactly that, with kind value (a
    # plain right-hand side) or call_result (a call, which covers append).
    stores = defaultdict(list)
    for edge in doc["edges"]:
        if edge["type"] != "flows_into":
            continue
        if edge.get("kind") not in ("value", "call_result"):
            continue
        if edge["dst"] not in field_of_ref:
            continue
        stores[edge["dst"]].append(edge["src"])

    added_store = 0
    for lhs_ref, sources in stores.items():
        field_id = field_of_ref[lhs_ref]
        for src in sources:
            added_store = added_store + add_edge(
                src, field_id, "store_to_field", via_selector=lhs_ref)

    added_read = 0
    for read_ref, field_id in field_of_ref.items():
        added_read = added_read + add_edge(
            field_id, read_ref, "field_to_read")

    # a declaration that HOLDS A VALUE -> every reference that resolves to it
    added_decl_read = 0
    for edge in doc["edges"]:
        if edge["type"] != "resolves_to":
            continue
        if edge.get("kind") not in (None, "cross_package_in_region"):
            continue
        target = nodes_by_id.get(edge["dst"])
        if target is None:
            continue
        if target["kind"] not in VALUE_DECL_KINDS:
            continue
        added_decl_read = added_decl_read + add_edge(
            edge["dst"], edge["src"], "decl_to_read")

    # -- re-parse for syntax the map never recorded ------------------------
    parser = Parser(bg.GO_LANG)
    files = bg.collect_region(args.go_src)
    sys.stderr.write("region: %d files\n" % len(files))

    path_to_pkg = {}
    for pkg_rel in bg.WHOLE_PACKAGES + [bg.SSA_PACKAGE]:
        path_to_pkg["cmd/compile/" + pkg_rel] = pkg_rel

    # pass A: parse every file and rebuild lap two's table of named types,
    # because the composite-literal rule needs to know which type `T{...}` is.
    trees = {}
    table = rd.TypeTable()
    for path, pkg_rel, fname, gen in files:
        rel = os.path.relpath(path, args.go_src)
        handle = open(path, "rb")
        src = handle.read()
        handle.close()
        tree = parser.parse(src)
        trees[rel] = (src, tree, pkg_rel)
        rd.scan_declarations(table, rel, pkg_rel, src, tree.root_node)

    # pass B: the syntax the map never recorded
    index = FuncIndex()
    calls = []
    literal_writes = []
    for rel, (src, tree, pkg_rel) in trees.items():
        set_source(src)
        rd.set_source(src)
        index_functions(rel, tree.root_node, have, index)
        scan_calls(rel, tree.root_node, have, calls)
        imports = bg.collect_imports(src, tree.root_node)
        scan_literals(rel, pkg_rel, tree.root_node, have, table, imports,
                      path_to_pkg, literal_writes)

    added_literal = 0
    for (src_id, field_id) in literal_writes:
        added_literal = added_literal + add_edge(
            src_id, field_id, "literal_to_field")

    sys.stderr.write("functions indexed: %d\n" % len(index.params))
    sys.stderr.write("call sites re-parsed: %d\n" % len(calls))

    # -- rule 3: across the function boundary ------------------------------
    # callees of a call node, taken from the map's own calls edges
    callees = defaultdict(list)
    for edge in doc["edges"]:
        if edge["type"] != "calls":
            continue
        target = nodes_by_id.get(edge["dst"])
        if target is None:
            continue
        if target["kind"] not in ("func", "method"):
            continue
        callees[edge["src"]].append(edge["dst"])

    added_arg = 0
    bound_calls = 0
    unbound_calls = 0
    for (node_id, per_position) in calls:
        targets = callees.get(node_id, ())
        if not targets:
            unbound_calls = unbound_calls + 1
            continue
        bound_calls = bound_calls + 1
        for func_id in targets:
            params = index.params.get(func_id)
            if not params:
                continue
            variadic = index.variadic.get(func_id, False)
            for position, sources in enumerate(per_position):
                slot = position
                if slot >= len(params):
                    if not variadic:
                        continue
                    slot = len(params) - 1
                param_id = params[slot]
                for src in sources:
                    added_arg = added_arg + add_edge(
                        src, param_id, "argument_to_param",
                        position=position, callee=func_id)

    added_return = 0
    added_result_param = 0
    for (node_id, _per_position) in calls:
        for func_id in callees.get(node_id, ()):
            for src in index.returns.get(func_id, ()):
                added_return = added_return + add_edge(
                    src, node_id, "return_to_call", callee=func_id)
            for src in index.result_params.get(func_id, ()):
                added_result_param = added_result_param + add_edge(
                    src, node_id, "result_param_to_call", callee=func_id)

    # -- rule 4: verified, re-used, not duplicated -------------------------
    existing_call_result = 0
    for edge in doc["edges"]:
        if edge["type"] != "flows_into":
            continue
        if edge.get("kind") == "call_result":
            existing_call_result = existing_call_result + 1

    # ------------------------------------------------------------- write --
    meta = doc["meta"]
    meta["lap"] = 3
    meta["forward_dataflow_step"] = {
        "tool": "compiler_graph/flow_forward.py",
        "direction": "forward only; no edge in this map is meant to be walked "
                     "backwards, and the acceptance query walks none",
        "over_approximation": "field-sensitive, object-INsensitive: a store "
                              "into a.f reaches every read of .f in the "
                              "region, b.f included.  Call binding follows "
                              "the map's candidate sets, so an argument binds "
                              "to the matching parameter of every candidate "
                              "callee.  Both are bounds over all runs, never "
                              "a claim about one run.",
        "rule_1_store_to_field": added_store,
        "rule_1_literal_to_field": added_literal,
        "rule_2_field_to_read": added_read,
        "rule_2_decl_to_read": added_decl_read,
        "rule_3_argument_to_param": added_arg,
        "rule_3_return_to_call": added_return,
        "rule_3_result_param_to_call": added_result_param,
        "rule_4_call_result_edges_reused_not_added":
            existing_call_result,
        "call_sites_with_a_known_callee": bound_calls,
        "call_sites_with_no_callee_in_the_map": unbound_calls,
        "functions_indexed": len(index.params),
        "not_done": [
            "object sensitivity (which x holds f)",
            "positional (unkeyed) composite literals: T{v1, v2} is refused, "
            "only T{f: v} is crossed",
            "flow sensitivity (statement order inside a function)",
            "interface dispatch beyond the map's candidate sets",
            "closures: a func literal's parameters and returns are not bound",
            "unnamed parameters occupy their position but carry no node",
        ],
    }
    counts = meta["counts"]
    counts["nodes"] = len(doc["nodes"])
    counts["edges"] = len(edges)

    doc["edges"] = edges
    handle = open(args.out, "w")
    json.dump(doc, handle)
    handle.close()
    sys.stderr.write(json.dumps(meta["forward_dataflow_step"], indent=2) + "\n")
    sys.stderr.write("wrote %s\n" % args.out)


if __name__ == "__main__":
    main()
