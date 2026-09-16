// probe 33 -- unary &
package main

//go:noinline
func op_33(a float32) *float32 {
	return &a
}

var ga float32
var sink interface{}

func main() {
	sink = op_33(ga)
	_ = sink
}
