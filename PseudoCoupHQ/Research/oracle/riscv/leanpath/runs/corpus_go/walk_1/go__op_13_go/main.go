// probe 13 -- unary !
package main

//go:noinline
func op_13(a int64) bool {
	return !a
}

var ga int64
var sink interface{}

func main() {
	sink = op_13(ga)
	_ = sink
}
