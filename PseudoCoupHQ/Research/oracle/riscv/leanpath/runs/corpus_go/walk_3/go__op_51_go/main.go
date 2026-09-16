// probe 51 -- unary --
package main

//go:noinline
func op_51(a float32) float32 {
	return a--
}

var ga float32
var sink interface{}

func main() {
	sink = op_51(ga)
	_ = sink
}
