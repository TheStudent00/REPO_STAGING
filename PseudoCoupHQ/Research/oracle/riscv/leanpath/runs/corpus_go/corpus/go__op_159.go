// probe 159 -- binary %
package main

//go:noinline
func op_159(a float64, b float32) float64 {
	return a % b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_159(ga, gb)
	_ = sink
}
