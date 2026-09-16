// probe 470 -- binary ==
package main

//go:noinline
func op_470(a uint64, b uint64) bool {
	return a == b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_470(ga, gb)
	_ = sink
}
