#!/usr/bin/env python3
"""super_op_miner.py -- SUPER-OP CANDIDATE miner (log_081 item 3, the
ruled automation).

AgentMemory's "SEEDED GROUPING UNDER CONDITIONS" paragraph (the owner,
2026-08-29, ratified): "an idiom recurring across arch-units is the
compiler's logic, not the operator's ... Detector: the component
miner's recurrence counts x unmodelled lifter names -> super-op
candidates, modelled once by recurrence rank, so lifter/whitelist
coverage gaps surface automatically and hand-intervention is never the
process."

This is an INSTRUMENT LAP.  It does not model anything and does not
touch any existing table.  It reads:

  * canon23_units_<lang>.json (newest of the canon2x_units_* chain) --
    per unit: `converged`, and (for not-yet-converged units) a `reason`
    field (and job-stage refusal-reason fields) naming the unmodelled
    lifter op that blocked convergence.
  * tree_units3.json -- per unit: `normal_path_raw`, the lifted
    expression text, read as a second source of the same unmodelled
    names (cross-reference, not a replacement for the reason text).
  * canon4_units_<lang>.json -- per unit: `mnem`, the REAL SHIP
    disassembly (verbatim instruction text, NOT the canonical-register
    runnable form canon.py produces and component_mine2.py mines).
    This is deliberate: super-op idioms are compiler output, and the
    compiler has not yet been steered onto the a->rdi/b->rsi/answer->
    rax convention at this stage of not-yet-converged units, so mining
    canon4's `mnem` is the only way to see the idiom as the compiler
    actually wrote it, across whichever registers it picked per call
    site.

MATCHING SCOPE (per THE SPELLING BAN, verbatim below): the candidate
set for comparison is machine-form evidence only -- it is every
not-yet-converged unit, drawn by the `converged` field, never by the
operator token.  Recurring sub-sequences are found by literal
instruction-text equality after register normalization (next
paragraph); nothing about which operator a unit belongs to enters the
grouping.

REGISTER NORMALIZATION (reusing component_mine2.py's mining shape;
this file's own twist, documented because it differs from
component_mine2): component_mine2 mines `derived_text`, whose
registers are ALREADY canonical (a->%rdi, b->%rsi, answer->%rax) by
construction of canon.py's rewrite, so no renaming is needed there.
Here the material is `mnem`, RAW ship disassembly: two units running
the *same* compiler idiom can and do land on different concrete
registers (e.g. one call site's temp is %r10, another's is %r11) while
performing the identical sequence of operations.  Since positional
VALUE identity (which value a register holds) is not what is being
compared here -- only the shape of the instruction sequence -- each
unit's own register tokens are rewritten to positional placeholders
`%P0`, `%P1`, ... in order of FIRST APPEARANCE in that unit's
instruction list, one placeholder per distinct concrete register
spelling (`%eax`/%rax/%al all normalize to whichever base register
name string is used verbatim -- no width-folding is performed; a unit
using %eax and one using %rax for "the same" register are NOT folded
together, since collapsing widths is a modeling decision this
instrument lap explicitly does not make). Immediate literals, mnemonic
names, and non-register operands are left verbatim. This makes the
same idiom, played out on different temp registers at different call
sites, compare equal; it does not claim the registers ARE the same
value.

THE SPELLING BAN, verbatim as required by AgentMemory.md and by the
job brief: "No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in 'which pairs get
compared', not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the
member. MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run check_no_spelling_keys.py and refuse its own
output on failure."

This miner never reads any unit's `operator` field for grouping,
pairing, or candidate selection. The candidate set (not-yet-converged
units) comes from the `converged` boolean, a machine-form field.
Output rows never key on the operator; it does not appear anywhere in
super_op_candidates.json, not even as a display label, because rows in
this output are keyed by SUB-SEQUENCE, not by unit -- there is no
per-unit object in this line for a display label to sit on. Instead
each row lists `sample_unit_ids` (bare unit-id strings, never operator
tokens) so a human can look a unit up.

Usage:
  super_op_miner.py [--out super_op_candidates.json]
"""

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

MIN_SUPPORT = 2       # recurring sub-sequence must appear in >=2 units
MIN_LENGTH = 2         # an "idiom" is a sub-sequence, not a lone instruction

# --- unmodelled-lifter-name extraction ------------------------------------

VEX_OP_RE = re.compile(r"VEX op '([A-Za-z0-9_]+)'")
ATOMS_PAREN_RE = re.compile(r"uninterpreted atoms? \(([^)]+)\)")
CALC_HELPER_RE = re.compile(r"\b(amd64g_[A-Za-z0-9_]+)\b")
SIMD_OP_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*(?:F0x\d+|V128))\b")


def names_from_text(text):
    """Every unmodelled-lifter name mentioned in a chunk of free text,
    by the three shapes actually observed in canon23's reason fields
    and in tree_units3's normal_path_raw expressions:
      - "VEX op 'NAME'"
      - "uninterpreted atoms (NAME[, NAME2])"
      - a bare amd64g_* helper-call name
      - a bare packed-float/SIMD VEX op name (NNNF0xN / *V128 shape)
    """
    found = set()
    for m in VEX_OP_RE.finditer(text):
        found.add(m.group(1))
    for m in ATOMS_PAREN_RE.finditer(text):
        for tok in m.group(1).split(","):
            tok = tok.strip()
            if tok:
                found.add(tok)
    for m in CALC_HELPER_RE.finditer(text):
        found.add(m.group(1))
    for m in SIMD_OP_RE.finditer(text):
        found.add(m.group(1))
    return found


def unmodelled_names_for_unit(canon23_rec, tree3_rec):
    """Union of unmodelled lifter names from the unit's canon23 refusal
    reason(s) and from its tree_units3 normal_path_raw text."""
    names = set()
    names |= names_from_text(json.dumps(canon23_rec))
    if tree3_rec is not None:
        raw = tree3_rec.get("normal_path_raw") or ""
        names |= names_from_text(raw)
    return names


# --- positional register normalization ------------------------------------

REG_RE = re.compile(r"%[a-z][a-z0-9]*")


def normalize_positionally(mnem_lines):
    """Rewrite every register token in a unit's instruction list to a
    positional placeholder %P0, %P1, ... in order of first appearance
    of that EXACT token spelling within this unit. Non-register text
    (mnemonics, immediates, punctuation) is left verbatim. See module
    docstring for why no width-folding is performed."""
    order = {}
    out = []
    for line in mnem_lines:
        def sub(m):
            tok = m.group(0)
            if tok not in order:
                order[tok] = "%%P%d" % len(order)
            return order[tok]
        out.append(REG_RE.sub(sub, line))
    return out


# --- loading ---------------------------------------------------------------

def load_blocked_units():
    """Returns list of {unit, lang, n, unmodelled_names(set),
    mnem_norm(list of normalized instruction lines)} for every
    not-yet-converged unit that has both a real-ship mnem list and at
    least one unmodelled lifter name."""
    tree3 = json.load(open(os.path.join(HERE, "tree_units3.json")))["units"]
    tree3_by_key = {(r["lang"], r["n"]): r for r in tree3}

    blocked = []
    load_report = {}
    for lang in LANGS:
        c23 = json.load(open(
            os.path.join(HERE, "canon23_units_%s.json" % lang)))["units"]
        c4 = json.load(open(
            os.path.join(HERE, "canon4_units_%s.json" % lang)))["units"]
        n_total = len(c23)
        n_not_converged = 0
        n_with_mnem = 0
        n_with_names = 0
        for key, rec in c23.items():
            if rec.get("converged"):
                continue
            n_not_converged += 1
            c4rec = c4.get(key)
            if c4rec is None or not isinstance(c4rec.get("mnem"), list):
                continue
            n_with_mnem += 1
            tree3rec = tree3_by_key.get((lang, key))
            names = unmodelled_names_for_unit(rec, tree3rec)
            if not names:
                continue
            n_with_names += 1
            blocked.append({
                "unit": rec["unit"],
                "lang": lang,
                "n": key,
                "unmodelled_names": names,
                "mnem_norm": normalize_positionally(c4rec["mnem"]),
            })
        load_report[lang] = {
            "total_units_in_file": n_total,
            "not_yet_converged": n_not_converged,
            "not_yet_converged_with_mnem": n_with_mnem,
            "not_yet_converged_with_unmodelled_name": n_with_names,
        }
    return blocked, load_report


# --- mining (contiguous sub-sequence recurrence, shape reused from
#     component_mine2.py's enumerate_occurrences / recurring components) --

def enumerate_occurrences(blocked):
    occ_by_key = {}
    for ui, u in enumerate(blocked):
        steps = u["mnem_norm"]
        n = len(steps)
        for start in range(n):
            for length in range(MIN_LENGTH, n - start + 1):
                key = tuple(steps[start:start + length])
                occ_by_key.setdefault(key, []).append(ui)
    return occ_by_key


def recurring_sequences(blocked, occ_by_key):
    """Recurring (support>=2) sub-sequences, joined against which
    unmodelled names their carrier units carry."""
    rows = []
    for key, occ_uis in occ_by_key.items():
        unit_idxs = sorted(set(occ_uis))
        if len(unit_idxs) < MIN_SUPPORT:
            continue
        carriers = [blocked[ui] for ui in unit_idxs]
        blocking_names = set()
        for c in carriers:
            blocking_names |= c["unmodelled_names"]
        rows.append({
            "instructions": list(key),
            "support": len(unit_idxs),
            "languages": sorted(set(c["lang"] for c in carriers)),
            "blocking_lifter_names": sorted(blocking_names),
            "blocked_unit_count": len(unit_idxs),
            "sample_unit_ids": sorted(c["unit"] for c in carriers)[:8],
        })
    # rank by units-blocked (ties broken by support, then length, then
    # the instruction text itself for determinism -- never by operator)
    rows.sort(key=lambda r: (-r["blocked_unit_count"], -r["support"],
                              -len(r["instructions"]),
                              "\n".join(r["instructions"])))
    return rows


# --- reporting helpers -----------------------------------------------------

def all_unmodelled_name_counts(blocked):
    counts = {}
    for u in blocked:
        for name in u["unmodelled_names"]:
            counts.setdefault(name, set()).add(u["unit"])
    return {name: len(units) for name, units in counts.items()}


def run_guard(out_path):
    guard = os.path.join(HERE, "check_no_spelling_keys.py")
    proc = subprocess.run([sys.executable, guard, out_path],
                           capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(
        HERE, "super_op_candidates.json"))
    args = ap.parse_args(argv[1:])

    blocked, load_report = load_blocked_units()
    occ_by_key = enumerate_occurrences(blocked)
    rows = recurring_sequences(blocked, occ_by_key)
    name_counts = all_unmodelled_name_counts(blocked)

    doc = {
        "role": "super-op candidate instrument (log_081 item 3)",
        "evidence_class": "the tool's own testimony -- every field mined "
            "here (canon23's converged/reason, tree_units3's "
            "normal_path_raw, canon4's mnem) is a pipeline stage "
            "reporting on its own output; recurrence counts and joins "
            "computed here are forced by construction from that "
            "testimony (exact literal-text comparison after a documented, "
            "reversible register-placeholder rewrite).",
        "normalization": "positional register placeholder rewrite over "
            "real-ship mnem text (canon4_units_<lang>.json's `mnem`); see "
            "module docstring normalize_positionally() for the exact rule; "
            "no width-folding performed",
        "min_support": MIN_SUPPORT,
        "min_length_instructions": MIN_LENGTH,
        "load_report": load_report,
        "distinct_unmodelled_names": len(name_counts),
        "unmodelled_name_unit_counts": name_counts,
        "candidates": rows,
    }

    with open(args.out, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")

    rc, out, err = run_guard(args.out)
    doc["spelling_guard"] = {
        "exit_code": rc,
        "passed": rc == 0,
        "stdout_tail": out[-4000:],
        "stderr_tail": err[-2000:],
    }
    with open(args.out, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")

    print("blocked units mined: %d" % len(blocked))
    print("recurring sub-sequences (support>=%d): %d" %
          (MIN_SUPPORT, len(rows)))
    print("distinct unmodelled names: %d" % len(name_counts))
    print("spelling guard exit code: %d (%s)" %
          (rc, "PASS" if rc == 0 else "FAIL"))
    if rc != 0:
        print(out)
        print(err, file=sys.stderr)
        return 1
    print("top candidates by blocked_unit_count:")
    for r in rows[:10]:
        print("  blocked=%d support=%d langs=%s names=%s len=%d" % (
            r["blocked_unit_count"], r["support"],
            ",".join(r["languages"]), ",".join(r["blocking_lifter_names"]),
            len(r["instructions"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
