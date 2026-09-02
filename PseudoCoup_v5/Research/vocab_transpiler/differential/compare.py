#!/usr/bin/env python3
"""Compare harness_out.txt (Rust, real cranelift-assembler-x64) against
python_out.txt (pc_vocab) and write report.txt.

Line formats understood, matched by (instrname, operandkey):
    NAME|KEY|HEXBYTES          -- a clean encode
    NAME|KEY|CUT|reason        -- python-side marked cut (NotImplementedError)
    NAME|KEY|ERROR|reason      -- python-side unexpected exception
Rust lines are only ever the first form; anything an instruction the Rust
harness couldn't build is simply absent from harness_out.txt (see
SKIPPED_RUST.txt) rather than printed with a sentinel.

Exit code: 0 if zero byte mismatches (SKIP/CUT/ERROR/one-sided-presence do
not count as mismatches, only as incomplete coverage), nonzero otherwise.
"""
import argparse
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_lines(path):
    """Return dict (name,key) -> ('OK', hexbytes) | ('CUT', reason) | ('ERROR', reason)."""
    out = OrderedDict()
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 3:
                continue
            name, key = parts[0], parts[1]
            if parts[2] in ("CUT", "ERROR"):
                reason = "|".join(parts[3:])
                out[(name, key)] = (parts[2], reason)
            else:
                hexbytes = parts[2]
                out[(name, key)] = ("OK", hexbytes)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rust", default=os.path.join(HERE, "harness_out.txt"))
    ap.add_argument("--python", default=os.path.join(HERE, "python_out.txt"))
    ap.add_argument("--report", default=os.path.join(HERE, "report.txt"))
    ap.add_argument("--skipped-rust", default=os.path.join(HERE, "SKIPPED_RUST.txt"))
    args = ap.parse_args()

    rust = parse_lines(args.rust)
    python = parse_lines(args.python)

    all_keys = list(OrderedDict.fromkeys(list(rust.keys()) + list(python.keys())))

    exact_matches = []
    mismatches = []
    rust_only = []
    python_only = []
    python_cut = []
    python_error = []

    for k in all_keys:
        r = rust.get(k)
        p = python.get(k)
        if r is not None and p is None:
            rust_only.append(k)
            continue
        if r is None and p is not None:
            python_only.append(k)
            if p[0] == "CUT":
                python_cut.append((k, p[1]))
            elif p[0] == "ERROR":
                python_error.append((k, p[1]))
            continue
        # both present
        if p[0] == "CUT":
            python_cut.append((k, p[1]))
            continue
        if p[0] == "ERROR":
            python_error.append((k, p[1]))
            continue
        # both are OK-form
        if r[1] == p[1]:
            exact_matches.append(k)
        else:
            mismatches.append((k, r[1], p[1]))

    rust_skipped = []
    if os.path.exists(args.skipped_rust):
        with open(args.skipped_rust) as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                rust_skipped.append(line)

    total_pairs_compared = len(exact_matches) + len(mismatches)

    lines = []
    lines.append("=== Differential test report: Rust (cranelift-assembler-x64) vs Python (pc_vocab) ===")
    lines.append("")
    lines.append(f"Rust output lines read     : {len(rust)}")
    lines.append(f"Python output lines read   : {len(python)}")
    lines.append("")
    lines.append(f"Total (instr,key) pairs present on BOTH sides with concrete bytes: {total_pairs_compared}")
    lines.append(f"  exact byte matches       : {len(exact_matches)}")
    lines.append(f"  MISMATCHES               : {len(mismatches)}")
    lines.append("")
    lines.append(f"Python-side CUT (NotImplementedError)  : {len(python_cut)}")
    lines.append(f"Python-side ERROR (unexpected exception): {len(python_error)}")
    lines.append(f"Rust-only lines (no Python counterpart) : {len(rust_only)}")
    lines.append(f"Python-only lines (no Rust counterpart, excluding CUT/ERROR accounted above): "
                 f"{len([k for k in python_only if python.get(k, (None,))[0] == 'OK'])}")
    lines.append(f"Instructions the Rust harness could not construct at all (SKIPPED_RUST.txt): {len(rust_skipped)}")
    lines.append("")

    if mismatches:
        lines.append("--- MISMATCHES (instr, key): rust_bytes vs python_bytes ---")
        for (name, key), rb, pb in mismatches:
            lines.append(f"  {name} [{key}]: rust={rb}  python={pb}")
        lines.append("")

    if python_error:
        lines.append("--- Python-side ERRORs (possible transpiler bugs, not fixed here) ---")
        for (name, key), reason in python_error:
            lines.append(f"  {name} [{key}]: {reason}")
        lines.append("")

    if rust_only:
        lines.append("--- Rust-only (instr,key) pairs (no matching Python line found) ---")
        for name, key in rust_only[:100]:
            lines.append(f"  {name} [{key}]")
        if len(rust_only) > 100:
            lines.append(f"  ... and {len(rust_only) - 100} more")
        lines.append("")

    py_only_ok = [k for k in python_only if python.get(k, (None,))[0] == "OK"]
    if py_only_ok:
        lines.append("--- Python-only (instr,key) pairs with a clean encode but no Rust line ---")
        lines.append("(expected while the Rust harness has not actually been run -- see README)")
        for name, key in py_only_ok[:20]:
            lines.append(f"  {name} [{key}]")
        if len(py_only_ok) > 20:
            lines.append(f"  ... and {len(py_only_ok) - 20} more")
        lines.append("")

    lines.append("--- Rust-side SKIPs (SKIPPED_RUST.txt), by reason ---")
    reason_counts = {}
    for line in rust_skipped:
        name, _, reason = line.partition("\t")
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  {count:4d}  {reason}")
    lines.append("")

    verdict = "PASS (no byte mismatches)" if not mismatches else f"FAIL ({len(mismatches)} byte mismatches)"
    lines.append(f"VERDICT: {verdict}")

    report_text = "\n".join(lines) + "\n"
    with open(args.report, "w") as f:
        f.write(report_text)
    print(report_text)

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
