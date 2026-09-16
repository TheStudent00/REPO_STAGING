// probe 22 -- unary ^
package main

//go:noinline
func op_22(a float64) float64 {
	return ^a
}

var ga float64
var sink interface{}

func main() {
	sink = op_22(ga)
	_ = sink
}
