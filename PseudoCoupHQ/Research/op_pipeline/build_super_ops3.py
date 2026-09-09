#!/usr/bin/env python3
"""build_super_ops3.py -- TASK 16: break super_ops2.json's 189
ambiguous-match ties by REACHABILITY, not by widening file count
(round-2 task 11's diagnosis: whole-function emit lists are too
coarse; the fix needs WHICH emitter is actually REACHED for the
idiom's IR operation kind).

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.

Mechanism, in order
--------------------
1. IDIOM KIND, from carrier-unit machine-form evidence (never the
   operator token): every idiom's `sample_unit_ids` point at probe
   rows in probe_manifest_c.json / probe_manifest_cpp.json. Each row
   carries `lhs_rep` / `rhs_rep` -- machine reps such as "u64", "i64",
   "f64" -- assigned by the probe generator from the C/C++ TYPE, not
   from the token. When one carrier's reps show an INTEGER rep paired
   with a FLOAT rep, the idiom's true IR kind is a conversion
   (ISD::UINT_TO_FP for an unsigned integer rep, ISD::SINT_TO_FP for a
   signed one) with SrcVT/DstVT read off the reps themselves -- this
   is machine-form evidence about the CARRIER, never a lookup on the
   idiom's own instruction spelling. When no carrier shows an
   int/float rep mismatch, the idiom's kind falls back to its single
   derived ISD root (already computed by build_super_ops.py's
   VEX_TO_ISD_ROOTS map) IF that idiom has exactly one root; more than
   one root gives no single forced kind and the row is refused at this
   step, not guessed.

2. DISPATCH DATA, parsed from the pinned source (llvmorg-21.1.8, via
   `git show`, never the working tree -- verified again this run),
   never hand-written: two switch tables are extracted as plain
   key->callee-text records --
     (a) X86TargetLowering::LowerOperation's big switch in
         X86ISelLowering.cpp (`case ISD::<KIND>: return Callee(...)`
         -- single-line format, regex-exact)
     (b) SelectionDAGLegalize::ExpandNode's big switch in
         LegalizeDAG.cpp (`case ISD::<KIND>:` label groups, body text
         up to the next case/default label)
   plus the target's own action table (`setOperationAction(ISD::<KIND>,
   <VT>, <Action>)` calls in X86ISelLowering.cpp's constructor) --
   whether X86 marks the kind+VT pair Custom (routes through (a)) or
   leaves it to the generic legalizer (routes through (b)).

3. REACHABILITY. For a Custom-routed kind: the callee named in (a)'s
   case body is hop 1. If a tied candidate's qualified name is that
   callee, it resolves outright. Otherwise hop 1's own function body
   is located in the same file (`SDValue X86TargetLowering::<callee>`
   or `static SDValue <callee>(`) and searched for a call to each
   tied candidate's own (unqualified) name -- a real second hop over
   real call text, the same kind of evidence build_graph3.py's `calls`
   edges already use, just followed one level deeper for this specific
   kind rather than for the whole function body. For an Expand-routed
   kind: (b)'s case body is searched directly (0-hop) for a call to
   each tied candidate's unqualified name.

   A tie breaks ONLY when EXACTLY ONE tied candidate is reached this
   way. More than one reached, or zero, is reported honestly and the
   row stays on the frontier -- never picked by list order (round 1's
   named lesson, restated by round 2, restated here).

Output: super_ops3.json (new file; super_ops2.json untouched).
"""

import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SUPER_OPS2_PATH = os.path.join(HERE, "super_ops2.json")
OUT_PATH = os.path.join(HERE, "super_ops3.json")

LLVM_REPO = os.path.expanduser("~/Programming/Sources/llvm-project")
LLVM_TAG = "llvmorg-21.1.8"

REGION_FILES = [
    "llvm/lib/Target/X86/X86ISelLowering.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeDAG.cpp",
    "llvm/lib/CodeGen/SelectionDAG/TargetLowering.cpp",
    "llvm/lib/CodeGen/SelectionDAG/SelectionDAG.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeTypes.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeFloatTypes.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeIntegerTypes.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeVectorOps.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeVectorTypes.cpp",
    "llvm/lib/CodeGen/SelectionDAG/LegalizeTypesGeneric.cpp",
]

REP_TO_VT = {
    "u8": "i8", "u16": "i16", "u32": "i32", "u64": "i64",
    "i8": "i8", "i16": "i16", "i32": "i32", "i64": "i64",
    "f32": "f32", "f64": "f64",
}
INT_REPS = set(["u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64"])
FLOAT_REPS = set(["f32", "f64"])


def pin_source(rel_path):
    """git show <tag>:<rel_path> from the pinned repo. Never the
    working tree (checked out at llvmorg-24-init -- re-verified this
    run below in main())."""
    out = subprocess.run(
        ["git", "show", "%s:%s" % (LLVM_TAG, rel_path)],
        cwd=LLVM_REPO, capture_output=True, text=True, check=True,
    )
    return out.stdout


def resolved_commit():
    out = subprocess.run(
        ["git", "rev-list", "-n1", LLVM_TAG],
        cwd=LLVM_REPO, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def working_tree_branch():
    out = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=LLVM_REPO, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


# ---------------------------------------------------------------------
# step 1: idiom kind from carrier machine-form evidence
# ---------------------------------------------------------------------

def load_probe_manifests():
    """lang -> {unit_number(str): probe_row_dict}. Only c/cpp -- the
    only languages graph_cpp3.json (and this source region) cover."""
    out = {}
    for lang, fname in [("c", "probe_manifest_c.json"),
                         ("cpp", "probe_manifest_cpp.json")]:
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            doc = json.load(fh)
        out[lang] = doc.get("probes", {})
    return out


def carrier_rows(sample_unit_ids, manifests):
    """sample_unit_ids look like 'c/op_118' -- split lang/unit number,
    look the row up in that language's probe manifest."""
    rows = []
    for uid in sample_unit_ids:
        if "/" not in uid:
            continue
        lang, sym = uid.split("/", 1)
        m = re.match(r"op_(\d+)$", sym)
        if not m or lang not in manifests:
            continue
        row = manifests[lang].get(m.group(1))
        if row is not None:
            rows.append(row)
    return rows


def derive_kind(cand, roots, manifests):
    """returns (kind_dict, evidence_note) or (None, refusal_note).
    kind_dict: {"isd_case": "UINT_TO_FP"|"SINT_TO_FP"|<root>,
                "src_vt": "..."|None, "dst_vt": "..."|None,
                "conversion": bool}

    The conversion override (a carrier's int/float rep mismatch ->
    UINT_TO_FP/SINT_TO_FP) is applied ONLY when the idiom's own
    derived ISD roots are a subset of {"FADD", "FSUB"} -- the two
    roots the *_TO_FP expansion algorithms in the pinned source
    (TargetLowering::expandUINT_TO_FP, LowerUINT_TO_FP_i64,
    SelectionDAGLegalize::ExpandLegalINT_TO_FP) all terminate in,
    verified by reading each of the three bodies. An idiom whose own
    root is a compare (SETCC/FCMP/...) or a bitwise/arith op unrelated
    to *_TO_FP is a DIFFERENT idiom riding the same carrier unit as an
    unrelated conversion (measured case: idiom_0153/0154, CmpEQ64F0x2/
    CmpEQ32F0x4 idioms whose sample carriers happen to also contain a
    UINT_TO_FP-shaped probe) -- for those the conversion override would
    misclassify the idiom's own operation, so it is refused here and
    the idiom falls through to its own root instead."""
    conversion_eligible = roots and roots <= set(["FADD", "FSUB"])
    rows = carrier_rows(cand["sample_unit_ids"], manifests) \
        if conversion_eligible else []
    for row in rows:
        lhs_rep = row.get("lhs_rep")
        rhs_rep = row.get("rhs_rep")
        if lhs_rep in INT_REPS and rhs_rep in FLOAT_REPS:
            int_rep, float_rep = lhs_rep, rhs_rep
        elif rhs_rep in INT_REPS and lhs_rep in FLOAT_REPS:
            int_rep, float_rep = rhs_rep, lhs_rep
        else:
            continue
        signed = not int_rep.startswith("u")
        isd_case = "SINT_TO_FP" if signed else "UINT_TO_FP"
        return (
            {"isd_case": isd_case, "src_vt": REP_TO_VT[int_rep],
             "dst_vt": REP_TO_VT[float_rep], "conversion": True},
            "carrier row %s: lhs_rep=%s rhs_rep=%s -> int/float rep "
            "mismatch, machine-form evidence of an implicit %s"
            % (row.get("symbol"), lhs_rep, rhs_rep, isd_case),
        )
    # no conversion carrier found -- fall back to the single derived
    # root, only if there is exactly one.
    if len(roots) == 1:
        only = next(iter(roots))
        return (
            {"isd_case": only, "src_vt": None, "dst_vt": None,
             "conversion": False},
            "no carrier shows an int/float rep mismatch; falling back "
            "to the single derived ISD root %s" % only,
        )
    return None, (
        "no conversion evidence on any carrier row, and %d derived "
        "ISD roots (not exactly one) -- no single forced kind, "
        "refused at the kind-derivation step" % len(roots)
    )


# ---------------------------------------------------------------------
# step 2: dispatch data, parsed from pinned source as DATA
# ---------------------------------------------------------------------

CASE_LINE_RE = re.compile(
    r'^\s*case ISD::([A-Za-z_0-9]+):\s*(?:return\s+([A-Za-z_][A-Za-z_0-9]*)\('
    r'.*)?$'
)
SETOP_RE = re.compile(
    r'setOperationAction\(\s*ISD::([A-Za-z_0-9]+)\s*,\s*MVT::([A-Za-z_0-9]+)'
    r'\s*,\s*(Legal|Custom|Promote|Expand|LibCall)\s*\)'
)
CALL_NAME_RE = re.compile(r'\b([A-Z][A-Za-z_0-9]{2,})\s*\(')

# noise identifiers that match CALL_NAME_RE's shape but are never a
# candidate emitting function -- LLVM/SelectionDAG API surface, not
# our tied candidates. Kept short: a tied candidate name is checked
# for literal presence directly, this list only prunes what
# lower_operation_callee() may pick up as "the hop-1 callee".
NOT_A_CALLEE = set([
    "SDLoc", "SDValue", "MVT", "EVT", "DAG", "Op", "ISD",
])


def parse_lower_operation_switch(x86_src):
    """X86TargetLowering::LowerOperation's big switch (single case-per-
    line, 'case ISD::X: return Callee(...)' format -- verified by hand
    at X86ISelLowering.cpp:33573-. Returns {isd_case: callee_name}."""
    start = x86_src.index("SDValue X86TargetLowering::LowerOperation(")
    # bound the scan to the next top-level function definition so a
    # same-named case token appearing later in the file is never
    # picked up as part of this switch.
    next_def = x86_src.find("\nSDValue X86TargetLowering::", start + 10)
    if next_def == -1:
        next_def = start + 20000
    body = x86_src[start:next_def]
    out = {}
    for line in body.splitlines():
        m = CASE_LINE_RE.match(line)
        if m and m.group(2):
            out.setdefault(m.group(1), m.group(2))
    return out


def parse_setoperationaction(x86_src, isd_case):
    """every setOperationAction(ISD::<isd_case>, MVT::<vt>, <action>)
    call anywhere in the file -- (vt -> [actions]) since the same
    (op,VT) pair can be set more than once under different subtarget
    guards; every occurrence is kept as data, not resolved to "the"
    single answer (that needs subtarget-feature evaluation this pass
    does not attempt)."""
    out = {}
    for m in SETOP_RE.finditer(x86_src):
        if m.group(1) != isd_case:
            continue
        out.setdefault(m.group(2), []).append(m.group(3))
    return out


def extract_case_body(src, func_signature_prefix, isd_case):
    """generic ExpandNode-shaped switch reader: find the function by
    its signature prefix, then within it find 'case ISD::<isd_case>:'
    (allowing a run of fallthrough case labels immediately above/
    below) and return the body text up to the next case/default
    label at the same nesting depth (approximated by the next line
    that is itself a bare 'case ' or 'default:' label -- true for
    every switch inspected in this region, which are all written one
    case-group per line block, LLVM's own style)."""
    idx = src.find(func_signature_prefix)
    if idx == -1:
        return None
    tail = src[idx:]
    label_re = re.compile(
        r'^\s*case ISD::%s:\s*$' % re.escape(isd_case), re.MULTILINE)
    m = label_re.search(tail)
    if not m:
        # also match a label with trailing code on the same line
        label_re2 = re.compile(
            r'^\s*case ISD::%s:' % re.escape(isd_case), re.MULTILINE)
        m = label_re2.search(tail)
        if not m:
            return None
    after = tail[m.end():]
    next_label = re.search(r'^\s*(case |default:)', after, re.MULTILINE)
    body = after[:next_label.start()] if next_label else after[:4000]
    return body


def callee_body(src, name):
    """locate a function's own body text by its definition line --
    'SDValue X86TargetLowering::<name>(' or 'static SDValue <name>('
    or 'void SelectionDAGLegalize::<name>(' etc. -- generic over
    return type, matched on '::<name>(' or ' <name>(' at line start
    after a type token, bounded to the next top-level function def."""
    pat = re.compile(
        r'^\S.*[\s:]%s\(' % re.escape(name), re.MULTILINE)
    m = pat.search(src)
    if not m:
        return None
    start = m.start()
    # bound to the function's own closing brace: a line consisting of
    # just "}" at column 0, followed by a blank line -- LLVM's own
    # formatting convention for a top-level function's end, checked
    # against LowerUINT_TO_FP itself (ends "  return Result;\n}\n\n").
    # Capped at 8000 chars as a hard backstop so a formatting outlier
    # never turns this into an unbounded, over-inclusive haystack.
    close_re = re.compile(r'\n\}\n\n')
    m2 = close_re.search(src, start, start + 8000)
    end = m2.end() if m2 else start + 8000
    return src[start:end]


def unqualified(name):
    return name.split("::")[-1]


def resolve_reachability(kind, tied_names, files):
    """returns (resolved_name_or_None, trace_lines[list of str]).
    files: dict filename-basename -> source text, for the 11 region
    files (already loaded once in main())."""
    trace = []
    x86 = files["X86ISelLowering.cpp"]
    isd_case = kind["isd_case"]

    action_table = parse_setoperationaction(x86, isd_case)
    trace.append(
        "setOperationAction(ISD::%s, ...) rows found: %s"
        % (isd_case, json.dumps(action_table, sort_keys=True))
    )

    vt_for_lookup = kind["src_vt"] if kind["conversion"] else None
    custom_here = False
    if vt_for_lookup and vt_for_lookup in action_table:
        custom_here = "Custom" in action_table[vt_for_lookup]
    elif not kind["conversion"]:
        # non-conversion kinds: Custom if ANY VT row for this op says
        # Custom anywhere in the table (coarser, stated as such).
        custom_here = any("Custom" in acts for acts in action_table.values())

    reached = set()

    if custom_here or vt_for_lookup is None and action_table:
        lop = parse_lower_operation_switch(x86)
        callee = lop.get(isd_case)
        trace.append(
            "X86TargetLowering::LowerOperation case ISD::%s -> %s"
            % (isd_case, callee if callee else "(no case found)")
        )
        if callee:
            for t in tied_names:
                if unqualified(t) == callee:
                    reached.add(t)
            if not reached:
                body = callee_body(x86, callee)
                if body:
                    for t in tied_names:
                        uq = unqualified(t)
                        if re.search(r'\b%s\s*\(' % re.escape(uq), body):
                            reached.add(t)
                    trace.append(
                        "hop-2 search inside %s(...)'s own body: %s"
                        % (callee,
                           ("found " + ", ".join(sorted(reached)))
                           if reached else "no tied candidate called")
                    )
                else:
                    trace.append(
                        "hop-2: could not locate %s's own definition "
                        "in X86ISelLowering.cpp -- refused, not guessed"
                        % callee
                    )

    # ExpandNode route (LegalizeDAG.cpp) -- always checked too, since
    # a kind can be Custom for one VT and still fall through to the
    # generic expander for another VT/strict-mode row (as ISD::UINT_TO_FP
    # itself does -- TLI.expandUINT_TO_FP is tried first inside
    # ExpandNode's own case body even though X86 marks the op Custom
    # for i64, because ExpandNode's case is reached only from nodes
    # the target left un-Customized or that the type legalizer routed
    # there -- checked as a candidate route, not assumed).
    legalize = files["LegalizeDAG.cpp"]
    body = extract_case_body(
        legalize, "bool SelectionDAGLegalize::ExpandNode(SDNode *Node) {",
        isd_case)
    if body:
        for t in tied_names:
            uq = unqualified(t)
            if re.search(r'\b%s\s*\(' % re.escape(uq), body):
                reached.add(t)
        trace.append(
            "SelectionDAGLegalize::ExpandNode case ISD::%s body: %s"
            % (isd_case,
               ("calls " + ", ".join(sorted(
                   t for t in tied_names if unqualified(t) in body)))
               if any(unqualified(t) in body for t in tied_names)
               else "no tied candidate named in this case's own text")
        )
    else:
        trace.append(
            "SelectionDAGLegalize::ExpandNode: no 'case ISD::%s' label "
            "found" % isd_case
        )

    if len(reached) == 1:
        return next(iter(reached)), trace
    return None, trace + [
        "reachability found %d tied candidates for kind %s (%s) -- %s"
        % (len(reached), isd_case,
           "conversion" if kind["conversion"] else "direct root",
           "still ambiguous" if len(reached) > 1 else "none reached")
    ]


def main():
    branch = working_tree_branch()
    commit = resolved_commit()

    files = {}
    for rel in REGION_FILES:
        files[os.path.basename(rel)] = pin_source(rel)

    manifests = load_probe_manifests()

    with open(SUPER_OPS2_PATH) as fh:
        doc2 = json.load(fh)

    broken = []
    still_frontier = []
    unchanged_frontier = []

    for rec in doc2["frontier"]:
        reason = rec.get("frontier_reason", "")
        if not reason.startswith("ambiguous match:"):
            unchanged_frontier.append(rec)
            continue

        tied_names = re.search(r'tied candidates: (.+?)(?: \(dispatcher|$)',
                                reason)
        tied_names = [s.strip() for s in tied_names.group(1).split(",")] \
            if tied_names else []

        # the reason text is "... derived ISD roots (R1, R2, from N1, N2) --
        # ...": the parenthetical holds the roots list, then the literal
        # ", from ", then the vex-name list -- split there, not on every
        # comma, so a name is never mistaken for a root.
        roots_m = re.search(
            r'against derived ISD roots \((.*?), from [^)]*\)', reason)
        roots = set(x.strip() for x in roots_m.group(1).split(",")) \
            if roots_m else set()

        kind, note = derive_kind(rec, roots, manifests)
        if kind is None:
            rec2 = dict(rec)
            rec2["task16_reachability"] = {
                "kind_derivation": "refused: %s" % note,
                "tied_candidates": tied_names,
            }
            still_frontier.append(rec2)
            continue

        resolved, trace = resolve_reachability(kind, tied_names, files)

        if resolved:
            rec2 = dict(rec)
            del rec2["frontier_reason"]
            rec2["emitting_function_qualified_name"] = resolved
            rec2["task16_reachability"] = {
                "kind_derivation": note,
                "derived_kind": kind,
                "tied_candidates_before": tied_names,
                "trace": trace,
                "evidence_class": (
                    "forced by construction: setOperationAction/"
                    "LowerOperation/ExpandNode case labels and callee "
                    "names are read verbatim from llvmorg-21.1.8 source "
                    "text (git show, pinned tag, never the working "
                    "tree); the carrier-row int/float rep mismatch "
                    "(when conversion=true) is machine-form evidence "
                    "from probe_manifest_*.json's own recorded types, "
                    "never the operator token"
                ),
            }
            broken.append(rec2)
        else:
            rec2 = dict(rec)
            rec2["task16_reachability"] = {
                "kind_derivation": note,
                "derived_kind": kind,
                "tied_candidates_before": tied_names,
                "trace": trace,
            }
            still_frontier.append(rec2)

    out = {
        "role": "TASK 16 -- reachability tie-break over super_ops2.json's "
                "189 ambiguous-match ties",
        "depends_on": "op_pipeline/super_ops2.json (TASK 11); "
                       "compiler_graph/build_graph3.py's REGION_FILES "
                       "(reused, unchanged) as the dispatcher source set",
        "unchanged_from_super_ops2": {
            "resolved": doc2["super_ops"],
            "frontier_non_ambiguous": unchanged_frontier,
        },
        "broken_this_lap": broken,
        "still_ambiguous_or_refused": still_frontier,
        "source_pins": {
            "llvm_tag": LLVM_TAG,
            "llvm_commit_resolved_this_run": commit,
            "working_tree_branch_at_run_time": branch,
            "note": "all region source read via `git show <tag>:<path>` "
                     "against ~/Programming/Sources/llvm-project; the "
                     "working tree itself was NOT read (it sits at %s, "
                     "verified above, not llvmorg-21.1.8)" % branch,
        },
        "counts": {
            "total_ambiguous_ties_in": len(
                [r for r in doc2["frontier"]
                 if r.get("frontier_reason", "").startswith(
                     "ambiguous match:")]),
            "broken": len(broken),
            "still_ambiguous_or_refused": len(still_frontier),
        },
    }

    with open(OUT_PATH, "w") as fh:
        json.dump(out, fh, indent=2)

    print("total ambiguous ties in: %d" % out["counts"]["total_ambiguous_ties_in"])
    print("broken: %d" % out["counts"]["broken"])
    print("still ambiguous/refused: %d" % out["counts"]["still_ambiguous_or_refused"])


if __name__ == "__main__":
    main()
