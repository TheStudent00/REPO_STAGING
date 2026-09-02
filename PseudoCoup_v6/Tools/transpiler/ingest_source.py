"""Run the four-stage ingress pipeline: parse -> census gate -> UR-AST -> ledger population.

The framework of the settled plan node
<WORKSPACE_DIR>/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_1_transpiler/SUPPORT_ingress.md.
An ingestor supplies ONLY: a grammar name, a node table (tree-sitter
kind -> build rule), a justified census baseline, and optionally a
type resolver. It cannot construct parsers, invent keys, or write
the ledger outside this framework — the historical bare-name
violation is structurally impossible here.

Stages:
  1. parse            — T1 (<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/tree_sitter/)
  2. census + GATE    — T1 recorder; leftover kinds REFUSE ingestion
  3. UR-AST build     — the ingestor's node table, ids threaded in
  4. ledger populate  — T2 (<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/),
                        semantic.type resolved or left "unresolvable"
"""
import os
import sys

_TOOLS = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
for _t in (os.path.join("ledgerer", "tree_sitter"), "ledgerer"):
    p = os.path.join(_TOOLS, _t)
    if p not in sys.path:
        sys.path.insert(0, p)

from parse_source import parse_file                    # noqa: E402
from record_coverage import census, partition          # noqa: E402
import build_ledger as ledger_mod                      # noqa: E402


class GateFailure(Exception):
    """Census gate refused ingestion: unhandled node kinds (the worklist)."""
    def __init__(self, leftover, file):
        self.leftover = sorted(leftover)
        super().__init__(
            f"ingress gate: {len(self.leftover)} unhandled node kind(s) in "
            f"{file}: {self.leftover}")


class Ingestor:
    """The specialization contract — a per-language ingestor IS this data.

    node_table: {tree-sitter kind: build_fn(builder, ts_node, ledger_id)
                 -> URNode | None}. None = the kind is structural
                 scaffolding consumed by a higher build rule.
    baseline:   {kind: one-line justification} — kinds deliberately
                not built (trivia), each justified.
    resolve_type(ts_node) -> str | None — optional; None leaves the
                 declaration marked "unresolvable" (T2 semantics).
    """
    grammar: str = None
    node_table: dict = {}
    baseline: dict = {}

    def resolve_type(self, node):
        return None


class Builder:
    """Passed to build rules so they can recurse without touching id math."""
    def __init__(self, ingestor):
        self.ing = ingestor
        self._segs = {}   # id bookkeeping filled by the walk

    def build(self, ts_node):
        """Build the UR node for a tree-sitter node via the node table."""
        fn = self.ing.node_table.get(ts_node.type)
        if fn is None:
            raise GateFailure({ts_node.type}, "<during build>")
        ur = fn(self, ts_node, self._segs.get(id(ts_node)))
        if ur is not None:
            ur.metadata["ledger_id"] = self._segs.get(id(ts_node))
        return ur

    def build_named_sub_nodes(self, ts_node):
        """Build every named sub-node that the table maps to a real UR node."""
        out = []
        for c in ts_node.named_children:  # tree-sitter's API name
            ur = self.build(c)
            if ur is not None:
                out.append(ur)
        return out

    def text(self, ts_node):
        return ts_node.text.decode("utf-8", "replace")


def ingest_file(path, ingestor, rel_name=None):
    """-> {"module": ModuleNode, "ledger": dict, "census": dict,
           "partition": dict}. Raises GateFailure on unhandled kinds."""
    rel = rel_name or os.path.basename(path)

    # stage 1: parse
    tree = parse_file(path, ingestor.grammar)
    root = tree.root_node

    # stage 2: census + gate (named kinds; anonymous nodes are
    # positions, not build targets)
    c = census(root)
    part = partition(set(c["named"]),
                     handled=set(ingestor.node_table),
                     baseline=set(ingestor.baseline))
    if part["leftover"]:
        raise GateFailure(part["leftover"], rel)

    # stage 3+4 share one walk so UR nodes and ledger records carry
    # THE SAME ids by construction (T2 keying: never two id maths)
    builder = Builder(ingestor)
    seg_of = builder._segs

    def assign(node, segs):
        seg_of[id(node)] = "/".join(segs)
        for i, ch in enumerate(node.children):
            assign(ch, segs + [f"{i}:{ch.type}"])

    assign(root, ["0:source_file"])

    module = builder.build(root)

    # stage 4: T2 ledger for this file, then overlay resolved types
    led = ledger_mod.build(os.path.dirname(path) or ".",
                           [(os.path.basename(path), ingestor.grammar)])
    decl = ledger_mod.DECLARATION_KINDS.get(ingestor.grammar, set())
    by_id = {}

    def collect(node):
        by_id[seg_of[id(node)]] = node
        for ch in node.named_children:
            collect(ch)
    collect(root)

    resolved = 0
    for rec in led["records"]:
        if rec["node_kind"] in decl:
            ts = by_id.get(rec["id"])
            t = ingestor.resolve_type(ts) if ts is not None else None
            if t is not None:
                rec["semantic"]["type"] = t
                resolved += 1
    led["meta"]["resolved_types"] = resolved

    return {"module": module, "ledger": led, "census": c,
            "partition": part}
