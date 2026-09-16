// probe 276 -- binary &^
package main

//go:noinline
func op_276(a int32, b int32) int32 {
	return a &^ b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = op_276(ga, gb)
	_ = sink
}
