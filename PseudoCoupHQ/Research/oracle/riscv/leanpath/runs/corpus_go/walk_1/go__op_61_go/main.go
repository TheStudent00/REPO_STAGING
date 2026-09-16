// probe 61 -- binary *
package main

//go:noinline
func op_61(a int32, b int64) int32 {
	return a * b
}

var ga int32
var gb int64
var sink interface{}

func main() {
	sink = op_61(ga, gb)
	_ = sink
}
