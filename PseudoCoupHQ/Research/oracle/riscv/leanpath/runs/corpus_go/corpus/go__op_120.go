// probe 120 -- binary /
package main

//go:noinline
func op_120(a float64, b int32) float64 {
	return a / b
}

var ga float64
var gb int32
var sink interface{}

func main() {
	sink = op_120(ga, gb)
	_ = sink
}
