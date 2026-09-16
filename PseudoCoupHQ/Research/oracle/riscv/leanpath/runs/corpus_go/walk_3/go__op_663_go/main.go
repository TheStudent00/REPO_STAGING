// probe 663 -- binary >=
package main

//go:noinline
func op_663(a float64, b float32) bool {
	return a >= b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_663(ga, gb)
	_ = sink
}
