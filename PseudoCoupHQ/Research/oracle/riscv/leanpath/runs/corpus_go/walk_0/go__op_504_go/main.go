// probe 504 -- binary !=
package main

//go:noinline
func op_504(a uint64, b int32) bool {
	return a != b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_504(ga, gb)
	_ = sink
}
