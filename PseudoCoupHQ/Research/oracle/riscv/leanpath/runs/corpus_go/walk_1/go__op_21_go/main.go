// probe 21 -- unary ^
package main

//go:noinline
func op_21(a float32) float32 {
	return ^a
}

var ga float32
var sink interface{}

func main() {
	sink = op_21(ga)
	_ = sink
}
