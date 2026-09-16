// probe 525 -- binary !=
package main

//go:noinline
func op_525(a bool, b float32) bool {
	return a != b
}

var ga bool
var gb float32
var sink interface{}

func main() {
	sink = op_525(ga, gb)
	_ = sink
}
