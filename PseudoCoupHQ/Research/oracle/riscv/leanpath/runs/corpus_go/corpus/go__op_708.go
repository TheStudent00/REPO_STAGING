// probe 708 -- binary ||
package main

//go:noinline
func op_708(a int32, b int32) bool {
	return a || b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = op_708(ga, gb)
	_ = sink
}
