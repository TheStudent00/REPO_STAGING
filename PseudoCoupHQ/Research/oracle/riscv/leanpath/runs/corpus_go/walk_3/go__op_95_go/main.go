// probe 95 -- binary *
package main

//go:noinline
func op_95(a bool, b bool) bool {
	return a * b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_95(ga, gb)
	_ = sink
}
