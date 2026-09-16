// probe 27 -- unary *
package main

//go:noinline
func op_27(a float32) float32 {
	return *a
}

var ga float32
var sink interface{}

func main() {
	sink = op_27(ga)
	_ = sink
}
