// probe 488 -- binary ==
package main

//go:noinline
func op_488(a bool, b uint64) bool {
	return a == b
}

var ga bool
var gb uint64
var sink interface{}

func main() {
	sink = op_488(ga, gb)
	_ = sink
}
