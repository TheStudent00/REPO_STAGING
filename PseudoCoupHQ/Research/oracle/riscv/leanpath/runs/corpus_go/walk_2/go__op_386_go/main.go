// probe 386 -- binary |
package main

//go:noinline
func op_386(a int32, b uint64) int32 {
	return a | b
}

var ga int32
var gb uint64
var sink interface{}

func main() {
	sink = op_386(ga, gb)
	_ = sink
}
