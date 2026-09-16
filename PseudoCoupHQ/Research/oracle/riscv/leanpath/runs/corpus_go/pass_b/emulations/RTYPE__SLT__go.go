package main

func op_535(a int64, b int64) bool {
	return a < b
}

func b2u(x bool) uint64 {
	if x {
		return 1
	}
	return 0
}

//go:noinline
func emu_RTYPE__SLT(a uint64, b uint64) uint64 {
	return b2u(op_535(int64(a), int64(b)))
}

var sink interface{}

func main() {
	sink = emu_RTYPE__SLT(0, 0)
	_ = sink
}
