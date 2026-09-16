// probe 604 -- binary >
package main

//go:noinline
func op_604(a int32, b float64) bool {
	return a > b
}

var ga int32
var gb float64
var sink interface{}

func main() {
	sink = op_604(ga, gb)
	_ = sink
}
