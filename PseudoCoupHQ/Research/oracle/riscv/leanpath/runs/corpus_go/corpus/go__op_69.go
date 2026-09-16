// probe 69 -- binary *
package main

//go:noinline
func op_69(a int64, b float32) int64 {
	return a * b
}

var ga int64
var gb float32
var sink interface{}

func main() {
	sink = op_69(ga, gb)
	_ = sink
}
