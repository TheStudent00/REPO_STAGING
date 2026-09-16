// probe 310 -- binary &^
package main

//go:noinline
func op_310(a bool, b float64) bool {
	return a &^ b
}

var ga bool
var gb float64
var sink interface{}

func main() {
	sink = op_310(ga, gb)
	_ = sink
}
