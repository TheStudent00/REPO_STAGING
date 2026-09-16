// probe 2 -- unary +
package main

//go:noinline
func op_2(a uint64) uint64 {
	return +a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_2(ga)
	_ = sink
}
