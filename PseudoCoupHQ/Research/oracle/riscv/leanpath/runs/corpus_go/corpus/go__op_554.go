// probe 554 -- binary <
package main

//go:noinline
func op_554(a float64, b uint64) bool {
	return a < b
}

var ga float64
var gb uint64
var sink interface{}

func main() {
	sink = op_554(ga, gb)
	_ = sink
}
