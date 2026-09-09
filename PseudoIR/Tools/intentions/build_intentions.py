"""Builds pc_intentions.json — the copied-forward verdict artifact extended with the four slicer-steering fields.

Assembly of the pre-existing fields reproduces
PseudoCoup_v5/Designing/build_verdicts.py exactly
(same construction over the vendored data), so every field the
R1-verified pc_verdicts.json already carries stays byte-stable.
The four extension fields of CORE 0_0_4_0 are added on top:
row_satisfiers, canon, minimum_set, policy_refs.

Refusal posture (same as build_verdicts.py, wider surface): a
missing satisfier row, a missing or drifted canon entry, a minimum
set that is not the 11 objects, or a dangling/unlinked policy
reference each REFUSE to emit, with the failure named.

Deterministic output: sorted keys, no timestamps; rebuilds are
byte-identical. Rerun after any data change:
    python3 PseudoIR/Tools/intentions/build_intentions.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import intentions_data  # noqa: E402

ARTIFACT = os.path.join(HERE, "pc_intentions.json")

# The fields pc_verdicts.json already carries; kept byte-stable.
PREEXISTING_FIELDS = (
    "meta", "languages", "intent_categories", "t1_realizations",
    "t2_compatibility", "t2_diagonal", "primitives", "operators",
    "basis_audit", "border_lattice")

# The four extension fields (working names, the owner's to settle).
EXTENSION_FIELDS = ("row_satisfiers", "canon", "minimum_set",
                    "policy_refs")

CANON_KINDS = ("language", "languages", "uniform", "legislated")


class Refusal(ValueError):
    """Raised when the data is incomplete; the artifact is not emitted."""


def assemble(d=None):
    """Assemble the artifact dict from a data namespace (default: intentions_data)."""
    d = d or intentions_data
    return {
        "meta": {
            "generated_by": "build_intentions.py",
            "copied_forward_from":
                "PseudoCoup_v5/Designing/pc_verdicts.json "
                "(R1-verified; PCv5 is archived, maintained in PCv6 "
                "from 2026-07-28 on)",
            "sources": ["intention_tables_gen.py",
                        "../Research/basis_audit/results.md",
                        "PCv7_policy_decisions.md"],
            "extension_sources": [
                "intention_row_satisfiers.md", "BEJ_expansion.md",
                "minimum_intention_set.md", "PCv7_policy_decisions.md",
                "the pc_verdict strings (canon citations)"],
        },
        "languages": d.LANGS,
        "intent_categories": [
            {"id": k, "name": n, "desc": desc} for k, n, desc in d.CATS],
        "t1_realizations": d.T1,
        "t2_compatibility": [
            {"a": a, "b": b, "verdict": v, "note": note}
            for (a, b), (v, note) in d.T2.items()],
        "t2_diagonal": d.DIAG,
        "primitives": [
            {"id": i, "name": n, "cells": dict(zip(d.LANGS, cells)),
             "pc_verdict": pc} for i, n, cells, pc in d.PRIMS],
        "operators": [
            {"id": i, "name": n, "cells": dict(zip(d.LANGS, cells)),
             "pc_verdict": pc} for i, n, cells, pc in d.OPS],
        "basis_audit": d.BASIS,
        "border_lattice": d.LATTICE,
        "row_satisfiers": d.ROW_SATISFIERS,
        "canon": d.CANON,
        "minimum_set": d.MINIMUM_SET,
        "policy_refs": {"policies": d.POLICIES, "refs": d.POLICY_REFS},
    }


def check(d=None):
    """Return the list of completeness errors (empty = emittable)."""
    d = d or intentions_data
    errors = []
    cat_ids = [c[0] for c in d.CATS]

    # ---- pre-existing checks, kept from build_verdicts.py ----
    pairs = set(d.T2)
    for i, a in enumerate(cat_ids):
        for b in cat_ids[i + 1:]:
            if (a, b) not in pairs and (b, a) not in pairs:
                errors.append(f"t2 missing pair {a}{b}")
    for k in cat_ids:
        missing = [lang for lang in d.LANGS if lang not in d.T1[k]]
        if missing:
            errors.append(f"t1 row {k} missing {missing}")
    for group, rows in (("primitives", d.PRIMS), ("operators", d.OPS)):
        for rid, name, cells, pc in rows:
            if len(cells) != len(d.LANGS):
                errors.append(
                    f"{group} {rid} has {len(cells)} cells, "
                    f"want {len(d.LANGS)}")
    for el, m in d.BASIS.items():
        missing = [lang for lang in d.LANGS if lang not in m]
        if missing:
            errors.append(f"basis {el} missing {missing}")
    for e in d.LATTICE:
        if e["verdict"] not in ("identical", "convertible", "incompatible"):
            errors.append(f"lattice bad verdict: {e}")
        if e["verdict"] == "convertible" and not e["spelling"]:
            errors.append(f"lattice convertible without spelling: {e}")

    # ---- extension checks (the widened refusal surface) ----
    # row_satisfiers: every intent category A-J must have an entry.
    for k in cat_ids:
        if k not in d.ROW_SATISFIERS:
            errors.append(f"row_satisfiers: category {k} has no "
                          f"satisfier row")
    for k, entry in d.ROW_SATISFIERS.items():
        if k not in cat_ids:
            errors.append(f"row_satisfiers: unknown category {k}")
            continue
        for field in ("satisfier", "kind", "native", "in_hub",
                      "status", "basis", "policies"):
            if field not in entry:
                errors.append(f"row_satisfiers {k}: missing field "
                              f"{field}")
        for lang in entry.get("native", []):
            if lang not in d.LANGS:
                errors.append(f"row_satisfiers {k}: unknown language "
                              f"{lang}")
        for p in entry.get("policies", []):
            if str(p) not in d.POLICIES:
                errors.append(f"row_satisfiers {k}: dangling policy "
                              f"reference {p}")

    # canon: every primitive/operator verdict must have an entry
    # whose citation matches the verdict string exactly.
    verdicts = {rid: pc for rid, _n, _c, pc in list(d.PRIMS) + list(d.OPS)}
    for rid, pc in verdicts.items():
        entry = d.CANON.get(rid)
        if entry is None:
            errors.append(f"canon: verdict {rid} has no canon entry")
            continue
        if entry.get("kind") not in CANON_KINDS:
            errors.append(f"canon {rid}: bad kind {entry.get('kind')!r}")
        if entry.get("cites") != pc:
            errors.append(f"canon {rid}: citation does not match the "
                          f"pc_verdict string (drift)")
        if entry.get("kind") in ("language", "languages") and \
                not entry.get("canon_languages"):
            errors.append(f"canon {rid}: kind names a language but "
                          f"canon_languages is empty")
        for lang in entry.get("canon_languages", []):
            if lang not in d.LANGS:
                errors.append(f"canon {rid}: unknown language {lang}")
        if not entry.get("statement"):
            errors.append(f"canon {rid}: empty statement")
    for rid in d.CANON:
        if rid not in verdicts:
            errors.append(f"canon: entry {rid} matches no verdict")

    # minimum_set: exactly the 11 objects, numbered 1..11.
    if len(d.MINIMUM_SET) != 11:
        errors.append(f"minimum_set: {len(d.MINIMUM_SET)} members, "
                      f"the set is 11")
    else:
        ns = [m.get("n") for m in d.MINIMUM_SET]
        if ns != list(range(1, 12)):
            errors.append(f"minimum_set: numbering {ns} is not 1..11")
        names = [m.get("object") for m in d.MINIMUM_SET]
        if len(set(names)) != len(names):
            errors.append("minimum_set: duplicate object names")

    # policy_refs: no dangling ref; no unlinked "policy" mention.
    for ref in d.POLICY_REFS:
        vid = ref.get("verdict_id")
        if vid not in verdicts:
            errors.append(f"policy_refs: verdict_id {vid} matches no "
                          f"verdict")
        elif ref.get("cites") != verdicts[vid]:
            errors.append(f"policy_refs {vid}: citation does not match "
                          f"the pc_verdict string (drift)")
        if str(ref.get("policy")) not in d.POLICIES:
            errors.append(f"policy_refs {vid}: dangling policy "
                          f"reference {ref.get('policy')}")
        if ref.get("mention") not in (ref.get("cites") or ""):
            errors.append(f"policy_refs {vid}: mention "
                          f"{ref.get('mention')!r} absent from citation")
    linked = {ref.get("verdict_id") for ref in d.POLICY_REFS}
    for rid, pc in verdicts.items():
        if "policy" in pc and rid not in linked:
            errors.append(f"policy_refs: verdict {rid} mentions a "
                          f"policy but has no ref")

    return errors


def build(d=None):
    """Check then assemble; raise Refusal (nothing emitted) on any error."""
    errors = check(d)
    if errors:
        raise Refusal("REFUSED to emit:\n" +
                      "\n".join("  " + e for e in errors))
    return assemble(d)


def render(artifact) -> str:
    """Serialize deterministically: sorted keys, no timestamps."""
    return json.dumps(artifact, indent=1, ensure_ascii=False,
                      sort_keys=True) + "\n"


def main():
    try:
        artifact = build()
    except Refusal as exc:
        print(exc)
        raise SystemExit(1)
    text = render(artifact)
    with open(ARTIFACT, "w", encoding="utf-8") as f:
        f.write(text)
    print("valid. wrote pc_intentions.json: "
          f"{len(artifact['intent_categories'])} categories, "
          f"{len(artifact['row_satisfiers'])} satisfier rows, "
          f"{len(artifact['canon'])} canon entries, "
          f"{len(artifact['minimum_set'])} set members, "
          f"{len(artifact['policy_refs']['refs'])} policy refs, "
          f"{len(artifact['policy_refs']['policies'])} policies")


if __name__ == "__main__":
    main()
