// probe 10 -- unary -
package main

//go:noinline
func op_10(a float64) float64 {
	return -a
}

var ga float64
var sink interface{}

func main() {
	sink = op_10(ga)
	_ = sink
}
