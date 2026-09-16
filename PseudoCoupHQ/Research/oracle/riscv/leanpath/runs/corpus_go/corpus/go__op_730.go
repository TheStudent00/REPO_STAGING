// probe 730 -- binary ||
package main

//go:noinline
func op_730(a float32, b float64) bool {
	return a || b
}

var ga float32
var gb float64
var sink interface{}

func main() {
	sink = op_730(ga, gb)
	_ = sink
}
