// probe 8 -- unary -
package main

//go:noinline
func op_8(a uint64) uint64 {
	return -a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_8(ga)
	_ = sink
}
