#!/usr/bin/env bash
# rv1 lane 5 -- the three causes lane 4 found, each probed to its remedy:
#   (a) the image has no riscv64 glibc headers -> -nostdlibinc alone, with
#       -ffreestanding beside it, so the two can be compared for codegen;
#   (b) llvm-objdump has no --no-aliases; its own spelling is -M no-aliases;
#   (c) go's riscv64 ELF carries no RISC-V attributes, so the disassembler
#       decodes the compressed halfwords as <unknown> -> --mattr.
set -u
export HOME=/work
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p "$GOCACHE" "$GOPATH"
total=4
W=/work/rv1rem; rm -rf $W; mkdir -p $W
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

echo "[1/$total] -nostdlibinc alone (the optimisation level untouched)"
clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc -c $W/unit.c -o $W/a.o 2>&1 | head -5
echo "rc=$?"
echo "--- llvm-objdump -dr -M no-aliases --disassemble-symbols=op_174"
llvm-objdump -dr -M no-aliases --disassemble-symbols=op_174 $W/a.o 2>&1 | head -20

echo "[2/$total] -ffreestanding -nostdlibinc, for comparison"
clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -ffreestanding -nostdlibinc -c $W/unit.c -o $W/b.o 2>&1 | head -5
llvm-objdump -dr -M no-aliases --disassemble-symbols=op_174 $W/b.o 2>&1 | head -20
echo "--- byte-identical? "
cmp -s $W/a.o $W/b.o && echo "the two objects are byte identical" || echo "the two objects DIFFER"

echo "[3/$total] the same object with aliases on, so both spellings are on the page"
llvm-objdump -dr --disassemble-symbols=op_174 $W/a.o 2>&1 | head -20

echo "[4/$total] go: the compressed halfwords decoded with --mattr"
G=/work/rv1rem_go; rm -rf $G; mkdir -p $G
printf 'module opprobe\n\ngo 1.26\n' > $G/go.mod
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
echo "--- default (no --mattr)"
llvm-objdump -d --disassemble-symbols=main.op_312 $G/bin_rv 2>&1 | head -12
echo "--- --mattr=+m,+a,+f,+d,+c"
llvm-objdump -d -M no-aliases --mattr=+m,+a,+f,+d,+c --disassemble-symbols=main.op_312 $G/bin_rv 2>&1 | head -12
echo "--- GORISCV64 default, and what go says it targets"
( cd $G && GOARCH=riscv64 GOOS=linux go env GORISCV64 GOARCH GOOS 2>&1 )

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
