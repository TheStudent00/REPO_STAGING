// probe 17 -- unary !
package main

//go:noinline
func op_17(a bool) bool {
	return !a
}

var ga bool
var sink interface{}

func main() {
	sink = op_17(ga)
	_ = sink
}
