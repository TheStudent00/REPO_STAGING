// probe 736 -- binary ||
package main

//go:noinline
func op_736(a float64, b float64) bool {
	return a || b
}

var ga float64
var gb float64
var sink interface{}

func main() {
	sink = op_736(ga, gb)
	_ = sink
}
