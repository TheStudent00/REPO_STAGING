#!/usr/bin/env python3
"""go_types_join.py -- task o6, arch_unit_oracle line, compiler_units node.

WHAT THIS IS, in relation: the join between task o4's search-only
operator sites in go's compiler source (operator_variants_by_search.py,
go_compiler row) and the go/types oracle's sites over the same files
(go_types_oracle.go -> go_types_sites.json), by POSITION -- (file,
start line, start column, end line, end column) of the operator node --
never by the operator token. It writes go_types_join.json and
go_types_report.md.

THE O4 SIDE IS RE-WALKED, NOT READ (stated up front, per protocol §5.4):
o4's json carries only AGGREGATES for the go compiler row -- 1,050
variant counts, one histogram, nine excerpt sites -- and no per-site
record at all (54 `site` strings in the whole 4.2 MB file, all
excerpts). A join by position needs one record per site, so this
script imports o4's own module unchanged (operator_variants_by_search:
its parser, rule tokens, lowered set, scope collectors, operand
finder, resolver, and describe()) and re-runs o4's per-file walk over
the same 734 files, recording per site what o4's counters summed:
position, operator label, per-operand resolution. The re-walk is GATED:
its four totals (sites / fully resolved / partly resolved / unresolved)
must equal o4's json row exactly, else this script stops with a named
refusal -- so the o4 side of every table below is o4's own walk, not a
re-implementation of it.

THE SPELLING BAN: no operator token keys anything here. The join key is
a position tuple. Variants are accumulated (as o4 did, log_210 §1) into
per-unit objects carrying `operator` as a display label and each
operand's type spelling on its own per-unit label object; "oracle-only"
sites are tallied by label as a census (the same shape task o3's tally
takes), never paired by it. check_no_spelling_keys.py runs over both
json files in its own lane and its output is pasted in the log.

MEMORY: bound 3 GB (ABORT_MEMORY_O6, resource.getrusage), checked after
each of the three phases (load oracle json, re-walk o4, join). The
oracle json (go_types_sites.json.gz, gzip because ~200k one-line site
records sit near GitHub's 100 MB file limit uncompressed and the
artifact folder is auto-committed) is read as a STREAM, one json line
per record, never as one document; what stays resident is the site
index (one record per site) that the position join needs. o4's re-walk
holds one file's tree at a time, as o4's own scan does.

THE TWO SHAPES OF THE ORACLE RUN (resume, 2026-09-06): go_types_oracle.go
-shape tree (one importer cache for the whole run; the deliverable
sites file) and -shape package (a fresh cache per package check; sites
to scratch, cost record kept as go_types_package_shape_cost.json). The
cost section below reports both when the second file is present.
"""
import collections
import json
import os
import re
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import operator_variants_by_search as o4  # noqa: E402  -- reuse, not fork
from compiler_operators_used import (  # noqa: E402
    OPERATOR_ARITY_PATH, SOURCES, build_language_inventory, lowered_set_for,
    build_parser, iter_source_files,
)

MEMORY_BOUND_MB = 3072  # ABORT_MEMORY_O6
ORACLE_JSON = f"{HERE}/go_types_sites.json.gz"
PACKAGE_SHAPE_COST_JSON = f"{HERE}/go_types_package_shape_cost.json"
O4_JSON = f"{HERE}/operator_variants_by_search.json"
OUT_JSON = f"{HERE}/go_types_join.json"
OUT_MD = f"{HERE}/go_types_report.md"
GO_COMPILER_DIR = f"{SOURCES}/golang_src/src/cmd/compile"


def abort_if_over_budget(phase):
    peak_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    if peak_mb > MEMORY_BOUND_MB:
        print(f"ABORT_MEMORY_O6: peak RSS {peak_mb:.1f} MB > {MEMORY_BOUND_MB} MB bound after {phase}", file=sys.stderr)
        sys.exit(97)
    print(f"  [{phase}] peak RSS so far {peak_mb:.1f} MB")
    return peak_mb


# ---------------------------------------------------------------------------
# 0. the oracle file, streamed: one json line per record, section by
#    section (the go program writes exactly this line shape)
# ---------------------------------------------------------------------------

def iter_oracle(path):
    """Yields (section, record) for section in meta / packages / files / sites."""
    import gzip
    opener = gzip.open if path.endswith(".gz") else open
    section = None
    with opener(path, "rt") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith('"meta": '):
                yield "meta", json.loads(line[len('"meta": '):].rstrip(","))
            elif line in ('"packages": [', '"files": [', '"sites": ['):
                section = line[1:line.index('"', 1)]
            elif line in ("],", "]", "{", "}"):
                continue
            elif section is not None:
                yield section, json.loads(line.rstrip(","))


def load_oracle(path):
    meta = None
    packages, files, sites = [], [], []
    for section, rec in iter_oracle(path):
        if section == "meta":
            meta = rec
        elif section == "packages":
            packages.append(rec)
        elif section == "files":
            files.append(rec)
        else:
            sites.append(rec)
    return {"meta": meta, "packages": packages, "files": files, "sites": sites}


# ---------------------------------------------------------------------------
# 1. o4's walk, re-run per site (mirrors scan_file_for_variants.walk;
#    every decision is o4's own function)
# ---------------------------------------------------------------------------

def o4_sites_for_file(path, parser, rule_tokens, lowered_ops, lang="go"):
    with open(path, "rb") as f:
        src = f.read()
    tree = parser.parse(src)
    root = tree.root_node
    enc = o4.enclosing_stacks(root, lang)
    func_scopes, class_scopes, global_scope = o4.COLLECTORS[lang](root, src, lang)

    def scopes_for(node_id):
        fid, cid = enc.get(node_id, (None, None))
        chain = []
        if fid is not None and fid in func_scopes:
            chain.append(func_scopes[fid])
        if cid is not None and cid in class_scopes:
            chain.append(class_scopes[cid])
        chain.append(global_scope)
        return chain

    sites = []

    def walk(node):
        rule = node.type
        toks = rule_tokens.get(rule)
        if toks:
            op = o4.get_operator_text(node, toks, src)
            if op is not None and op in toks and op in lowered_ops:
                operands = o4.operand_nodes(node, lang)
                results = []
                for opnd in operands:
                    scopes = scopes_for(node.id)
                    res, extra = o4.unwrap_and_resolve(opnd, src, lang, scopes, path)
                    results.append((res, extra))
                resolved = [r for r, _ in results if r is not None]
                unresolved = [(r, e) for r, e in results if r is None]
                spellings = [o4.describe(r) if r is not None else None for r, _ in results]
                if not operands:
                    status = "unresolved"
                    reason = f"{o4.R.OTHER} (no operand node found for {rule})"
                elif len(operands) == 1:
                    if resolved:
                        status, reason = "full", None
                    else:
                        status, reason = "unresolved", unresolved[0][1]
                else:
                    if len(resolved) == 2:
                        status, reason = "full", None
                    elif len(resolved) == 1:
                        status, reason = "partial", unresolved[0][1]
                    else:
                        status, reason = "unresolved", unresolved[0][1]
                sites.append({
                    "file": path,
                    "line": node.start_point[0] + 1, "col": node.start_point[1] + 1,
                    "end_line": node.end_point[0] + 1, "end_col": node.end_point[1] + 1,
                    "rule": rule, "op": op, "status": status, "reason": reason,
                    "spellings": spellings,
                })
        for c in node.children:
            walk(c)

    walk(root)
    del tree
    del src
    return sites


def rewalk_o4(o4_row):
    with open(OPERATOR_ARITY_PATH) as f:
        arity_doc = json.load(f)
    inv = build_language_inventory("go", arity_doc)
    lowered = lowered_set_for("go")
    import tree_sitter_go
    parser = build_parser(tree_sitter_go)
    all_sites = []
    n_files = 0
    for path in iter_source_files(GO_COMPILER_DIR, (".go",), None, None):
        n_files += 1
        all_sites.extend(o4_sites_for_file(path, parser, inv["rule_tokens"], lowered))
    counts = collections.Counter(s["status"] for s in all_sites)
    got = (n_files, len(all_sites), counts["full"], counts["partial"], counts["unresolved"])
    want = (o4_row["source_files_parsed"], o4_row["sites_lowered_operators"], o4_row["sites_fully_resolved"],
            o4_row["sites_partly_resolved"], o4_row["sites_unresolved"])
    print(f"  o4 re-walk: files={got[0]} sites={got[1]} full={got[2]} partial={got[3]} unresolved={got[4]}")
    print(f"  o4 json row: files={want[0]} sites={want[1]} full={want[2]} partial={want[3]} unresolved={want[4]}")
    if got != want:
        print("REFUSE: the re-walk does not reproduce o4's own row totals; the o4 side would not be o4's walk", file=sys.stderr)
        sys.exit(96)
    print("  GATE PASSED: re-walk totals equal o4's json row")
    return all_sites, sorted(lowered), inv["rule_tokens"]


# ---------------------------------------------------------------------------
# 2. classification helpers (strings in, cause names out; the recorded
#    spellings are never altered)
# ---------------------------------------------------------------------------

GO_INTEGER_SPELLINGS = {"int", "int8", "int16", "int32", "int64", "uint", "uint8", "uint16", "uint32",
                        "uint64", "uintptr", "byte", "rune", "untyped int", "untyped rune"}
GO_FLOAT_SPELLINGS = {"float32", "float64", "untyped float", "complex64", "complex128", "untyped complex"}
ALIAS_PAIRS = {("byte", "uint8"), ("rune", "int32")}


def strip_qualifiers(s):
    # classification only: drop `path/to/pkg.` and `pkg.` before an identifier
    return re.sub(r"(?:[\w\-.]+/)*[\w\-.]+\.(?=[A-Za-z_])", "", s)


def expand_grouped_params(s):
    """classification only: `func(x, y any) any` -> `func(x any, y any) any`
    (go/types prints every parameter with its own type; o4 kept the
    grouped form as written). One level of parentheses."""
    def fix(m):
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(",")]
        out = []
        pending = []
        for p in parts:
            toks = p.split(" ", 1)
            if len(toks) == 1:
                pending.append(toks[0])
            else:
                name, typ = toks
                for q in pending:
                    out.append(f"{q} {typ}")
                pending = []
                out.append(f"{name} {typ}")
        if pending:
            out.extend(pending)
        return "(" + ", ".join(out) + ")"
    return re.sub(r"\(([^()]*)\)", fix, s)


def same_type_printed_differently(o4_sp, or_sp):
    a = re.sub(r"\s+", "", expand_grouped_params(strip_qualifiers(o4_sp)))
    b = re.sub(r"\s+", "", expand_grouped_params(strip_qualifiers(or_sp)))
    return a == b


UNTYPED_BOOL = "untyped bool (go's type for a comparison's result and for a bool constant)"
UNTYPED_NUMERIC = "untyped numeric constant (untyped int / float / rune / complex: a constant expression not yet given a type)"
UNTYPED_STRING = "untyped string constant"
UNTYPED_NIL = "untyped nil"
UNTYPED_CAUSES = (UNTYPED_BOOL, UNTYPED_NUMERIC, UNTYPED_STRING, UNTYPED_NIL)
CAUSE_ORDER = ["no type recorded by go/types", "invalid type (go/types reported an error at this expression)",
               "type parameter (generics)", UNTYPED_NIL, UNTYPED_STRING, UNTYPED_NUMERIC, UNTYPED_BOOL]


def untyped_cause(sp):
    if sp == "untyped bool":
        return UNTYPED_BOOL
    if sp == "untyped string":
        return UNTYPED_STRING
    if sp == "untyped nil":
        return UNTYPED_NIL
    return UNTYPED_NUMERIC


def oracle_operand_cause(label, untyped_is_typed=False):
    """One cause name for an oracle operand that is not a concrete type.
    untyped_is_typed=True: go's `untyped ...` spellings count as types
    (the spelling is kept as printed), so only empty / invalid / type
    parameter remain causes."""
    sp = label["spelling"]
    if sp == "":
        return "no type recorded by go/types"
    if sp == "invalid type":
        return "invalid type (go/types reported an error at this expression)"
    if label.get("type_param"):
        return "type parameter (generics)"
    if sp.startswith("untyped ") and not untyped_is_typed:
        return untyped_cause(sp)
    return None


def disagreement_cause(o4_sp, or_label):
    or_sp = or_label["spelling"]
    if or_sp == "":
        return "oracle: no type recorded"
    if or_sp == "invalid type":
        return "oracle: invalid type"
    if or_sp.startswith("untyped "):
        return "oracle: untyped spelling where o4 wrote the default type (a nested comparison is `untyped bool` to go/types; o4 wrote `bool`)"
    if strip_qualifiers(or_sp) == strip_qualifiers(o4_sp):
        return "package qualification only (same name)"
    if same_type_printed_differently(o4_sp, or_sp):
        return "same type, printed differently (go/types prints every parameter with its own type and qualifies every name)"
    if (o4_sp, or_sp) in ALIAS_PAIRS or (strip_qualifiers(o4_sp), strip_qualifiers(or_sp)) in ALIAS_PAIRS:
        return "alias spelling (byte/rune written; go/types prints uint8/int32)"
    if strip_qualifiers(or_sp).replace("*", "") == strip_qualifiers(o4_sp).replace("*", ""):
        return "pointer-ness differs (same base name)"
    return "different type (o4's same-file search read another declaration of the same name -- a shadowing binding, or a type-switch case where go/types gives the case's type)"


def literal_kind_class(or_sp):
    if or_sp == "":
        return "no type recorded"
    if or_sp in GO_INTEGER_SPELLINGS:
        return "integer basic"
    if or_sp in GO_FLOAT_SPELLINGS:
        return "float/complex basic"
    if or_sp in ("string", "untyped string"):
        return "string basic"
    if or_sp in ("bool", "untyped bool"):
        return "bool basic"
    if or_sp.startswith("untyped "):
        return "other untyped"
    return "named or composite type"


# ---------------------------------------------------------------------------
# 3. main
# ---------------------------------------------------------------------------

def unit(lang, uid, **fields):
    d = {"lang": lang, "unit": uid}
    d.update(fields)
    return d


def main():
    t0 = time.time()
    with open(O4_JSON) as f:
        o4_doc = json.load(f)
    o4_row = [r for r in o4_doc["rows"] if r["row_id"] == "go_compiler"][0]
    core = {c["spelling"] for c in json.load(open(o4.TYPE_INVENTORY_CORE_PATH))["languages"]["go"]["scalar_core"]}

    oracle = load_oracle(ORACLE_JSON)
    abort_if_over_budget("load oracle json (streamed)")
    package_shape = None
    if os.path.exists(PACKAGE_SHAPE_COST_JSON):
        with open(PACKAGE_SHAPE_COST_JSON) as f:
            package_shape = json.load(f)
    o_sites = oracle["sites"]
    o_files = {fr["file"]: fr for fr in oracle["files"]}

    o4_sites, lowered_sorted, rule_tokens = rewalk_o4(o4_row)
    abort_if_over_budget("o4 re-walk")

    key = lambda s: (s["file"], s["line"], s["col"], s["end_line"], s["end_col"])
    o4_by = collections.defaultdict(list)
    for s in o4_sites:
        o4_by[key(s)].append(s)
    or_by = collections.defaultdict(list)
    for s in o_sites:
        or_by[key(s)].append(s)
    dup_o4 = sum(1 for v in o4_by.values() if len(v) > 1)
    dup_or = sum(1 for v in or_by.values() if len(v) > 1)

    both_keys = [k for k in o4_by if k in or_by]
    o4_only_keys = [k for k in o4_by if k not in or_by]
    or_only_keys = [k for k in or_by if k not in o4_by]
    n_both = sum(min(len(o4_by[k]), len(or_by[k])) for k in both_keys)
    n_o4_only = sum(len(o4_by[k]) for k in o4_only_keys) + sum(len(o4_by[k]) - min(len(o4_by[k]), len(or_by[k])) for k in both_keys)
    n_or_only = sum(len(or_by[k]) for k in or_only_keys) + sum(len(or_by[k]) - min(len(o4_by[k]), len(or_by[k])) for k in both_keys)

    # --- o4-only causes ---
    or_starts = collections.defaultdict(list)
    for s in o_sites:
        or_starts[(s["file"], s["line"], s["col"])].append(s)
    o4_only_cause = collections.Counter()
    o4_only_samples = collections.defaultdict(list)
    for k in o4_only_keys:
        for s in o4_by[k]:
            if s["file"] not in o_files:
                cause = "file has no oracle record at all"
            elif (s["file"], s["line"], s["col"]) in or_starts:
                cause = "same start position, different node span"
            else:
                fr = o_files[s["file"]]
                if fr.get("syntax_error"):
                    cause = "file has a parse error under go/parser (tree-sitter parsed it; no go/ast node here)"
                else:
                    cause = "no oracle node starts here (tree-sitter node with no go/ast operator counterpart)"
            o4_only_cause[cause] += 1
            if len(o4_only_samples[cause]) < 5:
                o4_only_samples[cause].append(s)

    # --- oracle-only causes (a census by label, o3's shape) ---
    lowered = set(lowered_sorted)
    or_only_cause = collections.Counter()
    or_only_label = collections.Counter()
    or_only_samples = collections.defaultdict(list)
    for k in or_only_keys:
        for s in or_by[k]:
            if s["operator"] not in lowered:
                cause = "operator label not in o4's lowered set (o4 never counted these)"
            else:
                cause = f"label in o4's lowered set but no o4 site at this span ({s['kind']})"
            or_only_cause[cause] += 1
            or_only_label[(cause, s["operator"], s["kind"])] += 1
            if len(or_only_samples[cause]) < 5:
                or_only_samples[cause].append(s)

    # --- agreement over joined sites ---
    label_mismatch = 0
    label_mismatch_samples = []
    agree = 0
    disagree = collections.Counter()      # cause -> n
    disagree_pairs = collections.Counter()  # (o4 spelling, oracle spelling, cause) -> n
    disagree_sample = {}
    literal_table = collections.Counter()  # (o4 literal kind, oracle class) -> n
    joined_pairs = []  # (o4 site, oracle site)
    for k in both_keys:
        for s4, so in zip(o4_by[k], or_by[k]):
            joined_pairs.append((s4, so))
            if s4["op"] != so["operator"]:
                label_mismatch += 1
                if len(label_mismatch_samples) < 5:
                    label_mismatch_samples.append((s4, so))
            for i, sp4 in enumerate(s4["spellings"]):
                if sp4 is None or i >= len(so["operands"]):
                    continue
                lab = so["operands"][i]
                if sp4.endswith(" literal") or " literal (" in sp4:
                    literal_table[(sp4, literal_kind_class(lab["spelling"]))] += 1
                    continue
                if sp4 == lab["spelling"]:
                    agree += 1
                else:
                    cause = disagreement_cause(sp4, lab)
                    disagree[cause] += 1
                    disagree_pairs[(sp4, lab["spelling"], cause)] += 1
                    disagree_sample.setdefault((sp4, lab["spelling"], cause), (s4, so))
    abort_if_over_budget("join")

    # --- the completed row: every o4 site, typed by the oracle ---
    joined_o4_ids = set(id(s4) for s4, _ in joined_pairs)
    variant_counter = collections.Counter()
    variant_sample = {}
    remainder = collections.Counter()
    n_resolved_by_oracle = 0
    for s4 in o4_sites:
        if id(s4) not in joined_o4_ids:
            remainder["not joined (o4-only site)"] += 1
            continue
    untyped_variant_counter = collections.Counter()
    untyped_variant_sample = {}
    untyped_remainder = collections.Counter()
    n_resolved_untyped_inclusive = 0
    untyped_spelling_census = collections.Counter()
    for s4, so in joined_pairs:
        causes = [oracle_operand_cause(l) for l in so["operands"]]
        causes = [c for c in causes if c]
        spell = tuple(l["spelling"] for l in so["operands"])
        # the untyped-inclusive reading (go's `untyped ...` spellings kept as types)
        causes_u = [c for c in (oracle_operand_cause(l, untyped_is_typed=True) for l in so["operands"]) if c]
        if causes_u:
            causes_u.sort(key=lambda c: CAUSE_ORDER.index(c))
            untyped_remainder[causes_u[0]] += 1
        else:
            n_resolved_untyped_inclusive += 1
            if any(sp.startswith("untyped ") for sp in spell):
                untyped_variant_counter[(so["operator"], spell)] += 1
                untyped_variant_sample.setdefault((so["operator"], spell), so)
                for sp in spell:
                    if sp.startswith("untyped "):
                        untyped_spelling_census[sp] += 1
        if causes:
            causes.sort(key=lambda c: CAUSE_ORDER.index(c))
            remainder[causes[0]] += 1
            continue
        n_resolved_by_oracle += 1
        vk = (so["operator"], spell)
        variant_counter[vk] += 1
        variant_sample.setdefault(vk, so)
    variants = []
    both_in_core = 0
    for i, ((op, spell), n) in enumerate(sorted(variant_counter.items(), key=lambda kv: (-kv[1], kv[0][1]))):
        uid = f"go_types_join#var{i}"
        roles = ["lhs", "rhs"] if len(spell) == 2 else ["operand"]
        in_core = all(sp in core for sp in spell)
        both_in_core += in_core
        variants.append(unit("go", uid, operator=op,
                             operands=[{"lang": "go", "unit": f"{uid}#{r}", "role": r, "spelling": sp} for r, sp in zip(roles, spell)],
                             sites=n, both_in_core_type_inventory=in_core,
                             example_site=f"{variant_sample[(op, spell)]['file']}:{variant_sample[(op, spell)]['line']}:{variant_sample[(op, spell)]['col']}"))
    untyped_variants = []
    for i, ((op, spell), n) in enumerate(sorted(untyped_variant_counter.items(), key=lambda kv: (-kv[1], kv[0][1]))):
        uid = f"go_types_join#uvar{i}"
        roles = ["lhs", "rhs"] if len(spell) == 2 else ["operand"]
        untyped_variants.append(unit("go", uid, operator=op,
                                     operands=[{"lang": "go", "unit": f"{uid}#{r}", "role": r, "spelling": sp} for r, sp in zip(roles, spell)],
                                     sites=n, example_site=f"{untyped_variant_sample[(op, spell)]['file']}:{untyped_variant_sample[(op, spell)]['line']}:{untyped_variant_sample[(op, spell)]['col']}"))
    # the same row over ALL oracle sites (o4's operator set widened to every go operator node)
    all_counter = collections.Counter()
    all_resolved = 0
    all_remainder = collections.Counter()
    all_resolved_u = 0
    all_counter_u = collections.Counter()
    for so in o_sites:
        spell = tuple(l["spelling"] for l in so["operands"])
        causes_u = [c for c in (oracle_operand_cause(l, untyped_is_typed=True) for l in so["operands"]) if c]
        if not causes_u:
            all_resolved_u += 1
            all_counter_u[(so["operator"], spell)] += 1
        causes = [oracle_operand_cause(l) for l in so["operands"]]
        causes = [c for c in causes if c]
        if causes:
            causes.sort(key=lambda c: CAUSE_ORDER.index(c))
            all_remainder[causes[0]] += 1
            continue
        all_resolved += 1
        all_counter[(so["operator"], spell)] += 1
    all_in_core = sum(1 for (op, spell) in all_counter if all(sp in core for sp in spell))
    all_in_core_u = sum(1 for (op, spell) in all_counter_u if all(sp in core for sp in spell))

    # --- cost ---
    pk = oracle["packages"]
    cost_rows = sorted(pk, key=lambda p: -p["wall_s"])
    bins = collections.Counter(p["bin"] for p in pk)
    bin_sites = collections.Counter()
    bin_typed = collections.Counter()
    bin_errors = collections.Counter()
    bin_typeskip = collections.Counter()
    for p in pk:
        bin_sites[p["bin"]] += p["sites"]
        bin_typed[p["bin"]] += p["sites_all_operands_typed"]
        bin_errors[p["bin"]] += p["errors"]
        bin_typeskip[p["bin"]] += p.get("type_expression_nodes_skipped", 0)
    err_causes = collections.Counter()
    for p in pk:
        for c, n in p["error_causes"].items():
            err_causes[c] += n
    pkgs_with_errors = [p for p in pk if p["errors"] > 0]
    shapes = [unit("go", "go_types_join#shape0", shape=oracle["meta"]["shape"], total_wall_s=oracle["meta"]["elapsed_s"],
                   peak_rss_mb=oracle["meta"]["peak_rss_mb"], packages=len(pk), sites=oracle["meta"]["sites"],
                   sites_all_operands_typed=oracle["meta"]["sites_all_operands_typed"], sites_file="go_types_sites.json.gz (the deliverable)")]
    pkg_wall = {}
    if package_shape:
        pm = package_shape["meta"]
        shapes.append(unit("go", "go_types_join#shape1", shape=pm["shape"], total_wall_s=pm["elapsed_s"], peak_rss_mb=pm["peak_rss_mb"],
                           packages=len(package_shape["packages"]), sites=pm["sites"], sites_all_operands_typed=pm["sites_all_operands_typed"],
                           sites_file="scratch (/work of the o6 instance; the lane log compares its site lines to the deliverable's)"))
        pkg_wall = {p["import_path"] + "|" + p["bin"]: p for p in package_shape["packages"]}

    peak = abort_if_over_budget("done")
    result = {
        "meta": {
            "generated_by": "go_types_join.py", "task": "o6", "line": "arch_unit_oracle",
            "node": "node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_1_variants_by_search",
            "oracle_json": ORACLE_JSON, "o4_json": O4_JSON,
            "package_shape_cost_json": PACKAGE_SHAPE_COST_JSON if package_shape else None,
            "join_key": "(file, start line, start col, end line, end col) of the operator node; tree-sitter points +1 to match go/token 1-based byte columns",
            "o4_side": "re-walk through operator_variants_by_search's own functions, gated equal to the json row totals (see gate)",
            "o4_gate": {"files": o4_row["source_files_parsed"], "sites": o4_row["sites_lowered_operators"],
                        "full": o4_row["sites_fully_resolved"], "partial": o4_row["sites_partly_resolved"],
                        "unresolved": o4_row["sites_unresolved"], "passed": True},
            "o4_lowered_set_labels": lowered_sorted,
            "o4_rule_tokens_go": rule_tokens,
            "core_type_inventory": sorted(core),
            "oracle_meta": oracle["meta"],
            "elapsed_s": round(time.time() - t0, 1), "peak_rss_mb": round(peak, 1), "memory_bound_mb": MEMORY_BOUND_MB,
        },
        "join_counts": {
            "o4_sites": len(o4_sites), "oracle_sites": len(o_sites), "both": n_both,
            "o4_only": n_o4_only, "oracle_only": n_or_only,
            "duplicate_position_keys_o4": dup_o4, "duplicate_position_keys_oracle": dup_or,
            "joined_label_mismatch": label_mismatch,
        },
        "o4_only_causes": [unit("go", f"go_types_join#o4only{i}", reason=c, sites=n,
                                samples=[f"{s['file']}:{s['line']}:{s['col']}-{s['end_line']}:{s['end_col']} ({s['rule']})" for s in o4_only_samples[c]])
                           for i, (c, n) in enumerate(o4_only_cause.most_common())],
        "oracle_only_causes": [unit("go", f"go_types_join#oronly{i}", reason=c, sites=n,
                                    samples=[f"{s['file']}:{s['line']}:{s['col']} ({s['kind']})" for s in or_only_samples[c]])
                               for i, (c, n) in enumerate(or_only_cause.most_common())],
        "oracle_only_by_label": [unit("go", f"go_types_join#orlabel{i}", reason=c, operator=op, kind=kind, sites=n)
                                 for i, ((c, op, kind), n) in enumerate(or_only_label.most_common())],
        "agreement": {
            "o4_typed_operands_agree_exactly": agree,
            "o4_typed_operands_disagree": sum(disagree.values()),
            "disagreement_by_cause": [unit("go", f"go_types_join#dcause{i}", reason=c, operands=n) for i, (c, n) in enumerate(disagree.most_common())],
            "literal_kind_vs_oracle_class": [unit("go", f"go_types_join#lit{i}", o4_literal_kind=k, oracle_class=cls, operands=n)
                                             for i, ((k, cls), n) in enumerate(literal_table.most_common())],
            "label_mismatch_samples": [f"{s4['file']}:{s4['line']}:{s4['col']} tree-sitter rule {s4['rule']} vs go/ast {so['kind']}" for s4, so in label_mismatch_samples],
        },
        "disagreements": [unit("go", f"go_types_join#dis{i}", reason=c, operands=n,
                               o4={"lang": "go", "unit": f"go_types_join#dis{i}#o4", "role": "o4 written type", "spelling": a},
                               oracle={"lang": "go", "unit": f"go_types_join#dis{i}#oracle", "role": "go/types", "spelling": b},
                               example_site=f"{disagree_sample[(a, b, c)][1]['file']}:{disagree_sample[(a, b, c)][1]['line']}:{disagree_sample[(a, b, c)][1]['col']}")
                          for i, ((a, b, c), n) in enumerate(disagree_pairs.most_common())],
        "completed_row": {
            "population": f"o4's go (cmd/compile) sites, {o4_row['sites_lowered_operators']}, each typed by the oracle where joined",
            "sites": len(o4_sites),
            "o4_by_search": {"sites_fully_resolved": o4_row["sites_fully_resolved"],
                             "distinct_variants": o4_row["distinct_variants_resolved"],
                             "variants_both_in_core": o4_row["variants_both_in_core"]},
            "oracle": {"sites_resolved": n_resolved_by_oracle, "distinct_variants": len(variants),
                       "variants_both_in_core": both_in_core},
            "oracle_untyped_spellings_counted_as_types": {
                "reading": "go's `untyped bool` / `untyped int` / ... spellings kept as the operand's type, as printed",
                "sites_resolved": n_resolved_untyped_inclusive,
                "distinct_variants": len(variant_counter) + len(untyped_variant_counter),
                "variants_both_in_core": both_in_core,
                "variants_with_an_untyped_operand": len(untyped_variant_counter),
                "sites_with_an_untyped_operand": sum(untyped_variant_counter.values()),
                "untyped_spelling_census": [unit("go", f"go_types_join#usp{i}", spelling=sp, operands=n) for i, (sp, n) in enumerate(untyped_spelling_census.most_common())],
                "remainder_by_cause": [unit("go", f"go_types_join#urem{i}", reason=c, sites=n) for i, (c, n) in enumerate(untyped_remainder.most_common())],
            },
            "remainder_by_cause": [unit("go", f"go_types_join#rem{i}", reason=c, sites=n) for i, (c, n) in enumerate(remainder.most_common())],
            "all_oracle_sites_row": {"sites": len(o_sites), "sites_resolved": all_resolved, "distinct_variants": len(all_counter),
                                     "variants_both_in_core": all_in_core,
                                     "sites_resolved_untyped_counted_as_types": all_resolved_u,
                                     "distinct_variants_untyped_counted_as_types": len(all_counter_u),
                                     "variants_both_in_core_untyped_counted_as_types": all_in_core_u,
                                     "remainder_by_cause": [unit("go", f"go_types_join#arem{i}", reason=c, sites=n) for i, (c, n) in enumerate(all_remainder.most_common())]},
        },
        "variants": variants,
        "variants_with_an_untyped_operand": untyped_variants,
        "cost": {
            "total_wall_s": oracle["meta"]["elapsed_s"], "peak_rss_mb": oracle["meta"]["peak_rss_mb"],
            "packages": len(pk), "files": oracle["meta"]["files"],
            "shapes": shapes,
            "by_bin": [unit("go", f"go_types_join#bin{i}", bin=b, packages=n, sites=bin_sites[b], sites_all_operands_typed=bin_typed[b], errors=bin_errors[b],
                            type_expression_nodes_skipped=bin_typeskip[b])
                       for i, (b, n) in enumerate(bins.most_common())],
            "error_causes": [unit("go", f"go_types_join#err{i}", reason=c, errors=n) for i, (c, n) in enumerate(err_causes.most_common())],
            "packages_with_errors": [unit("go", f"go_types_join#perr{i}", import_path=p["import_path"], bin=p["bin"], errors=p["errors"],
                                          error_causes=p["error_causes"], error_samples=p["error_samples"])
                                     for i, p in enumerate(sorted(pkgs_with_errors, key=lambda p: -p["errors"]))],
            "per_package": [unit("go", f"go_types_join#cost{i}", import_path=p["import_path"], bin=p["bin"], files=p["files"],
                                 wall_s=p["wall_s"], maxrss_mb_after=p["maxrss_mb_after"], sites=p["sites"],
                                 sites_all_operands_typed=p["sites_all_operands_typed"], errors=p["errors"],
                                 package_shape_wall_s=pkg_wall.get(p["import_path"] + "|" + p["bin"], {}).get("wall_s"),
                                 package_shape_maxrss_mb_after=pkg_wall.get(p["import_path"] + "|" + p["bin"], {}).get("maxrss_mb_after"))
                            for i, p in enumerate(cost_rows)],
        },
    }
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=1)
    write_md(result)
    print(f"done in {time.time()-t0:.1f}s, peak RSS {peak:.1f} MB")
    jc = result["join_counts"]
    print(f"join: o4={jc['o4_sites']} oracle={jc['oracle_sites']} both={jc['both']} o4_only={jc['o4_only']} oracle_only={jc['oracle_only']}")
    cr = result["completed_row"]
    print(f"completed row: sites={cr['sites']} oracle_resolved={cr['oracle']['sites_resolved']} variants={cr['oracle']['distinct_variants']} both_in_core={cr['oracle']['variants_both_in_core']}")
    print(f"o4 row:        sites={cr['sites']} search_resolved={cr['o4_by_search']['sites_fully_resolved']} variants={cr['o4_by_search']['distinct_variants']} both_in_core={cr['o4_by_search']['variants_both_in_core']}")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def write_md(r):
    L = []
    m = r["meta"]
    om = m["oracle_meta"]
    jc = r["join_counts"]
    cr = r["completed_row"]
    L.append("# go/types over the go compiler's source, joined to task o4's sites -- task o6")
    L.append("")
    L.append("Generated by `go_types_join.py` from `go_types_sites.json.gz` (go_types_oracle.go) and o4's re-walk. "
             f"GOROOT used by the oracle: `{om['goroot_used']}`; overlay (generated files the checked-in tree lacks, read from the image's GOROOT copy): "
             f"{', '.join('`' + o + '`' for o in om['overlay']) or 'none'}; shape: {om['shape']}; toolchain: {om['go_toolchain']}; cgo enabled: {om['cgo_enabled']}; "
             f"release tags through `{om['release_tags'][-1]}`.")
    L.append("")
    L.append("## 1. Typing, by bin and by cause")
    L.append("")
    L.append(md_table(["file bin", "packages checked", "sites", "sites with every operand typed", "go/types errors", "BinaryExpr/UnaryExpr nodes that are type expressions (constraint unions, `~T`), skipped"],
                      [(b["bin"], b["packages"], b["sites"], b["sites_all_operands_typed"], b["errors"], b["type_expression_nodes_skipped"]) for b in r["cost"]["by_bin"]]))
    L.append("")
    L.append(md_table(["error cause (classified from the go/types message)", "errors"], [(e["reason"], e["errors"]) for e in r["cost"]["error_causes"]]))
    L.append("")
    L.append("Packages with at least one error, with the first literal messages:")
    L.append("")
    L.append(md_table(["package (bin)", "errors", "causes", "first messages (LITERAL, go/types)"],
                      [(f"`{p['import_path']}` ({p['bin']})", p["errors"], "; ".join(f"{c} {n}" for c, n in p["error_causes"].items()),
                        "<br>".join(f"`{s}`" for s in p["error_samples"][:3])) for p in r["cost"]["packages_with_errors"]]))
    L.append("")
    L.append("## 2. The join, by position")
    L.append("")
    L.append(f"Key: {m['join_key']}. o4 side: {m['o4_side']}; gate {m['o4_gate']}.")
    L.append("")
    L.append(md_table(["sites in o4", "sites go/types typed", "both", "o4-only", "go/types-only", "joined sites whose two labels differ"],
                      [(jc["o4_sites"], jc["oracle_sites"], jc["both"], jc["o4_only"], jc["oracle_only"], jc["joined_label_mismatch"])]))
    L.append("")
    L.append("o4-only, by cause (a finding about o4's walk):")
    L.append("")
    L.append(md_table(["cause", "sites", "samples"], [(c["reason"], c["sites"], "<br>".join(f"`{s}`" for s in c["samples"])) for c in r["o4_only_causes"]]))
    L.append("")
    L.append("go/types-only, by cause (a finding about o4's operator set):")
    L.append("")
    L.append(md_table(["cause", "sites", "samples"], [(c["reason"], c["sites"], "<br>".join(f"`{s}`" for s in c["samples"])) for c in r["oracle_only_causes"]]))
    L.append("")
    L.append(md_table(["cause", "operator (label)", "go/ast node", "sites"], [(c["reason"], f"`{c['operator']}`", c["kind"], c["sites"]) for c in r["oracle_only_by_label"]]))
    L.append("")
    L.append("## 3. Agreement where o4 resolved an operand")
    L.append("")
    ag = r["agreement"]
    L.append(md_table(["o4 typed operands that equal the oracle's spelling exactly", "that differ"],
                      [(ag["o4_typed_operands_agree_exactly"], ag["o4_typed_operands_disagree"])]))
    L.append("")
    L.append(md_table(["disagreement cause", "operands"], [(c["reason"], c["operands"]) for c in ag["disagreement_by_cause"]]))
    L.append("")
    L.append("Every distinct disagreement, LITERAL, both spellings (o4's written type as its search read it | go/types' TypeString), with one site each:")
    L.append("")
    L.append(md_table(["o4 spelling", "go/types spelling", "cause", "operands", "example site"],
                      [(f"`{d['o4']['spelling']}`", f"`{d['oracle']['spelling']}`" if d['oracle']['spelling'] else "(empty)", d["reason"], d["operands"], f"`{d['example_site']}`") for d in r["disagreements"]]))
    L.append("")
    L.append("o4's literal KINDS against the oracle's type class at the same operand (a kind is not a type; this is the consistency census):")
    L.append("")
    L.append(md_table(["o4 literal kind", "go/types class", "operands"], [(c["o4_literal_kind"], c["oracle_class"], c["operands"]) for c in ag["literal_kind_vs_oracle_class"]]))
    L.append("")
    L.append("## 4. The completed row: variants used by the go compiler")
    L.append("")
    cu = cr["oracle_untyped_spellings_counted_as_types"]
    ar = cr["all_oracle_sites_row"]
    L.append(md_table(["row", "sites", "sites resolved", "distinct variants", "variants with every operand in go's core inventory"],
                      [("o4, by search alone (log_210)", cr["sites"], cr["o4_by_search"]["sites_fully_resolved"], cr["o4_by_search"]["distinct_variants"], cr["o4_by_search"]["variants_both_in_core"]),
                       ("o4's sites, typed by go/types, every operand a concrete type (this task)", cr["sites"], cr["oracle"]["sites_resolved"], cr["oracle"]["distinct_variants"], cr["oracle"]["variants_both_in_core"]),
                       ("o4's sites, typed by go/types, go's `untyped ...` spellings counted as types (this task, second reading)", cr["sites"], cu["sites_resolved"], cu["distinct_variants"], cu["variants_both_in_core"]),
                       ("every go/types operator site (o4's operator set widened), concrete types", ar["sites"], ar["sites_resolved"], ar["distinct_variants"], ar["variants_both_in_core"]),
                       ("every go/types operator site, untyped spellings counted as types", ar["sites"], ar["sites_resolved_untyped_counted_as_types"], ar["distinct_variants_untyped_counted_as_types"], ar["variants_both_in_core_untyped_counted_as_types"])]))
    L.append("")
    L.append("The second reading, in numbers: " + f"{cu['sites_with_an_untyped_operand']} of o4's joined sites carry an `untyped ...` operand spelling, in {cu['variants_with_an_untyped_operand']} variants; the spellings, by operand:")
    L.append("")
    L.append(md_table(["go/types spelling", "operands"], [(f"`{u['spelling']}`", u["operands"]) for u in cu["untyped_spelling_census"]]))
    L.append("")
    L.append("Remainder under the second reading, by cause:")
    L.append("")
    L.append(md_table(["cause", "sites"], [(c["reason"], c["sites"]) for c in cu["remainder_by_cause"]]))
    L.append("")
    L.append("Remainder of o4's sites the oracle could not type (first reading: every operand a concrete type), by cause:")
    L.append("")
    L.append(md_table(["cause", "sites"], [(c["reason"], c["sites"]) for c in cr["remainder_by_cause"]]))
    L.append("")
    L.append("Remainder over every go/types site, by cause:")
    L.append("")
    L.append(md_table(["cause", "sites"], [(c["reason"], c["sites"]) for c in cr["all_oracle_sites_row"]["remainder_by_cause"]]))
    L.append("")
    L.append("## 5. The variant table, full (operator label | lhs type | rhs type | sites), sorted by sites")
    L.append("")
    rows = []
    for v in r["variants"]:
        ops = v["operands"]
        lhs = ops[0]["spelling"]
        rhs = ops[1]["spelling"] if len(ops) == 2 else "-"
        rows.append((f"`{v['operator']}`", f"`{lhs}`", f"`{rhs}`" if rhs != "-" else "-", v["sites"], "yes" if v["both_in_core_type_inventory"] else "no"))
    L.append(md_table(["operator", "lhs type", "rhs type", "sites", "both in core"], rows))
    L.append("")
    L.append("## 5b. The variants with an `untyped ...` operand (the second reading's additions), full, sorted by sites")
    L.append("")
    rows = []
    for v in r["variants_with_an_untyped_operand"]:
        ops = v["operands"]
        lhs = ops[0]["spelling"]
        rhs = ops[1]["spelling"] if len(ops) == 2 else "-"
        rows.append((f"`{v['operator']}`", f"`{lhs}`", f"`{rhs}`" if rhs != "-" else "-", v["sites"], f"`{v['example_site']}`"))
    L.append(md_table(["operator", "lhs type", "rhs type", "sites", "example site"], rows))
    L.append("")
    L.append("## 6. Cost")
    L.append("")
    c = r["cost"]
    L.append(f"Total wall clock of the go program: {c['total_wall_s']} s; peak RSS {c['peak_rss_mb']} MB; {c['packages']} package checks over {c['files']} files. "
             "Per-package wall clock includes the first-time import of every dependency that package pulled into the shared importer cache; "
             "maxrss is the process's running peak after that package.")
    L.append("")
    L.append("The two shapes of the same run (tree: one importer cache for the whole run; package: a fresh cache per package check, GC + FreeOSMemory after each):")
    L.append("")
    L.append(md_table(["shape", "total wall s", "peak RSS MB", "package checks", "sites", "sites with every operand typed", "sites file"],
                      [(sh["shape"], sh["total_wall_s"], sh["peak_rss_mb"], sh["packages"], sh["sites"], sh["sites_all_operands_typed"], sh["sites_file"]) for sh in c["shapes"]]))
    L.append("")
    L.append(md_table(["package", "bin", "files", "wall s (tree)", "maxrss MB after (tree)", "wall s (package shape)", "maxrss MB after (package shape)", "sites", "all operands typed", "errors"],
                      [(f"`{p['import_path']}`", p["bin"], p["files"], p["wall_s"], p["maxrss_mb_after"],
                        p["package_shape_wall_s"] if p["package_shape_wall_s"] is not None else "-",
                        p["package_shape_maxrss_mb_after"] if p["package_shape_maxrss_mb_after"] is not None else "-",
                        p["sites"], p["sites_all_operands_typed"], p["errors"]) for p in c["per_package"]]))
    L.append("")
    L.append(f"Join script: {m['elapsed_s']} s, peak RSS {m['peak_rss_mb']} MB (bound {m['memory_bound_mb']} MB, ABORT_MEMORY_O6).")
    with open(OUT_MD, "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
