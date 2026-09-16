// probe 28 -- unary *
package main

//go:noinline
func op_28(a float64) float64 {
	return *a
}

var ga float64
var sink interface{}

func main() {
	sink = op_28(ga)
	_ = sink
}
