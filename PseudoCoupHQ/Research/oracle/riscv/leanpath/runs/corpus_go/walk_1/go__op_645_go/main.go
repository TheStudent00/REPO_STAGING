// probe 645 -- binary >=
package main

//go:noinline
func op_645(a int64, b float32) bool {
	return a >= b
}

var ga int64
var gb float32
var sink interface{}

func main() {
	sink = op_645(ga, gb)
	_ = sink
}
