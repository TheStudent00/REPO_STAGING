// probe 58 -- unary ...
package main

//go:noinline
func op_58(a float64) float64 {
	return a...
}

var ga float64
var sink interface{}

func main() {
	sink = op_58(ga)
	_ = sink
}
