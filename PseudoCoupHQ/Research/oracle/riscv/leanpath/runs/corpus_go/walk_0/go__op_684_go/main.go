// probe 684 -- binary &&
package main

//go:noinline
func op_684(a uint64, b int32) bool {
	return a && b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_684(ga, gb)
	_ = sink
}
