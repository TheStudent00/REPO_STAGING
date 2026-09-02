#!/usr/bin/env python3
"""component_mine.py -- compositional-matching miner (the owner, 2026-08-26 ruling).

Loads every erasure=="ok" record from canon2_units_{c,cpp,go,rust,swift}.json,
mines recurring LITERAL sub-sequences of erased-form steps ("components"),
assigns each a level by the recurrence rule (alpha = contains no smaller
recurring component; beta/gamma/... = 1 + max level of any recurring
component it contains), and writes:

  components.json    -- the library: id, level, support, literal step text,
                         which languages carry it, one level up: block-
                         sequence components for branching units.
  compositions.json   -- per unit: the component ids covering its steps, in
                          order, plus honestly-recorded residue.

THE SPELLING BAN is respected throughout: no operator token appears in any
key, grouping, pairing, row structure or comparison scope. Component ids are
K-numbers; grouping is by literal step text and by mined recurrence, never
by the `operator` field (which is not read by this program's matching logic
at all -- it only ever reads `erased_form` / `blocks[*].steps`).

NORMALIZATION (recorded, not silent): within a candidate contiguous
sub-sequence, value names matching the regex \\b[ukw][0-9]+\\b are renumbered
per-prefix in first-appearance order (u0/u1/.., k0/k1/.., w0/w1/..) so the
same computation under different absolute numbering compares equal. `a`,
`b`, `answer` are anchored identities and are NEVER renumbered. Block-target
labels (L0, L1, ...) are NOT renumbered -- the ruling that authorizes this
miner names only uN/kN/wN; L-labels are left exactly as recorded. This is a
real limitation, reported honestly below: two branching units whose guard
blocks are structurally identical but whose block labels differ in text
will not be recognized as sharing a component that includes the label-
bearing branch line, UNLESS the branch line's target label happens to
coincide. It does not affect componentws drawn from a single block's
`steps` list, since those never include the "L0:" header lines themselves.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

VALUE_NAME = re.compile(r"\b([ukw])([0-9]+)\b")


def normalize(steps):
    """renumber uN/kN/wN per-prefix in first-appearance order across this
    candidate sub-sequence. a/b/answer are untouched. Returns a tuple of
    normalized strings (hashable) plus the rename map used, for audit."""
    mapping = {}
    counters = {"u": 0, "k": 0, "w": 0}

    def repl(m):
        prefix = m.group(1)
        orig = prefix + m.group(2)
        if orig not in mapping:
            mapping[orig] = prefix + str(counters[prefix])
            counters[prefix] += 1
        return mapping[orig]

    out = []
    for s in steps:
        out.append(VALUE_NAME.sub(repl, s))
    return tuple(out), mapping


def load_units():
    """returns a list of unit records:
    {unit, lang, sequences: [{seq_id, block_label_or_None, steps}]}"""
    units = []
    stats = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon2_units_%s.json" % lang)
        doc = json.load(open(path))
        u = doc["units"]
        n_total = len(u)
        n_ok = 0
        for _k, rec in u.items():
            if rec.get("erasure") != "ok":
                continue
            n_ok += 1
            unit_id = rec["unit"]
            sequences = []
            if "blocks" in rec:
                for b in rec["blocks"]:
                    steps = b.get("steps") or []
                    if steps:
                        sequences.append({
                            "seq_id": b.get("label"),
                            "is_block": True,
                            "steps": steps,
                        })
            else:
                steps = rec.get("erased_form") or []
                if steps:
                    sequences.append({
                        "seq_id": None,
                        "is_block": False,
                        "steps": steps,
                    })
            units.append({
                "unit": unit_id,
                "lang": lang,
                "operator_label": rec.get("operator"),
                "branching": "blocks" in rec,
                "sequences": sequences,
            })
        stats[lang] = {"total_units_in_file": n_total, "erasure_ok": n_ok}
    return units, stats


def enumerate_occurrences(units):
    """for every contiguous sub-sequence of every material sequence of
    every unit, compute its normalized key. Returns:
      occ_by_key: key -> list of (unit_id, lang, seq_index, start, length)
      occ_index: (unit_idx, seq_index, start, length) -> key
    """
    occ_by_key = {}
    occ_index = {}
    for ui, u in enumerate(units):
        for si, seq in enumerate(u["sequences"]):
            steps = seq["steps"]
            n = len(steps)
            for start in range(n):
                for length in range(1, n - start + 1):
                    sub = steps[start:start + length]
                    key, _mapping = normalize(sub)
                    occ_index[(ui, si, start, length)] = key
                    occ_by_key.setdefault(key, []).append(
                        (ui, si, start, length))
    return occ_by_key, occ_index


def recurring_components(units, occ_by_key):
    """filter to keys carried by >=2 DISTINCT units. Returns dict
    key -> {support (unit count), occurrences, length}"""
    out = {}
    for key, occs in occ_by_key.items():
        unit_ids = set()
        for (ui, _si, _start, _length) in occs:
            unit_ids.add(units[ui]["unit"])
        if len(unit_ids) >= 2:
            out[key] = {
                "occurrences": occs,
                "unit_ids": unit_ids,
                "length": len(key),
            }
    return out


def assign_levels_full(units, recurring):
    """level(component) = 0 if it contains no strictly-smaller recurring
    component; else 1 + max level of any recurring component it contains.
    Containment is tested structurally: take one witness occurrence of the
    component, slice every strictly-shorter contiguous sub-span of that
    occurrence's RAW steps, renormalize, and check whether the result is
    itself a recurring key."""
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
        ui, si, start, _length = info["occurrences"][0]
        raw_steps = units[ui]["sequences"][si]["steps"][start:start + L]
        contained = set()
        for sub_start in range(L):
            for sub_len in range(1, L - sub_start + 1):
                if sub_start == 0 and sub_len == L:
                    continue
                sub = raw_steps[sub_start:sub_start + sub_len]
                sub_key, _m = normalize(sub)
                if sub_key in recurring and sub_key != key:
                    contained.add(sub_key)
        contains[key] = frozenset(contained)
        if contained:
            levels[key] = 1 + max(levels[k2] for k2 in contained)
        else:
            levels[key] = 0
    return levels, contains


def assign_component_ids(recurring, levels):
    """K-numbers ordered by (level, -support, length), ties broken by the
    literal text for determinism (never by operator token -- the text
    compared is the whole normalized step tuple, a machine form)."""
    keys = list(recurring.keys())

    def sort_key(k):
        info = recurring[k]
        return (levels[k], -len(info["unit_ids"]), info["length"],
                "\n".join(k))

    keys.sort(key=sort_key)
    ids = {}
    for i, k in enumerate(keys):
        ids[k] = "K%04d" % i
    return ids


def languages_of(recurring, units, key):
    langs = set()
    for (ui, _si, _start, _length) in recurring[key]["occurrences"]:
        langs.add(units[ui]["lang"])
    return sorted(langs)


def build_library(units, recurring, levels, comp_ids):
    rows = []
    for key, cid in sorted(comp_ids.items(), key=lambda kv: kv[1]):
        info = recurring[key]
        rows.append({
            "id": cid,
            "level": levels[key],
            "support_units": len(info["unit_ids"]),
            "length_steps": info["length"],
            "steps": list(key),
            "languages": languages_of(recurring, units, key),
            "member_unit_ids": sorted(info["unit_ids"]),
        })
    return rows


def cover_sequence(steps, comp_ids, occ_by_key_for_seq):
    """greedy longest-first, leftmost-first cover of one material sequence
    by recurring components. Returns list of {kind, component/steps,
    start, length}. occ_by_key_for_seq: dict (start,length)->key that are
    RECURRING (already filtered), for this exact sequence."""
    n = len(steps)
    covered = [False] * n
    spans = sorted(occ_by_key_for_seq.keys(), key=lambda sl: (-sl[1], sl[0]))
    picks = []
    for (start, length) in spans:
        if any(covered[start:start + length]):
            continue
        key = occ_by_key_for_seq[(start, length)]
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
                out.append({"kind": "residue", "step": steps[j]})
        out.append({"kind": "component", "id": cid, "length": length})
        n_covered += length
        i = start + length
    for j in range(i, n):
        out.append({"kind": "residue", "step": steps[j]})
    return out, n_covered


def build_compositions(units, occ_index, comp_ids):
    comps = []
    fully_covered_by_lang = {}
    total_by_lang = {}
    for ui, u in enumerate(units):
        total_by_lang[u["lang"]] = total_by_lang.get(u["lang"], 0) + 1
        seq_comps = []
        n_steps_total = 0
        n_covered_total = 0
        for si, seq in enumerate(u["sequences"]):
            n = len(seq["steps"])
            occ_for_seq = {}
            for length in range(1, n + 1):
                for start in range(0, n - length + 1):
                    key = occ_index.get((ui, si, start, length))
                    if key is not None and key in comp_ids:
                        occ_for_seq[(start, length)] = key
            cover, n_covered = cover_sequence(seq["steps"], comp_ids,
                                               occ_for_seq)
            n_steps_total += n
            n_covered_total += n_covered
            seq_comps.append({
                "seq_id": seq["seq_id"],
                "is_block": seq["is_block"],
                "cover": cover,
            })
        fully = (n_steps_total > 0 and n_covered_total == n_steps_total)
        if fully:
            fully_covered_by_lang[u["lang"]] = (
                fully_covered_by_lang.get(u["lang"], 0) + 1)
        comps.append({
            "unit": u["unit"],
            "lang": u["lang"],
            "operator": u["operator_label"],
            "branching": u["branching"],
            "sequences": seq_comps,
            "fully_covered": fully,
            "n_steps": n_steps_total,
            "n_covered": n_covered_total,
        })
    return comps, fully_covered_by_lang, total_by_lang


def main():
    units, load_stats = load_units()
    print("loaded %d erasure-ok units across %d languages" %
          (len(units), len(LANGS)))
    for lang, s in load_stats.items():
        print("  %-6s total=%-4d erasure_ok=%-4d" %
              (lang, s["total_units_in_file"], s["erasure_ok"]))

    occ_by_key, occ_index = enumerate_occurrences(units)
    print("enumerated %d distinct normalized sub-sequences "
          "(no cap needed: sum of seq-length^2 is small)" % len(occ_by_key))

    recurring = recurring_components(units, occ_by_key)
    print("of those, %d recur in >=2 distinct units" % len(recurring))

    levels, contains = assign_levels_full(units, recurring)
    by_level = {}
    for k, lv in levels.items():
        by_level[lv] = by_level.get(lv, 0) + 1
    print("levels:", sorted(by_level.items()))

    comp_ids = assign_component_ids(recurring, levels)
    library = build_library(units, recurring, levels, comp_ids)

    compositions, fully_covered_by_lang, total_by_lang = (
        build_compositions(units, occ_index, comp_ids))

    out_doc_components = {
        "meta": {
            "role": "compositional-matching component library",
            "generator": "component_mine.py",
            "ruling": "COMPOSITIONAL MATCHING (the owner, 2026-08-26)",
            "normalization": "uN/kN/wN renumbered per-prefix by "
                              "first-appearance order within each "
                              "candidate sub-sequence; a/b/answer fixed; "
                              "L-labels NOT renumbered (limitation, see "
                              "module docstring)",
            "level_definition": "level 0 (alpha) = contains no smaller "
                                 "recurring component; level N = 1 + max "
                                 "level of any recurring component it "
                                 "structurally contains",
            "spelling_ban": "no operator token used as a key anywhere in "
                             "this document; components are identified by "
                             "K-number and by literal step text mined from "
                             "erased_form/blocks[*].steps only",
        },
        "component_count": len(library),
        "components_by_level": {str(k): v for k, v in
                                 sorted(by_level.items())},
        "components": library,
    }

    out_doc_compositions = {
        "meta": {
            "role": "compositional-matching per-unit compositions",
            "generator": "component_mine.py",
        },
        "unit_count": len(compositions),
        "fully_covered_by_language": fully_covered_by_lang,
        "total_by_language": total_by_lang,
        "compositions": compositions,
    }

    comp_path = os.path.join(HERE, "components.json")
    compo_path = os.path.join(HERE, "compositions.json")
    with open(comp_path, "w") as f:
        json.dump(out_doc_components, f, indent=2)
    with open(compo_path, "w") as f:
        json.dump(out_doc_compositions, f, indent=2)
    print("wrote", comp_path)
    print("wrote", compo_path)

    return units, recurring, levels, comp_ids, library, compositions, \
        fully_covered_by_lang, total_by_lang


if __name__ == "__main__":
    main()
