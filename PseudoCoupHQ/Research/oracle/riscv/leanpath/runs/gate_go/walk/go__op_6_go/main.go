// probe 6 -- unary -
package main

//go:noinline
func op_6(a int32) int32 {
	return -a
}

var ga int32
var sink interface{}

func main() {
	sink = op_6(ga)
	_ = sink
}
