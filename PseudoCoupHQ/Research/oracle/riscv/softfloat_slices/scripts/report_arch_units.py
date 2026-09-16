#!/usr/bin/env python3
"""Merge the decomposition record and the verification verdict into
softfloat_slices/arch_units/arch_units.json, and print the tables.

    python3 scripts/build_arch_units.py       # emit the sources
    python3 scripts/verify_arch_units.py      # build and run the six programs
    python3 scripts/report_arch_units.py      # this
"""

import collections
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "arch_units")
SCRATCH = os.environ.get(
    "AU_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/archunits")
LANGS = ("c", "cpp", "rust", "go")


def tool(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True
                              ).stdout.strip().splitlines()[0]
    except Exception:
        return "unknown"


def main():
    units = json.load(open(os.path.join(OUT, "_units.json")))["units"]
    verdict = json.load(open(os.path.join(SCRATCH, "verdict.json")))
    nfp = os.path.join(OUT, "_nofloat.json")
    nofloat = {}
    if os.path.exists(nfp):
        raw = json.load(open(nfp))
        nofloat = {l: {k: v for k, v in r.items() if k != "instructions"}
                   for l, r in raw.items()}
        nofloat["what"] = ("scripts/nofloat_probe.py: every host instruction "
                           "in the compiled arch-unit and emulation code, "
                           "per language, and any float register it touches")
    per = verdict["per_unit"]

    # ------------------------------------------------- float arch-opcodes --
    ops = collections.OrderedDict()
    for u in units:
        for s in u["arch_opcodes"]:
            if s["kind"] != "float":
                continue
            m = s["mnemonic"]
            r = ops.setdefault(m, {"arch_opcode": m,
                                   "sail_clause": s.get("sail_clause", ""),
                                   "occurrences": 0, "units": 0,
                                   "mapped_to": s["mapped_to"]})
            r["occurrences"] += 1
    seen = collections.defaultdict(set)
    for u in units:
        for s in u["arch_opcodes"]:
            if s["kind"] == "float":
                seen[s["mnemonic"]].add(u["index"])
    for m, r in ops.items():
        r["units"] = len(seen[m])
        if r["mapped_to"].startswith("emulation:"):
            r["status"] = "emulation"
        elif r["mapped_to"] == "bit-manipulation":
            r["status"] = ("bit-manipulation"
                           if m not in ("fsw", "flw", "c.fsdsp", "c.fldsp")
                           else "bit-manipulation (in a REDUCED unit only)")
        else:
            r["status"] = "FAILED"

    # ---------------------------------------------------------- per unit --
    out_units = []
    tot = {l: dict(inputs=0, mismatches=0, nan_divergent=0,
                   cross_language_mismatches=0) for l in LANGS}
    failures = []
    for u in units:
        rec = {k: u[k] for k in
               ("index", "name", "lang", "operator", "expression",
                "lhs_type", "rhs_type", "symbol", "unit", "outcome",
                "result_kind", "result_bits", "n_params", "reduced",
                "blocked")}
        rec["body"] = u["body"]
        rec["arch_opcodes"] = u["arch_opcodes"]
        rec["languages"] = {}
        v = per.get(str(u["index"]), {})
        for l in LANGS:
            r = v.get(l) or {}
            rec["languages"][l] = {
                "file": u["languages"][l]["file"],
                "entry": u["languages"][l]["entry"],
                "source_lines": u["languages"][l]["lines"],
                "inputs_tested": r.get("tested", 0),
                "mismatches": r.get("mismatch", 0),
                "nan_divergent": r.get("nan_divergent", 0),
                "cross_language_mismatches": r.get("cross_lang_mismatch", 0),
            }
            tot[l]["inputs"] += r.get("tested", 0)
            tot[l]["mismatches"] += r.get("mismatch", 0)
            tot[l]["nan_divergent"] += r.get("nan_divergent", 0)
            tot[l]["cross_language_mismatches"] += r.get("cross_lang_mismatch",
                                                         0)
            if r.get("mismatch", 0) or r.get("cross_lang_mismatch", 0):
                failures.append({"unit": u["name"], "language": l,
                                 "mismatches": r.get("mismatch", 0),
                                 "cross_language_mismatches":
                                     r.get("cross_lang_mismatch", 0)})
        out_units.append(rec)

    grand = {
        "inputs_per_language": tot["c"]["inputs"],
        "comparisons_against_the_native_operator":
            sum(tot[l]["inputs"] for l in LANGS),
        "mismatches": sum(tot[l]["mismatches"] for l in LANGS),
        "nan_divergent": sum(tot[l]["nan_divergent"] for l in LANGS),
        "cross_language_comparisons":
            sum(tot[l]["inputs"] for l in ("cpp", "rust", "go")),
        "cross_language_mismatches":
            sum(tot[l]["cross_language_mismatches"] for l in LANGS),
    }

    doc = {
        "what": "every RISC-V arch-unit in attest_rv.json that contains a "
                "float instruction, emulated with integer operators only in "
                "c, c++, rust and go, and verified against the original "
                "compiler-operator",
        "proved": False,
        "tested": True,
        "source": "Research/oracle/riscv/attest_rv.json (task rv2)",
        "population": {
            "arch_units_in_attest_rv": 1244,
            "with_a_body": 507,
            "containing_a_float_instruction": len(units),
            "by_language": dict(collections.Counter(u["lang"]
                                                    for u in units)),
            "emulated_as_a_bit_function":
                sum(1 for u in units if not u["reduced"]),
            "emulated_under_a_stated_reduction":
                sum(1 for u in units if u["reduced"]),
        },
        "rounding_mode": 0,
        "rounding_mode_note":
            "the c arch-units carry `dyn`, which reads frm; frm is 0 (RNE) on "
            "a fresh hart and is what the host rounds with, and the go "
            "arch-units name `rne` outright.  The emulations are therefore "
            "the rounding-mode-0 emission of the 67 SoftFloat operations, "
            "under arch_units/emul_rm0/.",
        "reference":
            "the arch-unit's own source expression, written as a native "
            "function in the arch-unit's own language and compiled for the "
            "HOST at -O2.  NOT SoftFloat.",
        "toolchains": {
            "c": tool(["clang", "--version"]),
            "cpp": tool(["clang++", "--version"]),
            "rust": tool(["rustc", "--version"]),
            "go": tool(["go", "version"]),
        },
        "inputs": {
            "edges": "every edge value of each operand, crossed: +/-0, "
                     "+/-inf, quiet and signalling NaN, largest and smallest "
                     "normal, largest and smallest subnormal, +/-1, +/-2, "
                     "+/-0.5, and one ulp either side of each; for integer "
                     "operands 0, 1, the extremes and the powers of two "
                     "either side of every significant bit",
            "uniform_random_per_operand": verdict["n_rand"],
            "exponent_banded": verdict["n_band"],
            "seed": verdict["seed"],
            "note": "all six programs draw the identical sequence from the "
                    "same xorshift64 seed in the same order",
        },
        "float_arch_opcodes": list(ops.values()),
        "totals": tot,
        "grand_totals": grand,
        "failures": failures,
        "nan_divergence": {
            "count": grand["nan_divergent"],
            "what": "inputs where the native operator and the emulation both "
                    "answer NaN of the result type but with different bits",
            "why": "C leaves the sign and payload of a NaN result "
                   "unspecified (C23 Annex F / IEEE 754-2019 6.2) and so does "
                   "go.  RISC-V pins every NaN-producing float result to the "
                   "canonical quiet NaN (0x7fc00000 / "
                   "0x7ff8000000000000); x86-64 SSE instead propagates a "
                   "quieted input NaN's payload, and for an invalid operation "
                   "with no NaN input returns the negative 'real indefinite' "
                   "(0xffc00000 / 0xfff8000000000000).  The two targets are "
                   "both conforming; the source operator does not pin the "
                   "answer.",
            "examples": [l for l in verdict["examples"]["c"]
                         if l.startswith("EXN")][:24],
            "units_affected": None,
            "scope": "only arch-units whose answer is a float and whose body "
                     "contains a SoftFloat-backed arithmetic or conversion "
                     "arch-opcode.  Comparisons, the logical operators, the "
                     "sign-splice `-a` and the address-of units diverge on "
                     "nothing.",
        },
        "no_float_attestation": nofloat,
        "units": out_units,
    }
    doc["nan_divergence"]["units_affected"] = sum(
        1 for u in out_units if u["languages"]["c"]["nan_divergent"])
    json.dump(doc, open(os.path.join(OUT, "arch_units.json"), "w"), indent=1)

    # ----------------------------------------------------------- printing --
    print("float arch-opcodes across the %d arch-units" % len(units))
    print("| arch-opcode | Sail clause | occurrences | arch-units | mapped to |"
          " status |")
    print("|---|---|---:|---:|---|---|")
    for m, r in sorted(ops.items()):
        print("| `%s` | `%s` | %d | %d | %s | %s |"
              % (m, r["sail_clause"], r["occurrences"], r["units"],
                 r["mapped_to"], r["status"]))
    print()
    print("| language | inputs | mismatches | NaN-divergent |"
          " cross-language mismatches |")
    print("|---|---:|---:|---:|---:|")
    for l in LANGS:
        print("| %s | %d | %d | %d | %d |"
              % (l, tot[l]["inputs"], tot[l]["mismatches"],
                 tot[l]["nan_divergent"], tot[l]["cross_language_mismatches"]))
    print()
    print(json.dumps(grand, indent=1))
    if failures:
        print("FAILURES:")
        for f in failures:
            print(" ", f)
    else:
        print("no failures")


if __name__ == "__main__":
    main()
