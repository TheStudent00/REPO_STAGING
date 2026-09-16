// probe 687 -- binary &&
package main

//go:noinline
func op_687(a uint64, b float32) bool {
	return a && b
}

var ga uint64
var gb float32
var sink interface{}

func main() {
	sink = op_687(ga, gb)
	_ = sink
}
