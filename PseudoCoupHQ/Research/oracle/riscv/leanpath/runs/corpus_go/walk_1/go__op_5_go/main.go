// probe 5 -- unary +
package main

//go:noinline
func op_5(a bool) bool {
	return +a
}

var ga bool
var sink interface{}

func main() {
	sink = op_5(ga)
	_ = sink
}
