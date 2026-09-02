#!/usr/bin/env python3
"""fold the CPython interpreter-track pilot into interp_cpython.json.

Reads the Airlock lane outputs (interp_b3, interp_c, interp_d) and
writes one record: pin, build flags, probe sources, the bytecode
middle form, the measured dispatch path, and the handler arch-units.

usage: fold_interp_cpython.py AIRLOCK_OUT_DIR DEST.json
"""

import json
import os
import re
import sys

OUTDIR = sys.argv[1]
DEST = sys.argv[2]

annot_path = os.path.join(OUTDIR, "interp_c", "annotated.txt")
byte_path = os.path.join(OUTDIR, "interp_b3", "bytecode.txt")
probe_dir = os.path.join(OUTDIR, "interp_b3", "probes")
au_anchor = os.path.join(OUTDIR, "interp_d", "arch_units_anchor.json")
au_ship = os.path.join(OUTDIR, "interp_d", "arch_units_ship.json")

fh = open(byte_path, "r")
bytecode_text = fh.read()
fh.close()

probes = {}
for name in sorted(os.listdir(probe_dir)):
    fh = open(os.path.join(probe_dir, name), "r")
    probes[name] = fh.read()
    fh.close()

records = {}
cur_run = None
cur_fn = None
line_re = re.compile(
    r"^\s+(\S+):(\d+)\s+delta=(-?\d+)\s+probe=(\d+)\s+baseline=(\d+)\s+\|(.*)$")

fh = open(annot_path, "r")
for line in fh:
    line = line.rstrip("\n")
    if line.startswith("################ "):
        cur_run = line.strip("# ").strip()
        records[cur_run] = []
        continue
    if line.strip().startswith("--- inside: "):
        cur_fn = line.split("--- inside: ", 1)[1].strip()
        continue
    m = line_re.match(line)
    if m is None:
        continue
    rec = {
        "file": m.group(1),
        "line": int(m.group(2)),
        "delta": int(m.group(3)),
        "count_probe_run": int(m.group(4)),
        "count_baseline_run": int(m.group(5)),
        "enclosing_definition": cur_fn,
        "source": m.group(6),
        "evidence": "tally (gcov line counters, per-run, order lost)",
    }
    records[cur_run].append(rec)
fh.close()


def load_units(path):
    fh = open(path, "r")
    d = json.load(fh)
    fh.close()
    out = {}
    for sym in d:
        u = d[sym]
        out[sym] = {
            "symbol": sym,
            "load_address": "0x" + u["addr"],
            "instruction_count": len(u["instructions"]),
            "instructions": u["instructions"],
            "evidence": "artifact fact (objdump of the built binary)",
        }
    return out


doc = {
    "meta": {
        "what": ("CPython pilot of the interpreter track: which "
                 "interpreter handler actually executes for a Python "
                 "addition on ints, measured; the bytecode middle "
                 "form; and the handler extracted from the "
                 "interpreter binary as an arch-unit."),
        "date": "2026-08-26",
        "home": ("Planning/node_0_3_research/node_0_3_5_compiler_graph/"
                 "SUPPORT_scaling_design.md, interpreter-track section"),
        "pin": {
            "project": "cpython",
            "tag": "v3.14.7",
            "commit": "823f0323ee6ec1402088b73bce1a38473cac36dc",
            "patchlevel_h": "PY_MAJOR 3 / PY_MINOR 14 / PY_MICRO 7 / FINAL",
            "runtime_banner": ("3.14.7 (tags/v3.14.7:823f032, Aug 26 2026) "
                               "[GCC 15.2.0]"),
            "clone": "git clone --depth 1 --branch v3.14.7",
            "evidence": "artifact fact (git rev-parse in the build lane)",
        },
        "builds": {
            "coverage": {
                "where": "/persist/cpython (Airlock)",
                "configure": ("./configure --disable-test-modules "
                              "CFLAGS=\"--coverage -O0 -g -fwrapv\" "
                              "LDFLAGS=\"--coverage\""),
                "actual_compile_line_longobject": (
                    "gcc -c -fno-strict-overflow -Wsign-compare -DNDEBUG -g "
                    "-O3 -Wall --coverage -O0 -g -fwrapv -std=c11 -Wextra ... "
                    "-DPy_BUILD_CORE -o Objects/longobject.o "
                    "Objects/longobject.c"),
                "note": ("CPython's own OPT (-O3) is placed BEFORE the "
                         "CFLAGS we passed, so the trailing -O0 is the "
                         "optimisation level that took effect. Read off "
                         "the make log, not assumed."),
                "used_for": "the dispatch measurement (lanes B/B3)",
            },
            "anchor": {
                "where": "/persist/cpython_anchor (Airlock)",
                "configure": ("./configure --disable-test-modules "
                              "CFLAGS=\"-O0 -g -fwrapv\""),
                "used_for": "the arch-unit slice, optimizer off",
                "gcov_symbols_present": 0,
            },
            "ship": {
                "where": "/persist/cpython_ship (Airlock)",
                "configure": "./configure --disable-test-modules",
                "effective_opt": "-DNDEBUG -g -O3 -Wall",
                "used_for": "the arch-unit slice, optimized",
                "gcov_symbols_present": 0,
            },
        },
        "lanes": [
            {"name": "interp_smoke.sh", "elapsed_s": 0.6,
             "did": "preflight + release-tag listing (the pin came from here)"},
            {"name": "interp_a_build.sh", "elapsed_s": 31.4,
             "did": "clone at the pin + coverage configure/make"},
            {"name": "interp_b_dispatch.sh", "elapsed_s": 3.4,
             "did": ("bytecode capture + first coverage attempt; the gcov "
                     "invocation was wrong (run from the output directory, "
                     "so gcov could not find the sources) and produced "
                     "header-only captures. Kept in the record as the "
                     "failed first attempt.")},
            {"name": "interp_b2_parse.sh", "elapsed_s": 0.0,
             "did": "showed the header-only .gcov bytes, diagnosing the above"},
            {"name": "interp_b3_dispatch.sh", "elapsed_s": 4.6,
             "did": "the dispatch measurement, gcov run from the build tree"},
            {"name": "interp_c_slice.sh", "elapsed_s": 1.6,
             "did": ("annotated the measured lines with source text and "
                     "enclosing definition; sliced the coverage binary "
                     "-- those slices carry __gcov0 counters and are NOT "
                     "the arch-unit")},
            {"name": "interp_d_clean.sh", "elapsed_s": 64.3,
             "did": "uninstrumented anchor + ship builds, and their slices"},
        ],
        "method": {
            "dispatch": ("DIFFERENTIAL coverage. A baseline probe runs the "
                         "same loop shape without the probed addition; the "
                         "addition probes run the same loop with it; the "
                         "difference in gcov line counts is what the "
                         "addition reached."),
            "baseline_caveat": ("the baseline is NOT addition-free: its "
                                "loop counter step is itself an addition, "
                                "which is why baseline counts on the "
                                "handler lines are near 100000 rather than "
                                "0. The DELTA is still exactly the 100000 "
                                "probed calls."),
            "instrument_honesty": ("This is a TALLY (coverage counters): "
                                   "how many times, order lost. The node's "
                                   "standing rule prefers a DIARY (order "
                                   "preserved). For this pilot the tally is "
                                   "accepted as the first instrument; the "
                                   "diary pattern (id-emission into the "
                                   "interpreter's own source) is a later "
                                   "lap and is NOT done here."),
        },
        "evidence_classes": {
            "pin_and_flags": "artifact fact (git and the make log)",
            "bytecode_listing": "the tool's own testimony (dis, this build)",
            "dispatch_path": ("tally, per-run: fact FOR THESE RUNS on this "
                              "build; it does not bound all runs"),
            "arch_units": "artifact fact (objdump of the built binary)",
            "expectations": "interpretation, marked as such below",
        },
        "expectations_stated_in_the_brief": {
            "text": ("The brief expected the ceval dispatch plus long_add "
                     "in Objects/longobject.c. MEASURED OUTCOME: partly "
                     "right, and more specific than expected -- see "
                     "findings. This entry is INTERPRETATION recorded for "
                     "comparison, not evidence."),
            "class": "interpretation",
        },
    },
    "probe_sources": probes,
    "bytecode_middle_form": {
        "text": bytecode_text,
        "evidence": "the tool's own testimony (dis on this build)",
        "note": ("two listings: as compiled, and after 100000 warm calls "
                 "with an int pair. The second is the adaptive form."),
    },
    "dispatch_path_measured": records,
    "handler_arch_units": {
        "anchor": load_units(au_anchor),
        "ship": load_units(au_ship),
        "not_found_in_ship": ["_PyLong_FromSTwoDigits", "long_normalize"],
        "not_found_note": ("both are static and were absorbed by the "
                           "optimizer in the ship build; they carry their "
                           "own symbols in the anchor build. Frontier "
                           "recorded rather than guessed at."),
    },
    "findings": [
        {"id": "F1",
         "text": ("The handler that executed is NOT the generic dispatch "
                  "the brief expected. After warm-up the interpreter runs "
                  "a SPECIALIZED case, TARGET(BINARY_OP_ADD_INT), at "
                  "Python/generated_cases.c.h:142-199, delta 99999 on "
                  "every line of it."),
         "evidence": "tally, per-run"},
        {"id": "F2",
         "text": ("That case calls _PyLong_Add "
                  "(generated_cases.c.h:187, delta 99999), which is a "
                  "13-instruction forwarder to long_add "
                  "(Objects/longobject.c:3773). So long_add WAS reached -- "
                  "the expectation held, one call deeper than stated."),
         "evidence": ("tally, per-run + artifact fact (the anchor slice "
                      "shows the call)")},
        {"id": "F3",
         "text": ("The small-int fast path is visible in the counts. For "
                  "the small pair, long_add took the compact branch: "
                  "longobject.c:3740 _PyLong_BothAreCompact delta 100000, "
                  ":3741 stwodigits z = medium_value + medium_value delta "
                  "100000, :3742 _PyLong_FromSTwoDigits delta 100000, and "
                  "inside that, :309 IS_SMALL_INT delta 100000 and :310 "
                  "get_small_int delta 100000. x_add was NOT entered: no "
                  "delta on it for the small pair. The result came from "
                  "the preallocated small-int table, not from an "
                  "allocation."),
         "evidence": "tally, per-run"},
        {"id": "F4",
         "text": ("The growth path is the SAME entry with a different "
                  "interior. For the 2000-bit pair the compact branch was "
                  "not taken; long_add:3765 called x_add (delta 100002) "
                  "and the digit loop at longobject.c:3667-3670 ran with "
                  "delta 6700002 -- 67 digit steps per call across 100000 "
                  "calls. long_alloc and long_normalize each ran 100004 "
                  "times. Same bytecode instruction, same specialized "
                  "case, same long_add; the divergence is inside."),
         "evidence": "tally, per-run"},
        {"id": "F5",
         "text": ("The generic route was measured too, and it is tiny: "
                  "Objects/abstract.c PyNumber_Add and binary_op1 show "
                  "delta=1 each, and Python/specialize.c "
                  "_Py_Specialize_BinaryOp:2607-2608 shows delta=1 for the "
                  "line that installs the specialized case. One trip "
                  "through the generic path, then the specialization, then "
                  "99999 trips through the specialized case."),
         "evidence": "tally, per-run"},
        {"id": "F6",
         "text": ("Slicing the COVERAGE binary produced polluted units: "
                  "every function opened with a __gcov0 counter increment "
                  "(long_add at 0x315996: mov 0x951a03(%rip),%rax # "
                  "__gcov0.long_add). Those slices are artifacts of the "
                  "instrument. The arch-units in this file come from the "
                  "separate uninstrumented anchor and ship builds of the "
                  "same pin, checked to carry zero __gcov symbols."),
         "evidence": "artifact fact (objdump + nm)"},
        {"id": "F7",
         "text": ("_PyEval_EvalFrameDefault is one symbol of 28811 "
                  "instructions at the anchor and 16821 at ship. It is the "
                  "whole interpreter loop, not a per-operator unit, so the "
                  "operator-sized arch-unit for a Python addition on ints "
                  "is long_add (78 anchor / 94 ship instructions) reached "
                  "through _PyLong_Add, with the dispatch-side work living "
                  "inside the big loop. UNVERIFIED: no attempt was made "
                  "here to carve the specialized case out of "
                  "_PyEval_EvalFrameDefault as its own address range."),
         "evidence": ("artifact fact for the counts; the carving claim is "
                      "marked unverified")},
    ],
    "frontier": [
        {"kind": "instrument",
         "text": ("order is not recorded anywhere in this file: a tally "
                  "cannot supply it. The call ORDER stated in the findings "
                  "is read off the source text, which is interpretation, "
                  "not measurement.")},
        {"kind": "scope",
         "text": ("one architecture (x86-64), one compiler (gcc 15.2.0), "
                  "one pin, one operator intention, one type pair plus a "
                  "large-int pair. Nothing here bounds other runs, other "
                  "types, or free-threaded builds.")},
        {"kind": "not attempted",
         "text": ("no normalization to the canonical runnable form, no "
                  "matching against the compiled-language units, no "
                  "bridge or dominance claim. This pilot only proves "
                  "probe -> bytecode -> handler-slice.")},
    ],
}

fh = open(DEST, "w")
json.dump(doc, fh, indent=1, sort_keys=False)
fh.write("\n")
fh.close()
print("wrote " + DEST)
for run in records:
    print("  dispatch records for " + run + ": " + str(len(records[run])))
print("  anchor units: " + str(len(doc["handler_arch_units"]["anchor"])))
print("  ship units: " + str(len(doc["handler_arch_units"]["ship"])))
