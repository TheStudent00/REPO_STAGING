// probe 351 -- binary -
package main

//go:noinline
func op_351(a int32, b float32) int32 {
	return a - b
}

var ga int32
var gb float32
var sink interface{}

func main() {
	sink = op_351(ga, gb)
	_ = sink
}
