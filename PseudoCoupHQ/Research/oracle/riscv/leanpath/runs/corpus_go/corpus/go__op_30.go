// probe 30 -- unary &
package main

//go:noinline
func op_30(a int32) *int32 {
	return &a
}

var ga int32
var sink interface{}

func main() {
	sink = op_30(ga)
	_ = sink
}
