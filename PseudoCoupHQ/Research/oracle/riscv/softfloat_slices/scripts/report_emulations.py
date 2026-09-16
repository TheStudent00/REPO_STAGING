#!/usr/bin/env python3
"""Merge the emitter's record and the differential test's verdict into
`emulations/emulations.json`, and print the family table."""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
EMU = os.path.join(BASE, "emulations")
SCRATCH = os.environ.get(
    "EMUL_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/emul")

LANGS = ("c", "cpp", "rust", "go")

TOOLCHAIN = {"c": "clang 21.1.8, -O2 -std=c17",
             "cpp": "clang++ 21.1.8, -O2 -std=c++20",
             "rust": "rustc 1.96.1, -O, edition 2021",
             "go": "go 1.26.0, cgo enabled"}

HELPERS = {
    "ctlz": {
        "c": ["written out",
              "__builtin_clz(0) is undefined; LLVM's ctlz must answer the "
              "bit width here"],
        "cpp": ["built-in std::countl_zero",
                "returns the bit width for 0, which is LLVM's ctlz with "
                "is_zero_poison=false"],
        "rust": ["built-in leading_zeros",
                 "returns the bit width for 0, matching LLVM"],
        "go": ["built-in math/bits.LeadingZeros32/64",
               "returns the bit width for 0, matching LLVM"]},
    "abs": {
        "c": ["written out",
              "C's abs() is int-only and undefined at INT_MIN; llvm.abs "
              "wraps to INT_MIN"],
        "cpp": ["written out",
                "std::abs is undefined at INT_MIN; llvm.abs wraps"],
        "rust": ["built-in wrapping_abs",
                 "wrapping_abs(MIN) == MIN, exactly llvm.abs with "
                 "is_int_min_poison=false; abs() would panic"],
        "go": ["written out", "go has no integer abs; math.Abs is float64"]},
    "usub.sat": {
        "c": ["written out", "C has no saturating subtract"],
        "cpp": ["written out", "C++ has no saturating subtract before C++26"],
        "rust": ["built-in saturating_sub",
                 "unsigned saturating_sub is exactly llvm.usub.sat"],
        "go": ["written out", "go has no saturating subtract"]},
    "fshl": {
        "c": ["written out", "C has no funnel shift"],
        "cpp": ["written out", "std::rotl is only the a == b case"],
        "rust": ["written out",
                 "rust has no stable funnel shift; rotate_left is a == b"],
        "go": ["written out",
               "bits.RotateLeft64 is only the a == b case"]},
}


def main():
    emitted = json.load(open(os.path.join(EMU, "_emitted.json")))
    report = json.load(open(os.path.join(SCRATCH, "report.json")))
    mode = emitted[next(iter(emitted))]["mode"]

    ops = {}
    totals = {lang: {"lines": 0, "tested": 0, "mismatches": 0}
              for lang in LANGS}
    failures = []
    for op in sorted(emitted):
        e = emitted[op]
        rec = {"operation": op,
               "rounding_mode": e["mode"],
               "variant": e["variant"],
               "source": "flattened/%s.rm%d.%s.flat.ll"
                         % (op, e["mode"], e["variant"]),
               "ir_instructions": e["ir_instructions"],
               "llvm_opcodes": e["opcodes"],
               "llvm_intrinsics": e["intrinsics"],
               "integer_widths": e["widths"],
               "i128_needed": e["i128"],
               "i128_split_for_go": e["i128"],
               "languages": {}}
        for lang in LANGS:
            per = report[lang]["per_op"].get(op, [0, 0])
            ex = report[lang]["examples"].get(op, [])
            rec["languages"][lang] = {
                "file": e["languages"][lang]["file"],
                "entry": e["languages"][lang]["entry"],
                "lines": e["languages"][lang]["lines"],
                "inputs_tested": per[0],
                "mismatches": per[1],
                "mismatch_examples": ex[:8],
                "operators_used": e["opcodes"] + ["llvm." + i
                                                  for i in e["intrinsics"]],
                "i128_splitting_needed": e["i128"] and lang == "go",
                "i128_native_used": e["i128"] and lang != "go",
                "toolchain": TOOLCHAIN[lang],
            }
            totals[lang]["lines"] += e["languages"][lang]["lines"]
            totals[lang]["tested"] += per[0]
            totals[lang]["mismatches"] += per[1]
            if per[1]:
                failures.append((op, lang, per[1]))
            if per[0] == 0:
                failures.append((op, lang, "NOT RUN"))
        ops[op] = rec

    out = {
        "what": ("every RISC-V float arch-opcode as ordinary integer source "
                 "in c, c++, rust and go, emitted from the flattened "
                 "single-block LLVM slices and tested bit-exactly against "
                 "Berkeley SoftFloat"),
        "proved": False,
        "tested": True,
        "rounding_mode": mode,
        "variant": "value",
        "n_operations": len(ops),
        "languages": list(LANGS),
        "toolchains": TOOLCHAIN,
        "reference": {
            "implementation": "Berkeley SoftFloat 3e, the copy vendored at "
                              "sail-riscv/dependencies/softfloat/"
                              "berkeley-softfloat-3",
            "specialisation": "source/RISCV",
            "defines": ["-DSOFTFLOAT_FAST_INT64", "-DSOFTFLOAT_ROUND_ODD",
                        "-DINLINE_LEVEL=5", "-DSOFTFLOAT_FAST_DIV32TO16",
                        "-DSOFTFLOAT_FAST_DIV64TO32"],
            "rounding_mode_set_per_call": mode,
            "exact_pinned_true_for": "the twelve float-to-integer conversions",
            "linkage": {"c": "direct", "cpp": 'extern "C"',
                        "rust": 'extern "C"', "go": "cgo"},
        },
        "inputs_per_operation": {
            "edge_cross_product": "+/-0, +/-inf, quiet and signalling NaN, "
                                  "largest and smallest normal, largest and "
                                  "smallest subnormal, +/-1, +/-2, +/-0.5, "
                                  "and one ulp either side of each, crossed "
                                  "over every operand",
            "uniform_random_per_operand": 200000,
            "exponent_banded": 100000,
        },
        "poison_pins": {
            "shift_amount_ge_width": "taken modulo the operand width",
            "ctlz_zero": "the bit width",
            "udiv_by_zero": "zero (the flattener already forces every "
                            "divisor non-zero)",
            "freeze": "a plain copy",
            "unobservable": "scripts/pin_probe.sh re-emits C with the "
                            "opposite reading of all three and gets the same "
                            "zero mismatches",
        },
        "intrinsic_helpers": HELPERS,
        "totals": totals,
        "failures": failures,
        "operations": ops,
    }
    json.dump(out, open(os.path.join(EMU, "emulations.json"), "w"), indent=1)

    fam = [("f16 arithmetic", ["f16_add", "f16_sub", "f16_mul", "f16_div",
                               "f16_mulAdd", "f16_sqrt"]),
           ("f32 arithmetic", ["f32_add", "f32_sub", "f32_mul", "f32_div",
                               "f32_mulAdd", "f32_sqrt"]),
           ("f64 arithmetic", ["f64_add", "f64_sub", "f64_mul", "f64_div",
                               "f64_mulAdd", "f64_sqrt"]),
           ("compare", ["f16_eq", "f16_lt", "f16_le", "f32_eq", "f32_lt",
                        "f32_le", "f64_eq", "f64_lt", "f64_le"]),
           ("roundToInt", ["f16_roundToInt", "f32_roundToInt",
                           "f64_roundToInt"]),
           ("float->float", ["f16_to_f32", "f16_to_f64", "f32_to_f16",
                             "f32_to_f64", "f32_to_bf16", "f64_to_f16",
                             "f64_to_f32"]),
           ("float->int", ["f16_to_i32", "f16_to_i64", "f16_to_ui32",
                           "f16_to_ui64", "f32_to_i32", "f32_to_i64",
                           "f32_to_ui32", "f32_to_ui64", "f64_to_i32",
                           "f64_to_i64", "f64_to_ui32", "f64_to_ui64"]),
           ("int->float", ["i32_to_f16", "i32_to_f32", "i32_to_f64",
                           "i64_to_f16", "i64_to_f32", "i64_to_f64",
                           "ui32_to_f16", "ui32_to_f32", "ui32_to_f64",
                           "ui64_to_f16", "ui64_to_f32", "ui64_to_f64"])]
    print("| operation | c | cpp | rust | go |")
    print("|---|---|---|---|---|")
    for op in sorted(ops):
        r = ops[op]["languages"]
        print("| %s | %d | %d | %d | %d |"
              % (op, r["c"]["lines"], r["cpp"]["lines"], r["rust"]["lines"],
                 r["go"]["lines"]))
    print()
    print("| family | ops | c | cpp | rust | go |")
    print("|---|---|---|---|---|---|")
    for name, members in fam:
        s = {lang: sum(ops[m]["languages"][lang]["lines"] for m in members)
             for lang in LANGS}
        print("| %s | %d | %d | %d | %d | %d |"
              % (name, len(members), s["c"], s["cpp"], s["rust"], s["go"]))
    print()
    for lang in LANGS:
        t = totals[lang]
        print("%-5s lines %6d   inputs %10d   mismatches %d"
              % (lang, t["lines"], t["tested"], t["mismatches"]))
    print("failures: %s" % (failures or "none"))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
