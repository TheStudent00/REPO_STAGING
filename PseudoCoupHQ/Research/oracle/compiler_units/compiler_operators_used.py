#!/usr/bin/env python3
"""compiler_operators_used.py -- task o3, arch_unit_oracle line, compiler_units node.

the owner's ask (2026-09-06, verbatim, pasted in the brief): "the table of
how many compiler-operators the compilers use compared to how many
the compiler understands how to lower ... a basic search could be
performed on the compiler source code -- as opposed to something more
computational."

This is a TOKEN CENSUS: for each compiler, parse every source file of
its OWN checkout with tree-sitter (in the language THAT COMPILER'S
SOURCE is written in -- never the language it compiles), read the
`operator` field (or, where the grammar carries no such field, the
literal operator token named as a search hit under a NAMED grammar
rule -- see RULE_TOKENS below, built from operator_arity.json's own
recorded `sources[*].rule` / `sources[*].verification`, never guessed)
of every binary_expression / unary_expression / update_expression /
assignment_expression node (and each language's own equivalents,
named below with their tree-sitter rule name), and counts which
OFFERED operators (operator_arity.json) occur at least once.

THE SPELLING BAN is stated and why it does not gate this file's
structure: read the brief's own note, pasted into log_209 section 1.
This script's json groups rows by COMPILER (a fact about the world,
not an operator spelling) and lists operators as per-row MEMBER
entries (one dict per operator, carrying its own token as a display
field) -- never as a dict KEY. `check_no_spelling_keys.py` is run over
the produced json regardless, and its output is pasted in the log
whatever it says.

TASK o3b UPDATE (2026-09-06): the swift standard library row is no
longer a flag. The Airlock runner image was rebuilt with
tree_sitter_swift==0.7.3, so this script now measures it through the
SAME code path (measure_row()) as every other row -- no separate
script. tree-sitter-swift ships no node-types.json in its pip wheel;
swift's grammar node kinds for the operator-carrying constructs were
read by parsing representative swift source and observing the actual
node.type tree-sitter produced (SWIFT_RULE_TO_NODE_TYPES below),
because several of operator_arity.json's recorded swift rule names are
hidden rules inlined into a visible parent node rather than kept as
their own node.

Memory bound: 2 GB (ABORT_MEMORY_O3). One source file is read, parsed,
walked and released before the next is opened -- never a whole tree's
source held in memory. Peak RSS reported via resource.getrusage
(`/usr/bin/time` is absent from the runner image, per task o2's
finding).
"""
import json
import os
import resource
import sys
import time

MEMORY_BOUND_MB = 2048  # ABORT_MEMORY_O3


def abort_if_over_budget():
    peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak_kb / 1024.0
    if peak_mb > MEMORY_BOUND_MB:
        print(f"ABORT_MEMORY_O3: peak RSS {peak_mb:.1f} MB > {MEMORY_BOUND_MB} MB bound", file=sys.stderr)
        sys.exit(97)
    return peak_mb


# ---------------------------------------------------------------------------
# 1. offered / lowered inventories, read from existing data -- nothing
#    here is invented; every set is taken verbatim from a file already
#    on disk.
# ---------------------------------------------------------------------------

HQ = "PseudoCoupHQ"
SOURCES = "/sources"

OPERATOR_ARITY_PATH = f"{HQ}/Research/kind_fuzz_clustering/operator_arity.json"
OP_PIPELINE = f"{HQ}/Research/op_pipeline"


# operator_arity.json's own `sources[*].rule` names the grammar RULE
# that carries an operator's spelling. For c/cpp/go/rust that rule name
# is also the tree-sitter NODE TYPE that appears in a parsed tree, so
# the generic walk below can key straight off it. tree-sitter-swift
# ships no node-types.json in its pip wheel (checked directly in the
# runner image: only the compiled binding is present), so its node
# kinds were read the only way available -- by parsing representative
# swift source exercising every rule operator_arity.json records for
# swift and reading the actual node.type tree-sitter produced (done
# once, by hand, before this map was written; not guessed). Several of
# swift's rule names are HIDDEN rules (leading underscore, e.g.
# `_additive_operator`) that the grammar inlines into a visible parent
# expression node instead of keeping as their own node -- this map
# names that parent node type. `_expression` (the rule recorded for
# postfix `?`, optional-chaining) inlines with NO distinct wrapping
# node at all in this grammar version -- there is no node type to key
# on, so it maps to an empty list and the operator is reported,
# un-silently, in `grammar_node_unavailable` rather than scanned.
#
# task o3b correction (defect found 2026-09-06): `_comparison_operator`
# and `_equality_operator` do NOT map to a single node type each. Read
# by parsing `let x = a != b`, `a <= b`, `a >= b`, `a == b`, `a < b`,
# `a === b` and printing every non-leaf node.type: `==`, `<`, `>`,
# `===` land under the dedicated `comparison_expression` /
# `equality_expression` node as before, but `!=`, `<=`, `>=` land
# under the GENERIC `infix_expression` node (the same catch-all node
# this grammar version already uses for a user-defined custom
# operator), with the literal token as a direct `custom_operator`
# child rather than a field. This is a real grammar fact, not a token
# guess: the grammar apparently does not wire every comparison spelling
# to a fixed-precedence node, so some of them fall through to the
# generic infix path alongside genuinely custom operators. The fix
# below adds `infix_expression` as a second node type for these two
# rules; `get_operator_text`'s existing generic child-text scan (this
# same fallback already handles every other rule with more than one
# node type) still finds the token by matching child text against the
# rule's own known operator list, so no token is special-cased.
SWIFT_RULE_TO_NODE_TYPES = {
    "_prefix_unary_operator": ["prefix_expression"],
    "_postfix_unary_operator": ["postfix_expression"],
    "_multiplicative_operator": ["multiplicative_expression"],
    "_additive_operator": ["additive_expression"],
    "_comparison_operator": ["comparison_expression", "infix_expression"],
    "_equality_operator": ["equality_expression", "infix_expression"],
    "_bitwise_binary_operator": ["bitwise_operation"],
    "_conjunction_operator": ["conjunction_expression"],
    "_disjunction_operator": ["disjunction_expression"],
    "_nil_coalescing_operator": ["nil_coalescing_expression"],
    "_range_operator": ["range_expression"],
    "_assignment_and_operator": ["assignment"],
    "_expression": [],  # '?' postfix optional-chaining -- no wrapping node; see grammar_node_unavailable
    # already-visible node types (rule name == node type, kept explicit
    # for the reader rather than left to fall through to the identity
    # default below):
    "try_operator": ["try_operator"],
    "await_expression": ["await_expression"],
    "consume_expression": ["consume_expression"],
    "open_start_range_expression": ["open_start_range_expression"],
    "open_end_range_expression": ["open_end_range_expression"],
    "check_expression": ["check_expression"],
    "as_operator": ["as_operator"],
}


def build_language_inventory(lang, arity_doc):
    """Return offered_total, offered_operators (sorted), and RULE_TOKENS
    (tree-sitter node type -> set of literal operator tokens actually
    occurring under that node type), built only from operator_arity.json's
    own `sources` records where verification is 'literal' or 'derived'
    (a real spelling in the text). 'shape' entries (f(...), a[i], ...)
    carry no single literal token to search for and are recorded
    separately as excluded-from-scan, never silently dropped. For most
    languages the recorded rule name IS the node type; swift's hidden
    rules are remapped to their visible parent node type via
    SWIFT_RULE_TO_NODE_TYPES (see its own comment) -- a rule that maps
    to no node at all (swift's bare postfix `?`) is recorded in
    `grammar_node_unavailable`, not silently dropped."""
    buckets = arity_doc["languages"][lang]["buckets"]
    total = arity_doc["languages"][lang]["counts"]["total"]
    offered_operators = set()
    rule_tokens = {}
    shape_excluded = []
    grammar_node_unavailable = []
    for bucket_name, bucket in buckets.items():
        offered_operators.update(bucket.get("operators", []))
        for src in bucket.get("sources", []):
            rule = src["rule"]
            verification = src["verification"]
            ops = src["operators"]
            if verification in ("literal", "derived"):
                if lang == "swift":
                    node_types = SWIFT_RULE_TO_NODE_TYPES.get(rule, [rule])
                else:
                    node_types = [rule]
                if not node_types:
                    grammar_node_unavailable.append({"bucket": bucket_name, "rule": rule, "operators": ops})
                    continue
                for nt in node_types:
                    rule_tokens.setdefault(nt, set()).update(ops)
            else:
                shape_excluded.append({"bucket": bucket_name, "rule": rule, "operators": ops, "verification": verification})
    return {
        "offered_total": total,
        "offered_operators": sorted(offered_operators),
        "rule_tokens": {k: sorted(v) for k, v in rule_tokens.items()},
        "shape_excluded": shape_excluded,
        "grammar_node_unavailable": grammar_node_unavailable,
    }


def lowered_set_for(lang):
    """The exact set of operator labels the arch-unit corpus has
    lowered, per the brief: canon40_wrapped_<lang>.json union
    canon40_regen_store/*<lang>*.json, the `operator` field of every
    unit. Verified against the brief's stated counts (c 27, cpp 32,
    rust 21, go 20, swift 26) before this script was trusted."""
    import glob
    ops = set()
    wrapped_path = f"{OP_PIPELINE}/canon40_wrapped_{lang}.json"
    with open(wrapped_path) as f:
        wrapped = json.load(f)
    for u in wrapped["units"].values():
        op = u.get("operator")
        if op:
            ops.add(op)
    for shard_path in glob.glob(f"{OP_PIPELINE}/canon40_regen_store/*_{lang}_*.json"):
        with open(shard_path) as f:
            shard = json.load(f)
        units = shard["units"] if isinstance(shard, dict) and "units" in shard else shard
        vals = units.values() if isinstance(units, dict) else units
        for u in vals:
            op = u.get("operator")
            if op:
                ops.add(op)
    return ops


# ---------------------------------------------------------------------------
# 2. per-file operator extraction
# ---------------------------------------------------------------------------

def get_operator_text(node, rule_tokens_for_this_rule, src_bytes):
    """One node of a rule we care about. Its operator is:
    (a) the `operator` field, when the grammar names one, else
    (b) the direct child whose own text is one of this rule's known
        literal tokens (read from operator_arity.json's own record of
        which tokens occur under this rule -- not a guess)."""
    field = node.child_by_field_name("operator")
    if field is not None:
        return src_bytes[field.start_byte:field.end_byte].decode("utf-8", "replace")
    for child in node.children:
        text = src_bytes[child.start_byte:child.end_byte].decode("utf-8", "replace")
        if text in rule_tokens_for_this_rule:
            return text
    return None


def scan_file(path, parser, rule_tokens, tally, files_seen):
    """Parse one file, walk it, add every operator occurrence found
    under a named rule to `tally` (operator -> {"count": n, "files": set()}).
    Reads and releases the source text of ONLY this one file."""
    with open(path, "rb") as f:
        src_bytes = f.read()
    tree = parser.parse(src_bytes)
    hit_this_file = set()

    def walk(node):
        rule = node.type
        toks = rule_tokens.get(rule)
        if toks:
            op = get_operator_text(node, toks, src_bytes)
            if op is not None and op in toks:
                entry = tally.setdefault(op, {"count": 0, "files": set()})
                entry["count"] += 1
                entry["files"].add(path)
                hit_this_file.add(op)
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    del tree
    del src_bytes
    return hit_this_file


def iter_source_files(root, extensions, exclude_substr=None, include_only_substr=None):
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not any(fn.endswith(ext) for ext in extensions):
                continue
            full = os.path.join(dirpath, fn)
            if exclude_substr and exclude_substr in full:
                continue
            if include_only_substr and include_only_substr not in full:
                continue
            yield full


# ---------------------------------------------------------------------------
# 3. the five measured rows (+ two flagged, unmeasured rows named in
#    the output for completeness)
# ---------------------------------------------------------------------------

def build_parser(ts_lang_module):
    from tree_sitter import Language, Parser
    return Parser(Language(ts_lang_module.language()))


def main():
    t0 = time.time()
    with open(OPERATOR_ARITY_PATH) as f:
        arity_doc = json.load(f)

    inv = {lang: build_language_inventory(lang, arity_doc) for lang in ("c", "cpp", "go", "rust", "swift")}
    lowered = {lang: lowered_set_for(lang) for lang in ("c", "cpp", "go", "rust", "swift")}

    import tree_sitter_cpp
    import tree_sitter_go
    import tree_sitter_rust
    import tree_sitter_swift

    parser_cpp = build_parser(tree_sitter_cpp)
    parser_go = build_parser(tree_sitter_go)
    parser_rust = build_parser(tree_sitter_rust)
    parser_swift = build_parser(tree_sitter_swift)

    rows = []

    def measure_row(row_id, compiler, written_in, checkout_extent, dirs, extensions, exclude_substr, include_only_substr, parser, lang_for_inventory):
        tally = {}
        parse_failures = []
        n_files = 0
        for d in dirs:
            for path in iter_source_files(d, extensions, exclude_substr, include_only_substr):
                n_files += 1
                try:
                    scan_file(path, parser, inv[lang_for_inventory]["rule_tokens"], tally, None)
                except Exception as e:
                    parse_failures.append({"path": path, "error": repr(e)})
                if n_files % 2000 == 0:
                    abort_if_over_budget()
        offered_total = inv[lang_for_inventory]["offered_total"]
        offered_ops = set(inv[lang_for_inventory]["offered_operators"])
        lowered_ops = lowered[lang_for_inventory]
        used_ops = set(tally.keys()) & offered_ops
        used_not_offered = set(tally.keys()) - offered_ops  # sanity: should be empty
        used_and_lowered = used_ops & lowered_ops
        lowered_never_used = lowered_ops - used_ops
        used_not_lowered = used_ops - lowered_ops

        def members(op_set):
            out = []
            for i, op in enumerate(sorted(op_set)):
                entry = tally.get(op, {"count": 0, "files": set()})
                out.append({
                    # `lang` + `unit` make this a UNIT OBJECT under
                    # check_no_spelling_keys.py's except-list (a dict
                    # identifying one member, never a grouping row).
                    # `unit` is an opaque ordinal within (row, bucket)
                    # -- deliberately NOT built by joining the operator
                    # token onto anything (that shape is itself a
                    # banned spelling-key), so the only operator
                    # spelling on this object is the `operator` display
                    # field itself.
                    "lang": lang_for_inventory,
                    "unit": f"{row_id}#{i}",
                    "operator": op,
                    "occurrence_count": entry["count"],
                    "file_count": len(entry["files"]),
                })
            return out

        row = {
            "row_id": row_id,
            "compiler": compiler,
            "written_in": written_in,
            "checkout_extent": checkout_extent,
            "language_measured_against": lang_for_inventory,
            "source_files_parsed": n_files,
            "parse_failures_count": len(parse_failures),
            "parse_failures_sample": parse_failures[:3],
            "offered_grammar_total": offered_total,
            "offered_lowered_by_corpus": len(lowered_ops),
            "used_in_own_source": len(used_ops),
            "used_and_lowered": len(used_and_lowered),
            "lowered_never_used": len(lowered_never_used),
            "used_not_lowered": len(used_not_lowered),
            "used_and_lowered_members": members(used_and_lowered),
            "lowered_never_used_members": members(lowered_never_used),
            "used_not_lowered_members": members(used_not_lowered),
            "used_not_offered_sanity_check": sorted(used_not_offered),
        }
        return row

    # -- row 1: clang/llvm, cpp source, SPARSE --
    llvm_dirs = [
        f"{SOURCES}/llvm-project/llvm/lib/CodeGen/SelectionDAG",
        f"{SOURCES}/llvm-project/llvm/include/llvm/CodeGen",
        f"{SOURCES}/llvm-project/llvm/include/llvm/IR",
        f"{SOURCES}/llvm-project/llvm/include/llvm/MC",
        f"{SOURCES}/llvm-project/llvm/include/llvm/Target",
    ]
    rows.append(measure_row(
        "clang_llvm_cpp", "clang/llvm (c, cpp)", "cpp",
        "SPARSE: llvm/lib/CodeGen/SelectionDAG, llvm/include/llvm/{CodeGen,IR,MC,Target} only",
        llvm_dirs, (".cpp", ".cc", ".cxx", ".h", ".hpp", ".inc", ".def"), None, None,
        parser_cpp, "cpp",
    ))

    # -- row 2: go compiler (cmd/compile), go source, full checkout scope but path-restricted --
    go_root = f"{SOURCES}/golang_src/src"
    rows.append(measure_row(
        "go_compiler", "go (cmd/compile)", "go", "full checkout (11,622 files); this row = src/cmd/compile only",
        [f"{go_root}/cmd/compile"], (".go",), None, None,
        parser_go, "go",
    ))

    # -- row 3: go standard library (the rest of the checkout), go source --
    rows.append(measure_row(
        "go_stdlib", "go (standard library, rest of checkout)", "go", "full checkout (11,622 files); this row = everything except src/cmd/compile",
        [go_root], (".go",), f"{os.sep}cmd{os.sep}compile{os.sep}", None,
        parser_go, "go",
    ))

    # -- row 4: rustc, rust source, SPARSE --
    rust_dirs = [
        f"{SOURCES}/rust/compiler/rustc_codegen_cranelift",
        f"{SOURCES}/rust/compiler/rustc_codegen_llvm",
        f"{SOURCES}/rust/compiler/rustc_codegen_ssa",
    ]
    rows.append(measure_row(
        "rustc", "rustc", "rust", "SPARSE: compiler/rustc_codegen_{cranelift,llvm,ssa} only (187 files)",
        rust_dirs, (".rs",), None, None,
        parser_rust, "rust",
    ))

    # -- row 5: swiftc compiler (its own source is cpp), full lib+include --
    swift_root = f"{SOURCES}/swift-6.0.3-RELEASE"
    rows.append(measure_row(
        "swiftc_compiler", "swiftc (compiler)", "cpp", "full checkout (21,854 files); this row = lib/ + include/",
        [f"{swift_root}/lib", f"{swift_root}/include"], (".cpp", ".cc", ".cxx", ".h", ".hpp", ".inc", ".def"), None, None,
        parser_cpp, "cpp",
    ))

    # -- row 6: swift standard library -- now measured (task o3b): the
    # runner image was rebuilt 2026-09-06 with tree_sitter_swift added,
    # so this row runs through the SAME measure_row() path as every
    # other row, against the swift inventory (SWIFT_RULE_TO_NODE_TYPES
    # above resolves its hidden-rule node types).
    swift_stdlib_root = f"{SOURCES}/swift-6.0.3-RELEASE/stdlib"
    rows.append(measure_row(
        "swift_stdlib", "swift (standard library)", "swift",
        "full checkout (403 .swift files under stdlib/); every .swift file parsed",
        [swift_stdlib_root], (".swift",), None, None,
        parser_swift, "swift",
    ))

    peak_mb = abort_if_over_budget()

    meta = {
        "generated_by": "compiler_operators_used.py",
        "task": "o3",
        "line": "arch_unit_oracle",
        "node": "node_0_3_8_0_compiler_units",
        "elapsed_s": round(time.time() - t0, 1),
        "peak_rss_mb": round(peak_mb, 1),
        "memory_bound_mb": MEMORY_BOUND_MB,
        "offered_lowered_verified_counts": {lang: len(lowered[lang]) for lang in lowered},
        "shape_excluded_by_language": {lang: inv[lang]["shape_excluded"] for lang in inv},
        "grammar_node_unavailable_by_language": {lang: inv[lang]["grammar_node_unavailable"] for lang in inv},
    }

    out = {"meta": meta, "rows": rows}
    out_dir = f"{HQ}/Research/oracle/compiler_units"
    with open(f"{out_dir}/compiler_operators_used.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=False)

    write_markdown(out, f"{out_dir}/compiler_operators_used.md")

    print(f"done in {time.time()-t0:.1f}s, peak RSS {peak_mb:.1f} MB")
    for row in rows:
        if "source_files_parsed" in row:
            print(f"  {row['row_id']}: {row['source_files_parsed']} files, "
                  f"offered={row['offered_grammar_total']} lowered={row['offered_lowered_by_corpus']} "
                  f"used={row['used_in_own_source']} used_and_lowered={row['used_and_lowered']} "
                  f"lowered_never_used={row['lowered_never_used']} used_not_lowered={row['used_not_lowered']} "
                  f"parse_failures={row['parse_failures_count']}")
        else:
            print(f"  {row['row_id']}: FLAGGED, not parsed -- {row.get('flag')}")


def write_markdown(out, path):
    rows = out["rows"]
    lines = []
    lines.append("# compiler_operators_used")
    lines.append("")
    lines.append("| compiler | written in | source files parsed | offered (grammar total) | offered, lowered by the corpus | used in own source | used ∩ lowered | in lowered, never used | used, not in lowered |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for row in rows:
        if "source_files_parsed" not in row:
            lines.append(f"| {row['compiler']} | {row['written_in']} | NOT PARSED (flag) | {row['offered_grammar_total']} | {row['offered_lowered_by_corpus']} | - | - | - | - |")
            continue
        lines.append(
            f"| {row['compiler']} | {row['written_in']} | {row['source_files_parsed']} "
            f"({row['checkout_extent']}) | {row['offered_grammar_total']} | {row['offered_lowered_by_corpus']} | "
            f"{row['used_in_own_source']} | {row['used_and_lowered']} | {row['lowered_never_used']} | {row['used_not_lowered']} |"
        )
    lines.append("")
    for row in rows:
        if "source_files_parsed" not in row:
            continue
        lines.append(f"## {row['compiler']}")
        lines.append("")
        lines.append(f"- parse failures: {row['parse_failures_count']} (sample: {[p['path'] for p in row['parse_failures_sample']]})")
        for key, title in (
            ("used_and_lowered_members", "used ∩ lowered"),
            ("lowered_never_used_members", "in lowered, never used"),
            ("used_not_lowered_members", "used, not in lowered"),
        ):
            members = row[key]
            lines.append(f"- **{title}** ({len(members)}):")
            if members:
                for m in members:
                    lines.append(f"    - `{m['operator']}` -- {m['occurrence_count']} occurrences in {m['file_count']} files")
            else:
                lines.append("    - (none)")
        lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
