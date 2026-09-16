// probe 59 -- unary ...
package main

//go:noinline
func op_59(a bool) bool {
	return a...
}

var ga bool
var sink interface{}

func main() {
	sink = op_59(ga)
	_ = sink
}
