// probe 634 -- binary >
package main

//go:noinline
func op_634(a bool, b float64) bool {
	return a > b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_634(ga, gb)
	_ = sink
}
