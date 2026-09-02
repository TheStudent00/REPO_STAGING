#!/usr/bin/env python3
"""canon24.py -- JOB 1's driver (log_082 lap): THE CMPEQ/CMPNEQ PACKED-
FLOAT-MASK FAMILY, closed by vex_names.py's own generic name translator.

TARGET SET: every not-yet-converged, straight-line unit (baseline:
canon23_units_<lang>.json, the newest generation on disk before this
lap) whose own tree_units3.json `normal_path_raw` (the ADOPTED, ret-
block-first tree_match3.py baseline) contains `CmpEQ32F0x4`/
`CmpEQ64F0x2` -- either standalone (a real `cmpeqss`/`cmpeqsd`) or
wrapped as `XorV128(all-ones-at-lane-width, CmpEQ...(P,Q))`, VEX's own
lowering of a single real `cmpneqss`/`cmpneqsd` (see vex_names.py's own
header for the measured evidence). SURVEYED (this lap's own script,
see report): 42 units, all five languages, ALL `!=`/`not_eq`, ALL
straight_line, ALL the identical shape `ins@0(ins@0(u0:256,<conv>),
XorV128(all-ones,CmpEQ...(P,Q)))` -- a clean, closed population.

OUT OF SCOPE, named honestly (not attempted here): the packed
arithmetic family's own residual (Add/Sub/Mul/Div at 32F0x4/64F0x2) is
either non-straight-line (the u64/i64->float overflow-guard branch,
needing the guarded-containment relation, a different lap's own job)
or the "magic bit-pattern constant" u64/i64->double idiom
(InterleaveLO32x4/Sub64Fx2/64HLtoV128) condition_table6.py's own header
already named out of scope; neither is a shape this file's own render
path (an Extract-of-one-atom collapse) reaches. vex_names.py's own
generic z3 dispatch DOES compute real terms for all twelve names
regardless (see tree_match4.py, JOB 1's normalization-level result);
this driver's own render+gate convergence is the narrower, PROVEN
subset.

THE WRAP: this family's real answer is read through a chain of dead-
write ins@0 bookkeeping with NO enclosing extract in normal_path_raw
itself (tree_match3.py's own block/value selection keeps the WHOLE
xmm-register write as "the answer", since that IS the normal-path
value at the VEX level) -- so this driver wraps each target unit's raw
text in an outer `ex32@0(...)` before normalizing. Measured directly
(this lap's own report): z3's own simplifier then collapses the dead
upper-lane bookkeeping away completely, mechanically, leaving exactly
`Extract(31, 0, <fcmpmask atom>)` -- never assumed, verified per unit
below (a unit whose own re-derivation does NOT collapse this way is
refused, not rendered).

RENDER: canon24_render.gen24 (Extract-of-atom interception -- see that
file's own header for why an Extract hook, not a bare-atom hook).
GATE: canon24_behaviour_check.anchored_check_24 (Sim24, canon22's own
GP+condition lineage plus real z3 FPA cmpeqss/cmpeqsd/cmpneqss/
cmpneqsd, plus a corrected movd/movq-from-xmm narrowing read -- see
that file's own header for the bug this lap found and fixed).

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened (identical discipline to every driver in this lineage); an
already-converged unit's own text is never touched by this file.

usage:
  canon24.py [--in DIR] [--out DIR]
"""

import json
import os
import re
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import vex_names as VN                                          # noqa: E402
import canon24_render as R24                                     # noqa: E402
import canon24_behaviour_check as BC24                            # noqa: E402
import canon17_render as R17                                      # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

LANE_CMP_NAME_RE = re.compile(r"CmpEQ(32|64)F0x\d+\(")


def load_tree_units3():
    path = os.path.join(HERE, "tree_units3.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def is_our_shape(raw_text):
    """cheap pre-filter: does this unit's raw text even mention the
    lane-compare family at all? (the expensive z3 attempt is only
    made when this is true)."""
    if raw_text is None:
        return False
    return LANE_CMP_NAME_RE.search(raw_text) is not None


def convert_one(lang, n, old_rec, tu3_rec, canon4_docs, sem_map,
                 workdir):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    if tu3_rec is None:
        return None
    raw = tu3_rec.get("normal_path_raw")
    if tu3_rec.get("sem_ok") is False or raw is None:
        return None
    if not is_our_shape(raw):
        return None

    wrapped = "ex32@0(%s)" % raw
    new_root, ok, note = VN.normalize_atoms_v3(wrapped)
    if not ok:
        return {
            "job1_cmpmask_candidate_text": None,
            "job1_cmpmask_refusal_reason":
                "z3 failed to normalize this unit's own atom+"
                "provenance form (%s)" % note,
        }

    meta = old_rec.get("meta") or {}
    a_is_vector = meta.get("lhs_rep") in ("f32", "f64")
    R17.set_render_context(a_is_vector)

    fixed_unit = dict(
        lang=lang, n=n, sem_ok=True,
        normal_path_root=new_root, normalize_ok=True,
        normal_path_raw=wrapped)

    result, ctxd = R24.render_unit24(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job1_cmpmask_wrapped_raw": wrapped,
            "job1_cmpmask_normalized_root": new_root,
            "job1_cmpmask_candidate_text": None,
            "job1_cmpmask_refusal_reason": result,
        }

    candidate = "; ".join(result)

    verdict, detail = BC24.anchored_check_24(
        lang, n, canon4_docs, sem_map, candidate, a_is_vector)

    update = {
        "job1_cmpmask_wrapped_raw": wrapped,
        "job1_cmpmask_normalized_root": new_root,
        "job1_cmpmask_candidate_text": candidate,
        "job1_cmpmask_ground_truth_verdict": verdict,
        "job1_cmpmask_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon24_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "canon24.py (JOB 1, log_082 lap: the " \
            "CmpEQ/CmpNEQ packed-float-mask family, closed by " \
            "vex_names.py's generic SIMD-float name translator): " \
            "candidate proved bit-level equal to the unit's own " \
            "real ship code directly"
        return update

    update["job1_cmpmask_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu3_map,
                  workdir):
    canon23_path = os.path.join(indir, "canon23_units_%s.json" % lang)
    doc = json.load(open(canon23_path))
    units = doc["units"]

    attempted = 0
    accepted = 0
    disproved = 0
    undecided = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        tu3 = tu3_map.get((lang, n))
        update = convert_one(lang, n, u, tu3, canon4_docs, sem_map,
                              workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job1_cmpmask_candidate_text") is None:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        elif update.get("job1_cmpmask_ground_truth_verdict") == \
                "DISPROVED":
            disproved = disproved + 1
        else:
            undecided = undecided + 1

    doc["job1_cmpmask_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "disproved": disproved,
        "undecided": undecided,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon24.py (JOB 1, log_082 lap: the " \
        "CmpEQ/CmpNEQ packed-float-mask family) over canon23_units_" \
        "%s.json, raw text re-sourced from tree_units3.json, wrapped " \
        "in an outer ex32@0(...)" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon24_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d disproved, %d "
          "undecided, %d no candidate, %d not our shape)"
          % (name, attempted, accepted, disproved, undecided,
             no_candidate, skipped_not_our_shape))
    return doc


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
    print("canon24.py -- JOB 1: the CmpEQ/CmpNEQ packed-float-mask "
          "family (vex_names.py's generic translator)")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = {}
    for lang in LANGS:
        path = os.path.join(indir, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]

    tu3_map = load_tree_units3()

    workdir = tempfile.mkdtemp(prefix="canon24_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "disproved": 0, "undecided": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map, workdir)
        for k in totals:
            totals[k] += doc["job1_cmpmask_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
