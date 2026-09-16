// probe 664 -- binary >=
package main

//go:noinline
func op_664(a float64, b float64) bool {
	return a >= b
}

var ga float64
var gb float64
var sink interface{}

func main() {
	sink = op_664(ga, gb)
	_ = sink
}
