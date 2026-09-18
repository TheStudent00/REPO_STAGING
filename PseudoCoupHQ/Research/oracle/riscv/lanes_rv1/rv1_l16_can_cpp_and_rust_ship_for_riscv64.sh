#!/bin/bash
# rv1_l16_can_cpp_and_rust_ship_for_riscv64.sh
#
# A SMALL RUN BEFORE A WIDE ONE. The riscv64 arch-unit corpus is c (400) and
# go (107). The x86-64 side carries twelve languages. The cheapest real
# growth is therefore not more emulation targets -- it is more languages whose
# compilers produce NEW riscv64 arch-units, and two are already within reach:
#
#   cpp    1002 probes in the manifest, clang has the riscv backend
#   rust    858 probes in the manifest, and the image already carries
#           riscv64gc-unknown-linux-gnu AND riscv64gc-unknown-none-elf std
#
# WHAT IS NOT KNOWN, and is the whole point of this lane: the c ship flags
# carry `-nostdlibinc`, and the cpp probes `#include <cstdint>`, `<compare>`
# and `<new>`. So c's flags cannot simply be reused. This lane tries four
# candidate flag sets on three real cpp probes and one on three real rust
# probes, and prints the exact command and the exact first error for each.
# Nothing is swept and nothing is written into the corpus.
#
# the owner reads this before any wide sweep is submitted.
set -uo pipefail
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
export HOME=/work
export CARGO_HOME=/opt/cargo RUSTUP_HOME=/opt/rustup
R=PseudoCoupHQ
OP=$R/Research/op_pipeline
W=/work/l16; rm -rf $W; mkdir -p $W
t0=$(date +%s)

echo "[1/3] the toolchains  ($(( $(date +%s) - t0 ))s)"
printf "  clang   %s\n" "$(clang --version 2>/dev/null | head -1)"
printf "  rustc   %s\n" "$(rustc --version 2>/dev/null)"
echo "  rust riscv64 std installed:"
ls /opt/rustup/toolchains/*/lib/rustlib/ 2>/dev/null | grep riscv | sed 's/^/    /'

echo "[2/3] three cpp probes, four candidate flag sets  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY' > $W/cpp_probes.txt
import json
d = json.load(open("PseudoCoupHQ/Research/op_pipeline/probe_manifest_cpp.json"))
pr = d["probes"]
keys = sorted(pr, key=lambda x: int(x))[:3]
for k in keys:
    print("=== %s ===" % k)
    print(pr[k]["source"])
    print("=== END ===")
PY
python3 - <<'PY'
import json, os, subprocess
OP = "PseudoCoupHQ/Research/op_pipeline"
W = "/work/l16"
pr = json.load(open(OP + "/probe_manifest_cpp.json"))["probes"]
keys = sorted(pr, key=lambda x: int(x))[:3]
BASE = ["-std=c++17", "-O1", "--target=riscv64-unknown-linux-gnu"]
SETS = [
    ("A mirror of c", BASE + ["-nostdlibinc"]),
    ("B stdlib headers", BASE),
    ("C freestanding", BASE + ["-nostdlibinc", "-ffreestanding"]),
    ("D host c++ headers", BASE + ["-nostdlibinc"] + sum(
        [["-isystem", p] for p in (
            "/usr/include/c++/14", "/usr/include/x86_64-linux-gnu/c++/14",
            "/usr/include/c++/13", "/usr/include/x86_64-linux-gnu/c++/13",
            "/usr/include")
         if os.path.isdir(p)], [])),
]
for label, flags in SETS:
    ok = 0
    first_err = ""
    for k in keys:
        src = os.path.join(W, "p%s.cpp" % k)
        obj = os.path.join(W, "p%s.o" % k)
        open(src, "w").write(pr[k]["source"])
        cmd = ["clang++"] + flags + ["-c", src, "-o", obj]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            ok += 1
        elif not first_err:
            first_err = (p.stderr or p.stdout).strip().split("\n")[0][:150]
    print("  %-22s %d/3 compiled" % (label, ok))
    print("      %s" % " ".join(["clang++"] + flags[:6] + (["..."] if len(flags) > 6 else [])))
    if first_err:
        print("      first error: %s" % first_err)
PY

echo "[3/3] three rust probes, inherit.py's own riscv64 flags  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, os, subprocess
OP = "PseudoCoupHQ/Research/op_pipeline"
W = "/work/l16"
pr = json.load(open(OP + "/probe_manifest_rust.json"))["probes"]
keys = sorted(pr, key=lambda x: int(x))[:3]
SETS = [
    ("linux-gnu", ["--crate-type=lib", "--emit=obj", "-C", "opt-level=1",
                   "-C", "debug-assertions=off",
                   "--target=riscv64gc-unknown-linux-gnu"]),
    ("none-elf (inherit.py)", ["--crate-type=lib", "--emit=obj",
                               "-C", "opt-level=1", "-C", "debug-assertions=off",
                               "--target=riscv64gc-unknown-none-elf"]),
]
for label, flags in SETS:
    ok = 0
    first_err = ""
    for k in keys:
        src = os.path.join(W, "p%s.rs" % k)
        open(src, "w").write(pr[k]["source"])
        cmd = ["rustc"] + flags + [src, "-o", os.path.join(W, "p%s_rs.o" % k)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            ok += 1
        elif not first_err:
            first_err = (p.stderr or p.stdout).strip().split("\n")[0][:150]
    print("  %-22s %d/3 compiled" % (label, ok))
    if first_err:
        print("      first error: %s" % first_err)
PY

echo "--- what actually got built, and does a symbol survive? ---"
for f in $W/*.o; do
  [ -f "$f" ] || continue
  n=$(llvm-objdump -d --no-show-raw-insn "$f" 2>/dev/null | grep -c "<op_")
  a=$(llvm-objdump -d "$f" 2>/dev/null | grep -m1 "file format")
  printf "  %-22s op_ symbols=%s  %s\n" "$(basename $f)" "$n" "$a"
done
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
