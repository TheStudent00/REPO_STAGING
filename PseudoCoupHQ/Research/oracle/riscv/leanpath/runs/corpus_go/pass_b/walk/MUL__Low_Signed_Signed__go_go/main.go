package main

func op_74(a uint64, b uint64) uint64 {
	return a * b
}

func b2u(x bool) uint64 {
	if x {
		return 1
	}
	return 0
}

//go:noinline
func emu_MUL__Low_Signed_Signed(a uint64, b uint64) uint64 {
	return uint64(op_74(uint64(a), uint64(b)))
}

var sink interface{}

func main() {
	sink = emu_MUL__Low_Signed_Signed(0, 0)
	_ = sink
}
