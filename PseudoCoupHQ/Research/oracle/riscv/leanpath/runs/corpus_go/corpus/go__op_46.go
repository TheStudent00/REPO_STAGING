// probe 46 -- unary ++
package main

//go:noinline
func op_46(a float64) float64 {
	return a++
}

var ga float64
var sink interface{}

func main() {
	sink = op_46(ga)
	_ = sink
}
