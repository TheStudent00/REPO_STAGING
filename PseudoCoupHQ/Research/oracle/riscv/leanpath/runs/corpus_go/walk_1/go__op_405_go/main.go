// probe 405 -- binary |
package main

//go:noinline
func op_405(a float32, b float32) float32 {
	return a | b
}

var ga float32
var gb float32
var sink interface{}

func main() {
	sink = op_405(ga, gb)
	_ = sink
}
