// probe 16 -- unary !
package main

//go:noinline
func op_16(a float64) bool {
	return !a
}

var ga float64
var sink interface{}

func main() {
	sink = op_16(ga)
	_ = sink
}
