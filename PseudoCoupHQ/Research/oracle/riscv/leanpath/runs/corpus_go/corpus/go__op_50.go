// probe 50 -- unary --
package main

//go:noinline
func op_50(a uint64) uint64 {
	return a--
}

var ga uint64
var sink interface{}

func main() {
	sink = op_50(ga)
	_ = sink
}
