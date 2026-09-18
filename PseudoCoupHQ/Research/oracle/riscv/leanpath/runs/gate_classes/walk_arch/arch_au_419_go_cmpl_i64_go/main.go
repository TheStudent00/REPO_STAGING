// probe 19 -- unary ^
package main

//go:noinline
func op_19(a int64) int64 {
	return ^a
}

var ga int64
var sink interface{}

func main() {
	sink = op_19(ga)
	_ = sink
}
