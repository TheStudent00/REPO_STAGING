// probe 26 -- unary *
package main

//go:noinline
func op_26(a uint64) uint64 {
	return *a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_26(ga)
	_ = sink
}
