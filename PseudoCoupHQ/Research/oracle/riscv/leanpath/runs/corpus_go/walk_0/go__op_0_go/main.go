// probe 0 -- unary +
package main

//go:noinline
func op_0(a int32) int32 {
	return +a
}

var ga int32
var sink interface{}

func main() {
	sink = op_0(ga)
	_ = sink
}
