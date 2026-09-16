// probe 377 -- binary -
package main

//go:noinline
func op_377(a float64, b bool) float64 {
	return a - b
}

var ga float64
var gb bool
var sink interface{}

func main() {
	sink = op_377(ga, gb)
	_ = sink
}
