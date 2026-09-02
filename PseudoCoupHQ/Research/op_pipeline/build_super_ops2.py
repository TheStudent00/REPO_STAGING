#!/usr/bin/env python3
"""build_super_ops2.py -- TASK 11: re-join the miner against the WIDENED
graph (build_graph3.py's graph_cpp3.json, 2280 nodes / 18331 edges,
against lap two's 1232 nodes / 3070 edges), and add ONE new tie-break
rule that build_super_ops.py did not have: DISPATCHER DEMOTION.

The rule, stated once so it is never confused with a spelling match:
among nodes tied at the maximum ISD-root-component overlap, if the
graph's own `calls` edges (tree_sitter_call_expression evidence, the
SAME edges build_graph2.py/build_graph3.py already produced -- nothing
new is asserted here) show that one tied node CALLS another tied node,
the caller is dropped from the tied set. A dispatcher that merely
delegates to a more specific tied sibling is demoted in favor of the
sibling it calls, because the sibling is the function whose OWN body
holds the emit, not a relay. This is graph-structural (call edges),
never a token/spelling comparison -- THE SPELLING BAN's mechanical
guard (check_no_spelling_keys.py) is run on this file's output same as
lap one's.

Everything else (VEX_TO_ISD_ROOTS map, component-overlap matching,
frontier reasons, record shape) is UNCHANGED from build_super_ops.py,
reused by copy so the two runs are comparable line for line. Output is
a NEW file, super_ops2.json -- super_ops.json is left untouched.
"""

"""build_super_ops.py -- TASK 6: join the graph to the miner (super-op
provenance).

THE SPELLING BAN, restated verbatim as required by every artifact on
this line: "THE SPELLING BAN, ABSOLUTE (the owner, restated in anger
2026-08-25 after a second violation). No operator token may appear in
ANY key, grouping, pairing, row structure, candidate selection, or
comparison scope, anywhere in this line -- not in matching, not in
"which pairs get compared", not in report rows, not in dropdowns. The
candidate set for comparison comes from machine-form evidence
(clusters, connections, type pairs) or from ratified intention -- never
from the token. The token appears exactly once per unit: as a display
label on the member."

What this does
--------------
Reads `idiom_candidates.json` (the recurrence miner's output) and
`../compiler_graph/graph_cpp2.json` (Task 1's dispatched graph over the
X86 SelectionDAG legalization/lowering region). For every candidate
with support >= 4, it asks: which function in the graph EMITS this
idiom's instructions? The candidate set is never keyed by the
instruction spelling; grouping/output keys are `idiom_id` strings
(idiom_0001, idiom_0002, ...) assigned by list position, not by token.

The search key is `names_within_own_lifted_form` -- a field the miner
already computed FORCED BY CONSTRUCTION (an exact-token check of the
row's own instruction text against VEX_NAME_TO_MNEM; see
idiom_candidates.json's own evidence_class string). This script adds
exactly one new mapping on top of that: VEX lifter name -> LLVM ISD
opcode root (VEX_TO_ISD_ROOTS below). That map is HUMAN INTERPRETATION
OF STATED DESIGN (the LLVM ISD naming convention: FADD/FSUB/FMUL/FDIV
for float arithmetic, AND/OR/XOR for bitwise, SETCC for compares) --
weakest evidence class, stated on every record that uses it.

A candidate resolves when a graph node's `emits` list contains an
opcode whose ISD::-stripped, underscore-split component set intersects
the candidate's derived ISD roots. Component-exact matching (never
substring) is used specifically to avoid false hits such as "OR"
matching inside "XOR".

Candidates outside c/cpp (go, rust, swift) have NO reader in
graph_cpp2.json (Task 1's own named frontier) -- they are recorded as
frontier by coverage gap, not searched.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(os.path.dirname(HERE), "compiler_graph",
                           "graph_cpp3.json")
CANDIDATES_PATH = os.path.join(HERE, "idiom_candidates.json")
OUT_PATH = os.path.join(HERE, "super_ops2.json")

MIN_SUPPORT = 4

# human interpretation of stated design (LLVM ISD opcode naming
# convention) -- weakest evidence class, applied on top of the miner's
# forced-by-construction names_within_own_lifted_form.
VEX_TO_ISD_ROOTS = {
    "Add32F0x4": ["FADD"],
    "Add64F0x2": ["FADD"],
    "Sub32F0x4": ["FSUB"],
    "Sub64F0x2": ["FSUB"],
    "Mul32F0x4": ["FMUL"],
    "Mul64F0x2": ["FMUL"],
    "Div32F0x4": ["FDIV"],
    "Div64F0x2": ["FDIV"],
    "Mul32": ["MUL", "SMUL", "UMUL"],
    "Mul64": ["MUL", "SMUL", "UMUL"],
    "DivModS128to64": ["SDIVREM", "SDIV", "SREM"],
    "DivModU128to64": ["UDIVREM", "UDIV", "UREM"],
    "AndV128": ["AND"],
    "OrV128": ["OR"],
    "XorV128": ["XOR"],
    "CmpEQ32F0x4": ["SETCC", "FCMP", "SETOEQ", "SETONE"],
    "CmpEQ64F0x2": ["SETCC", "FCMP", "SETOEQ", "SETONE"],
}

COVERED_LANGUAGES = set(["c", "cpp"])

SPLIT_RE = re.compile(r"::|_")


def opcode_components(opcode):
    """split an emitted opcode string ("ISD::STRICT_FADD") into its
    exact name components (["ISD", "STRICT", "FADD"]). non-ISD opcode
    text (raw hex constants, variable names the reader captured verbatim
    off DAG.getConstant/getLoad/... calls) yields no components at all,
    which is correct: those are not opcode names to match against."""
    if not isinstance(opcode, str):
        return []
    if not opcode.startswith("ISD::"):
        return []
    return [p for p in SPLIT_RE.split(opcode) if p]


def stage_for_file(file_name):
    """the emitting function's stage, by which of the four region files
    it lives in (Task 1's region, unchanged): LegalizeDAG.cpp is
    legalization; X86ISelLowering.cpp and X86InstrSSE.td (TableGen
    selection patterns) are selection; TargetLowering.cpp is the
    target-independent legalization hook surface, grouped with
    legalization since ExpandLegalINT_TO_FP-shaped work lives there.
    No runtime-library file is in this region -- a candidate whose only
    match were a runtime-library call would not be reachable by this
    stage classifier, and none were, recorded under numbers below."""
    if file_name in (
        "LegalizeDAG.cpp", "TargetLowering.cpp", "SelectionDAG.cpp",
        "LegalizeTypes.cpp", "LegalizeFloatTypes.cpp",
        "LegalizeIntegerTypes.cpp", "LegalizeVectorOps.cpp",
        "LegalizeVectorTypes.cpp", "LegalizeTypesGeneric.cpp",
    ):
        return "legalization"
    if file_name == "X86ISelLowering.cpp":
        return "selection"
    if file_name == "X86InstrSSE.td":
        return "selection"
    return "unclassified:%s" % file_name


def load(path):
    with open(path) as fh:
        return json.load(fh)


def build_node_index(graph):
    """cpp_function nodes that emit at least one opcode, plus their
    ISD root component sets, precomputed once."""
    out = []
    for n in graph["nodes"]:
        if n.get("kind") != "cpp_function":
            continue
        if n.get("emit_count", 0) <= 0:
            continue
        comps = set()
        opcodes = []
        for e in n.get("emits", []):
            op = e.get("opcode")
            c = opcode_components(op)
            if c:
                comps.update(c)
            if op and op not in opcodes:
                opcodes.append(op)
        out.append({
            "node": n,
            "isd_components": comps,
            "extent": opcodes,
        })
    return out


def derive_roots(names_within_own_lifted_form):
    roots = set()
    unmapped = []
    for nm in names_within_own_lifted_form:
        r = VEX_TO_ISD_ROOTS.get(nm)
        if r:
            roots.update(r)
        else:
            unmapped.append(nm)
    return roots, unmapped


def build_call_index(graph):
    """id -> set(ids this node calls), from the graph's own `calls`
    edges (tree_sitter_call_expression evidence -- the same edges
    build_graph2.py/build_graph3.py already emit; nothing new is
    asserted here). Used only for dispatcher demotion below."""
    out = {}
    for e in graph.get("edges", []):
        if e.get("type") != "calls":
            continue
        out.setdefault(e["src"], set()).add(e["dst"])
    return out


def demote_dispatchers(tied, calls_index):
    """TASK 11's new rule. tied is a list of (entry, overlap) all at the
    SAME maximum ISD-root overlap. If one tied node's own `calls` edges
    reach ANOTHER tied node, the caller is a dispatcher relative to that
    sibling -- it relays, the callee is the one whose OWN body holds the
    matching emit -- so the caller is dropped. Fixed point: repeat until
    no more drops happen or one node remains. This is a GRAPH-STRUCTURAL
    rule (call edges only) -- no operator token is read or compared."""
    ids = {e["node"]["id"] for e, _ in tied}
    current = list(tied)
    while len(current) > 1:
        callers = set()
        for e, _ in current:
            reaches = calls_index.get(e["node"]["id"], set())
            if reaches & ids:
                callers.add(e["node"]["id"])
        if not callers:
            break
        remaining = [(e, o) for e, o in current if e["node"]["id"] not in callers]
        if not remaining:
            # every tied node calls another tied node (a cycle) -- demoting
            # all of them would leave nothing; refuse the demotion pass
            # rather than produce an empty tied set.
            break
        dropped = [e["node"]["qualified_name"] for e, _ in current
                   if e["node"]["id"] in callers]
        current = remaining
        ids = {e["node"]["id"] for e, _ in current}
    return current


def match_node(roots, node_entries, calls_index=None):
    """best node = most overlapping ISD root components. MEASURED (see
    log_088): a single-root overlap (roots has exactly one member, e.g.
    {"FADD"}) is not selective -- 10 distinct functions in this region
    all emit ISD::FADD somewhere in their body. Picking one by list
    order there would be an UNFOUNDED choice dressed as a resolved
    provenance record. So this function reports EVERY node tied at the
    maximum overlap size; the caller resolves only when exactly one
    node holds the maximum, and records an ambiguous-match frontier
    otherwise, naming every tied candidate.

    TASK 11 addition: once the tie is found, demote_dispatchers() is
    applied on top (graph-structural, see its own docstring) BEFORE the
    caller checks tie length. This can shrink or fully resolve a tie
    that lap two could not, without ever comparing operator spelling."""
    best_overlap_len = 0
    tied = []
    for entry in node_entries:
        overlap = roots & entry["isd_components"]
        if not overlap:
            continue
        if len(overlap) > best_overlap_len:
            best_overlap_len = len(overlap)
            tied = [(entry, overlap)]
        elif len(overlap) == best_overlap_len:
            tied.append((entry, overlap))
    demoted = False
    if len(tied) > 1 and calls_index is not None:
        before = len(tied)
        tied = demote_dispatchers(tied, calls_index)
        demoted = len(tied) < before
    return tied, demoted


def main():
    graph = load(GRAPH_PATH)
    candidates_doc = load(CANDIDATES_PATH)
    all_candidates = candidates_doc["candidates"]

    node_entries = build_node_index(graph)
    calls_index = build_call_index(graph)

    selected = [c for c in all_candidates if c["support"] >= MIN_SUPPORT]

    super_ops = []
    frontier = []

    for i, cand in enumerate(selected):
        idiom_id = "idiom_%04d" % (i + 1)
        langs = cand["languages"]
        uncovered_langs = [l for l in langs if l not in COVERED_LANGUAGES]

        base_record = {
            "idiom_id": idiom_id,
            "instructions": cand["instructions"],
            "support": cand["support"],
            "languages": langs,
            "sample_unit_ids": cand["sample_unit_ids"],
            "names_within_own_lifted_form":
                cand["names_within_own_lifted_form"],
        }

        if uncovered_langs:
            rec = dict(base_record)
            rec["frontier_reason"] = (
                "no graph coverage: graph_cpp3.json (Task 11) reads only "
                "cpp/tablegen sources over the widened 11-file region; "
                "these languages have no reader in that graph: %s (named "
                "frontier, reused from Task 1/6, unchanged by widening)"
                % ", ".join(sorted(set(uncovered_langs)))
            )
            frontier.append(rec)
            continue

        names = cand["names_within_own_lifted_form"]
        if not names:
            rec = dict(base_record)
            rec["frontier_reason"] = (
                "no forced-by-construction search key: "
                "names_within_own_lifted_form is empty on this row (its "
                "blocking_lifter_names, if any, are co-occurrence only -- "
                "querying the graph on a co-occurrence name would not be "
                "forced by construction, so this row is refused rather "
                "than guessed at)"
            )
            frontier.append(rec)
            continue

        roots, unmapped = derive_roots(names)
        if not roots:
            rec = dict(base_record)
            rec["frontier_reason"] = (
                "names_within_own_lifted_form present (%s) but none has "
                "an entry in this script's VEX_TO_ISD_ROOTS map -- the "
                "map covers the 17 names idiom_candidates.json's own "
                "vex_name_to_mnem carries; extending it is a named "
                "frontier, not a guess" % ", ".join(names)
            )
            frontier.append(rec)
            continue

        tied, demoted = match_node(roots, node_entries, calls_index)
        if not tied:
            rec = dict(base_record)
            rec["frontier_reason"] = (
                "derived ISD roots (%s, from %s) found no overlapping "
                "emitting function in the widened graph region (Task 11) -- the "
                "idiom's emitter, if any, is outside this region too"
                % (", ".join(sorted(roots)), ", ".join(names))
            )
            frontier.append(rec)
            continue

        if len(tied) > 1:
            rec = dict(base_record)
            tied_names = sorted(e["node"]["qualified_name"] for e, _ in tied)
            rec["frontier_reason"] = (
                "ambiguous match: %d functions tie at the same overlap "
                "size against derived ISD roots (%s, from %s) -- picking "
                "one by list order would be unfounded, so this idiom is "
                "refused rather than resolved. tied candidates: %s%s"
                % (len(tied), ", ".join(sorted(roots)), ", ".join(names),
                   ", ".join(tied_names),
                   " (dispatcher demotion applied and reduced this tie but "
                   "did not break it)" if demoted else "")
            )
            frontier.append(rec)
            continue

        best, overlap = tied[0]
        node = best["node"]
        rec = dict(base_record)
        rec["emitting_function"] = {
            "id": node["id"],
            "file": node["file"],
            "qualified_name": node.get("qualified_name"),
            "start_line": node.get("start_line"),
            "end_line": node.get("end_line"),
        }
        rec["stage"] = stage_for_file(node["file"])
        rec["dispatcher_demotion_applied"] = demoted
        rec["extent"] = best["extent"]
        rec["carrier_units"] = cand["sample_unit_ids"]
        rec["match_basis"] = {
            "derived_isd_roots": sorted(roots),
            "matched_isd_components": sorted(overlap),
            "unmapped_vex_names": unmapped,
            "evidence_class": (
                "names_within_own_lifted_form is forced by construction "
                "(idiom_candidates.json's own evidence_class string); "
                "the VEX-name -> ISD-root map and the component-overlap "
                "match against the graph's emit list are human "
                "interpretation of stated design (LLVM ISD opcode naming "
                "convention) -- weakest evidence class, stated here so "
                "it is never read as forced"
            ),
        }
        super_ops.append(rec)

    doc = {
        "role": "super-op provenance re-join, TASK 11 (widened graph + "
                "dispatcher-demotion tie-break, over TASK 6's join)",
        "depends_on": "TASK 11 (compiler_graph/build_graph3.py, "
                       "graph_cpp3.json); prior lap: TASK 1/6 "
                       "(build_graph2.py, graph_cpp2.json, super_ops.json, "
                       "left untouched)",
        "candidate_source": "idiom_candidates.json",
        "graph_source": "compiler_graph/graph_cpp3.json (co-node of "
                         "op_pipeline under Research/)",
        "graph_pins": graph.get("pins"),
        "min_support_included": MIN_SUPPORT,
        "population": {
            "total_candidates_in_file": len(all_candidates),
            "candidates_support_ge_%d" % MIN_SUPPORT: len(selected),
            "resolved_super_ops": len(super_ops),
            "frontier": len(frontier),
        },
        "vex_to_isd_roots_map": VEX_TO_ISD_ROOTS,
        "super_ops": super_ops,
        "frontier": frontier,
    }

    with open(OUT_PATH, "w") as fh:
        json.dump(doc, fh, indent=2)

    print("wrote", OUT_PATH)
    print("candidates support>=%d: %d" % (MIN_SUPPORT, len(selected)))
    print("resolved super_ops:", len(super_ops))
    print("frontier:", len(frontier))


if __name__ == "__main__":
    main()
