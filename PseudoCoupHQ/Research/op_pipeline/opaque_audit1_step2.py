#!/usr/bin/env python3
"""opaque_audit1_step2.py -- STEP 2 ground-truth spot check support.

Finds every unit whose SELECTED VALUE changed between tree_match2 and
tree_match3 (normal_path_raw text differs -- the raw VEX-lifted text
before z3 normalization, so the diff is exactly the selection-rule
change, since normalize() itself is byte-identical between the two
files), then draws a stratified sample of >=20 units across languages
and shapes (bare-atom-old-vs-structured-new, structured-old-vs-bare-
new, structured-vs-structured) for hand ground-truth reading.

This script does NOT itself run the canon22 z3 ground-truth gate (that
machinery expects canon4_units_<lang>.json / sem_anchored_<lang>.json
loaded and matched to a specific unit id space that tree_units2/3's
`n` does not directly carry a join key for in this corpus layout).
What it DOES do, honestly: print each sampled unit's own raw lifted
expression (`normal_path_raw`) for OLD and NEW selection side by side,
plus the block/rule note that explains WHY each was picked, which is
enough evidence -- read against VEX's own semantics (the tool's own
testimony class, not forced-by-construction) -- to score each sample
old-right / new-right / both-defensible / neither, by hand, in the
final report.

THE SPELLING BAN: sampling key is (lang, n) unit identity plus the raw
text diff; `operator` is carried only as a per-unit display label.
"""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def load_units(path):
    doc = json.load(open(path))
    return {(u["lang"], u["n"]): u for u in doc["units"]}


def main():
    u2 = load_units(os.path.join(HERE, "tree_units2.json"))
    u3 = load_units(os.path.join(HERE, "tree_units3.json"))

    changed = []
    for key in sorted(u2.keys()):
        if key not in u3:
            continue
        a = u2[key]
        b = u3[key]
        if not a.get("sem_ok") or not b.get("sem_ok"):
            continue
        if a.get("normal_path_raw") != b.get("normal_path_raw"):
            changed.append(key)

    print("units whose selected raw value changed:", len(changed))

    by_lang = {}
    for lang, n in changed:
        by_lang.setdefault(lang, []).append((lang, n))
    for lang in sorted(by_lang):
        print("  %s: %d" % (lang, len(by_lang[lang])))

    random.seed(20260830)
    sample = []
    per_lang = max(1, 24 // max(1, len(by_lang)))
    for lang in sorted(by_lang):
        pool = by_lang[lang]
        take = min(per_lang, len(pool))
        sample.extend(random.sample(pool, take))
    if len(sample) < 20:
        remaining = [k for k in changed if k not in sample]
        random.shuffle(remaining)
        sample.extend(remaining[: 20 - len(sample)])
    sample = sample[:24]

    print()
    print("=== sample (%d units), old vs new raw + rule note ===" %
          len(sample))
    out_rows = []
    for lang, n in sample:
        a = u2[(lang, n)]
        b = u3[(lang, n)]
        print()
        print("%s/%s  operator(display)=%s  type_pair=%s" %
              (lang, n, a.get("operator"), a.get("type_pair")))
        print("  OLD (tree_match2) rule: %s" %
              a.get("normal_path_block_rule"))
        print("  OLD raw : %s" % a.get("normal_path_raw"))
        print("  OLD norm: %s" % a.get("normal_path_root"))
        print("  NEW (tree_match3) rule: %s" %
              b.get("normal_path_block_rule"))
        print("  NEW raw : %s" % b.get("normal_path_raw"))
        print("  NEW norm: %s" % b.get("normal_path_root"))
        out_rows.append(dict(
            lang=lang, n=n, operator=a.get("operator"),
            type_pair=a.get("type_pair"),
            old_rule=a.get("normal_path_block_rule"),
            old_raw=a.get("normal_path_raw"),
            old_norm=a.get("normal_path_root"),
            new_rule=b.get("normal_path_block_rule"),
            new_raw=b.get("normal_path_raw"),
            new_norm=b.get("normal_path_root"),
        ))

    out = dict(
        role="generator provenance",
        note="output of opaque_audit1_step2.py -- STEP 2 sampling "
             "support. Evidence class: raw lifted text read against "
             "VEX's own semantics (tool's own testimony), NOT the "
             "canon22 z3 ground-truth gate -- that gate was not wired "
             "up in this session for this unit-id space; scores in "
             "the final report are HAND READ from this dump, and are "
             "SPOT-CHECKED (N=%d), not exhaustive." % len(sample),
        total_changed=len(changed),
        changed_by_lang={k: len(v) for k, v in by_lang.items()},
        sample=out_rows,
    )
    out_path = os.path.join(HERE, "opaque_audit1_step2_sample.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print()
    print("wrote", out_path)


if __name__ == "__main__":
    main()
