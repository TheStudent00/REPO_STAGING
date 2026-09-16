#!/bin/bash
# lp3_l21_cross_toolchains.sh -- which of the four languages can emit a
# riscv64 object in this container without fetching: clang (c, cpp),
# rustc (its installed targets), go (its native cross-compile).
set -uo pipefail
export PATH=/persist/lp1/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache /work/t && cd /work/t
echo "--- clang c"; printf '#include <stdint.h>\nuint64_t f(uint64_t a, uint64_t b){return a*b;}\n' > t.c; clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr -c t.c -o t_c.o && llvm-objdump -d t_c.o | grep -E "^\s+[0-9a-f]+:" | head -3
echo "--- clang++ cpp"; printf '#include <cstdint>\nextern "C" uint64_t f(uint64_t a, uint64_t b){return a*b;}\n' > t.cpp; clang++ -std=c++17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr -c t.cpp -o t_cpp.o && llvm-objdump -d t_cpp.o | grep -E "^\s+[0-9a-f]+:" | head -3
echo "--- rustc targets"; rustc --version; rustup target list --installed 2>&1 | head; ls /opt/rustup/toolchains/*/lib/rustlib/ 2>/dev/null | head; ls /persist/rustup076/toolchains/*/lib/rustlib/ 2>/dev/null | head
printf '#[no_mangle] pub extern "C" fn f(a: u64, b: u64) -> u64 { a.wrapping_mul(b) }\n' > t.rs
rustc --target riscv64gc-unknown-linux-gnu --crate-type lib --emit obj -O -o t_rs.o t.rs 2>&1 | head -3 && llvm-objdump -d t_rs.o 2>/dev/null | grep -E "^\s+[0-9a-f]+:" | head -3
echo "--- go"; go version; printf 'package main\n//go:noinline\nfunc F(a, b uint64) uint64 { return a * b }\nfunc main() { println(F(3, 4)) }\n' > main.go; printf 'module t\n\ngo 1.26\n' > go.mod
GOARCH=riscv64 GOOS=linux go build -o t_go . 2>&1 | head -3 && llvm-objdump -d t_go 2>/dev/null | sed -n '/<main.F>:/,/ret/p' | head -6
echo done
