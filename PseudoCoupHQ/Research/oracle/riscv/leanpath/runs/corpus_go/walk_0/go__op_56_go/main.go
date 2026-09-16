// probe 56 -- unary ...
package main

//go:noinline
func op_56(a uint64) uint64 {
	return a...
}

var ga uint64
var sink interface{}

func main() {
	sink = op_56(ga)
	_ = sink
}
