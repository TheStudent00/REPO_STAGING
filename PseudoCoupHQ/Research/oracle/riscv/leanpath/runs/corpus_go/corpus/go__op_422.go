// probe 422 -- binary ^
package main

//go:noinline
func op_422(a int32, b uint64) int32 {
	return a ^ b
}

var ga int32
var gb uint64
var sink interface{}

func main() {
	sink = op_422(ga, gb)
	_ = sink
}
