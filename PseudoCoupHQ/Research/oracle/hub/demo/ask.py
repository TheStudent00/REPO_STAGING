#!/usr/bin/env python3
"""ask.py -- a SMALL DEMONSTRATION, not a build. The Hub in miniature.

the owner, 2026-09-17: "it would be great to have some real indicators of it doing
actual work. an oracle in a sense. but small. i dont want things to get too
far into that realm yet."

So this is deliberately one file that BUILDS NOTHING. It reads artifacts other
tasks already wrote and answers one question with its provenance attached:

    give me <operator> on <lhs, rhs> from <language>, in <target language>

and it answers with four things, each from a named file:

  1. does the TARGET language accept that operator on those operands at all?
     -- `attest_rv.json`, the compile-or-refuse gate
  2. what does the SOURCE language lower it to?
     -- the same file's carved riscv64 body: the arch-unit
  3. the emulation, in the target language
     -- `arch_units/<lang>/`, byte for byte, as the emitter wrote it
  4. is it PROVED equal to that arch-unit, and what does the proof cover?
     -- the gate runs, by way of the equivalence class

Every line of the answer names where it came from. Nothing here re-derives,
re-compiles or re-proves anything; if an artifact is missing the answer says
so rather than filling the hole.

    python3 ask.py --operator + --lhs int32_t --rhs int64_t --from c --to go
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.abspath(os.path.join(HERE, "..", "..", "riscv"))
AU = os.path.join(RV, "softfloat_slices", "arch_units")
EXT = {"c": "c", "cpp": "cpp", "rust": "rs", "go": "go", "java": "java",
       "python": "py", "ruby": "rb", "js": "js"}


# The arrival shape, not the spelling. `int32_t` and `int32` are one shape;
# so are `float` and `uint32_t` as far as a 64-bit register is concerned.
SHAPE = {
    "int32_t": "s32", "int32": "s32", "i32": "s32",
    "int64_t": "s64", "int64": "s64", "i64": "s64",
    "uint64_t": "u64", "uint64": "u64", "u64": "u64",
    "uint32_t": "u32", "uint32": "u32", "u32": "u32",
    "float": "f32", "float32": "f32", "f32": "f32",
    "double": "f64", "float64": "f64", "f64": "f64",
    "bool": "b1", "_Bool": "b1",
}


def shape_of(name):
    text = (name or "").strip()
    if text in ("", "None", "none"):
        return "-"
    return SHAPE.get(text, text)


def load(path, default=None):
    if not os.path.exists(path):
        return default
    fh = open(path)
    try:
        return json.load(fh)
    finally:
        fh.close()


def attest_rows():
    rows = []
    for name in ("attest_rv.json", "attest_rv_langs.json"):
        doc = load(os.path.join(RV, name))
        if doc:
            rows += doc["rows"]
    return rows


def unit_records():
    out = {}
    for name in ("_units_int.json", "_units.json"):
        doc = load(os.path.join(AU, name))
        if doc:
            for u in doc["units"]:
                out[u["unit"]] = u
    return out


def verdicts():
    """unit name -> the latest Lean verdict recorded for it."""
    out = {}
    runs = os.path.join(RV, "leanpath", "runs")
    for name in ("gate_classes", "gate_bridge3", "gate_bridge2", "gate_float"):
        doc = load(os.path.join(runs, name, "gate.json"))
        if not doc:
            continue
        for r in doc["rows"]:
            v = (r.get("abi") or {}).get("verdict")
            if v and v != "NOT REACHED":
                out.setdefault(r["unit"], (v, name))
            elif v:
                out.setdefault(r["unit"], (v, name))
    return out


def say(label, value, source):
    print("  %-26s %s" % (label, value))
    if source:
        print("  %-26s   from %s" % ("", source))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--operator", required=True)
    p.add_argument("--lhs", required=True)
    p.add_argument("--rhs", default=None)
    p.add_argument("--from", dest="src", required=True)
    p.add_argument("--to", dest="dst", required=True)
    a = p.parse_args()

    rows = attest_rows()
    if not rows:
        print("no attestation on disk; nothing to answer from")
        return 2

    def match(lang, lhs, rhs):
        for r in rows:
            if (r["lang"] == lang and r.get("operator") == a.operator
                    and (r.get("lhs_type") or "") == (lhs or "")
                    and (r.get("rhs_type") or "") == (rhs or "")):
                return r
        return None

    print()
    print("QUESTION  %s %s %s   from %s, wanted in %s"
          % (a.lhs, a.operator, a.rhs or "", a.src, a.dst))
    print()

    # ---- 1. does the target accept it natively? -------------------------
    # THE QUESTION IS ABOUT THESE OPERANDS, NOT THE OPERATOR IN GENERAL. A
    # first version asked only "is there a BUILDFAIL of this operator in the
    # target" and answered that rust REFUSES `int64 + int64`, which is false:
    # rust refuses `+` on MISMATCHED operands and accepts it on matched ones.
    # So the probe has to agree on the operand SHAPES -- the same notion the
    # equivalence classes key on, because type spellings differ per language
    # and the shapes do not.
    print("1. does %s accept it?" % a.dst)
    want = (shape_of(a.lhs), shape_of(a.rhs))
    here = [r for r in rows if r["lang"] == a.dst
            and r.get("operator") == a.operator
            and (shape_of(r.get("lhs_type")), shape_of(r.get("rhs_type"))) == want]
    lifted = [r for r in here if r.get("outcome") == "LIFTED"]
    refused = [r for r in here if r.get("outcome") == "BUILDFAIL"]
    if lifted:
        say("answer", "yes -- %s lowers it itself, e.g. %s"
            % (a.dst, lifted[0]["unit"]), "attest_rv.json")
        say("its own arch-opcodes", " ; ".join(lifted[0].get("body") or []), None)
    elif refused:
        say("answer", "NO -- the compiler refuses it on these operands",
            "attest_rv.json")
        # go prefixes its output with a `# <package>` line; the reason is the
        # first line that is not that header
        lines = [l.strip() for l in (refused[0].get("diagnostic") or "").split("\n")
                 if l.strip() and not l.strip().startswith("#")]
        say("what it said", (lines[0][:90] if lines else "(none recorded)"), None)
    else:
        say("answer", "not probed in %s on these operands" % a.dst,
            "attest_rv.json")
    print()

    # ---- 2. what does the source language lower it to? ------------------
    print("2. what does %s lower it to?" % a.src)
    src = match(a.src, a.lhs, a.rhs)
    if src is None or not src.get("body"):
        say("answer", "no arch-unit on record for that", "attest_rv.json")
        return 1
    say("arch-unit", src["unit"], "attest_rv.json")
    say("arch-opcodes", " ; ".join(src["body"]), None)
    print()

    # ---- 3. the emulation, in the target -------------------------------
    print("3. the emulation, in %s" % a.dst)
    recs = unit_records()
    rec = recs.get(src["unit"])
    if rec is None:
        say("answer", "that arch-unit has no emulation built yet", AU)
        return 1
    lang = rec["languages"].get(a.dst)
    if lang is None:
        say("answer", "no %s emulation for it" % a.dst, AU)
        return 1
    path = os.path.join(os.path.dirname(AU), lang["file"].split("softfloat_slices/", 1)[-1]) \
        if "softfloat_slices/" in lang["file"] else os.path.join(AU, a.dst,
            "%s.%s" % (rec["name"], EXT[a.dst]))
    if not os.path.exists(path):
        path = os.path.join(AU, a.dst, "%s.%s" % (rec["name"], EXT[a.dst]))
    say("entry point", lang["entry"], os.path.relpath(path, RV))
    if os.path.exists(path):
        body = [l for l in open(path).read().split("\n")
                if l.strip() and not l.strip().startswith(("//", "#", "/*", "*", "--"))]
        print()
        for line in body:
            print("      %s" % line)
    print()

    # ---- 4. is it proved? ----------------------------------------------
    print("4. is that emulation PROVED equal to the arch-unit?")
    classes = load(os.path.join(RV, "equivalence_classes.json"))
    mine = None
    if classes:
        for c in classes["classes"]:
            if src["unit"] in c["members"]:
                mine = c
                break
    if mine is None:
        say("answer", "no equivalence class on record", "equivalence_classes.json")
        return 1
    rep = recs.get(mine["representative"])
    v = verdicts().get(rep["name"] if rep else None)
    if v is None:
        say("answer", "its class has not been put to Lean", "the gate runs")
    else:
        verdict, where = v
        say("verdict", verdict, "leanpath/runs/%s/gate.json" % where)
        say("statement", "the psABI `abi` form -- operands arrive widened", None)
    say("proved once, covers", "%d arch-unit(s): %s"
        % (mine["member_count"], ", ".join(mine["members"][:6])
           + (" ..." if mine["member_count"] > 6 else "")),
        "equivalence_classes.json")
    say("across languages", ", ".join(mine["languages"]), None)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
