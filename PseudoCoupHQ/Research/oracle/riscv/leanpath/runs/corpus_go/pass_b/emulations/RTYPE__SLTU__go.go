package main

func op_542(a uint64, b uint64) bool {
	return a < b
}

func b2u(x bool) uint64 {
	if x {
		return 1
	}
	return 0
}

//go:noinline
func emu_RTYPE__SLTU(a uint64, b uint64) uint64 {
	return b2u(op_542(uint64(a), uint64(b)))
}

var sink interface{}

func main() {
	sink = emu_RTYPE__SLTU(0, 0)
	_ = sink
}
