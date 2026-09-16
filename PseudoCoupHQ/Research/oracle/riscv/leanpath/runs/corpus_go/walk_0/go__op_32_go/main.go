// probe 32 -- unary &
package main

//go:noinline
func op_32(a uint64) *uint64 {
	return &a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_32(ga)
	_ = sink
}
