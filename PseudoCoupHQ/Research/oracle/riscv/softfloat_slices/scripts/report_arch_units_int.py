#!/usr/bin/env python3
"""Merge the INTEGER layer into softfloat_slices/arch_units/arch_units.json
alongside the float layer already there, and print the tables.

    python3 scripts/build_arch_units_int.py     # emit the 318 x 4 sources
    python3 scripts/verify_arch_units_int.py    # build and run the six programs
    python3 scripts/probe_answer_width.py       # the answer-register probe
    python3 scripts/report_arch_units_int.py    # this

The float layer's own records are read back out of arch_units.json and carried
across untouched; this script never re-runs the float verification.
"""

import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
RV = os.path.dirname(BASE)
OUT = os.path.join(BASE, "arch_units")
ATTEST = os.path.join(RV, "attest_rv.json")
SCRATCH = os.environ.get(
    "AU_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/archunits_int")
LANGS = ("c", "cpp", "rust", "go")
FLOAT_KEYS = ("rounding_mode", "rounding_mode_note", "float_arch_opcodes",
              "totals", "grand_totals", "failures", "nan_divergence",
              "no_float_attestation", "inputs", "reference")


def tool(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True
                              ).stdout.strip().splitlines()[0]
    except Exception:
        return "unknown"


# ------------------------------------------------ the rows with no body ----
def census_not_emulable():
    rows = json.load(open(ATTEST))["rows"]
    bf = [r for r in rows if r["outcome"] == "BUILDFAIL"]
    wr = [r for r in rows if r["outcome"] == "WALK_REFUSED"]

    def first_error(t):
        m = re.search(r"(?:error: |invalid operation: |unexpected |"
                      r"call to undeclared function )([^\n]*)", t)
        return (m.group(0) if m else t.splitlines()[0])[:120]

    def bucket(r):
        t, lang = r["diagnostic"], r["lang"]
        if lang == "go":
            if "shifted operand" in t or "shift count" in t:
                return "go: the shifted operand or the shift count is not an integer type"
            if "mismatched types" in t:
                return "go: mismatched types -- go has no implicit conversion, so an operator between two unequal types does not exist"
            if "not defined on" in t:
                return "go: the operator is not defined on that type"
            if "unexpected ++" in t or "unexpected --" in t \
                    or "unexpected ..." in t:
                return "go: ++ / -- / ... are statements, not expressions"
            if "receive from non-chan" in t or "<-" in t:
                return "go: receive from a non-channel"
            return "go: other invalid operation"
        if "invalid operands to binary expression" in t:
            return "c: invalid operands to a binary expression (a float operand to an integer-only operator)"
        if "undeclared function" in t:
            return "c: 'alignof' / '_alignof' are not C spellings"
        if "indirection requires pointer" in t:
            return "c: unary * on a scalar"
        if "invalid argument type" in t:
            return "c: invalid argument type to a unary expression (~ on a float)"
        return "other: " + first_error(t)

    buckets = collections.Counter(bucket(r) for r in bf)
    bfg = collections.Counter(first_error(r["diagnostic"]) for r in bf)
    wrg = collections.Counter(
        re.sub(r" \(line '.*'\)", "", r["cause"]) for r in wr)
    return {
        "BUILDFAIL": {
            "count": len(bf),
            "what": "the probe source did not compile for riscv64 at all, so "
                    "there is no arch-unit: the compiler-operator does not "
                    "exist in that language on those operand types.  No body, "
                    "nothing to decompose, nothing to emulate.",
            "by_language": dict(collections.Counter(r["lang"] for r in bf)),
            "by_operator": dict(collections.Counter(r["operator"]
                                                    for r in bf)),
            "why": [{"reason": k, "rows": v}
                    for k, v in buckets.most_common()],
            "diagnostics": [{"diagnostic": k, "rows": v}
                            for k, v in bfg.most_common()],
            "x86_ship_body_in_the_store": dict(collections.Counter(
                str(r["x86_ship_body_in_the_store"]) for r in bf)),
        },
        "WALK_REFUSED": {
            "count": len(wr),
            "what": "the probe compiled and a body was carved, but the "
                    "RISC-V reference walker has no entry in its opcode table "
                    "for one arch-opcode in it, so task rv2 refused to call "
                    "the body lifted.  The body is present; what is missing "
                    "is the walker's model of that arch-opcode.",
            "by_language": dict(collections.Counter(r["lang"] for r in wr)),
            "causes": [{"cause": k, "rows": v} for k, v in wrg.most_common()],
            "rows": [{"unit": r["unit"], "lang": r["lang"],
                      "operator": r["operator"], "expression": r["expression"],
                      "lhs_type": r["lhs_type"], "rhs_type": r["rhs_type"],
                      "body": r["body"], "cause": r["cause"]} for r in wr],
        },
    }


# ---------------------------------------------------------------- main -----
def main():
    old = json.load(open(os.path.join(OUT, "arch_units.json")))
    # idempotent: re-running keeps only the float layer's own records
    float_units = [u for u in old["units"]
                   if u.get("layer") != "integer" and u["index"] < 174]
    assert len(float_units) == 174, len(float_units)
    if "layers" in old and "float" in old["layers"]:
        old = dict(old, **old["layers"]["float"])

    units = json.load(open(os.path.join(OUT, "_units_int.json")))["units"]
    verdict = json.load(open(os.path.join(SCRATCH, "verdict.json")))
    aw = {}
    awp = os.path.join(OUT, "_answer_width.json")
    if os.path.exists(awp):
        aw = json.load(open(awp))
    per = verdict["per_unit"]

    # ------------------------------------------- the integer arch-opcodes --
    ops = collections.OrderedDict()
    seen = collections.defaultdict(set)
    for u in units:
        for s in u["arch_opcodes"]:
            m = s["mnemonic"]
            r = ops.setdefault(m, {"arch_opcode": m, "occurrences": 0,
                                   "arch_units": 0, "maps": set(),
                                   "kinds": set()})
            r["occurrences"] += 1
            r["kinds"].add(s["kind"])
            r["maps"].add(s["mapped_to"])
            seen[m].add(u["index"])
    for m, r in ops.items():
        r["arch_units"] = len(seen[m])
        r["kind"] = "/".join(sorted(r.pop("kinds")))
        r["mapped_to"] = "; ".join(sorted(r.pop("maps")))

    # ----------------------------------------------------------- per unit --
    out_units = []
    tot = {l: dict(inputs=0, mismatches=0, reference_undefined=0,
                   trap_agreements=0, cross_language_mismatches=0)
           for l in LANGS}
    failures = []
    awper = aw.get("per_unit", {})
    for u in units:
        rec = {k: u[k] for k in
               ("index", "name", "lang", "operator", "expression",
                "lhs_type", "rhs_type", "symbol", "unit", "outcome",
                "result_tag", "result_type", "result_bits", "n_params",
                "reduced", "blocked", "guarded")}
        rec["layer"] = "integer"
        rec["body"] = u["body"]
        rec["arch_opcodes"] = u["arch_opcodes"]
        a = awper.get(str(u["index"]))
        if a:
            rec["answer_register"] = {
                "probe_inputs": a["tested"],
                "non_canonical": a["non_canonical"],
                "note": "inputs where the arch-unit leaves the answer "
                        "register above its own result width in a form that "
                        "is not the canonical widening",
            }
        rec["languages"] = {}
        v = per.get(str(u["index"]), {})
        for l in LANGS:
            r = v.get(l) or {}
            rec["languages"][l] = {
                "file": u["languages"][l]["file"],
                "entry": u["languages"][l]["entry"],
                "trap_entry": u["languages"][l]["trap_entry"],
                "source_lines": u["languages"][l]["lines"],
                "inputs_tested": r.get("tested", 0),
                "mismatches": r.get("mismatch", 0),
                "reference_undefined": r.get("reference_undefined", 0),
                "trap_agreements": r.get("trap_agreements", 0),
                "cross_language_mismatches": r.get("cross_lang_mismatch", 0),
            }
            tot[l]["inputs"] += r.get("tested", 0)
            tot[l]["mismatches"] += r.get("mismatch", 0)
            tot[l]["reference_undefined"] += r.get("reference_undefined", 0)
            tot[l]["trap_agreements"] += r.get("trap_agreements", 0)
            tot[l]["cross_language_mismatches"] += r.get("cross_lang_mismatch",
                                                         0)
            if r.get("mismatch", 0) or r.get("cross_lang_mismatch", 0):
                failures.append({"unit": u["name"], "language": l,
                                 "mismatches": r.get("mismatch", 0),
                                 "cross_language_mismatches":
                                     r.get("cross_lang_mismatch", 0)})
        out_units.append(rec)

    inputs = tot["c"]["inputs"]
    undef = tot["c"]["reference_undefined"]
    traps = tot["c"]["trap_agreements"]
    grand = {
        "arch_units": len(units),
        "inputs_per_language": inputs,
        "comparisons_against_the_native_operator":
            sum(tot[l]["inputs"] - tot[l]["reference_undefined"]
                for l in LANGS),
        "of_which_value_comparisons":
            sum(tot[l]["inputs"] - tot[l]["reference_undefined"]
                - tot[l]["trap_agreements"] for l in LANGS),
        "of_which_trap_comparisons": sum(tot[l]["trap_agreements"]
                                         for l in LANGS),
        "mismatches": sum(tot[l]["mismatches"] for l in LANGS),
        "reference_undefined_excluded": sum(tot[l]["reference_undefined"]
                                            for l in LANGS),
        "cross_language_comparisons":
            sum(tot[l]["inputs"] for l in ("cpp", "rust", "go")),
        "cross_language_mismatches":
            sum(tot[l]["cross_language_mismatches"] for l in LANGS),
    }

    divergences = build_divergences(units, aw, undef, traps, inputs)

    combined = {
        "readable_arch_units_in_attest_rv": 474,
        "float_layer": {"arch_units": len(float_units),
                        "emulated_in_all_four_languages": len(float_units),
                        "note": "156 of the 474 LIFTED rows plus the 18 "
                                "WALK_REFUSED rows that carry a float "
                                "instruction"},
        "integer_layer": {"arch_units": len(units),
                          "emulated_in_all_four_languages": len(units)},
        "arch_units_emulated_in_all_four_languages":
            len(float_units) + len(units),
        "of_the_474_readable": 156 + len(units),
        "emulated_under_a_stated_reduction":
            sum(1 for u in float_units if u.get("reduced"))
            + sum(1 for u in units if u["reduced"]),
        "failed_to_emulate": 0,
    }

    doc = {
        "what": "every RISC-V arch-unit in attest_rv.json that has a readable "
                "body, emulated in c, c++, rust and go and verified against "
                "the original compiler-operator.  Two layers: the 174 that "
                "contain a float instruction (emulated with integer operators "
                "only) and the 318 integer-only ones.",
        "proved": False,
        "tested": True,
        "source": "Research/oracle/riscv/attest_rv.json (task rv2)",
        "population": {
            "arch_units_in_attest_rv": 1244,
            "LIFTED": 474, "BUILDFAIL": 737, "WALK_REFUSED": 33,
            "with_a_body": 507,
            "float_layer": len(float_units),
            "integer_layer": len(units),
            "emulated_in_total": len(float_units) + len(units),
            "by_language_integer": dict(collections.Counter(u["lang"]
                                                            for u in units)),
        },
        "combined": combined,
        "toolchains": {
            "c": tool(["clang", "--version"]),
            "cpp": tool(["clang++", "--version"]),
            "rust": tool(["rustc", "--version"]),
            "go": tool(["go", "version"]),
        },
        "layers": {
            "float": {k: old[k] for k in FLOAT_KEYS if k in old},
            "integer": {
                "reference":
                    "the arch-unit's own source expression, written as a "
                    "native function in the arch-unit's own language and "
                    "compiled for the HOST at -O2: c for the 235 c "
                    "arch-units, go for the 83 go ones.  In c the result TYPE "
                    "is taken from the compiler itself with __typeof__, so "
                    "the usual arithmetic conversions are not assumed.",
                "answer_convention":
                    "the result type's own bit pattern, zero-extended into a "
                    "uint64 -- 1 bit for a boolean result, 32 for a 32-bit "
                    "one, 64 otherwise.  See divergences/answer_register for "
                    "why the full register is not the right comparison.",
                "inputs": {
                    "edges": "every edge value of each operand crossed: zero, "
                             "one, minus one, the signed and unsigned "
                             "extremes, the value just inside and just "
                             "outside every bit boundary, and the shift "
                             "amounts at and either side of both widths "
                             "(31/32/33, 63/64/65) and beyond; for a float "
                             "operand the float edge set",
                    "uniform_random_per_operand": verdict["n_rand"],
                    "boundary_banded_per_operand": verdict["n_band"],
                    "banded_bands": "zero, all-ones, the sign bit, a shift "
                                    "count in [0,130), a power of two +/- 1, "
                                    "a small value, a value just below "
                                    "all-ones, and a plain uniform draw -- so "
                                    "divisors of zero, shift counts at and "
                                    "above the width, and the most-negative "
                                    "over minus one are all reached",
                    "seed": verdict["seed"],
                    "note": "all six programs draw the identical sequence "
                            "from the same xorshift64 seed in the same order",
                },
                "integer_arch_opcodes": list(ops.values()),
                "totals": tot,
                "grand_totals": grand,
                "failures": failures,
                "divergences": divergences,
                "answer_register_probe": {k: aw[k] for k in
                                          ("what", "probed",
                                           "arch_units_with_a_non_canonical"
                                           "_answer_register", "units")
                                          if k in aw},
            },
        },
        "not_emulable": census_not_emulable(),
        "units": float_units + out_units,
    }
    json.dump(doc, open(os.path.join(OUT, "arch_units.json"), "w"), indent=1)

    # ----------------------------------------------------------- printing --
    print("integer arch-opcodes across the %d integer arch-units" % len(units))
    print("| arch-opcode | occurrences | arch-units | kind | mapped to |")
    print("|---|---:|---:|---|---|")
    for m, r in sorted(ops.items()):
        print("| `%s` | %d | %d | %s | %s |"
              % (m, r["occurrences"], r["arch_units"], r["kind"],
                 r["mapped_to"]))
    print()
    print("| language | inputs | mismatches | reference undefined |"
          " trap agreements | cross-language mismatches |")
    print("|---|---:|---:|---:|---:|---:|")
    for l in LANGS:
        print("| %s | %d | %d | %d | %d | %d |"
              % (l, tot[l]["inputs"], tot[l]["mismatches"],
                 tot[l]["reference_undefined"], tot[l]["trap_agreements"],
                 tot[l]["cross_language_mismatches"]))
    print()
    print(json.dumps(grand, indent=1))
    print()
    print(json.dumps(combined, indent=1))
    print()
    for d in divergences:
        print("DIVERGENCE:", d["name"], "--", d["arch_units"], "arch-units")
    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print(" ", f)
    else:
        print("no failures")
    print("written to", os.path.join(OUT, "arch_units.json"))


def build_divergences(units, aw, undef, traps, inputs):
    def names(pred):
        return [u["name"] for u in units if pred(u)]

    cdiv = names(lambda u: u["lang"] == "c" and u["operator"] in ("/", "%")
                 and u["rhs_type"] is not None)
    cdivbool = names(lambda u: u["lang"] == "c" and u["operator"] in ("/", "%")
                     and u["rhs_type"] == "bool")
    goguard = names(lambda u: u["guarded"])
    goshift = names(lambda u: u["lang"] == "go"
                    and u["operator"] in ("<<", ">>"))
    red = names(lambda u: u["reduced"])
    awu = [x["name"] for x in aw.get("units", [])]
    return [
        {
            "name": "C leaves division undefined where RISC-V defines it",
            "arch_units": len(cdiv),
            "units": cdiv,
            "what": "RISC-V's div/divu/rem/remu do not trap.  b == 0 gives an "
                    "all-ones quotient and the dividend back as the "
                    "remainder; the signed most-negative over minus one gives "
                    "the most-negative back with a zero remainder.  C "
                    "(6.5.5p5) leaves both undefined, and the host faults on "
                    "both, so the native reference has no answer to compare "
                    "against.",
            "what_was_done": "the emulation writes the RISC-V answer out "
                             "explicitly in all four languages (au_div / "
                             "au_rem / au_divu / au_remu, restoring long "
                             "division, no `/` or `%` of the host language "
                             "anywhere).  The reference flags those inputs and "
                             "they are excluded from the comparison against "
                             "the native operator and counted apart; they are "
                             "still compared across the four languages, where "
                             "they agree exactly.",
            "inputs_excluded_per_language": undef,
        },
        {
            "name": "clang folds `a / (bool)b` to the identity",
            "arch_units": len(cdivbool),
            "units": cdivbool,
            "what": "a _Bool is 0 or 1 and a division by 0 is undefined, so "
                    "clang concludes b == 1 and emits nothing at all for "
                    "`a / b` (`c.jr ra`) and a constant 0 for `a % b`.  The "
                    "arch-unit is therefore NOT the RISC-V div instruction: "
                    "at b == 0 it answers `a`, where a raw `div` would answer "
                    "all-ones.",
            "what_was_done": "emulated exactly as the arch-unit is -- the "
                             "identity, and the constant zero.  b == 0 is one "
                             "of the C-undefined inputs above and is excluded "
                             "from the native comparison.",
        },
        {
            "name": "go panics where RISC-V does not",
            "arch_units": len(goguard),
            "units": goguard,
            "what": "go's `/` and `%` panic on a zero divisor and its shifts "
                    "panic on a negative count.  RISC-V's div/rem/sll/srl/sra "
                    "do none of that, so the go compiler wraps the "
                    "arch-opcode in a guard branch to runtime.panicdivide or "
                    "runtime.panicshift.",
            "what_was_done": "each of these arch-units is emitted as TWO "
                             "functions: the fall-through value, and a "
                             "`_trap` predicate that is 1 exactly when the "
                             "arch-unit takes the branch.  The go reference "
                             "observes the real panic with recover() rather "
                             "than assuming the condition, and the predicate "
                             "is checked against it on every input in all "
                             "four languages.",
            "trap_agreements_per_language": traps,
        },
        {
            "name": "a RISC-V shift is not a go shift, and is undefined in C",
            "arch_units": len(goshift),
            "units": goshift,
            "what": "RISC-V's sll/srl/sra use the low 6 bits of the count "
                    "(sllw/sraw the low 5), so a count of 64 shifts by 0.  go "
                    "defines a shift at or above the width as zero, or a full "
                    "sign fill for an arithmetic right shift.  C and C++ "
                    "leave it undefined outright (C 6.5.7p3).  The three do "
                    "not agree, which is why every one of these arch-units is "
                    "four or more arch-opcodes rather than one.",
            "what_was_done": "the sltiu/mask idiom the compiler emitted is "
                             "composed as written, and every shift count that "
                             "reaches a `<<` or `>>` in the emitted source is "
                             "masked to the 5 or 6 bits RISC-V uses first, so "
                             "no shift in any of the four languages is ever "
                             "undefined.  Counts at, above and far above both "
                             "widths are in the edge set and in the banded "
                             "draw.",
        },
        {
            "name": "go leaves a 32-bit answer non-canonical in the register",
            "arch_units": len(awu),
            "units": awu,
            "what": "the RISC-V psABI wants a 32-bit value sign-extended into "
                    "the register, and clang does that (`subw a0, zero, a0` "
                    "for c's `-a` on int32_t).  go's register ABI does not "
                    "require it of a RESULT: go emits `sub a0, zero, a0` for "
                    "`-a` on int32 and `c.add a0, a1` for `a + b`, leaving "
                    "the bits above 32 as they fall.  Measured, not assumed: "
                    "scripts/probe_answer_width.py recomposes every arch-unit "
                    "without the final mask and counts it.",
            "what_was_done": "the comparison is made at the RESULT's own "
                             "width, which is what the compiler-operator's "
                             "answer is.  Of the arch-units whose result is "
                             "narrower than the register, only these leave "
                             "the register non-canonical, and every one of "
                             "them is a go arch-unit with an int32 result.",
        },
        {
            "name": "`&a` answers an address",
            "arch_units": len(red),
            "units": red,
            "what": "the answer is the address of a stack slot (c) or a heap "
                    "cell from the go runtime allocator (go), which is not a "
                    "function of the operand bits.",
            "what_was_done": "emulated and verified under the stated "
                             "reduction `*(&a)` -- the bit pattern the "
                             "store/load moves -- with the same reduction as "
                             "the reference, exactly as the float layer does.",
        },
    ]


if __name__ == "__main__":
    main()
