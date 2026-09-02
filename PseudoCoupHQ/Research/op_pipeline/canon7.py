#!/usr/bin/env python3
"""canon7.py -- canon5's renderer, WITH ITS CONTEXT, CAUSE 1/2/3/4
salvaged from canon6, canon6's renderer regressions NOT carried.

AgentMemory's op_pipeline lap, 2026-08-29 ("the owner's diagnosis": the
return path fails because THE EXPRESSION TRAVELS WITHOUT ITS CONTEXT).
This file is canon5.py's own driver shape (convert_one/run_language/
main, unchanged), pointed at TWO upstream fixes and one new renderer:

  SALVAGED FROM CANON6 (per the brief -- "canon6's two real gains"):
    * condition_table.py's canonical-context route for the lifter's
      opaque amd64g_calculate_condition helper (CAUSE 1) -- applied
      the same way canon6.py's own `apply_cause123` did: substituted
      into a unit's raw VEX text using THAT UNIT'S OWN canon4
      derived_text, never the lifter's numeric cc/op arguments.
    * tree_match2.py's 8-bit VEX operation entries + extract-widen
      fix (CAUSE 2/3) -- these are UNCONDITIONAL in tree_match2.py's
      current to_z3_fixed (not something this file re-applies), but
      tree_units2.json ON DISK predates them (verified empirically:
      c/op_5's stored normal_path_root is the bare opaque atom `op_2`;
      re-running TM2.normalize() on the SAME raw text today yields a
      real expression, `atom_0 ^ Extract(7,0,atom_1)`) -- so this file
      re-normalizes every unit's raw text through the CURRENT
      tree_match2.py, exactly as canon6.py's apply_cause123 already
      did, rather than trusting the stale stored root.

  NOT CARRIED FROM CANON6: canon6.py's own renderer changes are not
  reused at all -- canon7 imports canon7_render.py (this lap's fresh
  copy of canon5's renderer, expr_to_canon.py, WITH the context-record
  fix) instead of expr_to_canon.py's Pool/gen/render_unit directly.
  The three measured canon6 regressions (temp-pool cap, 8-bit refusal,
  assembly failures) do not reproduce against canon7_render.py -- see
  that file's header for the diagnosis and fix of each, and this
  file's own generated report for the counts.

THE BEHAVIOUR GATE (mandatory, per this lap's brief): every unit whose
freshly-rendered candidate text differs from its PREVIOUS canonical
text (canon5_units_<lang>.json's own `canon5_text` -- the last
GOOD/ratified state, chosen as the baseline rather than canon4_text
because canon5 is what AgentMemory and the brief both name as "the
good state") is z3-proved equivalent (canon7_behaviour_check.py) before
being written. DISPROVED or UNDECIDED -> the OLD (canon5) text is kept
and the unit is recorded "not_yet_converged" with the disproof/
undecided reason; a DISPROVED pair is additionally cross-checked
against the unit's own real disassembly (canon4's own `mnem`), and
that ground-truth verdict is recorded too, never silently dropped.

THE CONTEXT RECORD travels on every unit this file renders fresh (see
canon7_render.py's own header for its exact fields) and is copied
into this file's own output as `context_record`, so a reader can see
what the render actually assumed without re-deriving it.

THE SPELLING BAN: unchanged -- `operator` is copied once per unit as
the display label; this file's own OUTPUT ROOT declares the same
`"meta": {"role": "generator provenance"}` exemption canon4/5/6.py
declare. Run check_no_spelling_keys.py on the output; it must pass.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon7.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2                                      # noqa: E402
import condition_table as CT                                   # noqa: E402
import canon7_render as R7                                      # noqa: E402
import canon7_behaviour_check as BC7                            # noqa: E402

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
    """CAUSE 1/2/3, salvaged from canon6.py's own function of the
    same name, unchanged in logic: re-normalize through the CURRENT
    tree_match2.py (CAUSE 2/3, unconditional there) and, when the raw
    text carries an amd64g_calculate_condition call, substitute it via
    condition_table.py's canonical-context route (CAUSE 1) using this
    unit's own canon4 derived_text before normalizing."""
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
    sub_text, applied, sub_note = TM2.resolve_conditions(
        raw, canon4_lines)
    norm, ok, note = TM2.normalize(sub_text)
    out["normal_path_raw"] = sub_text
    out["normal_path_root"] = norm
    out["normalize_ok"] = ok
    out["normalize_note"] = note
    return out, applied, sub_note


def assembly_failure_key(reason):
    """groups an assembly-failure reason string by the assembler's
    OWN message (item 3 of the brief: capture the assembler's actual
    messages, group by complaint). The reason has the shape
    "no return path: rendered instructions failed to assemble
    (<as stderr>); rendered lines were: ...".  The grouping key is the
    <as stderr> text, normalized to drop the one thing that varies
    per-unit inside it (the source line number, "u.s:N:")."""
    marker = "failed to assemble ("
    i = reason.find(marker)
    if i < 0:
        return None
    j = reason.find("); rendered lines were:", i)
    if j < 0:
        j = len(reason)
    msg = reason[i + len(marker):j]
    import re as _re
    msg = _re.sub(r"u\.s:\d+:", "u.s:N:", msg)
    return msg.strip()


def convert_one(lang, n, canon4_rec, canon5_rec, sem_blocks, tu2_map,
                 workdir):
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
        out["canon5_text"] = None
        out["canon7_text"] = None
        out["converged"] = False
        return out

    out["branch_kind"] = kind
    out["canon4_text"] = canon4_text
    old_text = (canon5_rec or {}).get("canon5_text", canon4_text)
    out["canon5_text"] = old_text

    if kind == "branching":
        result = R7.render_branching_unit7(
            lang, n, canon4_rec, sem_blocks or [], workdir,
            BC7.check_pair)
        lines_or_reason, contexts = result
        if isinstance(lines_or_reason, tuple):
            lines, per_block = lines_or_reason
            candidate = "; ".join(lines)
            out["canon7_text"] = candidate
            out["per_block_report"] = per_block
            out["context_records"] = contexts
            out["cause4_applied"] = True
            if candidate != old_text:
                out["status"] = "converged"
                out["converged"] = True
            else:
                out["status"] = "unchanged"
                out["converged"] = False
            return out
        out["status"] = "not_yet_converged"
        out["reason"] = lines_or_reason
        out["canon7_text"] = old_text
        out["cause4_applied"] = True
        out["converged"] = False
        return out

    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        out["status"] = "not_yet_converged"
        out["reason"] = "no tree_match2 (tree_units2.json) record " \
            "for this unit -- cannot lift to an expression form"
        out["canon7_text"] = old_text
        out["converged"] = False
        return out

    canon4_lines = canon4_rec.get("derived_text")
    fixed_unit, cond_applied, cond_note = apply_cause123(
        tu2, canon4_lines)
    out["cause1_condition_substitutions"] = cond_applied
    out["cause1_note"] = cond_note

    result, context_record = R7.render_unit7(fixed_unit, workdir)
    if isinstance(result, list):
        candidate = "; ".join(result)
        out["normalized_expression"] = fixed_unit.get(
            "normal_path_root")
        out["context_record"] = context_record
        if candidate == old_text:
            out["canon7_text"] = candidate
            out["status"] = "unchanged"
            out["converged"] = False
            return out
        verdict, detail = BC7.check_pair(old_text, candidate)
        if verdict == "PROVED_EQUAL":
            out["canon7_text"] = candidate
            out["status"] = "converged"
            out["converged"] = True
            out["behaviour_gate"] = verdict
            return out
        # DISPROVED or UNDECIDED -- KEEP THE OLD TEXT, record why.
        gt = None
        if verdict == "DISPROVED":
            canon4_docs_for_gt = {lang: _CANON4_DOCS[lang]}
            gt = BC7.ground_truth_check(
                lang, n, canon4_docs_for_gt, old_text, candidate)
        out["status"] = "not_yet_converged"
        out["reason"] = "rendered a candidate that differs from " \
            "the previous canonical text but the behaviour-" \
            "preservation gate did not prove it equal (%s: %s) -- " \
            "keeping the old text rather than risk a wrong answer" \
            % (verdict, detail[:200])
        out["behaviour_gate"] = verdict
        out["behaviour_gate_detail"] = detail
        out["ground_truth_check"] = gt
        out["rejected_candidate_text"] = candidate
        out["canon7_text"] = old_text
        out["converged"] = False
        return out

    out["status"] = "not_yet_converged"
    out["reason"] = result
    out["canon7_text"] = old_text
    out["normalized_expression"] = fixed_unit.get("normal_path_root")
    out["converged"] = False
    key = assembly_failure_key(result)
    if key is not None:
        out["assembly_failure_key"] = key
    return out


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


_CANON4_DOCS = {}


def run_language(lang, indir, outdir, workdir, tu2_map, sem_map):
    canon4_path = os.path.join(indir, "canon4_units_%s.json" % lang)
    canon5_path = os.path.join(indir, "canon5_units_%s.json" % lang)
    canon4_doc = json.load(open(canon4_path))
    canon5_doc = json.load(open(canon5_path))
    canon4_units = canon4_doc["units"]
    canon5_units = canon5_doc["units"]
    _CANON4_DOCS[lang] = canon4_units
    keys = sorted(canon4_units.keys(), key=lambda x: int(x))

    rows = {}
    counts = {"no_canon4_text": 0, "unchanged": 0, "converged": 0,
              "not_yet_converged": 0}
    reasons = {}
    assembly_failures = {}
    behaviour_gate_tally = {"PROVED_EQUAL": 0, "DISPROVED": 0,
                             "UNDECIDED": 0}

    for n in keys:
        sem_blocks = sem_map.get(lang, {}).get(n, {}) \
            .get("sem", {}).get("blocks", [])
        rec = convert_one(lang, n, canon4_units[n], canon5_units.get(n),
                           sem_blocks, tu2_map, workdir)
        rows[n] = rec
        counts[rec["status"]] = counts.get(rec["status"], 0) + 1
        if rec.get("behaviour_gate"):
            behaviour_gate_tally[rec["behaviour_gate"]] = \
                behaviour_gate_tally.get(rec["behaviour_gate"], 0) + 1
        if rec["status"] == "not_yet_converged":
            key = (rec.get("reason") or "").split(" -- ")[0]
            key = key.split(" (")[0][:90]
            reasons[key] = reasons.get(key, 0) + 1
        if rec.get("assembly_failure_key"):
            k = rec["assembly_failure_key"]
            assembly_failures[k] = assembly_failures.get(k, 0) + 1

    out = {}
    out["language"] = lang
    out["meta"] = {
        "role": "generator provenance",
        "form": "canon7: canon5's renderer (expr_to_canon.py, via "
               "canon7_render.py's context-record fix) with CAUSE "
               "1/2/3/4 salvaged from canon6 (condition_table.py's "
               "canonical-context route + tree_match2.py's 8-bit/"
               "extract-widen fixes + a block-aware branching "
               "renderer) -- canon6's OWN renderer changes are not "
               "reused; canon7_render.py fixes the temp-pool cap, "
               "8/16-bit answer refusal, and two verbose-rendering "
               "defects found while tracing canon6's regressions",
        "spelling": "the operator token appears once per unit, as "
                   "the display label `operator` on a unit object",
        "generator": "canon7.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                      time.gmtime()),
        "behaviour_gate_baseline": "canon5_units_<lang>.json's own "
                                  "canon5_text -- the previous "
                                  "canonical text a changed unit "
                                  "must be proved equal to before "
                                  "the new text is written",
    }
    out["units_read"] = len(keys)
    out["counts"] = counts
    out["not_yet_converged_reasons"] = reasons
    out["assembly_failure_groups"] = assembly_failures
    out["behaviour_gate_tally"] = behaviour_gate_tally
    out["units"] = rows

    name = os.path.join(outdir, "canon7_units_%s.json" % lang)
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
    log("canon7.py -- the context-carrying convergence engine")
    tu2_map = load_tree_units2()
    sem_map = {}
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]
    workdir = tempfile.mkdtemp(prefix="canon7_asm_")
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
