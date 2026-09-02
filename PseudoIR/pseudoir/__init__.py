"""
pseudoir -- the operator registry + Hub transpiler, packaged.

This is the productization (v2 PLAN T1) of the PseudoIR v2 research repo: the loose
probers, the loose registry JSON, and the gate become one importable, pip-installable
package that PseudoCoup can consult.

CONSUMER SURFACE (the minimal API INTEGRATION.md documents)
-----------------------------------------------------------
    from pseudoir import U                       # the Hub null-safety runtime
    import pseudoir
    pseudoir.transpile(source, target)           # gate-checked whole-file transpile
    pseudoir.registry.lookup(op_id, target)      # per-op per-target strategy/status
    pseudoir.hoist()                             # a fresh shared Hoister
    pseudoir.gate.check(src_bytes, targets)      # the Map-Wrap-Fail gate
"""
from . import registry, gate, binder, ir, emit  # noqa: F401
from . import U  # noqa: F401  (re-export the Hub runtime: `from pseudoir import U`)
from .hoister import Hoister
from .transpile import transpile, transpile_file, GateFailure  # noqa: F401

__version__ = "0.1.0"


def hoist():
    """Return a fresh shared statement Hoister (pseudoir.Hoister). One mechanism for
    every synthetic-statement lowering; see hoister.py."""
    return Hoister()


__all__ = [
    "registry", "gate", "binder", "ir", "emit", "U",
    "Hoister", "hoist", "transpile", "transpile_file", "GateFailure",
    "__version__",
]
