// probe 24 -- unary *
package main

//go:noinline
func op_24(a int32) int32 {
	return *a
}

var ga int32
var sink interface{}

func main() {
	sink = op_24(ga)
	_ = sink
}
