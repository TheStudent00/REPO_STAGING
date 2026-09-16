// probe 20 -- unary ^
package main

//go:noinline
func op_20(a uint64) uint64 {
	return ^a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_20(ga)
	_ = sink
}
