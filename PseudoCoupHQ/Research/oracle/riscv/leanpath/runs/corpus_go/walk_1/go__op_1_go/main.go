// probe 1 -- unary +
package main

//go:noinline
func op_1(a int64) int64 {
	return +a
}

var ga int64
var sink interface{}

func main() {
	sink = op_1(ga)
	_ = sink
}
