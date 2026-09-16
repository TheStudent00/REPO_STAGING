// probe 527 -- binary !=
package main

//go:noinline
func op_527(a bool, b bool) bool {
	return a != b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_527(ga, gb)
	_ = sink
}
