// probe 23 -- unary ^
package main

//go:noinline
func op_23(a bool) bool {
	return ^a
}

var ga bool
var sink interface{}

func main() {
	sink = op_23(ga)
	_ = sink
}
