#!/usr/bin/env python3
"""component_mine2.py -- compositional-matching miner, RUNNABLE-TEXT lap
(the owner's rulings of 2026-08-26, restated 2026-08-26 evening lap).

Supersedes component_mine.py.  The material mined here is the RUNNABLE
derived text (`derived_text`, real arch opcodes on the designated
registers a->%rdi/%edi.., b->%rsi/%esi.., answer->%rax..), never the
pseudo-step notation (`erased_form`, e.g. "u0 = cltd(a)").  The pseudo
notation is read ONLY to report block structure in prose/comments.

ALPHA FLOOR (ruling 2): computed from the measured opcode-mnemonic
support distribution, not hand-picked.  For every erasure-ok,
non-branching unit's derived_text, record which opcode mnemonics occur
and which (lhs_rep, rhs_rep) type-pair the unit belongs to.  For each
mnemonic, compute the fraction of the corpus's distinct type-pairs it
appears in.  Sort mnemonics by that fraction descending and take the
largest gap between consecutive values as the threshold (an elbow cut,
not a hardcoded number) -- everything above the gap is SCAFFOLDING,
everything below is DISCRIMINATING.  The alpha of a unit is its
discriminating-opcode instruction line(s) on the traced registers;
hardware-welded feeder pairs (ruling 3: cltd/cqto -> idiv/imul, tested
by co-occurrence) travel as one two-line alpha.

COMPONENTS ABOVE ALPHA (ruling 4): recurring contiguous sub-sequences
of a unit's derived_text list (literal instruction-line equality --
registers are ALREADY standardized by the canonical runnable form, so
no uN/kN renumbering is needed or performed here, unlike
component_mine.py's pseudo-notation renumbering).  A component must
CONTAIN at least one alpha instruction line to count as a component;
scaffolding-only recurring sequences are never components (residue).
Level: alpha=0; level = 1 + max level of any strictly-smaller
recurring, alpha-containing component it structurally contains.

MATERIAL POPULATION AND HONEST SKIPS: only erasure=="ok" AND
non-branching (derived_text is a list) units are mined.  Branching
units (blocks present) have derived_text refused upstream
("not derived this slice: ...") -- per-block derived instructions are
NOT present in canon2_units_*.json (checked: blocks[*].steps carry
only pseudo-notation), so per ruling 4 ("else skip that unit with an
honest count") those units are SKIPPED here, counted and reported by
reason, not silently dropped.  Units whose erasure itself was refused
upstream (join conflicts) are likewise skipped and counted.

THE SPELLING BAN is respected: components.json rows are keyed by
K-number and literal instruction text; compositions.json per-unit rows
carry `operator` only on a UNIT OBJECT (lang + unit id present, the
one place the token is a display label), mirroring component_mine.py's
already-passing shape.  Run check_no_spelling_keys.py on both outputs.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

MNEM_RE = re.compile(r"^\s*([a-zA-Z][a-zA-Z0-9]*)")

# hardware-welded feeder mnemonics (ruling 3): tested by co-occurrence,
# not asserted -- see feeder_pairing() below. This is the CANDIDATE list
# of feeder-shaped mnemonics to test; whether each actually welds is a
# measured co-occurrence fraction, reported in the acceptance answer.
FEEDER_CANDIDATES = {"cltd", "cqto", "cwtl", "cbtw"}


def mnem_of(line):
    m = MNEM_RE.match(line)
    return m.group(1) if m else line.strip()


def load_units():
    """Returns (units, load_stats, skip_counts).
    units: list of {unit, lang, operator_label, type_pair, steps}
      -- only erasure=="ok" non-branching units with a derived_text list.
    skip_counts: {lang: {reason: count}}
    """
    units = []
    load_stats = {}
    skip_counts = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon2_units_%s.json" % lang)
        doc = json.load(open(path))
        u = doc["units"]
        n_total = len(u)
        n_ok_nonbranch = 0
        skips = {}
        for _k, rec in u.items():
            erasure = rec.get("erasure")
            branching = "blocks" in rec
            dt = rec.get("derived_text")
            if erasure != "ok":
                skips["erasure_refused: %s" % erasure] = (
                    skips.get("erasure_refused: %s" % erasure, 0) + 1)
                continue
            if branching or not isinstance(dt, list):
                reason = ("branching-no-per-block-derived-instructions"
                          if branching else
                          "erasure-ok-but-derived_text-not-a-list")
                skips[reason] = skips.get(reason, 0) + 1
                continue
            n_ok_nonbranch += 1
            meta = rec.get("meta") or {}
            type_pair = (meta.get("lhs_rep"), meta.get("rhs_rep"))
            units.append({
                "unit": rec["unit"],
                "lang": lang,
                "operator_label": rec.get("operator"),
                "type_pair": type_pair,
                "steps": list(dt),
            })
        load_stats[lang] = {
            "total_units_in_file": n_total,
            "mined_ok_nonbranching": n_ok_nonbranch,
        }
        skip_counts[lang] = skips
    return units, load_stats, skip_counts


def alpha_floor(units):
    """Returns (scaffolding_set, discriminating_set, stat_rows, threshold,
    gap_index) computed from the measured support distribution."""
    type_pairs_all = set(u["type_pair"] for u in units)
    n_type_pairs = len(type_pairs_all)
    mnem_type_pairs = {}
    mnem_unit_count = {}
    for u in units:
        seen_here = set()
        for line in u["steps"]:
            mn = mnem_of(line)
            seen_here.add(mn)
        for mn in seen_here:
            mnem_type_pairs.setdefault(mn, set()).add(u["type_pair"])
            mnem_unit_count[mn] = mnem_unit_count.get(mn, 0) + 1

    rows = []
    for mn, tps in mnem_type_pairs.items():
        frac = len(tps) / n_type_pairs if n_type_pairs else 0.0
        rows.append({
            "mnemonic": mn,
            "type_pair_span": len(tps),
            "type_pair_fraction": frac,
            "unit_support": mnem_unit_count[mn],
        })
    rows.sort(key=lambda r: (-r["type_pair_fraction"], -r["unit_support"],
                              r["mnemonic"]))

    # elbow cut: largest gap between consecutive fractions
    best_gap = -1.0
    gap_idx = 0
    for i in range(len(rows) - 1):
        gap = rows[i]["type_pair_fraction"] - rows[i + 1]["type_pair_fraction"]
        if gap > best_gap:
            best_gap = gap
            gap_idx = i + 1  # rows[0:gap_idx] = scaffolding, rows[gap_idx:] = discriminating
    threshold = (rows[gap_idx - 1]["type_pair_fraction"] +
                 rows[gap_idx]["type_pair_fraction"]) / 2 if rows else 0.0

    scaffolding = set(r["mnemonic"] for r in rows[:gap_idx])
    discriminating = set(r["mnemonic"] for r in rows[gap_idx:])
    return scaffolding, discriminating, rows, threshold, gap_idx, n_type_pairs


def feeder_pairing(units, discriminating):
    """For each feeder candidate present as a mnemonic in the corpus,
    measure: of the units whose derived_text contains that feeder
    mnemonic, what fraction have an idiv/imul mnemonic immediately
    following it (same unit, feeder line directly followed by an idiv-
    family line)? Returns dict feeder -> {partner, n_with_feeder,
    n_immediately_paired, fraction, welded(bool)}."""
    out = {}
    idiv_family = {"idiv", "idivl", "idivq", "div"}
    for u in units:
        for i, line in enumerate(u["steps"]):
            mn = mnem_of(line)
            if mn in FEEDER_CANDIDATES:
                rec = out.setdefault(mn, {"n_with_feeder": 0,
                                           "n_immediately_paired": 0,
                                           "partner_mnems": {}})
                rec["n_with_feeder"] += 1
                if i + 1 < len(u["steps"]):
                    nxt = mnem_of(u["steps"][i + 1])
                    if nxt in idiv_family:
                        rec["n_immediately_paired"] += 1
                        rec["partner_mnems"][nxt] = (
                            rec["partner_mnems"].get(nxt, 0) + 1)
    result = {}
    for feeder, rec in out.items():
        frac = (rec["n_immediately_paired"] / rec["n_with_feeder"]
                if rec["n_with_feeder"] else 0.0)
        result[feeder] = {
            "n_with_feeder": rec["n_with_feeder"],
            "n_immediately_paired": rec["n_immediately_paired"],
            "fraction": frac,
            "partner_mnems": rec["partner_mnems"],
            "welded": frac >= 0.95,
        }
    return result


FUSED_SEP = " ; "  # marks a hardware-welded feeder+partner fused into one
                    # atomic alpha line (ruling 3), never used as a key


def fuse_welded_pairs(units, welded_feeders, idiv_family):
    """Ruling 3: a feeder hard-wired to its partner (cltd/cqto -> idiv)
    travels WITH its discriminating opcode as ONE alpha. Mechanically this
    is realized by fusing the adjacent [feeder, partner] instruction pair
    into a single atomic instruction-text entry (joined by FUSED_SEP)
    BEFORE mining, so the pair can never be pulled apart into a
    smaller/larger relationship with either half alone -- it IS the
    alpha, level 0, not a composition. This is a literal-text transform
    on machine instructions, not a token-spelling grouping."""
    fused_count = 0
    for u in units:
        steps = u["steps"]
        out = []
        i = 0
        n = len(steps)
        while i < n:
            if (i + 1 < n and mnem_of(steps[i]) in welded_feeders and
                    mnem_of(steps[i + 1]) in idiv_family):
                out.append(steps[i] + FUSED_SEP + steps[i + 1])
                fused_count += 1
                i += 2
            else:
                out.append(steps[i])
                i += 1
        u["steps"] = out
    return fused_count


def line_is_alpha(line, discriminating):
    if FUSED_SEP in line:
        return True  # a welded feeder+partner pair is always the alpha
    return mnem_of(line) in discriminating


def enumerate_occurrences(units):
    occ_by_key = {}
    occ_index = {}
    for ui, u in enumerate(units):
        steps = u["steps"]
        n = len(steps)
        for start in range(n):
            for length in range(1, n - start + 1):
                key = tuple(steps[start:start + length])
                occ_index[(ui, start, length)] = key
                occ_by_key.setdefault(key, []).append((ui, start, length))
    return occ_by_key, occ_index


def recurring_alpha_components(units, occ_by_key, discriminating):
    out = {}
    for key, occs in occ_by_key.items():
        if not any(line_is_alpha(l, discriminating) for l in key):
            continue  # scaffolding-only: never a component
        unit_ids = set(units[ui]["unit"] for (ui, _s, _l) in occs)
        if len(unit_ids) >= 2:
            out[key] = {"occurrences": occs, "unit_ids": unit_ids,
                        "length": len(key)}
    return out


def assign_levels(units, recurring):
    keys_by_length = sorted(recurring.keys(), key=lambda k: len(k))
    levels = {}
    contains = {}
    for key in keys_by_length:
        info = recurring[key]
        L = info["length"]
        if L == 1:
            levels[key] = 0
            contains[key] = frozenset()
            continue
        ui, start, _length = info["occurrences"][0]
        raw = units[ui]["steps"][start:start + L]
        contained = set()
        for sub_start in range(L):
            for sub_len in range(1, L - sub_start + 1):
                if sub_start == 0 and sub_len == L:
                    continue
                sub_key = tuple(raw[sub_start:sub_start + sub_len])
                if sub_key in recurring and sub_key != key:
                    contained.add(sub_key)
        contains[key] = frozenset(contained)
        levels[key] = (1 + max(levels[k2] for k2 in contained)
                       if contained else 0)
    return levels, contains


def assign_component_ids(recurring, levels):
    keys = list(recurring.keys())

    def sort_key(k):
        info = recurring[k]
        return (levels[k], -len(info["unit_ids"]), info["length"],
                "\n".join(k))

    keys.sort(key=sort_key)
    return {k: "K2%04d" % i for i, k in enumerate(keys)}


def languages_of(recurring, units, key):
    return sorted(set(units[ui]["lang"] for (ui, _s, _l) in
                       recurring[key]["occurrences"]))


def build_library(units, recurring, levels, comp_ids, discriminating):
    rows = []
    for key, cid in sorted(comp_ids.items(), key=lambda kv: kv[1]):
        info = recurring[key]
        rows.append({
            "id": cid,
            "level": levels[key],
            "support_units": len(info["unit_ids"]),
            "length_instructions": info["length"],
            "instructions": list(key),
            "alpha_lines": [l for l in key
                           if line_is_alpha(l, discriminating)],
            "languages": languages_of(recurring, units, key),
            "member_unit_ids": sorted(info["unit_ids"]),
        })
    return rows


def cover_sequence(steps, comp_ids, occ_for_seq, discriminating):
    n = len(steps)
    covered = [False] * n
    spans = sorted(occ_for_seq.keys(), key=lambda sl: (-sl[1], sl[0]))
    picks = []
    for (start, length) in spans:
        if any(covered[start:start + length]):
            continue
        key = occ_for_seq[(start, length)]
        cid = comp_ids.get(key)
        if cid is None:
            continue
        picks.append((start, length, cid))
        for i in range(start, start + length):
            covered[i] = True
    picks.sort(key=lambda p: p[0])
    out = []
    i = 0
    n_covered = 0
    for (start, length, cid) in picks:
        if start > i:
            for j in range(i, start):
                kind = ("unique" if line_is_alpha(steps[j], discriminating)
                        else "scaffolding")
                out.append({"kind": "residue", "residue_kind": kind,
                            "instruction": steps[j]})
        out.append({"kind": "component", "id": cid, "length": length})
        n_covered += length
        i = start + length
    for j in range(i, n):
        kind = ("unique" if line_is_alpha(steps[j], discriminating)
                else "scaffolding")
        out.append({"kind": "residue", "residue_kind": kind,
                    "instruction": steps[j]})
    return out, n_covered


def build_compositions(units, occ_index, comp_ids, discriminating):
    comps = []
    fully_covered_by_lang = {}
    residue_only_scaffolding_by_lang = {}
    total_by_lang = {}
    for ui, u in enumerate(units):
        total_by_lang[u["lang"]] = total_by_lang.get(u["lang"], 0) + 1
        n = len(u["steps"])
        occ_for_seq = {}
        for length in range(1, n + 1):
            for start in range(0, n - length + 1):
                key = occ_index.get((ui, start, length))
                if key is not None and key in comp_ids:
                    occ_for_seq[(start, length)] = key
        cover, n_covered = cover_sequence(u["steps"], comp_ids, occ_for_seq,
                                          discriminating)
        fully = (n > 0 and n_covered == n)
        residue_kinds = set(c["residue_kind"] for c in cover
                            if c["kind"] == "residue")
        residue_only_scaffolding = (residue_kinds <= {"scaffolding"})
        if fully:
            fully_covered_by_lang[u["lang"]] = (
                fully_covered_by_lang.get(u["lang"], 0) + 1)
        if residue_only_scaffolding:
            residue_only_scaffolding_by_lang[u["lang"]] = (
                residue_only_scaffolding_by_lang.get(u["lang"], 0) + 1)
        comps.append({
            "unit": u["unit"],
            "lang": u["lang"],
            "operator": u["operator_label"],
            "cover": cover,
            "fully_covered": fully,
            "residue_only_scaffolding": residue_only_scaffolding,
            "n_instructions": n,
            "n_covered": n_covered,
        })
    return (comps, fully_covered_by_lang, residue_only_scaffolding_by_lang,
            total_by_lang)


def main():
    units, load_stats, skip_counts = load_units()
    print("mined population (erasure-ok, non-branching, derived_text "
          "list): %d units" % len(units))
    for lang, s in load_stats.items():
        print("  %-6s total_in_file=%-4d mined=%-4d skipped=%s" %
              (lang, s["total_units_in_file"], s["mined_ok_nonbranching"],
               skip_counts[lang]))

    scaffolding, discriminating, stat_rows, threshold, gap_idx, n_tp = (
        alpha_floor(units))
    print("\nALPHA FLOOR: %d distinct type-pairs in mined corpus" % n_tp)
    print("elbow gap at rank %d, threshold fraction=%.4f" %
          (gap_idx, threshold))
    print("scaffolding (%d): %s" %
          (len(scaffolding), sorted(scaffolding)))
    print("discriminating (%d): %s" %
          (len(discriminating), sorted(discriminating)))

    feeders = feeder_pairing(units, discriminating)
    print("\nFEEDER PAIRING (ruling 3):")
    for f, info in sorted(feeders.items()):
        print("  %s: n_with_feeder=%d n_immediately_paired=%d "
              "fraction=%.4f welded=%s partners=%s" %
              (f, info["n_with_feeder"], info["n_immediately_paired"],
               info["fraction"], info["welded"], info["partner_mnems"]))

    idiv_family = {"idiv", "idivl", "idivq", "div"}
    welded_feeders = set(f for f, info in feeders.items() if info["welded"])
    n_fused = fuse_welded_pairs(units, welded_feeders, idiv_family)
    print("\nfused %d welded feeder+partner pairs into single atomic "
          "alpha instructions (welded feeders: %s)" %
          (n_fused, sorted(welded_feeders)))

    occ_by_key, occ_index = enumerate_occurrences(units)
    recurring = recurring_alpha_components(units, occ_by_key, discriminating)
    print("\n%d distinct instruction sub-sequences contain >=1 alpha and "
          "recur in >=2 units" % len(recurring))

    levels, contains = assign_levels(units, recurring)
    by_level = {}
    for k, lv in levels.items():
        by_level[lv] = by_level.get(lv, 0) + 1
    print("levels:", sorted(by_level.items()))

    comp_ids = assign_component_ids(recurring, levels)
    library = build_library(units, recurring, levels, comp_ids,
                            discriminating)

    (compositions, fully_covered_by_lang, residue_only_scaffolding_by_lang,
     total_by_lang) = build_compositions(units, occ_index, comp_ids,
                                         discriminating)

    out_components = {
        "meta": {
            "role": "compositional-matching component library (runnable "
                    "derived_text lap)",
            "generator": "component_mine2.py",
            "ruling": "COMPOSITIONAL MATCHING + ALPHA FLOOR + CANONICAL "
                      "RUNNABLE FORM (the owner, 2026-08-26)",
            "material": "derived_text (runnable arch opcodes on "
                        "designated registers), one opcode per stored "
                        "instruction line; erased_form/blocks pseudo-"
                        "notation is NOT mined, comments only",
            "alpha_floor_statistic": "type_pair_fraction = distinct "
                                     "(lhs_rep,rhs_rep) type-pairs an "
                                     "opcode mnemonic appears in, divided "
                                     "by total distinct type-pairs in the "
                                     "mined corpus; threshold = midpoint "
                                     "of the largest gap between "
                                     "consecutive fractions (elbow cut, "
                                     "not hand-picked)",
            "alpha_floor_threshold": threshold,
            "alpha_floor_gap_rank": gap_idx,
            "n_type_pairs_in_corpus": n_tp,
            "scaffolding_mnemonics": sorted(scaffolding),
            "discriminating_mnemonics": sorted(discriminating),
            "feeder_pairing": feeders,
            "level_definition": "level 0 (alpha) = contains no smaller "
                                "recurring alpha-containing component; "
                                "level N = 1 + max level of any such "
                                "component structurally contained. Every "
                                "component must contain >=1 discriminating"
                                "-opcode instruction line (scaffolding-"
                                "only sequences are never components).",
            "spelling_ban": "no operator token used as a key, grouping, "
                            "pairing, row structure or comparison scope "
                            "anywhere in this document; components are "
                            "identified by K-number and literal "
                            "instruction text mined from derived_text "
                            "only",
        },
        "component_count": len(library),
        "components_by_level": {str(k): v for k, v in sorted(by_level.items())},
        "components": library,
    }

    out_compositions = {
        "meta": {
            "role": "compositional-matching per-unit compositions "
                    "(runnable derived_text lap)",
            "generator": "component_mine2.py",
        },
        "unit_count": len(compositions),
        "fully_covered_by_language": fully_covered_by_lang,
        "residue_only_scaffolding_by_language":
            residue_only_scaffolding_by_lang,
        "total_by_language": total_by_lang,
        "skip_counts_by_language": skip_counts,
        "load_stats": load_stats,
        "compositions": compositions,
    }

    comp_path = os.path.join(HERE, "components2.json")
    compo_path = os.path.join(HERE, "compositions2.json")
    with open(comp_path, "w") as f:
        json.dump(out_components, f, indent=2)
    with open(compo_path, "w") as f:
        json.dump(out_compositions, f, indent=2)
    print("\nwrote", comp_path)
    print("wrote", compo_path)

    return (units, recurring, levels, comp_ids, library, compositions,
            fully_covered_by_lang, total_by_lang, stat_rows, feeders,
            skip_counts)


if __name__ == "__main__":
    main()
