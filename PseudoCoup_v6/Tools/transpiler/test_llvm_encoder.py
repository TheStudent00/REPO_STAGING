"""Acceptance for the LLVM encoder ingestor: determinism and a runtime smoke test.

The ingestor mechanically transpiles a named slice of LLVM's
hand-written X86 encoder (X86MCCodeEmitter.cpp) into Python. This
module's own text was previously pinned to be byte-identical with a
PCv5 artifact carrying commentary about a retired reference backend's
cross-checked encoder; that byte-identity requirement was removed
along with the commentary it depended on (2026-07-30) — determinism
and runtime behavior are what this suite verifies now.

Run:
    python3 -m pytest PseudoCoup_v6/Tools/transpiler/test_llvm_encoder.py -q

No environment variable and no other repo needed. The source is
vendored beside this test — see `fixtures/upstream/MANIFEST.md`.

Vendored 2026-07-31. X86MCCodeEmitter.cpp used to be read out of
PseudoCoup_v5 through a PCV5_ROOT environment variable, which made
this suite unable to pass without another repo on disk. It is upstream
LLVM source rather than PCv5's work, so copying it here loses nothing
and makes this repo self-sufficient.
"""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ingest_llvm_encoder import build_encoder  # noqa: E402

CPP = os.path.join(HERE, "fixtures", "upstream", "X86MCCodeEmitter.cpp")

# Kept, but it should never fire now that the source is vendored: a
# missing fixture is a broken checkout, not an absent optional repo.
pytestmark = pytest.mark.skipif(
    not os.path.isfile(CPP),
    reason=f"vendored upstream source missing: {CPP}")


def test_deterministic(tmp_path):
    a, b = tmp_path / "a.py", tmp_path / "b.py"
    build_encoder(CPP, str(a))
    build_encoder(CPP, str(b))
    assert a.read_bytes() == b.read_bytes()


def test_generated_encoder_runs_and_cut_arms_refuse(tmp_path):
    """Smoke the artifact itself: modRM packing works, cut prefix arms raise."""
    out = tmp_path / "llvm_encoder_gen.py"
    build_encoder(CPP, str(out))
    sys.path.insert(0, str(tmp_path))
    try:
        import importlib
        mod = importlib.import_module("llvm_encoder_gen")
        importlib.reload(mod)
        assert mod.mod_rm_byte(3, 2, 5) == (3 << 6) | (2 << 3) | 5
        h = mod.X86OpcodePrefixHelper()
        h.Kind = mod.PREFIX_KIND_NAMES["EVEX"]
        with pytest.raises(NotImplementedError):
            h.emit(bytearray())
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop("llvm_encoder_gen", None)
