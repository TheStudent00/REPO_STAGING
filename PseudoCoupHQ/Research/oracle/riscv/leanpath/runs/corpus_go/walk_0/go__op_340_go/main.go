// probe 340 -- binary +
package main

//go:noinline
func op_340(a float64, b float64) float64 {
	return a + b
}

var ga float64
var gb float64
var sink interface{}

func main() {
	sink = op_340(ga, gb)
	_ = sink
}
