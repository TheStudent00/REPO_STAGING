"""
gate.py -- the registry gate (Map-Wrap-Fail), re-expressed on package internals.

This is v2/gate/gate.py rebuilt so it reads the PACKAGED registry (pseudoir.registry)
and classifies constructs through the PACKAGED binder (pseudoir.binder), instead of
loading loose JSON and walking the tree inline. The check is unchanged:

    MAP  -- every named construct is baseline OR a recognized registry op/xform;
            anything else (lambda, yield, comprehension) is a FAIL (binder.classify).
    WRAP -- every bound op has a non-fail, confirmed column in EVERY active target
            (registry.lookup(op_id, target).ok); a fail/unconfirmed cell FAILS.

Output: a per-construct binding table (markdown pipe table -- the communication
protocol bans whitespace-aligned code-block tables), a per-op target-coverage table,
and a PASS/FAIL verdict. `check()` returns a GateResult; `run()` prints the report
and returns an exit code (0 PASS, 1 FAIL). The transpiler (pseudoir.transpile) calls
`check()` FIRST and refuses to emit on FAIL.
"""
import json

from . import binder as _binder
from . import registry as _registry


class GateResult:
    __slots__ = ("hub_file", "targets", "u_import_verified", "passed",
                 "bound_ops", "map_failures", "wrap_failures",
                 "baseline_node_types", "coverage", "classification")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    def as_dict(self):
        return {
            "hub_file": self.hub_file,
            "targets": self.targets,
            "u_import_verified": self.u_import_verified,
            "verdict": "PASS" if self.passed else "FAIL",
            "bound_ops": self.bound_ops,
            "map_failures": self.map_failures,
            "wrap_failures": [
                {"op": o, "target": t, "strategy": s, "status": st}
                for (o, t, s, st) in self.wrap_failures
            ],
            "baseline_node_types": self.baseline_node_types,
            "coverage": [
                {"op": o, "target": t, "ok": ok, "strategy": s, "status": st}
                for (o, t, ok, s, st) in self.coverage
            ],
        }


def check(src_bytes, targets, hub_file="<source>"):
    """Run the gate over Hub source bytes for a target set. Returns a GateResult."""
    reg = _registry.load()
    tree = _binder.parse(src_bytes)
    root = tree.root_node
    u_ok = _binder.u_import_present(root, src_bytes)
    cls = _binder.classify(root, src_bytes, u_ok)

    # ---- MAP failures ----
    map_fail_items = []
    for b in cls.forbidden:
        map_fail_items.append((b.kind.upper(), b.line, b.snippet))
    for t, (cnt, ex) in sorted(cls.unknown.items()):
        map_fail_items.append(("OUT_OF_SCOPE", ex,
                               f"unbound node type '{t}' (x{cnt}) -- no registry op covers it"))

    # ---- WRAP coverage ----
    coverage_rows = []
    wrap_fail_items = []
    for op_id in cls.bound_op_ids:
        kind, entry = reg.entry(op_id)
        if entry is None:
            wrap_fail_items.append((op_id, "*", "UNREGISTERED", "not-in-registry"))
            coverage_rows.append((op_id, "*", False, "UNREGISTERED", "not-in-registry"))
            continue
        for tgt in targets:
            r = reg.lookup(op_id, tgt)
            coverage_rows.append((op_id, tgt, r.ok, r.strategy, r.status))
            if not r.ok:
                wrap_fail_items.append((op_id, tgt, r.strategy, r.status))

    passed = not map_fail_items and not wrap_fail_items
    return GateResult(
        hub_file=hub_file, targets=targets, u_import_verified=u_ok, passed=passed,
        bound_ops=cls.bound_op_ids, map_failures=map_fail_items,
        wrap_failures=wrap_fail_items, baseline_node_types=cls.baseline_types,
        coverage=coverage_rows, classification=cls,
    )


def check_file(path, targets):
    src = open(path, "rb").read()
    return check(src, targets, hub_file=path)


# ===========================================================================
# REPORT (G1-style; markdown pipe tables only, per the communication protocol)
# ===========================================================================
def format_report(res):
    lines = []
    bar = "=" * 78
    lines.append(bar)
    lines.append("PseudoIR -- REGISTRY GATE (G1)")
    lines.append(bar)
    lines.append(f"Hub file : {res.hub_file}")
    lines.append(f"Targets  : {', '.join(res.targets)}")
    u_note = ("verified" if res.u_import_verified
              else "NOT present (bare coalesce/safe/not_null will NOT bind as ops)")
    lines.append(f"U import  : {u_note}")
    lines.append("")

    lines.append("PER-CONSTRUCT BINDING TABLE")
    lines.append("")
    lines.append("| line | kind | op/xform | construct |")
    lines.append("|---|---|---|---|")
    op_rows = [b for b in res.classification.bindings if b.op_id]
    for b in sorted(op_rows, key=lambda x: x.line):
        snip = b.snippet.replace("\n", " ").strip()
        if len(snip) > 46:
            snip = snip[:43] + "..."
        lines.append(f"| {b.line} | {b.kind} | `{b.op_id}` | `{snip}` |")
    if not op_rows:
        lines.append("| - | - | (none) | no registry ops bound; file is pure baseline |")
    lines.append("")
    total_baseline = sum(res.baseline_node_types.values())
    lines.append(f"Plain-Python baseline nodes: {total_baseline} across "
                 f"{len(res.baseline_node_types)} node types.")
    lines.append("")

    if res.map_failures:
        lines.append("MAP FAILURES (unbound constructs -- neither baseline nor a registered op):")
        for kind, line, snip in res.map_failures:
            lines.append(f"  [{kind}] line {line}: {snip}")
        lines.append("")

    lines.append("PER-OP TARGET-COVERAGE TABLE (WRAP: every bound op must be non-fail + "
                 "confirmed in every active target)")
    lines.append("")
    lines.append("| op/xform | " + " | ".join(res.targets) + " |")
    lines.append("|" + "---|" * (len(res.targets) + 1))
    by_op = {}
    for (o, t, ok, s, st) in res.coverage:
        by_op.setdefault(o, {})[t] = (ok, s, st)
    for o in sorted(by_op):
        cells = []
        for t in res.targets:
            if t in by_op[o]:
                ok, s, st = by_op[o][t]
                cells.append(f"{'OK' if ok else 'FAIL'} ({s})")
            else:
                cells.append("-")
        lines.append(f"| `{o}` | " + " | ".join(cells) + " |")
    lines.append("")

    if res.wrap_failures:
        lines.append("WRAP FAILURES (bound op with a fail/unconfirmed cell in an active target):")
        for (o, t, s, st) in res.wrap_failures:
            lines.append(f"  `{o}` @ {t}: strategy={s}, status={st}")
        lines.append("")

    lines.append(bar)
    lines.append(f"VERDICT: {'PASS' if res.passed else 'FAIL'}")
    if not res.passed:
        reasons = []
        if res.map_failures:
            reasons.append(f"{len(res.map_failures)} unbound construct(s)")
        if res.wrap_failures:
            reasons.append(f"{len(res.wrap_failures)} uncovered op-cell(s)")
        lines.append("Reason: " + "; ".join(reasons) + ".")
    lines.append(bar)
    return "\n".join(lines)


def run(path, targets, as_json=False):
    """Gate a file; print the report (or JSON); return 0 PASS / 1 FAIL."""
    res = check_file(path, targets)
    if as_json:
        print(json.dumps(res.as_dict(), indent=2))
    else:
        print(format_report(res))
    return 0 if res.passed else 1
