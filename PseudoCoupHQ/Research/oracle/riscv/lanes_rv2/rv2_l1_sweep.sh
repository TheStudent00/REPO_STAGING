#!/usr/bin/env bash
# rv2 lane 1 -- the tools this task needs, each verified with a one-line
# probe, then the RISC-V model table: the sweep over riscv_reference's own
# opcode table at every operand form and width, and the markdown beside it.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2probe
total=6

echo "[1/$total] the tools, each with its own probe"
clang --version | head -1
llvm-objdump --version | head -2
go version
rustc --version
rustup target list --installed
python3 -c 'import z3; print("z3", z3.get_version_string())'

echo "[2/$total] clang for riscv64, on a two-line c function"
cat > /work/rv2probe/probe.c <<'EOF'
#include <stdint.h>
int32_t probe(int32_t a, int32_t b) { return a + b; }
EOF
clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc \
  -c /work/rv2probe/probe.c -o /work/rv2probe/probe.o
echo "clang riscv64 rc=$?"
llvm-objdump -dr -M no-aliases --mattr=+m,+a,+f,+d,+c \
  --disassemble-symbols=probe /work/rv2probe/probe.o | tail -5

echo "[3/$total] rustc for riscv64, on the same function"
cat > /work/rv2probe/probe.rs <<'EOF'
#[no_mangle]
pub extern "C" fn probe(a: i32, b: i32) -> i32 { a.wrapping_add(b) }
EOF
rustc --crate-type=lib --emit=obj -C opt-level=1 -C debug-assertions=off \
  --target=riscv64gc-unknown-none-elf \
  -o /work/rv2probe/probe_rs.o /work/rv2probe/probe.rs
echo "rustc riscv64 rc=$?"

echo "[4/$total] go for riscv64"
mkdir -p /work/rv2probe/gomod
cat > /work/rv2probe/gomod/go.mod <<'EOF'
module opprobe

go 1.26
EOF
cat > /work/rv2probe/gomod/main.go <<'EOF'
package main

//go:noinline
func probe(a int32, b int32) int32 { return a + b }

var g0 int32
var sink interface{}

func main() { sink = probe(g0, g0); _ = sink }
EOF
( cd /work/rv2probe/gomod && GOARCH=riscv64 GOOS=linux GOTOOLCHAIN=local \
  GOPROXY=off GOFLAGS=-mod=mod go build -o /work/rv2probe/bin_rv . )
echo "go riscv64 rc=$?"

echo "[5/$total] the RISC-V model table -- the sweep"
python3 $RV/model_table_rv.py sweep $OP $RV/model_table_rv

echo "[6/$total] the markdown beside it, then the spelling guard"
python3 $RV/model_table_rv.py report $RV/model_table_rv
python3 $OP/check_no_spelling_keys.py $RV/model_table_rv.json
echo "guard rc=$?"

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
