"""Acceptance test for the phase-1 ledger: uniqueness, recount equality, round-trip, refusal.

Run:
    python3 -m pytest ~/Programming/PseudoCoup_v6/Tools/ledgerer/ -q

No environment variable and no other repo needed. The corpus is
vendored beside this test — see `fixtures/upstream/MANIFEST.md`.

Pinned corpus: representative LLVM/rustc-LLVM-facing compiler files
(rustc_codegen_llvm's declare.rs and va_arg.rs, LLVM's
X86MCCodeEmitter.cpp, and rustc_codegen_ssa's mir/rvalue.rs) — the
settled LLVM/rustc-LLVM direction, generic enough to exercise the
ledger's uniqueness/recount/round-trip/refusal acceptance regardless
of which compiler source it is pointed at.

Vendored 2026-07-31. These four files used to be read out of
PseudoCoup_v5 through a PCV5_ROOT environment variable, which made
this suite unable to pass without another repo on disk — a dependency
on a past project rather than a transplant from one. The files are
upstream rustc and LLVM source, not PCv5's work, so copying them here
loses nothing and makes this repo self-sufficient.
"""
import os

import pytest

from build_ledger import (LedgerRefusal, build, dump, index_by_id, load,
                          require_type)
from check_ledger import check

# The corpus root is this test's own fixtures folder.
CORPUS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "fixtures", "upstream")

CORPUS = [
    ("declare.rs", "rust"),
    ("va_arg.rs", "rust"),
    ("X86MCCodeEmitter.cpp", "cpp"),
    ("rvalue.rs", "rust"),
]

# Kept as the old name so the rest of this file reads unchanged; it is
# no longer PCv5's root and no longer overridable by the environment.
PCV5 = CORPUS_ROOT


@pytest.fixture(scope="module")
def ledger():
    return build(PCV5, CORPUS)


def test_check_green(ledger):
    report = check(ledger, PCV5)
    assert report["ok"], report


def test_build_deterministic(tmp_path, ledger):
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    dump(ledger, str(a))
    dump(build(PCV5, CORPUS), str(b))
    assert a.read_bytes() == b.read_bytes()


def test_dump_load_round_trip(tmp_path, ledger):
    p1, p2 = tmp_path / "l1.json", tmp_path / "l2.json"
    dump(ledger, str(p1))
    dump(load(str(p1)), str(p2))
    assert p1.read_bytes() == p2.read_bytes()


def test_declarations_marked_unresolvable_not_omitted(ledger):
    decls = [r for r in ledger["records"]
             if r["semantic"]["type"] == "unresolvable"]
    assert decls, "phase-1 corpus has declarations; none marked is a bug"


def test_consumer_refusal_halts(ledger):
    idx = index_by_id(ledger)
    unresolved = next(r for r in ledger["records"]
                      if r["semantic"]["type"] == "unresolvable")
    with pytest.raises(LedgerRefusal):
        require_type(idx[unresolved["id"]])


def test_resolved_type_passes_consumer():
    rec = {"id": "x", "node_kind": "function_item", "file": "f",
           "span": {"start_line": 1}, "semantic": {"type": "fn(i64)->i64"}}
    assert require_type(rec) == "fn(i64)->i64"


def test_duplicate_id_detected(ledger):
    import copy
    bad = copy.deepcopy(ledger)
    bad["records"].append(dict(bad["records"][0]))
    report = check(bad, PCV5)
    assert not report["ok"] and report["duplicate_ids"]
