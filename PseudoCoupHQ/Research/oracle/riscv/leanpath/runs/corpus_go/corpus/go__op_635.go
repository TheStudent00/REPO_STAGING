// probe 635 -- binary >
package main

//go:noinline
func op_635(a bool, b bool) bool {
	return a > b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_635(ga, gb)
	_ = sink
}
