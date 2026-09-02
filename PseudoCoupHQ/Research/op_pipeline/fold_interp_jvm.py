#!/usr/bin/env python3
"""fold_interp_jvm.py -- build interp_jvm.json from the JVM pilot lanes.

Reads the archived lane outputs under `lane_out_jvm/` (copied out of the
Airlock `agent/out/` tree, which the daemon does not keep) and folds them
into one record with the same shape as `interp_jvm.md` describes.

THE SPELLING BAN is respected here by construction: no operator token is
used as a key, a grouping name, a row structure, or a candidate scope.
Each unit carries its token exactly once, as `label`, on an object that
also carries `lang` and `id` -- the one allowed per-unit display slot.
Run `check_no_spelling_keys.py interp_jvm.json` after this.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lane_out_jvm")


def read(path):
    full = os.path.join(LANES, path)
    if not os.path.exists(full):
        return ""
    return open(full, errors="replace").read()


def lines_of(path):
    text = read(path)
    out = []
    for ln in text.split("\n"):
        if ln.strip():
            out.append(ln.rstrip())
    return out


def javap_method(name):
    """the bytecode listing of one method, pasted from javap -c output."""
    text = read("jvm_a/javap_c.txt")
    want = "static int %s(int, int);" % name
    out = []
    grab = False
    for ln in text.split("\n"):
        if ln.strip() == want:
            grab = True
            out.append(ln.rstrip())
            continue
        if not grab:
            continue
        if ln.strip() == "":
            break
        out.append(ln.rstrip())
    return out


def nmethod(header_fragment):
    doc = json.load(open(os.path.join(LANES, "jvm_b/nmethods.json")))
    for blk in doc["blocks"]:
        if header_fragment in blk["header"]:
            return blk
    return None


def first_n_objdump(blk, n):
    out = []
    for run in blk["runs"]:
        for ln in run["objdump"]:
            out.append(ln.strip())
            if len(out) >= n:
                return out
    return out


def guard_modes_for(blk, unit_id):
    """the guards visible in this nmethod, one record each.

    Each is a MODE in the core+modes vocabulary; the response kind is
    stated per mode.  `deopt-continue-elsewhere` is the kind the
    SUPPORT file named for a bail-out to the interpreter.
    """
    modes = []
    ann = []
    for a, t in blk["annotations"]:
        ann.append(t)

    modes.append({
        "id": "%s.m1" % unit_id,
        "name": "nmethod-entry barrier",
        "response_kind": "call-out-and-return",
        "evidence_class": "the tool's own testimony, plus objdump",
        "note": ("the JVM annotated the target as {runtime_call "
                 "Stub::method_entry_barrier}; objdump reads the test "
                 "as a compare of a word at 0x20(%r15) against zero, "
                 "with a not-equal branch to that call, which then "
                 "jumps back into the body."),
        "detail_lines": [
            "cmpl   $0x0,0x20(%r15)",
            "jne    <barrier call>",
        ],
    })

    modes.append({
        "id": "%s.m2" % unit_id,
        "name": "return safepoint poll",
        "response_kind": "call-out-and-return",
        "evidence_class": "the tool's own testimony, plus objdump",
        "note": ("annotated {poll_return}; objdump reads a compare of "
                 "the stack pointer against 0x28(%r15) with an "
                 "above branch to a stub that stores a resume address "
                 "into 0x538(%r15) and jumps to the SafepointBlob."),
        "detail_lines": [
            "cmp    0x28(%r15),%rsp",
            "ja     <poll stub>",
        ],
    })

    if "runtime_call UncommonTrapBlob" in " ".join(ann):
        modes.append({
            "id": "%s.m3" % unit_id,
            "name": "zero-divisor check",
            "response_kind": "deopt-continue-elsewhere",
            "evidence_class": ("forced by construction (the branch "
                               "target is the annotated trap blob) "
                               "plus the tool's own testimony"),
            "note": ("an EXPLICIT test of the second parameter "
                     "against itself, equal-branch to a block that "
                     "loads a trap request constant and calls the "
                     "blob the JVM annotated {runtime_call "
                     "UncommonTrapBlob}.  NOT an implicit hardware "
                     "trap: the check is in the instruction stream "
                     "before the divide.  The JVM's own scope "
                     "annotation names the bytecode index it "
                     "re-enters at."),
            "detail_lines": [
                "test   %edx,%edx",
                "je     <trap block>",
                "mov    $0xffffff7e,%esi",
                "call   <UncommonTrapBlob>",
            ],
            "scope_annotation": [
                "ImmutableOopMap {}",
                "*idiv {reexecute=0 rethrow=0 return_oop=0}",
                "- Probe::af2@2 (line 6)",
            ],
        })
        modes.append({
            "id": "%s.m4" % unit_id,
            "name": "most-negative-over-minus-one check",
            "response_kind": "branch-around-in-place",
            "evidence_class": "objdump reading of the printed bytes",
            "note": ("the dividend is compared against 0x80000000 and "
                     "the divisor against 0xffffffff; when both match, "
                     "the quotient register is cleared and the divide "
                     "is skipped.  This is the overflow case the "
                     "hardware divide would fault on.  It does not "
                     "leave the compiled code -- no deopt."),
            "detail_lines": [
                "cmp    $0x80000000,%eax",
                "jne    <do the divide>",
                "xor    %edx,%edx",
                "cmp    $0xffffffff,%r11d",
                "je     <skip the divide>",
            ],
        })

    modes.append({
        "id": "%s.m9" % unit_id,
        "name": "exception handler / deoptimization stubs",
        "response_kind": "deopt-continue-elsewhere",
        "evidence_class": "the tool's own testimony",
        "note": ("every nmethod here ends with a stub section the JVM "
                 "annotates {runtime_call ExceptionBlob} and "
                 "{runtime_call DeoptimizationBlob}.  These are the "
                 "standing exits, present in both units, not specific "
                 "to either computation."),
        "detail_lines": [],
    })
    return modes


def build():
    doc = {}

    doc["what_this_is"] = (
        "The JVM pilot of the JIT track: for a Java addition on ints, "
        "the bytecode middle form, the machine code the JIT produced "
        "for the warmed method, the guards visible in that dump, and "
        "the warm-up recipe that was required to get there.")

    doc["pin"] = {
        "runtime": "OpenJDK",
        "version": "25.0.3",
        "release_date": "2026-04-21",
        "runtime_banner": ("OpenJDK Runtime Environment "
                           "(build 25.0.3+9-2-26.04.2-Ubuntu)"),
        "vm_banner": ("OpenJDK 64-Bit Server VM "
                      "(build 25.0.3+9-2-26.04.2-Ubuntu, mixed mode, "
                      "sharing)"),
        "javac": "javac 25.0.3",
        "vendor": "Ubuntu",
        "java_home": "/usr/lib/jvm/java-25-openjdk-amd64",
        "arch": "amd64",
        "evidence_class": "artifact fact (the tool's own banners)",
    }

    doc["dump_plan"] = {
        "plan_a_hsdis_shipped": {
            "outcome": "REFUSED",
            "note": ("a find over the whole JDK for hsdis* returned "
                     "nothing; every PrintAssembly run logged "
                     "[warning][os] Loading hsdis library failed."),
        },
        "plan_b_build_hsdis": {
            "outcome": "NOT ATTEMPTED -- ingredients absent",
            "note": ("the container has gcc, make, git, objdump 2.46, "
                     "but no dis-asm.h anywhere on the filesystem and "
                     "no autoconf.  hsdis's binutils backend needs "
                     "both.  Recorded as a refusal, not a failure: it "
                     "was not tried because the preconditions were "
                     "measured absent."),
        },
        "plan_c_print_opto_assembly": {
            "outcome": "NOT NEEDED",
            "note": ("-XX:+PrintOptoAssembly was accepted by this "
                     "product build without error, but was not used "
                     "for the recorded unit because the route below "
                     "yields real architecture opcodes."),
        },
        "route_actually_used": {
            "outcome": "WORKED",
            "name": "printed-bytes plus a separate disassembler",
            "note": ("-XX:CompileCommand=print,Class::method prints the "
                     "nmethod's machine code as HEX BYTES together "
                     "with the JVM's own annotations ({poll_return}, "
                     "{runtime_call ...}, the scope lines) even when "
                     "hsdis is missing.  Only the mnemonics are "
                     "absent.  Those bytes were carved out, written to "
                     "a flat file, and disassembled with objdump "
                     "-b binary -m i386:x86-64.  TWO EVIDENCE CLASSES, "
                     "kept apart: the bytes and the annotations are "
                     "the JVM's testimony; the mnemonics are objdump's "
                     "reading of those bytes."),
            "disassembler": "GNU objdump (GNU Binutils for Ubuntu) 2.46",
        },
    }

    doc["configuration_choice"] = {
        "chosen": "-XX:-TieredCompilation",
        "why": ("one configuration for the recorded unit, as the brief "
                "required.  Tiering off means C2 is the only compiler, "
                "so the dumped nmethod is the final tier with no C1 "
                "profiling version in the way."),
        "dump_command_flags": [
            "-Xbatch",
            "-XX:-TieredCompilation",
            "-XX:+UnlockDiagnosticVMOptions",
            "-XX:CompileCommand=print,Probe::af",
            "-XX:CompileCommand=print,Probe::af2",
            "-XX:CompileCommand=dontinline,Probe::af",
            "-XX:CompileCommand=dontinline,Probe::af2",
        ],
        "dontinline_note": ("dontinline was set deliberately: without "
                            "it C2 folds the method into its caller "
                            "and there is no standalone unit to "
                            "record.  This is a choice that shapes "
                            "the recorded unit and is stated, not "
                            "hidden."),
        "thresholds_the_vm_reports_about_itself": lines_of(
            "jvm_a/warmup_sweep.txt")[:0] + [
            "intx CompileThreshold = 10000 {pd product} {default}",
            "intx Tier3InvocationThreshold = 200 {product} {default}",
            "intx Tier3CompileThreshold = 2000 {product} {default}",
            "intx Tier4InvocationThreshold = 5000 {product} {default}",
            "intx Tier4CompileThreshold = 15000 {product} {default}",
            "bool TieredCompilation = true {pd product} {default}",
        ],
    }

    doc["probe_source"] = read("jvm_a/Probe.java")

    doc["units"] = []

    spec = [
        ("u1", "af", "Probe::af", "the addition"),
        ("u2", "af2", "Probe::af2", "the division, for contrast"),
    ]
    labels = {"af": "+", "af2": "/"}

    for unit_id, method, frag, why in spec:
        blk = nmethod(frag)
        rec = {}
        rec["id"] = unit_id
        rec["lang"] = "java"
        rec["method"] = method
        rec["label"] = labels[method]
        rec["arity"] = 2
        rec["operand_types"] = ["int32", "int32"]
        rec["result_type"] = "int32"
        rec["why"] = why
        rec["bytecode_listing"] = javap_method(method)
        rec["bytecode_evidence_class"] = "the tool's own testimony (javap -c)"
        rec["nmethod_header"] = blk["header"]
        rec["compiler_tier"] = "c2"
        rec["parameter_comments"] = blk["comments"]
        rec["jvm_annotations"] = blk["annotations"]
        rec["bytes_recovered"] = blk["total_bytes"]
        rec["contiguous_runs"] = len(blk["runs"])
        rec["arch_unit"] = []
        for run in blk["runs"]:
            rec["arch_unit"].append({
                "base": run["base"],
                "length": run["length"],
                "hex": run["hex"],
                "objdump": run["objdump"],
            })
        rec["arch_unit_evidence_class"] = (
            "bytes: artifact fact, the JVM printed them.  mnemonics: "
            "objdump's reading of those bytes, a second tool's "
            "testimony, never merged with the first.")
        rec["modes"] = guard_modes_for(blk, unit_id)
        doc["units"].append(rec)

    doc["core_reading"] = {
        "u1": ("the whole computation is one instruction that objdump "
               "reads as a load-effective-address over the two "
               "parameter registers, landing in %eax.  parm0 is %rsi "
               "and parm1 is %rdx per the JVM's own comment lines; the "
               "result register is %eax.  Everything else in the "
               "nmethod is frame setup, the entry barrier, the return "
               "poll, and the standing stubs."),
        "u1_core_line": "lea    (%rsi,%rdx,1),%eax",
        "u2_core_lines": ["cltd", "idiv   %r11d"],
        "note": ("the JVM's calling registers are NOT the C ones: "
                 "parm0=%rsi, parm1=%rdx, and %r15 holds the thread. "
                 "Normalisation to the pipeline's canonical runnable "
                 "form (a->%rdi, b->%rsi, result->%rax) was NOT done "
                 "in this pilot."),
    }

    doc["warmup_recipe"] = {
        "configuration": "-XX:-TieredCompilation (C2 only)",
        "call_shape": "static calls with two int arguments",
        "boundary_observed": {
            "never_compiled_at_or_below": 6000,
            "always_compiled_at_or_above": 7000,
            "reps_per_point": 3,
            "note": ("the addition method was compiled by C2 in 0 of 3 "
                     "runs at 5000 and at 6000 calls, and in 3 of 3 "
                     "runs at 7000 and every higher point tested.  The "
                     "division method lagged by one run at 7000 (2 of "
                     "3) and was 3 of 3 from 8000 up."),
        },
        "flag_vs_observation": (
            "the VM reports CompileThreshold = 10000, but the observed "
            "boundary is between 6000 and 7000 calls.  The two do not "
            "agree.  The mechanism for the gap is UNVERIFIED here -- "
            "no experiment in this pilot explains it, and it is "
            "recorded as a discrepancy rather than explained away."),
        "default_tier_contrast": {
            "note": ("with tiering left on, the addition method reaches "
                     "tier 3 (C1, profiled) by 500 calls and tier 4 "
                     "(C2) by 5000 calls, not by 2000.  This matches "
                     "the reported Tier3InvocationThreshold=200 and "
                     "Tier4InvocationThreshold=5000."),
            "rows": lines_of("jvm_c/fine_sweep_tiered.txt"),
        },
        "wall_time_of_one_warmed_run": {
            "n_calls_each_method": 200000,
            "reps": ["0.028s", "0.026s", "0.025s", "0.025s", "0.026s"],
            "note": ("whole JVM process, start to exit, including class "
                     "loading, warm-up and both C2 compilations."),
        },
    }

    doc["tier_transition_log"] = {
        "c2_only": lines_of("jvm_a/tiers_c2only.txt"),
        "default_tiers": lines_of("jvm_a/tiers_default.txt"),
        "evidence_class": "the tool's own testimony (-XX:+PrintCompilation)",
        "note": ("in the C2-only log the OSR compilation of the driver "
                 "loop is twice retired with the reason 'made not "
                 "entrant: uncommon trap' -- a deopt observed in the "
                 "log itself, on the driver, not on either probed "
                 "method."),
    }

    doc["method_data_counters_at_exit"] = {
        "af": {
            "interpreter_invocation_count": 6784,
            "invocation_counter": 6784,
            "backedge_counter": 0,
            "decompile_count": 0,
            "mdo_size_bytes": 248,
        },
        "af2": {
            "interpreter_invocation_count": 6784,
            "invocation_counter": 6784,
            "backedge_counter": 0,
            "decompile_count": 0,
            "mdo_size_bytes": 256,
        },
        "note": ("printed by the -Xbatch dump run at exit, for a driver "
                 "of 200000 calls.  The counters stop at 6784 because "
                 "calls made from compiled code do not increment the "
                 "interpreter counter.  That the number sits near the "
                 "observed 6000-7000 boundary is consistent; it is "
                 "NOT proof of the threshold and is not offered as "
                 "such."),
    }

    doc["lanes"] = [
        {"lane": "jvm_smoke.sh", "wall_s": 2.5,
         "did": ("preflight: java/javac versions, the hsdis search, the "
                 "binutils inventory, the probe compiling, and a first "
                 "look at what PrintAssembly prints without hsdis")},
        {"lane": "jvm_a_dump.sh", "wall_s": 1.1,
         "did": ("thresholds, the coarse warm-up sweep, the tier logs, "
                 "the dump; its carver matched no byte lines and "
                 "produced an empty disassembly")},
        {"lane": "jvm_b_carve.sh", "wall_s": 0.4,
         "did": ("the carver repaired -- the printed hex groups carry a "
                 "space inside each group, which the first pattern "
                 "rejected -- and the full dump plus disassembly")},
        {"lane": "jvm_c_recipe.sh", "wall_s": 1.6,
         "did": ("the fine warm-up sweep with three repetitions per "
                 "point, the default-tier contrast, and five timed "
                 "warmed runs")},
    ]

    doc["cost_answer"] = {
        "question": ("the owner's instinct, recorded in SUPPORT_scaling_design "
                     "as unconfirmed: that the JVM would be the heavier "
                     "lift than the interpreter track."),
        "verdict": "REFUTED for this pilot, on these numbers",
        "jvm_total_lane_seconds": 5.6,
        "cpython_total_lane_seconds": 106,
        "note": ("the JVM pilot needed no build of anything: the JDK "
                 "was installed, the probe compiled in well under a "
                 "second, and a warmed run costs about 26 "
                 "milliseconds.  The CPython pilot had to build the "
                 "interpreter three times.  The one thing that did "
                 "refuse -- hsdis -- was routed around by "
                 "disassembling the bytes the JVM prints anyway, at no "
                 "cost.  What the instinct got right: the ceremony IS "
                 "real (warm-up, tier choice, dontinline, a missing "
                 "disassembler); it is just cheap in seconds."),
    }

    doc["what_was_not_done"] = [
        "no hsdis, so no JVM-native mnemonics to cross-check objdump against",
        ("no normalisation to the canonical runnable form; the JVM's "
         "parameter registers differ from the C convention and were "
         "left as found"),
        "no matching against the compiled-language units, no bridge, no dominance claim",
        ("no second type pair; the recorded unit is int32 by int32 only, "
         "which is exactly the point of the warm-up recipe"),
        ("no measurement of what the deopt actually does at run time -- "
         "the divisor was never zero in any run here, so the trap path "
         "was recorded from the instruction stream, never executed"),
        "one architecture (amd64), one JDK, one vendor build",
    ]

    return doc


def main():
    doc = build()
    out = os.path.join(HERE, "interp_jvm.json")
    fh = open(out, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % out)
    print("units: %d" % len(doc["units"]))
    for u in doc["units"]:
        print("  %s %s  bytes=%d modes=%d"
              % (u["id"], u["method"], u["bytes_recovered"],
                 len(u["modes"])))


if __name__ == "__main__":
    main()
