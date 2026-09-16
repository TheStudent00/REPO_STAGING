// probe 494 -- binary !=
package main

//go:noinline
func op_494(a int32, b uint64) bool {
	return a != b
}

var ga int32
var gb uint64
var sink interface{}

func main() {
	sink = op_494(ga, gb)
	_ = sink
}
