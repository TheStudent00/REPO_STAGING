// probe 108 -- binary /
package main

//go:noinline
func op_108(a uint64, b int32) uint64 {
	return a / b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_108(ga, gb)
	_ = sink
}
