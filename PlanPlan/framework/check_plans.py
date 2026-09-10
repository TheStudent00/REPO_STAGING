#!/usr/bin/env python3
"""Multi-project consistency checker for planning trees.

A thin entry point: builds the `checks.Checker` with every check in
`checks.py`, runs it over the given roots, and prints the report.
`checks.py` holds the checks themselves; this file holds only argument
parsing and the exit-code contract.

Usage:
    python3 PRIVATE/PlanPlan/framework/check_plans.py \
        <root>... [--strict] [--quiet]

Exit codes: 0 = no errors, 1 = errors found, 2 = usage error.

No dependencies beyond the standard library. Imports `checks.py` for
the checks themselves and `planning_model.py` for the shared parsing —
never `render_plan.py`.
"""
import argparse
import os
import sys

import checks
import planning_model  # noqa: F401 — the shared data model checks.py builds on


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("roots", nargs="+", help="one or more planning roots")
    ap.add_argument("--strict", action="store_true",
                     help="promote all warnings to errors")
    ap.add_argument("--quiet", action="store_true",
                     help="print only the summary line")
    args = ap.parse_args()

    programming_root = os.path.expanduser("~/Programming")

    roots_existing = []
    items = []
    for raw in args.roots:
        root = os.path.abspath(os.path.expanduser(raw))
        label = os.path.relpath(root, programming_root)
        if label.startswith(".."):
            label = root
        if not os.path.isdir(root):
            items.append(checks.Finding("ERROR", "missing-root",
                               f"root does not exist: {raw} (resolved {root})"))
            continue
        roots_existing.append((root, label))

    checker = checks.Checker([
        checks.GrammarCheck(),
        checks.ArchiveNameCheck(),
        checks.DanglingPathCheck(),
        checks.DuplicateProseCheck(),
        checks.IdCollisionCheck(),
        checks.RequiredFilesCheck(),
        checks.NodesRegisterCheck(),
        checks.EdgeRegisterCheck(),
        checks.NodeSelfCheck(),
        checks.CheckFrontmatterCheck(),
        checks.ProjectionCheck(),
        checks.DesignationCheck(),
        checks.CompletenessCheck(),
    ])
    items += checker.run_all(roots_existing, programming_root)

    if args.strict:
        for i in items:
            if i.severity == "WARN":
                i.severity = "ERROR"

    n_errors = checker.report(items, roots_existing, args.quiet)
    sys.exit(1 if n_errors else 0)


if __name__ == "__main__":
    main()
