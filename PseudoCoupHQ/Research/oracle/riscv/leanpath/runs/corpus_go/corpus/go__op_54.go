// probe 54 -- unary ...
package main

//go:noinline
func op_54(a int32) int32 {
	return a...
}

var ga int32
var sink interface{}

func main() {
	sink = op_54(ga)
	_ = sink
}
