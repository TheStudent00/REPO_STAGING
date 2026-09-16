// probe 283 -- binary &^
package main

//go:noinline
func op_283(a int64, b int64) int64 {
	return a &^ b
}

var ga int64
var gb int64
var sink interface{}

func main() {
	sink = op_283(ga, gb)
	_ = sink
}
