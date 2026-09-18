#!/bin/bash
# rv2_l11_cpp_and_rust_arch_units_for_riscv64.sh
#
# LANGUAGE EXPANSION ON THE SIDE THAT MATTERS. The riscv64 arch-unit corpus
# is c (400) and go (107). The x86-64 side carries TWELVE languages -- cpp,
# swift, rust, csharp, dart, javascript, php, java, ruby, cpython among them.
# Adding an emulation TARGET does not grow the arch-unit population; adding a
# language whose compiler lowers for riscv64 does.
#
# Two are reachable with what the image already has, and lane rv1_l16
# measured both rather than assuming either:
#
#   cpp   clang++ -std=c++17 -O1 --target=riscv64-unknown-linux-gnu
#         3 of 3 probes compiled.  c's flags compiled 0 of 3 -- the probes
#         `#include <cstdint>` and `-nostdlibinc` hides it.
#   rust  rustc --target=riscv64gc-unknown-linux-gnu, with the corpus's own
#         ship flags.  2 of 3 compiled and the third is a REAL refusal
#         (`u64: Neg` is not satisfied -- rust will not negate an unsigned),
#         which is a BUILDFAIL of exactly the kind the corpus already records.
#         inherit.py's `riscv64gc-unknown-none-elf` compiled 0 of 3: no std.
#
# The objects came out `elf64-littleriscv` with the `op_` symbol intact, so
# the carve and the disassembly have something to hold.
#
# WHAT IS NOT TOUCHED. This writes `attest_rv_langs.json`, a NEW prefix.
# `attest_rv.json` is the corpus of record for c and go and is left exactly
# as it is; nothing downstream of it moves because of this lane.
#
# Fetches nothing. Budget: thirty minutes.
set -uo pipefail
export HOME=/work
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
export CARGO_HOME=/opt/cargo RUSTUP_HOME=/opt/rustup
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2langs
R=PseudoCoupHQ
RV=$R/Research/oracle/riscv
OP=$R/Research/op_pipeline
t0=$(date +%s)

echo "[1/3] the rules this lane adds, printed from the code that will run"
python3 - <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_carve as C
for lang in sorted(C.SHIP):
    print("  %-6s %s" % (lang, " ".join(C.SHIP[lang])))
print("  compile rules registered:", ", ".join(sorted(C.COMPILE)))
PY

echo "[2/3] the sweep: cpp and rust, every probe  ($(( $(date +%s) - t0 ))s)"
# c:0 and go:0 -- the corpus of record is not re-swept here
python3 -u $RV/rv_attest.py run $OP $RV/attest_rv_langs /work/rv2langs 0 0 \
        cpp:all rust:all 2>&1 | tail -25

echo "[3/3] what came out  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections
p = "PseudoCoupHQ/Research/oracle/riscv/attest_rv_langs.json"
d = json.load(open(p))
rows = d["rows"]
print("  rows: %d" % len(rows))
by = collections.Counter((r.get("lang"), r.get("outcome")) for r in rows)
langs = sorted(set(l for l, _ in by))
outs = sorted(set(o for _, o in by))
print("  %-6s %s" % ("lang", " ".join("%14s" % o for o in outs)))
for l in langs:
    print("  %-6s %s" % (l, " ".join("%14d" % by.get((l, o), 0) for o in outs)))
lifted = [r for r in rows if r.get("outcome") == "LIFTED"]
print()
print("  NEW riscv64 arch-units: %d" % len(lifted))
print("  by language:", dict(collections.Counter(r["lang"] for r in lifted)))
if lifted:
    print()
    print("  five of them, with their arch-opcodes:")
    for r in lifted[:5]:
        print("    %-14s %-4s %-16s %s" % (
            r.get("unit"), r.get("lang"), (r.get("expression") or "")[:16],
            " ; ".join((r.get("body") or [])[:4])[:90]))
fails = [r for r in rows if r.get("outcome") == "BUILDFAIL"]
if fails:
    print()
    print("  refused by the compiler: %d; the first few reasons:" % len(fails))
    c = collections.Counter((r["lang"], (r.get("diagnostic") or "").split("\n")[0][:80]) for r in fails)
    for (l, why), n in c.most_common(8):
        print("    %-5s %-82s x%d" % (l, why, n))
PY
python3 $OP/check_no_spelling_keys.py $RV/attest_rv_langs.json 2>&1 | tail -1
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
