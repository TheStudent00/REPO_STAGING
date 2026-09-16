// probe 7 -- unary -
package main

//go:noinline
func op_7(a int64) int64 {
	return -a
}

var ga int64
var sink interface{}

func main() {
	sink = op_7(ga)
	_ = sink
}
