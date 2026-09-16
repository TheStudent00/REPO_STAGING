// probe 483 -- binary ==
package main

//go:noinline
func op_483(a float64, b float32) bool {
	return a == b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_483(ga, gb)
	_ = sink
}
