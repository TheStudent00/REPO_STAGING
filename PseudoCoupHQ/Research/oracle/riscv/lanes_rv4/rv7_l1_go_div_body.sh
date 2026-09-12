#!/bin/bash
# the owner's question, 2026-09-12: with the zero case handled upstream, does go's
# compiler drop its own zero-divisor check? Compile the divide emulation's
# shape at ship flags for riscv64 and print the body.
set -u
export HOME=/work GOCACHE=/work/rv7gocache GOPATH=/work/rv7gopath GOARCH=riscv64 GOOS=linux
mkdir -p /work/rv7 "$GOCACHE" "$GOPATH"; cd /work/rv7
cat > go.mod <<'EOM'
module emu
go 1.22
EOM
cat > main.go <<'EOM'
package main

//go:noinline
func emu_div(a1 uint64, a2 uint64) uint64 {
	if a2 == 0 {
		return ^uint64(0)
	}
	if a2 == ^uint64(0) && a1 == 1<<63 {
		return 1 << 63
	}
	return uint64(int64(a1) / int64(a2))
}

//go:noinline
func plain_div(a1 uint64, a2 uint64) uint64 {
	return uint64(int64(a1) / int64(a2))
}

func main() { println(emu_div(7, 3), plain_div(7, 3)) }
EOM
go build -o bin_rv . && echo "built"
echo "===== the emulation (zero and overflow handled upstream):"
llvm-objdump -d --mattr=+m,+a,+f,+d,+c -M no-aliases --disassemble-symbols=main.emu_div bin_rv | sed -n '/emu_div/,$p' | head -40
echo "===== plain a/b, for comparison (go's own checks visible):"
llvm-objdump -d --mattr=+m,+a,+f,+d,+c -M no-aliases --disassemble-symbols=main.plain_div bin_rv | sed -n '/plain_div/,$p' | head -30
