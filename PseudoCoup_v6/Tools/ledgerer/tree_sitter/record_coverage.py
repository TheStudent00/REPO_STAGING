"""Census a parse tree's node kinds and partition them totally into handled/baseline/leftover.

Provenance: recorder concept from
WFL_Projects/WFL_PseudoCoup/pseudocoup/ingress/coverage.py
(handled / justified-baseline buckets); total-partition strictness
from StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/
classify.py (leftover == the worklist, driven to zero). The census
is deterministic: same source, byte-identical rendering.
"""
import json
from collections import Counter


def census(root) -> dict:
    """Count every node kind in the tree, split named vs anonymous."""
    named, anon = Counter(), Counter()
    stack = [root]
    while stack:
        n = stack.pop()
        (named if n.is_named else anon)[n.type] += 1
        stack.extend(n.children)  # .children: tree-sitter's API name
    return {
        "named": {k: named[k] for k in sorted(named)},
        "anonymous": {k: anon[k] for k in sorted(anon)},
    }


def render_census(c: dict) -> str:
    """Render a census deterministically (byte-identical across runs)."""
    return json.dumps(c, indent=1, sort_keys=True) + "\n"


def partition(kinds, handled, baseline) -> dict:
    """Totally partition node kinds; anything neither handled nor
    baseline-justified is leftover — the worklist. handled and
    baseline must be disjoint (an overlap means a kind is claimed
    twice, which hides mistakes)."""
    kinds, handled, baseline = set(kinds), set(handled), set(baseline)
    overlap = handled & baseline
    if overlap:
        raise ValueError(
            f"coverage partition: kinds claimed both handled and "
            f"baseline: {sorted(overlap)}")
    part = {
        "handled": sorted(kinds & handled),
        "baseline": sorted(kinds & baseline),
        "leftover": sorted(kinds - handled - baseline),
    }
    total = len(part["handled"]) + len(part["baseline"]) + len(part["leftover"])
    assert total == len(kinds), "partition not total — recorder bug"
    return part
