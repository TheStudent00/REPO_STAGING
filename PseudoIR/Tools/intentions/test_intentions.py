"""Acceptance suite for T5 intentions: both sub-node acceptance sections of node_0_0_4 (schema extension + slicing request forms).

Implements the acceptance sections of
PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_intentions_data_shape.md
and
PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_retired_seam_declarations.md

Run:  python3 -m pytest PseudoIR/Tools/intentions/ -q

No environment variable and no other repo needed.

Vendored 2026-07-31. `pc_verdicts.json` — the R1-verified artifact
this suite checks the copy-forward against — used to be read out of
`PseudoCoup_v5/Designing/` through a PCV5_ROOT
environment variable, with a fallback that guessed at a co-tree beside
this repo. That made this suite unable to pass without another repo on
disk, and it broke the day PCv5 was gutted. The artifact is now
vendored beside this test; see `fixtures/upstream/MANIFEST.md`.
"""

import copy
import json
import os
import types

import pytest

import build_intentions
import intentions_data

HERE = os.path.dirname(os.path.abspath(__file__))
VERDICTS = os.path.join(HERE, "fixtures", "upstream", "pc_verdicts.json")

# every field pc_verdicts.json carries today, except meta (meta
# names its generator, which necessarily changed in the copy-forward;
# the sources it listed are asserted preserved instead)
DATA_FIELDS = ("languages", "intent_categories", "t1_realizations",
               "t2_compatibility", "t2_diagonal", "primitives",
               "operators", "basis_audit", "border_lattice")


def _data_copy():
    """A deep, independent copy of the data module as a namespace."""
    ns = types.SimpleNamespace()
    for key in ("LANGS", "CATS", "T1", "T2", "DIAG", "PRIMS", "OPS",
                "BASIS", "LATTICE", "ROW_SATISFIERS", "CANON",
                "MINIMUM_SET", "POLICIES", "POLICY_REFS"):
        setattr(ns, key, copy.deepcopy(getattr(intentions_data, key)))
    return ns


def _canonical(value) -> str:
    """One canonical serialization for byte-level field comparison."""
    return json.dumps(value, indent=1, ensure_ascii=False,
                      sort_keys=True)


# ---------------- (a) byte-identical rebuild ----------------

def test_rebuild_byte_identical():
    """Two rebuilds render byte-identically and match the committed artifact."""
    first = build_intentions.render(build_intentions.build())
    second = build_intentions.render(build_intentions.build())
    assert first == second, "rebuild is not byte-identical"
    with open(build_intentions.ARTIFACT, "r", encoding="utf-8") as f:
        committed = f.read()
    assert first == committed, \
        "committed pc_intentions.json drifted from a rebuild"


def test_artifact_contains_all_four_new_fields():
    artifact = build_intentions.build()
    for field in build_intentions.EXTENSION_FIELDS:
        assert field in artifact, f"missing extension field {field}"


# ---------------- (b) pre-existing fields byte-identical ----------------

@pytest.mark.parametrize("field", DATA_FIELDS)
def test_preexisting_field_byte_identical(field):
    """Each pre-existing field equals the R1-verified artifact, compared field by field."""
    assert os.path.isfile(VERDICTS), f"R1 artifact not found: {VERDICTS}"
    with open(VERDICTS, "r", encoding="utf-8") as f:
        verified = json.load(f)
    ours = build_intentions.build()
    assert _canonical(ours[field]) == _canonical(verified[field]), \
        f"pre-existing field {field} drifted from the R1-verified artifact"


def test_meta_preserves_original_sources():
    """meta.generated_by necessarily changed in the copy-forward; the original sources list must survive inside ours."""
    with open(VERDICTS, "r", encoding="utf-8") as f:
        verified = json.load(f)
    ours = build_intentions.build()
    for src in verified["meta"]["sources"]:
        assert src in ours["meta"]["sources"], \
            f"original meta source {src} dropped in copy-forward"


# ---------------- (c) four negative tests: each removal REFUSES ----------------

def test_refuses_missing_satisfier_row():
    d = _data_copy()
    del d.ROW_SATISFIERS["G"]
    with pytest.raises(build_intentions.Refusal, match="row_satisfiers"):
        build_intentions.build(d)


def test_refuses_missing_canon():
    d = _data_copy()
    del d.CANON["O4"]
    with pytest.raises(build_intentions.Refusal, match="canon"):
        build_intentions.build(d)


def test_refuses_missing_set_member():
    d = _data_copy()
    d.MINIMUM_SET = d.MINIMUM_SET[:-1]
    with pytest.raises(build_intentions.Refusal, match="minimum_set"):
        build_intentions.build(d)


def test_refuses_missing_policy_link():
    d = _data_copy()
    d.POLICY_REFS = []          # P12 still mentions policy 6 -> unlinked
    with pytest.raises(build_intentions.Refusal, match="policy"):
        build_intentions.build(d)


def test_refuses_dangling_policy_target():
    """The other direction: the ref stays but its policy entry is removed."""
    d = _data_copy()
    del d.POLICIES["6"]
    with pytest.raises(build_intentions.Refusal, match="dangling"):
        build_intentions.build(d)


# ---------------- (d) schema check ----------------

def test_every_category_has_satisfiers_every_verdict_has_canon():
    artifact = build_intentions.build()
    for cat in artifact["intent_categories"]:
        assert cat["id"] in artifact["row_satisfiers"], \
            f"category {cat['id']} lacks a satisfier entry"
    for row in artifact["primitives"] + artifact["operators"]:
        assert row["id"] in artifact["canon"], \
            f"verdict {row['id']} lacks a canon entry"
        assert artifact["canon"][row["id"]]["cites"] == row["pc_verdict"]


def test_minimum_set_is_eleven():
    artifact = build_intentions.build()
    assert len(artifact["minimum_set"]) == 11

# Sections (e)/(f)/(g) of this suite exercised validate_form.py against four
# proven-chain slicing-request forms built against a retired reference
# backend. Both the forms and that chain were removed as mis-aimed
# (2026-07-30); the forward direction is LLVM/rustc-LLVM. validate_form.py
# itself is generic (rust/python/cpp) and stays; new form-validation tests
# belong here once an LLVM-facing form exists to validate.
