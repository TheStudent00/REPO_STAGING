// probe 66 -- binary *
package main

//go:noinline
func op_66(a int64, b int32) int64 {
	return a * b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_66(ga, gb)
	_ = sink
}
