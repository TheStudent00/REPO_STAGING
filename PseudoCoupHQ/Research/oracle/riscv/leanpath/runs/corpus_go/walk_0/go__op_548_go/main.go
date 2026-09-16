// probe 548 -- binary <
package main

//go:noinline
func op_548(a float32, b uint64) bool {
	return a < b
}

var ga float32
var gb uint64
var sink interface{}

func main() {
	sink = op_548(ga, gb)
	_ = sink
}
