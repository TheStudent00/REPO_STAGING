package main

func op_535(a int64, b int64) bool {
	return a < b
}

//go:noinline
func emu_RTYPE__SLT(a uint64, b uint64) uint64 {
	return uint64(op_535(int64(a), int64(b)))
}

var sink interface{}

func main() {
	sink = emu_RTYPE__SLT(0, 0)
	_ = sink
}
