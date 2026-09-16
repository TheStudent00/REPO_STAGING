// probe 288 -- binary &^
package main

//go:noinline
func op_288(a uint64, b int32) uint64 {
	return a &^ b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_288(ga, gb)
	_ = sink
}
