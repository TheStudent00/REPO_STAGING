// probe 407 -- binary |
package main

//go:noinline
func op_407(a float32, b bool) float32 {
	return a | b
}

var ga float32
var gb bool
var sink interface{}

func main() {
	sink = op_407(ga, gb)
	_ = sink
}
