// probe 474 -- binary ==
package main

//go:noinline
func op_474(a float32, b int32) bool {
	return a == b
}

var ga float32
var gb int32
var sink interface{}

func main() {
	sink = op_474(ga, gb)
	_ = sink
}
