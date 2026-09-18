// probe 491 -- binary ==
package main

//go:noinline
func op_491(a bool, b bool) bool {
	return a == b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_491(ga, gb)
	_ = sink
}
