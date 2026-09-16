#!/usr/bin/env python3
"""results.json -> flattened/flattened.json, plus the tables for the report."""
import json
import os
import sys

HOME = os.path.expanduser("~")   # no machine path is written into this file

ROOT = ("/tmp/claude-1000/-home-<user>-Programming/"
        "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/fl")
OUT = (HOME + "/Programming/PRIVATE/PseudoCoupHQ/Research/oracle/riscv/"
       "softfloat_slices/flattened")
MODES = [0, 1, 2, 3, 4]

FAMILY = [
    ("arithmetic", ["f16_add", "f16_sub", "f16_mul", "f16_div",
                    "f32_add", "f32_sub", "f32_mul", "f32_div",
                    "f64_add", "f64_sub", "f64_mul", "f64_div"]),
    ("fused multiply-add", ["f16_mulAdd", "f32_mulAdd", "f64_mulAdd"]),
    ("square root", ["f16_sqrt", "f32_sqrt", "f64_sqrt"]),
    ("float to integer", ["f16_to_i32", "f16_to_ui32", "f16_to_i64",
                          "f16_to_ui64", "f32_to_i32", "f32_to_ui32",
                          "f32_to_i64", "f32_to_ui64", "f64_to_i32",
                          "f64_to_ui32", "f64_to_i64", "f64_to_ui64"]),
    ("integer to float", ["i32_to_f16", "ui32_to_f16", "i64_to_f16",
                          "ui64_to_f16", "i32_to_f32", "ui32_to_f32",
                          "i64_to_f32", "ui64_to_f32", "i32_to_f64",
                          "ui32_to_f64", "i64_to_f64", "ui64_to_f64"]),
    ("float to float", ["f16_to_f32", "f16_to_f64", "f32_to_f64",
                        "f32_to_f16", "f64_to_f16", "f64_to_f32",
                        "f32_to_bf16"]),
    ("compare", ["f16_lt", "f16_lt_quiet", "f16_le", "f16_le_quiet", "f16_eq",
                 "f32_lt", "f32_lt_quiet", "f32_le", "f32_le_quiet", "f32_eq",
                 "f64_lt", "f64_lt_quiet", "f64_le", "f64_le_quiet",
                 "f64_eq"]),
    ("round to integer", ["f16_roundToInt", "f32_roundToInt",
                          "f64_roundToInt"]),
]


def why(p):
    """The first thing that stops an operation being a clean single block."""
    for key, v in sorted(p["modes"].items()):
        for k in ("refused", "error", "verify_error"):
            if v.get(k):
                return "%s: %s: %s" % (key, k, v[k])
        if v.get("branches") or v.get("jumps") or v.get("calls") \
                or v.get("memory_data") or v.get("blocks") != 1:
            return ("%s: branches=%s jumps=%s calls=%s data_memory=%s "
                    "blocks=%s" % (key, v.get("branches"), v.get("jumps"),
                                   v.get("calls"), v.get("memory_data"),
                                   v.get("blocks")))
    return "?"


def main():
    res = json.load(open(os.path.join(ROOT, "results.json")))
    ex = {r["tag"]: r for r in
          json.load(open(os.path.join(ROOT, "results_exact.json")))}
    for r in res:
        e = ex.get(r["tag"], {})
        r["exact_ir_inputs_tested"] = e.get("inputs_tested", 0)
        r["exact_ir_mismatches"] = e.get("mismatches")
        if e.get("error"):
            r["exact_ir_error"] = e["error"]
    by = {(r["operation"], r["mode"], r["variant"]): r for r in res}
    ops = []
    seen = set()
    for _, fam in FAMILY:
        for o in fam:
            if o not in seen:
                seen.add(o)
                ops.append(o)

    per_op = {}
    for op in ops:
        rec = {"operation": op, "modes": {}}
        for m in MODES:
            for v in ("value", "flags"):
                r = by.get((op, m, v))
                if r is None:
                    continue
                key = "%d.%s" % (m, v)
                rec["modes"][key] = {
                    k: r.get(k) for k in
                    ("entry", "sliced_instructions", "sliced_branches",
                     "sliced_blocks", "sliced_memory",
                     "instructions", "branches", "jumps", "calls", "memory",
                     "memory_stack_spill", "memory_data", "blocks",
                     "ir_instructions", "size_bytes", "inputs_tested",
                     "mismatches", "ir_identical_host_vs_riscv",
                     "exact_ir_inputs_tested", "exact_ir_mismatches",
                     "refused", "error", "verify_error")
                    if r.get(k) is not None}
                rec["modes"][key]["guarded"] = r.get("guarded", [])
                rec["modes"][key]["tables_lowered"] = r.get("tables_lowered",
                                                            [])
        vals = [rec["modes"]["%d.value" % m] for m in MODES
                if "%d.value" % m in rec["modes"]]
        if vals:
            rec["value_instructions_per_mode"] = {
                str(m): rec["modes"]["%d.value" % m]["instructions"]
                for m in MODES if "%d.value" % m in rec["modes"]}
            rec["min_instructions_value"] = min(
                v["instructions"] for v in vals)
            rec["max_instructions_value"] = max(
                v["instructions"] for v in vals)
            rec["sliced_min_instructions_value"] = min(
                v["sliced_instructions"] for v in vals)
        flg = [rec["modes"]["%d.flags" % m] for m in MODES
               if "%d.flags" % m in rec["modes"]]
        if flg:
            rec["min_instructions_flags"] = min(
                v["instructions"] for v in flg)
        rec["all_single_block"] = all(
            v.get("blocks") == 1 for v in rec["modes"].values())
        rec["all_branch_free"] = all(
            v.get("branches") == 0 and v.get("jumps") == 0
            for v in rec["modes"].values())
        rec["all_call_free"] = all(v.get("calls") == 0
                                   for v in rec["modes"].values())
        rec["all_data_memory_free"] = all(v.get("memory_data") == 0
                                          for v in rec["modes"].values())
        rec["inputs_tested"] = sum(v.get("inputs_tested", 0)
                                   for v in rec["modes"].values())
        rec["mismatches"] = sum(v.get("mismatches", 0)
                                for v in rec["modes"].values())
        rec["exact_ir_inputs_tested"] = sum(
            v.get("exact_ir_inputs_tested", 0) for v in rec["modes"].values())
        rec["exact_ir_mismatches"] = sum(
            v.get("exact_ir_mismatches", 0) or 0
            for v in rec["modes"].values())
        per_op[op] = rec

    good = [o for o in ops if per_op[o]["all_single_block"]
            and per_op[o]["all_branch_free"] and per_op[o]["all_call_free"]
            and per_op[o]["all_data_memory_free"]]
    bad = [o for o in ops if o not in good]

    sum_flat_value = sum(per_op[o]["min_instructions_value"] for o in ops
                         if "min_instructions_value" in per_op[o])
    sum_slice_value = sum(per_op[o]["sliced_min_instructions_value"]
                          for o in ops
                          if "sliced_min_instructions_value" in per_op[o])
    sum_flat_flags = sum(per_op[o]["min_instructions_flags"] for o in ops
                         if "min_instructions_flags" in per_op[o])
    sum_all_modes_value = sum(
        sum(per_op[o]["value_instructions_per_mode"].values())
        for o in ops if "value_instructions_per_mode" in per_op[o])
    largest = max(((per_op[o].get("min_instructions_value", 0), o)
                   for o in ops))

    summary = {
        "what": ("every RISC-V float operation as ONE basic block of pure "
                 "arithmetic: no branches, no memory, no calls"),
        "chain": [
            "slice with the caller's context pinned (-Oz, rounding mode a "
            "literal, `exact` a literal, everything but the entry forced "
            "inline)",
            "localise the state globals (scripts/localise.py), then "
            "sroa/instcombine/simplifycfg, which removes all memory",
            "flatten the DAG to one block (scripts/flatten_dag.py)",
            "lower every select, phi and min/max to mask arithmetic",
            "early-cse,instsimplify,dce,globaldce - no pass that can invent "
            "control flow",
            "llc -march=riscv64 -mattr=+m -O2 "
            "--riscv-disable-using-constant-pool-for-large-ints",
        ],
        "n_operations": len(ops),
        "n_single_block_branch_free_memory_free_call_free": len(good),
        "not_clean": {o: why(per_op[o]) for o in bad},
        "sum_flattened_value_best_mode": sum_flat_value,
        "sum_sliced_value_best_mode": sum_slice_value,
        "sum_flattened_flags_best_mode": sum_flat_flags,
        "sum_flattened_value_all_five_modes": sum_all_modes_value,
        "published_sliced_total_best_mode_O1": 8160,
        "largest": {"operation": largest[1], "instructions": largest[0]},
        "inputs_tested_total": sum(per_op[o]["inputs_tested"] for o in ops),
        "mismatches_total": sum(per_op[o]["mismatches"] for o in ops),
        "operations_with_mismatches": [o for o in ops
                                       if per_op[o]["mismatches"]],
        "exact_ir_inputs_tested_total": sum(
            r.get("exact_ir_inputs_tested", 0) for r in res),
        "exact_ir_mismatches_total": sum(
            r.get("exact_ir_mismatches") or 0 for r in res),
        "host_and_riscv_ir_identical": sum(
            1 for r in res if r.get("ir_identical_host_vs_riscv")),
        "host_and_riscv_ir_compared": sum(
            1 for r in res if "ir_identical_host_vs_riscv" in r),
        "guarded_instructions": {
            r["tag"]: r["guarded"] for r in res if r.get("guarded")},
        "tables_lowered": {
            r["tag"]: r["tables_lowered"] for r in res
            if r.get("tables_lowered")},
        "verification": {
            "method": ("the ORIGINAL slice and the FLATTENED one, both built "
                       "for the host from the same sources by the same "
                       "slicer, linked into one binary with a generated "
                       "driver and given identical inputs; the returned bits "
                       "are compared exactly, and the exception flags too for "
                       "the `flags` variant"),
            "random_per_operand": 200000,
            "structured_random_per_operand": 100000,
            "edge_cases": ("+/-0, +/-inf, quiet and signalling NaN, largest "
                           "and smallest normal, largest and smallest "
                           "subnormal, +/-0.5 +/-1 +/-2, and one ulp either "
                           "side of every one of those; the full cross "
                           "product over all operands"),
        },
        "per_operation": per_op,
    }
    os.makedirs(OUT, exist_ok=True)
    json.dump(summary, open(os.path.join(OUT, "flattened.json"), "w"),
              indent=1)

    # ------- report tables -------
    print("| family | operation | sliced | flattened | branches after | "
          "blocks after |")
    print("|---|---|---|---|---|---|")
    for fam, members in FAMILY:
        for o in members:
            p = per_op.get(o)
            if not p or "min_instructions_value" not in p:
                print("| %s | `%s` | ? | ? | ? | ? |" % (fam, o))
                continue
            m1 = p["modes"].get("1.value") or list(p["modes"].values())[0]
            print("| %s | `%s` | %d | %d | %d | %d |"
                  % (fam, o, m1["sliced_instructions"], m1["instructions"],
                     m1["branches"] + m1["jumps"], m1["blocks"]))
    print()
    print("single block + no branch + no call + no data memory: %d / %d"
          % (len(good), len(ops)))
    if bad:
        print("NOT CLEAN:", summary["not_clean"])
    print("sum flattened (value, best mode)  : %d" % sum_flat_value)
    print("sum sliced    (value, best mode)  : %d" % sum_slice_value)
    print("sum flattened (flags, best mode)  : %d" % sum_flat_flags)
    print("sum flattened (value, all 5 modes): %d" % sum_all_modes_value)
    print("largest: %s at %d" % (largest[1], largest[0]))
    print("inputs tested: %d   mismatches: %d"
          % (summary["inputs_tested_total"], summary["mismatches_total"]))
    print("exact-IR pass: %d inputs, %d mismatches"
          % (summary["exact_ir_inputs_tested_total"],
             summary["exact_ir_mismatches_total"]))
    print("host/riscv IR identical: %d of %d"
          % (summary["host_and_riscv_ir_identical"],
             summary["host_and_riscv_ir_compared"]))


if __name__ == "__main__":
    main()
