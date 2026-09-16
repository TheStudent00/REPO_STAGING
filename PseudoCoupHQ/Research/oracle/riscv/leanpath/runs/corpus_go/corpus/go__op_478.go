// probe 478 -- binary ==
package main

//go:noinline
func op_478(a float32, b float64) bool {
	return a == b
}

var ga float32
var gb float64
var sink interface{}

func main() {
	sink = op_478(ga, gb)
	_ = sink
}
