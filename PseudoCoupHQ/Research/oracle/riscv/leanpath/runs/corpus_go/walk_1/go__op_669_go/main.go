// probe 669 -- binary >=
package main

//go:noinline
func op_669(a bool, b float32) bool {
	return a >= b
}

var ga bool
var gb float32
var sink interface{}

func main() {
	sink = op_669(ga, gb)
	_ = sink
}
