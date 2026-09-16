package main

func op_542(a uint64, b uint64) bool {
	return a < b
}

//go:noinline
func emu_RTYPE__SLTU(a uint64, b uint64) uint64 {
	return uint64(op_542(uint64(a), uint64(b)))
}

var sink interface{}

func main() {
	sink = emu_RTYPE__SLTU(0, 0)
	_ = sink
}
