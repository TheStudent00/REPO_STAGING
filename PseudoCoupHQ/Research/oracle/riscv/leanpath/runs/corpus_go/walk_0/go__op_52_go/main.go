// probe 52 -- unary --
package main

//go:noinline
func op_52(a float64) float64 {
	return a--
}

var ga float64
var sink interface{}

func main() {
	sink = op_52(ga)
	_ = sink
}
