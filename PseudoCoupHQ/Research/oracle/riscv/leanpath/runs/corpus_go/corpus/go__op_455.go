// probe 455 -- binary ^
package main

//go:noinline
func op_455(a bool, b bool) bool {
	return a ^ b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_455(ga, gb)
	_ = sink
}
