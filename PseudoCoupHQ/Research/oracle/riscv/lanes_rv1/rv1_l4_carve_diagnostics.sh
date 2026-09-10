#!/usr/bin/env bash
# rv1 lane 4 -- why lane 3's ten compiles refused: the compiler's own words,
# LITERAL, and the two candidate remedies probed side by side.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p "$GOCACHE" "$GOPATH"
total=5

echo "[1/$total] the diagnostics lane 3 recorded"
python3 -c "
import json
d = json.load(open('$RV/carved.json'))
for r in d['rows']:
    print('%-12s %-10s %s' % (r['unit'], r['outcome'], r.get('compile_command','')))
    print('    %s' % (r.get('diagnostic','') or '(none)')[:400])
"

echo "[2/$total] the c probe as lane 3 compiles it, by hand"
W=/work/rv1diag; rm -rf $W; mkdir -p $W
cat > $W/unit.c <<'EOF'
/* probe 174 -- binary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} * (int32_t){0})
op_174(int32_t a, int32_t b)
{
    return a * b;
}
EOF
echo "--- clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -c"
clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -c $W/unit.c -o $W/a.o 2>&1 | head -20; echo "rc=$?"

echo "[3/$total] remedy A: -nostdlibinc, clang's own freestanding headers"
clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -ffreestanding -nostdlibinc -c $W/unit.c -o $W/b.o 2>&1 | head -20; echo "rc=$?"
llvm-objdump -dr --no-aliases --disassemble-symbols=op_174 $W/b.o 2>&1 | head -20

echo "[4/$total] remedy B: --target=riscv64-unknown-elf"
clang -std=c17 -O1 --target=riscv64-unknown-elf -march=rv64gc -mabi=lp64d -c $W/unit.c -o $W/c.o 2>&1 | head -20; echo "rc=$?"
llvm-objdump -dr --no-aliases --disassemble-symbols=op_174 $W/c.o 2>&1 | head -20

echo "[5/$total] go: what symbols the riscv64 binary actually carries"
G=/work/rv1diag_go; rm -rf $G; mkdir -p $G
cat > $G/go.mod <<'EOF'
module opprobe

go 1.26
EOF
cat > $G/main.go <<'EOF'
// probe 312 -- binary +
package main

//go:noinline
func op_312(a int32, b int32) int32 {
	return a + b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = op_312(ga, gb)
	_ = sink
}
EOF
( cd $G && GOARCH=riscv64 GOOS=linux GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod go build -o $G/bin_rv . 2>&1; echo "go rc=$?" )
echo "--- llvm-objdump -t | grep op_312"
llvm-objdump -t $G/bin_rv 2>&1 | grep -i "op_312" | head -5
echo "--- llvm-objdump -dr --no-aliases --disassemble-symbols=main.op_312"
llvm-objdump -dr --no-aliases --disassemble-symbols=main.op_312 $G/bin_rv 2>&1 | head -25
echo "--- with aliases, for comparison"
llvm-objdump -d --disassemble-symbols=main.op_312 $G/bin_rv 2>&1 | head -25

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
