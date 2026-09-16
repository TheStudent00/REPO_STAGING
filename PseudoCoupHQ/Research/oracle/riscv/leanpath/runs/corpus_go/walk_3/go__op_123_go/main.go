// probe 123 -- binary /
package main

//go:noinline
func op_123(a float64, b float32) float64 {
	return a / b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_123(ga, gb)
	_ = sink
}
