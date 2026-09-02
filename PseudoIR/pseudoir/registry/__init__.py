"""
pseudoir.registry -- the operator registry, loaded from packaged JSON data.

WHAT THIS IS
------------
The research repo kept `ops.json` + `xforms.json` as loose files under v2/registry/,
read by each prober with a hand-rolled `json.load(open(...))` and an ad-hoc
`{o["id"]: o for o in ...["ops"]}` index. This module is that load-and-index done
ONCE, with the JSON shipped as PACKAGE DATA (pseudoir/registry/data/*.json) so an
installed `pseudoir` carries its own registry -- no dependency on the source tree
layout. The data files here are COPIES of v2/registry/ (copied at package build, not
moved); v2/registry/ stays the probers' working copy.

The two files are DATA, described by data/schema.md: `ops.json` holds expression
operators (op.null_coalesce, op.destructure, op.overloaded_binary, op.range,
op.string_interp, op.match_expr, ...) each with a `columns` object keyed by target
language; `xforms.json` holds call-convention transforms (xform.named_args,
decl.variadic) each with a `targets` object keyed by target language. Both are merged
into one id->entry index here so a consumer looks an op up by id without caring which
file it came from.

PUBLIC SURFACE (the T1.4 consumer API)
--------------------------------------
    load()                  -> Registry           (cached)
    Registry.entry(op_id)   -> ("op"|"xform", entry_dict)
    Registry.column(op_id, target) -> the per-target column dict (or None)
    Registry.lookup(op_id, target) -> LookupResult(strategy, status, lowering, ok, ...)
    Registry.languages      -> the fixed target list
    Registry.op_ids / xform_ids

`lookup` is the one call the gate and the emitters both make: "for this op in this
target, what is the strategy/status/lowering, and is it a non-fail confirmed cell?"
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "data")

# A cell "passes" (is usable in a build) if its confirmation is runtime- or
# parse-confirmed. Compound statuses like "parse-confirmed, runtime-pending" pass
# on their confirmed half. Ported verbatim from gate.py CONFIRMED / _status_ok.
CONFIRMED = ("runtime-confirmed", "parse-confirmed")


def _status_ok(status):
    parts = [p.strip() for p in str(status).split(",")]
    return any(p in CONFIRMED for p in parts)


class LookupResult:
    """The answer to 'how does <op_id> realize in <target>?'. Carries the raw
    column fields plus the two derived booleans the gate and emitters need:
      ok       -- strategy != 'fail' AND status is confirmed (safe to emit as-is)
      is_fail  -- the strategy is literally 'fail' (no known lowering)."""
    __slots__ = ("op_id", "target", "kind", "strategy", "status",
                 "lowering", "source_binding", "evidence", "ok", "is_fail", "present")

    def __init__(self, op_id, target, kind, column):
        self.op_id = op_id
        self.target = target
        self.kind = kind          # "op" | "xform"
        self.present = column is not None
        if column is None:
            self.strategy = "MISSING"
            self.status = "no-column"
            self.lowering = None
            self.source_binding = None
            self.evidence = None
            self.ok = False
            self.is_fail = False
            return
        self.strategy = column.get("strategy", "?")
        self.status = column.get("status", "?")
        self.lowering = column.get("lowering")
        self.source_binding = column.get("source_binding")
        self.evidence = column.get("evidence")
        self.is_fail = (self.strategy == "fail")
        self.ok = (not self.is_fail) and _status_ok(self.status)

    def __repr__(self):
        return (f"LookupResult({self.op_id}@{self.target}: "
                f"strategy={self.strategy}, status={self.status}, ok={self.ok})")


class Registry:
    """The loaded, indexed registry. One instance is cached by `load()`."""

    def __init__(self, ops_doc, xforms_doc):
        self._ops_doc = ops_doc
        self._xforms_doc = xforms_doc
        self.languages = list(ops_doc["languages"])
        self._by_id = {}
        for o in ops_doc["ops"]:
            self._by_id[o["id"]] = ("op", o)
        for x in xforms_doc["xforms"]:
            self._by_id[x["id"]] = ("xform", x)
        self.op_ids = [o["id"] for o in ops_doc["ops"]]
        self.xform_ids = [x["id"] for x in xforms_doc["xforms"]]

    # -- entry access --------------------------------------------------------
    def entry(self, op_id):
        """Return ('op'|'xform', entry_dict) for an op id, or (None, None)."""
        return self._by_id.get(op_id, (None, None))

    def column(self, op_id, target):
        """The raw per-target column dict for an op in a target, or None. An op's
        columns live under key 'columns'; a xform's under key 'targets'."""
        kind, entry = self._by_id.get(op_id, (None, None))
        if entry is None:
            return None
        cols = entry["columns"] if kind == "op" else entry["targets"]
        return cols.get(target)

    def lookup(self, op_id, target):
        """The one call the gate + emitters share: a LookupResult carrying strategy,
        status, lowering, and the derived `ok`/`is_fail` flags for op_id in target."""
        kind, _ = self._by_id.get(op_id, (None, None))
        return LookupResult(op_id, target, kind, self.column(op_id, target))

    def operators_table(self):
        """The op.overloaded_binary symbol->method table (add/sub/...), needed by the
        binder and the overloaded-op emitters. Returns {} if that op is absent."""
        _, ob = self._by_id.get("op.overloaded_binary", (None, None))
        return (ob or {}).get("operators", {})

    def __repr__(self):
        return (f"Registry({len(self.op_ids)} ops, {len(self.xform_ids)} xforms, "
                f"{len(self.languages)} languages)")


_CACHE = None


def load():
    """Load (and cache) the packaged registry."""
    global _CACHE
    if _CACHE is None:
        ops_doc = json.load(open(os.path.join(_DATA, "ops.json")))
        xforms_doc = json.load(open(os.path.join(_DATA, "xforms.json")))
        _CACHE = Registry(ops_doc, xforms_doc)
    return _CACHE


# ---- module-level conveniences (the flat consumer API T1.4 documents) ----
def lookup(op_id, target):
    """pseudoir.registry.lookup(op, target) -- see Registry.lookup."""
    return load().lookup(op_id, target)


def languages():
    return load().languages


def operators_table():
    """pseudoir.registry.operators_table() -- the op.overloaded_binary symbol->method
    table (add/sub/...); see Registry.operators_table."""
    return load().operators_table()
