// probe 9 -- unary -
package main

//go:noinline
func op_9(a float32) float32 {
	return -a
}

var ga float32
var sink interface{}

func main() {
	sink = op_9(ga)
	_ = sink
}
