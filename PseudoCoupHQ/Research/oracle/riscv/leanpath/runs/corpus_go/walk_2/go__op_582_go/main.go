// probe 582 -- binary <=
package main

//go:noinline
func op_582(a float32, b int32) bool {
	return a <= b
}

var ga float32
var gb int32
var sink interface{}

func main() {
	sink = op_582(ga, gb)
	_ = sink
}
