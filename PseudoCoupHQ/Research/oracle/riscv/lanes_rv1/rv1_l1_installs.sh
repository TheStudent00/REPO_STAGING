#!/usr/bin/env bash
# rv1 lane 1 -- the brief's section 1: verify every install the coordinator
# made, each with a ONE-LINE probe whose output is quoted LITERAL in the log.
# A tool that is absent is a FLAG, not a workaround, so this lane never
# exits non-zero on an absent tool: it prints ABSENT and carries on.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
total=8

say() { echo "--- $1"; }

echo "[1/$total] rust: the riscv64gc-unknown-none-elf target"
say "rustc --print target-list | grep -c riscv64"
rustc --print target-list 2>&1 | grep -c riscv64 || echo "ABSENT: rustc"
say "rustup target list --installed"
rustup target list --installed 2>&1 || echo "ABSENT: rustup"
say "ls \$(rustc --print sysroot)/lib/rustlib"
ls "$(rustc --print sysroot 2>/dev/null)/lib/rustlib" 2>&1 || echo "ABSENT"

echo "[2/$total] clang for riscv64"
say "clang --version | head -1"
clang --version 2>&1 | head -1 || echo "ABSENT: clang"
say "printf 'int f(int a,int b){return a+b;}' | clang --target=riscv64-unknown-linux-gnu -c -x c - -o /tmp/rv_probe.o ; echo rc=\$?"
printf 'int f(int a,int b){return a+b;}\n' | clang --target=riscv64-unknown-linux-gnu -O1 -c -x c - -o /tmp/rv_probe.o 2>&1; echo "rc=$?"
say "file /tmp/rv_probe.o"
file /tmp/rv_probe.o 2>&1 || echo "ABSENT: file"

echo "[3/$total] llvm-objdump carves it"
say "llvm-objdump --version | head -2"
llvm-objdump --version 2>&1 | head -3 || echo "ABSENT: llvm-objdump"
say "llvm-objdump -dr --disassemble=f /tmp/rv_probe.o"
llvm-objdump -dr --disassemble=f /tmp/rv_probe.o 2>&1 || echo "ABSENT"

echo "[4/$total] go for riscv64"
say "go version"
go version 2>&1 || echo "ABSENT: go"
export HOME=/work
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p /work/rv1probe "$GOCACHE" "$GOPATH"
cat > /work/rv1probe/go.mod <<'EOF'
module rvprobe

go 1.26
EOF
cat > /work/rv1probe/main.go <<'EOF'
package main

//go:noinline
func Op(a int32, b int32) int32 { return a + b }

func main() { println(Op(1, 2)) }
EOF
say "cd /work/rv1probe && GOARCH=riscv64 GOOS=linux go build -o bin_rv . ; echo rc=\$?"
( cd /work/rv1probe && GOARCH=riscv64 GOOS=linux go build -o bin_rv . 2>&1; echo "rc=$?" )
say "file /work/rv1probe/bin_rv"
file /work/rv1probe/bin_rv 2>&1 || true
say "llvm-objdump -d --disassemble='main.Op' /work/rv1probe/bin_rv | head -20"
llvm-objdump -d --disassemble='main.Op' /work/rv1probe/bin_rv 2>&1 | head -20 || true

echo "[5/$total] Sail: the opam-built compiler and the model simulator"
say "which sail sail_riscv_sim"
which sail 2>&1 || echo "ABSENT: sail"
which sail_riscv_sim 2>&1 || echo "ABSENT: sail_riscv_sim on PATH"
say "ls -la /opt /usr/local/bin | grep -i sail"
ls -la /opt 2>/dev/null | grep -i sail || true
ls -la /usr/local/bin 2>/dev/null | grep -i sail || true
say "find / -maxdepth 5 -name 'sail_riscv_sim*' -not -path '/proc/*' 2>/dev/null"
find / -maxdepth 6 -name 'sail_riscv_sim*' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null | head -10
say "sail --version"
sail --version 2>&1 | head -3 || true

echo "[6/$total] sail_riscv_sim --help (the flags the brief says name the reset address)"
SIM="$(command -v sail_riscv_sim || find / -maxdepth 6 -name 'sail_riscv_sim' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null | head -1)"
echo "SIM=$SIM"
if [ -n "$SIM" ]; then "$SIM" --help 2>&1 | head -120; else echo "ABSENT: sail_riscv_sim"; fi

echo "[7/$total] the Sail model's own source, mounted"
say "ls /sources/sail-riscv"
ls /sources/sail-riscv 2>&1 | head -20 || echo "ABSENT: /sources/sail-riscv"
say "ls /sources/sail-riscv/model | head -40"
ls /sources/sail-riscv/model 2>&1 | head -40 || true
say "wc -l /sources/sail-riscv/model/riscv_insts_base.sail"
wc -l /sources/sail-riscv/model/riscv_insts_base.sail 2>&1 || true

echo "[8/$total] the rest of the toolchain this task uses"
say "python3 -c 'import z3; print(z3.get_version_string())'"
python3 -c 'import z3; print("z3", z3.get_version_string())' 2>&1 || echo "ABSENT: z3"
say "riscv64-linux-gnu-gcc --version | head -1  (a native riscv toolchain, if any)"
riscv64-linux-gnu-gcc --version 2>&1 | head -1 || echo "ABSENT: riscv64-linux-gnu-gcc"
say "ld.lld --version"
ld.lld --version 2>&1 | head -1 || echo "ABSENT: ld.lld"
say "clang --target=riscv64-unknown-elf -march=rv64gc -mabi=lp64d -nostdlib probe"
printf 'void _start(void){}\n' > /tmp/rv_start.c
clang --target=riscv64-unknown-elf -march=rv64gc -mabi=lp64d -nostdlib -fuse-ld=lld -Wl,-Ttext=0x80000000 /tmp/rv_start.c -o /tmp/rv_start.elf 2>&1; echo "rc=$?"
file /tmp/rv_start.elf 2>&1 || true

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
