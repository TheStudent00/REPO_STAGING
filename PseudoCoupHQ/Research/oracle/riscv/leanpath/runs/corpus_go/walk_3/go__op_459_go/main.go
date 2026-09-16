// probe 459 -- binary ==
package main

//go:noinline
func op_459(a int32, b float32) bool {
	return a == b
}

var ga int32
var gb float32
var sink interface{}

func main() {
	sink = op_459(ga, gb)
	_ = sink
}
