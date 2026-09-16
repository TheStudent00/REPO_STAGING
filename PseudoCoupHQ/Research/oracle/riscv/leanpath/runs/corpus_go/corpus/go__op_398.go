// probe 398 -- binary |
package main

//go:noinline
func op_398(a uint64, b uint64) uint64 {
	return a | b
}

var ga uint64
var gb uint64
var sink interface{}

func main() {
	sink = op_398(ga, gb)
	_ = sink
}
