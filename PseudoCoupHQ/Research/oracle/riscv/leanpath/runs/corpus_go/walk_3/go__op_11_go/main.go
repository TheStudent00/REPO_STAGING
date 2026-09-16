// probe 11 -- unary -
package main

//go:noinline
func op_11(a bool) bool {
	return -a
}

var ga bool
var sink interface{}

func main() {
	sink = op_11(ga)
	_ = sink
}
