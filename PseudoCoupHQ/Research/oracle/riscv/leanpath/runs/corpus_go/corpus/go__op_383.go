// probe 383 -- binary -
package main

//go:noinline
func op_383(a bool, b bool) bool {
	return a - b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_383(ga, gb)
	_ = sink
}
