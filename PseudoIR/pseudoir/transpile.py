"""
transpile.py -- the unified entry point (T1.2).

`transpile(source, target)` runs the gate FIRST and refuses to emit on a FAIL (raising
GateFailure carrying the G1-style report), then walks the parsed tree with the target's
emitter (pseudoir.emit.get_emitter) to produce a complete target source file.

The gate-check-precedes-transpile ordering is the production-grade contract: a Hub file
that binds a construct with no confirmed lowering in the chosen target NEVER silently
emits half a file -- it fails loudly with the per-op coverage table, exactly like the
gate CLI, and the process exits nonzero.
"""
from . import binder as _binder
from . import gate as _gate
from .emit import get_emitter


class GateFailure(Exception):
    """Raised when the gate rejects the Hub source for the chosen target. Carries the
    formatted G1 report in `.report` and the GateResult in `.result`."""

    def __init__(self, result):
        self.result = result
        self.report = _gate.format_report(result)
        super().__init__(f"gate FAIL for target(s) {result.targets}")


def transpile(source, target):
    """Transpile Hub `source` (str or bytes) to `target`. Gate-checks against `target`
    first; raises GateFailure on a gate FAIL. Returns the emitted target source string."""
    src = source.encode() if isinstance(source, str) else source
    res = _gate.check(src, [target])
    if not res.passed:
        raise GateFailure(res)
    tree = _binder.parse(src)
    emitter = get_emitter(target)
    return emitter.emit_module(tree, src)


def transpile_file(path, target):
    src = open(path, "rb").read()
    res = _gate.check(src, [target], hub_file=path)
    if not res.passed:
        raise GateFailure(res)
    tree = _binder.parse(src)
    emitter = get_emitter(target)
    return emitter.emit_module(tree, src)
