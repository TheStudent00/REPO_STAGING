// probe 598 -- binary <=
package main

//go:noinline
func op_598(a bool, b float64) bool {
	return a <= b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_598(ga, gb)
	_ = sink
}
