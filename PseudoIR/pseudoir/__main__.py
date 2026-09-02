"""
pseudoir CLI (T1.2).

    python -m pseudoir transpile <file> --target <lang> [-o out]
    python -m pseudoir gate <file> --targets a,b [--json]

`transpile` gate-checks against the single target first; on a gate FAIL it prints the
G1 report to stderr and exits nonzero (never emits a partial file). `gate` runs the
Map-Wrap-Fail check for the target set and exits 0 PASS / 1 FAIL.
"""
import argparse
import sys

from . import gate as _gate
from .transpile import transpile_file, GateFailure


def _cmd_transpile(args):
    try:
        out = transpile_file(args.file, args.target)
    except GateFailure as e:
        sys.stderr.write("pseudoir transpile: gate FAILED; refusing to emit.\n\n")
        sys.stderr.write(e.report + "\n")
        return 1
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        sys.stderr.write(f"pseudoir: wrote {args.output} (target {args.target})\n")
    else:
        sys.stdout.write(out)
    return 0


def _cmd_gate(args):
    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    return _gate.run(args.file, targets, as_json=args.json)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pseudoir", description="PseudoIR Hub transpiler + registry gate.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    tp = sub.add_parser("transpile", help="gate-check then transpile a Hub file to a target")
    tp.add_argument("file")
    tp.add_argument("--target", required=True, help="target language (python, typescript, go, dart)")
    tp.add_argument("-o", "--output", help="write to this path instead of stdout")
    tp.set_defaults(func=_cmd_transpile)

    gt = sub.add_parser("gate", help="run the Map-Wrap-Fail gate over a Hub file")
    gt.add_argument("file")
    gt.add_argument("--targets", required=True, help="comma-separated target languages")
    gt.add_argument("--json", action="store_true")
    gt.set_defaults(func=_cmd_gate)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
