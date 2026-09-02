#!/usr/bin/env python3
"""build_graph_cpp_probe.py -- BOUNDED probe graph, C++/TableGen region.

Not lap-two of the Go compiler graph. This is a single-measurement,
purpose-built graph over the exact handful of LLVM/clang source units
needed to answer one question: is a single-instruction case (signed
i32 -> float) structurally distinguishable, in the compiler's own
source graph, from a super-op case (unsigned i64 -> float)?

Scope decision (recorded, not hidden): build_graph.py (lap one) is
hardcoded to Go (tree_sitter_go, cmd/compile region rules). It was
NOT extended to a generic multi-language dispatcher -- that is the
CORE node's still-open item 3 ("second language"). Building that
properly (SelectionDAG legalization + X86 ISel patterns, whole
region) is a campaign, not a bounded probe. This script instead
applies the SAME node/edge shape (declarations, call edges, emit
sites) to the SMALL set of functions the grep-based location step
found, dispatched by file extension per the node's own rule:
  .cpp -> tree-sitter-cpp (parseable code region)
  .td  -> a data-table reader (per CORE_0_3_5 sec 4: ".td/.rules/.ad
          are not code; each node is a PAIR: the table parsed as
          data + its consuming loop already in the parseable region")
No tree-sitter-tablegen binding exists on PyPI (checked, absent) --
named dead end for a general .td parser; the data-table reader here
is a regex reader scoped to the one multiclass instantiation needed.

Pins:
  tree-sitter     == 0.26.0  (matches lap-one Go graph's pin)
  tree-sitter-cpp == 0.23.4  (first use on this line; no prior pin
                              existed to match -- recorded here)
  LLVM/clang tree commit == 42befb84c672d78de430feb4c96710e6aa4fc774
    (tag llvmorg-21.1.8, tagged 2026-08-05 per llvm-project's own
    tag; source dated 2025-12-12 per `git log -1` on that tag)
    -- this is the PINNED release the op_pipeline's c/cpp lanes
    actually run (Ubuntu clang version 21.1.8, confirmed from
    Research/op_pipeline/lane_out_ordering/compiler.txt). The
    llvm-project checkout's *current HEAD* is llvmorg-24-init
    (commit 6a33b69d8bae, 2026-07-17) -- NOT what shipped op_117 /
    op_501. Files were extracted at the correct tag with
    `git show llvmorg-21.1.8:<path>` rather than read off the
    working tree, so the region analyzed matches the pinned
    compiler. This mismatch (repo HEAD vs. pinned tag) is itself
    a finding -- see the probe's .md report.

Region (5 C++ functions + 1 TableGen defm; hand-located by grep,
not yet by a general graph walk -- see report for what a next probe
would need to remove this human-location step):
  X86TargetLowering::LowerUINT_TO_FP        (X86ISelLowering.cpp)
  X86TargetLowering::LowerOperation          (X86ISelLowering.cpp, dispatch only)
  SelectionDAGLegalize::LegalizeOp           (LegalizeDAG.cpp)
  SelectionDAGLegalize::ExpandNode           (LegalizeDAG.cpp)
  TargetLowering::expandUINT_TO_FP           (TargetLowering.cpp)
  SelectionDAGLegalize::ExpandLegalINT_TO_FP (LegalizeDAG.cpp)
  defm CVTSI2SS : sse12_cvt_s<...>           (X86InstrSSE.td, data)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from importlib.metadata import version as _pkg_version
except ImportError:  # pragma: no cover
    _pkg_version = None

import tree_sitter_cpp
from tree_sitter import Language, Parser

CPP_LANG = Language(tree_sitter_cpp.language())

SRC_DIR = Path("/tmp/probe_src")
OUT_DIR = Path(__file__).resolve().parent

LLVM_TAG = "llvmorg-21.1.8"
LLVM_COMMIT = "42befb84c672d78de430feb4c96710e6aa4fc774"
LLVM_HEAD_COMMIT_MISMATCH = "6a33b69d8bae737e5e1d60c7b7776a0b1f885bfa"  # llvmorg-24-init, repo's checked-out HEAD

# ------------------------------------------------------------- targets ----

# (file, qualified_name, is_definition_line_regex)
TARGET_FUNCS = [
    ("X86ISelLowering.cpp", "X86TargetLowering::LowerUINT_TO_FP",
     r"^SDValue X86TargetLowering::LowerUINT_TO_FP\("),
    ("X86ISelLowering.cpp", "X86TargetLowering::LowerOperation",
     r"^SDValue X86TargetLowering::LowerOperation\("),
    ("LegalizeDAG.cpp", "SelectionDAGLegalize::LegalizeOp",
     r"^void SelectionDAGLegalize::LegalizeOp\("),
    ("LegalizeDAG.cpp", "SelectionDAGLegalize::ExpandNode",
     r"^bool SelectionDAGLegalize::ExpandNode\("),
    ("TargetLowering.cpp", "TargetLowering::expandUINT_TO_FP",
     r"^bool TargetLowering::expandUINT_TO_FP\("),
    ("LegalizeDAG.cpp", "SelectionDAGLegalize::ExpandLegalINT_TO_FP",
     r"^SDValue SelectionDAGLegalize::ExpandLegalINT_TO_FP\("),
]

# DAG-node-construction call prefixes: each one of these calls
# constructs one SDNode, which is legalization/isel's unit of
# "an operation on the graph" -- the nearest machine-independent
# analogue of "an emit". Recorded as data, not asserted by kind.
EMIT_CALL_PREFIXES = (
    "DAG.getNode", "DAG.getSetCC", "DAG.getSelect", "DAG.getSelectCC",
    "DAG.getConstant", "DAG.getConstantFP", "DAG.getShiftAmountConstant",
    "DAG.getLoad", "DAG.getStore", "DAG.getBitcast", "DAG.getMemIntrinsicNode",
)

# calls from one target function into another target function: recorded
# as "calls" edges. TLI.LowerOperation / TLI.expandUINT_TO_FP are virtual
# / plain calls respectively; their resolution to a specific target
# function is justified per-edge in EDGE_JUSTIFICATION below, forced by
# construction from X86TargetLowering::LowerOperation's own switch (a
# node in this same graph), not by assumption.
CALL_TARGET_MAP = {
    "ExpandNode": "SelectionDAGLegalize::ExpandNode",
    "TLI.expandUINT_TO_FP": "TargetLowering::expandUINT_TO_FP",
    "ExpandLegalINT_TO_FP": "SelectionDAGLegalize::ExpandLegalINT_TO_FP",
    "TLI.LowerOperation": "X86TargetLowering::LowerOperation",
    "LowerUINT_TO_FP": "X86TargetLowering::LowerUINT_TO_FP",
}


def find_function_span(src_lines: list[str], pattern: str) -> tuple[int, int]:
    """Return (start_line_1based, end_line_1based) of a top-level
    function definition matched by its signature-start regex, ending
    at the matching closing brace at column 0."""
    rx = re.compile(pattern)
    start = None
    for i, line in enumerate(src_lines):
        if rx.match(line):
            start = i
            break
    if start is None:
        raise SystemExit(f"FRONTIER: pattern not found: {pattern}")
    depth = 0
    seen_open = False
    for j in range(start, len(src_lines)):
        depth += src_lines[j].count("{") - src_lines[j].count("}")
        if "{" in src_lines[j]:
            seen_open = True
        if seen_open and depth <= 0:
            return (start + 1, j + 1)
    raise SystemExit(f"FRONTIER: unterminated function body: {pattern}")


def extract_calls(parser: Parser, body_text: str) -> list[dict]:
    """Walk a C++ function body and list every call_expression's callee
    text plus, for DAG-node-construction calls, the first argument text
    (usually the ISD opcode) as machine-readable testimony of what the
    call constructs."""
    tree = parser.parse(body_text.encode("utf-8"))
    calls = []

    def callee_text(node) -> str:
        fn = node.child_by_field_name("function")
        return body_text[fn.start_byte:fn.end_byte] if fn else ""

    def first_arg_text(node) -> str:
        args = node.child_by_field_name("arguments")
        if not args or args.named_child_count == 0:
            return ""
        a0 = args.named_children[0]
        return body_text[a0.start_byte:a0.end_byte]

    def walk(node):
        if node.type == "call_expression":
            calls.append({
                "callee": callee_text(node),
                "first_arg": first_arg_text(node),
                "line": node.start_point[0] + 1,
            })
        for c in node.children:
            walk(c)

    walk(tree.root_node)
    return calls


def build():
    parser = Parser(CPP_LANG)

    nodes = {}
    edges = []

    file_cache = {}
    for fname, _qname, _pat in TARGET_FUNCS:
        if fname not in file_cache:
            file_cache[fname] = (SRC_DIR / fname).read_text().splitlines(keepends=True)

    for fname, qname, pat in TARGET_FUNCS:
        lines = file_cache[fname]
        start, end = find_function_span(lines, pat)
        body_text = "".join(lines[start - 1:end])
        calls = extract_calls(parser, body_text)

        emit_calls = [c for c in calls if c["callee"].startswith(EMIT_CALL_PREFIXES)]
        internal_calls = [c for c in calls
                           if any(c["callee"] == k or c["callee"].endswith("." + k.split(".")[-1])
                                  for k in CALL_TARGET_MAP)
                           and c["callee"] in CALL_TARGET_MAP]

        node_id = f"{fname}::{qname}"
        nodes[node_id] = {
            "id": node_id,
            "kind": "cpp_function",
            "language": "cpp",
            "file": fname,
            "qualified_name": qname,
            "start_line": start,
            "end_line": end,
            "emit_count": len(emit_calls),
            "emits": [
                {"opcode": c["first_arg"], "line": c["line"], "call": c["callee"]}
                for c in emit_calls
            ],
        }

        for c in internal_calls:
            target_qname = CALL_TARGET_MAP[c["callee"]]
            target_file = next(f for f, q, _ in TARGET_FUNCS if q == target_qname)
            edges.append({
                "from": node_id,
                "to": f"{target_file}::{target_qname}",
                "kind": "calls",
                "at_line": c["line"],
                "callee_text": c["callee"],
            })

    # the one non-call, semantically load-bearing edge: LowerUINT_TO_FP's
    # decline for (i64 -> f32) on 64-bit targets without AVX512. This is
    # a `return SDValue();` -- no call, so tree-sitter's call-expression
    # walk cannot find it as an edge; it is recorded as a DECLINE edge,
    # located by direct line match on the guarded return, kept separate
    # from the call-graph edges so the difference in HOW it was found is
    # visible (this is the weaker "grep-located" class, see report).
    x86_body = "".join(file_cache["X86ISelLowering.cpp"][
        nodes["X86ISelLowering.cpp::X86TargetLowering::LowerUINT_TO_FP"]["start_line"] - 1:
        nodes["X86ISelLowering.cpp::X86TargetLowering::LowerUINT_TO_FP"]["end_line"]
    ])
    decline_rx = re.compile(
        r"if \(Subtarget\.is64Bit\(\) && SrcVT == MVT::i64 &&\s*\n\s*"
        r"\(DstVT == MVT::f32 \|\| DstVT == MVT::f64\)\)\s*\n\s*return SDValue\(\);"
    )
    m = decline_rx.search(x86_body)
    edges.append({
        "from": "X86ISelLowering.cpp::X86TargetLowering::LowerUINT_TO_FP",
        "to": "LegalizeDAG.cpp::SelectionDAGLegalize::LegalizeOp",
        "kind": "declines_custom_lowering",
        "guard_matched_in_source": bool(m),
        "guard_text": ("Subtarget.is64Bit() && SrcVT == MVT::i64 && "
                       "(DstVT == MVT::f32 || DstVT == MVT::f64) -> return SDValue();"),
        "note": ("Custom-lowering hook returns null for (i64,f32) and "
                 "(i64,f64) on 64-bit non-AVX512 targets. LegalizeOp's "
                 "own source (case TargetLowering::Custom, this same "
                 "file) falls through to Expand when LowerOperation "
                 "returns null -- that fallthrough IS this edge."),
    })

    # TableGen data node: the single-pattern instruction-selection case.
    td_text = (SRC_DIR / "X86InstrSSE.td").read_text()
    multiclass_m = re.search(
        r"multiclass sse12_cvt_s<.*?\n(?:.*\n)*?^\}\n", td_text, re.MULTILINE
    )
    defm_m = re.search(
        r"defm CVTSI2SS  : sse12_cvt_s<0x2A, GR32, FR32, any_sint_to_fp,.*",
        td_text,
    )
    pattern_m = re.search(
        r"\[\(set DstRC:\$dst, \(OpNode SrcRC:\$src\)\)\]", multiclass_m.group(0)
    ) if multiclass_m else None

    td_node_id = "X86InstrSSE.td::CVTSI2SS(defm sse12_cvt_s)"
    nodes[td_node_id] = {
        "id": td_node_id,
        "kind": "tablegen_defm",
        "language": "tablegen_data",  # read by the custom data-table
                                       # reader below, per CORE sec 4:
                                       # ".td is not code; node is the
                                       # table entry, paired with its
                                       # consuming loop (TableGen's
                                       # -gen-dag-isel, off-tree, not
                                       # parsed here -- see report)
        "file": "X86InstrSSE.td",
        "defm_line": td_text[:defm_m.start()].count("\n") + 1 if defm_m else None,
        "multiclass_line": td_text[:multiclass_m.start()].count("\n") + 1 if multiclass_m else None,
        "emit_count": 1 if pattern_m else 0,
        "emits": ([{"opcode": "(any_sint_to_fp GR32:$src) -> CVTSI2SSrr",
                    "line": None, "call": "Pat"}] if pattern_m else []),
        "defm_text": defm_m.group(0) if defm_m else None,
        "pattern_text": pattern_m.group(0) if pattern_m else None,
    }

    # edge: the DAG node any_sint_to_fp(i32) reaches CVTSI2SSrr through
    # ISel pattern match -- not a call, a TABLE LOOKUP. Recorded as a
    # distinct edge kind so it is never confused with a C++ call edge.
    edges.append({
        "from": "ISD::any_sint_to_fp(GR32)",
        "to": td_node_id,
        "kind": "isel_pattern_match",
        "note": ("TableGen's -gen-dag-isel backend compiles this [(set "
                 "...)] Pat into the ISel matcher table at build time "
                 "(X86GenDAGISel.inc, generated, not checked into the "
                 "source tree -- FRONTIER: the generated matcher table "
                 "itself was not built or inspected in this probe; the "
                 "TableGen source pattern is the forced-by-construction "
                 "fact available without a build)."),
    })

    graph = {
        "pins": {
            "tree_sitter": _pkg_version("tree-sitter") if _pkg_version else "unknown",
            "tree_sitter_cpp": _pkg_version("tree-sitter-cpp") if _pkg_version else "unknown",
            "llvm_tag": LLVM_TAG,
            "llvm_commit": LLVM_COMMIT,
            "llvm_repo_head_commit_MISMATCH": LLVM_HEAD_COMMIT_MISMATCH,
            "pinned_compiler_per_op_pipeline": "Ubuntu clang version 21.1.8 (6ubuntu1)",
        },
        "nodes": list(nodes.values()),
        "edges": edges,
    }

    out_path = OUT_DIR / "graph_cpp_probe.json"
    out_path.write_text(json.dumps(graph, indent=2))
    sys.stderr.write(f"wrote {out_path} : {len(nodes)} nodes, {len(edges)} edges\n")
    return graph


if __name__ == "__main__":
    build()
