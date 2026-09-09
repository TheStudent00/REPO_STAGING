"""Acceptance test for tree_sitter_base: frozen-census equality, determinism, partition totality.

Run:  python3 -m pytest PseudoCoup_v6/Tools/ledgerer/tree_sitter/ -q
"""
import os

import pytest

from parse_source import GRAMMARS, parse_file
from record_coverage import census, partition, render_census

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

FIXTURES = {
    "python": "sample_python.py",
    "rust": "sample_rust.rs",
    "cpp": "sample_cpp.cc",
}


@pytest.mark.parametrize("lang", sorted(GRAMMARS))
def test_census_matches_frozen(lang):
    """Parse the pinned fixture; rendered census must equal the frozen file byte for byte."""
    tree = parse_file(os.path.join(FIX, FIXTURES[lang]), lang)
    got = render_census(census(tree.root_node))
    frozen_path = os.path.join(FIX, f"expected_{lang}.json")
    with open(frozen_path, "r", encoding="utf-8") as f:
        frozen = f.read()
    assert got == frozen, f"census drifted from frozen for {lang}"


@pytest.mark.parametrize("lang", sorted(GRAMMARS))
def test_census_deterministic(lang):
    """Two independent parses render byte-identical censuses."""
    path = os.path.join(FIX, FIXTURES[lang])
    a = render_census(census(parse_file(path, lang).root_node))
    b = render_census(census(parse_file(path, lang).root_node))
    assert a == b


@pytest.mark.parametrize("lang", sorted(GRAMMARS))
def test_fixture_has_no_parse_errors(lang):
    """The pinned fixtures parse clean — an ERROR node means the fixture or grammar broke."""
    tree = parse_file(os.path.join(FIX, FIXTURES[lang]), lang)
    kinds = census(tree.root_node)["named"]
    assert "ERROR" not in kinds, f"fixture for {lang} has parse errors"


def test_partition_is_total_and_leftover_is_worklist():
    kinds = {"a", "b", "c", "d"}
    part = partition(kinds, handled={"a"}, baseline={"b"})
    assert part == {"handled": ["a"], "baseline": ["b"],
                    "leftover": ["c", "d"]}


def test_partition_rejects_double_claim():
    with pytest.raises(ValueError):
        partition({"a", "b"}, handled={"a"}, baseline={"a"})


def test_unknown_grammar_refuses():
    from parse_source import get_parser
    with pytest.raises(KeyError):
        get_parser("cobol")
