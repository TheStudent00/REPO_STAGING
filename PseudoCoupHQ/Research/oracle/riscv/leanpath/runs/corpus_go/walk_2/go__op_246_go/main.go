// probe 246 -- binary &
package main

//go:noinline
func op_246(a int64, b int32) int64 {
	return a & b
}

var ga int64
var gb int32
var sink interface{}

func main() {
	sink = op_246(ga, gb)
	_ = sink
}
