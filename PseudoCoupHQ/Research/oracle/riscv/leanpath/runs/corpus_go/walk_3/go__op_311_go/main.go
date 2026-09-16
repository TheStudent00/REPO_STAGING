// probe 311 -- binary &^
package main

//go:noinline
func op_311(a bool, b bool) bool {
	return a &^ b
}

var ga bool
var gb bool
var sink interface{}

func main() {
	sink = op_311(ga, gb)
	_ = sink
}
