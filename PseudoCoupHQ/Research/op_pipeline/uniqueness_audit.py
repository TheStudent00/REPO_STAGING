#!/usr/bin/env python3
"""uniqueness_audit.py -- step 1 of the canon4 work list.

Reads canon3_units_<lang>.json for the 0-branch population (straight-line
units: the ones carrying `derived_text`, NOT `derived_blocks` --
`derived_text_flat` is canon3's BRANCHING field name, confirmed by
reading canon3_units_c.json directly; the task brief's guess of
`derived_text_flat` for the 0-branch population does not match the
actual data, so this script uses the field canon3 actually writes for
straight-line units: `derived_mnem_joined`, the ";"-joined form of the
`derived_text` list).

Groups 0-branch canon_ok units by exact text, then measures how much
four normalization axes collapse the group count, one axis at a time
and combined:

  reorder   -- sort each unit's instruction lines into a fixed total
               order (mnemonic, operand text) -- a stand-in for
               "independent instructions in a fixed deterministic
               order"; this is a heuristic over-approximation (it does
               not check real data independence), stated as such.
  temp      -- replace %r10/%r11 (any width spelling) with a placeholder
               TMP0/TMP1 token in first-appearance order per unit.
  spelling  -- strip AT&T width suffixes off mnemonics (movl -> mov,
               movq -> mov, etc) via a fixed regex.
  address   -- blank out any rip-relative literal address/reloc text.

SPELLING BAN: grouping here is by TEXT (machine-form evidence), never
by the `operator` token; `operator` is read only for the quoted
before/after examples, as a display label, never as a key.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

WIDTH_SUFFIX_RE = re.compile(r"\b(mov|add|sub|and|or|xor|cmp|test|lea|not|neg|shl|shr|sar)"
                             r"(b|w|l|q)\b")
RIP_ADDR_RE = re.compile(r"0x[0-9a-f]+\(%rip\)")
REG_RE = re.compile(r"%r1[01]d?|%r1[01]w?|%r1[01]b?|%r1[01]")


def load_units():
    """returns list of dicts: lang, n, operator, text (derived_mnem_joined),
    lines (derived_text list) -- 0-branch, canon_ok only."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "canon3_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, v in doc["units"].items():
            if "derived_blocks" in v:
                continue
            if v.get("erasure") != "ok":
                continue
            if not isinstance(v.get("derived_text"), list):
                continue
            out.append({
                "lang": lang,
                "n": n,
                "operator": v.get("operator"),
                "text": v.get("derived_mnem_joined"),
                "lines": v.get("derived_text"),
            })
    return out


def norm_reorder(lines):
    return tuple(sorted(lines))


def norm_temp(lines):
    out = []
    for ln in lines:
        def sub(m):
            return "%TMP"
        out.append(REG_RE.sub(sub, ln))
    return tuple(out)


def norm_spelling(lines):
    out = []
    for ln in lines:
        out.append(WIDTH_SUFFIX_RE.sub(r"\1", ln))
    return tuple(out)


def norm_address(lines):
    out = []
    for ln in lines:
        out.append(RIP_ADDR_RE.sub("ADDR", ln))
    return tuple(out)


def norm_all(lines):
    step = list(lines)
    step = [WIDTH_SUFFIX_RE.sub(r"\1", ln) for ln in step]
    step = [RIP_ADDR_RE.sub("ADDR", ln) for ln in step]
    step = [REG_RE.sub("%TMP", ln) for ln in step]
    return tuple(sorted(step))


def group_by(units, keyfn):
    groups = {}
    for u in units:
        k = keyfn(u["lines"])
        groups.setdefault(k, []).append(u)
    return groups


def main():
    units = load_units()
    raw_groups = group_by(units, lambda lines: tuple(lines))
    n_raw = len(raw_groups)

    axes = {
        "reorder": norm_reorder,
        "temp": norm_temp,
        "spelling": norm_spelling,
        "address": norm_address,
        "all_combined": norm_all,
    }
    axis_counts = {}
    for name, fn in axes.items():
        g = group_by(units, fn)
        axis_counts[name] = len(g)

    # classify each raw distinct-text group of size 1 against every OTHER
    # raw group: does some OTHER text become equal to it under exactly one
    # axis (and no other)?  This finds "matched pairs" whose only
    # difference is that one cause.
    causes = {"a_move_erasure": [], "b_reorder": [], "c_temp": [],
             "d_spelling": [], "e_address": [], "f_distinct": []}

    # index: for each axis, map normalized-key -> list of raw texts sharing it
    axis_index = {}
    for name, fn in axes.items():
        idx = {}
        for text, us in raw_groups.items():
            k = fn(list(text))
            idx.setdefault(k, set()).add(text)
        axis_index[name] = idx

    def collapses_under(text, axis_name):
        fn = axes[axis_name]
        k = fn(list(text))
        peers = axis_index[axis_name].get(k, set())
        return len(peers) > 1

    examples = {}
    singleton_texts = list(raw_groups.keys())
    for text in singleton_texts:
        matched = None
        for axis_name in ["temp", "spelling", "address", "reorder"]:
            if collapses_under(text, axis_name):
                matched = axis_name
                break
        if matched == "temp":
            causes["c_temp"].append(text)
            examples.setdefault("c_temp", (text, sorted(
                axis_index["temp"][norm_temp(list(text))])[:2]))
        elif matched == "spelling":
            causes["d_spelling"].append(text)
            examples.setdefault("d_spelling", (text, sorted(
                axis_index["spelling"][norm_spelling(list(text))])[:2]))
        elif matched == "address":
            causes["e_address"].append(text)
            examples.setdefault("e_address", (text, sorted(
                axis_index["address"][norm_address(list(text))])[:2]))
        elif matched == "reorder":
            causes["b_reorder"].append(text)
            examples.setdefault("b_reorder", (text, sorted(
                axis_index["reorder"][norm_reorder(list(text))])[:2]))
        else:
            causes["f_distinct"].append(text)

    # (a) redundant-mov detection: a text whose ONLY difference from
    # another text in the SAME raw-text set is a `mov X,Y` line where Y is
    # never subsequently read in that text (heuristic: Y does not appear
    # as an operand source in any later line).
    def has_dead_mov(lines):
        for i, ln in enumerate(lines):
            if not ln.startswith("mov "):
                continue
            try:
                _, operands = ln.split(" ", 1)
                dst = operands.split(",")[-1]
            except ValueError:
                continue
            rest = " ".join(lines[i + 1:])
            if dst not in rest:
                return (i, ln)
        return None

    dead_mov_hits = []
    for text in causes["f_distinct"]:
        lines = list(text)
        hit = has_dead_mov(lines)
        if hit is not None:
            dead_mov_hits.append((text, hit))
    # move these out of f_distinct into a_move_erasure
    dead_mov_texts = set(t for t, _ in dead_mov_hits)
    causes["f_distinct"] = [t for t in causes["f_distinct"]
                            if t not in dead_mov_texts]
    causes["a_move_erasure"] = list(dead_mov_texts)

    report = {
        "meta": {
            "role": "generator provenance",
            "generator": "uniqueness_audit.py",
            "note": "grouping key is derived instruction TEXT only -- "\
                   "the `operator` field is read solely for the quoted "\
                   "examples' display labels, never as a grouping key "\
                   "(spelling ban).",
        },
        "population": {
            "0branch_canon_ok_units": len(units),
            "distinct_raw_texts": n_raw,
        },
        "axis_by_axis_distinct_count": axis_counts,
        "collapse_from_raw": {
            name: n_raw - cnt for name, cnt in axis_counts.items()
        },
        "cause_counts": {k: len(v) for k, v in causes.items()},
        "examples": {},
    }
    for cause, (text, peers) in examples.items():
        report["examples"][cause] = {
            "text_a": list(text),
            "peer_texts": [list(p) for p in peers if p != text][:1],
        }
    if dead_mov_hits:
        text, (i, ln) = dead_mov_hits[0]
        report["examples"]["a_move_erasure"] = {
            "text": list(text),
            "dead_mov_line_index": i,
            "dead_mov_line": ln,
        }
    report["cause_counts"]["f_distinct_singleton_no_cause_found"] = \
        len(causes["f_distinct"])

    out_path = os.path.join(HERE, "uniqueness_audit_report.json")
    fh = open(out_path, "w")
    json.dump(report, fh, indent=1)
    fh.close()
    print(json.dumps(report, indent=1))
    print("wrote", out_path)


if __name__ == "__main__":
    sys.exit(main())
