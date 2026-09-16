// probe 274 -- binary &
package main

//go:noinline
func op_274(a bool, b float64) bool {
	return a & b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_274(ga, gb)
	_ = sink
}
