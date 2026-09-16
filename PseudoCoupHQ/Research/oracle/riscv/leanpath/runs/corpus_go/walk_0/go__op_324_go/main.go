// probe 324 -- binary +
package main

//go:noinline
func op_324(a uint64, b int32) uint64 {
	return a + b
}

var ga uint64
var gb int32
var sink interface{}

func main() {
	sink = op_324(ga, gb)
	_ = sink
}
