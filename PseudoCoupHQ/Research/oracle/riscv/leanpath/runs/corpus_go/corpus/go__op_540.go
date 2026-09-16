// probe 540 -- binary <
package main

//go:noinline
func op_540(a uint64, b int32) bool {
	return a < b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_540(ga, gb)
	_ = sink
}
