#!/usr/bin/env python3
"""ref2_compare.py -- two runs of `level0_check.py`, BEFORE and AFTER one
correction to the reference, put side by side per written place.

WHAT THIS IS, in relation.  `level0_check.py` (task ref1) writes one row per
(instruction variant, written place) with z3's verdict on whether our
reference's term and the K-framework semantics' term can differ.  Task ref2
corrects the reference four times and re-runs that check after each.  This
program is the DIFFERENCE: same key, two verdicts, counted by direction and
named by mnemonic, so a correction's effect is measured rather than asserted.

THE KEY is (their variant name, the written place, which occurrence of that
place in the variant's own row list) -- their variant name is their identifier
for one instruction form and the place is a destination or a flag as Intel's
manual names it.  None of the three is an operator token; the mnemonic rides
on the row as the machine-form field `mnem`, which the spelling guard reads as
machine form (the ruling of 2026-09-08).

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in
this line -- not in matching, not in "which pairs get compared", not in report
rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per unit:
as a display label on the member.  HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the
fix brief itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own
output on failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Coding discipline: no compound one-liner statements.

usage:
  ref2_compare.py <before.json> <after.json> <out.json> <label>
"""

import json
import sys


OUTCOMES = ("unsat", "sat", "unknown", "undefined", "refused")


def places_of(document):
    """(their variant name, place, which occurrence) -> the row.

    THE THIRD FIELD IS NOT DECORATION.  28 variants of the packed-float
    family write `reg_xmm0` TWICE in one row list -- the whole register
    and the low lane -- so a key of (variant, place) alone covers 1,751
    of the check's 1,779 rows and quietly drops 28.  The occurrence
    index carries them, and the totals below then equal the check's own
    tally exactly."""
    out = {}
    for variant in document["variants"]:
        seen = {}
        for place in variant["places"]:
            name = place["place"]
            seen[name] = seen.get(name, 0) + 1
            key = (variant["variant"], name, seen[name])
            out[key] = {
                "mnem": variant["mnem"],
                "shape": variant["shape"],
                "key_width": variant["key_width"],
                "line": variant["line"],
                "outcome": place["outcome"],
                "ours": place.get("ours"),
                "theirs": place.get("theirs"),
                "counterexample": place.get("counterexample"),
                "ours_at_the_counterexample":
                    place.get("ours_at_the_counterexample"),
                "theirs_at_the_counterexample":
                    place.get("theirs_at_the_counterexample"),
                "cause": place.get("cause"),
                "rows": variant["attestation_ledger_rows"],
            }
    return out


def compare(before, after):
    left = places_of(before)
    right = places_of(after)
    moved = []
    for key in sorted(set(left) | set(right), key=str):
        was = left.get(key)
        now = right.get(key)
        if was is None:
            moved.append({"variant": key[0], "place": key[1],
                          "occurrence": key[2],
                          "before": None, "after": now["outcome"],
                          "mnem": now["mnem"], "shape": now["shape"],
                          "key_width": now["key_width"],
                          "line": now["line"], "rows": now["rows"],
                          "ours_after": now["ours"],
                          "theirs": now["theirs"],
                          "cause_after": now["cause"]})
            continue
        if now is None:
            moved.append({"variant": key[0], "place": key[1],
                          "occurrence": key[2],
                          "before": was["outcome"], "after": None,
                          "mnem": was["mnem"], "shape": was["shape"],
                          "key_width": was["key_width"],
                          "line": was["line"], "rows": was["rows"],
                          "ours_before": was["ours"],
                          "theirs": was["theirs"],
                          "cause_before": was["cause"]})
            continue
        same_outcome = was["outcome"] == now["outcome"]
        same_term = was["ours"] == now["ours"]
        if same_outcome and same_term:
            continue
        moved.append({
            "variant": key[0], "place": key[1],
            "occurrence": key[2],
            "before": was["outcome"], "after": now["outcome"],
            "mnem": now["mnem"], "shape": now["shape"],
            "key_width": now["key_width"], "line": now["line"],
            "rows": now["rows"],
            "ours_before": was["ours"], "ours_after": now["ours"],
            "theirs": now["theirs"],
            "counterexample_before": was["counterexample"],
            "counterexample_after": now["counterexample"],
            "ours_at_the_counterexample_before":
                was["ours_at_the_counterexample"],
            "theirs_at_the_counterexample_before":
                was["theirs_at_the_counterexample"],
            "ours_at_the_counterexample_after":
                now["ours_at_the_counterexample"],
            "theirs_at_the_counterexample_after":
                now["theirs_at_the_counterexample"],
            "cause_before": was["cause"], "cause_after": now["cause"],
            "term_text_changed": not same_term,
        })
    return left, right, moved


def tally(rows):
    counts = {}
    for name in OUTCOMES:
        counts[name] = 0
    for row in rows.values():
        counts[row["outcome"]] = counts[row["outcome"]] + 1
    return counts


def direction_table(moved):
    """how many places went from which verdict to which."""
    counts = {}
    for row in moved:
        key = "%s -> %s" % (row["before"], row["after"])
        entry = counts.setdefault(key, {"places": 0, "mnems": set(),
                                        "rows": 0})
        entry["places"] = entry["places"] + 1
        entry["mnems"].add(row["mnem"])
        entry["rows"] = entry["rows"] + (row["rows"] or 0)
    out = []
    for key in sorted(counts, key=str):
        entry = counts[key]
        # THE MNEMONIC RIDES IN THE FIELD `mnem`, NEVER AS A BARE LIST
        # ELEMENT.  A list of bare tokens is a row structure, and the
        # spelling guard refuses it -- correctly: `and`, `or`, `xor` and
        # `not` are arch mnemonics AND operator spellings.  `mnem` is the
        # one field the guard reads as machine form (the ruling of
        # 2026-09-08), so each name is wrapped in one.
        out.append({"direction": key, "places": entry["places"],
                    "ledger_rows": entry["rows"],
                    "mnems": [{"mnem": name}
                              for name in sorted(entry["mnems"])]})
    return out


def per_mnem_table(moved):
    counts = {}
    for row in moved:
        entry = counts.setdefault(row["mnem"], {})
        key = "%s -> %s" % (row["before"], row["after"])
        entry[key] = entry.get(key, 0) + 1
    out = []
    for name in sorted(counts):
        out.append({"mnem": name, "moves": counts[name]})
    return out


def main(argv):
    if len(argv) != 5:
        print(__doc__)
        return 2
    before_path, after_path, out_path, label = argv[1:]
    with open(before_path) as handle:
        before = json.load(handle)
    with open(after_path) as handle:
        after = json.load(handle)
    left, right, moved = compare(before, after)
    counts_before = tally(left)
    counts_after = tally(right)
    directions = direction_table(moved)
    out = {
        "what": ("one correction to the reference, measured as the "
                 "difference between two runs of level0_check.py"),
        "label": label,
        "before_file": before_path,
        "after_file": after_path,
        "places_before": sum(counts_before.values()),
        "places_after": sum(counts_after.values()),
        "counts_before": counts_before,
        "counts_after": counts_after,
        "directions": directions,
        "per_mnem": per_mnem_table(moved),
        "moved": moved,
    }
    with open(out_path, "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
    print("| outcome | before | after | change |")
    print("|---|---|---|---|")
    for name in OUTCOMES:
        change = counts_after[name] - counts_before[name]
        print("| `%s` | %d | %d | %+d |"
              % (name, counts_before[name], counts_after[name], change))
    print("")
    print("| direction | places | ledger rows | mnemonics |")
    print("|---|---|---|---|")
    for row in directions:
        names = " ".join("`%s`" % m["mnem"] for m in row["mnems"])
        print("| %s | %d | %d | %s |"
              % (row["direction"], row["places"], row["ledger_rows"],
                 names))
    print("")
    print("places whose row changed at all: %d" % len(moved))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
