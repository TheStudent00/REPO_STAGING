// probe 90 -- binary *
package main

//go:noinline
func op_90(a bool, b int32) bool {
	return a * b
}

var ga bool
var gb int32
var sink interface{}

func main() {
	sink = op_90(ga, gb)
	_ = sink
}
