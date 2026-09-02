#!/usr/bin/env python3
"""query_hypothesis.py -- path query over graph_cpp_probe.json, plus one
sub-block refinement the whole-function emit counts cannot give.

Function-level emit_count (in graph_cpp_probe.json) is honest but coarse:
ExpandNode and ExpandLegalINT_TO_FP are big multi-case functions covering
many src/dst type combinations, not just ours. This script re-locates,
inside ExpandLegalINT_TO_FP's already-extracted body, the ONE `if` block
that actually fires for (unsigned, SrcVT in {i32,i64}, DstVT==f32) --
the exact case op_117 hits -- and counts emits INSIDE JUST THAT BLOCK.
That sub-block count is the number that should be compared to op_501's
single-pattern count, not the whole-function number.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import tree_sitter_cpp
from tree_sitter import Language, Parser

CPP_LANG = Language(tree_sitter_cpp.language())
HERE = Path(__file__).resolve().parent
SRC_DIR = Path("/tmp/probe_src")

EMIT_CALL_PREFIXES = (
    "DAG.getNode", "DAG.getSetCC", "DAG.getSelect", "DAG.getSelectCC",
    "DAG.getConstant", "DAG.getConstantFP", "DAG.getShiftAmountConstant",
    "DAG.getLoad", "DAG.getStore", "DAG.getBitcast", "DAG.getMemIntrinsicNode",
)


def extract_calls(parser, body_text):
    tree = parser.parse(body_text.encode("utf-8"))
    calls = []

    def callee_text(node):
        fn = node.child_by_field_name("function")
        return body_text[fn.start_byte:fn.end_byte] if fn else ""

    def first_arg_text(node):
        args = node.child_by_field_name("arguments")
        if not args or args.named_child_count == 0:
            return ""
        a0 = args.named_children[0]
        return body_text[a0.start_byte:a0.end_byte]

    def walk(node):
        if node.type == "call_expression":
            calls.append({"callee": callee_text(node), "first_arg": first_arg_text(node),
                          "line": node.start_point[0] + 1})
        for c in node.children:
            walk(c)

    walk(tree.root_node)
    return calls


def main():
    graph = json.loads((HERE / "graph_cpp_probe.json").read_text())
    print("=== PINS ===")
    print(json.dumps(graph["pins"], indent=2))

    print()
    print("=== PATH QUERY: unsigned i64 -> f32 (op_117's case) ===")
    print("X86TargetLowering::LowerOperation")
    print("  --[calls, forced-by-construction: switch case ISD::UINT_TO_FP]-->")
    print("X86TargetLowering::LowerUINT_TO_FP")
    print("  --[declines_custom_lowering, guard: is64Bit && SrcVT==i64 &&")
    print("     (DstVT==f32||DstVT==f64) -> return SDValue()]-->")
    print("SelectionDAGLegalize::LegalizeOp")
    print("  --[calls: case TargetLowering::Custom, TLI.LowerOperation")
    print("     returned null -> [[fallthrough]] to case Expand]-->")
    print("SelectionDAGLegalize::ExpandNode")
    print("  --[calls: case ISD::UINT_TO_FP, TLI.expandUINT_TO_FP(...)]-->")
    print("TargetLowering::expandUINT_TO_FP")
    print("  --[declines: early return false, DstVT.getScalarType() != f64]-->")
    print("  (back in ExpandNode, expandUINT_TO_FP returned false)")
    print("  --[[fallthrough]] case ISD::SINT_TO_FP: ExpandLegalINT_TO_FP(...)]-->")
    print("SelectionDAGLegalize::ExpandLegalINT_TO_FP")

    # --- sub-block refinement ---
    body_full = "".join(
        Path(SRC_DIR / "LegalizeDAG.cpp").read_text().splitlines(keepends=True)
    )
    func_start_m = re.search(
        r"^SDValue SelectionDAGLegalize::ExpandLegalINT_TO_FP\(", body_full, re.MULTILINE
    )
    # locate the specific unsigned-expansion if-block by its opening condition
    block_start_m = re.search(
        r"if \(\(\(SrcVT == MVT::i32 \|\| SrcVT == MVT::i64\) && DestVT == MVT::f32\)",
        body_full,
    )
    assert func_start_m and block_start_m
    # walk braces from the first '{' after block_start_m to find the block end
    i = body_full.index("{", block_start_m.start())
    depth = 0
    j = i
    while True:
        if body_full[j] == "{":
            depth += 1
        elif body_full[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    sub_block_text = body_full[i:j + 1]
    start_line = body_full[:block_start_m.start()].count("\n") + 1
    end_line = body_full[:j].count("\n") + 1

    parser = Parser(CPP_LANG)
    calls = extract_calls(parser, sub_block_text)
    emit_calls = [c for c in calls if c["callee"].startswith(EMIT_CALL_PREFIXES)]

    print()
    print(f"=== SUB-BLOCK: the specific unsigned-i64/i32->f32/f64 branch ===")
    print(f"LegalizeDAG.cpp lines {start_line}-{end_line} "
          f"(inside ExpandLegalINT_TO_FP, {end_line - start_line + 1} source lines)")
    print(f"emit_count (SDNode-constructing calls) in this block, ALL sub-branches"
          f" (strict + non-strict) combined: {len(emit_calls)}")
    for c in emit_calls:
        print(f"    {c['callee']}({c['first_arg']!r})  [relative source line offset {c['line']}]")
    has_branch = any("Select" in c["callee"] or "SetCC" in c["callee"] for c in emit_calls)
    print(f"contains a guard/select (branch-shaped) node: {has_branch}")

    # refine: op_117 (a+b, ordinary float add) is NOT strictfp, so the
    # `if (Node->isStrictFPOpcode())` sub-branch never executes for our
    # probed instance. Split the emits by which side of that guard they
    # sit on (found by the literal source text, not re-parsed) so the
    # AS-RUN emit count for op_117's own compile is a separate, sharper
    # number from the whole-block combined count above.
    strict_if_pos = sub_block_text.index("if (Node->isStrictFPOpcode())")
    strict_else_pos = sub_block_text.index("} else {", strict_if_pos)
    strict_else_end = sub_block_text.index("\n    }\n", strict_else_pos) + len("\n    }\n")

    def offset_of(call):
        # call['line'] is 1-based line within sub_block_text
        lines = sub_block_text.splitlines(keepends=True)
        return sum(len(l) for l in lines[:call["line"] - 1])

    shared_prefix = [c for c in emit_calls if offset_of(c) < strict_if_pos]
    strict_only = [c for c in emit_calls if strict_if_pos <= offset_of(c) < strict_else_pos]
    non_strict_only = [c for c in emit_calls if strict_else_pos <= offset_of(c) < strict_else_end]
    shared_suffix = [c for c in emit_calls if offset_of(c) >= strict_else_end]

    as_run_for_op_117 = shared_prefix + non_strict_only + shared_suffix
    print()
    print(f"as-run emit count for op_117's actual instance (non-strict, "
          f"i64->f32, drops the {len(strict_only)} strict-only emits "
          f"{[c['callee'] for c in strict_only]}): {len(as_run_for_op_117)}")
    for c in as_run_for_op_117:
        print(f"    {c['callee']}({c['first_arg']!r})")

    print()
    print("=== PATH QUERY: signed i32 -> float (op_501's case) ===")
    print("ISD::any_sint_to_fp(GR32:$src)")
    print("  --[isel_pattern_match, TableGen Pat, X86InstrSSE.td]-->")
    print("defm CVTSI2SS : sse12_cvt_s<0x2A, GR32, FR32, any_sint_to_fp, ...>")
    for n in graph["nodes"]:
        if n["kind"] == "tablegen_defm":
            print(f"  file={n['file']}  defm_line={n['defm_line']}  "
                  f"multiclass_line={n['multiclass_line']}  emit_count={n['emit_count']}")
            print(f"  pattern: {n['pattern_text']}")
            print(f"  defm text: {n['defm_text']}")

    print()
    print("=== VERDICT INPUTS (no interpretation, just the two numbers) ===")
    print(f"unsigned i64->f32 sub-block emit_count = {len(emit_calls)}  (branch present: {has_branch})")
    td_node = next(n for n in graph["nodes"] if n["kind"] == "tablegen_defm")
    print(f"signed   i32->f32 pattern emit_count   = {td_node['emit_count']}  (branch present: False)")


if __name__ == "__main__":
    main()
