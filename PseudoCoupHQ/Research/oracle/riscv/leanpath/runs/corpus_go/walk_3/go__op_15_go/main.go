// probe 15 -- unary !
package main

//go:noinline
func op_15(a float32) bool {
	return !a
}

var ga float32
var sink interface{}

func main() {
	sink = op_15(ga)
	_ = sink
}
