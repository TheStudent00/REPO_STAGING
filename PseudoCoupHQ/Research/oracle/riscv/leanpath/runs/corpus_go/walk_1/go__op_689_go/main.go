// probe 689 -- binary &&
package main

//go:noinline
func op_689(a uint64, b bool) bool {
	return a && b
}

var ga uint64
var gb bool
var sink interface{}

func main() {
	sink = op_689(ga, gb)
	_ = sink
}
