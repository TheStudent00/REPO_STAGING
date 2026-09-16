// probe 89 -- binary *
package main

//go:noinline
func op_89(a float64, b bool) float64 {
	return a * b
}

var ga float64
var gb bool
var sink interface{}

func main() {
	sink = op_89(ga, gb)
	_ = sink
}
