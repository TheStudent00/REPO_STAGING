// probe 34 -- unary &
package main

//go:noinline
func op_34(a float64) *float64 {
	return &a
}

var ga float64
var sink interface{}

func main() {
	sink = op_34(ga)
	_ = sink
}
