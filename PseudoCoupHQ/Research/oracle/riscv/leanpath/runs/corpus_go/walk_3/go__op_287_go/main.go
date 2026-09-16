// probe 287 -- binary &^
package main

//go:noinline
func op_287(a int64, b bool) int64 {
	return a &^ b
}

var ga int64
var gb bool
var sink interface{}

func main() {
	sink = op_287(ga, gb)
	_ = sink
}
