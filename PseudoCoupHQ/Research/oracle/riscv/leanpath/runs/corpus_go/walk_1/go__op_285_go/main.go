// probe 285 -- binary &^
package main

//go:noinline
func op_285(a int64, b float32) int64 {
	return a &^ b
}

var ga int64
var gb float32
var sink interface{}

func main() {
	sink = op_285(ga, gb)
	_ = sink
}
