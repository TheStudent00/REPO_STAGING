#!/usr/bin/env python3
"""
MINIMUM SLICE of every RISC-V float operation, SPECIALISED to the context the
Sail model already fixes.

The previous run sliced each of the 67 operations the Sail RISC-V model
declares (model/core/softfloat_interface.sail) generically.  That was an
over-approximation: Sail never calls SoftFloat with an unknown rounding mode.
c_emulator/riscv_softfloat.cpp does

    softfloat_exceptionFlags = 0;
    softfloat_roundingMode   = uint8_of_rm(rm);

before every call, with `rm` the 3-bit RISC-V rm field, so the mode is one of
five literals (RM_DYN is resolved to one of them before the call).  Pinning it
deletes the arms no RISC-V caller can reach and, for the roundToInt family,
removes the switch jump table entirely.

Two specialisation mechanisms, matching how SoftFloat takes the mode:

 (a) GLOBAL.  For 64 of the 67 operations the mode is read from the global
     softfloat_roundingMode.  A copy of source/softfloat_state.c with the
     initialiser replaced by a literal is linked in; `internalize` makes the
     global internal, `globalopt` sees no writer and marks it constant, and
     `ipsccp` propagates the literal into every comparison.

 (b) PARAMETER.  f16/f32/f64_roundToInt take the mode as an argument.  A tiny
     wrapper per mode calls the operation with the mode as a literal and is the
     only public symbol, so the inliner folds the operation into the wrapper and
     ipsccp kills the dead arms.

GENERIC baseline: the same pipeline with the state file NOT linked, so
softfloat_roundingMode (and exceptionFlags / detectTininess) stay undefined
externals and nothing about the mode can be assumed.  A second baseline,
`generic_rm_unknown`, links the state file but keeps softfloat_roundingMode in
the public API list so only THAT global stays unknown; the difference between
the two isolates the rounding mode from the other two state globals.

Everything is written under SCRATCH.  $SF is read-only throughout.
"""

import hashlib
import json
import os
import shutil
import sys

SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad")
sys.path.insert(0, os.path.join(SCRATCH, "lib"))
import sfcore as C                                        # noqa: E402
import sfmeasure as M                                     # noqa: E402

WORK = os.path.join(SCRATCH, "work", "spec")
BCDIR = os.path.join(WORK, "bc")
GEN = os.path.join(WORK, "gen")                 # pinned state / wrapper sources
OUT = os.path.join(SCRATCH, "slices_spec")

# The RISC-V rm field can only be these five (RM_DYN=0b111 is resolved first).
RISCV_MODES = [0, 1, 2, 3, 4]
# SoftFloat also supports round-odd, which RISC-V never selects; measured for
# completeness because the validation set named it.
EXTRA_MODES = [6]
ALL_MODES = RISCV_MODES + EXTRA_MODES

ADDSUB = ["f16_add", "f16_sub", "f32_add", "f32_sub", "f64_add", "f64_sub"]


def src(name):
    return os.path.join(C.SF, "source", name + ".c")


def build(seeds, entry, tag, wdir, extra_public=(), force_inline=False):
    """compile -> link -> internalize/specialise/inline/DCE -> riscv64 object"""
    files, bcs, unresolved = C.link_closure(seeds, BCDIR)
    api = ",".join([entry] + list(extra_public))
    linked = os.path.join(wdir, tag + ".linked.bc")
    rc, _, err = C.run([C.B + "/llvm-link"] + bcs + ["-o", linked])
    if rc:
        raise RuntimeError("llvm-link: " + err[:300])

    others = []
    if force_inline:
        defined, _ = C.nm(linked)
        others = sorted(s for s in defined if s != entry)

    passes = C.PASSES
    if force_inline:
        passes = passes.replace("internalize,", "internalize,forceattrs,")
    cmd = [C.B + "/opt", "-passes=" + passes,
           "-internalize-public-api-list=" + api]
    for s in others:
        cmd.append("-force-attribute=" + s + ":alwaysinline")
    sbc = os.path.join(wdir, tag + ".bc")
    cmd += [linked, "-o", sbc]
    rc, _, err = C.run(cmd)
    if rc and "did not reach a fixpoint" in err:
        passes = passes.replace("instcombine,", "instcombine<no-verify-fixpoint>,")
        cmd[1] = "-passes=" + passes
        rc, _, err = C.run(cmd)
    if rc:
        raise RuntimeError("opt: " + err[:300])

    sobj = os.path.join(wdir, tag + ".o")
    rc, _, err = C.run([C.B + "/llc", "-march=riscv64", "-mattr=+m", "-O2",
                        "-filetype=obj", sbc, "-o", sobj])
    if rc:
        raise RuntimeError("llc: " + err[:300])

    dis = M.disasm(sobj)
    r, _ = M.measure(sobj, entry, dis)
    if r is None:
        raise RuntimeError("entry symbol %s absent from %s" % (entry, tag))
    psym = C.per_symbol_counts(dis)
    rec = {
        "entry_symbol": entry,
        "instructions": r["instructions"],
        "instructions_all_symbols": sum(psym.values()),
        "per_symbol_instructions": psym,
        "branches": r["branches"],
        "jumps": r["jumps"],
        "back_edges": r["back_edges"],
        "back_edge_spans": r["back_edge_spans"],
        "loop_back_edges": r["loop_back_edges"],
        "loop_back_edge_spans": r["loop_back_edge_spans"],
        "has_loop": r["has_loop"],
        "calls_remaining": r["calls"],
        "calls_remaining_callees": r["callees"],
        "indirect_jumps": len(r["indirect_jumps"]),
        "indirect_jump_detail": r["indirect_jumps"],
        "loads": r["loads"],
        "stores": r["stores"],
        "memory": r["memory"],
        "multiply_divide": r["multiply_divide"],
        "muldiv_ops": r["muldiv_ops"],
        "unreachable_insns": r["unreachable_insns"],
        "size_bytes": r["size_bytes"],
        "surviving_symbols": sorted(M.symbols(sobj)),
        "source_files_linked": [os.path.relpath(f, C.SF)
                                if f.startswith(C.SF) else os.path.basename(f)
                                for f in files],
        "unresolved_externals": unresolved,
        "opt_passes": passes,
    }
    # Normalised disassembly, for the "did pinning change anything" test.
    # Two things must be erased or the test answers the wrong question:
    #   * llvm-objdump's first line names the OBJECT FILE (rm0.o, rm1.o, ...),
    #   * the entry symbol differs per mode for the roundToInt wrappers.
    # Relocations are hashed too: identical .text bytes with different
    # relocation targets would not be the same code.
    relocs = C.run([C.B + "/llvm-readelf", "-r", sobj])[1]
    norm = "\n".join(l for l in dis.splitlines() if "file format" not in l)
    norm = norm.replace(entry, "ENTRY")
    rec["disasm_sha256"] = hashlib.sha256(
        (norm + "\n" + relocs.replace(entry, "ENTRY")).encode()).hexdigest()
    # raw .text bytes, the strongest form of "byte-identical"
    tsec = sobj + ".text.bin"
    rc, _, _ = C.run([C.B + "/llvm-objcopy", "--dump-section=.text=" + tsec,
                      sobj, "/dev/null"])
    rec["text_sha256"] = (hashlib.sha256(open(tsec, "rb").read()).hexdigest()
                          if rc == 0 and os.path.exists(tsec) else None)
    rec["object_sha256"] = hashlib.sha256(open(sobj, "rb").read()).hexdigest()
    return rec, sobj, dis


def emit(op, label, rec, sobj, dis):
    base = "%s.%s" % (op, label)
    shutil.copy(sobj, os.path.join(OUT, base + ".o"))
    with open(os.path.join(OUT, base + ".txt"), "w") as fh:
        fh.write("# %s  [%s]\n# entry symbol: %s\n" % (op, label, rec["entry_symbol"]))
        fh.write("# linked: %s\n" % ", ".join(rec["source_files_linked"]))
        fh.write("# instructions %d (all symbols %d), branches %d, jumps %d,\n"
                 "# indirect jumps %d, natural loops %d, calls %d %s\n"
                 % (rec["instructions"], rec["instructions_all_symbols"],
                    rec["branches"], rec["jumps"], rec["indirect_jumps"],
                    rec["loop_back_edges"], rec["calls_remaining"],
                    rec["calls_remaining_callees"] or ""))
        fh.write("#\n# Branch/jump targets in an unlinked .o live in the\n"
                 "# relocations; the resolved table follows the disassembly.\n\n")
        fh.write(dis)
        fh.write("\n=== resolved relocations (llvm-readelf -r) ===\n")
        fh.write(C.run([C.B + "/llvm-readelf", "-r", sobj])[1])
        fh.write("\n=== measured ===\n")
        fh.write(json.dumps(rec, indent=2))


def main():
    for d in (WORK, BCDIR, GEN, OUT):
        os.makedirs(d, exist_ok=True)
    mapping = json.load(open(os.path.join(C.OLD, "mapping.json")))

    pinned = {m: C.pinned_state(m, GEN) for m in ALL_MODES}

    results, failures = {}, []
    for ent in mapping:
        op = ent["sf"]
        wdir = os.path.join(WORK, op)
        shutil.rmtree(wdir, ignore_errors=True)
        os.makedirs(wdir, exist_ok=True)
        is_param = C.takes_mode_parameter(op)
        base_seeds = [src(op)] + C.ALWAYS

        rec = {"function": op,
               "sail_externals": [m["sail"] for m in mapping if m["sf"] == op],
               "prototype": C.PROTOS.get(op),
               "mechanism": ("parameter_wrapper+pinned_global" if is_param
                             else "pinned_global"),
               "modes": {}}
        try:
            # ---- generic: rounding mode (and the other state globals) unknown
            g, gobj, gdis = build(base_seeds, op, "generic", wdir)
            emit(op, "generic", g, gobj, gdis)
            rec["generic"] = g
            # ---- generic with the state file linked but the mode still unknown
            g2, g2obj, g2dis = build(base_seeds + [C.STATE_SRC], op,
                                     "generic_rmunknown", wdir,
                                     extra_public=("softfloat_roundingMode",))
            emit(op, "generic_rm_unknown", g2, g2obj, g2dis)
            rec["generic_rm_unknown"] = g2

            for m in ALL_MODES:
                if is_param:
                    # the literal mode arrives BOTH ways in the real caller:
                    # softfloat_init(rm) sets the global and uint8_of_rm(rm) is
                    # passed as the argument, so do both
                    wrap, name = C.param_wrapper(op, m, GEN)
                    seeds = [wrap] + base_seeds + [pinned[m]]
                    entry = name
                else:
                    seeds = base_seeds + [pinned[m]]
                    entry = op
                r, sobj, dis = build(seeds, entry, "rm%d" % m, wdir)
                emit(op, "rm%d" % m, r, sobj, dis)
                rec["modes"][str(m)] = r

            # For the twelve float-to-integer conversions the emulator also
            # passes a literal `exact = true`.  Recorded separately so the
            # rounding-mode saving is not conflated with it.
            if is_param and not op.endswith("roundToInt"):
                rec["modes_exact_true"] = {}
                for m in ALL_MODES:
                    wrap, name = C.param_wrapper(op, m, GEN, fix_exact=True)
                    r, sobj, dis = build([wrap] + base_seeds + [pinned[m]],
                                         name, "rm%d_exact" % m, wdir)
                    emit(op, "rm%d.exact_true" % m, r, sobj, dis)
                    rec["modes_exact_true"][str(m)] = r

            if op in ADDSUB:
                fg, fo, fd = build(base_seeds, op, "generic_forced", wdir,
                                   force_inline=True)
                emit(op, "generic.forced", fg, fo, fd)
                rec["generic_forced_inline"] = fg
                rec["modes_forced_inline"] = {}
                for m in ALL_MODES:
                    r, sobj, dis = build(base_seeds + [pinned[m]], op,
                                         "rm%d_forced" % m, wdir,
                                         force_inline=True)
                    emit(op, "rm%d.forced" % m, r, sobj, dis)
                    rec["modes_forced_inline"][str(m)] = r
        except Exception as exc:                            # noqa: BLE001
            failures.append({"function": op, "reason": str(exc)[:500]})
            continue

        # ---------------- mode-affected, decided by MEASUREMENT --------------
        sig5 = {str(m): rec["modes"][str(m)]["disasm_sha256"] for m in RISCV_MODES}
        cnt5 = {str(m): rec["modes"][str(m)]["instructions"] for m in RISCV_MODES}
        affected = len(set(sig5.values())) > 1
        rec["mode_affected"] = affected
        rec["identical_across_riscv_modes"] = not affected
        rec["byte_identical_text_across_riscv_modes"] = len(set(
            rec["modes"][str(m)]["text_sha256"] for m in RISCV_MODES)) == 1
        rec["byte_identical_objects_across_riscv_modes"] = len(set(
            rec["modes"][str(m)]["object_sha256"] for m in RISCV_MODES)) == 1
        rec["instructions_per_riscv_mode"] = cnt5
        # The six add/sub operations keep softfloat_roundPackToF<n> out of line
        # in most modes, so the entry-symbol count alone understates them; the
        # all-symbols count is the honest total for those.
        alls5 = {str(m): rec["modes"][str(m)]["instructions_all_symbols"]
                 for m in RISCV_MODES}
        rec["instructions_all_symbols_per_riscv_mode"] = alls5
        rec["min_instructions_all_symbols"] = min(alls5.values())
        rec["max_instructions_all_symbols"] = max(alls5.values())
        rec["sum_all_riscv_modes_all_symbols"] = sum(alls5.values())
        rec["best_mode"] = min(cnt5, key=lambda k: (cnt5[k], int(k)))
        rec["worst_mode"] = max(cnt5, key=lambda k: (cnt5[k], -int(k)))
        rec["min_instructions"] = min(cnt5.values())
        rec["max_instructions"] = max(cnt5.values())
        rec["sum_all_riscv_modes"] = sum(cnt5.values())
        rec["saving_vs_generic"] = g["instructions"] - rec["min_instructions"]
        rec["saving_vs_generic_rm_unknown"] = (g2["instructions"]
                                              - rec["min_instructions"])
        rec["worst_case_saving_vs_generic"] = (g["instructions"]
                                               - rec["max_instructions"])
        if "modes_exact_true" in rec:
            c5 = {str(m): rec["modes_exact_true"][str(m)]["instructions"]
                  for m in RISCV_MODES}
            rec["instructions_per_riscv_mode_exact_true"] = c5
            rec["min_instructions_exact_true"] = min(c5.values())
            rec["max_instructions_exact_true"] = max(c5.values())
            rec["sum_all_riscv_modes_exact_true"] = sum(c5.values())
        results[op] = rec
        print("%-16s generic %-4d  modes %s  %s" %
              (op, g["instructions"],
               " ".join("%d:%d" % (m, cnt5[str(m)]) for m in RISCV_MODES),
               "AFFECTED" if affected else "independent"), flush=True)

    # --------------------------------- totals ------------------------------
    aff = sorted(k for k, v in results.items() if v["mode_affected"])
    ind = sorted(k for k, v in results.items() if not v["mode_affected"])
    sum_generic = sum(v["generic"]["instructions"] for v in results.values())
    sum_generic_rmu = sum(v["generic_rm_unknown"]["instructions"]
                          for v in results.values())
    sum_min = sum(v["min_instructions"] for v in results.values())
    sum_all5 = sum(v["sum_all_riscv_modes"] if v["mode_affected"]
                   else v["min_instructions"] for v in results.values())
    sum_min_exact = sum(v.get("min_instructions_exact_true", v["min_instructions"])
                        for v in results.values())
    sum_all5_exact = sum(
        (v.get("sum_all_riscv_modes_exact_true", v["sum_all_riscv_modes"])
         if v["mode_affected"] else
         v.get("min_instructions_exact_true", v["min_instructions"]))
        for v in results.values())

    indirect = {k: v["modes"][m]["indirect_jump_detail"]
                for k, v in results.items() for m in v["modes"]
                if v["modes"][m]["indirect_jumps"]}
    indirect_generic = {k: v["generic"]["indirect_jump_detail"]
                        for k, v in results.items()
                        if v["generic"]["indirect_jumps"]}
    loops = {k: v["modes"][m]["loop_back_edge_spans"]
             for k, v in results.items() for m in v["modes"]
             if v["modes"][m]["loop_back_edges"]}
    loops_generic = {k: v["generic"]["loop_back_edge_spans"]
                     for k, v in results.items() if v["generic"]["loop_back_edges"]}
    calls = {}
    for k, v in results.items():
        for m in v["modes"]:
            if v["modes"][m]["calls_remaining"]:
                calls.setdefault(k, {})[m] = v["modes"][m]["calls_remaining_callees"]

    summary = {
        "method": {
            "compile": " ".join([C.CLANG] + C.TARGET + C.DEFINES + C.INCLUDES
                                + ["-emit-llvm", "-c", "<src>.c", "-o", "<x>.bc"]),
            "link": C.B + "/llvm-link <all>.bc -o linked.bc",
            "slice": (C.B + "/opt -passes='" + C.PASSES +
                      "' -internalize-public-api-list=<entry> linked.bc -o slice.bc"),
            "lower": (C.B + "/llc -march=riscv64 -mattr=+m -O2 -filetype=obj "
                      "slice.bc -o slice.o"),
            "count": C.B + "/llvm-objdump -d --no-show-raw-insn slice.o",
            "always_linked": ["source/softfloat_state.c (pinned copy)",
                              "source/s_approxRecipSqrt_1Ks.c",
                              "source/s_approxRecip_1Ks.c"],
            "generic_baseline": ("the two sqrt TABLES linked, softfloat_state.c "
                                 "NOT linked, so softfloat_roundingMode, "
                                 "softfloat_exceptionFlags and "
                                 "softfloat_detectTininess stay undefined "
                                 "externals"),
            "generic_rm_unknown_baseline": (
                "softfloat_state.c linked but softfloat_roundingMode kept in the "
                "public API list, so only the rounding mode stays unknown; "
                "isolates the rounding mode from the other two state globals"),
            "mode_affected_test": (
                "measured, not guessed: the normalised disassembly (entry symbol "
                "name erased) of all five RISC-V modes is hashed; more than one "
                "hash means the operation is mode-affected"),
        },
        "rounding_modes": {
            "source": "$SF/source/include/softfloat.h enum, ~line 70",
            "values": {"softfloat_round_near_even": 0, "softfloat_round_minMag": 1,
                       "softfloat_round_min": 2, "softfloat_round_max": 3,
                       "softfloat_round_near_maxMag": 4, "softfloat_round_odd": 6},
            "riscv_reachable": RISCV_MODES,
            "riscv_note": ("c_emulator/riscv_softfloat.cpp assigns the 3-bit "
                           "RISC-V rm field straight into softfloat_roundingMode; "
                           "encdec_rounding_mode gives RNE=0 RTZ=1 RDN=2 RUP=3 "
                           "RMM=4 DYN=7, and DYN is resolved to one of the five "
                           "before the call, so 5 is the reachable set. "
                           "softfloat_round_odd=6 is SoftFloat's own extra and is "
                           "never selected by RISC-V; measured anyway."),
        },
        "n_operations": len(results),
        "n_failures": len(failures),
        "failures": failures,
        "n_mode_affected": len(aff),
        "n_mode_independent": len(ind),
        "mode_affected": aff,
        "mode_independent": ind,
        "sum_generic": sum_generic,
        "sum_generic_rm_unknown": sum_generic_rmu,
        "sum_of_minimum_slice_per_operation": sum_min,
        "sum_keeping_all_five_modes": sum_all5,
        "saving_min_vs_generic": sum_generic - sum_min,
        "sum_generic_all_symbols": sum(v["generic"]["instructions_all_symbols"]
                                       for v in results.values()),
        "sum_of_minimum_slice_all_symbols": sum(v["min_instructions_all_symbols"]
                                                for v in results.values()),
        "sum_keeping_all_five_modes_all_symbols": sum(
            v["sum_all_riscv_modes_all_symbols"] if v["mode_affected"]
            else v["min_instructions_all_symbols"] for v in results.values()),
        "all_symbols_note": (
            "instructions counts the entry symbol only.  The six add/sub "
            "operations keep softfloat_roundPackToF<n> out of line in every "
            "mode except minMag, where it is folded in, so the *_all_symbols "
            "totals are the honest comparison for that family."),
        "sum_of_minimum_slice_also_pinning_exact_true": sum_min_exact,
        "sum_keeping_all_five_modes_also_pinning_exact_true": sum_all5_exact,
        "exact_true_note": (
            "the twelve float-to-integer conversions are also called with a "
            "literal exact=true; pinning that as well is reported separately so "
            "it is not conflated with the rounding-mode saving"),
        "previous_run_generic_sum": 9769,
        "previous_run_note": ("9769 is the earlier run's sum: different pass "
                              "list, and neither the state file nor the two "
                              "sqrt tables linked.  The comparable generic sum "
                              "under THIS pipeline is sum_generic."),
        "indirect_jumps_in_specialised_slices": indirect,
        "indirect_jumps_in_generic_slices": indirect_generic,
        "natural_loops_in_specialised_slices": loops,
        "natural_loops_in_generic_slices": loops_generic,
        "calls_remaining_in_specialised_slices": calls,
        "operations": results,
    }
    with open(os.path.join(SCRATCH, "softfloat_slices_specialised.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print("\n%d operations, %d failures; affected %d, independent %d"
          % (len(results), len(failures), len(aff), len(ind)))
    print("sum generic %d, sum min %d, sum all-five %d"
          % (sum_generic, sum_min, sum_all5))
    for f in failures:
        print("  FAIL", f["function"], f["reason"][:200])


if __name__ == "__main__":
    main()
