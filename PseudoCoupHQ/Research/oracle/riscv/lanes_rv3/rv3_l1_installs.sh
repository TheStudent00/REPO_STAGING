#!/usr/bin/env bash
# rv3 lane 1 -- the installs task rv2's flags 2, 3 and 7 asked for, each
# verified with a one-line probe, LITERAL: the rust riscv64 LINUX target
# (with a standard library), the riscv64 gcc cross toolchain (glibc and
# libstdc++ headers), clang aimed at riscv64 through it for c and for cpp,
# and llvm-objdump's own flag spellings.
set -u
export HOME=/work
export GOCACHE=/work/rv3gocache GOPATH=/work/rv3gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv3probe
total=8

echo "[1/$total] the tools, each with its own probe"
clang --version | head -1
llvm-objdump --version | head -2
go version
rustc --version
rustup target list --installed
python3 -c 'import z3; print("z3", z3.get_version_string())'

echo "[2/$total] the riscv64 gcc cross toolchain and where its headers sit"
ls -d /usr/riscv64-linux-gnu/include 2>&1
ls /usr/riscv64-linux-gnu/include/string.h 2>&1
which riscv64-linux-gnu-g++ riscv64-linux-gnu-gcc 2>&1
riscv64-linux-gnu-g++ --version 2>&1 | head -1

echo "[3/$total] clang for riscv64 on c, with string.h"
cat > /work/rv3probe/probe.c <<'EOF'
#include <stdint.h>
#include <string.h>
int32_t probe(int32_t a, int32_t b) { return a + b; }
double bits(int64_t a) { double d; memcpy(&d, &a, 8); return d; }
EOF
clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr \
  -c /work/rv3probe/probe.c -o /work/rv3probe/probe.o
echo "clang c riscv64 rc=$?"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c \
  --disassemble-symbols=probe /work/rv3probe/probe.o | tail -4

echo "[4/$total] clang++ for riscv64 on cpp, with <vector>"
cat > /work/rv3probe/probe.cpp <<'EOF'
#include <cstdint>
#include <vector>
extern "C" int32_t probe_cpp(int32_t a, int32_t b) {
  std::vector<int32_t> v; v.push_back(a); v.push_back(b);
  return v[0] + v[1];
}
EOF
/usr/bin/clang++ -std=c++20 -O1 --target=riscv64-linux-gnu \
  --gcc-toolchain=/usr -c /work/rv3probe/probe.cpp \
  -o /work/rv3probe/probe_cpp.o
echo "clang++ cpp riscv64 rc=$?"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c \
  --disassemble-symbols=probe_cpp /work/rv3probe/probe_cpp.o | tail -4

echo "[5/$total] rustc for riscv64-unknown-linux-gnu, --emit=obj, no linker"
cat > /work/rv3probe/probe.rs <<'EOF'
#[no_mangle]
pub extern "C" fn probe(a: i32, b: i32) -> i32 { a.wrapping_add(b) }
EOF
rustc --crate-type=lib --emit=obj -C opt-level=1 -C debug-assertions=off \
  --target=riscv64gc-unknown-linux-gnu \
  -o /work/rv3probe/probe_rs.o /work/rv3probe/probe.rs
echo "rustc riscv64 linux rc=$?"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c \
  --disassemble-symbols=probe /work/rv3probe/probe_rs.o | tail -4

echo "[6/$total] rustc on a source that needs the standard library"
cat > /work/rv3probe/probe_std.rs <<'EOF'
#[no_mangle]
pub extern "C" fn probe_std(a: i64, b: i64) -> i64 {
    let v: Vec<i64> = vec![a, b];
    v[0].wrapping_mul(v[1])
}
EOF
rustc --crate-type=lib --emit=obj -C opt-level=1 -C debug-assertions=off \
  --target=riscv64gc-unknown-linux-gnu \
  -o /work/rv3probe/probe_std.o /work/rv3probe/probe_std.rs
echo "rustc riscv64 std rc=$?"

echo "[7/$total] swift for riscv64, asked and answered by name"
which swiftc 2>&1
swiftc --version 2>&1 | head -2
echo "swift riscv64 targets:"
swiftc -print-target-info -target riscv64-unknown-linux-gnu 2>&1 | head -6

echo "[8/$total] the Sail model and its simulator"
sail --version 2>&1
which sail_riscv_sim 2>&1
ls /sources/sail-riscv/model | head -5
echo "lane rv3_l1 done"
