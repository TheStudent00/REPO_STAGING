// probe 599 -- binary <=
package main

//go:noinline
func op_599(a bool, b bool) bool {
	return a <= b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_599(ga, gb)
	_ = sink
}
