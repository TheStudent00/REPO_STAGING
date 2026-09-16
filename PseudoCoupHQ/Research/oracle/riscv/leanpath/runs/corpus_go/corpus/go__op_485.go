// probe 485 -- binary ==
package main

//go:noinline
func op_485(a float64, b bool) bool {
	return a == b
}

var ga float64
var gb bool
var sink interface{}

func main() {
	sink = op_485(ga, gb)
	_ = sink
}
