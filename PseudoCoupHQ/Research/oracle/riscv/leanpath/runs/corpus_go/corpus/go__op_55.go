// probe 55 -- unary ...
package main

//go:noinline
func op_55(a int64) int64 {
	return a...
}

var ga int64
var sink interface{}

func main() {
	sink = op_55(ga)
	_ = sink
}
