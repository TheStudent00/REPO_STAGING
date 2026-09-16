// probe 78 -- binary *
package main

//go:noinline
func op_78(a float32, b int32) float32 {
	return a * b
}

var ga float32
var gb int32
var sink interface{}

func main() {
	sink = op_78(ga, gb)
	_ = sink
}
