// probe 12 -- unary !
package main

//go:noinline
func op_12(a int32) bool {
	return !a
}

var ga int32
var sink interface{}

func main() {
	sink = op_12(ga)
	_ = sink
}
