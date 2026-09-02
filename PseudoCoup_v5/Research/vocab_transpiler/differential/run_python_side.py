#!/usr/bin/env python3
"""Drive pc_vocab with the SAME instructions and SAME operand keys that
gen_rust_harness.py uses (via common_operands.py), and print

    INSTRNAME|operandkey|hexbytes            on a clean encode
    INSTRNAME|operandkey|CUT|reason          on NotImplementedError
    INSTRNAME|operandkey|ERROR|reason        on any other exception

for every instruction common_operands.py could classify (i.e. the same 973
of 1071 that gen_rust_harness.py emits Rust for -- the 98 Amode-only
instructions are skipped identically on both sides and are not attempted
here either, since pc_vocab's own Mem/GprMem::Mem path is an explicit,
intentional cut -- see vocab_support.py).

This script must never crash: every exception other than a deliberate
`NotImplementedError` is caught and reported as an ERROR line so the run
always completes and produces one line per (instruction, key) attempted.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB_DIR = os.path.normpath(os.path.join(HERE, ".."))
DEFAULT_ASSEMBLER_RS = os.path.normpath(
    os.path.join(HERE, "..", "..", "rust_routing", "sources", "encoder", "asm", "assembler.rs")
)

sys.path.insert(0, HERE)
sys.path.insert(0, VOCAB_DIR)

import common_operands as co  # noqa: E402
from vocab_support import CodeSink, Gpr, GprMem, Xmm, XmmMem, Imm  # noqa: E402
import pc_vocab  # noqa: E402


def python_operand_value(field, value):
    k = field.kind
    if k == "gpr":
        return Gpr(value)
    if k == "gprmem":
        return GprMem(value)
    if k == "xmm":
        return Xmm(value)
    if k == "xmmmem":
        return XmmMem(value)
    if k == "fixed":
        return Gpr(value)      # Gpr doubles as the Fixed<> wrapper (see vocab_support.py)
    if k == "fixed_xmm":
        return Xmm(value)
    if k in co.IMM_FIXED_VALUES:
        return Imm(value, co.IMM_WIDTH_BYTES[k])
    if k == "trap":
        return "T"             # arbitrary marker; only read if isinstance(Mem), never true here
    raise AssertionError(f"unhandled field kind for python construction: {k}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assembler-rs", default=DEFAULT_ASSEMBLER_RS)
    args = ap.parse_args()

    instructions = co.parse_instructions(args.assembler_rs)
    ok, skipped = co.constructible_instructions(instructions)

    counts = {"ok": 0, "cut": 0, "error": 0, "missing_in_pc_vocab": 0}
    error_samples = []

    for name, inst in ok.items():
        cls = pc_vocab.INSTRUCTIONS.get(name)
        if cls is None:
            cls = getattr(pc_vocab, name, None)
        if cls is None:
            for key in co.OPERAND_KEYS:
                print(f"{name}|{key}|ERROR|not found in pc_vocab.INSTRUCTIONS or as module attribute")
            counts["missing_in_pc_vocab"] += 2
            continue

        for key in co.OPERAND_KEYS:
            try:
                values = co.build_operand_values(inst, key)
                pyargs = [python_operand_value(f, v) for f, v in values]
                sink = CodeSink()
                cls(*pyargs).encode(sink)
                print(f"{name}|{key}|{sink.bytes().hex()}")
                counts["ok"] += 1
            except NotImplementedError as e:
                print(f"{name}|{key}|CUT|{e}")
                counts["cut"] += 1
            except Exception as e:
                msg = f"{type(e).__name__}: {e}"
                print(f"{name}|{key}|ERROR|{msg}")
                counts["error"] += 1
                if len(error_samples) < 20:
                    error_samples.append((name, key, msg))

    total_lines = sum(counts.values())
    print(f"# --- run_python_side.py summary ---", file=sys.stderr)
    print(f"# instructions attempted   : {len(ok)} (of {len(instructions)} total; "
          f"{len(skipped)} skipped identically to the Rust side, Amode-only)",
          file=sys.stderr)
    print(f"# lines printed            : {total_lines}", file=sys.stderr)
    print(f"# clean encodes            : {counts['ok']}", file=sys.stderr)
    print(f"# CUT (NotImplementedError): {counts['cut']}", file=sys.stderr)
    print(f"# ERROR (other exception)  : {counts['error']}", file=sys.stderr)
    print(f"# missing from pc_vocab    : {counts['missing_in_pc_vocab']}", file=sys.stderr)
    if error_samples:
        print("# sample ERROR reasons:", file=sys.stderr)
        for name, key, msg in error_samples[:10]:
            print(f"#   {name} [{key}]: {msg}", file=sys.stderr)


if __name__ == "__main__":
    main()
