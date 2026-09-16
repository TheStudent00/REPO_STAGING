// probe 563 -- binary <
package main

//go:noinline
func op_563(a bool, b bool) bool {
	return a < b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_563(ga, gb)
	_ = sink
}
