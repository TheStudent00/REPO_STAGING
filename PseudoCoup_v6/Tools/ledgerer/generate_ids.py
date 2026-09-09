"""Generate positional-path node ids over tree_sitter_base trees; unique by construction.

Provenance: transplanted 2026-07-28 from
~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py
(v0's id generator, verified green in place by R3). Kept exactly:
the segment rule "<childIndex>:<nodeKind>" recorded UNCONDITIONALLY
at every node (tree-sitter's own child order, named and anonymous
alike); anchors are metadata, never keys; files are positioned
nodes among their sorted co-nodes; check_uniqueness. Adapted for
PCv6 phase 1 (recorded in README.md): grammar-agnostic via T1;
records emitted for NAMED nodes only (anonymous nodes still consume
index positions); the corpus is an explicit pinned file list, not a
directory scan.
"""
import os
import sys

_T1 = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "ledgerer", "tree_sitter"))
if _T1 not in sys.path:
    sys.path.insert(0, _T1)

from parse_source import parse_file  # noqa: E402

# sub-node types whose text serves as a human-readable anchor
_ANCHOR_TYPES = ("identifier", "type_identifier", "field_identifier", "name")


class Record:
    __slots__ = ("id", "file", "node_kind", "span", "anchor")

    def __init__(self, id_, file_, node):
        self.id = id_
        self.file = file_
        self.node_kind = node.type
        self.span = {
            "start_byte": node.start_byte, "end_byte": node.end_byte,
            "start_line": node.start_point[0] + 1,
            "start_col": node.start_point[1],
            "end_line": node.end_point[0] + 1,
            "end_col": node.end_point[1],
        }
        self.anchor = _anchor_of(node)

    def as_dict(self):
        return {"id": self.id, "file": self.file,
                "node_kind": self.node_kind, "span": dict(self.span),
                "anchor": self.anchor}


def _anchor_of(node):
    for c in node.children:  # .children: tree-sitter's API name
        if c.type in _ANCHOR_TYPES:
            try:
                return c.text.decode("utf-8", "replace")[:80]
            except Exception:
                return None
    return None


def walk_file(path, grammar, file_seg):
    """-> ([Record for every NAMED node], total_node_count).

    file_seg is this file's own positional segment in the corpus
    (e.g. "2:source_file") — the file is a positioned node, so ids
    are unique across the whole corpus, not just within one file.
    """
    tree = parse_file(path, grammar)
    records = []
    total = 0

    def walk(node, segs):
        nonlocal total
        total += 1
        if node.is_named:
            records.append(Record("/".join(segs), None, node))
        for i, c in enumerate(node.children):
            walk(c, segs + [f"{i}:{c.type}"])

    walk(tree.root_node, [file_seg])
    return records, total


def check_uniqueness(records):
    """-> (ok, total, distinct, dupes {id: [Record,...]}). Transplanted verbatim in spirit."""
    by_id = {}
    for r in records:
        by_id.setdefault(r.id, []).append(r)
    dupes = {k: v for k, v in by_id.items() if len(v) > 1}
    return (len(dupes) == 0), len(records), len(by_id), dupes
