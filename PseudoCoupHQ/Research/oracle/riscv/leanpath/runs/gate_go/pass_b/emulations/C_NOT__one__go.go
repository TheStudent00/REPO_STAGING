package main

func op_19(a int64) int64 {
	return ^a
}

//go:noinline
func emu_C_NOT__one(a uint64) uint64 {
	return uint64(op_19(int64(a)))
}

var sink interface{}

func main() {
	sink = emu_C_NOT__one(0)
	_ = sink
}
