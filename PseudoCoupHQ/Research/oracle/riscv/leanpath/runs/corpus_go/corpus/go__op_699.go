// probe 699 -- binary &&
package main

//go:noinline
func op_699(a float64, b float32) bool {
	return a && b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_699(ga, gb)
	_ = sink
}
