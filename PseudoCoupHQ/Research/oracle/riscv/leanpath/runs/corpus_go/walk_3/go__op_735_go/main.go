// probe 735 -- binary ||
package main

//go:noinline
func op_735(a float64, b float32) bool {
	return a || b
}

var ga float64
var gb float32
var sink interface{}

func main() {
	sink = op_735(ga, gb)
	_ = sink
}
