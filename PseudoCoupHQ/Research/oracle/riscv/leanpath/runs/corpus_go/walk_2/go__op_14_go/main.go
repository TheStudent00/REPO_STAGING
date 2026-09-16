// probe 14 -- unary !
package main

//go:noinline
func op_14(a uint64) bool {
	return !a
}

var ga uint64
var sink interface{}

func main() {
	sink = op_14(ga)
	_ = sink
}
