// probe 603 -- binary >
package main

//go:noinline
func op_603(a int32, b float32) bool {
	return a > b
}

var ga int32
var gb float32
var sink interface{}

func main() {
	sink = op_603(ga, gb)
	_ = sink
}
