// probe 480 -- binary ==
package main

//go:noinline
func op_480(a float64, b int32) bool {
	return a == b
}

var ga float64
var gb int32
var sink interface{}

func main() {
	sink = op_480(ga, gb)
	_ = sink
}
