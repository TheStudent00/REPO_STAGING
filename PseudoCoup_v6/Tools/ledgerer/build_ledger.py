"""Build the phase-1 ledger (one record per named source node) and serialize it deterministically.

Phase-1 record per the settled schema
(~/Programming/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_ur_ast.md):
id / file / node_kind / span / anchor / semantic.type — where a
declaration-kind node with no resolved type carries the EXPLICIT
value "unresolvable" (never a guess, never an omission), and
consumers halt on it (require_type). Later slots (ui, connectivity,
divergence, runtime) arrive with their writers per the growth gate.
"""
import json

from generate_ids import Record, check_uniqueness, walk_file

# phase-1 declaration kinds per grammar: nodes that MUST carry a
# type ("unresolvable" until an ingestor resolves them). Small on
# purpose; grows with the ingestors.
DECLARATION_KINDS = {
    "rust": {"function_item", "struct_item", "enum_item", "const_item",
             "static_item", "let_declaration"},
    "cpp": {"function_definition", "class_specifier", "struct_specifier",
            "declaration", "field_declaration"},
    "python": {"function_definition", "class_definition"},
}


class LedgerRefusal(Exception):
    """A consumer touched an entry the ledger cannot vouch for."""


def build(corpus_root, corpus):
    """corpus: [(relpath, grammar)] — pinned, ORDER-SIGNIFICANT
    (sorted by the caller once, then frozen; each file's index is
    its positional segment). -> ledger dict."""
    entries = []
    per_file_totals = {}
    for i, (rel, grammar) in enumerate(corpus):
        decl = DECLARATION_KINDS.get(grammar, set())
        records, total = walk_file(f"{corpus_root}/{rel}", grammar,
                                   f"{i}:source_file")
        per_file_totals[rel] = {"all_nodes": total, "named_records": len(records)}
        for r in records:
            d = r.as_dict()
            d["file"] = rel
            d["semantic"] = {
                "type": "unresolvable" if r.node_kind in decl else None}
            entries.append(d)
    entries.sort(key=lambda d: d["id"])
    return {
        "meta": {"corpus_root": "<supplied at build>", "corpus": [
            {"file": rel, "grammar": g} for rel, g in corpus],
            "per_file": per_file_totals,
            "entry_count": len(entries)},
        "records": entries,
    }


def dump(ledger, path):
    """Serialize deterministically (sorted keys, sorted records; byte-identical rebuilds)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ledger, indent=1, sort_keys=True) + "\n")


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def index_by_id(ledger):
    return {r["id"]: r for r in ledger["records"]}


def require_type(record):
    """Consumer gate: returns the resolved type or HALTS. Refusal at
    consumption (settled): 'unresolvable' is honest at ingest and
    fatal at use."""
    t = record["semantic"]["type"]
    if t == "unresolvable":
        raise LedgerRefusal(
            f"ledger refusal: {record['id']} ({record['node_kind']} in "
            f"{record['file']} line {record['span']['start_line']}) has no "
            f"resolved type — consumer must not proceed")
    return t
