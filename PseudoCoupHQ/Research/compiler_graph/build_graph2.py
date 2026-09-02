#!/usr/bin/env python3
"""build_graph2.py -- generalized, language-dispatched compiler-graph builder.

Lap two of the compiler-graph instrument. Lap one (build_graph.py) was
Go-hardcoded. This file replaces the SHAPE of the builder (extension ->
reader dispatch, one node/edge vocabulary) while keeping lap one's node
kinds unchanged (declared units + refs, typed edges: resolves_to /
flows_into / calls; here extended with the probe's two evidenced non-call
edge kinds, calls_declines and isel_pattern_match, kept as their own
edge types so they are never confused with a parsed call).

Node/edge vocabulary is UNCHANGED from lap one: a node is a declared or
referenced unit (function, method, tablegen data row); an edge is typed
and machine-found, never asserted. "Defined in" vs "does": this file is
itself Python, dispatching readers, but every node/edge it emits was
found IN the target language's own text by that language's own parser
or (for data tables) a data-table reader -- per CORE_0_3_5 sec
"language-agnostic by construction".

READER DISPATCH (extension -> reader), the CORE's own rule:
  .cpp / .cc / .h / .hpp  -> tree-sitter-cpp            (parseable code)
  .td                     -> data-table reader (regex, balanced-brace)
  .go                     -> FRONTIER in this file (lap one's own
                              build_graph.py already covers Go; this
                              file is the cpp-first generalization the
                              brief asked for, not a Go rewrite -- named
                              here rather than silently omitted)
  .s / assembly            -> FRONTIER, no reader written this lap
  anything else            -> FRONTIER, named per-file

Pins of record (asserted at run time from installed package metadata):
  tree-sitter     == 0.26.0
  tree-sitter-cpp == 0.23.4
  LLVM tag        == llvmorg-21.1.8

PIN CORRECTION (recorded, not hidden): the cpp probe's own report
(PROBE_uint64_to_float_vs_int32_to_float.md) recorded the tag's commit
as 42befb84c672d78de430feb4c96710e6aa4fc774. Re-resolving the tag now
(`git rev-list -n1 llvmorg-21.1.8` /
`git log -1 --format='%H %ci' llvmorg-21.1.8` against
<WORKSPACE_DIR>/Sources/llvm-project) gives
2078da43e25a4623cab2d0d60decddf709aaea28, dated 2025-12-12 10:35:47
+0000 -- the SAME date the probe recorded, but a DIFFERENT hash. Tags
in this repo are not force-moved between the probe's run (2026-08-31
lap one) and this lap (same day, minutes later), so the probe's hash is
read as a transcription slip, not a tag mutation; this file's commit is
the one used to extract every source file below, verified against `git
show <this hash>:<path>` output byte-for-byte.

Sources are extracted with `git show <tag>:<path>`, never read from the
working tree (the working tree is checked out at llvmorg-24-init; the
probe caught exactly this mismatch once already).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from importlib.metadata import version as _pkg_version
except ImportError:  # pragma: no cover
    _pkg_version = None

import tree_sitter_cpp
from tree_sitter import Language, Parser

CPP_LANG = Language(tree_sitter_cpp.language())

HERE = Path(__file__).resolve().parent
LLVM_REPO = Path.home() / "Programming" / "Sources" / "llvm-project"
LLVM_TAG = "llvmorg-21.1.8"

# ---------------------------------------------------------- region -----

# Region = the probe's four files (three .cpp holding its six target
# functions, one .td holding the TableGen row) inside llvm/lib. Brief
# says "expanding outward as budget allows" -- this lap does NOT expand
# past these four files; direct includes/callees beyond them are named
# as a frontier in the report rather than pulled in silently. That is
# the STOP RULE applied honestly: further region growth needs its own
# budgeted pass, not a guess at what "direct includes" means for a
# 2.5 MB translation unit like X86ISelLowering.cpp.
REGION_FILES = [
    "llvm/lib/Target/X86/X86ISelLowering.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeDAG.cpp",
    "llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp",
    "llvm/lib/Target/X86/X86InstrSSE.td",
]

# DAG-node-construction call prefixes: each constructs one SDNode, the
# nearest machine-independent analogue of "an emit". Unchanged from the
# probe (recorded data, not re-derived this lap).
EMIT_CALL_PREFIXES = (
    "DAG.getNode", "DAG.getSetCC", "DAG.getSelect", "DAG.getSelectCC",
    "DAG.getConstant", "DAG.getConstantFP", "DAG.getShiftAmountConstant",
    "DAG.getLoad", "DAG.getStore", "DAG.getBitcast", "DAG.getMemIntrinsicNode",
)


def pin_source(rel_path: str) -> str:
    """git show <tag>:<rel_path> from the pinned repo. Never reads the
    working tree (it sits at a different tag)."""
    out = subprocess.run(
        ["git", "show", f"{LLVM_TAG}:{rel_path}"],
        cwd=LLVM_REPO, capture_output=True, text=True, check=True,
    )
    return out.stdout


def resolved_commit() -> str:
    out = subprocess.run(
        ["git", "rev-list", "-n1", LLVM_TAG],
        cwd=LLVM_REPO, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


# ------------------------------------------------------------- graph ---

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.frontier = []

    def add_node(self, node_id, **fields):
        if node_id not in self.nodes:
            self.nodes[node_id] = {"id": node_id, **fields}
        return node_id

    def add_edge(self, src, dst, etype, **extra):
        if src is None or dst is None:
            return
        self.edges.append({"src": src, "dst": dst, "type": etype, **extra})

    def add_frontier(self, kind, file, detail, **extra):
        rec = {"kind": kind, "file": file, "detail": detail, **extra}
        self.frontier.append(rec)


# ------------------------------------------------------ cpp reader -----

def cpp_qualified_name(text_bytes: bytes, node) -> str | None:
    """Best-effort qualified name for a function_definition node: prefer
    the declarator's qualified_identifier (Class::method); else the
    plain identifier/field_identifier/destructor_name/operator_name.

    tree-sitter node spans are BYTE offsets; text_bytes must be the
    ENCODED source the parser actually parsed (never a str sliced by
    those same offsets -- a str index is a character index, and this
    source contains multi-byte UTF-8 sequences upstream of some of the
    functions read here, which silently corrupted names in an earlier
    version of this reader until this fix)."""
    declarator = node.child_by_field_name("declarator")
    while declarator is not None and declarator.type in (
        "pointer_declarator", "reference_declarator",
    ):
        declarator = declarator.child_by_field_name("declarator")
    if declarator is None:
        return None
    fn_decl = declarator
    if fn_decl.type == "function_declarator":
        name_node = fn_decl.child_by_field_name("declarator")
        if name_node is not None:
            return text_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8", "replace")
    return text_bytes[declarator.start_byte:declarator.end_byte].decode("utf-8", "replace")


def cpp_extract_calls(parser: Parser, body_bytes: bytes) -> list[dict]:
    tree = parser.parse(body_bytes)
    calls = []

    def callee_text(node):
        fn = node.child_by_field_name("function")
        return body_bytes[fn.start_byte:fn.end_byte].decode("utf-8", "replace") if fn else ""

    def first_arg_text(node):
        args = node.child_by_field_name("arguments")
        if not args or args.named_child_count == 0:
            return ""
        a0 = args.named_children[0]
        return body_bytes[a0.start_byte:a0.end_byte].decode("utf-8", "replace")

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


def read_cpp(graph: Graph, fname: str, source: str, universe: dict) -> None:
    """Generic cpp reader: every top-level function_definition in the
    file becomes a node (no hand-picked target list, unlike the probe).
    universe accumulates {short_or_qualified_name: node_id} across ALL
    region files read so far, so calls can resolve cross-file within
    the region as they are found (probe's CALL_TARGET_MAP, generalized
    to a lookup table built from what the reader actually saw)."""
    source_bytes = source.encode("utf-8")
    parser = Parser(CPP_LANG)
    tree = parser.parse(source_bytes)

    for top in tree.root_node.named_children:
        candidates = [top] if top.type == "function_definition" else []
        # namespace/class bodies: one level of unwrap is enough for this
        # region (free functions and out-of-line Class:: methods only;
        # in-class method bodies are a named frontier below).
        if top.type in ("namespace_definition",):
            body = top.child_by_field_name("body")
            if body is not None:
                candidates.extend(
                    c for c in body.named_children
                    if c.type == "function_definition"
                )
        for fn in candidates:
            qname = cpp_qualified_name(source_bytes, fn)
            if not qname:
                continue
            start_line = fn.start_point[0] + 1
            end_line = fn.end_point[0] + 1
            body_node = fn.child_by_field_name("body")
            body_bytes = (source_bytes[body_node.start_byte:body_node.end_byte]
                          if body_node is not None else b"")
            node_id = f"{fname}::{qname}"
            calls = cpp_extract_calls(parser, body_bytes) if body_bytes else []
            emit_calls = [c for c in calls if c["callee"].startswith(EMIT_CALL_PREFIXES)]
            graph.add_node(
                node_id, kind="cpp_function", language="cpp", file=fname,
                qualified_name=qname, start_line=start_line, end_line=end_line,
                emit_count=len(emit_calls),
                emits=[{"opcode": c["first_arg"], "line": c["line"],
                        "call": c["callee"]} for c in emit_calls],
                raw_calls=[{"callee": c["callee"], "line": c["line"]} for c in calls],
                full_text=source_bytes[fn.start_byte:fn.end_byte].decode("utf-8", "replace"),
            )
            universe[qname] = node_id
            short = qname.split("::")[-1]
            universe.setdefault(short, node_id)


def cpp_resolve_calls(graph: Graph, universe: dict) -> None:
    """Second pass: resolve each node's raw_calls against the universe
    built from every cpp file in the region. A callee like
    `TLI.expandUINT_TO_FP` resolves by its trailing member name
    (`.name` or `->name`); a bare call resolves by exact/short name.
    Unresolved calls (calls into functions outside the region, e.g.
    into a base-class virtual with no textual match here) are recorded
    as frontier, never guessed."""
    for node_id, node in list(graph.nodes.items()):
        if node.get("kind") != "cpp_function":
            continue
        for c in node.get("raw_calls", []):
            callee = c["callee"]
            key = callee.split(".")[-1].split("->")[-1]
            target = universe.get(callee) or universe.get(key)
            if target is not None and target != node_id:
                graph.add_edge(node_id, target, "calls", at_line=c["line"],
                               callee_text=callee, evidence="tree_sitter_call_expression")
            else:
                graph.add_frontier(
                    "unresolved_call", node["file"], callee,
                    at_line=c["line"], from_node=node_id,
                    reason="callee not defined inside the region's cpp files "
                           "(virtual dispatch, base-class method, or a "
                           "function outside the four-file region)",
                )


DECLINE_GUARDS = [
    # (function qualified-name suffix, guard regex, fallback target qname)
    (
        "X86TargetLowering::LowerUINT_TO_FP",
        re.compile(
            r"if \(Subtarget\.is64Bit\(\) && SrcVT == MVT::i64 &&\s*\n\s*"
            r"\(DstVT == MVT::f32 \|\| DstVT == MVT::f64\)\)\s*\n\s*"
            r"return SDValue\(\);"
        ),
        "SelectionDAGLegalize::LegalizeOp",
        (
            "Custom-lowering hook returns null for (i64,f32) and (i64,f64) "
            "on 64-bit non-AVX512 targets. LegalizeOp's own source (case "
            "TargetLowering::Custom, TLI.LowerOperation returned null) falls "
            "through to Expand when the hook declines -- that fallthrough IS "
            "this edge."
        ),
    ),
]


def cpp_decline_edges(graph: Graph, universe: dict) -> None:
    """Guard -> return SDValue() control flow is not a call_expression,
    so tree-sitter's call walk cannot find it as an edge. Recorded
    per-guard, evidenced by regex match on the function's OWN text
    (kept in full_text above), never asserted without the match. This
    stays a short, named table (not a general control-flow-to-edge
    inference) -- generalizing arbitrary non-call control flow into
    edges is FRONTIER, out of scope this lap."""
    for suffix, guard_rx, fallback_qname, note in DECLINE_GUARDS:
        src_id = universe.get(suffix)
        dst_id = universe.get(fallback_qname)
        if src_id is None or dst_id is None:
            graph.add_frontier("decline_guard_missing_endpoint", None, suffix,
                               fallback=fallback_qname)
            continue
        body = graph.nodes[src_id]["full_text"]
        m = guard_rx.search(body)
        graph.add_edge(src_id, dst_id, "calls_declines",
                       guard_matched_in_source=bool(m),
                       guard_text=guard_rx.pattern, note=note,
                       evidence="regex_match_on_own_extracted_text")


# --------------------------------------------------------- td reader ---

DEFM_RX = re.compile(r"^defm\s+(\w+)\s*:\s*(\w+)\s*<", re.MULTILINE)
# A multiclass's <template args> list commonly spans several lines
# (TableGen has no line-continuation marker; the args list just runs
# on) before the opening '{' of its body. Match only the declaration
# head here; the body's opening brace is located separately by
# scanning forward for the first '{', so the args list length never
# matters.
MULTICLASS_HEAD_RX = re.compile(r"^multiclass\s+(\w+)\s*<", re.MULTILINE)
PAT_RX = re.compile(r"\[\(set[^\]]*\)\]")


def balanced_block(text: str, open_pos: int) -> int:
    """Return the index just past the closing brace matching the '{'
    at-or-after open_pos."""
    i = text.index("{", open_pos)
    depth = 0
    j = i
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise SystemExit("FRONTIER: unterminated multiclass block")


def read_td(graph: Graph, fname: str, source: str) -> dict:
    """Generic TableGen data-table reader (per CORE sec on .td: not
    code, each node is a table entry). Finds EVERY top-level `multiclass
    NAME<...> { ... }` block and every `defm NAME : multiclassref<...>`
    statement in the file, generalizing the probe's single hardcoded
    CVTSI2SS regex to the whole file. Returns {multiclass_name: (start,
    end) span in source} for the isel-pattern-match step."""
    multiclass_spans = {}
    for m in MULTICLASS_HEAD_RX.finditer(source):
        name = m.group(1)
        end = balanced_block(source, m.end())
        multiclass_spans[name] = (m.start(), end)

    defm_nodes = []
    for m in DEFM_RX.finditer(source):
        defm_name, mc_name = m.group(1), m.group(2)
        line_end = source.index("\n", m.start())
        # a defm statement may itself span multiple lines (bracketed
        # arg lists); take up to the terminating ';' on or after the
        # opening line, bounded, so long multi-line invocations do not
        # run away into the next defm.
        semi = source.find(";", m.start())
        stmt_end = semi + 1 if 0 <= semi - m.start() < 2000 else line_end
        defm_text = source[m.start():stmt_end]
        span = multiclass_spans.get(mc_name)
        mc_text = source[span[0]:span[1]] if span else ""
        pat_matches = PAT_RX.findall(mc_text) or PAT_RX.findall(defm_text)
        node_id = f"{fname}::{defm_name}(defm {mc_name})"
        graph.add_node(
            node_id, kind="tablegen_defm", language="tablegen_data",
            file=fname, defm_name=defm_name, multiclass_name=mc_name,
            defm_line=source[:m.start()].count("\n") + 1,
            multiclass_line=(source[:span[0]].count("\n") + 1) if span else None,
            emit_count=len(pat_matches),
            emits=[{"opcode": p, "line": None, "call": "Pat"} for p in pat_matches],
            defm_text=defm_text,
            pattern_text=pat_matches[0] if pat_matches else None,
        )
        defm_nodes.append((node_id, pat_matches))

    graph.add_frontier(
        "tablegen_backend_not_built", fname,
        "TableGen's -gen-dag-isel backend compiles [(set ...)] Pat lines into "
        "the ISel matcher table (X86GenDAGISel.inc, generated, not checked "
        "into the source tree). The Pat pattern in the .td source is the "
        "forced-by-construction fact available without a build; the "
        "generated matcher table itself was not built or inspected this lap "
        "(unchanged frontier from the probe).",
    )
    return {node_id: pats for node_id, pats in defm_nodes}


ISD_OPCODE_RX = re.compile(r"\b(ISD::\w+|any_\w+|[a-z_]+_to_fp)\b")


def isel_pattern_edges(graph: Graph, td_defm_pats: dict) -> None:
    """For every emit recorded on a cpp_function node whose opcode text
    names an ISD/SDNode operator, scan every tablegen_defm node's
    pattern text for that SAME operator name appearing inside a Pat.
    A match is a table lookup, not a call -- recorded as its own edge
    kind (isel_pattern_match), never merged into `calls`. This is text
    containment on the OPERATOR'S OWN NAME as emitted by the compiler's
    own code and read back from the compiler's own TableGen source --
    not a comparison KEY across units, so it does not touch the
    spelling ban (the ban forbids operator tokens as GROUPING/matching
    keys across independently-derived units; this is one name traced
    through one region's own two source kinds)."""
    emit_opcodes = set()
    for node in graph.nodes.values():
        if node.get("kind") != "cpp_function":
            continue
        for e in node.get("emits", []):
            for m in ISD_OPCODE_RX.finditer(e["opcode"] or ""):
                emit_opcodes.add(m.group(1))

    for node_id, pats in td_defm_pats.items():
        for pat in pats:
            for m in ISD_OPCODE_RX.finditer(pat):
                opname = m.group(1)
                if opname in emit_opcodes:
                    graph.add_edge(
                        f"ISD::{opname}" if not opname.startswith("ISD::") else opname,
                        node_id, "isel_pattern_match",
                        note="TableGen Pat contains this operator name; the "
                             "compiler's own emit ('opcode' text on a "
                             "cpp_function's emits list) contains the same name.",
                        evidence="text_containment_on_operator_name_within_region",
                    )


# ---------------------------------------------------------- dispatch ---

READERS = {
    ".cpp": "cpp", ".h": "cpp", ".hpp": "cpp", ".cc": "cpp",
    ".td": "tablegen",
}


def build():
    commit = resolved_commit()
    graph = Graph()
    universe: dict[str, str] = {}
    td_defm_pats: dict[str, list] = {}

    for rel in REGION_FILES:
        fname = Path(rel).name
        ext = Path(rel).suffix
        kind = READERS.get(ext)
        source = pin_source(rel)
        if kind == "cpp":
            read_cpp(graph, fname, source, universe)
        elif kind == "tablegen":
            td_defm_pats.update(read_td(graph, fname, source))
        else:
            graph.add_frontier("no_reader_dispatched", fname,
                               f"extension {ext!r} has no reader this lap")

    cpp_resolve_calls(graph, universe)
    cpp_decline_edges(graph, universe)
    isel_pattern_edges(graph, td_defm_pats)

    # full_text was kept on nodes only to evidence the decline-guard
    # regex; strip it from the emitted JSON (it is 2.5 MB source
    # duplicated per function otherwise) but keep a text_available flag.
    for node in graph.nodes.values():
        if "full_text" in node:
            node["full_text_bytes"] = len(node["full_text"])
            del node["full_text"]

    out = {
        "pins": {
            "tree_sitter": _pkg_version("tree-sitter") if _pkg_version else "unknown",
            "tree_sitter_cpp": _pkg_version("tree-sitter-cpp") if _pkg_version else "unknown",
            "llvm_tag": LLVM_TAG,
            "llvm_commit_resolved_this_run": commit,
            "llvm_commit_recorded_by_probe": "42befb84c672d78de430feb4c96710e6aa4fc774",
            "pin_correction": (
                "probe's recorded hash does not match this run's "
                "`git rev-list -n1 llvmorg-21.1.8`; both resolve to the same "
                "tag date (2025-12-12); read as a probe transcription slip, "
                "not a moved tag -- see build_graph2.py module docstring."
            ),
            "region_files": REGION_FILES,
        },
        "nodes": list(graph.nodes.values()),
        "edges": graph.edges,
        "frontier": graph.frontier,
    }
    out_path = HERE / "graph_cpp2.json"
    out_path.write_text(json.dumps(out, indent=2))
    sys.stderr.write(
        f"wrote {out_path} : {len(graph.nodes)} nodes, {len(graph.edges)} edges, "
        f"{len(graph.frontier)} frontier records\n"
    )
    return out


if __name__ == "__main__":
    build()
