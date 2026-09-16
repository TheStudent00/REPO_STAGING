// probe 25 -- unary *
package main

//go:noinline
func op_25(a int64) int64 {
	return *a
}

var ga int64
var sink interface{}

func main() {
	sink = op_25(ga)
	_ = sink
}
