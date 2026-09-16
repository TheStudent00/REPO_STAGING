// probe 48 -- unary --
package main

//go:noinline
func op_48(a int32) int32 {
	return a--
}

var ga int32
var sink interface{}

func main() {
	sink = op_48(ga)
	_ = sink
}
