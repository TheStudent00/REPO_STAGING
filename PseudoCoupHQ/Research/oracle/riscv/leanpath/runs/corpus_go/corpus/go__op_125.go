// probe 125 -- binary /
package main

//go:noinline
func op_125(a float64, b bool) float64 {
	return a / b
}

var ga float64
var gb bool
var sink interface{}

func main() {
	sink = op_125(ga, gb)
	_ = sink
}
