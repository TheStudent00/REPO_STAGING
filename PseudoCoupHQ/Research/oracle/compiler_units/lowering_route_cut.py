#!/usr/bin/env python3
"""lowering_route_cut.py -- task o5, arch_unit_oracle line, compiler_units
node, sub-node lowering_route_cut. Step 1 of the master order.

CORE (node_0_3_2_0_2_lowering_route_cut), verbatim: "the variant records
of variants_by_search cut to the LOWERING ROUTE -- the emitter
definitions task 95 found (57 in go, 251 in clang, arch-opcode-nodes,
log_200) and the functions task 81's diaries recorded per operator
probe -- so the operators a compiler's routing uses are counted apart
from its whole source. Answers the owner's surprise at the whole-source counts
(2026-09-06): the routing is expected to use tens of variants in a
handful of types."

WHAT "ON THE LOWERING ROUTE" MEANS, made mechanical
----------------------------------------------------
o4 (operator_variants_by_search.py) found operator SITES in a
compiler's own source (go_compiler and clang_llvm_cpp rows only --
the two rows with route data; rustc/swift_stdlib/swiftc_compiler/
go_stdlib have neither a diary nor an arch-opcode-node measurement and
are out of scope here, unchanged from o4's json). A site is ON THE
ROUTE when its ENCLOSING FUNCTION's own declaration coordinate
(file, start_line), in the checkout-relative spelling arch_opcode_nodes
and the diaries already use, is a member of the union of:

  (a) EMITTER DEFINITIONS -- task 95's `definitions_marked` in
      arch_opcode_nodes_{go,cpp}.json: a function whose OWN source
      names or reaches a machine-instruction emitter. 57 for go, 251
      for clang (log_200 section 1.2). These are already exactly the
      non-`emits_nothing` definitions -- `definitions_marked`'s length
      equals `populations.definitions_with_at_least_one_call_site`.

  (b) DIARY-VISITED FUNCTIONS -- task 81/72's diaries: every function
      whose own hook fired while the instrumented compiler compiled
      SOME probe of the original corpus. One line's last `|`-separated
      field is always `file:line` of the enclosing function's own
      declaration (task 81's t81diary::note convention, log_190
      section 2.1-2.2; task 72's go lap uses the same last-field
      convention, checked below). Diary sources used: `diaries/go`
      (590 files, task 72's go lap) for go; `diaries/c_and_cpp` (1,380
      files, task 81's own headline population) for clang. `diaries/
      extended` (3,980, +2,600 regenerated probes) and the separate
      `diaries/c` (610) / `diaries/cpp` (770) directories are the same
      underlying content -- op_0.txt in `cpp/` and `c_and_cpp/c__op_0.
      txt` are hard-linked (`ls -la` link count 3) -- so `c_and_cpp` is
      not a narrower sample than `c`+`cpp` combined, and `extended`'s
      additional 2,600 regenerated-probe diaries are read SEPARATELY
      below and reported as a robustness check, not folded into the
      primary cut (task 95/81's own citation is the base corpus).

This does not re-run o4's full six-row scan. It re-scans ONLY the two
routed rows' own file sets (identical dirs/extensions to o4's
`rows_def`, reused not copied -- see the header comment there), because
o4's json stores per-variant SITE COUNTS, not each site's own file:line
and enclosing function (only a handful of sample excerpts are kept).
Getting the per-site enclosing-function coordinate needs the tree
walked again; the walk, the operand resolver, the collectors and the
operator-token inventory are IMPORTED from operator_variants_by_search.py
and compiler_operators_used.py, not forked. What is new here is: (1)
the enclosing-function-OWN-LINE map (o4's own `enclosing_stacks` keeps
the function node's tree-sitter id, not its line -- a small addition),
and (2) the two population sets from (a) and (b) above and the
route-membership filter.

THE SPELLING BAN, applied here exactly as o3/o4 explain it: the json
groups by ROW and lists route variants as per-row MEMBER entries (each
carrying `lang` + `unit`), never as a dict key. `check_no_spelling_
keys.py` is run over the produced json and its output pasted in the
log whatever it says.

Memory bound: 2 GB (ABORT_MEMORY_O5), per this task's own instance
config (o5.conf). The diary text (~2.3 GB across the directories
read) is streamed one line at a time; only the DISTINCT (file, line)
coordinates found are kept (thousands, not the size of the files).
"""
import json
import os
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compiler_operators_used import (  # noqa: E402 -- reuse, not fork
    HQ, SOURCES, build_language_inventory, lowered_set_for, iter_source_files,
    build_parser,
)
from operator_variants_by_search import (  # noqa: E402 -- reuse, not fork
    FUNC_TYPES, CLASS_TYPES, COLLECTORS, get_operator_text, operand_nodes,
    unwrap_and_resolve, describe, line_of,
)

MEMORY_BOUND_MB = 2048  # ABORT_MEMORY_O5, this task's own instance config


def abort_if_over_budget():
    peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak_kb / 1024.0
    if peak_mb > MEMORY_BOUND_MB:
        print(f"ABORT_MEMORY_O5: peak RSS {peak_mb:.1f} MB > {MEMORY_BOUND_MB} MB bound", file=sys.stderr)
        sys.exit(97)
    return peak_mb


GRAPHS = "PseudoCoupGraphs"
DIARIES = f"{GRAPHS}/diaries"

# ---------------------------------------------------------------------------
# the two routed rows -- SAME dirs/extensions as o4's rows_def (task o4's
# rows_def is a local in main(), not an importable constant; reproduced
# verbatim here so the scanned file population is identical to o4's)
# ---------------------------------------------------------------------------
ROUTED_ROWS = [
    ("clang_llvm_cpp", "clang/llvm (c, cpp)", "cpp",
     [f"{SOURCES}/llvm-project/llvm/lib/CodeGen/SelectionDAG",
      f"{SOURCES}/llvm-project/llvm/include/llvm/CodeGen",
      f"{SOURCES}/llvm-project/llvm/include/llvm/IR",
      f"{SOURCES}/llvm-project/llvm/include/llvm/MC",
      f"{SOURCES}/llvm-project/llvm/include/llvm/Target"],
     (".cpp", ".cc", ".cxx", ".h", ".hpp", ".inc", ".def"), "cpp"),
    ("go_compiler", "go (cmd/compile)", "go",
     [f"{SOURCES}/golang_src/src/cmd/compile"], (".go",), "go"),
]

# checkout-relative root each row's absolute paths are stripped of, to
# land on the SAME spelling arch_opcode_nodes.json and the diaries use
# ("src/cmd/compile/..." for go, "llvm/lib/..." / "clang/lib/..." for cpp)
CHECKOUT_ROOT = {
    "go_compiler": f"{SOURCES}/golang_src/",
    "clang_llvm_cpp": f"{SOURCES}/llvm-project/",
}

ARCH_OPCODE_NODES_PATH = {
    "go_compiler": f"{GRAPHS}/arch_opcode_nodes_go.json",
    "clang_llvm_cpp": f"{GRAPHS}/arch_opcode_nodes_cpp.json",
}

DIARY_DIRS = {
    "go_compiler": [f"{DIARIES}/go"],
    "clang_llvm_cpp": [f"{DIARIES}/c_and_cpp"],
}
DIARY_DIRS_ROBUSTNESS = {
    # not folded into the primary cut -- read separately, count only
    "clang_llvm_cpp": [f"{DIARIES}/extended"],
}


def load_emitter_defs(row_id):
    """task 95's definitions_marked: already exactly the non-emits_nothing
    definitions (populations.definitions_with_at_least_one_call_site)."""
    with open(ARCH_OPCODE_NODES_PATH[row_id]) as f:
        doc = json.load(f)
    defs = {}
    for rec in doc["definitions_marked"]:
        defs[(rec["file"], rec["start_line"])] = rec["state"]
    pop = doc["populations"]["definitions_with_at_least_one_call_site"]
    assert len(defs) == pop, f"{row_id}: definitions_marked len {len(defs)} != stated population {pop}"
    return defs


def stream_diary_visited(dirpaths):
    """Distinct (file, line) enclosing-function coordinates named in the
    LAST '|'-separated field of every diary line, across every .txt file
    in every dir given. One line at a time; only the distinct set is
    kept (bounded by the region's own definition count, not file size)."""
    visited = set()
    n_files = 0
    n_lines = 0
    n_unparsed = 0
    for d in dirpaths:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".txt"):
                continue
            n_files += 1
            path = os.path.join(d, fn)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    n_lines += 1
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) < 3:
                        n_unparsed += 1
                        continue
                    last = parts[2].split("|")[-1]
                    file_part, sep, line_part = last.rpartition(":")
                    if not sep or not line_part.isdigit():
                        n_unparsed += 1
                        continue
                    visited.add((file_part, int(line_part)))
            if n_files % 100 == 0:
                abort_if_over_budget()
    return visited, n_files, n_lines, n_unparsed


def enclosing_func_lines(root, lang):
    """node.id -> nearest enclosing function's OWN start line (1-based),
    or None. o4's own enclosing_stacks() keeps the function node's
    tree-sitter id, not its line; this is that map with the line kept
    instead, everything else identical."""
    func_types = FUNC_TYPES.get(lang, ())
    enc = {}

    def walk(n, cur_line):
        nl = cur_line
        if n.type in func_types:
            nl = n.start_point[0] + 1
        enc[n.id] = nl
        for c in n.children:
            walk(c, nl)
    walk(root, None)
    return enc


def enclosing_stacks_ids(root, lang):
    """Verbatim copy of o4's enclosing_stacks (id-based), needed for the
    scope lookup COLLECTORS' func_scopes/class_scopes are keyed by."""
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


def scan_file_for_route_sites(path, rel_path, parser, rule_tokens, lowered_ops,
                               lang, route_set, route_reason_of, row_id, out):
    """Mirrors o4's scan_file_for_variants classification (same rules,
    same helper calls) but restricted to sites whose ENCLOSING FUNCTION
    is a member of route_set, and keeping each such site's own
    file:line + the route reason, not just an aggregate count."""
    with open(path, "rb") as f:
        src_bytes = f.read()
    tree = parser.parse(src_bytes)
    root = tree.root_node
    func_line_of_node = enclosing_func_lines(root, lang)
    enc_ids = enclosing_stacks_ids(root, lang)
    func_scopes, class_scopes, global_scope = COLLECTORS[lang](root, src_bytes, lang)

    def scopes_for(node_id):
        fid, cid = enc_ids.get(node_id, (None, None))
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
                out["all_sites"] += 1
                func_line = func_line_of_node.get(node.id)
                route_key = (rel_path, func_line) if func_line is not None else None
                if route_key is not None and route_key in route_set:
                    out["route_sites"] += 1
                    operands = operand_nodes(node, lang)
                    scopes = scopes_for(node.id)
                    results = [unwrap_and_resolve(o, src_bytes, lang, scopes, path) for o in operands]
                    resolved = [r for r, _ in results if r is not None]
                    if operands and len(resolved) == len(operands):
                        if len(resolved) == 1:
                            vkey = (op, describe(resolved[0]), None)
                        else:
                            vkey = (op, describe(resolved[0]), describe(resolved[1]))
                        out["variant_counter"][vkey] = out["variant_counter"].get(vkey, 0) + 1
                        if len(out["route_examples"]) < 200:
                            # lang + unit (an OPAQUE id, never colon-joined with
                            # the operator token -- o3's own log_209 correction,
                            # rule 1 of the guard's violation list) so the
                            # operator sits on a genuine per-unit object, not a
                            # bare grouping key
                            ex_unit = f"{row_id}#ex{len(out['route_examples'])}"
                            out["route_examples"].append({
                                "lang": lang, "unit": ex_unit,
                                "site": f"{rel_path}:{line_of(node)}",
                                "operator": op,
                                "operand_types": [describe(r) for r in resolved],
                                "enclosing_function_line": func_line,
                                "route_reason": route_reason_of(route_key),
                            })
                    else:
                        out["route_unresolved"] += 1
        for c in node.children:
            walk(c)
    walk(root)
    del tree
    del src_bytes


def run_row(row_id, compiler, lang_for_inventory, dirs, extensions, lang, inv, lowered, parser):
    checkout_root = CHECKOUT_ROOT[row_id]
    emitter_defs = load_emitter_defs(row_id)
    diary_visited, diary_n_files, diary_n_lines, diary_n_unparsed = stream_diary_visited(DIARY_DIRS[row_id])

    def reason_of(key):
        in_e = key in emitter_defs
        in_d = key in diary_visited
        if in_e and in_d:
            return "emitter_def+diary"
        if in_e:
            return "emitter_def"
        return "diary"

    route_set = set(emitter_defs) | diary_visited
    both = set(emitter_defs) & diary_visited

    out = {"all_sites": 0, "route_sites": 0, "route_unresolved": 0,
           "variant_counter": {}, "route_examples": []}
    n_files = 0
    parse_failures = 0
    for d in dirs:
        for path in iter_source_files(d, extensions, None, None):
            n_files += 1
            rel_path = path[len(checkout_root):] if path.startswith(checkout_root) else path
            try:
                scan_file_for_route_sites(path, rel_path, parser, inv["rule_tokens"], lowered,
                                           lang, route_set, reason_of, row_id, out)
            except Exception as e:
                parse_failures += 1
                if parse_failures <= 3:
                    print(f"  [warn] {path}: {e!r}", file=sys.stderr)
            if n_files % 500 == 0:
                abort_if_over_budget()

    variants_list = []
    for (op, lhs, rhs), count in out["variant_counter"].items():
        unit_id = f"{row_id}#route_var{len(variants_list)}"
        operands_out = [{"lang": lang, "unit": f"{unit_id}#lhs", "role": "lhs", "spelling": lhs}]
        if rhs is not None:
            operands_out.append({"lang": lang, "unit": f"{unit_id}#rhs", "role": "rhs", "spelling": rhs})
        variants_list.append({
            "lang": lang, "unit": unit_id, "operator": op,
            "operands": operands_out, "sites": count,
        })
    variants_list.sort(key=lambda v: -v["sites"])
    for i, v in enumerate(variants_list):
        old_unit = v["unit"]
        v["unit"] = f"{row_id}#route_var{i}"
        for o in v["operands"]:
            o["unit"] = o["unit"].replace(old_unit, v["unit"])

    # robustness check for clang: diaries/extended (+2,600 regenerated
    # probes), coordinate-set size only, not folded into the cut above
    extended_note = None
    if row_id in DIARY_DIRS_ROBUSTNESS:
        ext_visited, ext_n_files, ext_n_lines, _ = stream_diary_visited(DIARY_DIRS_ROBUSTNESS[row_id])
        extended_note = {
            "dirs": DIARY_DIRS_ROBUSTNESS[row_id], "n_files": ext_n_files,
            "n_lines": ext_n_lines, "distinct_coords": len(ext_visited),
            "distinct_coords_gained_over_base_diary": len(ext_visited - diary_visited),
        }

    return {
        "row_id": row_id, "compiler": compiler, "written_in": lang,
        "source_files_parsed": n_files, "parse_failures": parse_failures,
        "population_at_each_filter": {
            "whole_source_sites_all_lowered_operators": out["all_sites"],
            "emitter_definitions": len(emitter_defs),
            "diary_visited_functions": len(diary_visited),
            "emitter_definitions_also_diary_visited": len(both),
            "route_population_union": len(route_set),
            "sites_on_route_total": out["route_sites"],
            "sites_on_route_resolved_to_a_variant": sum(v["sites"] for v in variants_list),
            "sites_on_route_unresolved_or_partial": out["route_unresolved"],
            "distinct_route_variants": len(variants_list),
        },
        "diary_source": {"dirs": DIARY_DIRS[row_id], "n_files": diary_n_files,
                          "n_lines": diary_n_lines, "n_unparsed_lines": diary_n_unparsed},
        "diary_extended_robustness_check": extended_note,
        "route_variants": variants_list,
        "route_examples_sample": out["route_examples"][:40],
    }


def main():
    t0 = time.time()
    from compiler_operators_used import OPERATOR_ARITY_PATH
    with open(OPERATOR_ARITY_PATH) as f:
        arity_doc = json.load(f)
    inv = {lang: build_language_inventory(lang, arity_doc) for lang in ("go", "cpp")}
    lowered = {lang: lowered_set_for(lang) for lang in ("go", "cpp")}

    import tree_sitter_cpp
    import tree_sitter_go
    parser_cpp = build_parser(tree_sitter_cpp)
    parser_go = build_parser(tree_sitter_go)
    parsers = {"cpp": parser_cpp, "go": parser_go}

    rows = []
    for row_id, compiler, lang_for_inv, dirs, extensions, lang in ROUTED_ROWS:
        print(f"[{row_id}] scanning...")
        row = run_row(row_id, compiler, lang_for_inv, dirs, extensions, lang,
                       inv[lang], lowered[lang], parsers[lang])
        rows.append(row)
        pf = row["population_at_each_filter"]
        print(f"  {row_id}: files={row['source_files_parsed']} "
              f"whole_source_sites={pf['whole_source_sites_all_lowered_operators']} "
              f"route_sites={pf['sites_on_route_total']} "
              f"route_variants={pf['distinct_route_variants']}")

    peak_mb = abort_if_over_budget()
    meta = {
        "generated_by": "lowering_route_cut.py",
        "task": "o5", "line": "arch_unit_oracle", "node": "node_0_3_2_0_2_lowering_route_cut",
        "reused_from": "operator_variants_by_search.py (task o4) and compiler_operators_used.py "
                        "(task o3): build_language_inventory, lowered_set_for, build_parser, "
                        "iter_source_files, get_operator_text, operand_nodes, unwrap_and_resolve, "
                        "describe, COLLECTORS, FUNC_TYPES, line_of -- and o4's own rows_def dirs/"
                        "extensions for the two routed rows, reproduced verbatim",
        "new_in_this_task": "enclosing_func_lines() (the enclosing function's OWN start line, "
                             "where o4's enclosing_stacks() kept only its tree-sitter node id), "
                             "the emitter-definition + diary-visited route-membership sets, and "
                             "the route filter applied inside the site walk",
        "elapsed_s": round(time.time() - t0, 1),
        "peak_rss_mb": round(peak_mb, 1),
        "memory_bound_mb": MEMORY_BOUND_MB,
        "rows_out_of_scope": ["go_stdlib", "rustc", "swiftc_compiler", "swift_stdlib"],
        "rows_out_of_scope_reason": "no arch-opcode-node measurement and no diary for these four "
                                     "rows (task 95/81/72 never ran the go stdlib, rustc or swift "
                                     "rows) -- unchanged from o4's json, not cut here.",
    }
    out_doc = {"meta": meta, "rows": rows}
    out_dir = f"{HQ}/Research/oracle/compiler_units"
    with open(f"{out_dir}/lowering_route_cut.json", "w") as f:
        json.dump(out_doc, f, indent=2, sort_keys=False)
    write_markdown(out_doc, f"{out_dir}/lowering_route_cut.md")
    print(f"done in {time.time()-t0:.1f}s, peak RSS {peak_mb:.1f} MB")


def write_markdown(out_doc, path):
    lines = ["# lowering_route_cut", "", "Generated by `lowering_route_cut.py` (task o5).", ""]
    m = out_doc["meta"]
    lines.append(f"Elapsed {m['elapsed_s']}s, peak RSS {m['peak_rss_mb']} MB "
                 f"(bound {m['memory_bound_mb']} MB).")
    lines.append("")
    for row in out_doc["rows"]:
        pf = row["population_at_each_filter"]
        lines.append(f"## {row['row_id']} ({row['compiler']})")
        lines.append("")
        lines.append("| filter stage | count |")
        lines.append("|---|---|")
        for k, v in pf.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
        ds = row["diary_source"]
        lines.append(f"Diary source: `{', '.join(ds['dirs'])}` -- {ds['n_files']} files, "
                     f"{ds['n_lines']} lines, {ds['n_unparsed_lines']} unparsed.")
        if row.get("diary_extended_robustness_check"):
            ext = row["diary_extended_robustness_check"]
            lines.append(f"Robustness check, `{', '.join(ext['dirs'])}`: {ext['n_files']} files, "
                         f"{ext['distinct_coords']} distinct coordinates "
                         f"({ext['distinct_coords_gained_over_base_diary']} beyond the base diary).")
        lines.append("")
        lines.append("| operator | lhs | rhs | sites |")
        lines.append("|---|---|---|---|")
        for v in row["route_variants"]:
            ops = v["operands"]
            lhs = ops[0]["spelling"] if ops else ""
            rhs = ops[1]["spelling"] if len(ops) > 1 else ""
            lines.append(f"| {v['operator']} | {lhs} | {rhs} | {v['sites']} |")
        lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
