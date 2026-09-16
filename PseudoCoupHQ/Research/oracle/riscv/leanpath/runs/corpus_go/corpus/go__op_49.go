// probe 49 -- unary --
package main

//go:noinline
func op_49(a int64) int64 {
	return a--
}

var ga int64
var sink interface{}

func main() {
	sink = op_49(ga)
	_ = sink
}
