// probe 489 -- binary ==
package main

//go:noinline
func op_489(a bool, b float32) bool {
	return a == b
}

var ga bool
var gb float32
var sink interface{}

func main() {
	sink = op_489(ga, gb)
	_ = sink
}
