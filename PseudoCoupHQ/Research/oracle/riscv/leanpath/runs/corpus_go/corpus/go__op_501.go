// probe 501 -- binary !=
package main

//go:noinline
func op_501(a int64, b float32) bool {
	return a != b
}

var ga int64
var gb float32
var sink interface{}

func main() {
	sink = op_501(ga, gb)
	_ = sink
}
