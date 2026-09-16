// probe 42 -- unary ++
package main

//go:noinline
func op_42(a int32) int32 {
	return a++
}

var ga int32
var sink interface{}

func main() {
	sink = op_42(ga)
	_ = sink
}
