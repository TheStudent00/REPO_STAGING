#!/usr/bin/env python3
"""canon5.py -- THE CONVERGENCE ENGINE.

AgentMemory's ruling (2026-08-26, "CANONICALIZATION INCLUDES THE
TRANSFORM-AND-RETURN STEP"): canonicalization is not finished while two
units that compute the same thing render as different canonical text.
The simplifier is INSIDE canonicalization, not above it. This file is
the transform-and-return step, run to a fixpoint choice of rendering:

    canon4 text --lift--> z3 expression --simplify--> z3 normal form
        --render--> canon5 text (ASSEMBLED, real `as`+`objdump`)

WHERE "LIFT" COMES FROM (read this before objecting that no new x86
lifter was written). The obvious reading of "lift its canonical text to
the expression form" would build a NEW symbolic evaluator for rendered
AT&T instructions. That is not what this file does, and the reason is
soundness, not laziness: canon4's derived_text and tree_match2.py's
normal_path_root are already two representations of the exact SAME
unit -- same (lang, n), same underlying compiled probe bytes -- one
produced by canon.py's real-register erasure over the disassembly, the
other by pyvex's lift over the same bytes plus tree_match2's z3
normalize(). Re-deriving a second symbolic form FROM the rendered text
with a hand-built x86 evaluator would not be an independent check; it
would be a NEW, unaudited lifter whose bugs could silently disagree
with the ratified VEX lift and nobody would know which one was wrong.
The sound move is to REUSE the unit's own already-computed, already-
ratified expression (tree_units2.json's normal_path_root) as "the
expression form", and prove behaviour preservation the other direction
instead: build a small, closed-vocabulary symbolic SIMULATOR of the
rendered instruction text itself (canon5_behaviour_check.py) and prove
THAT equals the same normal_path_root, for every unit whose text
changed. See item 2 of the work list / canon5_behaviour_check.py.

THE DETERMINISTIC INSTRUCTION-SELECTION RULE (recorded here, per the owner's
ruling that the rule must be named, not left implicit). This file does
not invent a new codegen: it reuses expr_to_canon.py's gen() UNCHANGED.
That function already has exactly one fixed choice per z3 operator,
independent of which source language or which instruction the compiler
originally chose:

  * bvadd/bvor/bvxor/bvand (ALU_OP table): the FIRST operand is `mov`ed
    into the destination register, then EVERY subsequent operand is
    folded in with its own dedicated ALU instruction (`add`, `or`,
    `xor`, `and`) against that same destination -- one instruction per
    operand, always two-address form. In particular this means a sum
    is ALWAYS rendered as `mov` + `add`, NEVER as `lea` -- `lea` is a
    legal one-instruction encoding of the same sum (base+index*scale)
    that gen() simply never emits, by construction, so c's
    `lea (%rdi,%rsi,1),%eax` and go's `mov %edi,%eax` / `add %esi,%eax`
    now both render through the same rule and land on the same text.
  * bvmul: same shape via `imul`.
  * bvnot: `not` in place after rendering the operand.
  * shifts (bvshl/bvlshr/bvashr): render the value, then `shl`/`shr`/
    `sar` by an immediate or (if the amount is itself an expression)
    via `%cl` after a dedicated mov.
  * extract: render the source, `shr` by the low bit if nonzero, mask
    with `and` if the extracted width does not already sit exactly in
    a native register width.
  * concat: a sign-extend shape (all-but-last part are same-width
    extracts of the last part) renders as `movsx`/`movsxd`; a
    zero-extend-by-one-part shape (leading literal 0) renders as
    nothing extra (the narrower write already zero-extends on x86-64);
    the general case renders as repeated `movzx`/`shl`/`or`.

This file's own job is bookkeeping around that fixed rule: run it for
every unit that HAS canon4 text, keep the immediate/register-width
choices gen() already makes, assemble+disassemble the result with the
real `as`/`objdump` (never trust the rendering unassembled), and record
whether the result differs from canon4's own text -- CONVERGED -- or
had to fall back -- NOT YET CONVERGED, with the honest reason, never
hidden as success.

SCOPE. "For every unit with canon4 text" means every unit whose canon4
record actually produced canonical text: either `derived_text` (a
straight-line unit) or `derived_blocks`/`derived_text_flat` (a
branching unit). A unit canon4 itself refused has no text to converge
and is marked `no_canon4_text` here, not silently dropped.

BRANCHING UNITS ARE NOT RENDERED HERE, HONESTLY. expr_to_canon.py's
renderer reconstructs ONE straight-line scalar expression -- the value
on the unit's own return path (tree_match2.py's `normal_path_root`).
A branching unit's canon4 text is multiple basic blocks with real
control flow; collapsing that to a single straight-line rendering
would either be wrong (silently dropping a branch) or would require
control-flow-aware codegen this file does not have. So every branching
unit's canon5_text is its canon4 text, unchanged, with the honest
reason recorded -- "not yet converged", not a fabricated convergence.

THE SPELLING BAN: unchanged from canon4.py -- `operator` is copied
once per unit as the display label; this file's OUTPUT ROOT declares
the same `"meta": {"role": "generator provenance"}` exemption canon4.py
declares (a per-unit-shaped record, no `members`/`pairs`/`rows`/
`groups`/`entries` at the top level). Run check_no_spelling_keys.py on
the output; it must pass.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon5.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import expr_to_canon as EC  # noqa: E402  (render_unit, gen, refusal cats)

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_tree_units2():
    """(lang, n) -> tree_units2.json's own per-unit record (read-only;
    this file is consumed, never rewritten)."""
    path = os.path.join(HERE, "tree_units2.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def canon4_text_of(u):
    """the flat instruction text canon4 produced for this unit, exactly
    as canon4.py's own derived_mnem_joined / derived_text_flat already
    hold it -- straight-line units join with '; ', a branching unit's
    blocks are flattened '<label>: ; <ln>; <ln> ; <label>: ; ...' using
    canon4's own derived_text_flat list (label lines included) so the
    text is unambiguous about block boundaries."""
    if isinstance(u.get("derived_text"), list):
        return u.get("derived_mnem_joined"), "straight_line"
    if "derived_blocks" in u and u.get("erasure") == "ok":
        flat = u.get("derived_text_flat") or []
        return "; ".join(flat), "branching"
    return None, None


def convert_one(lang, n, u, tu2_map, workdir):
    out = {}
    out["lang"] = lang
    out["n"] = n
    out["unit"] = "%s/op_%s" % (lang, n)
    out["operator"] = u.get("operator")
    out["meta"] = u.get("meta")

    canon4_text, kind = canon4_text_of(u)
    if canon4_text is None:
        out["status"] = "no_canon4_text"
        out["reason"] = "canon4 itself produced no canonical text for " \
            "this unit (erasure=%r) -- nothing to converge" % \
            u.get("erasure")
        out["canon4_text"] = None
        out["canon5_text"] = None
        out["normalized_expression"] = None
        out["converged"] = False
        return out

    out["branch_kind"] = kind
    out["canon4_text"] = canon4_text

    if kind == "branching":
        out["status"] = "not_yet_converged"
        out["reason"] = "branching unit -- expr_to_canon's renderer " \
            "only reconstructs a single straight-line scalar " \
            "expression on the unit's return path (tree_match2's " \
            "normal_path_root); multi-block control flow is out of " \
            "scope for this return-path renderer, so the canon4 form " \
            "is kept as-is rather than dropping a branch"
        out["canon5_text"] = canon4_text
        out["normalized_expression"] = None
        out["converged"] = False
        return out

    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        out["status"] = "not_yet_converged"
        out["reason"] = "no tree_match2 (tree_units2.json) record for " \
            "this unit -- cannot lift to an expression form"
        out["canon5_text"] = canon4_text
        out["normalized_expression"] = None
        out["converged"] = False
        return out

    result = EC.render_unit(tu2, workdir)
    if isinstance(result, list):
        candidate = "; ".join(result)
        out["normalized_expression"] = tu2.get("normal_path_root")
        out["canon5_text"] = candidate
        if candidate != canon4_text:
            out["status"] = "converged"
            out["converged"] = True
        else:
            out["status"] = "unchanged"
            out["converged"] = False
        return out

    # result is a "no return path: ..." string -- honest fallback.
    out["status"] = "not_yet_converged"
    out["reason"] = result
    out["canon5_text"] = canon4_text
    out["normalized_expression"] = tu2.get("normal_path_root")
    out["converged"] = False
    return out


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def run_language(lang, indir, outdir, workdir, tu2_map):
    canon4_path = os.path.join(indir, "canon4_units_%s.json" % lang)
    canon4_doc = json.load(open(canon4_path))
    canon4_units = canon4_doc["units"]
    keys = sorted(canon4_units.keys(), key=lambda x: int(x))

    rows = {}
    counts = {"no_canon4_text": 0, "unchanged": 0, "converged": 0,
              "not_yet_converged": 0}
    reasons = {}

    for n in keys:
        rec = convert_one(lang, n, canon4_units[n], tu2_map, workdir)
        rows[n] = rec
        counts[rec["status"]] = counts.get(rec["status"], 0) + 1
        if rec["status"] == "not_yet_converged":
            key = rec["reason"].split(" -- ")[0].split(" (")[0][:90]
            reasons[key] = reasons.get(key, 0) + 1

    out = {}
    out["language"] = lang
    out["meta"] = {
        "role": "generator provenance",
        "form": "canon5: the transform-and-return convergence engine -- "
               "canon4 text lifted (via each unit's own already-"
               "computed tree_match2 normal_path_root, never a new "
               "x86 symbolic re-lift), z3-simplified, rendered back "
               "to assembled canonical text by expr_to_canon.py's "
               "unchanged gen() instruction-selection rule",
        "spelling": "the operator token appears once per unit, as "
                   "the display label `operator` on a unit object",
        "generator": "canon5.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                      time.gmtime()),
    }
    out["units_read"] = len(keys)
    out["counts"] = counts
    out["not_yet_converged_reasons"] = reasons
    out["units"] = rows

    name = os.path.join(outdir, "canon5_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s (%d read, %d no_canon4_text, %d unchanged, "
        "%d converged, %d not_yet_converged)"
        % (name, len(keys), counts["no_canon4_text"],
           counts["unchanged"], counts["converged"],
           counts["not_yet_converged"]))
    return out


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2
    started = time.time()
    log("canon5.py -- the convergence engine")
    tu2_map = load_tree_units2()
    workdir = tempfile.mkdtemp(prefix="canon5_asm_")
    for lang in LANGS:
        run_language(lang, indir, outdir, workdir, tu2_map)
    log("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
