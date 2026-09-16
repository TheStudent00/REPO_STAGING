// probe 126 -- binary /
package main

//go:noinline
func op_126(a bool, b int32) bool {
	return a / b
}

var ga bool
var gb int32
var sink interface{}

func main() {
	sink = op_126(ga, gb)
	_ = sink
}
