// probe 4 -- unary +
package main

//go:noinline
func op_4(a float64) float64 {
	return +a
}

var ga float64
var sink interface{}

func main() {
	sink = op_4(ga)
	_ = sink
}
