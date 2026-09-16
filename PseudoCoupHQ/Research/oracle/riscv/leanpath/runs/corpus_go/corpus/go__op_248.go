// probe 248 -- binary &
package main

//go:noinline
func op_248(a int64, b uint64) int64 {
	return a & b
}

var ga int64
var gb uint64
var sink interface{}

func main() {
	sink = op_248(ga, gb)
	_ = sink
}
