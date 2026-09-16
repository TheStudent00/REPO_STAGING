package main

func op_20(a uint64) uint64 {
	return ^a
}

func b2u(x bool) uint64 {
	if x {
		return 1
	}
	return 0
}

//go:noinline
func emu_C_NOT__one(a uint64) uint64 {
	return uint64(op_20(uint64(a)))
}

var sink interface{}

func main() {
	sink = emu_C_NOT__one(0)
	_ = sink
}
