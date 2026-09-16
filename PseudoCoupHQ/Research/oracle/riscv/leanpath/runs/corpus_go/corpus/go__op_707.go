// probe 707 -- binary &&
package main

//go:noinline
func op_707(a bool, b bool) bool {
	return a && b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_707(ga, gb)
	_ = sink
}
