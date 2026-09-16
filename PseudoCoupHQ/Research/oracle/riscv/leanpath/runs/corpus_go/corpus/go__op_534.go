// probe 534 -- binary <
package main

//go:noinline
func op_534(a int64, b int32) bool {
	return a < b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_534(ga, gb)
	_ = sink
}
