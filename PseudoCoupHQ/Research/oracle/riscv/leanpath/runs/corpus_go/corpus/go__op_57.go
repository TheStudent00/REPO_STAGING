// probe 57 -- unary ...
package main

//go:noinline
func op_57(a float32) float32 {
	return a...
}

var ga float32
var sink interface{}

func main() {
	sink = op_57(ga)
	_ = sink
}
