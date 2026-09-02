#!/usr/bin/env python3
"""canon6.py -- canon5.py re-run with the four measured causes fixed.

AgentMemory's op_pipeline lap, 2026-08-28.  canon5.py measured 1,274
of 1,641 units "not yet converged" for four causes.  This file is
canon5.py's own driver (convert_one/run_language/main), unchanged in
SHAPE, with the fixes wired in at the two points canon5 delegates to:
the normalizer (tree_match2.py) and the renderer (expr_to_canon.py).
Nothing here re-implements canon5's logic; it calls the same fixed
modules canon5 would call if re-run today.

THE FOUR FIXES, each in its own file, each with its own header:
  CAUSE 2 (8-bit ops unmodeled)      -- tree_match2.py's to_z3_fixed
  CAUSE 1 (condition helper opaque)  -- condition_table.py (route a,
                                         canonical-context, primary)
                                         + tree_match2.py/expr_to_
                                         canon.py's CondXX/ite/ins@
                                         handling
  CAUSE 3 (z3 "invalid extract")     -- tree_match2.py's to_z3_fixed
                                         widen_cache (honest fresh-
                                         bits widening, never a
                                         fabricated zero)
  CAUSE 4 (branching units untouched) -- expr_to_canon.py's
                                         render_branching_unit

Per-unit flow (straight-line units): canon4 text -> (CAUSE 1)
condition_table.py substitutes any amd64g_calculate_condition call
using THIS unit's own canon4 derived_text, never the lifter -> (CAUSE
2/3-fixed) tree_match2.normalize() -> expr_to_canon.render_unit().

Per-unit flow (branching units): expr_to_canon.render_branching_unit,
which applies the SAME per-block pipeline to every ret-terminated
block's own value, keeping every other block (guards, traps, calls)
as canon4 wrote it.

THE SPELLING BAN: unchanged from canon5.py -- `operator` is copied
once per unit as the display label; no grouping/pairing anywhere in
this file. Run check_no_spelling_keys.py on the output.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon6.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2       # noqa: E402
import condition_table as CT    # noqa: E402
import expr_to_canon as EC      # noqa: E402
import canon6_behaviour_check as C6BC  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_tree_units2():
    path = os.path.join(HERE, "tree_units2.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def canon4_text_of(u):
    if isinstance(u.get("derived_text"), list):
        return u.get("derived_mnem_joined"), "straight_line"
    if "derived_blocks" in u and u.get("erasure") == "ok":
        flat = u.get("derived_text_flat") or []
        return "; ".join(flat), "branching"
    return None, None


def apply_cause123(tu2_unit, canon4_lines):
    """returns a FRESH tree_units2-shaped dict with CAUSE 1/2/3 fixes
    applied (condition substitution + re-normalize).  CAUSE 2/3 are
    unconditional normalizer fixes (always active in tree_match2.py);
    CAUSE 1's substitution only fires when the raw text actually
    contains amd64g_calculate_condition and canon4_lines is
    available."""
    out = dict(tu2_unit)
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return out, 0, "n/a"
    if "amd64g_calculate_condition" not in raw:
        # still re-normalize: CAUSE 2 (8-bit ops) / CAUSE 3 (widen
        # fix) apply unconditionally, even with no condition call.
        norm, ok, note = TM2.normalize(raw)
        out["normal_path_root"] = norm
        out["normalize_ok"] = ok
        out["normalize_note"] = note
        return out, 0, "no amd64g_calculate_condition call"
    sub_text, applied, sub_note = TM2.resolve_conditions(
        raw, canon4_lines)
    norm, ok, note = TM2.normalize(sub_text)
    out["normal_path_raw"] = sub_text
    out["normal_path_root"] = norm
    out["normalize_ok"] = ok
    out["normalize_note"] = note
    return out, applied, sub_note


def convert_one(lang, n, canon4_rec, sem_blocks, tu2_map, workdir):
    out = {}
    out["lang"] = lang
    out["n"] = n
    out["unit"] = "%s/op_%s" % (lang, n)
    out["operator"] = canon4_rec.get("operator")
    out["meta"] = canon4_rec.get("meta")

    canon4_text, kind = canon4_text_of(canon4_rec)
    if canon4_text is None:
        out["status"] = "no_canon4_text"
        out["reason"] = "canon4 itself produced no canonical text " \
            "for this unit (erasure=%r) -- nothing to converge" % \
            canon4_rec.get("erasure")
        out["canon4_text"] = None
        out["canon6_text"] = None
        out["converged"] = False
        return out

    out["branch_kind"] = kind
    out["canon4_text"] = canon4_text

    if kind == "branching":
        result = EC.render_branching_unit(
            lang, n, canon4_rec, sem_blocks or [], workdir)
        if isinstance(result, tuple):
            lines, per_block = result
            candidate = "; ".join(lines)
            out["canon6_text"] = candidate
            out["per_block_report"] = per_block
            out["cause4_applied"] = True
            if candidate != canon4_text:
                out["status"] = "converged"
                out["converged"] = True
            else:
                out["status"] = "unchanged"
                out["converged"] = False
            return out
        out["status"] = "not_yet_converged"
        out["reason"] = result
        out["canon6_text"] = canon4_text
        out["cause4_applied"] = True
        out["converged"] = False
        return out

    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        out["status"] = "not_yet_converged"
        out["reason"] = "no tree_match2 (tree_units2.json) record " \
            "for this unit -- cannot lift to an expression form"
        out["canon6_text"] = canon4_text
        out["converged"] = False
        return out

    canon4_lines = canon4_rec.get("derived_text")
    fixed_unit, cond_applied, cond_note = apply_cause123(
        tu2, canon4_lines)
    out["cause1_condition_substitutions"] = cond_applied
    out["cause1_note"] = cond_note

    result = EC.render_unit(fixed_unit, workdir)
    if isinstance(result, list):
        candidate = "; ".join(result)
        out["normalized_expression"] = fixed_unit.get(
            "normal_path_root")
        if candidate == canon4_text:
            out["canon6_text"] = candidate
            out["status"] = "unchanged"
            out["converged"] = False
            return out
        # BEHAVIOUR-PRESERVATION GATE (found necessary on c/op_678,
        # `a << b`: canon4's own derived_text for this unit reads
        # `%cl` without ever loading it in that snippet -- the real
        # disassembly does `mov %esi,%ecx` first, but the move-
        # erasure pass that produced derived_text erased that mov
        # WITHOUT substituting `%cl`'s downstream reads back to the
        # entry contract's actual `b` register, a pre-existing gap
        # AgentMemory already names ("MOVES ARE ERASED BY
        # SUBSTITUTION... NOT YET IMPLEMENTED"). This renderer
        # correctly used the entry contract's stated `b` register;
        # canon4's OWN text is the one carrying the latent defect for
        # this class of unit -- proved by cross-checking BOTH against
        # this unit's own real disassembly below, not asserted).
        # Never accept a CHANGED rendering on faith: prove it
        # behaviourally equal to canon4_text first (canon6_behaviour_
        # check.py's own checker, the SAME routine used for the
        # published behaviour-preservation report, so "accepted" and
        # "reported PROVED_EQUAL" can never silently disagree).
        verdict, detail = C6BC.check_pair(canon4_text, candidate)
        if verdict == "PROVED_EQUAL":
            out["canon6_text"] = candidate
            out["status"] = "converged"
            out["converged"] = True
            out["behaviour_gate"] = verdict
            return out
        out["status"] = "not_yet_converged"
        out["reason"] = "rendered a candidate that differs from " \
            "canon4_text but the behaviour-preservation gate did " \
            "not prove it equal (%s: %s) -- refusing rather than " \
            "risk a wrong answer" % (verdict, detail[:200])
        out["canon6_text"] = canon4_text
        out["normalized_expression"] = fixed_unit.get(
            "normal_path_root")
        out["converged"] = False
        return out

    out["status"] = "not_yet_converged"
    out["reason"] = result
    out["canon6_text"] = canon4_text
    out["normalized_expression"] = fixed_unit.get("normal_path_root")
    out["converged"] = False
    return out


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def run_language(lang, indir, outdir, workdir, tu2_map, sem_map):
    canon4_path = os.path.join(indir, "canon4_units_%s.json" % lang)
    canon4_doc = json.load(open(canon4_path))
    canon4_units = canon4_doc["units"]
    keys = sorted(canon4_units.keys(), key=lambda x: int(x))

    rows = {}
    counts = {"no_canon4_text": 0, "unchanged": 0, "converged": 0,
              "not_yet_converged": 0}
    reasons = {}

    for n in keys:
        sem_blocks = sem_map.get(lang, {}).get(n, {}) \
            .get("sem", {}).get("blocks", [])
        rec = convert_one(lang, n, canon4_units[n], sem_blocks,
                           tu2_map, workdir)
        rows[n] = rec
        counts[rec["status"]] = counts.get(rec["status"], 0) + 1
        if rec["status"] == "not_yet_converged":
            key = (rec.get("reason") or "").split(" -- ")[0]
            key = key.split(" (")[0][:90]
            reasons[key] = reasons.get(key, 0) + 1

    out = {}
    out["language"] = lang
    out["meta"] = {
        "role": "generator provenance",
        "form": "canon6: canon5 re-run with CAUSE 1/2/3/4 fixed -- "
               "condition_table.py's canonical-context route for "
               "amd64g_calculate_condition, tree_match2.py's 8-bit "
               "ops + extract-widen fix, expr_to_canon.py's block-"
               "aware branching renderer",
        "spelling": "the operator token appears once per unit, as "
                   "the display label `operator` on a unit object",
        "generator": "canon6.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                      time.gmtime()),
    }
    out["units_read"] = len(keys)
    out["counts"] = counts
    out["not_yet_converged_reasons"] = reasons
    out["units"] = rows

    name = os.path.join(outdir, "canon6_units_%s.json" % lang)
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
    log("canon6.py -- canon5 re-run, CAUSE 1/2/3/4 fixed")
    tu2_map = load_tree_units2()
    sem_map = {}
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]
    workdir = tempfile.mkdtemp(prefix="canon6_asm_")
    all_counts = {"no_canon4_text": 0, "unchanged": 0, "converged": 0,
                  "not_yet_converged": 0}
    for lang in LANGS:
        res = run_language(lang, indir, outdir, workdir, tu2_map,
                            sem_map)
        for k, v in res["counts"].items():
            all_counts[k] = all_counts.get(k, 0) + v
    log("TOTAL across all languages: %r" % all_counts)
    log("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
