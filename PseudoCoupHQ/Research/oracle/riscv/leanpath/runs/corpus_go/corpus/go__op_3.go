// probe 3 -- unary +
package main

//go:noinline
func op_3(a float32) float32 {
	return +a
}

var ga float32
var sink interface{}

func main() {
	sink = op_3(ga)
	_ = sink
}
