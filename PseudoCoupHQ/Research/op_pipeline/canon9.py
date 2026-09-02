#!/usr/bin/env python3
"""canon9.py -- JOB 2, first attack on the 813 units canon8.py left
not_yet_converged: the largest single bucket, 186 units refusing
because their lifted expression carries an opaque
`amd64g_calculate_condition` atom left behind by condition_table.py's
too-narrow flagsetter recognition (see condition_table2.py's header
for the full diagnosis and why the fix is safe).

SCOPE, stated honestly: this pass only re-attempts STRAIGHT-LINE units
(all 186 of the targeted bucket are straight_line -- verified by
direct count against canon8_units_<lang>.json's own `branch_kind`
field; branching units' CAUSE-1 substitution lives inside canon7_
render.py's render_branching_unit7, which this file does not touch,
so branching units are copied through from canon8 UNCHANGED).

DRIVER SHAPE: canon7.py's convert_one/run_language, reused for
everything except:
  1. apply_cause123 -> apply_cause123_v2, which calls condition_
     table2.resolve_conditions instead of tree_match2.resolve_
     conditions (which itself calls condition_table.py, the narrow
     table) -- THE ONLY substantive change to the render path.
  2. THE GATE IS THE RE-ANCHORED ONE (JOB 1's fix, canon8_behaviour_
     check.py): a candidate is accepted iff it proves equal to the
     unit's OWN REAL SHIP CODE directly, never against a prior
     rendering. This is what makes widening condition_table.py SAFE
     even without a fresh per-mnemonic angr proof (see condition_
     table2.py's header, "THE SAFETY NET").
  3. THE BASELINE is canon8_units_<lang>.json (JOB 1's output, the
     current-best corpus), not canon5. Only units still
     not_yet_converged there are re-attempted; everything else is
     copied through byte-for-byte -- ZERO REGRESSION by construction
     (a copied-through unit's text field is never touched).

usage:
  canon9.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2                                       # noqa: E402
import condition_table2 as CT2                                  # noqa: E402
import canon7_render as R7                                      # noqa: E402
import canon8_behaviour_check as BC8                             # noqa: E402
import z3                                                        # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


class Sim9(BC8.Sim8):
    """canon8_behaviour_check.Sim8, PLUS logic-family flag tracking
    for `or`/`and`/`xor` (real x86-64 hardware sets ZF/SF/PF/CF=0/
    OF=0 on EVERY execution of these, unconditionally -- the checker
    must track that too, or it cannot verify real ship code whose
    setcc reads flags left by an `or`/`and`/`xor` instead of a `cmp`/
    `test`, which is exactly the shape condition_table2.py's render-
    side fix targets (16 units, all `or`/`xor` -- see condition_
    table2.py's header; `add`/`sub`/`neg` are DELIBERATELY NOT added
    here, matching condition_table2.py's own conservative scope: none
    of this lap's target units need them, and this checker's generic
    (L,R)=(result,0) formula is UNVERIFIED for CF/OF-dependent
    conditions after an arithmetic op, unlike the logic family, which
    IS verified sound -- see condition_table2.py's header for the
    per-condition derivation). Kept as a SEPARATE class from Sim8
    (JOB 1's own, already reported and validated) rather than edited
    in place, so JOB 1's numbers stay exactly reproducible."""

    def exec_line(self, line):
        stripped = line.strip()
        parts = stripped.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem in ("or", "and", "xor"):
            operands = BC8.split_operands(rest)
            src, dst = operands
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            b = self.read_at(src, width)
            if mnem == "or":
                r = a | b
            elif mnem == "and":
                r = a & b
            else:
                r = a ^ b
            self.write(dst, r)
            self.last_cmp = (r, z3.BitVecVal(0, width))
            return
        BC8.Sim8.exec_line(self, line)


def job2_anchored_check(lang, n, canon4_docs, sem_docs, text):
    """canon8_behaviour_check.anchored_check, using Sim9 (this file's
    logic-family-flag-aware simulator) instead of Sim8 -- everything
    else (real-text lookup, register-identity pre-binding, shift-
    count masking) is reused UNCHANGED from JOB 1's own module."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit"
    a_fam, b_fam = BC8.real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = BC8.seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = BC8.seed_family(shared_seed, "rsi")
    sim_real = Sim9(shared_seed, "real")
    sim_cand = Sim9(shared_seed, "cand")
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in text.split(";")]
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except BC8.NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)
    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved this text equal to the " \
            "unit's own real ship code (register-identity-bound, " \
            "shift-masked, logic-flag-aware model)"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample: %s" % model
    return "UNDECIDED", "z3 returned %r" % result


def load_tree_units2():
    path = os.path.join(HERE, "tree_units2.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def apply_cause123_v2(tu2_unit, canon4_lines):
    """canon7.py's apply_cause123, pointed at condition_table2's
    WIDENED flagsetter table instead of tree_match2's (condition_
    table.py's narrow one)."""
    out = dict(tu2_unit)
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return out, 0, "n/a"
    if "amd64g_calculate_condition" not in raw:
        norm, ok, note = TM2.normalize(raw)
        out["normal_path_root"] = norm
        out["normalize_ok"] = ok
        out["normalize_note"] = note
        return out, 0, "no amd64g_calculate_condition call"
    sub_text, applied, sub_note = CT2.resolve_conditions(
        raw, canon4_lines)
    norm, ok, note = TM2.normalize(sub_text)
    out["normal_path_raw"] = sub_text
    out["normal_path_root"] = norm
    out["normalize_ok"] = ok
    out["normalize_note"] = note
    return out, applied, sub_note


def convert_one(lang, n, canon4_rec, old_rec, tu2_map, canon4_docs,
                 sem_map, workdir):
    """returns None if this unit is not a candidate for re-attempt
    (copy old_rec through unchanged); otherwise a dict of the FIELDS
    TO UPDATE on top of old_rec."""
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        return None

    canon4_lines = canon4_rec.get("derived_text")
    fixed_unit, cond_applied, cond_note = apply_cause123_v2(
        tu2, canon4_lines)

    old_text = old_rec.get("canon8_text", old_rec.get("canon7_text"))

    result, context_record = R7.render_unit7(fixed_unit, workdir)
    if not isinstance(result, list):
        return None  # still refuses, for a DIFFERENT reason -- JOB 2
                      # later buckets, not this pass's target.

    candidate = "; ".join(result)
    if candidate == old_text:
        return None  # no change -- nothing to re-adjudicate

    verdict, detail = job2_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job2_cause1_v2_condition_substitutions": cond_applied,
        "job2_cause1_v2_note": cond_note,
        "job2_candidate_text": candidate,
        "job2_ground_truth_verdict": verdict,
        "job2_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon9_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 2 (condition_table2.py widened " \
            "flagsetter recognition): candidate proved equal to " \
            "the unit's own real ship code directly"
        return update

    update["canon9_text"] = old_text
    update["job2_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon8_path = os.path.join(indir, "canon8_units_%s.json" % lang)
    doc = json.load(open(canon8_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    not_applicable = 0

    for n, u in units.items():
        if u["status"] != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units[n], u, tu2_map,
                              canon4_docs, sem_map, workdir)
        if update is None:
            not_applicable += 1
            continue
        attempted += 1
        u.update(update)
        if update.get("status") == "converged":
            accepted += 1
        else:
            still_refused += 1

    doc["job2_pass1_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon9.py (JOB 2 pass 1: condition_" \
        "table2.py widened flagsetter recognition) over " \
        "canon8_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon9_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d not applicable this pass)"
          % (name, attempted, accepted, still_refused, not_applicable))
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
    print("canon9.py -- JOB 2 pass 1: widened flagsetter recognition")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = {}
    for lang in LANGS:
        path = os.path.join(indir, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]

    tu2_map = load_tree_units2()
    workdir = tempfile.mkdtemp(prefix="canon9_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job2_pass1_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
