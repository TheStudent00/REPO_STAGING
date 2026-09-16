// probe 31 -- unary &
package main

//go:noinline
func op_31(a int64) *int64 {
	return &a
}

var ga int64
var sink interface{}

func main() {
	sink = op_31(ga)
	_ = sink
}
