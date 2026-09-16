// probe 18 -- unary ^
package main

//go:noinline
func op_18(a int32) int32 {
	return ^a
}

var ga int32
var sink interface{}

func main() {
	sink = op_18(ga)
	_ = sink
}
